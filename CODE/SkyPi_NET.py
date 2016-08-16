import subprocess
from time import sleep, strftime

import netifaces
from pythonwifi.iwlibs import Wireless


DIR='/home/pi/SkyPi/CODE/'


class SkyPi_NET:
    """
    Class implementing SkyPi network functionality
    - check address
    - change WiFI mode to/from Ad-Hoc (TODO)
    """

    WIFI_INTERFACE='wlan0'
    
    def __init__(self):
        # IP
        self.interface,self.address = self.first_ip()
        self.wifi_dev=Wireless(SkyPi_NET.WIFI_INTERFACE)

    def get_ip(self):
        ip_dict={}
        for i in netifaces.interfaces():
            addr = netifaces.ifaddresses(i).get(netifaces.AF_INET)
            if addr:
                ip_dict[i] = addr[0]['addr']
        return ip_dict

    def first_ip(self):
        priority_list = [SkyPi_NET.WIFI_INTERFACE, 'eth0', 'lo']
        ips = self.get_ip()
        for i in priority_list:
            addr = ips.get(i)
            if addr:
                return (i, addr) 
        
    def check_net(self):
        """
        Check net status: returns True if status has changed
        """
        interface_new,address_new = self.first_ip()
        # if address has changed
        if ( self.address   != address_new   or
             self.interface != interface_new ):
             self.interface = interface_new 
             self.address   = address_new
             return True
        else:
            return False

    def net_status_str(self):
        """
        Returns strng with the network status
        """
        interface_chr=self.interface[0]
        # capital letter for Ad-Hoc mode
        if self.get_wifi_mode_chr()=='A':
              interface_chr=interface_chr.upper()
        return '%s%s' % (interface_chr ,self.address)


    def get_wifi_mode_chr(self):
        """
        Return A/M/X for WiFi modes
        """
        mode=self.get_wifi_mode()
        if mode == 'Managed':
            return 'M'
        elif mode == 'Ad-Hoc':
            return 'A'
        else:
            return 'X'

    def get_wifi_mode(self):
        try:
            return self.wifi_dev.getMode()
        except:
            return None

    def change_to_AdHoc(self):
        subprocess.call(DIR + 'WiFi_Mode_Scripts/AdHoc_WiFi.sh')

    def change_to_Managed(self):
        subprocess.call(DIR + 'WiFi_Mode_Scripts/Managed_WiFi.sh')

if __name__ == "__main__" :
    print "NET status: %s" % SkyPi_NET().net_status_str()
