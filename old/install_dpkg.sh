#!/bin/bash

# Download dpkg from ubuntu
wget http://ports.ubuntu.com/pool/main/d/dpkg/dpkg_1.22.0ubuntu1_armhf.deb

# Extract it
ar -x dpkg_1.22.0ubuntu1_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /
cp -a ./etc /
cp -a ./var /
cp -a ./sbin /
cp -a ./lib /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/libm/libmd/libmd0_1.1.0-2build1_armhf.deb

# Extract it
ar -x libmd0_1.1.0-2build1_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/x/xz-utils/liblzma5_5.6.2-2_armhf.deb

# Extract it
ar -x liblzma5_5.6.2-2_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/g/glibc/libc6_2.38-1ubuntu6.3_armhf.deb

# Extract it
ar -x libc6_2.38-1ubuntu6.3_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /
cp -a ./etc /
cp -a ./lib /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/b/bzip2/libbz2-1.0_1.0.8-6_armhf.deb

# Extract it
ar -x libbz2-1.0_1.0.8-6_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/libs/libselinux/libselinux1_3.5-2ubuntu5_armhf.deb

# Extract it
ar -x libselinux1_3.5-2ubuntu5_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/p/pcre2/libpcre2-8-0_10.42-4ubuntu2_armhf.deb

# Extract it
ar -x libpcre2-8-0_10.42-4ubuntu2_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/libz/libzstd/libzstd1_1.5.5+dfsg2-2build1.1_armhf.deb

# Extract it
ar -x libzstd1_1.5.5+dfsg2-2build1.1_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/z/zlib/zlib1g_1.3.dfsg-3.1ubuntu2.1_armhf.deb

# Extract it
ar -x zlib1g_1.3.dfsg-3.1ubuntu2.1_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/t/tar/tar_1.35+dfsg-3build1_armhf.deb

# Extract it
ar -x tar_1.35+dfsg-3build1_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /
cp -a ./etc /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/z/zlib/zlib1g_1.3.dfsg-3.1ubuntu2.1_armhf.deb

# Extract it
ar -x zlib1g_1.3.dfsg-3.1ubuntu2.1_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /

# Clean
rm -r *

# Download
wget http://ports.ubuntu.com/pool/main/a/acl/libacl1_2.3.2-2_armhf.deb

# Extract it
ar -x libacl1_2.3.2-2_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /

# Clean
rm -r *

## Configure dpkg - Not sure if being used!

# Download
wget http://ports.ubuntu.com/pool/main/g/glibc/libc-bin_2.38-1ubuntu6.3_armhf.deb

# Extract it
ar -x libc-bin_2.38-1ubuntu6.3_armhf.deb
unzstd data.tar.zst 
tar -xvf data.tar

# Copy
cp -a ./usr /
cp -a ./sbin /
#cp -a ./var / <- Don't need because it's empty
cp -a ./etc /

# Clean
rm -r *
