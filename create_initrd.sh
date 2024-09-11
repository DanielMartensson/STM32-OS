# Download BusyBox
git clone https://github.com/mirror/busybox.git

# Go into busybox
cd busybox

# Download the compiler for ARMv7l
sudo apt install gcc-arm-linux-gnueabihf -y

# Configu the menue
echo "Enters menuconfig: Settings ---> Build static binary (no shared libs)"
make menuconfig

# Export the ARM GCC for cross compilation
export CROSS_COMPILE=arm-linux-gnueabihf-

# Export architecture
export ARCH=arm

# Compile busybox with 8 threads
make -j 8
make install

# Create initrd
mkdir initrd

# Inside initrd create these folders
mkdir -p initrd/bin initrd/sbin initrd/etc initrd/proc initrd/sys initrd/dev initrd/usr/bin initrd/usr/sbin

# Copy all
cp -a _install/* ./initrd

# Create the init file
cat << EOF > initrd/init
#!/bin/sh
# Copyright (C) 2011 O.S. Systems Software LTDA.
# Licensed on MIT
#
# Provides the API to be used by the initramfs modules
#
# Modules need to provide the following functions:
#
# <module>_enabled : check if the module ought to run (return 1 to skip)
# <module>_run     : do what is need
#
# Boot parameters are available on environment in the as:
#
# 'foo=value' as 'bootparam_foo=value'
# 'foo' as 'bootparam_foo=true'
# 'foo.bar[=value] as 'foo_bar=[value|true]'

# Register a function to be called before running a module
# The hook is called as:
#   <function> pre <module>
add_module_pre_hook() {
	MODULE_PRE_HOOKS="\$MODULE_PRE_HOOKS \$1"
}

# Register a function to be called after running a module
# The hook is called as:
#   <function> post <module>
add_module_post_hook() {
	MODULE_POST_HOOKS="\$MODULE_POST_HOOKS \$1"
}

# Load kernel module
load_kernel_module() {
	if modprobe \$1 >/dev/null 2>&1; then
		info "Loaded module \$1"
	else
		debug "Failed to load module \$1"
	fi
}

# Prints information
msg() {
	echo "\$@" >/dev/console
}

# Prints information if verbose bootparam is used
info() {
	[ -n "\$bootparam_verbose" ] && echo "\$@" >/dev/console
}

# Prints information if debug bootparam is used
debug() {
	[ -n "\$bootparam_debug" ] && echo "DEBUG: \$@" >/dev/console
}

# Prints a message and start a endless loop
fatal() {
    echo \$1 >/dev/console
    echo >/dev/console

    if [ -n "\$bootparam_init_fatal_sh" ]; then
        sh
    else
	while [ "true" ]; do
		sleep 3600
	done
    fi
}

# Variables shared amoung modules
ROOTFS_DIR="/rootfs" # where to do the switch root
MODULE_PRE_HOOKS=""  # functions to call before running each module
MODULE_POST_HOOKS="" # functions to call after running each module
MODULES_DIR=/init.d  # place to look for modules
EFI_DIR=/sys/firmware/efi  # place to store device firmware information

# make mount stop complaining about missing /etc/fstab
touch /etc/fstab

# initialize /proc, /sys, /run/lock and /var/lock
mkdir -p /proc /sys /run/lock /var/lock
mount -t proc proc /proc
mount -t sysfs sysfs /sys

if [ -d \$EFI_DIR ];then
	mount -t efivarfs none /sys/firmware/efi/efivars
fi

# populate bootparam environment
for p in `cat /proc/cmdline`; do
	if [ -n "\$quoted" ]; then
		value="\$value \$p"
		if [ "`echo \$p | sed -e 's/\"\$//'`" != "\$p" ]; then
			eval "bootparam_\${quoted}=\${value}"
			unset quoted
		fi
		continue
	fi

	opt=`echo \$p | cut -d'=' -f1`
	opt=`echo \$opt | sed -e 'y/.-/__/'`
	if [ "`echo \$p | cut -d'=' -f1`" = "\$p" ]; then
		eval "bootparam_\${opt}=true"
	else
		value="`echo \$p | cut -d'=' -f2-`"
		if [ "`echo \$value | sed -e 's/^\"//'`" != "\$value" ]; then
			quoted=\${opt}
			continue
		fi
		eval "bootparam_\${opt}=\"\${value}\""
	fi
done

# use /dev with devtmpfs
if grep -q devtmpfs /proc/filesystems; then
	mkdir -p /dev
	mount -t devtmpfs devtmpfs /dev
else
	if [ ! -d /dev ]; then
		fatal "ERROR: /dev doesn't exist and kernel doesn't has devtmpfs enabled."
	fi
fi

mkdir \$ROOTFS_DIR

# Load and run modules
for m in \$MODULES_DIR/*; do
	# Skip backup files
	if [ "`echo \$m | sed -e 's/\~\$//'`" != "\$m" ]; then
		continue
	fi

	module=`basename \$m | cut -d'-' -f 2`
	debug "Loading module \$module"

	# pre hooks
	for h in \$MODULE_PRE_HOOKS; do
		debug "Calling module hook (pre): \$h"
		eval "\$h pre \$module"
		debug "Finished module hook (pre): \$h"
	done

	# process module
	. \$m

	if ! eval "\${module}_enabled"; then
		debug "Skipping module \$module"
		continue
	fi

	debug "Running \${module}_run"
	eval "\${module}_run"

	# post hooks
	for h in \$MODULE_POST_HOOKS; do
		debug "Calling module hook (post): \$h"
		eval "\$h post \$module"
		debug "Finished module hook (post): \$h"
	done
done

# Catch all
fatal "ERROR: Initramfs failed to initialize the system."

EOF

# Make it executable
chmod +x initrd/init

# Go into initrd
cd initrd

# Compress
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../../initrd.cpio.gz



