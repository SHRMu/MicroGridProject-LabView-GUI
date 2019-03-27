import socket
import random
import struct
import time

if __name__ == '__main__':
	IP = "192.168.1.100"
	PORT = 8002
	client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	while True:
	    msg = 12
	    client.sendto(struct.pack('d',msg),(IP, PORT))
	    print("send data")
	    time.sleep(10)
