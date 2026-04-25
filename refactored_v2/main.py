# main.py
# This is an example of what a "clean" non-blocking code should look like (a replacement for mode2.py).
# Instead of `time.sleep()`, it uses a non-blocking design utilizing `time.ticks_ms()`.
# This means the main loop runs as fast as possible, and tasks are triggered
# only when a specific time interval has passed. Thus, the system reacts to buttons instantly!

import time
from lib.button import Button
from lib.oled import OLED
from lib.encoder import RotaryEncoder
from lib.lm393 import SpeedSensor
from motor_controller import MotorController, SystemState

# 1. Class for a non-blocking button (Debounce without sleep)
class NonBlockingButton:
    def __init__(self, pin_num, debounce_ms=200):
        self.btn = Button(pin_num)
        self.debounce_ms = debounce_ms
        self.last_pressed_time = 0
        self.last_state = False

    def was_just_pressed(self):
        """Returns True only when the button has just been pressed (debounced)."""
        current_state = self.btn.is_pressed()
        now = time.ticks_ms()
        
        # Edge detection (change from False to True) and time check
        if current_state and not self.last_state:
            if time.ticks_diff(now, self.last_pressed_time) > self.debounce_ms:
                self.last_pressed_time = now
                self.last_state = current_state
                return True
        
        self.last_state = current_state
        return False

def main():
    print("Starting V2 - Non-blocking architecture (Mode 2 + Encoder and Sensor)")
    
    # Initialize peripherals
    oled = OLED(sda_pin=20, scl_pin=21)
    controller = MotorController() # Motor and all LEDs are initialized here
    
    btn_start = NonBlockingButton(13)
    btn_direction = NonBlockingButton(12)
    
    encoder = RotaryEncoder(clk_pin=9, dt_pin=8, sw_pin=1)
    sensor = SpeedSensor(pin_d0=10, holes=20)
    
    # Timers for periodic tasks
    last_display_update = time.ticks_ms()
    
    # Initial setup
    controller.update_hardware()
    oled.clear()

    try:
        # Main non-blocking loop (similar to void loop() in Arduino)
        while True:
            current_time = time.ticks_ms()
            
            # --- 1. Input handling (Buttons) ---
            # These functions are evaluated instantly and the program does not freeze!
            if btn_start.was_just_pressed():
                print("START button pressed.")
                controller.toggle_state()
                
            if btn_direction.was_just_pressed():
                print("DIRECTION button pressed.")
                controller.toggle_direction()
            
            # --- 2. Reading the encoder and setting speed ---
            # There is no ++ or -- in Python, encoder returns a number.
            speed_val = encoder.get_value()
            controller.set_speed(speed_val)
            
            # --- 3. Independent updates (e.g. Display and Sensor) ---
            # Display redraws only every 200 ms (5 FPS).
            # Because of this, it doesn't blink and doesn't slow down the rest of the code.
            if time.ticks_diff(current_time, last_display_update) > 200:
                last_display_update = current_time
                
                rpm = sensor.get_rpm()
                bar = controller.get_progress_bar_text()
                
                # Writing to the display efficiently - clearing only when necessary,
                # but even calling clear() every 200ms is much better than every millisecond.
                oled.clear()
                oled.print_text(bar, 0, 0)
                oled.print_text(f"Req Spd: {controller.speed}", 0, 15)
                oled.print_text(f"Real RPM: {rpm}", 0, 30)

            # Extra short sleep just so it doesn't consume 100% CPU time and block interrupts
            time.sleep_ms(1) 

    except KeyboardInterrupt:
        print("\nProgram safely terminated.")
        # Turn everything off safely upon exit
        controller.state = SystemState.STOPPED
        controller.update_hardware()

if __name__ == "__main__":
    main()