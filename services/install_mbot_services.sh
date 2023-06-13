#!/bin/bash

set -e  # Quit on error.

# Copy the scripts we need for the services.
sudo cp mbot_start_networking.py /usr/local/etc/
sudo cp mbot_publish_info.sh /usr/local/etc/

# Copy the services.
sudo cp mbot_start_network.service /etc/systemd/system/mbot_start_network.service
sudo cp mbot_publish_info.service /etc/systemd/system/mbot_publish_info.service
sudo cp mbot_lcm_serial.service /etc/systemd/system/mbot_lcm_serial.service

# Enable the services.
sudo systemctl daemon-reload
sudo systemctl enable mbot_start_network.service
sudo systemctl enable mbot_publish_info.service
sudo systemctl enable mbot_lcm_serial.service
