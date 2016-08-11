import os
import time
import gps

class SkyPi_GPS:

    location_file_lock = '/var/run/SkyPi_GPS_Location_Current'
    location_file = '/home/pi/SkyPi/GPS_Location.txt'
    
    def __init__(self, dt_check=5):
        """
        dt_check - minimum interval in seconds between successive gps mode checks
        """
        if dt_check < 0:
            raise Exception("dt_check musy be positive!")
        # remove location file lock
        if os.path.exists(SkyPi_GPS.location_file_lock):
            os.unlink(SkyPi_GPS.location_file_lock)
        # initialize variables
        self.dt_check = dt_check
        self.t_last_check = time.clock()
        self.gps_mode = self.get_gps_mode()

    def has_gps_mode_changed(self):
        """
        Returns True of GPS mode has changes, False otherwise
        """
        if  time.clock()-self.t_last_check > self.dt_check:
            self.t_last_check = time.clock()
            current_gps_mode = self.get_gps_mode()
            if ( current_gps_mode != self.gps_mode ):
                self.gps_mode = current_gps_mode
                return True
        return False

    def save_location_to_file(self):
        """
        Save GPS location into file SkyPi_GPS.location_file
        """
        if self.gps_mode == 3 and not os.path.exists(SkyPi_GPS.location_file_lock):
            os.mknod(SkyPi_GPS.location_file_lock)
        if self.gps_mode == 2 and not os.path.exists(SkyPi_GPS.location_file_lock):
            os.mknod(SkyPi_GPS.location_file_lock)
        
    
    def gps_status_str(self):
        """
        return string desribing gps status
        """
        if self.gps_mode == 3 or self.gps_mode == 2:
            gps_message="G:%i" % self.gps_mode
        elif self.gps_mode == 1:
            gps_message="G:X"
        elif self.gps_mode == 0:
            gps_message="err"
        else:
            gps_message="ERR"
        return gps_message
            
    def get_gps_mode(self):
        """
        Return GPS fix mode
        """
        # Listen on port 2947 (gpsd) of localhost
        try:
            session = gps.gps("localhost", "2947")
        except:
            return 0
        # setup session
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        # read stream until receiving a 'TPV' packet
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
    print "gps mode: %i" % SkyPi_GPS().gps_mode

