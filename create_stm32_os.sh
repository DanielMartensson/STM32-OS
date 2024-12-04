#!/bin/sh

# Remove old
rm rootfs.ext4

# Make file
dd if=/dev/zero of=rootfs.ext4 bs=1M count=3000

# Make filesystem
mkfs.ext4 rootfs.ext4

# Create folder
sudo mkdir -p /mnt/rootfs

# Mount
sudo mount -o loop rootfs.ext4 /mnt/rootfs

# Go inside
cd rootfs

# Fill except /proc
sudo cp -a bin home/ media/ opt/ root/ sbin usr/ boot/ etc/ lib mnt/ srv/ tmp/ var/ dev/ run/ sys/ /mnt/rootfs/

# Restore file ownership and permissions
sudo setfacl --restore=../rootfs.facl

# Umount
sudo umount /mnt/rootfs

# Get out
cd ..

# Copy
cp rootfs.ext4 ../STM32-Computer/Firmware/STM32-Computer-Firmware/CA7/FIP_artifacts/rootfs.ext4
