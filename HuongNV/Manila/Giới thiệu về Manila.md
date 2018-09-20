# Tìm hiểu về Manila

## Mục lục

- [1. Giới thiệu về Manila](#1)
- [2. Manila Architecture](#2)


<a name="1"></a>

# 1. Giới thiệu về Manila

The Openstack Shared File Systems service (Manila )là một project về chia sẻ file trong Openstack. Manila ban đầu được hình thành như là một extension cho Block Storage service (Cinder), nhưng giờ nó phát triển thành một project độc lập.

Với Shared File Systems service, ta có thể tạo hệ thống tệp từ xa, mount file system vào các instance hoặc đọc, ghi data từ các instance tới file system
 

<a name="2"></a>

# 2. Manila Architecture

![Imgur](https://i.imgur.com/Zm8jLyT.jpg)


Kiến trúc của Manila service bao gồm các thành các thành phần sau:
- **manila-api** - Tiếp nhận các request từ người dùng, nó sẽ xác thực và định tuyến các request tới hệ thống Shared File Systems service,
- **python-manilaclient** - Giao diện người dùng để cho client thực hiện các command line thao tác Manila thông qua *mania-api*
- **manila-scheduler** - Thực hiện lập lịch/định tuyến các request tới các manila-share service phù hơp. Nó thực hiện được bằng cách lọc dựa trên một số thuộc tính như Capacity, Availability Zone... và chọn ra một back-end phù hợp nhất
- **manila-share** - Thực hiện việc quản lý các thiết bị Shared File Service, cụ thể là các back-end devices
- **Auth Manager** - Thành phần quản lý user, projects và roles
- **SQL database** - Manila sử dụng một sơ sở dữ liệu tập trung sql-based central database để chia sẻ giữa các dịch vụ Manila trong hệ thống.





