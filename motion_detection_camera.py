from picamera import PiCamera
from time import sleep
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)	# Read output from PIR motion sensor

camera = PiCamera()
camera.resolution = (720,480)
#camera.start_preview()
while True:
	i = GPIO.input(11)
	if i == 0:
		sleep(.1)	
	elif i == 1:
		
		ticks = int(time.time())
		datetime_stamp = datetime.datetime.now().time()
		camera.annotate_text = str(datetime_stamp)
		print("Motion detected at %s" % datetime_stamp)
		camera.capture('/home/pi/Desktop/motioncamera/image%s.jpg' % ticks)
		sleep(.1)



