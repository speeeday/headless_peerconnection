#!/bin/bash

target_time=$1

while [ "$(date +%H:%M)" != "$target_time" ]; do
    sleep 1
done

sleep 5
./headless_peerconnection_client --server=128.111.5.228 --port=8888 --autoconnect=true --autocall=True
