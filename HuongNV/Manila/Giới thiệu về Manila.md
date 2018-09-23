# Tìm hiểu về Manila

## Mục lục

- [1. Giới thiệu về Manila](#1)
    - [1.1 How Manila work](#11)
- [2. Các thành phần trong Manila](#2)
- [3. Key concept](#3)
    - [3.1 Share](#31)
    - [3.2 Share Access Rules](#32)
    - [3.3 Snapshot](#33)
    - [3.4 Share Networks](#34)
    - [3.5 Security Services](#35)
    - [3.6 Storage Pool](#36)


<a name="1"></a>

# 1. Giới thiệu về Manila

The Openstack Shared File Systems service (Manila )là một project về chia sẻ file trong Openstack. Manila ban đầu được hình thành như là một extension cho Block Storage service (Cinder), nhưng giờ nó phát triển thành một project độc lập.

![Imgur](https://i.imgur.com/2Emyfro.png)

Với Shared File Systems service, ta có thể tạo hệ thống tệp từ xa, mount file system vào các instance. Manila có từ bản Kilo được phát hành vào năm 2015. Manila mang đến sự bổ sung các dịch vụ lưu trữ hiện có, mở rộng và cải thiện khả năng tiêu thụ tài nguyên lưu trữ dùng chung bên ngoài.

Ví dụ sau đây miêu tả 2 file share giữa các VM với nhau. `Marketing file` share file giữa VM 6 và 8, còn `R&D file` share giữa VM 1 và 7.

![Imgur](https://i.imgur.com/1W0mccx.png)


<a name="11"></a>

## 1.1 How Manila work

Nhiệm vụ chính của Manila là cho phép Nova compute instances truy cập tới storage dựa trên shared-file, các storage ở đây có thể là các external storage như `Ceph` hoặc `GlusterFS`

Manila cung cấp các components để quản lý việc create of file share và ánh xạ những file-share này tới Nova compute instances. vIệc này thực hiện dễ dàng qua API, command line interface CLI hoặc dashboard horizon.


<a name="2"></a>

# 2. Các thành phần trong Manila

![Imgur](https://i.imgur.com/Zm8jLyT.jpg)


Kiến trúc của Manila service bao gồm các thành các thành phần sau:
- **manila-api** - Tiếp nhận các request từ người dùng, nó sẽ xác thực và định tuyến các request tới hệ thống Shared File Systems service,
- **python-manilaclient** - Giao diện người dùng để cho client thực hiện các command line thao tác Manila thông qua *mania-api*
- **manila-scheduler** - Thực hiện lập lịch/định tuyến các request tới các manila-share service phù hơp. Nó thực hiện được bằng cách lọc dựa trên một số thuộc tính như Capacity, Availability Zone... và chọn ra một back-end phù hợp nhất
- **manila-share** - Thực hiện việc quản lý các thiết bị Shared File Service, cụ thể là các back-end devices
- **Auth Manager** - Thành phần quản lý user, projects và roles
- **SQL database** - Manila sử dụng một sơ sở dữ liệu tập trung sql-based central database để chia sẻ giữa các dịch vụ Manila trong hệ thống.


<a name="3"></a>

# 3. Key concept

<a name="31"></a>

## 3.1 Share 
- User định nghĩa size, access protocol và sharing type
- Multiple instances có thể truy cập file system này

<a name="32"></a>

## 3.2 Share Access Rules
- Thiết lập clients nào có thể truy cập vào `share` file system
- Việc thiết lập này có thể dựa trên IP address

<a name="33"></a>

## 3.3 Snapshot 
- Read-only copy of share contents
- New share can be created from a snapshot

<a name="34"></a>

## 3.4 Share Networks
- Defines the Neutron network & subnet through which instances access the share
- A share can be associated with only one share network

<a name=""35></a>

## 3.5 Security Services
- Định nghĩa, thiết lập rules cho việc xác thực, truy cập vào file share(ví dụ: Có thể khai báo các rules thông qua các external service: LDAP, Active Directory, Kerberos)
- Có thể khai báo Shares với multiple security services

<a name="36"></a>

## 3.6 Storage Pool
Từ bản Kilo trở đi, Shared File Systems có thể sử dụng `storage pool`. Storage pool là một hoặc một nhóm tài nguyên lưu trữ mà dịch vụ Shared File Systems chọn làm lưu trữ khi cấp phép chia sẻ.



