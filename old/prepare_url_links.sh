#!/bin/bash

# Set the base address
base_url="http://ports.ubuntu.com/"

replace="amd64.deb"
with="armhf.deb"
package_name="apt"

# List all dependencies for $package_name
dependencies=$(apt-rdepends $package_name | grep -E '^ ' | sed 's/^ //g' | awk -F' ' '{print $2}' | sort | uniq)

# Create the long wget string
wget_string=""
while read -r pkg; do
	file_path=$(apt-cache show $pkg | grep ^Filename | awk '{print $2}' | sort -V | head -n 1)
	url_path="$base_url$file_path"
	new_url_path=$(echo "$url_path" | sed "s/${replace}/${with}/")
	wget_string="$wget_string $new_url_path"
done <<< "$dependencies"

# Add the last wget
wget_string="wget -nc $wget_string"

# Save
echo "#!/bin/bash"  >> download_install_$package_name.sh
echo "$wget_string" >> download_install_$package_name.sh
echo "dpkg i *.deb" >> download_install_$package_name.sh

# Make executable
chmod +x download_install_$package_name.sh

# End
echo "Done!"
