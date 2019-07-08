import socket
import re
  
         
IP=socket.gethostbyname_ex("www.carnaubais.rn.gov.br")
check = ''.join(str(IP))
        
if re.search('\\b.domain.name\\b', check, re.IGNORECASE):
        print("Tem o domain.name")
else:
        print("Não tem")       
   

