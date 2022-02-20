import utime
import machine
import utime
import _thread

DUTY_OFF = 0
DUTY_50 = 32767

# Setup digital input for buttons
ButtonA = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Setup 3 digital outputs to drive LEDs
Red = machine.Pin(10, machine.Pin.OUT)
Yellow = machine.Pin(12, machine.Pin.OUT)
Green = machine.Pin(9, machine.Pin.OUT)
for led in [Red, Yellow, Green]:
    led.off()

# Setup the PWN Output
Buzzer = machine.PWM(machine.Pin(15))
Buzzer.duty_u16(DUTY_OFF)
Frequency = 1000

# Control variable
Beeping = False

' This is the thread routine, which will beep the buzzer'
def Beep():
    global Beeping
    ONTIME=50
    SECOND = 1000
    print('Start Beeping Thread')
    while Beeping:
        Buzzer.duty_u16(DUTY_50)
        utime.sleep_ms(ONTIME)
        Buzzer.duty_u16(DUTY_OFF)
        utime.sleep_ms(SECOND - ONTIME)
    print('End beeping thread')

def ButtonAIRQHandler(pin):
    global Beeping
    if Beeping == False:
        print("Start Beep")
        Beeping = True
        _thread.start_new_thread(Beep, ())
    else:
        Beeping = False # this causes the thread to exit
        print("Stop Beep")

# setup the IRQ and hook it to the handler
ButtonA.irq(trigger=machine.Pin.IRQ_RISING, handler=ButtonAIRQHandler)

while True:
    Red.toggle()
    utime.sleep_ms(100)
    Yellow.toggle()
    utime.sleep_ms(100)
    Green.toggle()
    utime.sleep_ms(100)