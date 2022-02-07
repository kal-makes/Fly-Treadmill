#============= IMPORTS =====================
import RPi.GPIO as GPIO
import time  
import _thread as thread
#============= a4988 CLASS ================
timer_done = False
class stepperMotor:
    def __init__(self, resolution_pins, direction_pin, step_pin):
        self.direction_pin = direction_pin
        self.step_pin = step_pin

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

    def run_forever(self):
        GPIO.output(self.direction_pin, 1)
        while 1:
            GPIO.output(self.step_pin, True)
            time.sleep(0.002)
            GPIO.output(self.step_pin, False)
            time.sleep(0.002) 

    def run_timed(self):
        global timer_done
        GPIO.output(self.direction_pin, 1)
        while timer_done == False:
            GPIO.output(self.step_pin, True)
            time.sleep(0.002)
            GPIO.output(self.step_pin, False)
            time.sleep(0.002) 

    def run_countdown(self):
        global timer_done
        t = int(input("Enter hour(s)"))
        t = t #*3600 #uncomment when wanting to convert back to hours
        start_time = time.time()
        timer_done = False
        while t:
            # Divmod takes only two arguments so
            # you'll need to do this for each time
            # unit you need to add
            mins, secs = divmod(t, 60) 
            hours, mins = divmod(mins, 60)
            days, hours = divmod(hours, 24)
            timer = '{:02d}:{:02d}:{:02d}:{:02d}'.format(days, hours, mins, secs) 
            print(timer, end="\r" )
            time_before_sleep = time.time() - start_time
            time.sleep(1) 
            time_after_sleep = time.time() - start_time
            print(timer, time_before_sleep, time_after_sleep)
            t -= 1
        timer_done = True
        #return timer

                   
GPIOPINS = (14, 15, 18)
testMotor = stepperMotor(GPIOPINS, 20, 21)
testMotor.resolution_set('1/8')

def countdown():
    thread.start_new_thread(testMotor.run_countdown, ())
    thread.start_new_thread(testMotor.run_timed, ())
    while 1:
        pass





    

