from lib.drv8833 import DRV8833
import time
from lib.led import LED
from lib.button import Button
from lib.oled import OLED
from lib.potentiometer import Potentiometer

""" Program for controlling motor with displayed values"""
print("Mode 1 program")


# set pins of LEDs
led_green = LED(16)
led_red = LED(17)
led_left = LED(18)
led_right = LED(19)
btn_start = Button(13)
btn_direction = Button(12)

# init display at 0x3C
oled = OLED(sda_pin=20,scl_pin=21)


# Motor Driver (DRV8833) 
PIN_IN1 = 14
PIN_IN2 = 15
motor = DRV8833(pin_in1=PIN_IN1, pin_in2=PIN_IN2)

#setup potentiometer
potentiometer = Potentiometer(26)

motorDirection: bool = False
motorState: bool = False
motor_speed = potentiometer.get_percentage()


def motorForward():
    motor.forward(motor_speed)
    led_green.on()
    led_red.off()
    led_left.on()
    led_right.off()
    
def motorBackward():
    motor.backward(motor_speed)
    led_green.on()
    led_red.off()
    led_left.off()
    led_right.on()
    
def motorStop():
    motor.stop()
    led_red.on()
    led_green.off()
    led_left.off()
    led_right.off()
    

def motorToggleDir():
    motor.stop()
    time.sleep(2)
    if(motorDirection):
        motorForward()
        
    else:
        motorBackward()
        

# returns the string for displaying progressbar           
def progressBar():
    oled.clear()
    if(motorState):
        if(motorDirection):
            return "[    ||==>]"
        else:
            return "[<==||    ]"
    else:
        return "[    ||    ]"
        
motorStop()
try:
    while True:
        # read value from potentiometer
        motor_speed = potentiometer.get_percentage()
        # print out the progressbar and motor speed in percents
        oled.print_text(progressBar() + f"{motor_speed}%")
        if(btn_start.is_pressed()):
            print("start pressed")
            motorState = not motorState
            if(motorState): # if motor is running
                if(motorDirection): # resolve direction in which to spin
                    motorForward()
                    
                else:
                    motorBackward()
            else:
                motorStop()
            time.sleep(1)
        if(btn_direction.is_pressed()):
            print("dir pressed")
            motorDirection = not motorDirection

            motorToggleDir()
            time.sleep(1)
# for stopping the program
except KeyboardInterrupt:
        motorStop()
        print("\n Program stopped")
        motor.stop()
