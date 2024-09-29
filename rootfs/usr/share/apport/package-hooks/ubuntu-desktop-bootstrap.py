"""Send reports about ubuntu-desktop-bootstrap to the correct Launchpad
project."""

# pylint: disable=invalid-name
# pylint: enable=invalid-name

import os

from apport import hookutils


def add_info(report, unused_ui):
    """Send reports about ubuntu-desktop-bootstrap to the correct Launchpad
    project."""
    udblog = os.path.realpath("/var/log/installer/ubuntu_bootstrap.log")
    hookutils.attach_file_if_exists(report, udblog, "UdbLog")

    report["SourcePackage"] = "ubuntu-desktop-bootstrap"
    # rewrite this section so the report goes to the project in Launchpad
    report[
        "CrashDB"
    ] = """\
{
    "impl": "launchpad",
    "project": "ubuntu-desktop-provision",
    "bug_pattern_url": "http://people.canonical.com/"
    "~ubuntu-archive/bugpatterns/bugpatterns.xml",
}
"""

    subiquitylog = os.path.realpath("/var/log/installer/subiquity-server-debug.log")
    if os.path.exists(subiquitylog):
        report["SubiquityLog"] = hookutils.root_command_output(["cat", subiquitylog])

    hookutils.attach_file_if_exists(
        report, "/var/log/installer/curtin-install.log", "CurtinLog"
    )
    hookutils.attach_file_if_exists(
        report, "/var/log/installer/curtin-errors.tar", "CurtinError.tar"
    )

    hookutils.attach_file_if_exists(
        report, "/var/log/installer/block/probe-data.json", "ProbeData"
    )

    # Always set reports to private since we might collect sensitive data
    report["LaunchpadPrivate"] = "1"
