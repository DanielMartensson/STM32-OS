# Download build root
wget -nc https://buildroot.org/downloads/buildroot-2024.02.6.tar.gz

# Extract
tar -xf buildroot-2024.02.6.tar.gz

# Remove
rm -f *.gz

# Install packages
sudo apt-get install g++ make libncurses-dev unzip bc bzip2 libelf-dev libssl-dev extlinux -ys

# Copy defconfig
cp stm32_os_defconfig buildroot-2024.02.6/configs

# Go inside
cd buildroot-2024.02.6

# Enter menuconfig
make stm32_os_defconfig

# Compile
make

# Create a rootfs folder
sudo mkdir /mnt/rootfs

# Mount rootfs.ext4
sudo mount -o loop output/images/rootfs.ext4 /mnt/rootfs


# Umount
#sudo umount /mnt/rootfs


