import socket
import urllib.request  as urllib2 


    
def URLVerification(url):
    socket.setdefaulttimeout( 23 )  
    
    
    try:
            response = urllib2.urlopen( url )
    except urllib2.HTTPError as err:
           if err.code == 404:
               return False
    except urllib2.URLError:
                return False
    else:
                return True