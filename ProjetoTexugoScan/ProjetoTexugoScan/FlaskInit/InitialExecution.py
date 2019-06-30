import Verification  
import time
import BannerGrabing 
import Whois 
import EnumerationSubdomain
import PortScanning
import IpBlock
class Init:
    if __name__ == '__main__':
        URL =""
       

    URL=input("enter the URL to start the collection")    
    ini = time.time()
    request= Verification.URLVerification(URL)
     
   
    
    if request== True:
        BannerGrabing.BannerCollect(URL)
        #PortScanning.PortScannerVerification(URL)
        Whois.WhoisCollect(URL)
        IpBlock.WhoisCollect(URL)
        EnumerationSubdomain.BruteforceEnumeration(URL)
        fim = time.time() 
        print(ini-fim)
    else: 
        pass