# Create build root folder
mkdir buildroot

# Go inside
cd buildroot

# Download build root
wget https://buildroot.org/downloads/buildroot-2024.08.tar.gz

# Extract
tar -xf buildroot-2024.08.tar.gz

# Remove
rm *.gz

# Install packages
sudo apt-get install g++ make libncurses-dev unzip bc bzip2 libelf-dev libssl-dev extlinux -ys

# Go inside
cd buildroot-2024.08

# Download the compiler for ARMv7l
sudo apt install gcc-arm-linux-gnueabihf -y

# Export the ARM GCC for cross compilation
export CROSS_COMPILE=arm-linux-gnueabihf-

# Export architecture
export ARCH=arm

# Enter menuconfig
make stm32mp157a_dk1_defconfig

# Compile
make
