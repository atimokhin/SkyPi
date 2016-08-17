from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

import sys
import time  # this is only being used as part of the example

import RPi.GPIO as GPIO

from SkyPi_GPS import SkyPi_GPS
from SkyPi_NET import SkyPi_NET
from SkyPi_FSM import SkyPi_FSM
from SkyPi_CONFIG import SkyPi_CONFIG as SP_CFG



class SkyPi:

    def __init__(self):
        self.FSM = SkyPi_FSM()
        # flags
        self.redraw_flag = True
        self.wifi_mode_adhoc_flag = False
        # setup LCD screen
        self.lcd = Adafruit_CharLCD()
        self.lcd.begin(16, 2)
        self.lcd.clear()
        self.lcd.message("Start SkyPi_LCDd\n")
        # setup datetime
        self.time_state = True
        self.time_str_fmt = ' %m/%d %H:%M'
        self.datetime_str=datetime.now().strftime(self.time_str_fmt)
        # gps
        self.gps = SkyPi_GPS(SP_CFG.DT_GPS_CHECK)
        # net
        self.net = SkyPi_NET()
        # setup GPIOs
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SP_CFG.PIN_BUTTON_HC_SETUP,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(SP_CFG.PIN_SWITCH_ADHOC_MODE, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def Show_GPS_IP(self):
        # gps status
        self._show_gps_status()
        # time
        self._show_time()
        # ip
        self._show_ip()
        # reset redraw_flag
        self.redraw_flag = False
        # monitor button
        self.check_buttons()

    def Change_WiFi_Mode(self,mode):
        if mode == 'A':
            self.net.switch_to_AdHoc()
        elif mode == 'M':
            self.net.switch_to_Managed()
            
    def Setup_HC(self):
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
        
    def check_buttons(self):
        if GPIO.input(SP_CFG.PIN_BUTTON_HC_SETUP) == False:
            self.Setup_HC()
        if GPIO.input(SP_CFG.PIN_SWITCH_ADHOC_MODE) == False:
            if not self.wifi_mode_adhoc_flag:
                self.Change_WiFi_Mode('A')
                self.wifi_mode_adhoc_flag = True
        else:
            if self.wifi_mode_adhoc_flag:
                self.Change_WiFi_Mode('M')
                self.wifi_mode_adhoc_flag = False
        
    def _show_gps_status(self):
        """
        show GPS status
        """ 
        if ( self.gps.check_gps() or self.redraw_flag ):
            # show GPS info on LCD
            self.lcd.setCursor(0,0)
            self.lcd.message(self.gps.gps_status_str())
                
    def _show_ip(self):
        local_redraw_flag = False
        # if address has changed
        if ( self.net.check_net() or self.redraw_flag ):                     
             # clear previous IP
             self.lcd.setCursor(0,1)
             self.lcd.message(16*' ')
             # new IP
             self.lcd.setCursor(0,1)
             self.lcd.message(self.net.net_status_str())

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

        
