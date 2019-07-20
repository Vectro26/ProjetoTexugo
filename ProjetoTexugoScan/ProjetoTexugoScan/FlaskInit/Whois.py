import whois
import tldextract


def WhoisCollect(URL):

    domainURL = AdequacyURL(URL)
    try:
        result = whois.query(domainURL)
        print(result.__dict__)
        return (result.__dict__)
    except :  #NOT FOUND
        return 'None'   
    
    
    


def AdequacyURL(URL):
    domainDetected = tldextract.extract(URL)
    URLFormated = ".".join(domainDetected[:3])
    if URLFormated[0]==".":

                newUrl= list(URLFormated)
                newUrl[0]=""
                URLFormated=''.join(newUrl)
                return (URLFormated)
    else:
                return (URLFormated.replace("www.",""))

