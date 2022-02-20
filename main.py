import machine
from machine import Pin
import utime


SEG_A = 1
SEG_B = 2
SEG_C = 3

def main():
    led_A = Pin(SEG_A, Pin.OUT)
    led_B = Pin(SEG_B, Pin.OUT)
    led_C = Pin(SEG_C, Pin.OUT)

    led_B.off()
    led_C.off()

    led_A.on()
    utime.sleep(1)
    led_A.off()
    led_B.on()
    utime.sleep(1)
    led_B.off()
    led_C.on()
    utime.sleep(1)
    led_C.off()
    return None

while True:
    main()