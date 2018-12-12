## Install Suricata + ELK:

### 1. Install suricata:

Install dependences:

```
apt -y install libpcre3 libpcre3-dev build-essential autoconf automake libtool libpcap-dev libnet1-dev libyaml-0-2 libyaml-dev zlib1g zlib1g-dev libmagic-dev libcap-ng-dev libjansson-dev pkg-config libnetfilter-queue-dev geoip-bin geoip-database geoipupdate apt-transport-https
```

Install suricata and suricata-update:

```
add-apt-repository ppa:oisf/suricata-stable
apt-get update
apt-get install suricata

vi /etc/suricata/suricata.yaml
vi /etc/default/suricata
```

And replace all instances of eth0 with the actual adaptor name: enp8s0 (in my computer)

#### Install suricata-update:

Install suricata update to update and download suricata rules:

```
apt install python-pip
pip install pyyaml
pip install https://github.com/OISF/suricata-update/archive/master.zip
```

Update suricata run:

```
pip install --pre --upgrade suricata-update
```

#### Update the rules

Without doing any configuration the default operation of suricata-update is use the Emerging Threats Open ruleset.

```
suricata-update
```

#### Reference
[https://www.howtoforge.com/tutorial/suricata-with-elk-and-web-front-ends-on-ubuntu-bionic-beaver-1804-lts/](https://www.howtoforge.com/tutorial/suricata-with-elk-and-web-front-ends-on-ubuntu-bionic-beaver-1804-lts/)

### 2. Install ELK

Add Oracle Java Repository

```
sudo add-apt-repository ppa:webupd8team/java
```

Download and install the public GPG signing key

```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
```

Download and install apt-transport-https package

```
sudo apt-get install apt-transport-https
```

Add Elasticsearch|Logstash|Kibana Repositories (version 6+) 

```
echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list

sudo apt-get update
```

Install Java8:

```
sudo apt-get install oracle-java8-installer
```

**Install Elasticsearch + Kibana + Logstash**

```
sudo apt-get install elasticsearch && sudo apt-get install kibana && sudo apt-get install logstash
```

Configure Kibana

```
sudo nano /etc/kibana/kibana.yml
```

add the lines:

```
server.port: 5601
server.host: "0.0.0.0"
```

Change Directory

```
cd /etc/logstash/conf.d
```

Download the following configuration files

```
sudo wget https://raw.githubusercontent.com/a3ilson/pfelk/master/01-inputs.conf
sudo wget https://raw.githubusercontent.com/a3ilson/pfelk/master/10-syslog.conf
sudo wget https://raw.githubusercontent.com/a3ilson/pfelk/master/11-pfsense.conf
sudo wget https://raw.githubusercontent.com/a3ilson/pfelk/master/30-outputs.conf
```

Make Patterns Folder

```
sudo mkdir /etc/logstash/conf.d/patterns
cd /etc/logstash/conf.d/patterns/
```

Download the following configuration file

```
sudo wget https://raw.githubusercontent.com/a3ilson/pfelk/master/pfsense_2_4_2.grok
sudo vi /etc/logstash/conf.d/10-syslog.conf
```
change host to 192.168.1.1

```
filter {  
  if [type] == "syslog" {
    #change to pfSense ip address
    if [host] =~ /192\.168\.1\.1/ {
      mutate {
        add_tag => ["PFSense", "Ready"]
      }
    }
    if "Ready" not in [tags] {
      mutate {
        add_tag => [ "syslog" ]
      }
    }
  }
}
```

```
sudo vi /etc/logstash/conf.d/11-pfsense.conf
```

change timezone to "Asia/Ho_Chi_Minh_city"

```
cd /etc/logstash
```

Download and install the MaxMind GeoIP database (recommended)

```
sudo wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
sudo gunzip GeoLite2-City.mmdb.gz

```

Automatic Start (on boot)

```
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
sudo /bin/systemctl enable kibana.service
sudo /bin/systemctl enable logstash.service
```

Manual Start

```
sudo -i service elasticsearch start
sudo -i service kibana start
sudo -i service logstash start
```

check ELK service

```
systemctl status elasticsearch.service
systemctl status kibana.service
systemctl status logstash.service
```

To view Logstash Log

```
vi /var/log/logstash
```