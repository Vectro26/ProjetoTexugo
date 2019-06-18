import whois
import tldextract



def WhoisCollect(URL):

    domainURL= AdequacyURL(URL)
    print(domainURL)
    result = whois.whois(domainURL)
    print(result.text)
def AdequacyURL(URL):
    domainDetected = tldextract.extract(URL)
    URLFormated=".".join(domainDetected[:3])
    return URLFormated
