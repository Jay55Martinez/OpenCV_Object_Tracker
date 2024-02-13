# tracker.py will draw bounding boxs around the tracked object and computing
# how many pixels (units) the object is displaced from the center of the screen

# Class Tracker
# - [ ] update method: takes in bounds of detected object from detector 
# - [ ] draw method: draws the bounding box onto the frame
# - [ ] get_displacement: ...

class Tracker:
    """Tracker()"""
    def __init__(self, frame_width=None, frame_height=None, draw_box=False):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.draw_box = draw_box
        self.box_x = None
        self.box_y = None
        self.box_width = 1
        self.box_height = 1
        self.displacement_filter = None
        self.displacement = 0
    
    def update(self, box_corrds):
        if box_corrds != None:
            self.box_x = box_corrds[0]
            self.box_y = box_corrds[1]
            self.box_width = box_corrds[2]
            self.box_height = box_corrds[3]
            
            self.displacement = self.find_displacement()
        else:
            self.displacement = 0
            
    # left of the center of the screen will have (-) displacement
    # right of the center of the screen will have (+) displacement
    def find_displacement(self):
        center = self.frame_width/2
        
        if self.box_x < center:
            pass
            
        
        
        