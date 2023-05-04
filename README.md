# mbot_sys_utils
Install scripts and utilities for setting up MBot environment on Ubuntu/Debian

### Setting up a fresh image ###

1. Install dependencies using scripts in install_scripts directory. \
`cd install_scripts` \
`sudo ./install_mbot_dependencies.sh`\
`sudo ./install_lcm.sh`

2. Optional installs \
`sudo ./install_nomachine.sh`\
`sudo ./install_vsvode.sh`

3. edit mbot_config.txt and copy it to the proper loacation in the boot folder. On Ubuntu 22.04 this is `/boot/firmware`, on Raspberry Pi OS this is just `/boot`.

4. Install udev rules \
`cd udev_rules`\
`sudo ./install_rules.sh`

5. Install services \
`cd services`\
`sudo ./install_mbot_services.sh`

6. Test 
