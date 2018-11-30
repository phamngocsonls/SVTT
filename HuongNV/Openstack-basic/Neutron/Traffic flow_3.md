# Tìm hiểu về traffic flow

## Mục lục
- [1. Provider with Linux bridge](#1)
    - [1.1 North-south](#11)
    - [1.2 East-west for instances on different network](#12)
    - [1.3 East-west for instances on same network](#13)
- [2. Provider with OpenvSwitch](#2)
    - [2.1 North-south](#21)
    - [2.2 East-west for instances on different network](#22)
    - [2.3 East-west for instances on same network](#23)

<a name="11"></a>

## 1.1 North-south

![Imgur](https://i.imgur.com/DeE9RYP.png)

Trên node compute 1:
1. Instance forward gói tin từ tap interface(1) tới provider bridge `qbr`. Gói tin chứa địa chỉ MAC đích 
2. Security group(2) trên provider bridge sẽ quản lý và giám sát các traffic
3. Provider bridge sẽ forward gói tin tới logical VLAN interface
4. Logical VLAn interface forward gói tin tới physical network qua các physical interface
5. Switch(3) xử lý VLAN tag của gói tin khi chuyển từ provider bridge và router(4)
5. Router(4) định tuyến gói tin từ provider bridge đi ra mạng ngoài
6. Switch(3) xử lý VLAN tag của gói tin khi forward từ router(4) ra mgnj ngoài
7. Switch(3) forward gói tin ra mạng ngoài

<a name="12"></a>

## 1.2 East-west for instances on different network

![Imgur](https://i.imgur.com/hmTJXF5.png)

Trên node compute 1:
1. Instance 1 forward gói tin từ tap interface(1) tới provider bridge.
2. Security group trên provider bridge sẽ giám sát và xử lý gói tin
3. Provider bridge forward gói tin tới logical VLAN interface
4. Logical VLAN interface forward gói tin tới physical network infrastructure

Trên hệ thống physical network
1. Switch(3) xử lý gói tin tagging giữa provider network 1 và router(4)
2. Router(4) định tuyến gói tin từ provider network 1 tới provider 2
3. Switch(3) xử lý gói tin tagging giữa router(4) và provider network 2
4. Switch(3) forward gói tin tới compute node 2

Trên node compute 2:
1. Physical provider interface forward gói tin tới logical VLAN interface.
2. Logical VLAN interface forward gói tin tới provider bridge `qbr`
3. Security group(5) trên provider bridge xywr lý các traffic
4. Provider bridge forward gói tin tới tap interface(6) là instance 2

<a name="13"></a>

## 1.3 East-west for instance on same network

![Imgur](https://i.imgur.com/l0REcW4.png)

Các bước trên node compute 1 và compute 2 vẫn thực hiện giống như trường hợp 1.2. Khác nhau ở chỗ trên hệ thống network physical, switch(3) sẽ forward gói tin từ compute node 1 tới node compute 2 mà không cần xử lý qua router.

<a name="2"></a>

# 2. Provider with OpenvSwitch

<a name="21"></a>

## 2.1 North-south

![Imgur](https://i.imgur.com/xBx4U49.png)

Trên node compute 1:
1. Instance 1 gửi gói tin từ tap interface(1) tới Linux bridge `qbr`. 
2. Security group(2) trên Linux bridge xử lý và giám sát gói tin
3. Linux bridge forward gói tin tới integration bridge `br-int`
4. OVS integration bridge add internel tag for provider network
5. OVS `br-int` forward gói tin tới provider OVS `br-provider`
6. OVS provider thay thế internal tag thành actual VLAN
7. OVS provider forward gói tin tới physical netửok

Trên hệ thống physical network:
1. Switch(3) xử lý VLAN tag giữa provider network và router(4)
2. Router(4) định tuyến gói tin từ provider 1 ra mạng ngoài
3. Switch(3) xử lý VLAN tag giữa router(4) và mạng ngoài
4. Switch(3) forward gói tin ra mạng ngoài

<a name="22"></a>

## 2.2 East-west for instances on different network

![Imgur](https://i.imgur.com/RTQ65dc.png)

