import cv2 as cv
from detector import Detector, Mode
from tracker import Tracker2D

capture = cv.VideoCapture(0)
detector = Detector(Mode.FACE)
tracker = Tracker2D(detector)

while True:
    
    ret, frame = capture.read()
    tracker.get_next_frame(ret, frame)
    
    if detector.box_x != None:
        detector.draw()
    else:
        print("None")
        
    cv.imshow("Video feed", frame)
    
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
    
capture.release()
cv.destroyAllWindows()