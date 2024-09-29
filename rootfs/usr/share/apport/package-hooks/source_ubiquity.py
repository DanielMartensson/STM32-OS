"""Apport package hook for the ubiquity live CD installer.

Copyright (C) 2009 Canonical Ltd.
Authors: Colin Watson <cjwatson@ubuntu.com>,
         Brian Murray <brian@ubuntu.com>
"""  # noqa: D208

import os.path
import pathlib
import re

import apport.hookutils


def _add_installation_log(report, ident, name):
    log_file = False
    for try_location in ("/var/log/installer/%s", "/var/log/%s", "/var/log/upstart/%s"):
        if os.path.exists(try_location % name):
            log_file = try_location % name
            break
    if not log_file:
        return

    if os.access(log_file, os.R_OK):
        report[ident] = pathlib.Path(log_file).read_text("UTF-8", "replace")
    elif os.path.exists(log_file):
        apport.hookutils.attach_root_command_outputs(
            report, {ident: f"cat '{log_file}'"}
        )

    if ident in report and isinstance(report[ident], bytes):
        try:
            report[ident] = report[ident].decode("UTF-8", "replace")
        except (UnicodeDecodeError, KeyError):
            pass


def _prepare_duplicate_signature(syslog, collect_grub, collect_trace):
    collect = ""
    for line in syslog.split("\n"):
        if collect_grub:
            if "grub-installer:" in line and collect == "":
                collect = " ".join(line.split(" ")[4:]) + "\n"
                continue
            if "grub-installer:" in line and collect != "":
                collect += " ".join(line.split(" ")[4:]) + "\n"
                continue
        if not collect_trace and collect != "":
            return collect
        if "Traceback (most recent call last):" in line and collect_grub:
            collect += " ".join(line.split(" ")[5:]) + "\n"
            continue
        if "Traceback (most recent call last):" in line and not collect_grub:
            collect = " ".join(line.split(" ")[5:]) + "\n"
            continue
        if len(line.split(" ")[5:]) == 1 and "Traceback" in collect:
            if collect != "":
                return collect
        if "Traceback" not in collect:
            continue
        collect += " ".join(line.split(" ")[5:]) + "\n"
    return None


# TODO: Split into smaller functions/methods
# pylint: disable-next=too-many-branches,too-many-locals,too-many-statements
def add_info(report, ui):
    """Add information for ubiquity live CD installer."""
    _add_installation_log(report, "UbiquitySyslog", "syslog")
    syslog = report["UbiquitySyslog"]
    if "Buffer I/O error on device" in syslog:
        if re.search("Attached .* CD-ROM (\\w+)", syslog):
            cd_drive = re.search("Attached .* CD-ROM (\\w+)", syslog).group(1)
            cd_error = re.search(f"Buffer I/O error on device {cd_drive}", syslog)
        else:
            cd_error = None
        if cd_error:
            ui.information(
                "The system log from your installation contains an error.  The"
                " specific error commonly occurs when there is an issue with"
                " the media from which you were installing.  This can happen"
                " when your media is dirty or damaged or when you've burned"
                " the media at a high speed.  Please try cleaning the media"
                " and or burning new media at a lower speed.  In the event"
                " that you continue to encounter these errors it may be an"
                " issue with your CD / DVD drive."
            )
            raise StopIteration
    if "I/O error, dev" in syslog:
        # check for either usb stick (install media) or hard disk I/O errors
        if re.search("I/O error, dev (\\w+)", syslog):
            error_disk = re.search("I/O error, dev (\\w+)", syslog).group(1)
            mount = apport.hookutils.command_output(
                ["grep", error_disk, "/proc/mounts"]
            )
            if "target" in mount:
                ui.information(
                    "The system log from your installation contains an error."
                    "  The specific error commonly occurs when there is an"
                    " issue with the disk to which you are trying to install"
                    " Ubuntu.  It is recommended that you back up important"
                    " data on your disk and investigate the situation."
                    "  Measures you might take include checking cable"
                    " connections for your disks and using software tools to"
                    " investigate the health of your hardware."
                )
                raise StopIteration
            if "cdrom" in mount:
                ui.information(
                    "The system log from your installation contains an error."
                    "  The specific error commonly occurs when there is an"
                    " issue with the media from which you were installing."
                    "  Please try creating the USB stick you were installing"
                    " from again or try installing from a different USB stick."
                )
                raise StopIteration
    if "SQUASHFS error: Unable to read" in syslog:
        ui.information(
            "The system log from your installation contains an error.  The"
            " specific error commonly occurs when there is an issue with the"
            " media from which you were installing.  This can happen when your"
            " media is dirty or damaged or when you've burned the media at a"
            " high speed.  Please try cleaning the media and or burning new"
            " media at a lower speed.  In the event that you continue to"
            " encounter these errors it may be an issue with your CD / DVD"
            " drive."
        )
        raise StopIteration

    if "Kernel command line" in syslog:
        install_cmdline = re.search("Kernel command line: (.*)", syslog).group(1)
    else:
        install_cmdline = None
    if install_cmdline:
        report["InstallCmdLine"] = install_cmdline

    if "Traceback" not in report:
        collect_grub = False
        collect_trace = False
        if (
            "grub-install ran successfully" not in syslog
            and "grub-installer:" in syslog
        ):
            collect_grub = True
        if "Traceback" in syslog:
            collect_trace = True
        if (
            report["ProblemType"] != "Bug"
            and collect_grub
            or report["ProblemType"] != "Bug"
            and collect_trace
        ):
            duplicate_signature = _prepare_duplicate_signature(
                syslog, collect_grub, collect_trace
            )
            if duplicate_signature:
                report["DuplicateSignature"] = duplicate_signature
        if collect_grub:
            report["SourcePackage"] = "grub-installer"

    match = re.search("ubiquity.*Ubiquity (.*)\n", syslog)
    if match:
        match = match.group(1)
    report.setdefault("Tags", "")
    if match:
        report["Tags"] += f" ubiquity-{match.split()[0]}"

    # tag bug reports where people choose to "upgrade" their install of Ubuntu
    if re.search("UpgradeSystem\\(\\) was called with safe mode", syslog):
        report["Tags"] += " ubiquity-upgrade"

    _add_installation_log(report, "UbiquityPartman", "partman")

    debug_log = "/var/log/installer/debug"
    debug_mode = False
    if os.path.exists(debug_log):
        try:
            debug_log_fp = open(debug_log, "r", encoding="utf-8")
        except (OSError, IOError):
            pass
        else:
            with debug_log_fp:
                for line in debug_log_fp:
                    if line.startswith("debconf (developer)"):
                        debug_mode = True
                        break
            if debug_mode:
                response = ui.yesno(
                    "The debug log file from your installation would help us"
                    " a lot but includes the password you used for your user"
                    " when installing Ubuntu.  Do you want to include this"
                    " log file?"
                )
                if response is None:
                    raise StopIteration
                if response:
                    _add_installation_log(report, "UbiquityDebug", "debug")
            else:
                _add_installation_log(report, "UbiquityDebug", "debug")

    _add_installation_log(report, "UbiquityDm", "dm")
    _add_installation_log(report, "UpstartUbiquity", "ubiquity.log")

    # add seed name as Tag so we know which image was used
    cmdline = pathlib.Path("/proc/cmdline").read_text(encoding="utf-8")
    match = re.search("([^/]+)\\.seed", cmdline)
    if match:
        report["Tags"] += " " + match.group(1)

    _add_installation_log(report, "Casper", "casper.log")
    _add_installation_log(report, "OemConfigLog", "oem-config.log")
    if "OemConfigLog" in report:
        report["Tags"] += " oem-config"
