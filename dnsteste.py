import socket 
  
IP = socket.gethostbyname("carnaubais.rn.gov.br")
nameServer=socket.gethostbyaddr(IP)
print(nameServer)