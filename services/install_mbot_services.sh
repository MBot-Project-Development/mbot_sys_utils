#!/bin/bash

set -e  # Quit on error.

SERVICE_LIST="mbot-start-network
              mbot-publish-info
              mbot-oled"

# Copy the scripts we need for the services.
sudo cp mbot_start_networking.py /usr/local/etc/
sudo cp mbot_publish_info.sh /usr/local/etc/
sudo cp mbot_oled_display.py /usr/local/etc/
sudo cp arial.ttf /usr/local/etc/

# Copy the services.
for serv in $SERVICE_LIST
do
    sudo cp $serv.service /etc/systemd/system/$serv.service
done

# Enable time sync wait service
sudo systemctl enable --now systemd-time-wait-sync.service

# Enable the services.
sudo systemctl daemon-reload
for serv in $SERVICE_LIST
do
    sudo systemctl enable $serv.service
    # echo "Copying $serv"
done

# Success message.
echo
echo "Installed and enabled the following services:"
echo
for serv in $SERVICE_LIST
do
    echo "    $serv.service"
done
echo
