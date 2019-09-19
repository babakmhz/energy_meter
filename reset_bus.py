import RPi.GPIO as GPIO
import time
import os

while 1==1:

    if (os.path.isdir("/sys/bus/w1/devices/28-xxxxxxxxxx") == False):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, GPIO.LOW)
        time.sleep(3)
        GPIO.output(17, GPIO.HIGH)
        time.sleep(5)


