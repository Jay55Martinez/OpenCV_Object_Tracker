import sys
import os
import time
sys.path.append(os.path.abspath('../src'))
from servo import ServoUtil

motor = ServoUtil(18)

motor.set_angle(90) #center
time.sleep(1)
motor.set_angle(0) #left
time.sleep(1)
motor.set_angle(90) #center
time.sleep(1)
motor.set_angle(180) #right
time.sleep(1)
motor.set_angle(90) #center
time.sleep(1)

motor.finish()
