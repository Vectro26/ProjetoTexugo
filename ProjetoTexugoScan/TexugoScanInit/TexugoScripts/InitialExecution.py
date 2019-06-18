import Verification  
import time
import BannerGrabing 
import Whois 
import EnumerationSubdomain
class Init:
    if __name__ == '__main__':
        URL =""
       

    URL=input("enter the URL to start the collection")    
    ini = time.time()
    request= Verification.URLVerification(URL)
    fim = time.time()    
   
    
    if request== True:
        BannerGrabing.BannerCollect(URL)
        Whois.WhoisCollect(URL)
        EnumerationSubdomain.BruteforceEnumeration(URL) 
    else: 
        pass