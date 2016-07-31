import gps

from datetime import datetime
from dateutil.tz import tzutc, tzlocal

def gps_status():
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
               else:
                   break
        except StopIteration:
                    session = None
                    print "GPSD has terminated"

    while True:
        try:
            report = session.next()
            # Wait for a 'TPV' report and display the current time
            # To see all report data, uncomment the line below
            # print report
            if report['class'] == 'TPV':
                if report.mode == 3 :
                    f = open( 'gps-coordinates.txt', 'w' )
                    f.write( 'latitude=%g\n'  % report.lat )
                    f.write( 'longitude=%g\n' % report.lon )
                    f.close()
                print 'mode=%d' % report.mode
                print 'time=%s' % report.time
                print 'latitude=%g longitude=%g' % (report.lat,report.lon)

                break
#                utc = datetime.strptime(report.time, "%Y-%m-%dT%H:%M:%S.000Z")
#                utc = utc.replace(tzinfo=tzutc())
#                local = utc.astimezone(tzlocal())
#                print local
#                print 'difference', (local-datetime.now(tzlocal())).total_seconds(), '\n'
        except KeyboardInterrupt:
                    quit()
        except StopIteration:
                    session = None
                    print "GPSD has terminated"
        return 0

if __name__ == '__main__':
    if gps_status():
        print "No GPS FIX"
