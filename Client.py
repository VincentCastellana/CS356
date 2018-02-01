#! /usr/bin/env python3
#Vincent Castellana
#vc259
#Section 6

from socket import *
import struct
import re
import sys, time

#sys.argv = [sys.argv[0], "127.0.0.1", 12007]

def program(address, port):
	packetsReceived = 0
	packetsLost = 0
	minRTT = 100000.0
	maxRTT = -1.0
	rttTotal = 0

	#https://docs.python.org/3/library/socket.html, slides
	clientSocket = socket(AF_INET, SOCK_DGRAM)
	clientSocket.settimeout(1)

	for i in range(1, 11):
		print("Pinging " + address + " " + str(port) + ":")
		before = time.clock() 												#https://docs.python.org/2/library/time.html
		clientSocket.sendto(struct.pack('!ii', 1, i), (address, port)) 		#https://docs.python.org/3/library/struct.html
		try:
			receivedMessage, serverAddress = clientSocket.recvfrom(port)
		except:
			print("Ping message number " + str(i) + " timed out")
			packetsLost+=1
		else:
			rtt = time.clock() - before
			rttTotal += rtt
			packetsReceived+=1
			if rtt < minRTT:
				minRTT = rtt
			if rtt > maxRTT:
				maxRTT = rtt
			print("Ping message number " + str(i) + ": " + str(rtt) + " seconds")
			
	print(str(i) + " packets sent, " + str(packetsReceived) + " packets received, " + str(packetsLost) + " packets lost (%" + str(float(packetsLost)/i*100) + " loss)")
	print("Minimum successful rtt: " + str(minRTT) + " seconds")
	print("Maximum successful rtt: " + str(maxRTT) + " seconds")
	print("Average rtt for all acknowledged ping packets: " + str(float(rttTotal)/packetsReceived) + " seconds")


if __name__ == '__main__':
	#check that first argument is in IP address format using regex
	#https://docs.python.org/2/library/re.html (using \A and \Z for exact match of whole expression)
	if re.match("\A([0-9]([0-9]?){3}\.){3}[0-9]([0-9]?){3}\Z", sys.argv[1]) is not None:
		address = sys.argv[1]
	else:
		print("Invalid IP address, please restart the application.")
		sys.exit(0)

	#check that second argument is a valid port number
	if 0 < int(sys.argv[2]) < 65535:
		port = sys.argv[2]
	else:
		print("Invalid port number, please restart the application.")
		sys.exit(0)

	program(address, port)