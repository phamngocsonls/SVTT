# Báo Cáo Thực Tập 
* Tìm hiểu về KVM Hypervisor 
* Người thực hiện: Nguyễn Xuân Lưu
* Ngày báo cáo 03/09/2018
* Tuần: 1
* ID: LuuNX_KVM_01 

## Cài Đặt Môi Trường
### 1. Hệ Điều Hành Ubuntu 16.04 LTS

Trong dự án này, chúng ta sử dụng hệ điều hành Ubuntu 16.04 LTS.

![Imgur](https://i.imgur.com/uQZ6J5O.png)

### 2. Phần mềm Eclipse for C/C++ Developers
Để nghiên cứu về KVM hypervisor, chúng ta sử dụng IDE Eclipse để phân tích cấu trúc mã nguồn của KVM hypervisor. 

![Imgur](https://i.imgur.com/eBdWdpU.png)

### 3. Phần mềm gedit và nano
gedit và nano là hai phần mềm mặc định trong Ubuntu 16.04 . Ta sử dụng hai công cụ này để xem, chỉnh sửa và cấu hình các file mã nguồn, file hệ thống. Ngoài ra, sử dụng gedit để tạo báo cáo định dạng file markdown.

![Imgur](https://i.imgur.com/mIBmKZx.png)

![Imgur](https://i.imgur.com/Rbz1bEZ.png)

### 4. Phần mềm git
Để tải xuống mã nguồn các gói mã nguồn của KVM hypervisor, ta sử dụng công cụ git.
Cài đặt
Trên màn hình terminal, sử dụng lệnh cài đặt git
```shell
sudo apt-get install git
```
Sau khi quá trình cài đặt hoàn tất, tiến hành cấu hình cho git trên terminal bằng lệnh
```shell
git config --global user.name "<Tên người dùng>"
git config --global user.email "<Địa chỉ mail>"
```

### 5. Phần mềm Microsoft Visio
Để tiến hành vẽ các sơ đồ, đồ thị trong việc phân tích cấu trúc của KVM hypervisor, ta sử dụng công cụ là phần mềm Microsoft Visio.

![MSV](https://i.imgur.com/2FnSqT4.png)

## Mã nguồn KVM hypervisor
Dựa trên bản hướng dẫn của anh Dũng qua telegram, có địa chỉ tại:

*https://taiosolve.xyz/installing-kvm-ubuntu-16-04-lts-headless-server/*

Tiến hành tải về mã nguồn cài đặt. Trên màn hình terminal, lần lượt dùng các lệnh
```shell
sudo apt-get source qemu-kvm
sudo apt-get source libvirt-bin
sudo apt-get source virtinst
sudo apt-get source cpu-checker
sudo apt-get source bridge-utils
```
Mã nguồn các gói sẽ được tải xuống.

### 1. qemu-kvm
* Số file: 4419
* Kích thước gói (chưa nén) : 49,274,918 Bytes
### 2. libvirt-bin
* Số file: 8777
* Kích thước gói (chưa nén) : 150,834,551 Bytes
### 3. virtinst
* Số file: 603
* Kích thước gói (chưa nén) : 13,107,217 Bytes
### 4. cpu-checker
* Số file: 7300
* Kích thước gói(chưa nén) : 9,378,199 Bytes
### 5. bridge-utils
* Số file: 41
* Kích thước gói (chưa nén) : 104,361 Bytes

## Biên dịch và cài đặt các gói

### 1. qemu-kvm
Trong thư mục source code qemu-kvm, mở terminal, lần lượt gõ các lệnh sau để compile và install
```shell
mkdir build
cd build
..\configure
make
sudo make install
```

![Imgur](https://i.imgur.com/iGOit7F.png)


### 2. libvirt-bin
Để cài libvirt-bin, ta cần cài bổ sung một vài gói hỗ trợ bao gồm: libxml2, yail, libdevmapper-dev, libpciaccess-dev, libnl-3-dev,libnl-route-3-dev.

Trong thư mục source code libvirt-bin, mở terminal, lần lượt gõ các lệnh sau để compile và install
```shell
sudo apt-get install libxml2
sudo apt-get install cmake
git clone git://github.com/lloyd/yajl
cd yajl
./configure
make
sudo make install
cd ..
sudo apt-get install libpciaccess-dev
sudo apt-get install libnl-3-dev
sudo apt-get install libnl-route-3-dev
.\configure
make
sudo make install
```

![Imgur](https://i.imgur.com/4URsjYO.png)


### 3. virtinst
Trong thư mục source code virtinst, mở terminal, lần lượt gõ các lệnh sau để compile và install
```shell
sudo python setup.py install
```

![Imgur](https://i.imgur.com/wcEPlqs.png)

### 4. bridge-utils
Trong thư mục source code bridge-utils, mở terminal, lần lượt gõ các lệnh sau để compile và install
```shell
autoconf
.\configure
make
sudo make install
```

![Imgur](https://i.imgur.com/OxB61ET.png)

### 5. libvirt-bin
Trong thư mục source code libvirt-bin, mở terminal, lần lượt gõ các lệnh sau để compile và install
```shell
make
sudo make install
```

![Imgur](https://i.imgur.com/PABBrnS.png)
