import sys
import pygame
import time
import random
import string
import serial
import numpy
from pygame.locals import *
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


def verify(string):
    keys = CODE.keys()
    for char in string:
        if char.upper() not in keys and char!= ' ':
            sys.exit('Error Nigga')

def pulse(duration):
    arduino.write('H'.encode()) # turns LED ON
    print("MOTOR ON")
    time.sleep(duration) # waits for duration
    arduino.write('L'.encode()) # turns LED OFF
    print("MOTOR OFF")
    print("PULSE COMPLETE")
def motorOn():
    arduino.write('H'.encode())
def motorOff():
    arduino.write('L'.encode())

def DisplayText(msg):
    left = 10
    for char in msg:
        msgSurfaceObj = fontObj.render(char,False,(0,0,255))
        msgRectObj = msgSurfaceObj.get_rect()
        msgRectObj.topleft = (left,20)
        screen.blit(msgSurfaceObj,msgRectObj)
        pygame.display.update()
        left += 100

def DDLength(char):
    morse = CODE[char.upper()]
    length = len(morse) - 1
    for dd in morse:
        if dd == ".":
            length += 1
        else:
            length += 1.5
    return length
            

def DisplayMorse(msg,rate,audio,visual,haptic,answer):
    ONE_UNIT = rate
    THREE_UNITS = 3 * ONE_UNIT
    SEVEN_UNITS = 7 * ONE_UNIT / 2
    dotSound = "C:/Users/Spencer's/Desktop/AudioLibrary/beep.wav"
    dashSound = "C:/Users/Spencer's/Desktop/AudioLibrary/beep.wav"
    time.sleep(2*ONE_UNIT)
    x = 10
    for char in msg:
        if char == " ":
            morse = ""
            time.sleep(4*ONE_UNIT)  # 4+3=7
            x+=50
        else:
            morse = CODE[char.upper()]
        for dd in range(0,len(morse)):
            x+=20#Shift to next dot/dash                                    #!#!#!#!#!# DEFINE GLOBAL VAR FOR FONT
            if visual :  #
                msgSurfaceObj = morseObj.render(morse[dd],False,(0,255,255))
                msgRectObj = msgSurfaceObj.get_rect()
                msgRectObj.topleft = (x,90)
                screen.blit(msgSurfaceObj,msgRectObj)
                pygame.display.update()     #Draw dot/dash to screen
            
            if len(morse)- dd == 1 and answer:
                pygame.event.get()
                msgSurfaceObj = morseObj.render(char,False,(0,0,255))#Alphabet Character Draw
                msgRectObj = msgSurfaceObj.get_rect()
                msgRectObj.topleft = (x-DDLength(char)*5,20)
                screen.blit(msgSurfaceObj,msgRectObj)
                pygame.display.update()

            if morse[dd] == ".":
                soundFile = "C:/Users/Spencer's/Desktop/AudioLibrary/03.wav"  #Dot Audio File
                dotObj = pygame.mixer.Sound(soundFile)    # Sound dot
                if audio :
                    dotObj.play()#Play dot sound
                if haptic :
                    motorOn()
                    pygame.event.get()
                    time.sleep(2*ONE_UNIT/3)    #. Dot Delay .
                    motorOff()
                else:
                    pygame.event.get()
                    time.sleep(ONE_UNIT/3)
                pygame.event.get()    
                time.sleep(ONE_UNIT/3)
                dotObj.stop()
                
                
            else:
                soundFile = "C:/Users/Spencer's/Desktop/AudioLibrary/09.wav"#3Dashes/" + char.lower() + ".wav"  #Dot Audio File
                dashObj = pygame.mixer.Sound(soundFile)    # Sound Dash
                if audio :
                    dashObj.play()#Play dash sound
                if haptic :
                    motorOn()
                    pygame.event.get()
                    time.sleep(2*THREE_UNITS/3)    #. dash Delay .
                    motorOff()
                else:
                    pygame.event.get()
                    time.sleep(THREE_UNITS/3)
                pygame.event.get()    
                time.sleep(THREE_UNITS/3)
                dashObj.stop()
                
            
                       

        pygame.event.get()    
        time.sleep(THREE_UNITS)   #Post character delay        
        x += 30 #Shift margin one character

    #pygame.quit()
    #sys.exit()

def BlindAnswer():
    letter = random.choice(string.ascii_letters)
    screen.fill((0,0,0))
    DisplayMorse(letter * 3, False, True, True, False) #########(Text, Audio, Visual, Haptic, Answer)
    screen.fill((0,0,0))
    time.sleep(SEVEN_UNITS)
    pygame.event.get()
    DisplayMorse(letter * 3, True, False, True, True)
    time.sleep(SEVEN_UNITS)
    pygame.event.get()
    main()


def GetRecord():
    Record = numpy.loadtxt("C:/Users/Spencer's/Desktop/Data.txt", delimiter=" ")
    return (Record)
def GetSRSLetter():
    y=0
    CR = 0.8
    chi=0
    Record = GetRecord()
    if Record == []:
        print ("No data found")
    PCorrect =[1/10]*26
    PObserve = [0]*26
    for row in Record:
        if row[0] == 0:
            chi += 8/26
        else:
            PCorrect[y] = row[0]/(row[0]+row[1])
            chi += (CR/26) * (1/PCorrect[y])
        y+=1
    selection = random.random()
    totalP = 0
    for i in range(0,26):
        PObserve[i] = (CR/26) * (1/(PCorrect[i]*chi))
        totalP += PObserve[i]
        if selection <= totalP :
            letter = chr(i + 97)
            break
    return (letter)

def RecordedPlay():
    letter = GetSRSLetter()
    Record = GetRecord()
    row = ord(letter.lower()) - 97
    speed = 0.09
    DisplayMorse(letter*3,speed,True,True,True,False)
    answer = input("Input Letter: ")
    pygame.event.get()
    if answer == letter:
        Record[row,0] +=1
    else:
        Record[row,1] +=1
    numpy.savetxt("C:/Users/Spencer's/Desktop/Data.txt", Record,newline='\r\n',fmt="%s", delimiter = " ")
    DisplayMorse(letter*3,speed,True,True,True,True)
    main()


###_____INIT_____###
ONE_UNIT = 0.9
THREE_UNITS = 3 * ONE_UNIT
SEVEN_UNITS = 7 * ONE_UNIT / 2
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
fpsClock = pygame.time.Clock()
fontObj = pygame.font.Font('freesansbold.ttf',90)
morseObj = pygame.font.Font('freesansbold.ttf',50)
screen = pygame.display.set_mode((600,200))
try:
    arduino = serial.Serial('COM4', 9600)
except:
    print ("Failed to connect to COMs")
    #pygame.display.quit()
    #sys.exit()
time.sleep(1) # waiting the initialization...
###_____INIT_____###

    
def main():
    screen.fill((0,0,0))  
    #RecordedPlay()

    DisplayMorse("Spencer",0.1, True, True, True, True)
    main()
    #if msg.upper() == letter.upper():
        #print ("Correct!")
    #else:
        #print ("WRONG! That was a(n) " + letter.upper())
    
    
##        for event in pygame.event.get():
##            if event.type == QUIT:
##                pygame.quit()
##                sys.exit()
##            if event.type == KEYDOWN:
##                if event.key == K_RIGHT:
##                    main()
                



