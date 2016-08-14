import os
import time
import gps

class SkyPi_GPS:

    loc_file_current = '/var/run/SkyPi_GPS_loc.current'
    loc_file         = '/home/pi/SkyPi/GPS.loc'
    loc_file_2       = '/home/pi/SkyPi/GPS.loc_2'
    
    def __init__(self, dt_check=5):
        """
        dt_check - minimum interval in seconds between successive gps mode checks
        """
        if dt_check < 0:
            raise Exception("dt_check musy be positive!")
        # remove location file lock
        if os.path.exists(SkyPi_GPS.loc_file_current):
            os.unlink(SkyPi_GPS.loc_file_current)
        # initialize variables
        self.dt_check = dt_check
        self.t_last_check = time.time()
        (self.gps_mode,self.lat,self.lon) = self.get_gps_data()

    def stop(self):
        """
        Remove lock file when stopping the service
        """
        # remove location file lock
        if os.path.exists(SkyPi_GPS.loc_file_current):
            os.unlink(SkyPi_GPS.loc_file_current)
        
        
    def check_gps(self):
        """
        if more than self.dt_check seconds has passed after the last check:
        - get GPS data
        - save mode, lat, lon in internal variables
        - writes location in to file, if necessary

        Returns True of GPS mode has changed, False otherwise
        """
        mode_changed=False
        if  time.time()-self.t_last_check > self.dt_check:
            self.t_last_check = time.time()
            # get GPS data
            current_gps_mode,lat,lon = self.get_gps_data()
            if current_gps_mode>1:
                (self.lat,self.lon) = (lat,lon)
            # check whether GPS mode has changed
            if ( current_gps_mode != self.gps_mode ):
                self.gps_mode = current_gps_mode
                mode_changed=True
            # save location into file (if necessary)
            self.save_location()
        # either not enough time has passed or the GPS mode has not changed
        return mode_changed

    def save_location(self):
        """
        Save correct GPS location into file SkyPi_GPS.loc_file
        """
        if self.gps_mode > 1 and not os.path.exists(SkyPi_GPS.loc_file_current):
            # mode 3 - accurate location -----
            if self.gps_mode == 3:
                # remove mode=2 file with less accurate coordinates
                if os.path.exists(SkyPi_GPS.loc_file_2):
                    os.unlink(SkyPi_GPS.loc_file_2)
                # save mode=3 location
                self._save_lat_lon_to_file(SkyPi_GPS.loc_file)
                # create lock file
                os.mknod(SkyPi_GPS.loc_file_current)
            # mode 2 - preliminary location
            elif self.gps_mode == 2:
                self._save_lat_lon_to_file(SkyPi_GPS.loc_file_2)

    def get_location(self):
        """
        retrives location saved in SkyPi_GPS.loc_file
        providing its status: 
        3 - fresh GPS-3 location 
        2 - fresh GPS-2 location
        30 - old GPS-3 location
        0  - no saved location available
        -1 - Error

        returns (lat,lon, status)
        """
        if os.path.exists(SkyPi_GPS.loc_file_current):
            if os.path.exists(SkyPi_GPS.loc_file):
                filename = SkyPi_GPS.loc_file
                status = 3
            else:
                status = -1
        elif os.path.exists(SkyPi_GPS.loc_file_2):
            filename = SkyPi_GPS.loc_file_2
            status = 2
        elif os.path.exists(SkyPi_GPS.loc_file):
            filename = SkyPi_GPS.loc_file
            status = 30
        else:
            status = 0
        # read location
        if status>0:
            lat,lon = self._get_lat_lon_from_file(filename)
        else:
            lat,lon = (0,0)
        return (lat,lon, status)
                
    def _get_lat_lon_from_file(self,filename):
        """
        helper function: get current location from file "filename"  
        """
        with open(filename,'r') as f:
            lat=float(f.readline())
            lon=float(f.readline())
            f.close()        
        return (lat,lon)
            
    def _save_lat_lon_to_file(self,filename):
        """
        helper function: save current location into file "filename"  
        """
        with open(filename,'w') as f:
            f.write("%g\n" % self.lat)
            f.write("%g\n" % self.lon)
            f.close()        
    
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
            
    def get_gps_data(self):
        """
        Return GPS fix mode, latitude and longitude
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
                        return (1, None, None)
                    elif report.mode == 2:
                        return (2, report.lat,report.lon)
                    elif report.mode == 3:
                        return (3, report.lat,report.lon)
            except StopIteration:
                return (0, None, None)
        # Timeout -  GPS respond NOT received
        return (-1,None,None)


if __name__ == "__main__" :
    print "gps mode: %i" % SkyPi_GPS().gps_mode

