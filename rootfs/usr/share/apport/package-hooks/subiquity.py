"""Send reports about subiquity to the correct Launchpad project."""

import os
import re

from apport import Report, hookutils
from apport.ui import HookUI


def get_journal(report: Report, log_map: dict[str, str]) -> None:
    """Get installer environment journal log.

    Appends the installer specific journal to the log map if it exists,
    otherwise appends the system journal to the report directly.
    """
    installer_journal = "/var/log/installer/installer-journal.txt"
    if os.path.exists(installer_journal):
        log_map["InstallerJournal"] = installer_journal
    else:
        report["SystemJournal"] = hookutils.recent_syslog(re.compile("."))


def get_revision(debug_log_contents: str) -> str:
    """Get subiquity revision from debug log contents.

    Returns revision found (e.g. "1234") or "unknown" if not found.
    """
    # Revision information is always in the first line of the log file
    first_line = debug_log_contents.splitlines()[0]
    marker = "Starting Subiquity server revision"
    if marker in first_line:
        revision = first_line.split(marker)[1].strip()
    else:
        revision = "unknown"

    return revision


def add_info(report: Report, unused_ui: HookUI) -> None:
    """Package hook entry point."""
    # Check if the snap was updated
    # TODO: Add logic to support this outside of the live environment.
    #       It may be possible someone wants to report a bug against the
    #       installer after first boot.
    report["SnapUpdated"] = str(os.path.exists("/run/subiquity/updating"))

    # rewrite this section so the report goes to the project in Launchpad
    report[
        "CrashDB"
    ] = """\
{
    "impl": "launchpad",
    "project": "subiquity",
    "bug_pattern_url": "http://people.canonical.com/"
    "~ubuntu-archive/bugpatterns/bugpatterns.xml",
}
"""

    # add in hardware information
    hookutils.attach_hardware(report)

    # This key is important for checking revision information later
    debug_log_key = "InstallerServerLog"

    # static subiquity generated logs
    log_map = {
        debug_log_key: "/var/log/installer/subiquity-server-debug.log",
        "InstallerServerLogInfo": "/var/log/installer/subiquity-server-info.log",
        "InstallerClientLog": "/var/log/installer/subiquity-client-debug.log",
        "InstallerClientLogInfo": "/var/log/installer/subiquity-client-info.log",
        "CurtinLog": "/var/log/installer/curtin-install.log",
        "CurtinAptConfig": "var/log/installer/curtin-install/subiquity-curtin-apt.conf",
        "CurtinCurthooksConfig": (
            "/var/log/installer/curtin-install/subiquity-curthooks.conf"
        ),
        "CurtinExtractConfig": (
            "/var/log/installer/curtin-install/subiquity-extract.conf"
        ),
        "CurtinInitialConfig": (
            "/var/log/installer/curtin-install/subiquity-initial.conf"
        ),
        "CurtinPartitioningConfig": (
            "/var/log/installer/curtin-install/subiquity-partitioning.conf"
        ),
        "ProbeData": "/var/log/installer/block/probe-data.json",
        "Traceback": "/var/log/installer/subiquity-traceback.txt",
        "NetplanInstallerConfig": "/etc/netplan/00-installer-config.yaml",
        "NetplanSnapdConfig": "/etc/netplan/00-snapd-config.yaml",
    }

    # Add journal log
    get_journal(report, log_map)

    # Add ubuntu-desktop-bootstrap information if available
    udb_log = os.path.realpath("/var/log/installer/ubuntu_bootstrap.log")
    if os.path.exists(udb_log):
        log_map["BootstrapLog"] = udb_log
        report.add_tags(["ubuntu-desktop-bootstrap"])
        # check for udb snap version
        udb_snap = os.path.realpath("/snap/ubuntu-desktop-bootstrap/current")
        if os.path.exists(udb_snap):
            # "current" is a symlink to the current revision and
            # os.path.realpath should have resolved it
            report["DesktopInstallerRev"] = os.path.basename(udb_snap)

    # Attach logs if they exist
    # The conventional way to attach logs would be to use the
    # hookutils.attach_file_if_exists method, but since subiquity logs
    # are mostly locked down with root r/w only then we will get a permission
    # error if the caller does not have permissions. Ask for elevated
    # permissions instead of requiring users know to run with sudo or similar
    command_mapping = {}
    for name, path in log_map.items():
        if os.path.exists(path):
            real_path = os.path.realpath(path)
            command_mapping[name] = f"cat {real_path}"

    hookutils.attach_root_command_outputs(report, command_mapping)

    # Get revision to display in the UI prompt
    # If attach_root_command_outputs fails the log won't be in the report
    revision = "unknown"
    if debug_log_key in report:
        revision = get_revision(report[debug_log_key])
    report["Package"] = f"subiquity ({revision})"
    report["SourcePackage"] = "subiquity"

    # Package and SourcePackage keys are deleted when the Snap is chosen,
    # so make a separate key to keep track of the revision
    report["SnapVersion"] = revision

    # Always set reports to private since we might collect sensitive data
    report["LaunchpadPrivate"] = "1"
