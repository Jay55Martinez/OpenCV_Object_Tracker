from picamera2 import Picamera2
import cv2 as cv
from detector import Detector, Mode
from tracker import Tracker2D

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={'format':'XRGB8888', 'size':(3280,2464)}))
camera.start()

detector = Detector(Mode.FACE)
tracker = Tracker2D(detector)
tracker.debug = True

while True:
    
    frame = camera.capture_array()
    tracker.get_next_frame(frame)
    
    if detector.box_x != None:
        detector.draw()
        
    cv.imshow("Video feed", frame)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
    
cv.destroyAllWindows()
