import os
import Whois as detected
import socket
import re
from multiprocessing.pool import ThreadPool as Pool

domain = ""
subdomainList=[]
domainDetected=[]
def BruteforceEnumeration(URL):
    domain = detected.AdequacyURL(URL)
    ListGenerate(domain)
    return domainDetected
def ListGenerate(domain):

    with open('/home/vectro26/Documentos/TexugoScan/ProjetoTexugoScan/ProjetoTexugoScan/FlaskInit/bruteforceSubdomain/subdomainNames.txt') as names:
        dnsName=names.readlines()
        
    for subdomain in dnsName :
            #print(subdomain.strip("\n")+"."+domain)
            subdomainList.append(subdomain.strip("\n")+"."+domain)
    pool = Pool(processes=os.cpu_count())
    pool.map(TestRequest, subdomainList)
    
def TestRequest(subdomainList):
    try:  
         
        IP=socket.gethostbyname_ex(subdomainList)
        check = ''.join(str(IP))
        
        if re.search('\\b.domain.name\\b', check, re.IGNORECASE):
            pass
        else:
            domainDetected.append(check) 
    except socket.gaierror: 
        pass
