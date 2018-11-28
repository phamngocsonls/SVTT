# Tìm hiểu về traffic flow

## Mục lục
- [1. VM access Internet](#1)
- [2. Open vSwitch and Openstack Neutron](#2)   
    - [2.1 Neutron flow tables](#21)
- [3. Network flows](#3)
    - [3.1 Boot VM](#31)
    - [3.2 VM1 access Internet](#32)
    - [3.3 VM1 ping to VM2](#33)
    - [3.4 VM1 ping VM5](#34)
    - [3.5 VM1 ping VM3](#35)

<a name="1"></a>

# 1. VM access Internet
- Step 1: VMM to br-int

![Imgur](https://i.imgur.com/O2JFFUT.png)

Sau khi khởi tạo 1 VM, nó được gắn tới TAP interface(vnetX). Các tap interface này kết nối tới các linux bridge qbrXXX, các qbrXXX này kết nối tới `br-int` thông qua port qv0XXX. Packet từ các VM sẽ được kiểm tra tại mỗi tap interface, sử dụng IPtables.

- Step 2: br-int to br-tun

![Imgur](https://i.imgur.com/69IT8Wv.png)

Br-int kết nối tới br-tun qua path ports. Các gói tin từ bên ngoài được tag VLAN id hay là gơ bỏ đi VLAN tagging sẽ được thực hiện tại br-tun. Tại br-tun sẽ thiết lập tunnel để gửi các packet từ compute node tới network node.

- Step 3: Packet forward to Network node through GRE tunnel

![Imgur](https://i.imgur.com/Z6QbGlC.png)

- Step 4: Packet reaches br-int from br-tun

![Imgur](https://i.imgur.com/w3AB1rZ.png)

eth1 interface được gán trực tiếp tới br-tun. br-tun nhận các packet, nó remove GRE header và forward traffic tới br-int qua path-ports

- Step 5: Firewall rules on network node

![Imgur](https://i.imgur.com/4CKIadY.png)

Packet rời khỏi br-int trên network node qua qrXXX interface và forward tới qgXXX interface. Cả 2 interface này đều thuộc qRouter namespace. Có thể kiểm tra các interface, route và iptables chi tiết như sau:

```
#ip netns exec ifconfig -a
#ip netns exec route -n
#ip netns exec iptables -L
#ip netns exec iptables -L -t nat
```

<a name="2"></a>

# 2. Open vSwitch and Openstack Neutron

![Imgur](https://i.imgur.com/OvgmS2e.png)

<a name="21"></a>

## 2.1 Neutron flow tables
Các flow tables được chia thành các loại như sau:
- table 0: Tất cả các packet được gửi tới table này
- table 1: Chứa thông tin về các packet được gửi từ VM đi ra mạng internet
- table 2: Chứa thông tin về các packet được gửi từ bên ngoài tới VM
- table 3: Không sử dụng
- table 10: Inject a rule into table 20 to cause a return Path, so when VM repond to the Packet it will work.
- table 20: does unicast packet
- table 21: does broadcast packet

<a name="3"></a>

# 3. Network flows in Openstack

Mô hình tham khảo: Gồm 2 compute node kết nối qua switch. Mô hình gồm `tenant 1` và `tenant 2`, 2 tenant thuộc 2 dải private khác nhau và thuộc 2 VLAN khác nhau(VLAN 100, 102)

![Imgur](https://i.imgur.com/SMfcR3h.png)

<a name="31"></a>

## 3.1 Boot VM

Mô hình miêu tả quá trình boot VM và thực hiện request IP address

![Imgur](https://i.imgur.com/t0E1scL.png)

1. VM1 boot và gửi bản tin DHCP DISCOVERY broadcast để yêu cầu cấp phát 1 địa chỉ IP
2. Bản tin được forward tới br100
3. dnsmasq server lắng nghe bản tin gửi từ VM1, trả về bản tin DHCP OFFER kèm theo IP cấp phát cho VM1 là `10.0.0.3` và default gateway là `10.0.0.1`
VM4 cũng thực hiện tương tự.

<a name="32"></a>

## 3.2 VM1 access Internet

![Imgur](https://i.imgur.com/4OE16xy.png)

1. VM1 muốn gửi 1 bản tin ping Google DNS 8.8.8.8
2. VM1 forward ping message tới default gateway là 10.0.0.1
3. Gói tin sẽ được forward tới default gateway của compute node là 91.207.15.105
4. Gói tin đi tới dafault gateway của compute node là `eth1` sẽ được NAT địa chỉ nguồn. Gói tin từ compute đi ra mạng ngoài sẽ có source address là `91.207.15.105`
```
nova-network-snat -s 10.0.0.0/24 -j SNAT --to-source 91.207.15.105
```
5. 8.8.8.8 reply lại bản tin icmp echo từ VM1 tới 91.207.15.105, qua NAT table và được forward trở lại VM1

<a name="33"></a>

## 3.3 VM1 ping to VM2

- 2 VM thuộc cùng tenant 1
- 2 VM thuộc cùng 1 compute node

![Imgur](https://i.imgur.com/WbTYoYJ.png)

1. VM1 muốn gửi 1 packet tới VM2 thuộc cùng subnet. VM1 gửi 1 bản tin ẢP broadcast với mong muốn tìm địa chỉ MAC của VM1
2. Bản tin broadcast được forward tới br100, đi tới tất cả các VM hiện có trong compute node này. VM2 so khớp với địa chỉ IP của nó và reply lại 1 bản tin tới VM1
3. Qúa trình xác định VM2_MAC address hoàn tất, gói tin được gửi thành công

*Lưu ý*: Bản tin ARP broadcast cũng được forward tới VM4  và VM5 thông qua VLAN100 

<a name="34"></a>

## 3.4 VM1 ping VM5 trên 2 node khác nhau

2 VM nằm trên 2 host khác nhau, thuộc cùng tenant 1

![Imgur](https://i.imgur.com/lciOTWd.png)

1. VM1 gửi bản tin ARP broadcast để tìm địa chỉ MAC của VM5
2. Bản tin broadcast được forward tới br100 
3. Bản tin được tagging theo chuẩn 802.1Q
4. Gói tin được tagged đi qua switch và forward tới compute node 2
5. Gói tin tới node compute 2 sẽ được remove tagging id với nhãn 100
6. Gói tin forward tới br100
7. VM5 nhận được bản tin broadcast và reply lại địa chỉ MAC của nó.

<a name="35"></a>

## 3.5 VM1 ping VM3

2 VM thuộc 2 tenant khác nhau và có địa chỉ khác nhau, nằm cùng trên 1 compute node

![Imgur](https://i.imgur.com/8K4XI7O.png)


# Tài liệu tham khảo
- http://maniksidana.blogspot.com/2015/05/journey-of-packet-when-vm-accesses.html
- https://www.mirantis.com/blog/vlanmanager-network-flow-analysis/


