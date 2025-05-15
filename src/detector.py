# Detector.py is responsible for object detection and recognition. At the moment
# there will be 3 modes of detection:

# - [x] recognition tracking: detector will be trained on images of an person and track only them
#   - ( ) create an iml file for traking yourself
#   - ( ) implement YeNet for face detection
# - [x] face tracking: detector will track faces

import cv2 as cv
import os
import numpy as np
from enum import Enum

# Need an enum for mode 
class Mode(Enum):
    FACE = 1
    MOTION = 2
    FILE = 3  
    RAW = 4 
    YUNET = 5
    
# Detector Class

class Detector:
    """
    Detector() 
    """
    def __init__(self, mode, xml_file_path=None):
        self.mode = mode
        self.ixl_file = xml_file_path
        self.frame = None
        self.frame_width = None
        self.frame_height = None
        self.box_x = None
        self.box_y = None
        self.box_width = None
        self.box_height = None
        
        # initialize the detection model based on the mode
        self.detection_model = None
        
        if self.mode == Mode.FACE:
            self.ixl_file = "../out/haar_face.xml"
            self.detection_model = cv.CascadeClassifier(self.ixl_file)
        elif self.mode == Mode.FILE:
            self.detection_model = cv.CascadeClassifier(self.ixl_file)
        elif self.mode == Mode.RAW:
            pass
        elif self.mode == Mode.YUNET:
            self.ixl_file = "../out/face_detection_yunet_2022mar.onnx"
            self.detection_model = cv.FaceDetectorYN.create(self.ixl_file,  '', (0, 0))          
        
    # get the next frame to be processed returns box corrds (x, y, w, h)
    def get_next_frame(self, frame):
        self.frame = frame
        self.frame_width = self.frame.shape[1]
        self.frame_height = self.frame.shape[0]
        
        if self.mode == Mode.FACE:
            self.reginition_dect()
        elif self.mode == Mode.FILE:
            self.reginition_dect()
        elif self.mode == Mode.RAW:
            self.no_dect()
        elif self.mode == Mode.YUNET:
            self.face_dect_YuNet()
        else:
            raise RuntimeError("Detector mode not recognized")
        
    def reginition_dect(self):
        # convert image to gray scale
        gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        
        aces_rect = self.detection_model.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
        
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

    def no_dect(self):
        '''
        No detection algorithm will run. Box will be drawn in the center of the screen.
        '''
        # draw box in center of screen
        self.box_x = int(self.frame_width/2)
        self.box_y = int(self.frame_height/2)
        
        # width and height of box
        self.box_width = 100
        self.box_height = 100
        
    def face_dect_YuNet(self):
        '''
        Face detection using YuNet
        --------------------------
        YuNet is a lightweight face detection model that is designed to run using a CPU.
        '''
        rgb_image = cv.cvtColor(self.frame, cv.COLOR_RGBA2RGB)

        self.detection_model.setInputSize([self.frame_width, self.frame_height])
        
        _, faces = self.detection_model.detect(rgb_image)
        
        # face detected get the largest could change to getting the most acurate one
        self.bounds = None
        
        if faces is not None:
            for face in faces:
                # Extract the bounding box coordinates
                coords = face[:-1].astype(np.int32)
                
                # reused code 
                if self.bounds == None:
                    self.box_x = coords[0]
                    self.box_y = coords[1]
                    self.box_width = coords[2]
                    self.box_height = coords[3]
                elif (coords[2] * coords[3]) > self.bounds[2] * self.bounds[3]:
                    self.box_x = coords[0]
                    self.box_y = coords[1]
                    self.box_width = coords[2]
                    self.box_height = coords[3]
        
        
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