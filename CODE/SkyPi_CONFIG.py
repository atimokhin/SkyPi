class SkyPi_CONFIG:
    """
    Class with configuration variables such as
    directory with the code
    PIN Layout
    Timing parameters

    It is imported by all other SkyPi classes
    """
    
    DIR='/home/pi/SkyPi/CODE/'

    DT_GPS_CHECK = 5 # GPS check interval in seconds
    DT_SLEEP     = 0.5   # sleep interval

    PIN_BUTTON_HC_SETUP   = 4
    PIN_SWITCH_ADHOC_MODE = 10

