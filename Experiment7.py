import machine
from machine import Pin
import utime
import _thread

DO_SONG = True

TEMPO = 180

LED_PORTS = {
    'Red': 10,
    'Yellow': 11,
    'Green': 12,
    'PedestrianRed': 6,
    'PedestrianWait': 7,
    'PedestrianGreen': 8
}

SONG = [
    ('c4', 1.5), ('-', 0.02), ('c4', 0.23), ('-', 0.02), ('c4', 0.23),
    ('a#3',1.5), ('-', 0.02), ('a#3',0.23), ('-', 0.02), ('a#3',0.23),
    ('c4',3.5), ('f4',0.25),('g4',0.25),
    ('g#4',1.5), ('g4',0.25),('f4',0.25),
    ('d#4',1.5), ('f4',0.25),('g4',0.25),
    ('f4',2),
    ('d#4',1), ('d4',1),
    ('c4',2)]

NOTES = {
    'a#3': 233.082,
    'c4': 261.626,
    'd4': 293.665,
    'd#4': 311.127,
    'f4': 349.228,
    'g4': 391.995,
    'g#4': 415.305,
    '-': 1000
}

DUTY_0 = 0
DUTY_50 = 32767
BUZZ_ON_TIME = 50
SECOND = 1000

# Setup 2 digital inputs for the buttons
ButtonA = Pin(0, Pin.IN, Pin.PULL_DOWN)
ButtonB = Pin(1, Pin.IN, Pin.PULL_DOWN)

# Setup 6 digital outputs to drive LEDs
LEDs = {k: Pin(v, Pin.OUT) for k, v in LED_PORTS.items()}

# Setup a PWM Output for the beeping for a crossing
Buzzer = machine.PWM(Pin(15))
Buzzer.duty_u16(DUTY_0) # Start with the buzzer off
Frequency = 1000 # Set a frequency of 1 kHz

# Control variable
CrossRequested = False

def play_song():
    note_duration = 1000*60/TEMPO
    for note, len_ in SONG:
        if note == '-':
            Buzzer.duty_u16(DUTY_0)
            utime.sleep_ms(int(note_duration*len_))
        else:
            Buzzer.freq(int(NOTES[note]))
            Buzzer.duty_u16(DUTY_50)
            utime.sleep_ms(int(note_duration*len_))
    Buzzer.duty_u16(DUTY_0)


# This is the thread that takes care of beeping the buzzer
def PedestrianCross():
    global CrossRequested
    LEDs['PedestrianRed'].value(0)
    LEDs['PedestrianGreen'].value(1)
    LEDs['PedestrianWait'].value(0)

    print('Beeping')
    if DO_SONG:
        play_song()
    else:
        for Beeping in range(10):
            Buzzer.duty_u16(DUTY_50)
            utime.sleep_ms(BUZZ_ON_TIME)
            Buzzer.duty_u16(DUTY_0)
            utime.sleep_ms(SECOND - BUZZ_ON_TIME)
    print('End beep thread')
    LEDs['PedestrianRed'].value(1)
    LEDs['PedestrianGreen'].value(0)
    CrossRequested = False

# Only set the request flag once - if its already set we just exit the IRQ
# We don't need to check who asked for the cross, it does the same for both
# "sides" of the road - either button.
def ButtonIRQHandler(pin):
    global CrossRequested
    if CrossRequested == False:
        print("Button pressed")
        CrossRequested = True
        LEDs['PedestrianWait'].value(1)

# Setup the IRQ and hook it to the handler
ButtonA.irq(trigger = Pin.IRQ_RISING, handler=ButtonIRQHandler)
ButtonB.irq(trigger = Pin.IRQ_RISING, handler=ButtonIRQHandler)

# Setup the initial Light states
# Road stopped, pedestrian stopped, wait off
for led in LEDs:
    LEDs[led].value(0)

for led in ['Red', 'PedestrianRed']:
    LEDs[led].value(1)

utime.sleep(2)
play_song()

# Main Loop - runs the LEDs on and off
while True:
    # We start with the Traffic Lights on Stop, so check if anyone Wants to cross
    if CrossRequested == True:
        _thread.start_new_thread(PedestrianCross, ())
        # Now hang around until the pedestrian is done.
        while CrossRequested:
            utime.sleep(1)
    else:
        LEDs['Yellow'].value(1)
        utime.sleep(1)
        LEDs['Red'].value(0)
        LEDs['Yellow'].value(0)
        LEDs['Green'].value(1)
        utime.sleep(2)
        LEDs['Yellow'].value(1)
        LEDs['Green'].value(0)
        utime.sleep(1)
        LEDs['Red'].value(1)
        LEDs['Yellow'].value(0)
        utime.sleep(2)