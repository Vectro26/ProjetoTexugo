import pdfkit
import Verification
import time
import BannerGrabing
import Whois
import EnumerationSubdomain
import PortScanning
import ReverseDNS
import TechnologyIdentification
import IpBlock
import csv

    
def execution(urls):
        print(urls)
        ini = time.time()
        request= Verification.URLVerification(urls)
        print(urls)
        if request== True:
            print("Valor")
            Subdomain = EnumerationSubdomain.BruteforceEnumeration(urls)
            QtdSub= len(Subdomain)
            Banner = BannerGrabing.BannerCollect(urls)
            whois = Whois.WhoisCollect(urls)
            Port = PortScanning.PortScannerVerification(urls)
            Technology = TechnologyIdentification.TechnologyIdentification(urls)
            IP = IpBlock.WhoisCollect(urls)
            DNS = ReverseDNS.ReverseNameDNS(urls)
            fim = time.time() 
            valortempo=ini-fim         
        with open('/home/vectro26/Documentos/TexugoScan/ProjetoTexugoScan/ProjetoTexugoScan/FlaskInit/Validação TCC - Página6.csv', 'a', newline='\n') as csvfile:
            print("Adicionando ao CSV")
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow([whois,Port ,Subdomain,IP,Banner,DNS,Technology,valortempo,QtdSub ])
        
    


if __name__ == '__main__':        
        with open("/home/vectro26/Documentos/TexugoScan/ProjetoTexugoScan/ProjetoTexugoScan/alvos.txt") as file:
            for urls in file :
                execution(urls)
                
        
