from drv8833 import DRV8833
import time
from led import LED
from button import Button
from oled import OLED
# Motor Driver (DRV8833) 
PIN_IN1 = 14
PIN_IN2 = 15

led_green = LED(16)
led_red = LED(17)
led_left = LED(18)
led_right = LED(19)
btn_start = Button(13)
btn_direction = Button(12)
# senzor (LM393) D0 pin
PIN_D0 = 16

oled = OLED(sda_pin=20,scl_pin=21)

motor = DRV8833(pin_in1=PIN_IN1, pin_in2=PIN_IN2)
motorDirection: bool = False
motorState: bool = False

motor_speed = 40


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
        
# def toggleMotorState():
#     motorState = not motorState
#     if(motorState):
#          if(motorDirection):
#              motorForward()
#          else:
#              motorBackward()
    
def progressBar():
    oled.clear()
    if(motorState):
        if(motorDirection):
            return "[    ||==>]"
        else:
            return "[<==||    ]"
    else:
        return "[    ||    ]"
        
        
try:
    while True:
        oled.print_text(progressBar())
        if(btn_start.is_pressed()):
            print("start pressed")
            motorState = not motorState
            if(motorState):
                if(motorDirection):
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

except KeyboardInterrupt:
        motorStop()
        print("\n Program stopped")
        motor.stop()
