import time
from drv8833 import DRV8833
from lm393 import SpeedSensor

# Motor Driver (DRV8833) 
PIN_IN1 = 14
PIN_IN2 = 15

# Optický senzor (LM393) D0 pin
PIN_D0 = 16

# ==========================================
# INICIALIZACE MODULŮ
# ==========================================

# Vytvoření objektu motoru
motor = DRV8833(pin_in1=PIN_IN1, pin_in2=PIN_IN2)

# Vytvoření objektu senzoru, který má 20 děr na disku
senzor = SpeedSensor(pin_d0=PIN_D0, holes=20)


# Proměnná pro naši požadovanou rychlost (0-100)
zvolena_rychlost_motoru = 30

# ==========================================
# HLAVNÍ PROGRAM
# ==========================================

print("Start programu")
motor.forward(zvolena_rychlost_motoru)

try:
    while True:
        # Vypočítáme otáčky za minutu (RPM)
        aktualni_rpm = senzor.get_rpm()
        celkove_pulzy = senzor.get_pulses()
        
        print(f"Rychlost: {aktualni_rpm} RPM | Pulzů celkem: {celkove_pulzy}")
        
        # Počkáme 1 vteřinu mezi měřeními
        time.sleep(1)

except KeyboardInterrupt:
    # Blok 'except' se provede, když zastavíš program v konzoli (Ctrl+C)
    print("\nProgram přerušen. Zastavuji motor...")
    motor.stop()
