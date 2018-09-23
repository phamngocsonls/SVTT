## Mục lục 
- [1. Các kiểu dữ liệu lưu trữ trong cloud computing](#1)
    - [Block device](#block-device)
    - [File](#file)
    - [Object storage](#object-storage)
    - [So Sánh 3 loại dữ liệu](#so-sanh)
- [2. Các kiểu dữ liệu trong ceph storage](#2)
- [3. Ceph-deploy toolkit - Tạo một ceph cluster đơn giản](#3)
    - [3.1 Cấu hình tất cả các node](#3.1)
    - [3.2 Cấu hình ssh server](#3.2)
    - [3.3 Cấu hình ceph storage cluster](#3.3)

## Nội dung

## 1. Các kiểu dữ liệu lưu trữ trong cloud computing

<a name="block-device"></a>

### Block device

Block storage device lưu trữ dữ liệu bằng cách chia dữ liệu thành các khối nhỏ có kích thước bằng nhau. Hệ thống lưu trữ có thể thực hiện việc này mà không cần cấu trúc tệp vì mỗi khối dữ liệu có một địa chỉ duy nhất. Điều này cho phép hệ thống lưu trữ phân tán các khối dữ liệu nhỏ hơn ở bất cứ nơi nào trong hệ thống mà nó thấy hiệu quả nhất. Phần mềm hệ thống lưu trữ tập hợp các khối cần thiết lại với nhua để tạo thành tệp bất cứ khi nào tệp được truy cập. Tạo nên hiệu suất lưu trữ cao.

<a name="file"></a>

### File

File storage lưu trữ dữ liệu như một phần thông tin đơn lẻ bên trong một thư mục giúp sắp xếp dữ liệu đó với các dữ liệu khác. Phương pháp này còn gọi là lưu trữ phân cấp theo kiến trúc thứ bậc hay cây thư mục-mô phỏng cách mà chúng ta vẫn lưu trữ các tệp giấy tờ. khi cần truy cập dữ liệu hệ thống máy tính chỉ cần xác định đường dẫn để  vào nơi lưu dữ liệu.

<a name="object-storage"></a>

### Object storage

Object storage lưu trữ dữ liệu dưới dạng object. Các đối tượng được lưu trữ trong một kho. Lưu trữ đói tượng sử dụng các khung logic để chứa đối tượng theo cơ chế ngang hàng. Mỗi object sẽ bao gồm dữ liệu của chính nó; metadata chứa thông tin của dữ liệu, bảo mật... và có thể mở rộng được, id global định danh duy nhất điều này làm cho nó có khả năng tìm dữ liệu mà không cần biết vị trí lưu trữ vật lý của dữ liệu.

Dữ liệu trong object storage thường được truy cập thông qua các giao thức Internet (http) bằng trình duyệt hoặc trực tiếp qua API như REST (representational state transfer). Các phần mềm này sử dụng định danh duy nhất được gán cho đối tượng để quy chiếu, xác đinh, và tìm bất kỳ đối tượng cụ thể nào, như 1 video hoặc hình ảnh chẳng hạn.

<a name="so-sanh"></a>

### So sánh 3 loại dữ liệu lưu trữ

|So sánh        | File storage          | Block storage       | Object storage        |
|---------------|:---------------------:|:-------------------:|:----------------------|
|Kiến trúc và   | Lưu trữ file          |  Lưu trữ block      | Lưu trữ hướng đối     |
|đơn vị lưu trữ | (files)               | (blocks)            | tượng                 |
|-------------------------------------------------------------------------------------|
|Cập nhật sửa   | hỗ trợ cập nhật tại   | Hỗ trợ cập nhật tại | Không hõ trợ cập nhât |
|đổi            | chỗ và sửa đổi 1 phần | và sửa đổi 1 phần   | tại chỗ và sửa đổi    |
|               | dữ liệu               | dữ liệu             | toàn phần dữ liệu     |
|-------------------------------------------------------------------------------------|
|Phù hợp nhất   | Chia sẻ dữ liệu       | Dữ liệu thường giao | Dữ liệu tập trung và  |
|cho            |                       | dịch và thay đổi    | unstructure.          |
|               |                       | (databases)         |                       |
|-------------------------------------------------------------------------------------|
|Lợi thế nổi    | Đơn giản hóa truy cập | Hiệu năng cao       | Khả năng mở rộng và   |
|bật            | và quản lý chia sẻ    |                     | và truy cập phân tán  |
|               | files                 |                     |                       |
|-------------------------------------------------------------------------------------|
|Tốc độ xử lý   | Trở nên nặng nề khi   | Phân mảnh dữ liệu,  | Truy xuất đến thẳng vị|
|               | số lượng file lên đến | không thể truy xuất | trí lưu trữ, tốc độ   |
|               | hàng tỷ               | 1 file nhanh chóng  | nhanh                 |
|-------------------------------------------------------------------------------------|
|Use case       | Nhu cầu chia sẻ dữ    | Databases cho các   | Big data              |
|               | liệu lớn, lưu trữ cục | ứng dụng, web.      | web apps,             |
|               | bộ                    | Virtual machine     | lưu trữ sao lưu       |
|               |                       | ramdom read/write   |                       |

<a name="2"></a>

## 2. Các kiểu dữ liệu trong Ceph storage:

Ceph storage cung cấp 3 lọai dữ liệu là files (CephFS), block (RBD), Object và chúng được lưu dưới dạng object tại các Object storage device (OSD) thông qua thư viện librados.

<a name="3"></a>

## 3. Ceph-deploy toolkit - Tạo một Ceph cluster đơn giản.

Ceph storage cluster bao gồm:
- 1 admin node
- 1 monitor
- 3 osd

Các node là các máy ảo chạy Centos 7 và linux kernel 3.10. VirtualBox version 5.2

<a name="3.1"></a>

### 3.1 Cấu hình chung cho tất cả các node

Chuyển hostname và sửa file /etc/hosts

![](w4-cài-hostname.png))

Cấu hình mạng cho máy ảo tại file /etc/sysconfig/network-scripts/ifcfg-emp0s3

![](w4-cấu-hình-mạng-cho-vm.png)

Sau khi cấu hình xong restart lại network service và reboot

```
systemctl restart network.service
reboot
```

Cấu hình cho user ceph có đặc quyền sudo mà không cần nhập mật khẩu:

```
echo "ceph ALL = (root) NOPASSWD:ALL" | tee /etc/sudoers.d/ceph
chmod 0440 /etc/sudoers.d/ceph
visudo
```

tại Defaults thêm vào Defaults:ceph !requiretty và lưu lại

### Cài đặt và cấu hình NTP (Network Time Protocol)

Cài đặt NTP để đồng bộ ngày và giờ trên tất cả các node

```
yum install -y ntp ntpdate ntp-doc
ntpdate 0.us.pool.ntp.org
hwclock --systohc
systemctl enable ntpd.service
systemctl start ntpd.service 
```

### Disable SELinux

Trên Centos SELinux là một tập bắt buộc thi hành theo mặc định. Vì vậy để có thể thi hành theo các cài đặt thì phải disable SELinux

```
sudo setenforce 0
```

file cấu hình /etc/selinux/config

**Cài đặt thêm epel và pip cho centos**

```
sudo yum install epel-release
sudo yum install python-pip
```

<a name="3.2"></a>

### 3.2 Cấu hình ssh server

Login vào admin node với user ceph

Generate ssh key cho ceph user

```
ssh-keygen
```

![](w4-ssh-keygen.png)

Tạo file cấu hình cho ssh vào file có đường dẫn /home/ceph/.ssh/config và thêm vào nội dung sau:

```
Host admin1
Hostname admin1
User ceph
Host node1
Hostname node1
User ceph
Host node2
Hostname node2
User ceph
Host node3
Hostname node3
User ceph
Host node4
Hostname node4
User ceph
```

và chuyển permission thành 644

```
chmod 644 /home/ceph/.ssh/config
```

Sau đó thêm tất cả key vào các node còn lại bằng câu lệnh ssh-copy-id

```
ssh-keyscan admin1 node1 node2 node3 node4 >> /home/ceph/.ssh/known_hosts
ssh-copy-id admin1
ssh-copy-id node1
ssh-copy-id node2
ssh-copy-id node3
ssh-copy-id node4
```

### Cài đặt tường lửa:

Sử dụng tường lửa để bảo vệ hệ thống. bật tường lửa ở tất cả các node và mở các port cần thiết cho admin, monintor và osd.

Vào admin node:

```
ssh root@node1
systemctl start firewalld
systemctl enable firewalld
# mở các port 80, 203, 4505-4506 và reload lại tường lửa.
sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
sudo firewall-cmd --zone=public --add-port=2003/tcp --permanent
sudo firewall-cmd --zone=public --add-port=4505-4506/tcp --permanent
sudo firewall-cmd --reload
```

Từ admin node login vào node1 (monitor) và bật firewall

```
ssh node1
sudo systemctl start firewalld
sudo systemctl enable firewalld
# mở port mới cho monitor và reload
sudo firewall-cmd --zone=public --add-port=6789/tcp --permanent
sudo firewall-cmd --reload
```

Cuối cùng mở cổng còn lại trên các node2 node3 node4:

```
ssh node2 # node3, node4
sudo systemctl start firewalld
sudo systemctl enable firewalld

sudo firewall-cmd --zone=public --add-port=6800-7300/tcp --permanent
sudo firewall-cmd --reload
```

<a name="3.3"></a>

### 3.3 Cấu hình các node osd

Tạo thư mục my-cluster và vào trong thư mục. Tạo mới một cấu hình cluster tại monitor node "node1"

```
ceph-deploy new  node1
```

![](w4-ceph-deploy-new.png)

sửa file cấu hình ceph.conf

```
osd pool default size = 2
```

Add the initial monitor and gather the keys:

```
ceph-deploy mon create-initial
```

Em đang gặp lỗi này

![](loi.png)

Cài lại không bật tường lửa và các port thì gặp lỗi 

![](loi2.png)