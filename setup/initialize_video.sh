#!/bin/bash

sudo ffmpeg -re -i bun33s.mp4 -map 0:v -f v4l2 /dev/video0 &> /dev/null

# Move the process to the background after using the 'bg' command
