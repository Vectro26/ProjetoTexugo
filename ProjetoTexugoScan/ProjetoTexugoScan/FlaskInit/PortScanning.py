import ReverseDNS as IP
import socket
StatusPort = []
def PortScannerVerification(URL):
     ports = [21,22,23,80]
     IpPort =IP.GetIp(URL)
     for port in ports: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) 
        codeReturn = sock.connect_ex((IpPort, port))  
        sock.close() 
        if codeReturn == 0:
             print (port)
             StatusPort.append(str(port))

             return StatusPort