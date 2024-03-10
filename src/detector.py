# Detector.py is responsible for object detection and recognition. At the moment
# there will be 3 modes of detection:

# - [x] recognition tracking: detector will be trained on images of an person and track only them
#   - ( ) create an iml file for traking yourself
# - [ ] motion tracking: detector will track anything moving in the frame TODO not sure how to acomplish if the frame
#       is also going to be moving
# - [x] face tracking: detector will track faces

import cv2 as cv
import os
from enum import Enum

# Need an enum for mode 
class Mode(Enum):
    FACE = 1
    MOTION = 2
    FILE = 3   
    
# Detector Class

class Detector:
    """
    Detector() 
    """
    def __init__(self, mode, xml_file_path=None):
        self.ret = None
        self.mode = mode
        self.ixl_file = xml_file_path
        self.frame = None
        self.frame_width = None
        self.frame_height = None
        self.box_x = None
        self.box_y = None
        self.box_width = None
        self.box_height = None
        
    # get the next frame to be processed returns box corrds (x, y, w, h)
    def get_next_frame(self, ret, frame):
        self.ret = ret
        self.frame = frame
        self.frame_width = self.frame.shape[1]
        self.frame_height = self.frame.shape[0]
        
        if self.mode == Mode.FACE:
            self.face_dect()
        elif self.mode == Mode.FILE:
            self.reginition_dect()
        else:
            raise RuntimeError("Detector mode not recognized")
        
    def reginition_dect(self):
        if os.path.exists(self.ixl_file):
            haar_cascade = cv.CascadeClassifier(self.ixl_file)
        
            # convert image to gray scale
            gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
            
            aces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
            
            # face detected get the largest could change to getting the most acurate one
            self.bounds = None
            for (x, y, w, h) in aces_rect:
                if self.bounds == None:
                    self.box_x = x
                    self.box_y = y
                    self.box_width = w
                    self.box_height = h
                elif (w * h) > self.bounds[2] * self.bounds[3]:
                    self.box_x = x
                    self.box_y = y
                    self.box_width = w
                    self.box_height = h
        else:
            raise RuntimeError("xml file not found")

    def face_dect(self):
        self.ixl_file = "../out/haar_face.xml"
        self.reginition_dect()
        
    def draw(self):
        """
        draws a bounding box around the object being tracked on the frame
        and a line from the center of the screen to the object
        """
        # bouning box dimensions
        
        cv.rectangle(self.frame, (self.box_x, self.box_y), (self.box_x+self.box_width, self.box_y+self.box_height), (0, 255, 0), thickness=2)
        
        cv.circle(self.frame, (self.box_x+self.box_width//2, self.box_y+self.box_height//2), 5, (0, 0, 255), thickness=10)
        
        # draw line from center of screen to object
        cv.line(self.frame, (self.frame_width//2, self.frame_height//2), (self.box_x+self.box_width//2, self.box_y+self.box_height//2), (0, 0, 255), thickness=2)      