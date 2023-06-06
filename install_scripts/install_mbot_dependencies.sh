#!/bin/bash

set -e  # Quit on error.

#### Install software from apt-get ####
apt-get update
apt-get upgrade -y
apt-get -y install ssh git software-properties-common apt-transport-https wget gpg cmake

# install dependencies !! Need to make this is complete and all are used
apt-get -y install build-essential wget dkms \
    autoconf automake autotools-dev gdb libglib2.0-dev libgtk2.0-dev \
    libusb-dev libusb-1.0-0-dev freeglut3-dev libboost-dev libatlas-base-dev \
    libgsl-dev libjpeg-dev default-jdk doxygen openssl libssl-dev libdc1394-dev \
    libcamera-dev v4l-utils minicom

apt-get -y install mesa-common-dev libgl1-mesa-dev libglu1-mesa-dev

# install python3 and scipy
apt-get -y install python3-dev python3-numpy python3-matplotlib python3-opencv python3-scipy python3-pygame


#### Enable features for specific platforms ####
# Check if running on RPi
if grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo "RPi detected, installing raspi-config"
    apt-get -y install raspi-config
    raspi-config nonint do_vnc 0
    raspi-config nonint do_ssh 0
    raspi-config nonint do_camera 0
fi

if grep -q "NVIDIA Jetson Nano" /proc/device-tree/model; then
    echo "Jetson Nano detected"
fi

echo "Done Installing!"
