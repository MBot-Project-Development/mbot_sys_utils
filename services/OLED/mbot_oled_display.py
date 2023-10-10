import os
import re
import time
import qrcode

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

#dtparam=i2c_arm=on,i2c_baudrate=400000 include above in /boot/config.txt
# Explicitly enable I2C via raspi-config (so i2cdetect -y 1 works)
# pip3 install luma.oled qrcode

fontpath = str("fonts/arial.ttf")
font = ImageFont.truetype(fontpath, 14)
fontpath = str("fonts/arial.ttf")
font_small = ImageFont.truetype(fontpath, 10)

device = ssd1306(i2c(port=1, address=0x3C))

# Function to get the IP address of the wlan0 interface
def get_wlan0_ip():
    try:
        # Execute the ifconfig command and capture the output
        command_output = os.popen("ifconfig wlan0").read()
        # Use regular expressions to find the IP address in the output
        ip_match = re.search(r'inet ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', command_output)
        if ip_match:
            ip_address = ip_match.group(1)
            return ip_address
        else:
            return None
    except Exception as e:
        return str(e)
    
def get_hostname():
    try:
        command_output = os.popen("hostname").read()
        return command_output.strip()
    except Exception as e:
        return str(e)
    
def get_uptime():
    try:
        uptime_output = os.popen("uptime -p").read().strip()
        words = uptime_output.split()
        word_mapping = {
            'days': 'd',
            'day': 'd',
            'hours': 'h',
            'hour': 'h',
            'minutes': 'm',
            'minute': 'm',
        }
        
        shortened_words = [word_mapping[word] if word in word_mapping else word for word in words]
        shortened_words = [word for word in shortened_words if word not in ['up', 'U']]
        shortened_output = ''.join(shortened_words)
        
        return shortened_output
    except Exception as e:
        return str(e)
    
def get_connected_ssid():
    try:
        # Execute the iwgetid command and capture the output
        ssid_output = os.popen("iwgetid -r").read().strip()
        if not ssid_output:
            ssid_output = "[Disconnected]"
        return ssid_output
    except Exception as e:
        return str(e)


def get_mem_free():
    try:
        mem_output = os.popen("free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'").read()
        return mem_output
    except Exception as e:
        return str(e)
    
def get_load_avg():
    try:
        load_output = os.popen("top -bn1 | grep load | awk '{print \"\", $11, $12, $13}'").read()
        return load_output
    except Exception as e:
        return str(e)

def get_QR_code(IP: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(IP)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((64, 64))
    return qr_img

def screen_wifi():
    #Get SSID
    SSID_str = get_connected_ssid()
    #Get IP
    IP_str = get_wlan0_ip()
    #Get Hostname
    hostname_str = get_hostname()
    #Get uptime
    uptime_str = get_uptime()
    
    # print it
    with canvas(device) as draw:
        draw.text((1,1), hostname_str, font=font_small, fill="white")
        draw.text((1,17), "SSID: "+ SSID_str, font=font, fill="white")
        draw.text((1,33), "IP: " + IP_str, font=font, fill="white")
        draw.text((1,49), "Uptime: "+ uptime_str, font=font, fill="white")
        

def screen_QR():
    #Get IP
    IP_str = get_wlan0_ip()
    #Get QR code TODO use qrcode lib.
    qr_img = get_QR_code("http://"+IP_str)
    with canvas(device) as draw:
        draw.text((1,1), "Webapp", font=font, fill="white")
        draw.bitmap((64, 0), qr_img, fill="white")

def screen_resources():
    #Get Mem
    mem_str = get_mem_free()
    #Get load avg
    load_avg_str = get_load_avg()
    
    with canvas(device) as draw:
        draw.text((1,1), "Load Average: ", font=font_small, fill="white")
        draw.text((20,17), load_avg_str, font=font_small, fill="white")
        draw.text((1,33), "RAM Used: ", font=font_small, fill="white")
        draw.text((20,49), mem_str, font=font_small, fill="white")

services=["mbot-start-network.service", "mbot-publish-info.service", "mbot-rplidar-driver.service", "mbot-lcm-serial.service", "mbot-web-server.service", "mbot-motion-controller.service","mbot-slam.service"]

def screen_services():
    for service in services:
        mem_output = os.popen("systemctl status " + service + " | head -3 | tail -1").read()
        print(service)
        print(mem_output.split())
       

def main():
    screen_resources()
    screen_services()
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()