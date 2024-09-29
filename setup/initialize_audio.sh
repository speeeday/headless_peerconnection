#!/bin/bash

pulseaudio --start

pactl load-module module-null-sink sink_name=virtual_speaker sink_properties=device.description="Virtual_Speaker"

pactl list sinks short

pactl set-default-sink virtual_speaker

pactl load-module module-loopback source=virtual_speaker.monitor

