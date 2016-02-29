import sys
import pygame
import time
import serial

CODE = {'A': '.-',     'B': '-...',   'C': '-.-.',
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
     	'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.'
        }

ONE_UNIT = 0.5
THREE_UNITS = 3 * ONE_UNIT
SEVEN_UNITS = 7 * ONE_UNIT
PATH = 'morse_sound_files/'


def pulse(duration):
    arduino.write('H'.encode()) # turns LED ON
    print("MOTOR ON")
    time.sleep(duration) # waits for duration
    arduino.write('L'.encode()) # turns LED OFF
    print("MOTOR OFF")
    print("PULSE COMPLETE")

def verify(string):
    keys = CODE.keys()
    for char in string:
        if char.upper() not in keys and char != ' ':
         sys.exit('Error the charcter ' + char + ' cannot be translated to Morse Code')

def main():
    arduino = serial.Serial('COM4', 9600)
    time.sleep(2) # waiting the initialization...

    msg = raw_input('MESSAGE: ')
    verify(msg)

    pygame.init()

    for char in msg:
        if char == ' ':
            print ' '*7,
	    time.sleep(SEVEN_UNITS)
        else:
	    print CODE[char.upper()],
	    #pygame.mixer.music.load(PATH + char.upper() + '_morse_code.ogg')
	    #pygame.mixer.music.play()
	    time.sleep(THREE_UNITS)

if __name__ == &amp;quot;__main__&amp;quot;:
    main()

