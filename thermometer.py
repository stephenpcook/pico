import machine
import utime

thermometer = machine.ADC(26)
lightmeter = machine.ADC(27)
thermometer = machine.ADC(4)

while True:
    th = 3.3*thermometer.read_u16()/65535
    deg_c = 27 - (th-0.706)/0.00172
    print(f'T: {th:.4f} {deg_c:.2f}')
    utime.sleep(2)