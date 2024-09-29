# This hook collects logs for Power systems and more specific logs for Pseries,
# PowerNV platforms.
#
# Author: Thierry FAUCK <thierry@linux.vnet.ibm.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

"""IBM Power System related information"""

import os
import pathlib
import platform
import subprocess
import tempfile

from apport.hookutils import (
    attach_file,
    attach_file_if_exists,
    attach_root_command_outputs,
    command_available,
    command_output,
)


def _add_tar(report, path, key):
    (tar_fd, tar_file) = tempfile.mkstemp(prefix="apport.", suffix=".tar")
    os.close(tar_fd)
    subprocess.call(["tar", "chf", tar_file, path])
    if os.path.getsize(tar_file) > 0:
        report[key] = (tar_file,)
    # NB, don't cleanup the temp file, it'll get read later by the apport main
    # code


# TODO: Split into smaller functions/methods
# pylint: disable-next=too-many-branches,too-many-statements
def add_info(report, unused_ui):
    """Add IBM Power System related information to report."""
    arch = platform.machine()
    if arch not in ["ppc64", "ppc64le"]:
        return

    is_kernel = report["ProblemType"].startswith("Kernel") or "linux" in report.get(
        "Package", ""
    )

    try:
        contents = pathlib.Path("/proc/cpuinfo").read_text("utf-8")
        is_pseries = "pSeries" in contents
        is_power_nv = "PowerNV" in contents
        is_power_kvm = "emulated by qemu" in contents
    except IOError:
        is_pseries = False
        is_power_nv = False
        is_power_kvm = False

    if is_pseries or is_power_nv:
        if is_kernel:
            _add_tar(report, "/proc/device-tree/", "DeviceTree.tar")
        attach_file(report, "/proc/misc", "ProcMisc")
        attach_file(report, "/proc/locks", "ProcLocks")
        attach_file(report, "/proc/loadavg", "ProcLoadAvg")
        attach_file(report, "/proc/swaps", "ProcSwaps")
        attach_file(report, "/proc/version", "ProcVersion")
        report["cpu_smt"] = command_output(["ppc64_cpu", "--smt"])
        report["cpu_cores"] = command_output(["ppc64_cpu", "--cores-present"])
        report["cpu_coreson"] = command_output(["ppc64_cpu", "--cores-on"])
        # To be executed as root
        if is_kernel:
            attach_root_command_outputs(
                report,
                {
                    "cpu_runmode": "ppc64_cpu --run-mode",
                    "cpu_freq": "ppc64_cpu --frequency",
                    "cpu_dscr": "ppc64_cpu --dscr",
                    "nvram": "cat /dev/nvram",
                },
            )
        attach_file_if_exists(report, "/var/log/platform")

    if is_pseries and not is_power_kvm:
        attach_file(report, "/proc/ppc64/lparcfg", "ProcLparCfg")
        attach_file(report, "/proc/ppc64/eeh", "ProcEeh")
        attach_file(report, "/proc/ppc64/systemcfg", "ProcSystemCfg")
        report["lscfg_vp"] = command_output(["lscfg", "-vp"])
        report["lsmcode"] = command_output(["lsmcode", "-A"])
        report["bootlist"] = command_output(["bootlist", "-m", "both", "-r"])
        report["lparstat"] = command_output(["lparstat", "-i"])
        if command_available("lsvpd"):
            report["lsvpd"] = command_output(["lsvpd", "--debug"])
        if command_available("lsvio"):
            report["lsvio"] = command_output(["lsvio", "-des"])
        if command_available("servicelog"):
            report["servicelog_dump"] = command_output(["servicelog", "--dump"])
        if command_available("servicelog_notify"):
            report["servicelog_list"] = command_output(["servicelog_notify", "--list"])
        if command_available("usysattn"):
            report["usysattn"] = command_output(["usysattn"])
        if command_available("usysident"):
            report["usysident"] = command_output(["usysident"])
        if command_available("serv_config"):
            report["serv_config"] = command_output(["serv_config", "-l"])

    if is_power_nv:
        _add_tar(report, "/proc/ppc64/", "ProcPpc64.tar")
        attach_file_if_exists(report, "/sys/firmware/opal/msglog")
        if os.path.exists("/var/log/dump"):
            report["VarLogDump_list"] = command_output(["ls", "-l", "/var/log/dump"])
        if is_kernel:
            _add_tar(report, "/var/log/opal-elog", "OpalElog.tar")
