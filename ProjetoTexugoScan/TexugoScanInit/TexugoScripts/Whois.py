import whois
import tldextract


def WhoisCollect(URL):

    domainURL = AdequacyURL(URL)
    print(domainURL)
    result = whois.whois(domainURL)
    print(result.text)


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

