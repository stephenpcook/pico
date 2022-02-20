from machine import Pin
import utime

PINS_TO_TEST = [10, 11, 12]

FLASHES = 10
ON_TIME = 500
OFF_TIME = 500
AFTER_ON_TIME = 2000
AFTER_OFF_TIME = 2000

def flash(led, t_on, t_off):
    led.value(1)
    utime.sleep_ms(t_on)
    led.value(0)
    utime.sleep_ms(t_off)


def flash_cycle(pin: int):
    LED = Pin(pin, Pin.IN, Pin.PULL_DOWN)
    print(f"Flashing pin {pin}")

    for _ in range(FLASHES):
        flash(LED,ON_TIME, OFF_TIME)
    utime.sleep_ms(AFTER_OFF_TIME)
    flash(LED, AFTER_ON_TIME, AFTER_OFF_TIME)


def main():
    for p_id in PINS_TO_TEST:
        print(f'Next pin: {p_id}')
        utime.sleep(1)
        flash_cycle(p_id)

#while True:
#    print('Starting cycle')
main()