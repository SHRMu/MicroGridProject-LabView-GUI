#!/usr/bin/python
from opcua import Server
from random import randint
import socket
import struct
#import datetime
import time

# retrieve the param.txt file from matlab program
# read all parameters from file param.txt
# build param_list = [[DS001], [DS002], [BT001], [PV001]]
def read_param_from_txt():
	param_list = []
	DS001_param_list = []
	DS002_param_list = []
	BT001_param_list = []
	PV001_param_list = []
	with open('param.txt', 'r') as file:
		data = file.readlines()
	for line in data:
		param = line[2:]
		param = param.split("'")[0]
		if "DS001" in param:
			DS001_param_list.append(param)
		elif "DS002" in param:
			DS002_param_list.append(param)
		elif "BT001" in param:
			BT001_param_list.append(param)
		else:
			PV001_param_list.append(param)
	param_list = [DS001_param_list, DS002_param_list, BT001_param_list, PV001_param_list]
	return param_list

def create_namespace_for_object(ns_list, param_list):
	object_list = []
	count = 0
	for ns in ns_list:
		# register 4 different namespace
		ns_name = "OPCUA_SIMULATION_SERVER_" + ns
		namespace = server.register_namespace(ns_name)

		# add object to ns_node
		object_item = server.get_objects_node().add_object(namespace, ns)

		for param in param_list[count]:
			# add variables to object and set writable
			object_item.add_variable(namespace, param, 0).set_writable()
		object_list.append(object_item)
		count = count + 1
	return object_list

if __name__ == '__main__':

	# Raspberry Pi IP adress
	Local_IP = "192.168.1.11"
	# used for UDP packet receiving
	Local_Port = 8001

	############################################## OPC Service ##############################################
	param_list = read_param_from_txt()

	server = Server()
	# start opc port in pi
	#opc_url = "opc.tcp://192.168.1.11:4840/"
	opc_url = "opc.tcp://" + Local_IP + ":4840/"
	server.set_endpoint(opc_url)

	# register namespaces for 4 diff devices
	namespace_list = ["DS001", "DS002", "Battery", "Photovoltaic"]
	object_list = create_namespace_for_object(namespace_list, param_list)

	#start opcua server
	server.start()
	print("OPCUA Server started at {}".format(opc_url))

	############################################## UDP Server Config ##############################################
	# UDP Server used for listening 
	#IP = "192.168.1.11"
	#PORT = 8001
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	address = (Local_IP, Local_Port)
	server_socket.bind(address)
	print("UDP server start at {}".format(Local_IP))

	############################################## UDP Client Config ##############################################
	# UDP target ip and port for sending data
	Target_IP = "192.168.1.22"
	PORT_send = 8002
	client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	try: 
		while True:
			############ 1 step : receive data from op4510 server #################
			receive_data, client_address = server_socket.recvfrom(80)
			print(receive_data)
			#unpack the data with double format
			receive_data = struct.unpack('dddddddddd', receive_data)
			print("received data from UDP : ", receive_data)

			############ 2 step : send parameters data to Labview #################
			#prepare parameters sent to the Labview
			data_list=[]
			#gas level 
			data_list.append(randint(10,60))
			for item in receive_data:
				#2 digits after dot
				data_list.append(float('%.3f' % (item)))

			#insert some missing parameters
			#Pmin, Pmax
			data_list.insert(3, 500)
			data_list.insert(4, 500)
			#opMode
			data_list.insert(5, 0)

			print ("parametsers data : ", data_list)

			#send data to labview with OPCUA protocal
			for object_item in object_list:
				var_list = object_item.get_variables()
				for var in var_list:
					# set node value
					index = var_list.index(var)
					var.set_value(float(data_list[index]))
					# get node info and node value
					#print(str(var) + " ---- " + str(var.get_value()))
				#print(object_item.get_display_name())

			############ 3 step : read the changed parameters from Labview #################
			kf_node = server.get_node("ns=2;i=8")
			kf_var = kf_node.get_value()
			tf_var = server.get_node("ns=2;i=9").get_value()
			kP_var = server.get_node("ns=2;i=10").get_value()

			print("changed kf_node value : ", kf_var, tf_var,kP_var)

			############ 4 step : send the changed value back to op4510 #################
			#client.sendto(struct.pack('d',kf_var),(Target_IP,PORT_send))
			client.sendto(struct.pack('dddddd',kf_var,tf_var,kP_var,4,5,6),(Target_IP,PORT_send))

			print("*" * 70)
			time.sleep(2)

	finally:
		server.stop()
