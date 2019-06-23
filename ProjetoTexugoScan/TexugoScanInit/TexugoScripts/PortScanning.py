import nmap
import ReverseDNS as IP
def PortScannerVerification(URL):
     scanNmap= nmap.PortScanner()
     scanNmap.scan(IP.GetIp(URL))
     for host in scanNmap.all_hosts():
        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, scanNmap[host].hostname()))
     print('State : %s' % scanNmap[host].state())
     for proto in scanNmap[host].all_protocols():
        print('----------')
        print('Protocol : %s' % proto)
 
        lport = scanNmap[host][proto].keys()
        lport.sort()
        for port in lport:
            print ('port : %s\tstate : %s' % (port, scanNmap[host][proto][port]['state']))