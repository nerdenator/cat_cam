import picamera
from time import sleep
camera = picamera.PiCamera()
camera.resolution = (1920, 1080)
camera.color_effects = (128, 128)
camera.start_preview()
sleep(600)
