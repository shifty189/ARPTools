"""
getHostName takes an IP address as a string, and returns the host name as provided by DNS

arp takes no arguments, and provides the arp tables from the computer its run on as a list of strings

myPing takes and IP address as a string, and optionaly 'y' or 'n' for verbose mode. 'y' as default
"""
import math
import os
import ipaddress
import socket
version_Num = '0.10'


class System:
    def __init__(self, ip):
        try:
            ipaddress.ip_address(ip)
            systemType = 'ip'
        except ValueError:
            systemType = 'hostname'
        if systemType == 'ip':
            self.Name = getHostName(ip)
            self.IP = ip
            # testing = arp()
            self.MAC = arp()[ip]
            self.OS = OScheck(ip)
            self.shares = self.shareCheck()
        else:
            self.Name = ip
            self.IP = socket.gethostbyname(self.Name)
            # testing = arp()
            if self.IP == 'unknown':
                ...
            else:
                self.MAC = arp()[self.IP]
            self.OS = OScheck(ip)
            self.shares = self.shareCheck()

    def report(self):
        print(f'Name: {self.Name}')
        print(f'Ip Address: {self.IP}')
        print(f'Mac address: {self.MAC}')
        print(f'Operating System: {self.OS}')
        print(f'Shares: {self.shares}')
        reportList = [f'Name: {self.Name}', f'Ip Address: {self.IP}', f'Mac address: {self.MAC}', f'Operating System: {self.OS}', f'Shares: {self.shares}']
        return reportList

    def shareCheck(self):
        temp = []
        temp2 = []
        with os.popen(f"net view \\\\{self.Name}") as a:
            shareData = a.readlines()

        for i, s in enumerate(shareData):
            if i < 7:
                ...
            else:
                temp.append(s.replace(' ', ''))
        for t in temp:
            temp2.append(t.strip())
        return temp2


def OScheck(IP):
    import os
    with os.popen(f"ping {IP}") as a:
        ping = a.readlines()
    try:
        temp = ping[2].split(' ')
        temp = temp[5]
        temp = temp.split('=')
    except:
        return'Unknown'
    if temp[1][:3] == '128':
        return 'win32'
    elif temp[1][:2] == '64':
        return 'Linux'
    else:
        return f'Unknown {temp[1]}'

def convert_size(size_bytes: int) -> str:
   if size_bytes < 0:
       return 'Negative numbers are not supported: -50'
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


def systemStatus() -> dict:
    import psutil
    import platform

    CPU = platform.processor()
    cpuRate = psutil.cpu_percent()
    processes = psutil.process_iter()
    processNum = len(psutil.pids())
    processList = []
    disks = {}
    for disk in psutil.disk_partitions():
        try:
            disks[disk.device] = psutil.disk_usage(disk.device)
        except PermissionError:
            disks[disk.device] = 'Non readable drive'
            ...
    for process in processes:
        processList.append(process.name())
    CPUload = psutil.cpu_percent(interval=1)
    tempmemory = psutil.virtual_memory()
    answer = {}
    answer['processNum'] = processNum
    answer['processes'] = processList
    answer['CPUName'] = CPU
    answer['CPUload'] = CPUload
    answer['disks'] = disks
    answer['cpuRate'] = cpuRate
    answer['freeRam'] = convert_size(tempmemory.available)
    answer['totalRam'] = convert_size(tempmemory.total)
    return answer


# provide a hostname if a proper valid IP address is provided
def getHostName(IP: str):
    import socket
    try:
        hostName = socket.gethostbyaddr(IP)[0]
    except socket.herror:  # this error means host can't be found
        hostName = None
    except socket.gaierror:  # this error means a bad IP was provided
        hostName = None
    return hostName


#arp() takes not argguments, and returns a dictionary of the systems arp table
def arp() -> dict:
    from sys import platform
    import re
    import os

    macs = []
    IPs = []
    macSearch = r"[0-9A-Fa-f]{2}[:-]{1}[0-9A-Fa-f]{2}[:-]{1}[0-9A-Fa-f]{2}[:-]{1}[0-9A-Fa-f]{2}[:-]{1}[0-9A-Fa-f]{2}[:-]{1}[0-9A-Fa-f]{2}"
    ipSearch = r"([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})"
    hostNames = []
    if platform == 'win32':
        # os.popen allows you to work the windows command line, "as a" lets us take the return and store it by line in a list
        with os.popen("arp -a") as a:
            arpData = a.readlines()

        """
        loop threw the arp -a return leave out the first blank line, then go threw each line and extract the MAC from
        the line + store it in a new list. if no MAC on the line new list gets ' '
        """
        for i, a in enumerate(arpData):
            if i > 0:
                try:
                    if a[2].isnumeric():
                        try:
                            ip_end = a.find(" ", 3)
                            IPs.append(a[2:ip_end:1])
                        except:
                            pass
                        try:
                            start = a.find("-") - 2
                            macs.append(a[start:start + 17:1])
                        except TypeError:
                            macs.append(' ')
                except ValueError:
                    macs.append(' ')
                    IPs.append(' ')
                except IndexError:
                    macs.append(' ')
                    IPs.append(' ')

        back = {}
        for i, ip in enumerate(IPs):
            venMac = f"{macs[i][0:2]}{macs[i][3:5]}{macs[i][6:8]}"
            back[f"{ip}"] = f'{macs[i]}({vendorLookup(venMac)})'
        return back
    elif platform == 'linux':
        with os.popen("arp -a") as a:
            arpData = a.readlines()
        for line in arpData:
            tempMac = re.search(macSearch, line)
            tempIP = re.search(ipSearch, line)
            IPs.append(tempIP.group(0))
            macs.append(tempMac.group(0))
        back = {}
        for i, ip in enumerate(IPs):
            venMac = f"{macs[i][0:2]}{macs[i][3:5]}{macs[i][6:8]}"
            back[f"{ip}"] = f'{macs[i]}({vendorLookup(venMac)})'
        return back


"""by default (v=y) will return a readout of the OS's ping results if v=n will simply 
return a True if a device is online and False if not"""
def myPing(IP: str, **kwargs):
    import re
    from icmplib import ping

    # test user input and confirm the IP address provided is within the range of valid IPv4 address'
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", IP) is None:
        raise ValueError(f"{IP} is not a valid IP address")
    else:
        for ip in IP.split("."):
            if int(ip) > 255:
                raise ValueError (f'{IP} is not a valid IPv4 address')

    for i, kwarg in enumerate(kwargs):
        if kwarg.lower() == 'verbose' or kwarg.lower() == 'v':
            v = kwargs[kwarg]
        elif kwarg.lower() == 'count' or kwarg.lower() == 'c':
            if not isinstance(kwargs[kwarg], int):
                raise ValueError (f'count argument must be a full number not {kwargs[kwarg]}')
            c = kwargs[kwarg]
        else:
            raise ValueError (f'Only Verbose and count can be provided as optinal arguments, you provided {kwarg}')

    try:#hacky way to deal with default arguments
        if v.lower() == 'n':
            pass
    except UnboundLocalError:
        v = 'y'

    try:  # hacky way to deal with default arguments
        if c == 0:
            pass
    except UnboundLocalError:
        c = 4

    if v.lower() == 'n' or v.lower() == 'no':
        temp = ping(IP, count=1, privileged=False)
    else:
        temp = ping(IP, count=c, privileged=False)

    # if verbose flag is no, only return if a single ping was replyed to with a boolan
    if v.lower() == 'n' or v.lower() == 'no':
        count = 0
        while count < 3:
            if temp.is_alive:
                return temp.is_alive
            else:
                count += 1
                if count < 3:
                    temp = ping(IP, count=1, privileged=False)
        return temp.is_alive

    elif v.lower() == 'y' or v.lower() == 'yes':
        lost = temp.packets_sent - temp.packets_received
        if lost < 1:
            return f"{temp.packets_sent} packets sent, and none of them where lost."
        else:
            return (
                f"{temp.packets_sent} packets sent, and {lost} of them where lost. {int(temp.packet_loss * 100)}% in total where lost")
    else:
        raise ValueError("Only y or n are allowed as an argument for verbose")


def vendorLookup(usermac: str) -> str:
    if usermac == "ffffff":
        return "Broadcast address"
    with open('vendor macs.txt', 'r', encoding='utf-8') as file:
        vendorAndMacs = file.read().splitlines()

    #dict with keys of vendors mac address (first 6 chars) in lower case
    tempMacs = {}
    for mac in vendorAndMacs:
        tempMacs[mac[0:6].lower()] = mac[7:-1]
    try:
        return tempMacs[usermac]
    except KeyError:
        return f"Unknown Vendor {usermac[0:2]}:{usermac[2:4]}:{usermac[4:]}"



PC = System('192.168.10.2')
# PC = System('CNSSRVR')

# print(socket.gethostbyname('CNSSRVR'))
PC.report()
# print(PC.shares)
