from machine import Pin

class RotaryEncoder:
    def __init__(self, clk_pin, dt_pin, sw_pin):
        self.clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self.dt = Pin(dt_pin, Pin.IN, Pin.PULL_UP)
        self.sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)
        
        self.value = 0
        self.last_clk = self.clk.value()
        
        self.clk.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._update)
        
    def _update(self, pin):
        clk_val = self.clk.value()
        if clk_val != self.last_clk:
            if self.dt.value() != clk_val:
                self.value += 1
            else:
                self.value -= 1
        self.last_clk = clk_val
        
    def get_value(self):
        return self.value
        
    def reset(self):
        self.value = 0
        
    def is_pressed(self):
        return self.sw.value() == 0
