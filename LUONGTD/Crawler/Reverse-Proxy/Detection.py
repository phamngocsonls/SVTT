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
    'Cloudfront': 'Cloudfront',
    'Akamai': 'Akamai',
    'Airee': 'Airee',
    'CacheFly': 'CacheFly',
    'EdgeCast': 'EdgeCast',
    'stackpath': 'Stack Path',
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
	'CDNetwork': 'CDNetwork',
	'CDNsun': 'CDNsun',
	'CDNvideo': 'CDNvideo',
	'ChinaCache': 'ChinaCache',
	'ChinaNetCenter': 'ChinaNetCenter',
	'Highwinds': 'Highwinds',
	'KeyCDN': 'KeyCDN',
	'centurylink': 'Level3',
	'NGENIX': 'NGENIX',
	'Quantil': 'Quantil',
	'SkyparkCDN': 'SkyparkCDN',
	'VerizonDigitalMedia': 'Verizon Digital Media services',
	'Turbobyte': 'Turbobyte',
	'Sucuri': 'Sucuri',
	'Dosarrest': 'Dosarrest',
	'Greywizard': 'Greywizard',
	'BitGravity': 'BitGravity',
	'Instartlogic': 'Instartlogic'
}


###Detect functions
def find(data):
	#data = data.lower()
    for keyword, description in CDN.items():		
        if data.find(keyword.lower()) != -1:
            return description
    return -1

def DNS_detect(hostname):
	hostname = urlparse.urlparse(hostname).netloc

	regexp = re.compile('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b')

	out = commands.getoutput("host " + hostname)
	
	finder = find(out)
	if finder != -1:
		return finder

	addresses = regexp.finditer(out)

	for addr in addresses:
		x = find(commands.getoutput('nslookup ' + addr.group()))
		if x != -1:
			return x

	return -1


def HTTP_detect(hostname):
    #print('[+] HTTP detection\n')

	hostname = urlparse.urlparse(hostname).scheme + '://' + urlparse.urlparse(hostname).netloc

	fields = {
		'Server': True,
		'X-CDN': True,
		'x-cache': True,
		'X-CDN-Forward': True,
		'Fastly-Debug-Digest': False
	}

	req = request_do(hostname)

	if req is None:
		return

	for field, state in fields.items():
		value = req.headers.get(field)
		if state and value is not None:
			x = find(value.lower())
			if x != -1:
				return x
		elif not state and value is not None:
			x = find(field.lower())
			if x != -1:
				return x

	return -1


def Subdomain_detect(hostname):
	hostname = "cdn." + urlparse.urlparse(hostname).netloc

	out = commands.getoutput("host -a " + hostname)

	x = find(out.lower())
	if x != -1:
		return x
	return -1


def Whois_detect(hostname):
	hostname = urlparse.urlparse(hostname).netloc

	out = commands.getoutput("whois " + hostname)

	x = find(out.lower())
	if x != -1:
		return x
	return -1


def ErrorServer_detect(hostname):

    print('[+] Error server detection\n')

    hostname = urlparse.urlparse(hostname).netloc
    regexp = re.compile('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b')
    out = commands.getoutput("host " + hostname)
    addresses = regexp.finditer(out)
    for addr in addresses:
        res = request_do("http://" + addr.group())
        if res is not None and res.status_code == 500:
            x = find(res.text.lower())
            if x != -1:
            	return x
    return -1
