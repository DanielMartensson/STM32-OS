"""Attach generally useful information, not specific to any package.

Copyright (C) 2009 Canonical Ltd.
Authors: Matt Zimmerman <mdz@canonical.com>,
         Brian Murray <brian@ubuntu.com>

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
the full text of the license.
"""

import os
import pathlib
import platform
import re
import subprocess
import sys
import time
from gettext import gettext as _
from glob import glob

import apport.hookutils
import apport.packaging
import problem_report


def add_info(report, ui):
    # TODO: Split into smaller functions/methods
    # pylint: disable=invalid-name,too-many-branches,too-many-locals,too-many-statements
    # pylint: disable=too-many-nested-blocks
    """Attach generally useful information, not specific to any package."""
    _add_release_info(report)
    _add_kernel_info(report)
    add_proposed_info(report)

    # collect a condensed version of /proc/cpuinfo
    apport.hookutils.attach_file(report, "/proc/cpuinfo", "ProcCpuinfo")
    short_cpuinfo = []
    for item in reversed(report.get("ProcCpuinfo", "").split("\n")):
        short_cpuinfo.append(item)
        if item.startswith("processor\t:"):
            break
    short_cpuinfo = reversed(short_cpuinfo)
    report["ProcCpuinfoMinimal"] = "\n".join(short_cpuinfo)
    report.pop("ProcCpuinfo")

    hook_errors = [k for k in report.keys() if k.startswith("HookError_")]
    if hook_errors:
        report.add_tags(["apport-hook-error"])

    # locally installed python versions can cause a multitude of errors
    if (
        report.get("ProblemType") == "Package"
        or "python" in report.get("InterpreterPath", "")
        or "python" in report.get("ExecutablePath", "")
    ):
        for python in ("python", "python3"):
            add_python_details(f"{python.title()}Details", python, report)

    try:
        report["ApportVersion"] = apport.packaging.get_version("apport")
    except ValueError:
        # might happen on local installs
        pass

    # We want to know if people have modified apport's crashdb.conf in case
    # crashes are reported to Launchpad when they shouldn't be e.g. for a
    # non-development release.
    apport.hookutils.attach_conffiles(report, "apport", ui=ui)

    # Should the system have been rebooted?
    apport.hookutils.attach_file_if_exists(
        report, "/var/run/reboot-required.pkgs", "RebootRequiredPkgs"
    )

    casper_md5check = "casper-md5check.json"
    if "LiveMediaBuild" in report:
        apport.hookutils.attach_casper_md5check(report, f"/run/{casper_md5check}")
    else:
        apport.hookutils.attach_casper_md5check(
            report, f"/var/log/installer/{casper_md5check}"
        )

    if report.get("ProblemType") == "Package":
        # every error report regarding a package should have package manager
        # version information
        apport.hookutils.attach_related_packages(report, ["dpkg", "apt"])
        _check_for_disk_error(report)
        # check to see if the real root on a persistent media is full
        if "LiveMediaBuild" in report:
            st = os.statvfs("/cdrom")
            free_mb = st.f_bavail * st.f_frsize / 1000000
            if free_mb < 10:
                report["UnreportableReason"] = (
                    f"Your system partition has less than {free_mb} MB"
                    f" of free space available, which leads to problems"
                    f" using applications and installing updates."
                    f" Please free some space."
                )

    _match_error_messages(report)

    # these attachments will not exist if ProblemType is Bug as the package
    # hook runs after the general hook
    for attachment in ("DpkgTerminalLog", "VarLogDistupgradeApttermlog"):
        if attachment in report:
            log_file = _get_attachment_contents(report, attachment)
            untrimmed_dpkg_log = log_file
            _check_attachment_for_errors(report, attachment)
            trimmed_log = _get_attachment_contents(report, attachment)
            trimmed_log = trimmed_log.split("\n")
            lines = []
            for line in untrimmed_dpkg_log.splitlines():
                if line not in trimmed_log:
                    lines.append(str(line))
                elif line in trimmed_log:
                    trimmed_log.remove(line)
            dpkg_log_without_error = "\n".join(lines)

    # crash reports from live system installer often expose target mount
    for f in ("ExecutablePath", "InterpreterPath"):
        if f in report and report[f].startswith("/target/"):
            report[f] = report[f][7:]

    # Allow filing update-manager bugs with obsolete packages
    if report.get("Package", "").startswith("update-manager"):
        os.environ["APPORT_IGNORE_OBSOLETE_PACKAGES"] = "1"

    # file bugs against OEM project for modified packages
    if "Package" in report:
        v = report["Package"].split()[1]
        oem_project = get_oem_project(report)
        if oem_project and ("common" in v or oem_project in v):
            report["CrashDB"] = "canonical-oem"

    if "Package" in report:
        package = report["Package"].split()[0]
        if package:
            apport.hookutils.attach_conffiles(report, package, ui=ui)

        # do not file bugs against "upgrade-system" if it is not installed
        # (LP#404727)
        if package == "upgrade-system" and "not installed" in report["Package"]:
            report["UnreportableReason"] = (
                "You do not have the upgrade-system package installed."
                " Please report package upgrade failures against the package"
                " that failed to install, or against upgrade-manager."
            )

    # build a duplicate signature tag for package reports
    if report.get("ProblemType") == "Package":
        if "DpkgTerminalLog" in report:
            # this was previously trimmed in check_attachment_for_errors
            termlog = report["DpkgTerminalLog"]
        elif "VarLogDistupgradeApttermlog" in report:
            termlog = _get_attachment_contents(report, "VarLogDistupgradeApttermlog")
        else:
            termlog = None
        if termlog:
            (package, version) = report["Package"].split(None, 1)
            # for packages that run update-grub include /etc/default/grub
            UPDATE_BOOT = [
                "friendly-recovery",
                "linux",
                "memtest86+",
                "plymouth",
                "ubuntu-meta",
                "virtualbox-ose",
            ]
            ug_failure = (
                r"/etc/kernel/post(inst|rm)\.d/"
                r"zz-update-grub exited with return code [1-9]+"
            )
            mkconfig_failure = (
                r"/usr/sbin/grub-mkconfig.*/etc/default/grub: Syntax error"
            )
            if re.search(ug_failure, termlog) or re.search(mkconfig_failure, termlog):
                if report["SourcePackage"] in UPDATE_BOOT:
                    apport.hookutils.attach_default_grub(report, "EtcDefaultGrub")
            dupe_sig = ""
            dupe_sig_created = False
            # messages we expect to see from a package manager (LP: #1692127)
            pkg_mngr_msgs = re.compile(
                r"^(Authenticating|De-configuring|Examining|Installing"
                r"|Preparing|Processing triggers|Purging|Removing|Replaced"
                r"|Replacing|Setting up|Unpacking|Would remove).*\.\.\.\s*$"
            )
            for line in termlog.split("\n"):
                if pkg_mngr_msgs.search(line):
                    dupe_sig = f"{line}\n"
                    dupe_sig_created = True
                    continue
                dupe_sig += f"{line}\n"
                # this doesn't catch 'dpkg-divert: error' LP: #1581399
                if "dpkg: error" in dupe_sig and line.startswith(" "):
                    if "trying to overwrite" in line:
                        conflict_pkg = re.search("in package (.*) ", line)
                        if conflict_pkg and not apport.packaging.is_distro_package(
                            conflict_pkg.group(1)
                        ):
                            report["UnreportableReason"] = _(
                                "An Ubuntu package has a file conflict with a "
                                "package that is not a genuine Ubuntu package."
                            )
                        report.add_tags(["package-conflict"])
                    if dupe_sig_created:
                        # the duplicate signature should be the first failure
                        report["DuplicateSignature"] = (
                            f"package:{package}:{version}\n{dupe_sig}"
                        )
                        break
                if dupe_sig:
                    if dpkg_log_without_error.find(dupe_sig) != -1:
                        report["UnreportableReason"] = _(
                            "You have already encountered this package"
                            " installation failure."
                        )


def _match_error_messages(report):
    # There are enough of these now that it is probably worth refactoring...
    # -mdz
    if report.get("ProblemType") == "Package":
        if "failed to install/upgrade: corrupted filesystem tarfile" in report.get(
            "Title", ""
        ):
            report["UnreportableReason"] = (
                "This failure was caused by a corrupted package download"
                " or file system corruption."
            )

        if "is already installed and configured" in report.get("ErrorMessage", ""):
            report["SourcePackage"] = "dpkg"


def _check_attachment_for_errors(report, attachment):
    # TODO: Split into smaller functions/methods
    # pylint: disable=too-many-branches,too-many-statements,too-many-nested-blocks
    if report.get("ProblemType") == "Package":
        wrong_grub_msg = _(
            """\
Your system was initially configured with grub version 2, but you have\
 removed it from your system in favor of grub 1 without configuring it.\
 To ensure your bootloader configuration is updated whenever a new kernel\
 is available, open a terminal and run:

      sudo apt-get install grub-pc
"""
        )

        trim_dpkg_log(report)
        log_file = _get_attachment_contents(report, attachment)

        grub_hook_failure = "DpkgTerminalLog" in report and bool(
            re.search(
                r"^Not creating /boot/grub/menu.lst as you wish",
                report["DpkgTerminalLog"],
                re.MULTILINE,
            )
        )

        if report["Package"] not in ["grub", "grub2"]:
            # linux-image postinst emits this when update-grub fails
            # https://wiki.ubuntu.com/KernelTeam/DebuggingUpdateErrors
            grub_errors = [
                r"^User postinst hook script \[.*update-grub\] exited with value",
                r"^run-parts: /etc/kernel/post(inst|rm).d"
                r"/zz-update-grub exited with return code [1-9]+",
                r"^/usr/sbin/grub-probe: error",
            ]

            for grub_error in grub_errors:
                if attachment in report and re.search(
                    grub_error, log_file, re.MULTILINE
                ):
                    # File these reports on the grub package instead
                    grub_package = apport.packaging.get_file_package(
                        "/usr/sbin/update-grub"
                    )
                    if (
                        grub_package is None
                        or grub_package == "grub"
                        and "grub-probe" not in log_file
                    ):
                        report["SourcePackage"] = "grub"
                        if os.path.exists("/boot/grub/grub.cfg") and grub_hook_failure:
                            report["UnreportableReason"] = wrong_grub_msg
                    else:
                        report["SourcePackage"] = "grub2"

        if report["Package"] != "initramfs-tools":
            # update-initramfs emits this when it fails, usually invoked
            # from the linux-image postinst
            # https://wiki.ubuntu.com/KernelTeam/DebuggingUpdateErrors
            if attachment in report and re.search(
                r"^update-initramfs: failed for ", log_file, re.MULTILINE
            ):
                # File these reports on the initramfs-tools package instead
                report["SourcePackage"] = "initramfs-tools"

        if report["Package"].startswith("linux-image-") and attachment in report:
            # /etc/kernel/*.d failures from kernel package postinst
            match = re.search(
                r"^run-parts: (/etc/kernel/\S+\.d/\S+) exited with return code \d+",
                log_file,
                re.MULTILINE,
            )
            if match:
                path = match.group(1)
                package = apport.packaging.get_file_package(path)
                if package:
                    report["SourcePackage"] = package
                    report["ErrorMessage"] = match.group(0)
                    if package == "grub-pc" and grub_hook_failure:
                        report["UnreportableReason"] = wrong_grub_msg
                else:
                    report["UnreportableReason"] = (
                        "This failure was caused by a program"
                        " which did not originate from Ubuntu"
                    )

        error_message = report.get("ErrorMessage")
        corrupt_package = (
            "This failure was caused by a corrupted package download"
            " or file system corruption."
        )
        out_of_memory = "This failure was caused by the system running out of memory."

        if "failed to install/upgrade: corrupted filesystem tarfile" in report.get(
            "Title", ""
        ):
            report["UnreportableReason"] = corrupt_package

        if "dependency problems - leaving unconfigured" in error_message:
            report["UnreportableReason"] = (
                "This failure is a followup error from a previous"
                " package install failure."
            )

        if "failed to allocate memory" in error_message:
            report["UnreportableReason"] = out_of_memory

        if "cannot access archive" in error_message:
            report["UnreportableReason"] = corrupt_package

        if re.search(
            r"(failed to read|failed in write|short read) on buffer copy", error_message
        ):
            report["UnreportableReason"] = corrupt_package

        if re.search(
            r"(failed to read|failed to write|failed to seek"
            r"|unexpected end of file or stream)",
            error_message,
        ):
            report["UnreportableReason"] = corrupt_package

        if re.search(
            r"(--fsys-tarfile|dpkg-deb --control) returned error exit status 2",
            error_message,
        ):
            report["UnreportableReason"] = corrupt_package

        if attachment in report and re.search(
            r"dpkg-deb: error.*is not a debian format archive", log_file, re.MULTILINE
        ):
            report["UnreportableReason"] = corrupt_package

        if "is already installed and configured" in report.get("ErrorMessage", ""):
            # there is insufficient information in the data currently gathered
            # so gather more data
            report["SourcePackage"] = "dpkg"
            report["AptdaemonVersion"] = apport.packaging.get_version("aptdaemon")
            apport.hookutils.attach_file_if_exists(
                report, "/var/log/dpkg.log", "DpkgLog"
            )
            apport.hookutils.attach_file_if_exists(
                report, "/var/log/apt/term.log", "AptTermLog"
            )
            # gather filenames in /var/crash to see if there is one for dpkg
            reports = glob("/var/crash/*")
            if reports:
                report["CrashReports"] = apport.hookutils.command_output(
                    ["stat", "-c", "%a:%u:%g:%s:%y:%x:%n"] + reports
                )
            report.add_tags(["already-installed"])


def _check_for_disk_error(report):
    devs_to_check = []
    if "Dmesg.txt" not in report and "CurrentDmesg.txt" not in report:
        return
    if "Df.txt" not in report:
        return
    df_output = report["Df.txt"]
    device_error = False
    for line in df_output:
        line = line.strip("\n")
        if line.endswith("/") or line.endswith("/usr") or line.endswith("/var"):
            # without manipulation it'd look like /dev/sda1
            device = line.split(" ")[0].strip("0123456789")
            device = device.replace("/dev/", "")
            devs_to_check.append(device)
    dmesg = report.get("CurrentDmesg.txt", report["Dmesg.txt"])
    for line in dmesg:
        line = line.strip("\n")
        if "I/O error" in line:
            # no device in this line
            if "journal commit I/O error" in line:
                continue
            for dev in devs_to_check:
                if re.search(dev, line):
                    error_device = dev
                    device_error = True
                    break
    if device_error:
        report["UnreportableReason"] = (
            f"This failure was caused by a hardware error on /dev/{error_device}"
        )


def _add_kernel_info(report):
    # This includes the Ubuntu packaged kernel version
    apport.hookutils.attach_file_if_exists(
        report, "/proc/version_signature", "ProcVersionSignature"
    )


def _add_release_info(report):
    # https://bugs.launchpad.net/bugs/364649
    media = "/var/log/installer/media-info"
    apport.hookutils.attach_file_if_exists(report, media, "InstallationMedia")
    # Preinstalled Raspberry Pi images include a build date breadcrumb
    apport.hookutils.attach_file_if_exists(report, "/.disk/info", "ImageMediaBuild")
    if "ImageMediaBuild" in report:
        report.add_tags([f"{report['Architecture']}-image"])
        try:
            compatible = pathlib.Path("/proc/device-tree/compatible").read_bytes()
            is_a_pi = any(
                vendor == "raspberrypi"
                for s in compatible.split(b"\0")
                if s
                for vendor, model in (s.decode("ascii").split(",", 1),)
            )
        except FileNotFoundError:
            is_a_pi = False
        if is_a_pi:
            report.add_tags(["raspi-image"])

    # if we are running from a live system, add the build timestamp
    apport.hookutils.attach_file_if_exists(
        report, "/cdrom/.disk/info", "LiveMediaBuild"
    )
    if os.path.exists("/cdrom/.disk/info"):
        report["CasperVersion"] = apport.packaging.get_version("casper")

    # https://wiki.ubuntu.com/FoundationsTeam/Specs/OemTrackingId
    apport.hookutils.attach_file_if_exists(
        report, "/var/lib/ubuntu_dist_channel", "DistributionChannelDescriptor"
    )

    os_release = platform.freedesktop_os_release()
    release_codename = os_release.get("VERSION_CODENAME")
    if release_codename:
        report.add_tags([release_codename])

    if os.path.exists(media):
        mtime = os.stat(media).st_mtime
        human_mtime = time.strftime("%Y-%m-%d", time.gmtime(mtime))
        delta = time.time() - mtime
        report["InstallationDate"] = (
            f"Installed on {human_mtime} ({round(delta / 86400)} days ago)"
        )

    log = "/var/log/dist-upgrade/main.log"
    if os.path.exists(log):
        mtime = os.stat(log).st_mtime
        human_mtime = time.strftime("%Y-%m-%d", time.gmtime(mtime))
        delta = time.time() - mtime

        # Would be nice if this also showed which release was originally
        # installed
        report["UpgradeStatus"] = (
            f"Upgraded to {release_codename} on {human_mtime}"
            f" ({round(delta / 86400)} days ago)"
        )
    else:
        report["UpgradeStatus"] = "No upgrade log present (probably fresh install)"


def add_proposed_info(report):
    """Tag if package comes from -proposed."""
    if "Package" not in report:
        return
    try:
        (package, version) = report["Package"].split()[:2]
    except ValueError:
        print("WARNING: malformed Package field: " + report["Package"])
        return

    apt_cache = subprocess.run(
        ["apt-cache", "showpkg", package],
        check=False,
        stdout=subprocess.PIPE,
        text=True,
    )
    if apt_cache.returncode != 0:
        print(f"WARNING: apt-cache showpkg {package} failed")
        return

    found_proposed = False
    found_updates = False
    found_security = False
    for line in apt_cache.stdout.splitlines():
        if line.startswith(version + " ("):
            if "-proposed_" in line:
                found_proposed = True
            if "-updates_" in line:
                found_updates = True
            if "-security" in line:
                found_security = True

    if found_proposed and not found_updates and not found_security:
        report.add_tags(["package-from-proposed"])


def get_oem_project(report):
    """Determine OEM project name from Distribution Channel Descriptor.

    Return None if it cannot be determined or does not exist.
    """
    dcd = report.get("DistributionChannelDescriptor", None)
    if dcd and dcd.startswith("canonical-oem-"):
        return dcd.split("-")[2]
    return None


def trim_dpkg_log(report):
    """Trim DpkgTerminalLog to the most recent installation session."""
    if "DpkgTerminalLog" not in report:
        return
    if not report["DpkgTerminalLog"].strip():
        report["UnreportableReason"] = "/var/log/apt/term.log does not contain any data"
        return
    lines = []
    dpkg_log = report["DpkgTerminalLog"]
    if isinstance(dpkg_log, bytes):
        trim_re = re.compile(b"^\\(.* ... \\d+ .*\\)$")
        start_re = re.compile(b"^Log started:")
    else:
        trim_re = re.compile("^\\(.* ... \\d+ .*\\)$")
        start_re = re.compile("^Log started:")
    for line in dpkg_log.splitlines():
        if start_re.match(line) or trim_re.match(line):
            lines = []
            continue
        lines.append(line)
    # If trimming the log file fails, return the whole log file.
    if not lines:
        return
    if isinstance(lines[0], str):
        report["DpkgTerminalLog"] = "\n".join(lines)
    else:
        report["DpkgTerminalLog"] = "\n".join(
            [str(line.decode("UTF-8", "replace")) for line in lines]
        )


def _get_attachment_contents(report, attachment):
    if isinstance(report[attachment], problem_report.CompressedValue):
        contents = report[attachment].get_value().decode("UTF-8")
    else:
        contents = report[attachment]
    return contents


def add_python_details(key, python, report):
    """Add comma separated details about which python is being used"""
    python_path = apport.hookutils.command_output(["which", python])
    if python_path.startswith("Error: "):
        report[key] = "N/A"
        return
    python_link = apport.hookutils.command_output(["readlink", "-f", python_path])
    python_pkg = apport.fileutils.find_file_package(python_path)
    if python_pkg:
        python_pkg_version = apport.packaging.get_version(python_pkg)
    python_version = apport.hookutils.command_output([python_link, "--version"])
    data = f"{python_link}, {python_version}"
    if python_pkg:
        data += f", {python_pkg}, {python_pkg_version}"
    else:
        data += ", unpackaged"
    report[key] = data


def main():  # pylint: disable=missing-function-docstring
    # for testing: update report file given on command line
    if len(sys.argv) != 2:
        sys.stderr.write(f"Usage for testing this hook: {sys.argv[0]} <report file>\n")
        sys.exit(1)

    report_file = sys.argv[1]

    report = apport.Report()
    with open(report_file, "rb") as report_fd:
        report.load(report_fd)
    report_keys = set(report.keys())

    new_report = report.copy()
    add_info(new_report, None)

    new_report_keys = set(new_report.keys())

    # Show differences
    # N.B. Some differences will exist if the report file is not from your
    # system because the hook runs against your local system.
    changed = 0
    for key in sorted(report_keys | new_report_keys):
        if key in new_report_keys and key not in report_keys:
            print(f"+{key}: {new_report[key]}")
            changed += 1
        elif key in report_keys and key not in new_report_keys:
            print(f"-{key}: (deleted)")
            changed += 1
        elif key in report_keys and key in new_report_keys:
            if report[key] != new_report[key]:
                print(f"~{key}: (changed)")
                changed += 1
    print(f"{changed} items changed")


if __name__ == "__main__":
    main()
