from machine import Pin, I2C
import ssd1306

class OLED:
    def __init__(self, i2c_num=0, sda_pin=0, scl_pin=1, width=128, height=64):
        self.width = width
        self.height = height
        self.i2c = I2C(i2c_num, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self.display = ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)
        self.clear()
        
    def clear(self):
        self.display.fill(0)
        self.display.show()
        
    def print_text(self, text, x=0, y=0):
        self.display.text(str(text), x, y)
        self.display.show()
        
    def draw_pixel(self, x, y, color=1):
        self.display.pixel(x, y, color)
        self.display.show()
        
    def draw_line(self, x1, y1, x2, y2, color=1):
        self.display.line(x1, y1, x2, y2, color)
        self.display.show()
        
    def draw_rect(self, x, y, w, h, color=1, filled=False):
        if filled:
            self.display.fill_rect(x, y, w, h, color)
        else:
            self.display.rect(x, y, w, h, color)
        self.display.show()
