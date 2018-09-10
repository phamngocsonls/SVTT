# Tìm hiểu về Neutron Networking

## Mục lục

* [1. Overview Openstack Networking](#1)
* [2. Openstack Networking Components](#2)
* [3. Network connectivity of physical server](#3)
* [4. Networking service](#4)


<a name="1"></a>

# 1. Overview Openstack Networking

- Openstack Networking có nhiệm vụ tạo và quản lý các mạng lưới virtual networking trong Openstack cloud bao gồm: networks, subnets, routers, sâu hơn nữa là các service như firewalls hoặc VPN-virtual private networks
- Openstack networking cung cấp cho người quản trị cloud tính linh hoạt trong việc quyết định service nào hoạt động trên hạ tầng physical. Mỗi service có thể nằm trên 1 host physical hoặc có thể nằm trên nhiều host physical, phục vụ dự phòng 

* Ưu điểm của Neutron networking:
    * User có thể tạo networks, control traffic, connect server, device tới more networks
    * Openstack offer tính linh hoạt trong networking
    * IP can be dedicated or floating, floating IP cho phép traffic dynamic rẻouting

<a name="2"></a>

# 2. Openstack Networking Components
    
Openstack Networking Architecture:

![Imgur](https://i.imgur.com/d0JXsDX.png)

* **neutron-server:**
Service này chạy trên các network node, cung cấp các API và kết nối trực tiếp tới database

* **plugin agent:**
Chạy trên mỗi compute node để quản lý virtual switch

* **DHCP agent:**
Cung cấp DHCP service cho project network

* **L3 agent:**
Cung cấp L3/NAT cho VM để access to external network

* **Network provider service(SDN server/service):**
Cung cấp các dịch vụ mạng bổ sung cho project network


<a name="3"></a>

# 3. Network connectivity of physical server

![Imgur](https://i.imgur.com/x2cZHTA.png)

Một standard Openstack networking có 4 loại network như sau:

* Management network:
    - Sử dụng cho việc comminicate giữa các Openstack service
    - IP address on this network được sử dụng trong local 

* Guest network:
    - Sử dụng cho viêc communicate VM data trong môi trường cloud deployment
    - IP address phục thuộc vào Openstack Networking pluggin được sử dụng và configuration network cho từng virtual network

* External network:
    - Sử dụng để cho VM access ra ngoài Internet

* API network
    - Exxposes Openstack APIs, including the Openstack Networking API

<a name="4"></a>

# 4. Networking service

Openstack networking tạo ra một dịch vụ mạng ảo hóa như:

* **L2 isolation using VLANs and tuneling**
Openstack networking service sử dụng hai cơ chế khác nhau để cô lập và tách biệt traffic là: VLANs và L2 tunnels sử dụng GRE encapsulation

* **VLANs:**
    - VLAN là virtual VLAN, được dùng để cô lập traffic giữa các project trong cùng một network
    - Các VLAN được phân biệt với nhau bởi VLAN ID
    - 1 ports mà cho tất cả các VLAN đi qua, gọi là `trunk port`

* **L2 tunneling**
    - Network tuneling đóng gói traffic và gửi qua một tunnel-đường hầm
    - Bằng cách đóng gói traffic trong IP packets, traffic có thể đi qua Layer-3 trong mạng
    - Openstack networking hỗ trợ 2 loại tunnel phổ biến là: GRE và VXLAN


* **Access controll lists**
    - Sử dung security groups applied to all virtual interfaces ports trên mỗi VM qua `iptables`
    - Security groups cho phép chúng ta kiểm soát traffic vào/ra qua từng virtal interface và có thể kiểm soát L2-L4 traffics
Lưu ý: Khi sử dụng Openstack networking service, ta nên sử dụng security groups trong mỗi service và nên disabled trong Compute service


* **L3 routing and NAT**
    - Openstack networking routers kết nối tới multiple L2 networks, provide a `gateway` forr one or more private L2 networks
    - L3 router hỗ trợ NAT trên `gateway port` để cho phép các private network access to the external network


* **Quality os Service(QoS):**
    - Cloud adminitrator set policies and rules cho từng port cụ thể
    - Networking service support bandwidth-limiting QoS rule, nó có tên là **QosBandwidthLimitRule**, trong đó thiết lập:
        - max-kbps: Bandwidth
        - max-burst-kbps: Burst buffer
    - QosBandwidthRuleLimit hoạt động trên Open vSwitch, Linux bridge


* **Load Balancing**
    - Openstack Networking supports Load-Balance-as-a-service(LBaaS), dựa trên HA_Proxy


* **Firewall-as-a-Service(FWaaS):**
    - Openstack firewall liên quan tới việc thiết lập các policy và rule. Một policy là tập hợp của các rules. Mỗi rules quy định về các thuộc tính như(port ranges, protocol, IP address) 
    - A policy có thể được made public hoặc có thể share giữa các projects
    - Firewall được thực hiện theo nhiều cách khác nhau, phụ thuộc vào driver được sử dụng, có thể là dùng `iptables rules`, `flow tables` trong OpenVSwitch

## FWaaS v1:
- FWaaS v1 provides protection cho routers. Khi firewall được apply trên router, tất cả internal port đều được protected
- Ví dụ dưới đây mô tả flow ingress/engress for VM2:

![Imgur](https://i.imgur.com/jvyNgMR.png)


## FWaaS v2:
- FWaaS cung cấp đa dạng hơn về mặt policy cũng như rule
- FWaaS v2 áp đặt các policy dưới dạng firewall group, bao gồm ingress policy và engress policy
- FWaaS v2 không apply all router level mà chỉ apply ở mức port level


## So sánh FWaaS v1 và v2
Bảng so sánh đặc điểm của v1 và v2.  

|Feature|v1|v2|
|---|---|---|
|Supports L3 firewalling for routers|YES|NO*|
|Supports L3 firewalling for router ports|NO|YES|
|Supports L2 firewalling (VM ports)|NO|NO**|
|CLI support|YES|YES|
|Horizon support|YES|NO|