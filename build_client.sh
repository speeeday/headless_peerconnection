#!/bin/bash

export PATH=/mnt/md0/sanjay/webrtc/depot_tools:$PATH

current_dir=$(pwd)
echo "Building peerconnection client from $current_dir"

# Replace with new source files
rm -rf /mnt/md0/sanjay/webrtc/webrtc-checkout/src/examples/peerconnection/client
cp -r client /mnt/md0/sanjay/webrtc/webrtc-checkout/src/examples/peerconnection/

# Set build configuration
cd /mnt/md0/sanjay/webrtc/webrtc-checkout/src/
gn gen out/Default --args='target_os="linux" target_cpu="arm64"'

# Build executable
ninja -C out/Default

# Return to original directory
cd $current_dir

# Copy over newly built files
mkdir -p build
cp /mnt/md0/sanjay/webrtc/webrtc-checkout/src/out/Default/peerconnection_client ./build/
