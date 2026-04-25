from machine import Pin, PWM

class DRV8833:
    def __init__(self, pin_in1, pin_in2):
        self.pwm1 = PWM(Pin(pin_in1, Pin.OUT))
        self.pwm2 = PWM(Pin(pin_in2, Pin.OUT))
        self.pwm1.freq(1000)
        self.pwm2.freq(1000)
        self.stop()
        
    def _calculate_speed(self, speed):
        if speed < 0:
            speed = 0
        if speed > 100:
            speed = 100
        return int((speed / 100.0) * 65535)

    def forward(self, speed):
        pwm_val = self._calculate_speed(speed)
        self.pwm1.duty_u16(pwm_val)
        self.pwm2.duty_u16(0)

    def backward(self, speed):
        pwm_val = self._calculate_speed(speed)
        self.pwm1.duty_u16(0)
        self.pwm2.duty_u16(pwm_val)

    def stop(self):
        self.pwm1.duty_u16(0)
        self.pwm2.duty_u16(0)
