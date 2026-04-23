from machine import Pin

class Relay:
    def __init__(self, pin_num, active_low=False):
        self.pin = Pin(pin_num, Pin.OUT)
        self.active_low = active_low
        self.off()
        
    def on(self):
        self.pin.value(0 if self.active_low else 1)
        
    def off(self):
        self.pin.value(1 if self.active_low else 0)
        
    def toggle(self):
        self.pin.toggle()

class DualRelay:
    def __init__(self, pin1, pin2, active_low=False):
        self.relay1 = Relay(pin1, active_low)
        self.relay2 = Relay(pin2, active_low)
