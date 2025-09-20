#!/bin/sh
set -ex

# Install sudo first
apk add sudo

# Create user 'alpine' and set its password to 'alpine'
adduser -D -g 'Alpine User' alpine
echo "alpine:alpine" | chpasswd

# Add the new user to the 'wheel' group for sudo privileges
adduser alpine wheel
# Configure the 'wheel' group to have passwordless sudo access
echo '%wheel ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/wheel

# Install Docker and add the user to the 'docker' group
apk add docker docker-compose
rc-update add docker boot
adduser alpine docker
