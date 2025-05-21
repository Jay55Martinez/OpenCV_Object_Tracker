import pigpio
import time

'''
Micro Servo 9g A0090:
50 - left -90 degrees
1500 - center 0 degrees
2500 - right 90 degrees
'''

class ServoUtil:
    '''
    ServoUtil(GPIO_Pin, Left, Center, Right)

    - Uses pigpio for smooth and stable servo control via pulse widths.
    - Left, Center, Right should be pulse widths in microseconds.
    '''
    def __init__(self, gpio_pin, left=500, center=1500, right=2500):
        self.gpio_pin = gpio_pin
        self.left = left
        self.center = center
        self.right = right

        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise IOError("Cannot connect to pigpio daemon. Did you run 'sudo pigpiod'?")

        self.pi.set_mode(gpio_pin, pigpio.OUTPUT)
    
    def set_angle(self, angle):
        '''
        Sets servo angle using linear interpolation of pulse widths.
        '''
        pulse_width = (angle * (self.right - self.left)) / 180 + self.left
        pulse_width = max(self.left, min(self.right, pulse_width))
        self.pi.set_servo_pulsewidth(self.gpio_pin, pulse_width)

    def finish(self):
        '''
        Stops sending PWM signal to the servo.
        '''
        self.set_angle(90)
        time.sleep(1)
        self.pi.set_servo_pulsewidth(self.gpio_pin, 0)
        self.pi.stop()
