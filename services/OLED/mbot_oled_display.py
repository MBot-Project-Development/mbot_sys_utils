import os
import re
import psutil


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


def get_cpu_load():
    try:
        # Get the CPU load for each core
        cpu_load = psutil.cpu_percent(percpu=True)
        return cpu_load
    except Exception as e:
        return str(e)



def screen_wifi():
    #Get SSID
    SSID_str = get_connected_ssid()
    #Get IP
    IP_str = get_wlan0_ip()
    #Get Hostname
    hostname_str = get_hostname()
    #Get uptime
    uptime_str = get_uptime()
    print(uptime_str)

def screen_QR():
    #Get IP
    IP_str = get_wlan0_ip()
    #Get QR code TODO use qrcode lib.
    pass
    
def screen_resources():
    # Get and display the CPU load for each core
    cpu_load = get_cpu_load()
    if cpu_load:
        for core, load in enumerate(cpu_load):
            print(f"CPU Core {core}: {load}%")
    else:
        print("Failed to retrieve CPU load.")
    #Get CPU
    #Get Mem
    #Get load avg
    pass
    
def screen_services():
    #Get list of services 
    pass   

def main():
    screen_resources()

if __name__ == '__main__':
    main()