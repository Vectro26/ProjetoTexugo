import socket 
import Whois as URLAdequacy
def ReverseNameDNS(URL):

    
    try:
       IP =  GetIp(URL) 
       nameServer=socket.gethostbyaddr(IP)
       return nameServer[0]
    except socket.error as e:
        return "None"
     
    

def GetIp(URL):

 IP=socket.gethostbyname(URLAdequacy.AdequacyURL(URL))

 return IP