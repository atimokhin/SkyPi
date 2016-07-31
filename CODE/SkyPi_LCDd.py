#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

from ip_address import  first_ip

import logging
import logging.handlers
import argparse
import sys
import time  # this is only being used as part of the example

from gps_mode import gps_mode


# Deafults
LOG_FILENAME = "/tmp/SkyPi_LCDd.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
	LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
	def __init__(self, logger, level):
		"""Needs a logger and a logger level."""
		self.logger = logger
		self.level = level

	def write(self, message):
		# Only log if there is a message (not just a new line)
		if message.rstrip() != "":
			self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)



lcd = Adafruit_CharLCD()


lcd.begin(16, 2)
lcd.clear()

lcd.message("Start SkyPi_LCDd\n")
# set IP
interface,address = first_ip()
lcd.setCursor(0,1)
lcd.message('%s%s' % (interface[0],address) )

while True:
    lcd.setCursor(0,0)
    current_gps_mode = gps_mode()
    if current_gps_mode == 3 or current_gps_mode == 2:
        lcd.message("G:%i" % current_gps_mode)
	# refresh time
	lcd.message(datetime.now().strftime(' %m/%d %H:%M \n'))
    elif current_gps_mode == 1:
        lcd.message("GPS:N0 FIX      \n")
    elif current_gps_mode == 0:
        lcd.message("      gpsd ERROR\n")
    else:
        lcd.message("gps_status ERROR\n")
    # refresh time
    #lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
    sleep(2)
    # check IP address
    interface_new,address_new = first_ip()
    if (  address != address_new or interface_new != interface):
	 interface = interface_new 
	 address = address_new
         lcd.setCursor(0,1)
	 lcd.message('%s%s' % (interface[0],address) )
