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
    def __init__(self, detector, servo, dampening_factor=4, refresh_rate=5, debug=False):
        self.current_angle = 90
        self.detector = detector
        self.servo = servo
        self.dampening_factor = dampening_factor
        self.displacement = 0
        self.refresh_rate = refresh_rate
        self.debug = debug
        
        
    def get_next_frame(self, frame):
        """
        get_next_frame(None, None) -> None:
        updates the frame and the bounds of the object in the frame.
        """
        self.detector.get_next_frame(frame)
        
        if self.detector.box_x != None:
            self.find_displacement2D()
        
    def find_displacement2D(self):
        """
        find_displacement(None) -> None:
        finds the displacement of the object from the center of the frame to the center of the bounding box.
        if the object is to the left of the frame, the displacement will be negative. If the object is to the right
        of the frame, the displacement will be positive. The max displacement absolute value is half the width of the frame.
        """
        frame_center = self.detector.frame_width // 2
        box_center = self.detector.box_x + (self.detector.box_width // 2)
        self.displacement = frame_center - box_center

        print('displacement ' + str(self.displacement))
        print('servo angel: ' + str(self.current_angle))

        if self.displacement < -100:
            # If object is to the left of center, displacement is positive => decrease angle => turn right
            self.current_angle = min(180, self.current_angle - 1)
            self.servo.set_angle(self.current_angle)
        elif self.displacement > 100:
            # If object is to the right of center, displacement is negative => increase angle => turn left
            self.current_angle = max(0, self.current_angle + 1)
            self.servo.set_angle(self.current_angle)
        else:
            # 200 pixel dampening zone 
            print('center')
        self.detector.box_x = None
    
        
        

        
        
        
            
        
        
        
