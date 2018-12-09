#!/usr/bin/python
from opcua import Server
from random import randint
#import datetime
import time

# retrieve the param.txt file from matlab program
# read all parameters from param.txt
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

# only used for Diesel 1
def set_param_value(count, var):
	# GasLevel, SOC, solIrr
	if count == 1:
		var.set_value(randint(0, 100))
	# P0
	elif count == 2:
		var.set_value(randint(25, 35))
	# f0
	elif count == 3:
		var.set_value(50)
	# Pmin
	elif count == 4:
		var.set_value(randint(10,25))
	# Pmax
	elif count == 5:
		var.set_value(randint(45,60))
	# opMode
	elif count == 6:
		var.set_value("Following")
	# f
	elif count == 14:
		var.set_value(randint(45,55))
	# P kf, tf, kP, tP, Ki, Kp
	else:
		var.set_value(randint(10, 60))

# used for Diesel 2, Battery, Photovoltaic
# because some params can be shared with Diesel 1
def set_diff_param_value(count, var):
	if count == 1:
		var.set_value(randint(0, 10))

if __name__ == '__main__':

	param_list = read_param_from_txt()

	server = Server()

	url = "opc.tcp://192.168.1.11:4840/"
	server.set_endpoint(url)

	# register namespaces for 4 diff devices
	namespace_list = ["DS001", "DS002", "Battery", "Photovoltaic"]

	object_list = create_namespace_for_object(namespace_list, param_list)

	#Temp = Param.add_variable(ns_DS001, "Temperature", 0)
	#Press = Param.add_variable(ns_DS001, "Pressure", 0)
	#Time = Param.add_variable(ns_DS001, "Time", 0)

	#Temp.set_writable()
	#Press.set_writable()
	#Time.set_writable()

	server.start()
	print("Server started at {}".format(url))

	try: 
	    while True:
			#Temperature = randint(10, 50)
			#Pressure = randint(200, 999)
			
			#TIME = datetime.datetime.now()
			
			#print(Temperature,Pressure,TIME)

			#Temp.set_value(Temperature)
			#Press.set_value(Pressure)
			#Time.set_value(TIME)

			diff_flag = False
			for object_item in object_list:
				var_list = object_item.get_variables()
				count = 1
				for var in var_list:
					if diff_flag:
						set_diff_param_value(count, var)
					else:
						set_param_value(count, var)
					count = count + 1
				print(object_item.get_display_name())
				diff_flag = True
			print("*" * 70)
			time.sleep(2)

	finally:
	    server.stop()