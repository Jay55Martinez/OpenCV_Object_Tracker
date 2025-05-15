import sys
import os
import time
import RPi.GPIO as GPIO
sys.path.append(os.path.abspath('../src'))
from servo import ServoUtil

gpio = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio, GPIO.OUT)

servo = GPIO.PWM(gpio, 50)

servo.start(0)
time.sleep(1)
servo.ChangeDutyCycle(5)
time.sleep(1)
servo.ChangeDutyCycle(10)
time.sleep(1)
servo.ChangeDutyCycle(0)

servo.stop()
GPIO.cleanup(gpio)