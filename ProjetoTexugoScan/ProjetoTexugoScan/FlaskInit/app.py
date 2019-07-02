from flask import Flask, render_template, request, url_for, redirect, make_response
import Verification  
import time
import BannerGrabing 
import Whois 
#import EnumerationSubdomain
import PortScanning
import ReverseDNS 
import TechnologyIdentification
import IpBlock

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
       # Banner=BannerGrabing.BannerCollect(URL)
        whois= Whois.WhoisCollect(URL)
        Port =PortScanning.PortScannerVerification(URL)
        Technology= TechnologyIdentification.TechnologyIdentification(URL)
        IP=IpBlock.WhoisCollect(URL)
        DNS=ReverseDNS.ReverseNameDNS(URL)
        return redirect('result.html',banner=Port)
    else: 
        return False
if __name__ == "__main__":
    app.debug = True
    app.run()
