# main.py
# Toto je ukázka toho, jak by měl vypadat "čistý" neblokující kód (náhrada za mode2.py).
# Místo `time.sleep()` využívá tzv. neblokující design s využitím `time.ticks_ms()`.
# To znamená, že hlavní smyčka ("loop") běží co nejrychleji a úkoly se spouštějí
# jen v momentech, kdy uběhne určitý časový úsek. Tím pádem systém reaguje na tlačítka okamžitě!

import time
from lib.button import Button
from lib.oled import OLED
from lib.encoder import RotaryEncoder
from lib.lm393 import SpeedSensor
from motor_controller import MotorController, SystemState

# 1. Třída pro neblokující tlačítko (Debounce bez sleepu)
class NonBlockingButton:
    def __init__(self, pin_num, debounce_ms=200):
        self.btn = Button(pin_num)
        self.debounce_ms = debounce_ms
        self.last_pressed_time = 0
        self.last_state = False

    def was_just_pressed(self):
        """Vrátí True, jen když bylo tlačítko právě teď stisknuto (ošetřeno proti zákmitům)."""
        current_state = self.btn.is_pressed()
        now = time.ticks_ms()
        
        # Detekce hrany (změna z False na True) a zároveň kontrola času
        if current_state and not self.last_state:
            if time.ticks_diff(now, self.last_pressed_time) > self.debounce_ms:
                self.last_pressed_time = now
                self.last_state = current_state
                return True
        
        self.last_state = current_state
        return False

def main():
    print("Spouštím V2 - Neblokující architektura (Mode 2 + Enkodér a Senzor)")
    
    # Inicializace periferií
    oled = OLED(sda_pin=20, scl_pin=21)
    controller = MotorController() # Zde se inicializuje motor i všechny LED
    
    btn_start = NonBlockingButton(13)
    btn_direction = NonBlockingButton(12)
    
    encoder = RotaryEncoder(clk_pin=9, dt_pin=8, sw_pin=1)
    sensor = SpeedSensor(pin_d0=10, holes=20)
    
    # Časovače pro periodické úlohy
    last_display_update = time.ticks_ms()
    
    # Úvodní nastavení
    controller.update_hardware()
    oled.clear()

    try:
        # Hlavní neblokující smyčka (podobná void loop() z Arduina)
        while True:
            current_time = time.ticks_ms()
            
            # --- 1. Obsluha vstupů (Tlačítka) ---
            # Tyto funkce se vyhodnotí okamžitě a program nezamrzne!
            if btn_start.was_just_pressed():
                print("Tlačítko START stisknuto.")
                controller.toggle_state()
                
            if btn_direction.was_just_pressed():
                print("Tlačítko SMĚR stisknuto.")
                controller.toggle_direction()
            
            # --- 2. Čtení enkodéru a nastavení rychlosti ---
            # V Pythonu není ++ nebo --, enkodér vrací číslo.
            speed_val = encoder.get_value()
            controller.set_speed(speed_val)
            
            # --- 3. Nezávislé aktualizace (např. Displej a Senzor) ---
                # Displej se překreslí jen každých 200 ms (5 FPS).
                # Tím pádem to nebliká a nezdržuje to zbytek kódu.
            if time.ticks_diff(current_time, last_display_update) > 200:
                last_display_update = current_time
                
                rpm = sensor.get_rpm()
                bar = controller.get_progress_bar_text()
                
                # Zápis na displej provádíme efektivně - přemažeme jen když je třeba,
                # ale i zavolání clear() každých 200ms je mnohem lepší než každou milisekundu.
                oled.clear()
                oled.print_text(bar, 0, 0)
                oled.print_text(f"Req Spd: {controller.speed}", 0, 15)
                oled.print_text(f"Real RPM: {rpm}", 0, 30)

            # Extra krátký sleep jen proto, aby to nesežralo 100% výkonu CPU a nebránilo přerušením
            time.sleep_ms(1) 

    except KeyboardInterrupt:
        print("\nProgram bezpečně ukončen.")
        # Při ukončení musíme natvrdo vše vypnout
        controller.state = SystemState.STOPPED
        controller.update_hardware()

if __name__ == "__main__":
    main()
