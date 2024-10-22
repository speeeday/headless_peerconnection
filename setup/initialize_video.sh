#!/bin/bash

sudo ffmpeg -re -i BigBuckBunny.mp4 -map 0:v -f v4l2 /dev/video0 &> /dev/null
#ffmpeg -i bun33s.mp4 -map 0:0 -f v4l2 /dev/video0 -map 0:1 -f pulse "virtual_speaker"

# Move the process to the background after using the 'bg' command
