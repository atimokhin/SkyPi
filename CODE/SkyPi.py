from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

from ip_address import  first_ip

import sys
import time  # this is only being used as part of the example

#from gps_mode import gps_mode

import RPi.GPIO as GPIO

from SkyPi_GPS import SkyPi_GPS


class SkyPi:

    def __init__(self):
        self.redraw_flag = True
        # setup LCD screen
        self.lcd = Adafruit_CharLCD()
        self.lcd.begin(16, 2)
        self.lcd.clear()
        self.lcd.message("Start SkyPi_LCDd\n")
        # setup datetime
        self.time_state = True
        self.time_str_fmt = ' %m/%d %H:%M'
        self.datetime_str=datetime.now().strftime(self.time_str_fmt)
        # gps mode - check no often than every 5 sec
        self.gps = SkyPi_GPS(4)
        # IP
        self.interface,self.address = first_ip()
        # setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def Task__GPS_IP(self):
        # gps status
        self._show_gps_status()
        # time
        self._show_time()
        # ip
        self._check_ip()
        # reset redraw_flag
        self.redraw_flag = False
        # monitor button
        self._check_button()
        
    def _check_button(self):
        input_state = GPIO.input(4)
        if input_state == False:
            self._set_HC()
        
    def _show_gps_status(self):
        """
        show GPS status
        """ 
        if ( self.gps.check_gps() or self.redraw_flag ):
            # show GPS info on LCD
            self.lcd.setCursor(0,0)
            self.lcd.message(self.gps.gps_status_str())
                
    def _check_ip(self):
        local_redraw_flag = False
        interface_new,address_new = first_ip()
        # if address has changed
        if ( self.address   != address_new   or
             self.interface != interface_new ):
             local_redraw_flag = True
             self.interface = interface_new 
             self.address   = address_new
        # show IP info on LCD
        if ( local_redraw_flag or self.redraw_flag ):                     
             self.lcd.setCursor(0,1)
             self.lcd.message('%s%s' % (self.interface[0],self.address) )

    def _show_time(self):
        current_datetime_str=datetime.now().strftime(self.time_str_fmt)
        if ( current_datetime_str != self.datetime_str or
             self.redraw_flag ):
            self.datetime_str = current_datetime_str
            self.lcd.setCursor(3,0)
            self.lcd.message(self.datetime_str)
        # blinking ":"
        self.time_state = not self.time_state
        self.lcd.setCursor(15,0)
        if self.time_state:
            self.lcd.message(':')
        else:
            self.lcd.message(' ')
             
    def _set_HC(self):
        self.lcd.clear()
        self.lcd.setCursor(0,0)
        self.lcd.message('Button pressed\n')
        sleep(1)
        self.lcd.clear()
        self.lcd.setCursor(0,0)
        lat,lon,status = self.gps.get_location()
        self.lcd.message('S:%2d lat:%g' % (status,lat))
        self.lcd.setCursor(0,1)
        self.lcd.message('    lon:%g' % lon)
        self.redraw_flag = True
        sleep(2)
        self.lcd.clear()
        
