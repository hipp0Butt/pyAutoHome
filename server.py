#!/usr/bin/python

import socket
import os
import sys
import signal
import select
import pickle
import commands

HOST = '0.0.0.0'
PORT = 6969
BACKLOG = 5
LOGFILE = './server.log'
BUFSIZE = 1024

# Stuff used for packet structure
HEAD = 0
OPCODE = 1

# Possible values for HEAD
LIGHTS = '0'

# OPCODES for LIGHTS
COMMAND_LIGHTS_ON = '0'
COMMAND_LIGHTS_OFF = '1'

running = True
logfile = None

def log(file, string):
	file.write(string)
	file.write('\n')
	print string

def handler(signum, frame):
	log(logfile, 'Interrupt detected.  Stopping server')
	global running
	running = False

def runSystemCall(call):
	ret = os.system(call)
	if ret != 0:
		log(logfile, 'System call failed: ' + call)
	return ret

def processPacket(packet):
	ret = 0
	# Defines a light control packet
	# format is: [ HEAD, OPCODE, ...]
	if packet[HEAD] == LIGHTS:
		if packet[OPCODE] == COMMAND_LIGHTS_ON:
			# Code to turn on the lights
			print 'Lights on'
			ret = runSystemCall('./lightControl.py -s on')
		elif packet[OPCODE] == COMMAND_LIGHTS_OFF:
			# Code to turn off the lights
			print 'Lights off'
			ret = runSystemCall('./lightControl.py -s off')
		else:
			log(logfile, "Unknown option for light control: " + str(packet[OPCODE]))
	else:
		log(logfile, "Uknown HEAD option: " + packet[HEAD])	
	return ret

def sendPacket(packet, sock):
	# TODO: Enable the sending of packets
	log(logfile, 'Sending packets is not yet implemented')

def main():
	global logfile
	global running
	data = ''
	recv = True
	
	# Open the logfile
	logfile = open(LOGFILE, 'w')

	# Set the signal handler
	signal.signal(signal.SIGINT, handler)
	signal.signal(signal.SIGQUIT, handler)
	signal.signal(signal.SIGHUP, handler)
	
	# Configure the socket
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serv.bind((HOST, PORT))
	serv.listen(BACKLOG)
	
	log(logfile, "Server listening on port: " + str(PORT))

	pot_readers = [serv]
	
	while running:
		#try:
			# Check for clients using select
			ready_to_read, ready_to_write, execption \
			    = select.select(pot_readers, [], [])
			for x in ready_to_read:
				if x == serv:
					# Handle a new client connection
					conn, addr = serv.accept()
					pot_readers.append(conn)
					log(logfile, "Accepting new client: " + str(conn.getpeername()))
				else:
					# This is coming from a client that we know about.  Figure out
					# where it's coming from and what they want
					data = x.recv(BUFSIZE)
					if data:
						while (data[-1] != '\n'):
							# Make sure we have the whole packet
							data += x.recv(BUFSIZE)
						pckt = data.rstrip().split(';')
						ret = processPacket(pckt)
						x.send(str(ret) + '\n')
						x.close()
		#except e:
		#	log(logfile, "ERROR: " + str(e))
		#	sys.exit(1)
	# Shut down the server (should only happen on interrupt)
	for s in pot_readers:
		s.close()
	logfile.close()


if __name__ == '__main__':
	main()
