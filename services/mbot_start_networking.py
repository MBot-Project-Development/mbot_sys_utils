#!/usr/bin/python3
import os
import time
import datetime
import subprocess
# Define the path to the config file
is_ubuntu = 'Ubuntu' in subprocess.check_output(['cat', '/etc/os-release']).decode('utf-8')
is_raspios = 'Raspberry Pi OS' in subprocess.check_output(['cat', '/etc/os-release']).decode('utf-8')

if(is_ubuntu):
    config_file = "/boot/firmware/mbot_config.txt"
else:
    config_file = "/boot/mbot_config.txt"

# Define the path to the log file
log_file = "/var/log/mbot/mbot_start_networking.log"
os.makedirs(os.path.dirname(log_file), exist_ok = True)
os.chmod(os.path.dirname(log_file), 0o777)
with open(log_file, "a") as log:
    os.chmod(log_file, 0o666)
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    log.write("===== ")
    log.write(formatted_time)
    log.write(" =====\n")
    # Read the config file and store the values in variables
    with open(config_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            key, value = line.strip().split("=")
            if key == "mbot_hostname":
                hostname = value
                ap_ssid = hostname + "-AP"
            elif key == "mbot_ap_ssid":
                ap_ssid = value
            elif key == "mbot_ap_password":
                ap_password = value
            elif key == "new_wifi_ssid":
                home_wifi_ssid = value
            elif key == "new_wifi_password":
                home_wifi_password = value

    # Change the hostname in /etc/hosts. This has to be done first.
    with open("/etc/hosts", "r") as f:
        filedata = f.read()
        filedata = filedata.replace(os.uname()[1], hostname)
    with open("/etc/hosts", "w") as f:
        f.write(filedata)
    # Set hostname on the system.
    os.system(f"hostnamectl set-hostname {hostname}")
    # Set the hostname in /etc/hostname
    with open("/etc/hostname", "w") as f:
        f.write(hostname)
    log.write(f"hostname set to '{hostname}'\n")

    # setup LO as multicast for localhost LCM connections
    os.system("sudo ifconfig lo multicast")
    os.system("sudo route add -net 224.0.0.0 netmask 240.0.0.0 dev lo")

    # Check if there is an active WiFi connection
    wifi_active = False
    wifi_status = os.popen("nmcli -t -f NAME,DEVICE,STATE c show --active").read().strip()
    if wifi_status:
        for line in wifi_status.split('\n'):
            name, device, state = line.split(':')
            if device == 'wlan0' and state == 'activated':
                wifi_active = True
                break

    if wifi_active:
        # Already connected to  WiFi network
        log.write(f"Connected to active WiFi network '{name}'. Done.\n")

    else:
        # We don't have a wifi network, check for ones we know
        available_networks = []
        known_networks = []
        bssid = []
        ssid = []
        channel = []
        signal = []
        log.write(f"Looking for home network '{home_wifi_ssid}'\n")
        log.write("Wifi Scan:\n")
        scan_output = os.popen("nmcli dev wifi list").read().split('\n')
        for line in scan_output:
            line = line.strip()  # Remove whitespace before and after.
            if len(line) > 0 and not line.startswith("IN-USE"):
                if home_wifi_ssid in line:
                    log.write(f"{line}\n")
                    # This line is the network we're looking for.
                    ssid.append(home_wifi_ssid)
                    # Some SSIDs have spaces so splitting will fail. Remove it from the line first.
                    line = line.replace(home_wifi_ssid, "")

                    # Grab the info for this network.
                    bssid.append(line.split()[0])
                    channel.append(line.split()[2])
                    signal.append(line.split()[5])
        log.write("\n")
        available = list(zip(bssid, ssid, channel, signal))
        sorted_avail = sorted(available, key=lambda x: (int(x[2]), int(x[3])), reverse=True)
        print(sorted_avail)
        if home_wifi_ssid in ssid:
            # Check if we've already added the home network
            for line in os.popen("nmcli connection show").readlines():
                ssid = line.strip().split()[0]
                log.write(f"{ssid}, ")
                if ssid not in known_networks:
                    known_networks.append(ssid)
                    log.write(f"{ssid}, ")
            log.write("\n")
            if home_wifi_ssid not in known_networks:
                home_wifi_bssid = sorted_avail[0][0]
                # Connect to home WiFi network
                os.system(f"nmcli dev wifi connect '{home_wifi_bssid}' password '{home_wifi_password}'")
            else:
                os.system(f"nmcli connection up '{home_wifi_ssid}'")
            log.write(f"Started connection to WiFi network '{home_wifi_ssid}'. Done.\n")

        else:
            log.write("No networks found, starting Access Point\n")
            # Check if the access point already exists to delete, otherwise hostname may be wrong
            for line in os.popen("nmcli connection show").readlines():
                if "mbot_wifi_ap" in line:
                    log.write("Access point already exists, removing... \n")
                    os.system(f"nmcli connection delete mbot_wifi_ap")
                    break
            # Configure Network Manager to create a WiFi access point
            os.system(f"nmcli connection add type wifi ifname '*' con-name mbot_wifi_ap autoconnect no ssid {ap_ssid}")
            os.system("nmcli connection modify mbot_wifi_ap 802-11-wireless.mode ap 802-11-wireless.band a ipv4.method shared")
            os.system(f"nmcli connection modify mbot_wifi_ap wifi-sec.key-mgmt wpa-psk wifi-sec.psk {ap_password}")
            os.system("nmcli connection modify mbot_wifi_ap ipv4.method manual ipv4.addresses 192.168.3.1/24 ipv4.gateway 192.168.3.1")
            log.write("Access point created successfully. \n")
            time.sleep(10.0)
            os.system("nmcli connection up mbot_wifi_ap")
            log.write("Access point started. \n")
