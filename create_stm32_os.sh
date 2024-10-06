# Remove old
rm rootfs.ext4

# Make file
dd if=/dev/zero of=rootfs.ext4 bs=1M count=2200

# Make filesystem
mkfs.ext4 rootfs.ext4

# Mount
sudo mount -o loop rootfs.ext4 /mnt/rootfs

# Go inside
cd rootfs

# Create folder
sudo mkdir /mnt/rootfs

# Fill
sudo cp -a bin proc/ home/ media/ opt/ root/ sbin usr/ boot/ etc/ lib mnt/ srv/ tmp/ var/ dev/ run/ sys/ /mnt/rootfs/

# Umount
sudo umount /mnt/rootfs

# Get out
cd ..

# Copy
cp rootfs.ext4 ../STM32-Computer/Firmware/STM32-Computer-Firmware/CA7/FIP_artifacts/rootfs.ext4






