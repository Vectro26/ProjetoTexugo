from flask import Flask, render_template, request, url_for, redirect
import Verification  
import time
import BannerGrabing 
import Whois 
import EnumerationSubdomain
import PortScanning

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/collect',methods=['POST'])
def collect():
    URL= request.form['url']
    
    requests= Verification.URLVerification(URL)
    if requests== True:
        BannerGrabing.BannerCollect(URL)
        Whois.WhoisCollect(URL)
        PortScanning.PortScannerVerification(URL)
        EnumerationSubdomain.BruteforceEnumeration(URL)
        
        
        return 'OK'
    else: 
        return 'OK'
if __name__ == "__main__":
    app.debug = True
    app.run()
