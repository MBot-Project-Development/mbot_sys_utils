# mbot_sys_utils
Install scripts and utilities for setting up MBot environment on Ubuntu/Debian

### Setting up a fresh image ###

1. Install dependencies using scripts in install_scripts directory.
```bash
sudo ./install_scripts/install_mbot_dependencies.sh
./install_scripts/install_lcm.sh
```

2. Optional installs:
```bash
sudo ./install_scripts/install_nomachine.sh
sudo ./install_scripts/install_vsvode.sh
```

3. edit mbot_config.txt and copy it to the proper loacation in the boot folder. On Ubuntu 22.04 this is `/boot/firmware`, on Raspberry Pi OS this is just `/boot`:
```bash
sudo cp mbot_config.txt [/boot, /boot/firmware]
```

4. Install udev rules:
```bash
cd udev_rules
./install_rules.sh
```

5. Install services:
```bash
cd services
./install_mbot_services.sh
```

7. Reboot.

6. Test
