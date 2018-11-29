# Tìm hiểu về traffic flow của VM

- [1. Traffic flow with LinuxBridge](#1)
    - [1.1 VLAN](#11)
    - [1.2 Flat](#12)
    - [1.3 VXLAN](#13)
    - [1.4 Local](#14)
- [2. Traffic flow with OpenvSwitch](#2)

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

