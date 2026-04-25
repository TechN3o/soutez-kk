# DC Motor Controller - Competition Repository

This directory contains the codebase for an MCU programming competition (40th year, Regional round 2025/2026), where I achieved 1st place. 

## Competition Context & Self-Reflection
The original code (`mode0.py`, `mode1.py`, `mode2.py`) was written rapidly under a strict 4-hour time constraint. To speed up development, I utilized AI before the competition to generate hardware abstraction libraries (now in `/lib`). 

While the solution secured 1st place, it only scored 17/70 points. After reviewing the official assignment retroactively, the reasons for the point deductions are clear:
1. **Hardware Deviations:** The assignment specifically requested using a 2-channel relay for direction and a MOSFET for PWM speed control. I used a DRV8833 H-Bridge motor driver instead. While functionally superior and more modern, it didn't strictly follow the component constraints. 
2. **Missing Modes & Features:** "Mode 3" (Serial command parser and sequential state machine) was not implemented. Smooth acceleration/deceleration and the complex 6-LED speed bargraph were also omitted due to time limits. 
3. **Missing Deliverables:** A 4-position switch was not used for mode selection (separate scripts were run instead), and the `schematics.png` file was missing.

### The `refactored_v2` Architecture
As a learning exercise and for professional presentation, I have created the `refactored_v2` directory. It addresses the poor software architecture (anti-patterns) present in the original competition code:
- **Removed Blocking Delays:** Replaced `time.sleep()` with non-blocking `time.ticks_ms()` logic.
- **State Machine Implementation:** Encapsulated motor state and hardware updates into a clean `MotorController` class, eliminating messy global variables.
- **Hardware Decoupling:** Solved DRY (Don't Repeat Yourself) violations by centralizing hardware toggles.

### Relevant Links (Context)
*Please note: The competition organizers do not maintain these websites well. There are no results for 2026, or the specifications available, and the linked sites are heavily outdated.*
- [Soutěže v programování](https://programuj.si/souteze/programovani)
- [SP STV](http://sp.stv.cz/)

## Pinout
Please refer to `readme.txt` for the exact GPIO pin mapping used on the Raspberry Pi Pico.