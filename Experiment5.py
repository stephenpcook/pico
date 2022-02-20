import machine

# Setup 2 digital outputs to drive LEDs
LED0 = machine.Pin(25, machine.Pin.OUT)
LED1 = machine.Pin(10, machine.Pin.OUT)

# Setup 2 bdigital inputs for buttons
ButtonA = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
ButtonB = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Initialise the LEDs as 'off'
LEDState0 = False
LEDState1 = False

# These IRQ Handlers toggle the variables we use to light the LEDs. They check
# which pin caused the IRQ so 1 button controls the onboard LED and the other
# button controls the breadboard LED
def ButtonAHandler(pin):
    global LEDState0
    if pin == ButtonA:
        if LEDState0 == True:
            LEDState0 = False
        else:
            LEDState0 = True

def ButtonBHandler(pin):
    global LEDState1
    if pin == ButtonB:
        if LEDState1 == True:
            LEDState1 = False
        else:
            LEDState1 = True

# Setup the IRQ and hook it to the handler
ButtonA.irq(trigger=machine.Pin.IRQ_RISING, handler=ButtonAHandler)
ButtonB.irq(trigger=machine.Pin.IRQ_RISING, handler=ButtonBHandler)

while True:
    LED0.value(LEDState0)
    LED1.value(LEDState1)