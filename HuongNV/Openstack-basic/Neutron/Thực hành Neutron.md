# Một vài tìm hiểu về thực hành Neutron trên Devstack

## Mục lục

* [1. Sử dụng Neutron command line](#1)
    * [1.1 Listing network](#11)
    * [1.2 Show network information](#12)
    * [1.3 Update network](#13)
    * [1.4 Listing port](#14)
    * [1.5 Show port information](#15)
    * [1.6 Update port information](#16)
    * [1.7 Listing security-group](#17)

* [2. Sử dụng Dashboard](#2)  


<a name="11"></a>

# 1.1 Listing network
Sử dụng Neutron CLI:
```
usage: neutron net-list [-h] [-f {csv,html,json,table,value,yaml}] [-c COLUMN]
                        [--max-width <integer>] [--print-empty] [--noindent]
                        [--quote {all,minimal,none,nonnumeric}]
                        [--request-format {json}] [-D] [-F FIELD] [-P SIZE]
                        [--sort-key FIELD] [--sort-dir {asc,desc}]
                        [--tenant-id TENANT_ID] [--name NAME]
                        [--admin-state-up {True,False}] [--status STATUS]
                        [--shared {True,False}]
                        [--router:external {True,False}] [--tags TAG]
                        [--tags-any TAG] [--not-tags TAG] [--not-tags-any TAG]
```
![Imgur](https://i.imgur.com/fihC9GC.png)

<a name="12"></a>

# 1.2 Show network information
Sử dụng:
```
usage: neutron net-show [-h] [-f {html,json,shell,table,value,yaml}]
                        [-c COLUMN] [--max-width <integer>] [--print-empty]
                        [--noindent] [--prefix PREFIX]
                        [--request-format {json}] [-D] [-F FIELD]
                        NETWORK
```
![Imgur](https://i.imgur.com/QRe3TuM.png)

<a name="13"></a>

# 1.3 Update network

Sử dụng:
```
usage: neutron net-update [-h] [--request-format {json}] [--name NAME]
                          [--description DESCRIPTION]
                          [--qos-policy QOS_POLICY | --no-qos-policy]
                          [--dns-domain DNS_DOMAIN | --no-dns-domain]
                          NETWORK
```

<a name="14"></a>

# 1.4 Listing port
Sử dụng:
```
usage: neutron port-list [-h] [-f {csv,html,json,table,value,yaml}]
                         [-c COLUMN] [--max-width <integer>] [--print-empty]
                         [--noindent] [--quote {all,minimal,none,nonnumeric}]
                         [--request-format {json}] [-D] [-F FIELD] [-P SIZE]
                         [--sort-key FIELD] [--sort-dir {asc,desc}]
```
- Ví dụ: Liệt kê tất cả các port của các subnet 
![Imgur](https://i.imgur.com/0XR82rg.png)
<a name="15"></a>

# 1.5  Show port information 
Sử dụng:
```
usage: neutron port-show [-h] [-f {html,json,shell,table,value,yaml}]
                         [-c COLUMN] [--max-width <integer>] [--print-empty]
                         [--noindent] [--prefix PREFIX]
                         [--request-format {json}] [-D] [-F FIELD]
                         PORT
```
Ví dụ: Hiển thị các thông số về port như: trạng thái port-security, security-groups
![Imgur](https://i.imgur.com/QnzWF27.png)

<a name="16"></a>

# 1.6 Update port information 
Sử dụng:
```
usage: neutron port-update [-h] [--request-format {json}] [--name NAME]
                           [--description DESCRIPTION]
                           [--fixed-ip subnet_id=SUBNET,ip_address=IP_ADDR]
                           [--device-id DEVICE_ID]
                           [--device-owner DEVICE_OWNER]
                           [--admin-state-up {True,False}]
                           [--security-group SECURITY_GROUP | --no-security-groups]
                           [--extra-dhcp-opt EXTRA_DHCP_OPTS]
                           [--qos-policy QOS_POLICY | --no-qos-policy]
                           [--allowed-address-pair ip_address=IP_ADDR[,mac_address=MAC_ADDR]
                           | --no-allowed-address-pairs]
                           [--dns-name DNS_NAME | --no-dns-name]
                           PORT
```
Ví dụ: Thực hiện enabled port-security đi, mặc định thuộc tính này sẽ luôn False(đây là một tính năng rất quan trong trong Neutron)
![Imgur](https://i.imgur.com/JOT7MO9.png)

<a name="17"></a>

# 1.7 Listing security-group
- Security group là 1 tính năng rất quan trọng trong Neutron, mục đích của nó nhằm kiểm soát traffic ra vào VMs
- Sử dụng:
```
usage: neutron security-group-list [-h] [-f {csv,html,json,table,value,yaml}]
                                   [-c COLUMN] [--max-width <integer>]
                                   [--print-empty] [--noindent]
                                   [--quote {all,minimal,none,nonnumeric}]
                                   [--request-format {json}] [-D] [-F FIELD]
                                   [-P SIZE] [--sort-key FIELD]
                                   [--sort-dir {asc,desc}]
```
Ví dụ liệt kê tất cả security-group
![Imgur](https://i.imgur.com/fftmeF4.png)

<a name="2"></a>

# 2. Sử dụng Dashboard
- Sử dụng Dashboard cực kì dễ thao tác với Neutron
- Liệt kê các Network có trong project:
![Imgur](https://i.imgur.com/IZzZG6u.png)

- Liệt kê các port có trong 1 network cụ thể
![Imgur](https://i.imgur.com/gkGOUWL.png)