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
```
**Lab1: Sử dụng VPNaaS đê truy cập vào mạng nội bộ của nhau**

Openstack1:
Subnet : 10.10.10.0/24
Gateway of External network: 200.200.128.100

Openstack2:
Subnet : 20.20.20.0/24
Gateway of External network: 200.200.128.151

Mô hình mạng:
<network_topology.png>

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
<vpn-service.png>

Tạo site-to-site connection, nếu muốn tạo kêt nối 2 chiều thì tạo 2 site-to-site, như hình tạo kết nối từ vm1 đến vm2.
<site-connection.png>

Hiện tại đang bị lỗi về phần lab, sẽ update sau.