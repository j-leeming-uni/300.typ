import sys

sys.path.append('/home/jonathan/.cache/pypoetry/virtualenvs/pt-vQ9_wA6r-py3.12/lib64/python3.12/site-packages/')
sys.path.append('/home/jonathan/.cache/pypoetry/virtualenvs/pt-vQ9_wA6r-py3.12/lib/python3.12/site-packages/')

from scapy.all import *

# Define the target IP and broadcast MAC address
target_ips = {"192.168.2.1", "192.168.2.2"}
broadcast_mac = "ff:ff:ff:ff:ff:ff"


def decode_hint(hint: int):
    id = (hint & 0xf0) >> 4
    data = hint & 0x0f
    north = int(data & 0x08 > 0)
    south = int(data & 0x04 > 0)
    east = int(data & 0x02 > 0)
    west = int(data & 0x01 > 0)
    print(f'{id}: {north=} {south=} {east=} {west=}')


# Function to process captured packets
def packet_callback(packet):
    if IP not in packet:
        return
    if TCP not in packet:
        return
    if packet[IP].dst not in target_ips:
        return
    if packet[TCP].dport != 23:
        return
    if Raw not in packet:
        return
    data = packet[Raw].load[0]
    decode_hint(data)


sniff(iface="enp45s0u1u3", filter="tcp", prn=packet_callback, store=0)

