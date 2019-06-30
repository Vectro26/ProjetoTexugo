from flask import Flask, render_template, request, url_for, redirect, make_response
import Verification  
import time
import BannerGrabing 
import Whois 
import EnumerationSubdomain
import PortScanning
import ReverseDNS 
import TechnologyIdentification
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")
@app.route('/result')
def result():
    return render_template("result.html")


@app.route('/collect',methods=['POST'])
def collect():
    URL= request.form['url']
    
    requests= Verification.URLVerification(URL)
    if requests== True:
        BannerGrabing.BannerCollect(URL)
        Whois.WhoisCollect(URL)
        #PortScanning.PortScannerVerification(URL)
        EnumerationSubdomain.BruteforceEnumeration(URL)
        
        
        return 'OK'
    else: 
        return 'OK'
if __name__ == "__main__":
    app.debug = True
    app.run()
