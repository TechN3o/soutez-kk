import time
from lib.drv8833 import DRV8833
from lib.lm393 import SpeedSensor
from lib.led import LED
from lib.button import Button
from lib.oled import OLED
from lib.encoder import RotaryEncoder
""" Program for reading RPM """

print("Mode 2 program")



# sensor (LM393) D0 pin
PIN_D0 = 10
# setup encoder
encoder = RotaryEncoder(9,8,1)

#setup speed sensor LM393
sensor = SpeedSensor(pin_d0=PIN_D0, holes=20)

# init oled display at 0x3C
oled = OLED(sda_pin=20,scl_pin=21)

# setup LEDs
led_green = LED(16)
led_red = LED(17)
led_left = LED(18)
led_right = LED(19)
btn_start = Button(13)
btn_direction = Button(12)

# Motor Driver (DRV8833) 
PIN_IN1 = 14
PIN_IN2 = 15
motor = DRV8833(pin_in1=PIN_IN1, pin_in2=PIN_IN2)
motorDirection: bool = False
motorState: bool = False
motor_speed = encoder.get_value()


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
        rpm_speed = sensor.get_rpm() # read from sensor
        
        print(f"speed: {rpm_speed} RPM")
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
            time.sleep(2)
        if(btn_direction.is_pressed()):
            print("dir pressed")
            motorDirection = not motorDirection

            motorToggleDir()
            time.sleep(2)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stop")
    motorStop()
    motor.stop()
