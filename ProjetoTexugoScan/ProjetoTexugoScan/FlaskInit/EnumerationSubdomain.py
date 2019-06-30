import os
import Whois as detected
import socket
from multiprocessing.pool import ThreadPool as Pool

domain = ""
subdomainList=[]
domainDetected=[]
def BruteforceEnumeration(URL):
    print("Anderson")
    domain = detected.AdequacyURL(URL)
    ListGenerate(domain)
    
def ListGenerate(domain):

    with open('/home/vectro26/Documentos/TexugoScan/ProjetoTexugoScan/ProjetoTexugoScan/FlaskInit/bruteforceSubdomain') as names:
        dnsName=names.readlines()
        
    for subdomain in dnsName :
            print(subdomain.strip("\n")+"."+domain)
            subdomainList.append(subdomain.strip("\n")+"."+domain)
    pool = Pool(processes=os.cpu_count())
    pool.map(TestRequest, subdomainList)
def TestRequest(subdomainList):
    try: 
            domainDetected.append("Subdomain:"+subdomainList+"IP"+socket.gethostbyname(subdomainList))
    except socket.gaierror: 
        pass
