# ARPTools
the ARP function is the root of this package. it returns dict with IP address as the key and there value is the mac address for the system (as listed in the arp tables)

```ARPTools.arp()```
This returns a dict of mac address IP address pairs
this function takes no arguments

```ARPTools.getHostName()```
This function takes a valid IP address (as a string) and returns a string of the target systems hostname. If the host can't be found or a valid IP address isn't provided, it returns ```None```

```ARPTools.myPing()```
This function takes a valid IP address (as a string) and optionaly 'verbose' as a flag. This function will either return a string explaing the ping result (as a normal system console would) or if 'verbose' is passed 'n' will simply return a bool representing if the provided IP address is able to be pinged or not.
Parameters: ```verbose``` - this flag by default is 'y' witch provides a string explaing the ping results. if 'n' is provided will return a bool ```True``` if the system is online and ```False``` if it can't be reached
```v``` - same as ```verbose```
```count``` - provide a int for the number of packets to send in the ping (this will only be used if ```verbose``` is 'y')
```c``` - same as ```count```
