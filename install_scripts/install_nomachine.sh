#!/bin/bash

set -e  # Quit on error.

wget https://download.nomachine.com/download/8.4/Arm/nomachine_8.4.2_1_arm64.deb
dpkg -i nomachine_8.4.2_1_arm64.deb

# Clean up.
rm nomachine_8.4.2_1_arm64.deb

echo "Done installing NoMachine."
