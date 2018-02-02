#!/usr/bin/python3

from picamera import PiCamera
from time import sleep
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN)	# Read output from PIR motion sensor

#camera = PiCamera()
#camera.resolution = (1920, 1080)
#camera.color_effects = (128, 128)

# TODO: try high ISO value for low light
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-in-low-light
# https://stackoverflow.com/questions/30063974/how-to-set-the-camera-in-raspberry-pi-to-take-black-and-white-image
print("Starting motion detection...")
while True:
	i = GPIO.input(40)
	if i == 0:
		sleep(.1)
	elif i == 1:
		#ticks = int(time.time())
		datetime_stamp = datetime.datetime.now().time()
		#camera.annotate_text = str(datetime_stamp)
		print("Motion detected at %s" % datetime_stamp)
		#camera.capture('/home/pi/Desktop/motioncamera/image%s.jpg' % ticks)
		sleep(.1)



