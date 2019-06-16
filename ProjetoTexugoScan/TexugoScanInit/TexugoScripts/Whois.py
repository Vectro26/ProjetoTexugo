import whois
import tldextract



def WhoisCollect(URL):
    
    domainDetected = tldextract.extract(URL) 
    domainURL=".".join(domainDetected[:3])
    print(domainURL)
    result = whois.query(domainURL)
    print(result.name)
    print(result.name_servers)
    print(result.registrar)
    print(result.creation_date)
    print(result.expiration_date)
    