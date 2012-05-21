#!/usr/bin/python
import sys
import getopt
import os

try:
	import serial
except:
	print 'You are missing the pySerial package.  Please install from: ',
	print 'http://sourceforge.net/projects/pyserial/files/pyserial/2.5/'


def turnLightsOn(device):
	sendSerial(device, "61")

def turnLightsOff(device):
	sendSerial(device, "71")

def sendSerial(dev, msg):
	try:
		ser = serial.Serial(dev)
		ser.write(msg)
		ser.close()
	except IOError:
		print 'Could not send message.  Make sure device is properly connected'

def printHelp():
	print 'Simple python script to control the Wunderboard serial light controller.'
	print 'Usage: \n'
	print 'lightControl.py [-h] [-s on|off] [-d devPath] [--set on|off] [--device devPath]'
	print ''
	print '-h, --help         : Print this usage message'
	print '-s, --set-lights   : Set the lights on or off'
	print '-d, --device       : Specify a device to use.  Defaults to /dev/ttyUSB0'
	print ''


if __name__ == "__main__":
	state = None

	# figure out the default device based on the executing platform
	if os.name == 'posix':
		device = '/dev/ttyUSB0'
	elif os.name == 'nt':
		device = 3
	else:
		device = 'unknown'

	opts, args = getopt.getopt(sys.argv[1:], 'hs:d:', ['set-lights=', 'help', 'device'])
	
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			printHelp()
			sys.exit(0)
		elif opt in ('-s', '--set'):
			state = arg
		elif opt in ('-d', '--device'):
			if os.name = 'nt':
				device = int(arg)
			else:
				device = arg
		else:
			print 'Unknown option: %s' % opt

		if device == 'unknown':
			print 'Your serial device could not be auto-detected.  Please specify the correct device',
			print 'using the --device option, and run lightControl.py again.'
			sys.exit(1)


	if state.lower() == 'on':
		turnLightsOn(device)
	elif state.lower() == 'off':
		turnLightsOff(device)
