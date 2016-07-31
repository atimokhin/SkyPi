import gps

def gps_mode():
    # Listen on port 2947 (gpsd) of localhost
    try:
        session = gps.gps("localhost", "2947")
    except:
        return 0

    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    i = 0
    while i < 100:
        try:
            report = session.next()
            # Wait for a 'TPV' report and get mode
            if report['class'] == 'TPV':
               if report.mode == 1:
                   return 1
               elif report.mode == 2:
                   return 2
               elif report.mode == 3:
                   return 3
        except StopIteration:
            return 0
    # Timeout
    return -1

if __name__ == "__main__" :
    print "gps mode: %i" % gps_mode()
