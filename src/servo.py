import RPi.GPIO as GPIO

'''
Micro Servo 9g A0090:
2.5 - left -90 degrees
7.5 - center 0 degrees
12 - right 90 degrees
'''

class ServoUtil:
    '''
    ServoUtil(GPIO_Pin, Frequency, Left, Center, Right) 

    - Allows for the set-up of a servo and handling angle control.
    - Left, Center, Right used to convert angle in to Duty Cycle
    '''
    def __init__(self, gpio_pin, frequency, left, center, right):
        self.left = left
        self.center = center
        self.right = right

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.OUT)
        
        self.servo = GPIO.PWM(gpio_pin, frequency)
        self.servo.start(0)
    
    def set_angle(self, angle):
        '''
        Changes the oritation of the servo based on the given center.
        '''
        duty_cycle = (angle * (self.right - self.left)) / 180 + self.left
        if duty_cycle < self.left:
            duty_cycle = self.left
        elif duty_cycle > self.right:
            duty_cycle = self.right 
        self.servo.ChangeDutyCycle(duty_cycle)

    def finish(self):
        '''
        Closes comunication with the servo.
        '''
        self.servo.stop()