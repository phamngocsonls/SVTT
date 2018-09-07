# tìm hiểu về Self-service và Provider Network


## Mục lục

* [1. Self-service Network](#1)
* [2. Provider Network](#2)


<a name="1"></a>

**1. Self-service network**

Self-service network được dùng cho general projects(non-privileged) mà không cần đến admin. Các mạng này đều là virtual network, nó cần virtual routers để có thể định tuyến giữa các traffic và access to thẻ Internet. Self-service provide DHCP và metadata service tới các instances

Trong thực tế, self-service sử dụng overlay protocol như VXLAN hoặc GRE. Ưu điểm là nó hỗ trợ many more networks khi là sử dụng VLAN tagging. Khi sử dụng VLAN tagging, ta cần phải configuration physical network infrastructure.

IPv4 self-service network sử dụng private IP address và interact with provider networks qua source NAT on virtual routers. Floating IP address được access tới instances từ provider network  qua destination NAT. IPv6 self-service network sủ dụng public IP address interact với provider networks qua virtual routers bằng static routes.

Networking service thực hiện định tuyến bằng cách sử dụng layer-3 agent, nó được đặt ở ít nhất 1 network node. Trái với provider network, kết nối từ instance tới physical network infrastructure tại layer-2, còn self-service network phải xử lý qua layer-3.

Khi oversubcription hoặc failure layer-3 agent, nó ảnh hướng lớn tới dịch vụ self-service cũng như các instance đang sử dụng chúng. Việc thực hiện one or more high-availability sẽ tăng tính dự phòng và nâng cao hiệu suất của self-service networks

Users có thể create tenant network cho từng project. Mặc định, chúng được cô lập hoàn toàn với các project khác. Openstack networking supports the following types of network isolation and overlay technologies.

Một ví dụ về OpenvSwitch Achitecture Self-service network:

![Imgur](https://i.imgur.com/fGM3Fcl.png)



<a name="2"></a>

**2. Provider network**

Provider network offer layer-2 connectivity to instances với sự support for DHCP and metadata services. Những networks này kết nối, map với existing layer-2 networks trong data center, sử dụng VLAN tagging để identity và cô lập với nhau.


Provider networks mang đến sự đơn giản, hiệu năng với chi phí linh hoạt. Only admin có thể quản lý provider network bởi vì chỉ có admin mưới có thể configuration network infrastructure. provider chỉ support layer-2 connectivity for instances, do đó có sự thiếu hụt tính năng như virtual router hay là floating IP address.


In many cases, khi admin quen với hạ tầng virtual networking dựa trên hạ tầng physical layer-2, layer-3, họ có thể deploy thêm other services trong kiến trúc Openstack networking. Trong provider network còn đặt ra một bài toán là làm sao để có thể `migrate` được service networking từ Compute node tới network node.

Bình thường, Provider networking software components hoạt động tại layer-3, có tá động trực tiếp tới hiệu năng, tính tin cậy của dịch vụ. Để năng cao hiệu năng và tính tin cậy, provider network move layer-3 operations tới hạ tầng physical.


Architecture trong Provider network:


![Imgur](https://i.imgur.com/DDBE2Va.png)



- Mô hình Provider network sử dụng Linux bridge


![Imgur](https://i.imgur.com/8V1g57t.png)



