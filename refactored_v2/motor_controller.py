# motor_controller.py
# This class solves the "DRY" (Don't Repeat Yourself) problem and removes 
# the need for global variables (motorState, motorDirection).
# All logic related to hardware (motor, LEDs) is neatly encapsulated in one place.

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
        
        # Encapsulated internal state (replaces original global variables)
        self.state = SystemState.STOPPED
        self.forward_direction = True
        self.speed = 70
        
        self.update_hardware()

    def toggle_state(self):
        """Toggles between STOP and RUNNING and immediately updates the hardware."""
        if self.state == SystemState.STOPPED:
            self.state = SystemState.RUNNING
        else:
            self.state = SystemState.STOPPED
        self.update_hardware()

    def toggle_direction(self):
        """Changes the direction and updates the hardware."""
        self.forward_direction = not self.forward_direction
        self.update_hardware()

    def set_speed(self, speed):
        """Sets the speed (0-100)."""
        # Clamp values
        self.speed = max(0, min(100, speed))
        
        # If we are currently running, apply the speed change immediately
        if self.state == SystemState.RUNNING:
            self.update_hardware()

    def update_hardware(self):
        """
        This method is the only place where LEDs and motor are physically turned on/off.
        It removes the duplicate code that was in the original `motorForward`, `motorBackward` and `motorStop`.
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
        """Returns the text representation of the state for the display."""
        if self.state == SystemState.RUNNING:
            return "[    ||==>]" if self.forward_direction else "[<==||    ]"
        return "[    ||    ]"