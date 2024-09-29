# STM32-OS 24.04 LTS

Target             |   Ecosystem
:-------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/DanielMartensson/STM32-OS/refs/heads/main/stm32mp1.png)  |  ![](https://raw.githubusercontent.com/DanielMartensson/STM32-OS/refs/heads/main/ubuntu.png)

This repository is about a minimal linux distro, based on `Ubuntu 24.04 LTS`. This linux distribution has the minimal setup for starting a system. Every package `Ubuntu 24.04 LTS` have, can be installed on `STM32-OS`.

# Important software pre-installed

* busybox
* ssh
* apt
* dpkg
* nano
* python
* bzip2
* gzip
* etc...

# How to use

First you need to clone two `repos`.

```sh
git clone https://github.com/danielmartensson/STM32-OS
git clone https://github.com/danielmartensson/STM32-Computer
```

Then you run this file. Enter super user password for root privileges. This will create a file callecd `rootfs.ext4`.
```sh
./create_stm32_os.sh
```

After that, go to this path and run `STM32CubeProgrammer`. Plug in your `Micro USB` cable (yes I know) into `STM32-Computer` and load the `FlashLayout - STM32-OS.tsv` inside `STM32CubeProgrammer`. Then you press `Download` and the `eMMC` will be flashed with the `STM32-OS`.
```
STM32-Computer/Firmware/STM32-Computer-Firmware/CA7/FIP_artifacts
```

Don't forget to change the `BOOT1` pin to `unconnected` when you're flashing and then change `BOOT1` pin to `connected` when you're booting the `STM32-OS`.

After the system has booted up, and you can either login(`user: root`. `password: root`) via `UART` or `ssh`, then it's important to run this command so you can take adventage of the total system space. This will resize the system to its true size, or else, you cannot even create a single file.

```sh
resize2fs /dev/mmcblk0p7
e2fsck -f /dev/mmcblk0p6
df -h
```

![](https://raw.githubusercontent.com/DanielMartensson/STM32-OS/refs/heads/main/memory.png)

# Packages pre-installed

A minimal system need to have:

* hdmi
* ssh
* net

So therefore, these must be installed, if they are not already installed.

```sh
apt-get install isc-dhcp-client net-tools drm-info libdrm2 libdrm-amdgpu1 libdrm-common libdrm-tests xorg xterm xserver-xorg-video-armsoc x11-xserver-utils xinit xserver-xorg-input-evdev weston seatd libinput-tools xcursor-themes libgl1-mesa-dri mesa-utils wayland-utils 
sudo touch ~/.Xauthority
```

## Starting the screen

```
weston --use-pixman
```

# Troubleshooting

```
Problem: sudo: unable to allocate pty: No such device
Solution: mount none -t devpts /dev/pts
```

# To large files to commit

These are important files that are to large to commit.

```
rootfs/usr/lib/arm-linux-gnueabihf/libLLVM-17.so.1
```

# FAQ

* Question: Can I use this for `STM32MP157` too?
  - Answer: The installation of this linux distribution is meant to work for `STM32-Computer`, but the `file_system` folder, which is the `STM32-OS`, can work for all types of `armhf` architectures. So the answer is yes, you can.
* Question: STMicroelectronics have a linux distribution called `OpenSTLinux`. Why did you not use that instead?
  - Answer: I find that `Ubunutu's` ecosystem of the `apt` packages are much richer compared to `OpenSTLinux`. Also there is more community support for `Ubuntu` compared to `OpenSTLinux`.
* Question: I want to build on my kernel, can I use this repository to build on my kernel?
  - Answer: No, if you want to build on your kernel, head over to `STM32-Computer`. I have separated the `bootfs`-work (kernel) and `rootfs`-work (STM32-OS).
* Question: What's the difference between `Ubuntu 24.04 LTS` and `STM32-OS 24.04 LTS`?
  - Answer: I'm keeping `STM32-OS` as thin as possible for minimal `RAM` usage.
 
