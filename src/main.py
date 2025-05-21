from picamera2 import Picamera2
import cv2 as cv
import RPi.GPIO as GPIO
import time
from servo import ServoUtil
from detector import Detector, Mode
from tracker import Tracker2D

video_window = True

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={'format':'XRGB8888', 'size':(1920,1080)}))
camera.start()

# A0090

motor = ServoUtil(18)
motor.set_angle(90) # center motor

detector = Detector(Mode.FACE)
tracker = Tracker2D(detector, motor)
tracker.debug = True

# want a detect once every 10 frames
counter = 0

try:
    while True:
        counter += 1

        frame = camera.capture_array()

        frame = cv.rotate(frame, cv.ROTATE_180)

        if counter == 20:
            tracker.get_next_frame(frame)

            if detector.box_x != None:
                detector.draw()

            counter = 0

        if video_window:
            cv.imshow("Video feed", frame)
            if cv.waitKey(20) & 0xFF==ord('d'):
                break

except KeyboardInterrupt:
    motor.finish()

if video_window:
    motor.finish()
    cv.destroyAllWindows()
