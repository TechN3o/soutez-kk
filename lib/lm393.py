from machine import Pin
import time

class SpeedSensor:
    def __init__(self, pin_d0, holes=20):
        self.sensor_pin = Pin(pin_d0, Pin.IN)
        self.holes = holes
        self.pulses = 0
        self.last_time = time.ticks_ms()
        self.last_pulses = 0
        self.sensor_pin.irq(trigger=Pin.IRQ_FALLING, handler=self._count_pulse)
        
    def _count_pulse(self, pin):
        self.pulses += 1
        
    def get_pulses(self):
        return self.pulses
        
    def reset(self):
        self.pulses = 0
        
    def get_rpm(self):
        current_time = time.ticks_ms()
        dt_ms = time.ticks_diff(current_time, self.last_time)
        
        if dt_ms == 0:
            return 0
            
        dpulses = self.pulses - self.last_pulses
        revolutions = dpulses / self.holes
        minutes = dt_ms / 60000.0
        
        rpm = revolutions / minutes
        
        self.last_time = current_time
        self.last_pulses = self.pulses
        
        return int(rpm)
