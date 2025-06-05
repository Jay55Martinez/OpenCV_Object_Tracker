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
        find_displacement2D(None) -> None:
        Computes the horizontal displacement of a detected object from the center of the frame
        and adjusts the servo angle to re-center the object.

        - Displacement is calculated as: frame_center - object_center
        - Positive displacement means object is to the left of center.
        - Negative displacement means object is to the right of center.
        - A ±100 pixel dead zone prevents unnecessary servo jitter.
        - Servo angle is adjusted within the range [0, 180].

        Behavior:
        - If object is left of center (displacement > 100): turn servo right (decrease angle)
        - If object is right of center (displacement < -100): turn servo left (increase angle)
        - If within center zone (abs(displacement) <= 100): do nothing
        """
        frame_center = self.detector.frame_width // 2
        box_center = self.detector.box_x + (self.detector.box_width // 2)
        self.displacement = frame_center - box_center

        print('displacement ' + str(self.displacement))
        print('servo angel: ' + self.current_angle)

        if self.displacement < -100:
            # Object is to the right of center → turn servo left
            self.current_angle = min(180, self.current_angle + 1)
            self.servo.set_angle(self.current_angle)
        elif self.displacement > 100:
            # Object is to the left of center → turn servo right
            self.currentgle = max(0, self.current_angle - 1)
            self.servo.set_angle(self.current_angle)
        else:
            # 200 pixel dampening zone
            print('Object is centered.')
        self.detector.box_x = None
    
        
        

        
        
        
            
        
        
        
