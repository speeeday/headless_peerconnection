#!/bin/bash

export PATH=/home/sanjay/research/depot_tools:$PATH

current_dir=$(pwd)
echo "Building peerconnection client from $current_dir"

# Replace with new source files
rm -rf /home/sanjay/research/webrtc-checkout/src/examples/peerconnection/client
cp -r client /home/sanjay/research/webrtc-checkout/src/examples/peerconnection/

# Set build configuration
cd /home/sanjay/research/webrtc-checkout/src/
gn gen out/Default
#gn gen out/Default --args='is_debug=true'

# Build executable
autoninja -C out/Default

# Return to original directory
cd $current_dir

# Copy over newly built files
mkdir -p build
cp /home/sanjay/research/webrtc-checkout/src/out/Default/peerconnection_client ./build/
