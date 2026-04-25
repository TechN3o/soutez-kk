# motor_controller.py
# Tato třída řeší problém "DRY" (Don't Repeat Yourself) a odstraňuje 
# potřebu globálních proměnných (motorState, motorDirection).
# Veškerá logika kolem hardwaru (motor, LEDky) je hezky zabalená na jednom místě.

from lib.drv8833 import DRV8833
from lib.led import LED

class SystemState:
    STOPPED = 0
    RUNNING = 1

class MotorController:
    def __init__(self, pin_in1=14, pin_in2=15, p_led_g=16, p_led_r=17, p_led_l=18, p_led_right=19):
        self.motor = DRV8833(pin_in1=pin_in1, pin_in2=pin_in2)
        
        self.led_green = LED(p_led_g)
        self.led_red = LED(p_led_r)
        self.led_left = LED(p_led_l)
        self.led_right = LED(p_led_right)
        
        # Zapouzdřený vnitřní stav (nahrazuje původní globální proměnné)
        self.state = SystemState.STOPPED
        self.forward_direction = True
        self.speed = 70
        
        self.update_hardware()

    def toggle_state(self):
        """Přepne mezi STOP a RUNNING a ihned aktualizuje HW."""
        if self.state == SystemState.STOPPED:
            self.state = SystemState.RUNNING
        else:
            self.state = SystemState.STOPPED
        self.update_hardware()

    def toggle_direction(self):
        """Změní směr a aktualizuje HW."""
        self.forward_direction = not self.forward_direction
        self.update_hardware()

    def set_speed(self, speed):
        """Nastaví rychlost (0-100)."""
        # Omezení hodnot
        self.speed = max(0, min(100, speed))
        
        # Pokud zrovna jedeme, projeví se změna rychlosti hned
        if self.state == SystemState.RUNNING:
            self.update_hardware()

    def update_hardware(self):
        """
        Tato metoda je jediným místem, kde se reálně zapínají LEDky a motor.
        Odstraňuje duplicitní kód, který byl v původním `motorForward`, `motorBackward` a `motorStop`.
        """
        if self.state == SystemState.STOPPED:
            self.motor.stop()
            self.led_red.on()
            self.led_green.off()
            self.led_left.off()
            self.led_right.off()
        else:
            self.led_red.off()
            self.led_green.on()
            if self.forward_direction:
                self.motor.forward(self.speed)
                self.led_left.on()
                self.led_right.off()
            else:
                self.motor.backward(self.speed)
                self.led_left.off()
                self.led_right.on()

    def get_progress_bar_text(self):
        """Vrátí textovou reprezentaci stavu pro displej."""
        if self.state == SystemState.RUNNING:
            return "[    ||==>]" if self.forward_direction else "[<==||    ]"
        return "[    ||    ]"
