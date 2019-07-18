import requests
BannerList= []

def BannerCollect(url):
    
    result= requests.head(url)

    for cabecalho,conteudo in result.headers.items():
        print(cabecalho,":",conteudo)
        BannerList.append(cabecalho+":"+conteudo)
                
        return BannerList       

