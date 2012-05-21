#!/usr/bin/python
import sys
import getopt
import os

HOME_AUTO_BASE = 0x00
HOME_AUTO_SUCCESS = HOME_AUTO_BASE
HOME_AUTO_FAIL_NODEVICE = HOME_AUTO_BASE + 1
HOME_AUT0_FAIL_UNKNOWN_OPTION = HOME_AUTO_BASE + 2


try:
	import serial
except:
	print 'You are missing the pySerial package.  Please install from:\n',
	print 'http://sourceforge.net/projects/pyserial/files/pyserial/2.5/'


def turnLightsOn(device):
	ret = HOME_AUTO_SUCCESS
	ret = sendSerial(device, "61")
	return ret

def turnLightsOff(device):
	ret = HOME_AUTO_SUCCESS
	ret = sendSerial(device, "71")
	return ret

def sendSerial(dev, msg):
	ret = HOME_AUTO_SUCCESS
	try:
		ser = serial.Serial(dev)
		ser.write(msg)
		ser.close()
	except IOError:
		print 'Could not send message.  Make sure device is properly connected'
		ret = HOME_AUTO_FAIL_NODEVICE
	return ret

def _printHelp():
	print 'Simple python script to control the Wunderboard serial light controller.'
	print 'Usage: \n'
	print 'lightControl.py [-h] [-s on|off] [-d devPath] [--set on|off] [--device devPath]'
	print ''
	print '-h, --help         : Print this usage message'
	print '-s, --set-lights   : Set the lights on or off'
	print '-d, --device       : Specify a device to use.  Defaults to /dev/ttyUSB0'
	print ''

def _main():
	state = None
	ret = HOME_AUTO_SUCCESS
	#print ret

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
			_printHelp()
			sys.exit(HOME_AUTO_SUCCESS)
		elif opt in ('-s', '--set'):
			state = arg
		elif opt in ('-d', '--device'):
			if os.name == 'nt':
				device = int(arg)
			else:
				device = arg
		else:
			print 'Unknown option: %s' % opt
			_printHelp()
			sys.exit(HOME_AUT0_FAIL_UNKNOWN_OPTION)

		if device == 'unknown':
			print 'Your serial device could not be auto-detected.  Please specify the correct device',
			print 'using the --device option, and run lightControl.py again.'
			sys.exit(HOME_AUTO_NODEVICE)


	if state.lower() == 'on':
		ret = turnLightsOn(device)
	elif state.lower() == 'off':
		ret = turnLightsOff(device)
	#print ret
		
	return ret

if __name__ == "__main__":	
	ret = _main()
	#print ret
	sys.exit(ret)

