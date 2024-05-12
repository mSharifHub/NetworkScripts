#!/usr/bin/env python
import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac-address", dest="mac_address", help="new MAC address")
    options_, arguments = parser.parse_args()
    if not options_.interface:
        options_.interface = input("Enter the network interface (e.g., eth0): ")

    if not options_.mac_address:
        options_.mac_address = input("Enter the new MAC address (e.g., 22:33:44:99:66:77): ")
    return options_


def is_valid_mac(mac):
    pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})')
    return pattern.match(mac)


options = get_arguments()

interface = options.interface
new_mac = options.mac_address

if not is_valid_mac(new_mac):
    print("Invalid MAC address format")
    exit()

commands = [
    f"ifconfig {interface} down",
    f"ifconfig {interface} hw ether {new_mac}",
    f"ifconfig {interface} up"
]


for command in commands:
    result = subprocess.call(command, shell=True)
    if result != 0:
        print(f"Command `{command}` failed with exit code {result}")
        break
