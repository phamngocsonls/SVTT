# Tìm hiểu về traffic flow của VM

- [1. Traffic flow with LinuxBridge](#1)
    - [1.1 VLAN](#11)
    - [1.2 Flat](#12)
    - [1.3 VXLAN](#13)
    - [1.4 Local](#14)
- [2. Traffic flow with OpenvSwitch](#2)
    - [2.1 Port trên OVS](#21)
    - [2.2 Flow rules trên OVS](#22)
        - [2.2.1 Flow rules cho VLANs](#221)
        - [2.2.2 Flow rules cho Flat networks](#222)
        - [2.2.3 Flow rules cho Local network](#223)

Một gói tin Ethernet frame xuất phát từ VM đi ra mạng ngoài phải đi qua 3 trong 4 devices phụ thuộc vào từng mô hình network như sau:
- Tap interface: `tapN`
- Linux bridge: `brqXXX`
- VXLAN interface: `vxlan-Z`, z là VNI_VXLAN Network Identifier
- VLAN interface: `ethX.Y`, X là tên của interface, Y là VLAN ID
- physical interface: `ethX`, X là tên của interface

<a name="1"></a>

# 1. Traffic flow with Linux bridge

<a name="11">

## 1.1 VLAN

Mô hình sau lấy ví dụ VLAN100 được sử dụng để trung chuyển lưu lượng cho các VM.

![Imgur](https://i.imgur.com/AKOb6Lb.jpg)

Mô hình có 3 VM được kết nối tới Linux bridge brqXXX qua các tap interface. Lưu lượng của các VM được forward tới bridge này được tagging với ID là 100 và forward tới interface `eth1.100`, đi tới interface `eth1` và đi ra mạng ngoài. 

Sử dụng command line sau để kiểm tra các interface có trên qbrXXX

![Imgur](https://i.imgur.com/WZRyMbi.jpg)

Trong trường hợp lưu lượng được tagging với nhiều VLAN khác nhau, sẽ cần nhiều hơn linux bridge để có thể cô lập lưu lượng giữa các VLAN với nhau. Trong trường hợp dưới đây có thêm lưu lượng ứng với VLAN 101, interface `eth1.101` được kết nối tới `brqYYY`

![Imgur](https://i.imgur.com/LdU0XUM.jpg)

Kiểm tra các interface trên bridge sử dụng

![Imgur](https://i.imgur.com/S7Yk3WA.jpg)

<a name="12"></a>

## 1.2 Flat

Flat network không giống như VLAN network. Lưu lượng sẽ không phải tagging để cô lập lưu lượng. Mỗi linux bridge sẽ cần 1 physical interface gán trực tiếp vào đó, có nghĩa là nếu có 2 bridge thì sẽ cần 2 flat network gán trực tiếp vào đó chứ. 

![Imgur](https://i.imgur.com/A49zmSH.jpg)

Mô hình trên mô tả interface `eth1` được gán trực tiếp tới `brqXXX`, kèm theo 3 tap interface trên bridge ứng với VM.

Kiểm tra các interface trên bridge sử dụng

![Imgur](https://i.imgur.com/v8FGU7v.jpg)

Trong trường hợp có nhiều hơn 1 flat network, sẽ gán trực tiếp mỗi physical interface ứng với mỗi linux bridge

![Imgur](https://i.imgur.com/ipkJW24.jpg)

<a name="13"></a>

## 1.3 VXLAN

VXLAN là công nghệ overlay qua lớp mạng. Overlay Network có thể được định nghĩa như là một mạng logic mà được tạo trên một nền tảng mạng vật lý đã có sẵn. VXLAN tạo một mạng vật lý layer 2 trên lớp mạng IP. Dưới đây là 2 từ khóa được dùng trong công nghệ overlay network:
- **Encapsulation**: Đóng gói những gói tin internet thông thường trong một header mới. Ví dụ trong công nghệ overlay IPsec VPN, đóng gói gói tin thông thường vào một IP header khác.
- **VTEP**: Việc liên lạc được thiết lập giữa hai đầu ống tunnel end points

Khi áp dụng vào với công nghệ overlay trong VXLAN, ta sẽ thấy VXLAN đóng gói một frame MAC thông thường vào một UDP header. Và tất cả các host tham gia vào VXLAN thì hoạt động như một tunnel end points. Người ta gọi đó là Virtual Tunnel Endpoints (VTEPs)

![Imgur](https://i.imgur.com/ZIKdErM.png)

VXLAN học tất cả địa chỉ MAC của máy ảo và việc kết nối nó tới VTEP IP thì được thực hiện thông qua sự hỗ trợ của mạng vật lý. Một trong những giao thức được sử dụng trong mạng vật lý là Ip multicast. VXLAN sử dụng giao thức của IP multicast để cư trú trong bảng forwarding trong VTEP.

<a name="14"></a>

## 1.4 Local

Local network là dạng mạng cục bộ, không có physical interface được vào bridge cũng như không có sự cô lập về VLAN ID gì trong đó. Các VM được gán tới cùng 1 bridge thì có thể liên lạc được với nhau do cùng thuộc một local network, giữa các VM nằm trên những bridge khác nhau thì không thể giao tiếp được với nhau.

![Imgur](https://i.imgur.com/8dGVkAg.jpg)

<a name="2"></a>

# 2. Traffic flow with OpenvSwitch

Khi sử dụng OpenvSwitch, các gói tin Internet frame xuất phát từ VM phải đi qua các interface như:
- tap interface: `tapXXX`
- Linux bridge: `qbrXXX`
- veth pair(virtual eth): `qvbXXXX`, `qv0XXXX`
- OVS integration bridge: `br-int`
- OVS patch ports: `int-br-ethX`, `phy-br-ethX`
- OVS provider bridge: `br-ethX`
- physical interface: `ethX`
- OVS tunnel bridge: `br-tun`

`br-int` là integration bridge. Là bridge kết nối tới hầu hết các virtual device như instances, DHCP servers, routers.

`br-ethX` được biết đến là provider bridge. Bridge này kết nối trực tiếp tới physical interface. Provider bridge kết nối tới integration bridge thông qua virtual patch là `int-br-ethX` và `phy-br-ethX`. 

Mô hình sử dụng OVS được thể hiện qua hình sau:

![Imgur](https://i.imgur.com/vpUm4RX.jpg)

Các instances kết nối tới Linux bridge thông qua các tap interface. Linux bridge kết nối tới OVS integration bridge thông qua veth cable. OpenFlow rules trên mỗi OVS integration bridge sẽ hướng kết nối cho các traffic đi như thế nào. Các integration kết nối tới provider bridge sử dụng OVS patch cable. Provider sẽ kết nối trực tiếp tới physical interface và cho phép lưu lượng đi ra mạng ngoài.

Khi sử dụng OVS driver, mỗi network và compute node đều cần các integration, provider và tunnel bridge khác nhau. Nếu có nhiều hơn một provider bridge được cấu hình trên host, sẽ cần các interface physical riêng rẽ trên từng provider bridge đó.

<a name="21"></a>

## 2.1 Nhận biết ports trên OVS bridge
Sử dụng `ovs-ofctl show <bridge_name>` để xem các thông tin về các ports được gán trên từng OVS cụ thể. Ví dụ sau minh họa integration ports trên node compute1:

![Imgur](https://i.imgur.com/q8PCXKe.jpg)

- port 6: Lầ `int-br-eth2`, là một đầu port nối từ integration tới provider bridge.
- port 7: Có tên là `patch-tun`, là một đầu nối sử dụng patch cable. Đầu còn lại nối tới tunnel bridge.
- port 8: Có tên là `qvo7140bc00-75`, là port nằm trên OVS integration bridge, port còn lại kết nối tới linux bridge
- port 9: Giống như port 8
- LOCAL port: Có tên là `br-int`, được sử dụng để quản lý các traffic từ các virtual switch.

Hình vẽ sau mô tả quá trình tagging, untagging traffic khi đi qua OVS integration

![Imgur](https://i.imgur.com/7thVTZb.jpg)

Mỗi port kết nối tới integration bridge đều được đặt trong 1 VLAN khác nhau. Sử dụng `ovs-vsctl show` để kiểm tra tagging trên các ports

![Imgur](https://i.imgur.com/B35yVok.jpg)

Hai port `qvo7140bc00-75` và `qvo017db302-dc` được tagging với id là 1 và 2

<a name="22"></a>

## 2.2 Flow rules trên OVS

Không giống như Linux bridge, OVS không sử dụng giao diện VLAN trên máy chủ để tagging traffic. Thay cào đó, các quy tắc mở trên mỗi OVS quyết định cách chuyển đổi lưu lượng trước khi nó được forrward đi. Khi traffic tới các switch ảo, flow rules trên đó sẽ thực hiện add hoặc remove VLAN tags các traffic đó trước khi forwarding. Flow rules có thể drop traffic.

Sử dụng `ovs-ofctl dump-flows <bridge_name>` để hiểu rõ hơn về thông tin của các traffic khi đi qua OVS.

<a name="221"></a>

### 2.2.1 Flow rules cho VLAN

Ví dụ dưới đây minh họa 2 VLAN có ID là 30 và 33. Traffic được tags với ID của 2 VLAN được floww rules trên `br-eth2` xử lý và chuyển tiếp.

![Imgur](https://i.imgur.com/VU8PF3R.jpg)

Flow rules xử lý traffic theo độ ưu tiên priority, từ cao nhất tới thấp nhât. Mặc định `ovs-ofctl` trả về các traffic theo thứ tự mà các gói tin đi tới switch đó. Sử dụng `--rsort` để trả về kết quả có độ ưu tiên từ cao nhất tới thấp nhất.

![Imgur](https://i.imgur.com/W70fdaK.jpg)

Traffic đi tới `br-eth2` bridge từ physical interface qua `port1`. Traffic sẽ được forward tới integration bridge. Oử hình minh họa dưới đây rule thứ 4 thể hiện forward traffic từ provider bridge tới integration bridge, 3 rule đầu tiên không sử dụng trong quá trình này. 

![Imgur](https://i.imgur.com/T06sMBx.jpg)

Flow với action `NORMAL` thể hiện rằng OVS học, forward và update FDB table. Các traffic được forward tới integration bridge. 

**Note*: FDB table tương đương với CAM và MACC address table.

Traffic từ `port4` trên `br-eth2` tới `port6` trên `br-int`, các rules trong integration bridge này như sau.

![Imgur](https://i.imgur.com/IwcluGF.jpg)

Trên bridge này, flow rules thể hiện quá trình chuyển đổi VLAN tags từ ID 30 thành ID 1, traffic này được gửi tới VM đích với tags ID là 1.

![Imgur](https://i.imgur.com/2AM2PxP.jpg)

Rule thứ 2 thực hiện chức năng tương tự khi chuyển đỏi tagging traffic ID từ 33 thành 2. Nếu rule thứ 3 khớp, có nghĩa là không có rule nào khác có độ ưu tiên cao hơn phù hợp với traffic đi tới cổng 6, lưu lượng sẽ bị `drop`. 

![Imgur](https://i.imgur.com/2hhLAUo.jpg)

Traffic từ instance được gửi tới integration bridge `br-int` và forward tới provider bridge

![Imgur](https://i.imgur.com/UIVsx20.jpg)

Traffic trên provider bridge sẽ được thực hiện ngược lại so với integration bridge. Traffic sẽ được chuyển đổi tagggin từ ID 30, 33 thành VLAN ID 1, 2. Các traffic khác đi tới provider bridge không được tagging với ID là 20 và 33 sẽ bị `drop`.

![Imgur](https://i.imgur.com/3GZWROJ.jpg)

<a name="222"></a>

### 2.2.2 Flow rules cho Flat networks

Flat networks trong Neutron là các mạng untagged, nghĩa là không có sử dụng VLAN tag 802.1q trong đó. Một sự khác biệt rõ ràng nhất kể đến là các traffic từ integration bridge tới provider bridge và ngược lại. Thay vì ánh xạ VLAN cục bộ trên integration bridge thành VLAN ID vật lý trên provider bridge thì VLAN cục bộ sẽ được thêm vào hoặc tước bỏ khỏi tiêu đề Ethernet bằng các flow rules trên mỗi OVS.

Ví dụ sau mô tả một flat network không có VLAN trong Neutron

![Imgur](https://i.imgur.com/1VARL8V.jpg)

Traffic đi tới integration bridge br-int được gán VLAN ID là 3 mặc dù đang sử dụng flat network. Trên mỗi integration bridge, đều có action là modify VLAN header của các gói tin đi tới nó nếu không có VLAN ID được set trên mỗi gói tin.

![Imgur](https://i.imgur.com/piBCH30.jpg)

Traffic từ instsance đi ra mạng ngoài tới provider bridge `br-eth2` sẽ bóc tách đi VLAN ID trên đó và forward ra mạng ngoài.

![Imgur](https://i.imgur.com/AxWQGU6.jpg)

# Tài liệu tham khảo
- https://www.safaribooksonline.com/library/view/learning-openstack-networking/9781785287725/ch04s06.html

