import socket 
import Whois as URLAdequacy
def ReverseNameDNS(URL):

    IP =  GetIp(URL)
    nameServer=socket.gethostbyaddr(IP) 
    return nameServer[0]

def GetIp(URL):

 IP=socket.gethostbyname(URLAdequacy.AdequacyURL(URL))

 return IP