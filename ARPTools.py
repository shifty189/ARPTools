"""
getHostName takes an IP address as a string, and returns the host name as provided by DNS

arp takes no arguments, and provides the arp tables from the computer its run on as a list of strings

myPing takes and IP address as a string, and optionaly 'y' or 'n' for verbose mode. 'y' as default
"""
import os
from icecream import ic
import socket


# provide a hostname if a proper valid IP address is provided
def getHostName(IP: str):
    try:
        hostName = socket.gethostbyaddr(IP)[0]
    except socket.herror:  # this error means host can't be found
        # hostName = f"Device Name for {IP} can't be found"
        hostName = None
    except socket.gaierror:  # this error means a bad IP was provided
        hostName = None
    return hostName


def arp():
    global arp_window
    var = []
    arpLabels = []
    arpButton = []
    saveButton = []
    macs = []
    IPs = []
    hostNames = []
    # os.popen allows you to work the windows command line, "as a" lets us take the return and store it by line in a list
    with os.popen("arp -a") as a:
        arpData = a.readlines()

    """loop threw the arp -a return leave out the first blank line, then go threw each line and extract the MAC from the 
    line + store it in a new list. if no MAC on the line new list gets ' '"""
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

    back = []
    for i, ip in enumerate(IPs):
        back.append(f"{IPs[i]}: {macs[i]}")

    return back


def myPing(IP, v='y'):
    import re
    answer = []

    #test user input
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",IP) == None:
        raise ValueError (f"{IP} is not a valid IP address")
    # os.popen allows you to work the windows command line, "as a" lets us take the return and store it by line in a list
    with os.popen(f"ping {IP}") as a:
        pingData = a.readlines()

    pingReturn = []
    for data in pingData:
        if data != "\n":
            pingReturn.append(data)

    if v.lower() == 'y':
        try:
            answer = [pingReturn[1], pingReturn[2], pingReturn[3], pingReturn[4], pingReturn[6]]
        except IndexError:
            raise ValueError (f"{IP} is not a valid IP address")

    elif v.lower() == 'n':
        test = re.search('Destination host unreachable.', pingReturn[1])
        if test is None:
            return True
        else:
            return False
    else:
        print(f"must pyPing requires 1 argument and an option one for verbose as y or n. you provided {v}")

    return answer
