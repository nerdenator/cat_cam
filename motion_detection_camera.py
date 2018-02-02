#!/usr/bin/python3

from picamera import PiCamera
from time import sleep
import time
import datetime
import RPi.GPIO as GPIO
import os
import spidev

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Function to read SPI data from MCP3008 chip
def ReadChannel(channel):
	adc = spi.xfer2([1, (8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data
	
def ConvertVolts(data, places):
	volts = (data * 3.3) / float(1023)
	volts = round(volts, places)
	return volts
	
# Function to convert a voltage level
# rounded to specified number of decimal places.
def ConvertTemp(data, places):
	# ADC Value
	# (approx)  Temp    Volts
    # 0         -50     0.00
    # 78        -25     0.25
    # 155       0       0.50
    # 233       25      0.75
    # 310       50      1.00
    # 465       100     1.50
    # 775       200     2.50
    # 1023      280     3.30
	
	temp = ((data * 330) / float(1023)) - 50
	temp = round(temp, places)
	return temp

# Define sensor channels
temp_channel = 0	
	
# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN)	# Read output from PIR motion sensor

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.color_effects = (128, 128)

# TODO: try high ISO value for low light
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-in-low-light
# https://stackoverflow.com/questions/30063974/how-to-set-the-camera-in-raspberry-pi-to-take-black-and-white-image
print("Starting motion detection...")
while True:
	i = GPIO.input(40)
	if i == 0:
		sleep(.1)
	elif i == 1:
		# Read the temperature sensor data
		temp_level = ReadChannel(temp_channel)
		temp_volts = ConvertVolts(temp_level, 2)
		temp = ConvertTemp(temp_level, 2)
		ticks = int(time.time())
		datetime_stamp = datetime.datetime.now().time()
		text_str = '{}, {}°C'.format(datetime_stamp, temp)
		camera.annotate_text = str(text_str)
		print("Motion detected at %s" % datetime_stamp)
		camera.capture('/home/pi/Desktop/motioncamera/image%s.jpg' % ticks)
		sleep(.1)



