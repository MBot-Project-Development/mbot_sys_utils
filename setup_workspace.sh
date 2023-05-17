#!/bin/bash

# Check if directory argument is provided
if [ -z "$1" ]; then
    echo "Please provide the top level directory as an argument."
    exit 1
fi

TOP_DIR="$1"
mkdir -p ~/"$TOP_DIR"
cd ~/"$TOP_DIR"

repos=("mbot_lcm_base" "mbot_firmware" "mbot_bridge" "mbot_autonomy" "mbot_gui" "mbot_web_app" "rplidar_lcm_driver" "Documentation")

for repo in "${repos[@]}"; do
  if [ -d "$repo" ]; then
    echo "Repo $repo already exists, pulling latest changes"
    cd "$repo"
    git pull
    cd ..
  else
    git clone "git@github.com:MBot-Project-Development/$repo.git"
  fi
done
