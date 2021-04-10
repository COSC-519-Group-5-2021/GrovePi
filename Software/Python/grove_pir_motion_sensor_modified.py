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
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
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
	
# 	retriggerable means the sensor will continue outputting high if motion was detected before the hold timer expires.
# 	non-retriggerable means the sensor will output high for the specified hold time only, then output low until motion is detected again.
# 	if there is constant motion detected, retriggerable will stay high for the res and non-retriggerable will oscillate between high/low.

import time
import datetime
import grovepi

# Connect the Grove PIR Motion Sensor to digital port D8
# NOTE: Some PIR sensors come with the SIG line connected to the yellow wire and some with the SIG line connected to the white wire.
# If the example does not work on the first run, try changing the pin number
# For example, for port D8, if pin 8 does not work below, change it to pin 7, since each port has 2 digital pins.
# For port 4, this would pin 3 and 4


pir_sensor = 8
#led = 4
motion=0
grovepi.pinMode(pir_sensor,"INPUT")
#grovepi.pinMode(led, "OUTPUT")

def execute(res):
	try:
		# Sense motion, usually human, within the target range
		motion= grovepi.pirRead(pir_sensor, options[res][1])
		if motion==0 or motion==1:	# check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
			if motion==1:
				#grovepi.digitalWrite(led, 1)
				print ('Motion Detected', time.ctime())
			else:
				#grovepi.digitalWrite(led, 0)
				print ('-')
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise

def getSetting():
	while True:
		res = input("\nUse selected duration settings from [1 - 3]: \n \t 1. High \n \t 2. Medium \n \t 3. Low \n")
		if res.isdigit():
			res = int(res)
			if (1 <= res <= 3):
				print("The program will run on {0} setting...\n".format(options[res][0]))
				return res
			else:
				print("'{0}' is an invalid number.\n \n".format(res))
		else:
			print("'{0}' is not a number.\n \n".format(res))

def instant():
	res = getSetting()
	while True:
		execute(res)

def elapse():
	elapseTime = int(input("How long would you like the program to run (in minutes): \n"))
	curr = datetime.datetime.now()
	stop = curr + datetime.timedelta(minutes=elapseTime)
	
	res = getSetting()
	while datetime.datetime.now() < stop:
		execute(res)
	
	print("Set time elapsed!")
	

modes = {1: ["Elapsed", elapse], 2: ["Instant", instant]}
options = {1: ["High", .2], 2: ["Medium", 1.2], 3: ["Low", 2]}

while True:
	res = input("Please select a mode to run on: \n \t 1. Elapsed \n \t 2. Instant \n")
	if res.isdigit():
		res = int(res)
		if (1 <= res <= 2):
			print("The program will run on {0} mode...\n".format(modes[res][0]))
			modes[res][1]()
			break
		else:
			print("'{0}' is an invalid number.\n \n".format(res))
	else:
		print("'{0}' is not a number.\n \n".format(res))