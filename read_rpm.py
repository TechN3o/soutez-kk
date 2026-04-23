import time
from drv8833 import DRV8833
from lm393 import SpeedSensor

# Motor Driver (DRV8833) 
PIN_IN1 = 14
PIN_IN2 = 15

# senzor (LM393) D0 pin
PIN_D0 = 16

motor = DRV8833(pin_in1=PIN_IN1, pin_in2=PIN_IN2)

senzor = SpeedSensor(pin_d0=PIN_D0, holes=20)


zvolena_rychlost_motoru = 30

print("Start programu")
motor.forward(zvolena_rychlost_motoru)

try:
    while True:
        aktualni_rpm = senzor.get_rpm()
        celkove_pulzy = senzor.get_pulses()
        
        print(f"Rychlost: {aktualni_rpm} RPM | Pulzů celkem: {celkove_pulzy}")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram přerušen. Zastavuji motor...")
    motor.stop()
