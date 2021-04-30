#!/usr/bin/env python
#
# GrovePi Example for using the Grove PIR Motion Sensor (http://www.seeedstudio.com/wiki/Grove_-_PIR_Motion_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without modetriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPmodeS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
# NOTE:
# 	There are also 2x potentiometers on the board for adjusting measuring distance and hold time
# 	Rotate the pot labelled "Delay time" clockwise to decrease the hold time (0.3s - 25s)
# 	Rotate the pot labelled "Distance" clockwise to decrease the measuring distance (10cm - 6m)
	
# 	There are multiple revisions of this board with different components for setting retriggerable/non-retriggerable.
# 	Revision 1.0 contains a switch and revision 1.2 contains a jumper hat.
# 	The 1.0 switch board is labelled with H,L - H=retriggerable, L=non-retriggerable.
# 	The 1.2 jumper board has a pin diagram printed on the back.
	
# 	retriggerable means the sensor will continue outputting high if motion was detected before the hold timer expimode.
# 	non-retriggerable means the sensor will output high for the specified hold time only, then output low until motion is detected again.
# 	if there is constant motion detected, retriggerable will stay high for the mode and non-retriggerable will oscillate between high/low.

import sys
import time
import datetime
import grovepi
import logging
import os
import argparse

# Connect the Grove PIR Motion Sensor to digital port D8
# NOTE: Some PIR sensors come with the SIG line connected to the yellow wire and some with the SIG line connected to the white wire.
# If the example does not work on the first run, try changing the pin number
# For example, for port D8, if pin 8 does not work below, change it to pin 7, since each port has 2 digital pins.
# For port 4, this would pin 3 and 4

def execute(mode):
	try:
		# Sense motion, usually human, within the target range
		motion= grovepi.pirRead(pir_sensor, options[mode][1])
		if motion==0 or motion==1:	# check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
			if motion==1:
				if args.led == 1:
					grovepi.digitalWrite(led, 1)
				print ('Motion Detected', time.ctime())
				logging.info('Motion Detected')
			else:
				grovepi.digitalWrite(led, 0)
				print ('-')
	except Exception as e:
		print("Unexpected error:", e)
		logging.error('Unexpected error: %s', e)
		raise
		
def getSetting(arg):
	if arg:
		setting = arg		
		if (1 <= setting <= 3):		
			print("Setting:"+str(args.setting))
			return setting
		else:
			print("'{0}' is an invalid number.\n \n".format(mode))
			parser.print_help(sys.stderr)
			sys.exit(1)
	else:
		while True:
			setting = input("\nSelect a sensitivity level from [1 - 3]: \n \t 1. High \n \t 2. Medium \n \t 3. Low \n")
			if setting.isdigit():
				setting = int(setting)
				if (1 <= setting <= 3):
					print("The program will run on {0} setting...\n".format(options[setting][0]))
					return setting
				else:
					print("'{0}' is an invalid number.\n \n".format(setting))
			else:
				print("'{0}' is not a number.\n \n".format(setting))

def instant():
	if args.setting:
		mode = getSetting(args.setting)
	else:
		mode = getSetting(0)
	while True:
		execute(mode)

def setTimer():
	curr = datetime.datetime.now()
	if args.timer:
		print("Timer:"+str(args.timer)+" Minute(s)")
		time = args.timer
	else:
		time = int(input("How long would you like the program to run (in minutes): \n"))
		
	if args.setting:
		mode = getSetting(args.setting)
	else:
		mode = getSetting(0)

	stop = curr + datetime.timedelta(minutes=time)
	while datetime.datetime.now() < stop:
		execute(mode)
	
	print("Program completed!")
	logging.info('Timer stopped. Exiting.')

def keyboardInterrupt():
	print("\nexiting due to keyboard interrupt\n")
	logging.info('Exiting due to keyboard interrupt')


def main():
	try:
		if args.timer:
			modes[1][1]()
		else:	
			time = input("Do you want to set a timer? Y/n \n")
			if time.upper() == "Y":
				print("The program will run with a timer...\n".format(modes[1][0]))
				modes[1][1]()
			else:
				modes[2][1]()

	except KeyboardInterrupt:
		grovepi.digitalWrite(led, 0)
		keyboardInterrupt()


if __name__ == "__main__":

	pir_sensor = 8
	led = 4
	motion=0
	grovepi.pinMode(pir_sensor,"INPUT")
	grovepi.pinMode(led, "OUTPUT")

	#Get the path from which the script is executing
	script = os.path.realpath(__file__)
	path = os.path.dirname(script)

	#Configure the Python logger
	logging.basicConfig(filename= path + '/grove_pir_motion_sensor/grove_pir_motion_sensor.log', 
		format='%(asctime)s - %(levelname)s - %(message)s',
		level=logging.INFO)

	# From https://stackoverflow.com/questions/40419139/argparse-add-example-usage
	example_text = '''example:

	python3 grove_pir_motion_sensor_modified.py -m 1
	python3 grove_pir_motion_sensor_modified.py -t 20 -m 1
	python3 grove_pir_motion_sensor_modified.py -t 20 -m 1 -l 0'''
	# END

	parser = argparse.ArgumentParser(prog='PIR motion sensor', description='Configurable motion sensor',epilog=example_text,formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-t', '--timer', nargs='?', type=int, metavar='timer', help="Set timer")
	parser.add_argument('-s', '--setting', nargs='?', type=int, metavar='mode', help="Sensitivity level from [1 - 3]: \n \t 1. High \n \t 2. Medium \n \t 3. Low \n")
	parser.add_argument('-l', '--led', nargs='?', type=int, metavar='led', help="Set LED: \n 0. Off \n \t 1. On \n ")
	args = parser.parse_args()

	modes = {1: ["Set Timer", setTimer], 2: ["Instant", instant]}
	options = {1: ["High", .2], 2: ["Medium", 1.2], 3: ["Low", 2]}

	main()

