# Reverse Proxy Maket Share

## Performs CDN detection by:
- DNS, using the ```nslookup``` command
- HTTP headers
- access the cdn subdomain of the specified hostname 
- ```whois``` command's
- information disclosure from server error

## Requirements
- python >= 2.7.9
- OpenSSL==1.0.2o (tested)
```
wget https://www.openssl.org/source/openssl-1.0.2o.tar.gz
tar xzvf openssl-1.0.2o.tar.gz
cd openssl-1.0.2o
./config -Wl,--enable-new-dtags,-rpath,'$(LIBRPATH)'
make
sudo make install

openssl version -a
```

- Install pip:
```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.python
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
* MaxCDN
* Beluga
* Limelight
* Fastly
* Myracloud
* Microsft Azure
* CDNetwork
* Quantil
* Sucuri
* ChinaCache
* ChinaCache
* Grey Wizard
* BitGravity
* CacheFly
* Dosarrest
* Azion
* ArvanCloud
* Verizon Digital Media
* Level3

## Issues:
