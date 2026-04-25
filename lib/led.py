from machine import Pin, PWM

class LED:
    def __init__(self, pin_num):
        self.pin = Pin(pin_num, Pin.OUT)
        self.off()
        
    def on(self):
        self.pin.value(1)
        
    def off(self):
        self.pin.value(0)
        
    def toggle(self):
        self.pin.toggle()

class DimmableLED:
    def __init__(self, pin_num, freq=1000):
        self.pwm = PWM(Pin(pin_num, Pin.OUT))
        self.pwm.freq(freq)
        self.off()
        
    def set_brightness(self, percentage):
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
        self.pwm.duty_u16(int((percentage / 100.0) * 65535))
        
    def on(self):
        self.set_brightness(100)
        
    def off(self):
        self.set_brightness(0)
