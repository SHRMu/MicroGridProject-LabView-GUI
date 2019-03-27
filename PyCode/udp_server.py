import socket
import struct

if __name__ == '__main__':
	Local_IP = "192.168.1.11"
	Local_PORT = 8001
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	address = (Local_IP, Local_PORT)
	server_socket.bind(address)
	print("udp server start ...")
	while True:
		receive_data, client_address = server_socket.recvfrom(1024)
		#receive_data = struct.unpack('u', receive_data)
		#float(receive_data[0])
		print ("msg :", receive_data)

