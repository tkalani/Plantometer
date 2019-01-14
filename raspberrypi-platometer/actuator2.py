import RPi.GPIO as gpio
import time

gpio.setwarnings(False)
def run_motor(flag,rain):
    gpio.setmode(gpio.BCM)
    gpio.setup(20, gpio.OUT)
    print('Soil moisture 2 is ' + str(flag))
    #print(flag<=35.0 and rain==0)
    if(flag<=35.0 and rain==0):
        print('Actuator 2 is On')
        gpio.output(20, gpio.HIGH) 
    else:
        gpio.output(20, gpio.LOW)
    return 
#run_motor(20,0)


