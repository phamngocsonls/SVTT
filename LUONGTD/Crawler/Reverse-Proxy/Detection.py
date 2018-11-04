from __future__ import print_function
import sys
import re

if sys.version_info >= (3, 0):
	import subprocess as commands
	import urllib.parse as urlparse
else:
	import commands
	import urlparse

import signal
import requests

from bs4 import BeautifulSoup
import ast
import ssl
### Request

def request_do(hostname):
    try:
        return requests.get(hostname, timeout=3)

    except requests.ConnectionError:
        print("\033[1;31mServer not found: test aborted\n\033[1;m")
        return None

    except:
        print("\033[1;31mRequest timeout: test aborted\n\033[1;m")
        return None


CDN = {
    'CloudFlare': 'Cloudflare',
    'Incapsula': 'Incapsula',
    'Cloudfront': 'Amazon CloudFront',
    'Akamai': 'Akamai',
    'Airee': 'Airee',
    'CacheFly': 'CacheFly',
    'EdgeCast': 'EdgeCast',
    'stack.*path': 'Stack Path',
    'NetDNA': 'Stack Path',
    'MaxCDN': 'Stack Path',
    'Beluga': 'BelugaCDN',
    'Limelight': 'Limelight',
    'Fastly': 'Fastly',
    'Myra': 'Myracloud',
    'msecnd.ne': 'Microsoft Azure',
    'Clever-cloud': 'Clever Cloud',
    'Arion': 'Azion',
    'ArvanCloud': 'ArvanCloud',
    'Beluga': 'Beluga',
	'DN77': 'DN77',
	'CDNetwork': 'CDNetworks',
	#'h0-': 'CDNetworks',
	'CDNsun': 'CDNsun',
	'CDNvideo': 'CDNvideo',
	'ChinaCache': 'ChinaCache',
	'ChinaNetCenter': 'ChinaNetCenter',
	'Highwinds': 'Highwinds',
	'KeyCDN': 'KeyCDN',
	'centurylink': 'Level3',
	'NGENIX': 'NGENIX',
	'Quantil': 'Quantil',
	'MileWeb': 'Quantil',
	'yn[0-9]': 'Quantil',
	'SkyparkCDN': 'SkyparkCDN',
	'VerizonDigitalMedia': 'Verizon Digital Media',
	'EdgeCast': 'Verizon Digital Media',
	'Turbobyte': 'Turbobyte',
	'Sucuri': 'Sucuri',
	'Dosarrest': 'Dosarrest',
	#'github': 'Github Pages',
	'Greywizard': 'Grey Wizard',
	'BitGravity': 'BitGravity',
	'Instart.*logic': 'Instart Logic',
	#'google.*cloud': 'Google Cloud',
	'Netlify': 'Netlify',
	'Backtory': 'Backtory',
	'CFS': 'CacheFly',
	'fbs': 'Fireblade'
}


###Detect functions
def find(data):
    for keyword, description in CDN.items():		
        if re.findall(keyword.lower(), data) != []:
        	return description
    return -1

def DNS_detect(hostname, result):
	hostname = urlparse.urlparse(hostname).netloc
	result = []
	regexp = re.compile('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b')

	out = commands.getoutput("host " + hostname)
	
	finder = find(out)
	if finder != -1:
		result.append(finder)

	addresses = regexp.finditer(out)
	for addr in addresses:
		x = find(commands.getoutput('nslookup ' + addr.group()))
		if x != -1:
			if x not in result:
				result.append(x)
	return result


def HTTP_detect(hostname, result):
    #print('[+] HTTP detection\n')
	result = []
	hostname = urlparse.urlparse(hostname).scheme + '://' + urlparse.urlparse(hostname).netloc

	fields = {
		'Server': True,
		'X-CDN': True,
		'x-cache': True,
		'X-CDN-Forward': True,
		'X-Via': True,
		'Via': True,
		'X-Px':True,
		'Fastly-Debug-Digest': False
	}

	req = request_do(hostname)
	if req is None:
		return result
	#print(req.headers)
	if req.headers.get('X-Instart-Request-ID'):
		result.append('Instart Logic')

	if req.headers.get('Powered-By-ChinaCache'):
		result.append('ChinaCache')

	for field, state in fields.items():
		value = req.headers.get(field)
		if state and value is not None:
			x = find(value.lower())
			if x != -1:
				if x not in result:
					result.append(x)
		elif not state and value is not None:
			x = find(field.lower())
			if x != -1:
				if x not in result:
					result.append(x)
	return result


def Subdomain_detect(hostname, result):
	hostname = "cdn." + urlparse.urlparse(hostname).netloc
	out = commands.getoutput("host -a " + hostname)

	x = find(out.lower())
	if x != -1:
		if x not in result:
			result.append(x)
	return result


def Whois_detect(url, result):
	hostname = url.split('www.')[1]
	out1 = commands.getoutput("host " + hostname)
	if out1 != '':
		regexp = re.compile('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b')
		addresses = regexp.finditer(out1)
		for addr in addresses:	
			out2 = commands.getoutput("whois " + addr.group())
			x = find(out2.lower())
			if x != -1:
				if x not in result:
					result.append(x)
	else:
		hostname = urlparse.urlparse(url).netloc
		out1 = commands.getoutput("host " + hostname)
		if out1 != '':
			regexp = re.compile('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b')
			addresses = regexp.finditer(out1)
			for addr in addresses:	
				print(addr.group())
				out2 = commands.getoutput("whois " + addr.group())
				x = find(out2.lower())
				if x != -1:
					if x not in result:
						result.append(x)
	return result


def ErrorServer_detect(hostname):

    print('[+] Error server detection\n')

    hostname = urlparse.urlparse(hostname).netloc
    regexp = re.compile('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b')
    out = commands.getoutput("host " + hostname)
    addresses = regexp.finditer(out)
    for addr in addresses:
        res = request_do("http://" + addr.group())
        if res is not None and res.status_code == 500:
        	print("@@@@@@@@@@@@@@@@@@@@@@@@")
        	x = find(res.text.lower())
        	if x != -1:
        		print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
        		print(x)
        		return x
	return -1

def IP_detect(url):
	out = commands.getoutput("host " + url)
	regexp = re.compile('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b')
	addresses = regexp.finditer(out)
	for addr in addresses:
		x = addr.group()
		hostname = "http://ipinfo.io/" + x
		try:
			req = requests.get(hostname)
			soup = BeautifulSoup(req.text, "lxml")
			dic = ast.literal_eval(soup.p.string)
			x = find(dic["org"].lower())
			if x != -1:
				return x
		except:
			print("SLL Error!!")
	return -1
