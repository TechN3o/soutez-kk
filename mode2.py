import time
from drv8833 import DRV8833
from lm393 import SpeedSensor
from potentiometer import Potentiometer
from led import LED
from button import Button
from oled import OLED
from encoder import RotaryEncoder
""" Program pro čtení otáček za minutu """

print("Mode 2 program")

# Motor Driver (DRV8833) 
PIN_IN1 = 14
PIN_IN2 = 15

# senzor (LM393) D0 pin
PIN_D0 = 10

motor = DRV8833(pin_in1=PIN_IN1, pin_in2=PIN_IN2)
potentiometer = Potentiometer(26)
encoder = RotaryEncoder(9,8,1)
senzor = SpeedSensor(pin_d0=PIN_D0, holes=20)
oled = OLED(sda_pin=20,scl_pin=21)


led_green = LED(16)
led_red = LED(17)
led_left = LED(18)
led_right = LED(19)
btn_start = Button(13)
btn_direction = Button(12)

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

def display(text):
    oled.clear()
    oled.print_text(text)

print("start")
motorStop()
try:
    while True:
        print(encoder.get_value())
        motor_speed = encoder.get_value()
        motorForward()
        rpm_speed = senzor.get_rpm()
        pulses = senzor.get_pulses()
        
        print(f"speed: {rpm_speed} RPM | Pulzů celkem: {pulses}")
        display(f"{rpm_speed} RPM")
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
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stop")
    motor.stop()
