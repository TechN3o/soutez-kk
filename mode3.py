import time
from drv8833 import DRV8833
from lm393 import SpeedSensor
from potentiometer import Potentiometer

""" Program pro čtení otáček za minutu """


# Motor Driver (DRV8833) 
PIN_IN1 = 14
PIN_IN2 = 15

# senzor (LM393) D0 pin
PIN_D0 = 10

motor = DRV8833(pin_in1=PIN_IN1, pin_in2=PIN_IN2)
potentiometer = Potentiometer(26)

senzor = SpeedSensor(pin_d0=PIN_D0, holes=20)




print("start")

try:
    while True:
        motor_speed = potentiometer.get_percentage()
        motor.forward(motor_speed)
        rpm_speed = senzor.get_rpm()
        pulses = senzor.get_pulses()
        
        print(f"speed: {rpm_speed} RPM | Pulzů celkem: {pulses}")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stop")
    motor.stop()
