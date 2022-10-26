"""
getHostName takes an IP address as a string, and returns the host name as provided by DNS

arp takes no arguments, and provides the arp tables from the computer its run on as a list of strings

myPing takes and IP address as a string, and optionaly 'y' or 'n' for verbose mode. 'y' as default
"""
version_Num = '0.03'


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
def arp():
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

        """loop threw the arp -a return leave out the first blank line, then go threw each line and extract the MAC from
         the line + store it in a new list. if no MAC on the line new list gets ' '"""
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
            back[f"{ip}"] = f'{macs[i]}'
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
            back[f"{ip}"] = f'{macs[i]}'
        return back


"""by default (v=y) will return a readout of the OS's ping results if v=n will simply 
return a True if a device is online and False if not"""
def myPing(IP, c=4, v='y'):
    import re
    from icmplib import ping

    # test user input
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", IP) is None:
        raise ValueError(f"{IP} is not a valid IP address")

    if v.lower() == 'n' or v.lower() == 'no':
        temp = ping(IP, count=1, privileged=False)
    else:
        temp = ping(IP, count=c, privileged=False)

    # if verbose flag is no, only return if a single ping was replyed to with a boolan
    if v.lower() == 'n' or v.lower() == 'no':
        return temp.is_alive
    elif v.lower() == 'y' or v.lower() == 'yes':
        lost = temp.packets_sent - temp.packets_received
        if lost < 1:
            return f"{temp.packets_sent} packets sent, and none of them where lost."
        else:
            return (
                f"{temp.packets_sent} packets sent, and {lost} of them where lost. {int(temp.packet_loss * 100)}% in total where lost")
    else:
        raise ValueError("Only y or n are allowed as a secondary argument")
