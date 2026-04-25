Project: DC Motor Controller (Competition Submission)
Author: [Your Name]

1. PINOUT / WIRING
------------------
Buttons:
- Start/Stop Button: GPIO 13
- Direction Button: GPIO 12

LEDs (Status Visualization):
- Green LED (Run/Stop status): GPIO 16
- Red LED (Run/Stop status): GPIO 17
- Left Blue LED (Direction): GPIO 18
- Right Blue LED (Direction): GPIO 19

Motor Driver (DRV8833 used instead of Relay + MOSFET):
- IN1 (PWM 1): GPIO 14
- IN2 (PWM 2): GPIO 15

Display (OLED I2C):
- SDA: GPIO 20 (I2C0)
- SCL: GPIO 21 (I2C0)

Sensors & Inputs:
- Potentiometer (Analog In): GPIO 26 (ADC0)
- Rotary Encoder CLK: GPIO 9
- Rotary Encoder DT: GPIO 8
- Rotary Encoder SW: GPIO 1
- LM393 Optical Sensor D0: GPIO 10


2. UNIMPLEMENTED FEATURES (Nerealizované funkce)
------------------------------------------------
Due to time constraints and hardware availability during the competition, the following features from the assignment were not implemented:
- 4-position switch for mode selection (separate scripts were used instead).
- Use of 2-channel relay and separate MOSFET (a more integrated DRV8833 H-bridge was used instead, which achieves the same motor control functionally but deviates from the strict hardware requirement).
- Smooth/gradual start and stop (PLYNULÉ zastavení a roztočení) in Mode 1 and 2.
- The 6-LED speed visualization (bargraph) in Mode 1 and Mode 2.
- Mode 3: Sequential state machine and serial communication parser.
- schematics.png was not generated during the competition time limit.