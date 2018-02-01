#! /usr/bin/env python3
#Vincent Castellana
#vc259
#Section 6

from socket import *
import struct
import re
import sys, time
from random import randint

port = 12007

serverSocket = socket(AF_INET, SOCK_DGRAM) #https://docs.python.org/3/library/socket.html, slides
serverSocket.bind(('', port))

print("The server is ready to receive on port: " + str(port))
while True:
	#https://docs.python.org/3/library/struct.html, https://docs.python.org/3/library/socket.html
	receivedMessage, clientAddress = serverSocket.recvfrom(port)
	sequenceNumber = struct.unpack("!ii", receivedMessage)[1]
	if randint(0, 10) < 3: #to simulate packet loss when pinging same machine
		time.sleep(1)
		print("Message with sequence number " + str(sequenceNumber) + " dropped")
	else:
		print("Responding to ping request with sequence number", sequenceNumber)
		serverSocket.sendto(struct.pack('!ii', 2, sequenceNumber), clientAddress) #this packs and sends 2 and the sequence number attained from unpacking the receivedMessage
