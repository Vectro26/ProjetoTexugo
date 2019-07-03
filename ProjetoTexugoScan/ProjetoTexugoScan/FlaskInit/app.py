from flask import Flask, render_template, request, url_for, redirect, make_response
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

app = Flask(__name__)


@app.route('/')
def index():

    return render_template("index.html")


@app.route('/result',methods=['POST'])
def result(Port): 
    if request.args.get('banner'):
        banner= request.args['banner']
    else:
        banner=""
    
    return  render_template('result.html', banner=banner)
    #return response


@app.route('/collect', methods=['POST'])
def collect():
    URL = request.form['url']

    requests = Verification.URLVerification(URL)
    if requests == True:
        Subdomain= EnumerationSubdomain.BruteforceEnumeration(URL)
        Banner = BannerGrabing.BannerCollect(URL)
        whois = Whois.WhoisCollect(URL)
        Port = PortScanning.PortScannerVerification(URL)
        Technology = TechnologyIdentification.TechnologyIdentification(URL)
        IP = IpBlock.WhoisCollect(URL)
        DNS = ReverseDNS.ReverseNameDNS(URL)
        return render_template('tables.html',banner=Banner,port=Port,whois=whois,nameServer=DNS,IpBlock=IP,Technology=Technology,subdomain=Subdomain)
    else:
        return  render_template('result.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
