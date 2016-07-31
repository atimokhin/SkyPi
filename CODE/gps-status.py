import gps

from datetime import datetime
from dateutil.tz import tzutc, tzlocal

def gps_mode():
    # Listen on port 2947 (gpsd) of localhost
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    while True:
        try:
            report = session.next()
            # Wait for a 'TPV' report and display the current time
            # To see all report data, uncomment the line below
            # print report
            if report['class'] == 'TPV':
               if report.mode == 1:
                   return 1
               else if report.mode == 2:
                   return 2
               else if report.mode == 3:
                   return 3
        except StopIteration:
            print "GPSD has terminated"

if ( __name__ == "main" ):
    print "gps mode: %i" % gps_mode()
