# Install Qemu for ARM
sudo apt-get install qemu-system-arm -y

# Simulate
qemu-system-arm -M virt -cpu cortex-a7 -kernel zImage \
-initrd initrd.cpio.gz -dtb stm32mp151a-stm32-computer-firmware-mx.dtb \
-nographic -append "console=ttyAMA0"
