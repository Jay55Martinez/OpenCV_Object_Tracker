from picamera2 import Picamera2
import cv2 as cv
import RPi.GPIO as GPIO
import time
from servo import ServoUtil
from detector import Detector, Mode
from tracker import Tracker2D

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={'format':'XRGB8888', 'size':(3280,2464)}))
camera.start()

# A0090
motor = ServoUtil(11, 50, 2.5, 7.5, 12)
print('here')
time.sleep(2)
motor.set_angle(0) # left -90 degrees 
print('here')
time.sleep(2)
motor.set_angle(90) # center 
print('here')
time.sleep(2)
motor.set_angle(180) # right 90 degrees

detector = Detector(Mode.RAW)
tracker = Tracker2D(detector)

while True:
    
    frame = camera.capture_array()
    tracker.get_next_frame(frame)
    
    if detector.box_x != None:
        detector.draw()
        
    cv.imshow("Video feed", frame)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
    
cv.destroyAllWindows()
motor.finish()
GPIO.cleanup()