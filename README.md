# STM32-OS
A Linux operative system for the STM32 Computer

* Qt6
* Ethernet
* USB
* HDMI
* Package manager
* etc.

Under construction....

Status: I have made the first version work with the `rootfs` system. Here is an log where I got the `ethernet` working.

# How to deploy

In order to make `openssh` working for a decent connection, one must enable this inside `/etc/ssh/sshd_config` file

```sh
PermitRootLogin yes
PasswordAuthentication yes

```

Then paste this inside `/etch/init.d/S40network` for be able to start the ethernet and let the DHCP server give the ethernet an address.

```sh
ifconfig end0 up
udhcpc -i end0
```

It's important to change the priority of the `PATH` inside `/etc/profile` so the kernel runs `/usr/bin` before the `BusyBox` binaries in `/bin`. Or else `dpkg` won't be able to install `.deb` files due to missing `GNU tar`, which is located inside `/usr/bin`.

```sh
export PATH="/usr/bin:/bin:/sbin:/usr/bin"
```
