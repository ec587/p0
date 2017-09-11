#!/usr/bin/env python
"""
get: returns messages
alive: returns alive
broadcast(message): stores a new message
"""

import os
import signal
import subprocess
import sys
import time
import select
# from socket import SOCK_STREAM, socket, AF_INET
import socket
from threading import Thread

address = 'localhost'

args = sys.argv
pid = args[1]
n = int(args[2])
masterPort = int(args[3])
# serverPort = 20000 + int(pid)
messages = []
alive = [None] * n # connection list
allports = list(range(20000, 20000 + n))
del allports[int(pid)]
masterConnection = None

masterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
masterSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(pid, "socket created")
try:
	masterSocket.bind((address, masterPort))
	print(pid, "socket bound to", masterPort)
except Exception as e:
	print("Can't bind", pid, "to port", masterPort, e)

# for port in allports:
# 	try:
# 		# announce
# 		success = masterSocket.connect((address,port)) 
# 		masterSocket.send(str(pid).encode("utf8"))
# 	except Exception as e:
# 		print(port, "exception = ", e)
# 	finally:
# 		masterSocket.close()
# 		masterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 		print(pid, "socket recreated")

masterSocket.listen(10)
print(pid, "masterSocket listening")
masterSocket.setblocking(0)

poll = select.poll()
poll.register(masterSocket.fileno(), select.POLLIN)

while True:
	events = poll.poll(1.0)
	for fd, event in events:
		if fd == masterSocket.fileno(): # new connection
			connection, address = masterSocket.accept()
			print(pid, "received new connection from", address)
			masterConnection = connection
		print(fd)
		# elif event & POLLHUP:
		# 	alive[address - 20000].close()
		# 	alive[address - 20000] = None
			# message = alive[address - 20000].recv(16)
			# if message:
			# 	print(pid, "received message", message, "from live server", socket)
			# 	messages.append(message)
	# try:
	# 	connection, address = server.accept()
	# 	print(pid, "received new connection from", address)
	# 	data = connection.recv(16)
	# 	if data:
	# 		print(data)
	# 		# print(int(data.decode("utf8")))
	# 		# connection.setblocking(0)
	# 		# alive[int(data.decode("utf8"))] = connection
	# 		# connection.send(str("HEARTBEAT " + pid).encode("utf8"))
	# except Exception as e:
	# 	print(e)

# send heartbeat to alive
# for connection in alive:
# 	try:
# 		if(connection):
# 			print(connection)
# 			success = connection.send(str("HEARTBEAT " + pid).encode("utf8"))
# 			print(success)
# 	except Exception as e:
# 		print(pid, "can't send to", port, e)


# print(pid, "polling...")
# events = poll.poll(1.0)
# for fd, event in events:
# 	print(pid,"received fd", fd, " with events", events)
# 	if fd == server.fileno():
# 		connection, address = server.accept()
# 		print(pid, "received new connection from", address)
# 		connection.settimeout(1.0)
# 		alive[address - 20000] = connection
# 	elif event & select.POLLIN:
# 		message = alive[address - 20000].recv(16)
# 		if message:
# 			print(pid, "received message", message, "from live server", socket)
# 			messages.append(message)
# 	elif event & POLLHUP:
# 		alive[address - 20000].close()
# 		alive[address - 20000] = None

# # send heartbeat
# for port in allports:
# 	try:
# 		success = server.(bytes(pid),(address,port))
# 		print(success)
# 	except Exception as e:
# 		print(pid, "to", port, e)

# server.settimeout(1.0) # set 1 second timeout for select call
# read, write, exception = select.select(allports, allports, allports)
# for socket in read:
# 	if socket == server:
# 		connection, address = server.accept()
# 		print(pid, "received new connection from", address)
# 		connection.settimeout(1.0)
# 		alive[address - 20000] = True
# 	else: 
# 		message = socket.recv(16)
# 		if message:
# 			# check if socket is masterPort?
# 			print(pid, "received message", message, "from live server", socket)
# 			messages.append(message)
# 		else:
# 			socket.close()