#============= IMPORTS =====================
import RPi.GPIO as GPIO
import time  
import _thread as thread
import threading
#============= a4988 CLASS ================
timer_done = False
t_delay=0
motor_status = False

def timerDone():
    global timer_done
    print("Timer Done")
    timer_done = True
    print("KILLED")

def time_converter(specific_time, duration):
    if(specific_time==1):
        duration = duration*3600
    if(specific_time==2):
        duration=duration*60
    if(specific_time==3):
        duration = duration
    else:
        print("ERROR: INCORRECT TIME VALUE")
    return duration

def countdown_timer(specificTime, duration):
    seconds = time_converter(specificTime, duration)
    timer = threading.Timer(seconds, timerDone)
    timer.start()
    print(timer)
   
        

class stepperMotor:
    def __init__(self, resolution_pins, direction_pin, step_pin, reset_pin):
        self.direction_pin = direction_pin
        self.step_pin = step_pin
        self.reset_pin = reset_pin

        if resolution_pins[0] != -1:
            self.resolution_pins = resolution_pins
        else:
            self.resolution_pins = False
        
        self.stop_motor = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.resolution_pins, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.reset_pin, GPIO.OUT)

    def resolution_set(self, steptype):
        resolution = {'Full': (0, 0, 0),
                        'Half': (1, 0, 0),
                        '1/4': (0, 1, 0),
                        '1/8': (1, 1, 0),
                        '1/16': (1, 1, 1)}
        if self.step_pin != False:
            GPIO.setup(self.resolution_pins, GPIO.OUT)
            GPIO.output(self.resolution_pins, resolution[steptype])
            print("Resolution set to: " + steptype)
        else:
            print("RESOLUTION OFF")

    def stepper_speed(self, v):
        global t_delay
        a = 0.0003125
        b= 60
        fz = v/(a*b)
        t_delay = 1/fz
        
    def run_forever(self):
        GPIO.output(self.direction_pin, 1)
        while timer_done == False:
            GPIO.output(self.step_pin, True)
            time.sleep(0.0125)
            GPIO.output(self.step_pin, False)
            time.sleep(0.0125) 

    def run_timed(self,specificTime, duration):
        global timer_done
        GPIO.output(self.direction_pin, 1)
        GPIO.output(self.reset_pin, GPIO.HIGH)
        countdown_timer(specificTime, duration)
        print("motor active")
        motor_status = True
        while timer_done == False:
            GPIO.output(self.step_pin, True)
            time.sleep(t_delay)
            GPIO.output(self.step_pin, False)
            time.sleep(t_delay) 
        GPIO.output(self.reset_pin, GPIO.LOW)
        timer_done = False
        motor_status = False
        print("motor not running")
    
    def stopMotor(self):
        GPIO.output(self.reset_pin, GPIO.LOW)
    def status(self):
        global motor_status
        if motor_status == True:
            return 1
        else:
            return 0
    def test_thread(self, t):
        global timer_done
        GPIO.output(self.direction_pin, 1)
        countdown_timer(t)
        
    def check_status(self):
        global timer_done
        if True:
            print("HIGH")
            time.sleep(0.002)
            print("LOW")
            time.sleep(0.002) 
        timer_done = False
















    

