#!/usr/bin/python
from Adafruit_CharLCD import Adafruit_CharLCD

lcd = Adafruit_CharLCD()

lcd.begin(16, 2)
lcd.clear()

lcd.message("STOP SkyPi_LCDd\n")
sleep(2)
