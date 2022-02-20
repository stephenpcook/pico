import machine
from machine import Pin
import utime
"""
Setup:
LED display pins (1,2,3,4,5,7,10,11) are the anodes corresponding to the
segments, which we connect through 330 ohm resistors to GP0 through GP7.
Pins (12, 9, 8 and 6) are the cathodes corresponding to the digits, which
we connect to four transistors with the lock controlled by GP18 through
GP21 with 570 ohm resistors.
"""
pin_to_segment = 'ED.CGBFA'
segment_to_pin = {'A':7, 'B':5, 'C':3, 'D': 1,
                  'E':0, 'F':6, 'G':4, '.': 2}

position_to_pin = {0: 20, 1: 21, 2: 19, 3: 18}

leds = {k: Pin(v, Pin.OUT) for k, v in segment_to_pin.items()}

positions = {k: Pin(v, Pin.OUT) for k, v in position_to_pin.items()}

digit = {'0': 'ABCDEF', '1': 'BC', '2': 'ABDEG', '3': 'ABCDG',
         '4': 'BCFG', '5': 'ACDFG', '6': 'ACDEFG', '7': 'ABC',
         '8': 'ABCDEFG', '9': 'ABCDFG',
         'a': 'ABCEFG', 'b': 'CDEFG', 'c': 'ADEF', 'd':  'BCDEG',
         'e': 'ADEFG', 'f': 'AEFG', '-': 'G', ' ': '',
         'g': 'ACDEF', 'h': 'CEFG', 'i': 'C', 'j': 'BCDE', 'k': 'ACEFG',
         'l': 'DEF', 'm':'ACEG' , 'n': 'CEG', 'o': 'CDEG', 'p': 'ABEFG',
         'q': 'ABCFG', 'r': 'EG', 's': 'ACDFG', 't': 'DEFG', 'u':'BCDEF',
         'v':'CDE', 'w': 'BDFG', 'x': 'BCEFG', 'y': 'BCDFG', 'z':'ABDG',
         '!': 'B.', '.': '.', ',': 'CD', '?': 'ABEG', "'": 'B',
         'H': 'BCEFG', 'I': 'EF'
         }

DIGIT_MISSING = 'ADG'


def clear_display():
    for seg in 'ABCDEFG.':
        leds[seg].off()
    return None


def display_digit(x, decimal=False):
    clear_display()
    for seg in digit.get(x, DIGIT_MISSING):  # type: ignore
        leds[seg].on()
    if decimal:
        leds['.'].on()
    return None


def flash_segs(delay=1):
    clear_display()
    for x in 'ABCDEFG.':
        leds[x].on()
        print(x)
        utime.sleep(delay)
        leds[x].off()
    return None


def flash_digits():
    flash_word(' -0123456789abcdef.')
    return None


def flash_word(word, delay=1):
    prev_char = ' '
    for character in word:
        if character == '.':
            print('.')
            display_digit(prev_char, decimal=True)
        else:
            utime.sleep(delay)
            display_digit(character)
            prev_char = character
            print(character)
    utime.sleep(delay)
    return None


def all_positions():
    for i in range(4):
        positions[i].on()
    return None


def set_position(pos):
    for i in range(4):
        if i == pos:
            positions[i].on()
        else:
            positions[i].off()
    return None


def test_all():
    all_positions()
    print('flashing segments')
    flash_segs()
    utime.sleep(4)
    print('flashing digits')
    flash_digits()
    print('Done test')
    flash_word('polly.')
    flash_word('dilly.')
    flash_word('steve.')
    clear_display()
    return None


def test_positions():
    for i in range(4):
        print('Position %d', i)
        set_position(i)
        flash_segs(0.2)
        utime.sleep(0.5)
    return None


def number_to_word(number):
    if (number <= -100):
        return '-99.9'
    if (number >= 1000):
        return '999.9'
    return '{:5.1f}'.format(number)


def render_number(number, duration=None, freq=None):
    word = number_to_word(number)
    word_without_decimal = word[0:3] + word[4]
    render_word(word_without_decimal, 2, duration, freq)
    return None


def render_word(word, decimal=None, duration=None, freq=None):
    if duration is None:
        duration = 5
    if freq is None:
        freq = 50
    n_flashes = duration * freq
    flash_time = 1 / (4 * freq)
    word_four_chars = '{:4s}'.format(word)[:4]
    for _ in range(n_flashes):
        for i, letter in enumerate(word_four_chars):
            set_position(i)
            display_digit(letter)
            if (i == decimal):
                display_digit(letter, decimal=True)
            else:
                display_digit(letter)
            utime.sleep(flash_time)
            clear_display()
    return None


def temp():
    thermometer = machine.ADC(4)
    th = 3.3 * thermometer.read_u16() / 65535
    deg_c = 27 - (th - 0.706) / 0.00172
    return deg_c


def report_temp():
    t = temp()
    render_number(t, duration=1)
    return None


def test_position_render():
    numbers = [0, 420, 1000, 3.14, -99.0, -100]
    for number in numbers:
        print(number_to_word(number))
        render_number(number)
    for word in ['poly', 'dily']:
        render_word(word)


def profess_love():
    sentence = 'I love poly and dily'
    print_text(sentence, duration=1)


def profess_more_love():
    text = '''
    I love phil
    I love andy
    I love you bro!
    I love you sis!
    and
    I love prue

    here is a pico
    '''
    print_text(text)
    return None


def print_text(text, duration=None, pause=None):
    if pause is None:
        pause = 2
    for line in text.split('\n'):
        for word in line.split():
            render_word(word, duration=duration)
        utime.sleep(pause)
    return None


hugo_text = '''
Hugo is the boss baby
jack is a good dad!

here is a rasp bery pi pico
'''


def flash_love():
    for dur in [0.05, 0.1, 0.15, 0.2]:
        for _ in range(int(1 / dur)):
            render_word('poly', duration=dur)
            render_word('dily', duration=dur)


def main():
    profess_love()
    while True:
        report_temp()


main()
