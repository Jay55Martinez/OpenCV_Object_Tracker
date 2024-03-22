# Tracker2D is a wrapper object that wraps around to Detector. It is responsible for sending signals to
# a servo to track the object in the frame. 

# Tracker2D only moves across the x axis. (left and right)
# anything to the left of the frame is negative, anything to the right is positive.
# Given a dampening factor, the Tracker2D will adjust the servo to keep the object in the center of the frame.
import cv2 as cv

class Tracker2D:
    """
    Tracker(Detector, float) -> Tracker2D:
    detector: (Detector) object used to detect objects in the frame and store the bounds
    
    dampening_factor: (float) a value between 0 and 1 that will be used to adjust the servo sensitivity
    of how close to the center of the frame the object should be.
    """
    def __init__(self, detector, dampening_factor=0.5, refresh_rate=5, debug=False):
        self.detector = detector
        self.dampening_factor = dampening_factor
        self.displacement = 0
        self.refresh_rate = refresh_rate
        self.debug = debug
        
        
    def get_next_frame(self, ret, frame):
        """
        get_next_frame(None, None) -> None:
        updates the frame and the bounds of the object in the frame.
        """
        self.detector.get_next_frame(ret, frame)
        self.find_displacement()
        
    def find_displacement(self):
        """
        find_displacement(None) -> None:
        finds the displacement of the object from the center of the frame to the center of the bounding box.
        if the object is to the left of the frame, the displacement will be negative. If the object is to the right
        of the frame, the displacement will be positive. The max displacement absolute value is half the width of the frame.
        """
        frame_center = self.detector.frame_width // 2
        box_center = self.detector.box_x + (self.detector.box_width // 2)
        
        self.displacement = frame_center - box_center
        # TODO: add a dampening factor to the displacement

        
    
        
        

        
        
        
            
        
        
        