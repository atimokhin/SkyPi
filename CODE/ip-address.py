import netifaces

def get_ip():
    ip_dict={}
    for i in netifaces.interfaces():
        addr = netifaces.ifaddresses(i).get(netifaces.AF_INET)
        if addr:
            ip_dict[i] = addr[0]['addr']
    return ip_dict

def first_ip():
    priority_list = ('wlan0', 'eth0', 'lo')
    ips = get_ip()
    for i in priority_list:
        addr = ips.get(i)
        if addr:
            return (i, addr) 

if __name__ == "__main__":
    print first_ip()
