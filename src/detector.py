# Detector.py is responsible for object detection and recognition. At the moment
# there will be 3 modes of detection:

# - [ ] recognition tracking: detector will be trained on images of an person and track only them
# - [ ] motion tracking: detector will track anything moving in the frame
# - [ ] face tracking: detector will track faces

# Detector Class

# Design choice 
#  - have Detector start the video or have frames be passed into it?
#  
#  - 
import cv2 as cv
from enum import Enum

# Need an enum for mode 
class Mode(Enum):
    FACE = 1
    MOTION = 2   

class Detector:
    """
    Detector() 
    """
    def __init__(self, mode, xml_file=None):
        self.ret = None
        self.mode = mode
        self.frame = None
        self.ixl_file = xml_file
        self.bounds = None
        
    # get the next frame to be processed returns box corrds (x, y, w, h)
    def get_next_frame(self, ret, frame):
        self.ret = ret
        self.frame = frame
        
        if self.mode == Mode.FACE:
            self.face_dect()
        elif self.mode == Mode.MOTION:
            self.motion_dect()
        else:
            raise RuntimeError("Detector mode not recognized")
        
    def reginition_dect(self):
        pass

    def face_dect(self):
        haar_cascade = cv.CascadeClassifier("../out/haar_face.xml")
        
        # convert image to gray scale
        gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        
        aces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
        
        # face detected get the largest could change to getting the most acurate one
        self.bounds = None
        for (x, y, w, h) in aces_rect:
            if self.bounds == None:
                self.bounds = (x, y, w, h)
            elif (w * h) > self.bounds[2] * self.bounds[3]:
                self.bounds = (x, y, w, h)
                
    
    def motion_dect(self):
        pass