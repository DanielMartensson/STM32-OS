
# constants.py - configured information and constants, this file is processed
#                and extended by the configure script
#
# Copyright (C) 2012-2015 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA


# Name of package
PACKAGE = '''nss-pam-ldapd'''

# Define to the address where bug reports for this package should be sent.
PACKAGE_BUGREPORT = '''nss-pam-ldapd-users@lists.arthurdejong.org'''

# Define to the full name of this package.
PACKAGE_NAME = '''nss-pam-ldapd'''

# Define to the full name and version of this package.
PACKAGE_STRING = '''nss-pam-ldapd 0.9.12'''

# Define to the home page for this package.
PACKAGE_URL = '''https://arthurdejong.org/nss-pam-ldapd/'''

# Version number of package
VERSION = '''0.9.12'''

# Path to nslcd configuration file.
NSLCD_CONF_PATH = '''/etc/nslcd.conf'''

# The location of the pidfile used for checking availability of the nslcd.
NSLCD_PIDFILE = '''/var/run/nslcd/nslcd.pid'''

# The location of the socket used for communicating.
NSLCD_SOCKET = '''/var/run/nslcd/socket'''

# The SONAME of the NSS library module.
NSS_LDAP_SONAME = '''libnss_ldap.so.2'''

# The name of the NSS and PAM modules.
MODULE_NAME = '''ldap'''

# The following is automatically generated from nslcd.h.
# See that file for details.

NSLCD_VERSION = 0x00000002
NSLCD_ACTION_CONFIG_GET = 0x00010001
NSLCD_CONFIG_PAM_PASSWORD_PROHIBIT_MESSAGE = 1
NSLCD_ACTION_ALIAS_BYNAME = 0x00020001
NSLCD_ACTION_ALIAS_ALL = 0x00020008
NSLCD_ACTION_ETHER_BYNAME = 0x00030001
NSLCD_ACTION_ETHER_BYETHER = 0x00030002
NSLCD_ACTION_ETHER_ALL = 0x00030008
NSLCD_ACTION_GROUP_BYNAME = 0x00040001
NSLCD_ACTION_GROUP_BYGID = 0x00040002
NSLCD_ACTION_GROUP_BYMEMBER = 0x00040006
NSLCD_ACTION_GROUP_ALL = 0x00040008
NSLCD_ACTION_HOST_BYNAME = 0x00050001
NSLCD_ACTION_HOST_BYADDR = 0x00050002
NSLCD_ACTION_HOST_ALL = 0x00050008
NSLCD_ACTION_NETGROUP_BYNAME = 0x00060001
NSLCD_ACTION_NETGROUP_ALL = 0x00060008
NSLCD_NETGROUP_TYPE_NETGROUP = 1
NSLCD_NETGROUP_TYPE_TRIPLE = 2
NSLCD_NETGROUP_TYPE_END = 3
NSLCD_ACTION_NETWORK_BYNAME = 0x00070001
NSLCD_ACTION_NETWORK_BYADDR = 0x00070002
NSLCD_ACTION_NETWORK_ALL = 0x00070008
NSLCD_ACTION_PASSWD_BYNAME = 0x00080001
NSLCD_ACTION_PASSWD_BYUID = 0x00080002
NSLCD_ACTION_PASSWD_ALL = 0x00080008
NSLCD_ACTION_PROTOCOL_BYNAME = 0x00090001
NSLCD_ACTION_PROTOCOL_BYNUMBER = 0x00090002
NSLCD_ACTION_PROTOCOL_ALL = 0x00090008
NSLCD_ACTION_RPC_BYNAME = 0x000a0001
NSLCD_ACTION_RPC_BYNUMBER = 0x000a0002
NSLCD_ACTION_RPC_ALL = 0x000a0008
NSLCD_ACTION_SERVICE_BYNAME = 0x000b0001
NSLCD_ACTION_SERVICE_BYNUMBER = 0x000b0002
NSLCD_ACTION_SERVICE_ALL = 0x000b0008
NSLCD_ACTION_SHADOW_BYNAME = 0x000c0001
NSLCD_ACTION_SHADOW_ALL = 0x000c0008
NSLCD_ACTION_PAM_AUTHC = 0x000d0001
NSLCD_ACTION_PAM_AUTHZ = 0x000d0002
NSLCD_ACTION_PAM_SESS_O = 0x000d0003
NSLCD_ACTION_PAM_SESS_C = 0x000d0004
NSLCD_ACTION_PAM_PWMOD = 0x000d0005
NSLCD_ACTION_USERMOD = 0x000e0001
NSLCD_USERMOD_END = 0
NSLCD_USERMOD_RESULT = 1
NSLCD_USERMOD_FULLNAME = 2
NSLCD_USERMOD_ROOMNUMBER = 3
NSLCD_USERMOD_WORKPHONE = 4
NSLCD_USERMOD_HOMEPHONE = 5
NSLCD_USERMOD_OTHER = 6
NSLCD_USERMOD_HOMEDIR = 7
NSLCD_USERMOD_SHELL = 8
NSLCD_RESULT_BEGIN = 1
NSLCD_RESULT_END = 2
NSLCD_PAM_SUCCESS = 0
NSLCD_PAM_PERM_DENIED = 6
NSLCD_PAM_AUTH_ERR = 7
NSLCD_PAM_CRED_INSUFFICIENT = 8
NSLCD_PAM_AUTHINFO_UNAVAIL = 9
NSLCD_PAM_USER_UNKNOWN = 10
NSLCD_PAM_MAXTRIES = 11
NSLCD_PAM_NEW_AUTHTOK_REQD = 12
NSLCD_PAM_ACCT_EXPIRED = 13
NSLCD_PAM_SESSION_ERR = 14
NSLCD_PAM_AUTHTOK_ERR = 20
NSLCD_PAM_AUTHTOK_DISABLE_AGING = 23
NSLCD_PAM_IGNORE = 25
NSLCD_PAM_ABORT = 26
NSLCD_PAM_AUTHTOK_EXPIRED = 27
