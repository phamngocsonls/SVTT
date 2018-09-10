# Hướng dẫn cài Devstack


## Giới thiệu

- Devstack là 1 extensible scripts dùng để triển khai một hệ thống Openstack một cách đơn giản và nhanh chóng, các service thường được cài đặt AIO(All in one) 
- Devstack là môi trường lý tưởng cho việc testing và deploy các chức năng cho hệ thống Openstack

## Yêu cầu tối thiểu

Hướng dẫn này cài trên VmWare, cấu hình máy ảo của bản thân như sau:

- RAM: 4GB
- Hard Disk: 60GB
- Network: IP address: `172.16.69.131` chế độ NAT
.- Cài trên ubuntu server 16.04


## Cài đặt

Đăng nhập bằng tài khoản root và thực hiện update hệ thống

```
apt-get update -y && apt-get upgrade -y && apt-get disk-upgrade -y && init 6
```

### Add Stack User

- Devstack nên được chạy với 1 user khác root, ta sẽ add thêm user với name là `stack`

```
sudo useradd -s /bin/bash -d /opt/stack -m stack
apt-get -y install sudo
apt-get -y install git
```

- `stack` user thao tác nhiều với hệ thống nên ta thiết lập cấu hình để không cần nhập password root khi chạy lệnh sudo

```
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
sudo su - stack
```

`sudo su - stack`: chuyển sang user stack

- Tại đây, ta tạo một thư mục mới `cd /opt/stack`

- Tiến hành tải Devstack về

```
git clone https://git.openstack.org/openstack-dev/devstack
cd devstack
```

- Tại thư mục `devstack`, tạo file `local.conf` để cấu hình các dịch vụ sẽ cài trong devstack
- Sau đây là nội dung của file local.conf mà bản thân đã sử dụng

```
[[local|localrc]]
DEST=/opt/stack

# Khai bao log cho devstack
LOGFILE=$DEST/logs/stack.sh.log
VERBOSE=True
SCREEN_LOGDIR=$DEST/logs/screen
OFFLINE=False

# Khai bao IP cua may cai dat devstack
HOST_IP=172.16.69.131

# Khai bao mat khau cho cac dich vu
ADMIN_PASSWORD=123test
MYSQL_PASSWORD=123test
RABBIT_PASSWORD=123test
SERVICE_PASSWORD=123test
SERVICE_TOKEN=123test


disable_service n-net
enable_service q-svc
enable_service q-agt
enable_service q-dhcp
enable_service q-meta
enable_service q-l3

#ml2
Q_PLUGIN=ml2
Q_AGENT=openvswitch

# vxlan
Q_ML2_TENANT_NETWORK_TYPE=vxlan

# Networking
FLOATING_RANGE=172.16.69.0/24
Q_FLOATING_ALLOCATION_POOL=start=172.16.69.150,end=172.16.69.200
PUBLIC_NETWORK_GATEWAY=172.16.69.1

FIXED_RANGE=10.20.20.0/24
NETWORK_GATEWAY=10.20.20.1

PUBLIC_INTERFACE=ens3

Q_USE_PROVIDERNET_FOR_PUBLIC=True
Q_L3_ENABLED=True
Q_USE_SECGROUP=True
OVS_PHYSICAL_BRIDGE=br-ex
PUBLIC_BRIDGE=br-ex
OVS_BRIDGE_MAPPINGS=public:br-ex

disable_service tempest
```

- Bước cuối cung, ta thực thi scripts

```
./stack.sh
```

Qúa trình cài nhanh hay chậm, phụ thuộc vào tốc độ internet của bạn


Sau khi thực thi scripts xong, ta truy cập Dashboard

![Imgur](https://i.imgur.com/n0xSWqB.png)

