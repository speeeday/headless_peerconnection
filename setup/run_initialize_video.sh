#!/bin/bash

target_time=$1

while [ "$(date +%H:%M)" != "$target_time" ]; do
    sleep 1
done

sleep 2

./initialize_video.sh
