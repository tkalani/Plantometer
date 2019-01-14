import RPi.GPIO as gpio
import time

gpio.setwarnings(False)
def run_motor(flag,rain):
    gpio.setmode(gpio.BCM)
    gpio.setup(21, gpio.OUT)
    #print(flag<=35.0 and rain==0)
    if(flag<=35.0 and rain==0):
        print('Actuator 1 is On')
        gpio.output(21, gpio.HIGH) 
    else:
        gpio.output(21, gpio.LOW)
    return 
#run_motor(20,0)