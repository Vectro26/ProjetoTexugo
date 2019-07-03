import os
import Whois as detected
import socket
from multiprocessing.pool import ThreadPool as Pool

domain = ""
subdomainList=[]
domainDetected=[]
def BruteforceEnumeration(URL):
    domain = detected.AdequacyURL(URL)
    ListGenerate(domain)
    return domainDetected
def ListGenerate(domain):

    with open('ProjetoTexugoScan/ProjetoTexugoScan/FlaskInit/bruteforceSubdomain/subdomainNames.txt') as names:
        dnsName=names.readlines()
        
    for subdomain in dnsName :
            #print(subdomain.strip("\n")+"."+domain)
            subdomainList.append(subdomain.strip("\n")+"."+domain)
    pool = Pool(processes=os.cpu_count())
    pool.map(TestRequest, subdomainList)
    
def TestRequest(subdomainList):
    try:   
         domainDetected.append("IP:"+socket.gethostbyname(subdomainList)+  "Subdomain:"+subdomainList) 
    except socket.gaierror: 
        pass
                