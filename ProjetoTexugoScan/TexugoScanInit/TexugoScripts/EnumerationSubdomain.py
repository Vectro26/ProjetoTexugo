import os
import glob
import Whois as detected
import socket
from multiprocessing.pool import ThreadPool as Pool
domain = ""

def BruteforceEnumeration(URL):
    print("Anderson")
    domain = detected.AdequacyURL(URL)
    domain = URLAdaption(domain)
    ListGenerate(domain)
    
def URLAdaption(domainURL):
   return domainURL.replace("www.","")

def ListGenerate(domain):

    with open('/home/vectro26/Documentos/TexugoScan/ProjetoTexugoScan/TexugoScanInit/TexugoScripts/bruteforceSubdomain/names.txt') as names:
        dnsName=names.readlines()
        i=1
    for subdomain in dnsName :
            
            print(subdomain.strip("\n")+"."+domain)
            i=i+1    
            print(i)
def TestRequest(url):
    try: 
        print(socket.gethostbyname(url))  
    except socket.gaierror: 
        pass
