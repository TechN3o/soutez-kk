from machine import ADC, Pin

class Potentiometer:
    def __init__(self, pin_num):
        self.adc = ADC(Pin(pin_num))
        
    def get_raw(self):
        return self.adc.read_u16()
        
    def get_percentage(self):
        return int((self.adc.read_u16() / 65535.0) * 100)
