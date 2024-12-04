#!/bin/sh
#
# Only run this if your local file ownership
# and permissions matches the target system!
#

(cd rootfs && getfacl -PRn .) > rootfs.facl
