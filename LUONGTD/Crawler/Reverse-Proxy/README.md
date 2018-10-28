# Reverse Proxy Maket Share

## Performs CDN detection by:
- DNS, using the ```nslookup``` command
- HTTP headers
- access the cdn subdomain of the specified hostname 
- ```whois``` command's
- information disclosure from server error

## Requirements
- Install pip:
```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

- Install the necessary python packages:
```sh
pip install -r requirements.txt
```

## Usage

To scan Alexa-top-1m websites:
```
python main.py
```

## CDN supported

* Cloudflare
* Incapsula
* Cloudfront
* Akamai
* Airee
* CacheFly
* EdgeCast
* MaxCDN
* Beluga
* Limelight
* Fastly
* Myracloud
* Microsft Azure

## TODO
* Dosarrest
* Azion
* ArvanCloud
* Beluga
* DN77
* CDNetwork
* CDNsun
* CDNvideo
* ChinaCache
* ChinaNetCenter
* Highwinds
* KeyCDN
* Level3
* NGENIX
* Quantil
* SkyparkCDN
* Verizon Digital Media services
* Turbobyte

## Issues:
