import cv2 as cv
from detector import Detector, Mode

capture = cv.VideoCapture(0)
detector = Detector(Mode.FACE)

while True:
    
    ret, frame = capture.read()
    detector.get_next_frame(ret, frame)
    
    if detector.bounds:
        x, y, w, h = detector.bounds
        print(f"{x}, {y}, {w}, {h}\n")
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)
    else:
        print("None")
        
    cv.imshow("Video feed", frame)
    
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
    
capture.release()
cv.destroyAllWindows()