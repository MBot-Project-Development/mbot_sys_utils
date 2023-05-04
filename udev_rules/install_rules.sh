#!/bin/bash
sudo cp 50-mbot.rules /etc/udev/rules.d/
sudo cp 50-rplidar.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
