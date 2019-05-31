# VPNaaS
## Cài đặt
**Môi trường** Môi trường cài đặt là DevStack phiên bản Pike chỉnh sửa file local.conf trước khi cài đặt.  [Xem hướng dẫn cài DevStack](https://docs.openstack.org/devstack/latest/)

```
[[local|localrc]]

ADMIN_PASSWORD=sh
DATABASE_PASSWORD=sh
RABBIT_PASSWORD=sh
SERVICE_PASSWORD=sh


GIT_BASE=http://github.com
HOST_IP=192.168.2.53
#HOST_IPV6=2001:db8::7

disable_service tempest

disable_service n-net
enable_service q-svc
enable_service q-agt
enable_service q-dhcp
enable_service q-l3
enable_service q-meta

enable_plugin neutron-vpnaas https://github.com/openstack/neutron-vpnaas stable/pike
enable_plugin neutron-vpnaas-dashboard https://github.com/openstack/neutron-vpnaas-dashboard stable/pike

IPSEC_PACKAGE="strongswan"
```
**Lab1: Sử dụng VPNaaS đê truy cập vào mạng nội bộ của nhau**

Mục tiêu: Kết nối 2 vùng mạng riêng với nhau bằng VPN site-to-site

Launch  instance vmE kết nối với net_east và vmW kết nối với net_west. Lưu ý rằng security group của 2  instance này phải cho phép ping.

net_west:
Subnet : 10.10.10.0/24
Gateway of External network: 127.24.4.5

net_east:
Subnet : 20.20.20.0/24
Gateway of External network: 172.24.4.3

Mô hình mạng:

<img src="https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/image/network_topology.png?raw=true">

Tạo ike policy
```
neutron vpn-ikepolicy-create ikepolicy1
```
Tạo ipec policy
```
neutron vpn-ipsecpolicy-create ipsecpolicy1
```
Tạo vpn-service service
```
neutron vpn-service-create ROUTER SUBNET
```
Tạo 2 vpn-service cho 2 router và subnet như hình

<img src="https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/image/vpn-service.png?raw=true">

Tạo site-to-site connection, nếu muốn tạo kêt nối 2 chiều thì tạo 2 site-to-site, như hình tạo kết nối từ vm1 đến vm2.

<img src="https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/image/site1-to-site2.png?raw=true">

Hiện tại đang bị lỗi về phần lab, sẽ update sau.

<img src="https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/image/down.png?raw=true">

## Update fix lỗi
Khi bị lỗi trên, tiếp tục tạo thêm site2-to-site1. Thường thì sau khi tạo site2-to-site1 sẽ được active, site1-to-site2 vẫn down. Trong trường hơp găp lỗi treo ở trang thái pending của Site-connection thi restart dịch vụ neutron. Để fix lỗi vừa nêu trên cũng restart dịch vụ neutron:
```
sudo service devstack@q-* restart
```
Sau khi restart dịch vụ sẽ được kêt quả sau:

<img src="https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/image/down.png?raw=true">

Tiến hành thử nghiệm ở vmE: ip 20.20.20.1
```
ping 10.10.10.12
``` 

<img src="https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/image/ping.png?raw=true">

