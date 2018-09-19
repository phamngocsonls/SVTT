# Tìm hiểu KVM
* Tuần 4
* Người tạo: Nguyễn Xuân Lưu

# Hướng Dẫn Sử Dụng KVM

KVM có nhiều hơn một cách quản trị, cụ thể người sử dụng có thể sử dụng các công cụ khác nhau để quản trị KVM

<img>

Có hai phương pháp chính. Thứ nhất là dùng nhóm công cụ do QEMU cung cấp. Ưu điểm là không cần công cụ trung gian, tốc độ thực hiện nhanh. Tuy nhiên, độ phức tạp cao và cần dùng những lệnh dài. Thứ hai là sử dụng một công cụ trung gian là libvirt. Libvirt hỗ trợ nhiều dòng hypervisor khác nhau quản trị máy ảo như KVM, Xen,... Libvirt bao gồm một nhóm các công cụ quản trị máy ảo. Trong số đó, hai công cụ cần tập chung quan tâm là virsh và virt-manager. virsh (virtual shell) là công cụ command line interface (CLI) và virt-manager là công cụ graphic user interface (GUI) hỗ trợ việc quản lý máy ảo một cách đơn giản và thao tác dễ dàng. Trong khuôn khổ tìm hiểu, ta sẽ đi từ công cụ đơn giản tới phức tạp cho từng loại tác vụ cơ bản.

## 1. Cài Đặt KVM

Trước hết là công việc cài đặt KVM, công việc cài đặt KVM thực hiện theo trình tự sau:

**Kiểm Tra sự hỗ trợ KVM từ phần cứng**

Trong màn hình Terminal, gõ lệnh kiểm tra:
```shell
grep --color -Ew 'vmx|svm' /proc/cpuinfo
```
Nếu xuất hiện cờ trạng thái vmx hoặc svm thì CPU hỗ trợ công nghệ ảo hóa để chạy được KVM.

**Kiểm Tra KVM module**

Như chúng ta đã tìm hiểu, KVM bao gồm phần nhân kvm.ko được hỗ trợ sẵn trong linux kernel. Để khởi chạy kvm.ko và kiểm tra ta sử dụng lần lượt các lệnh:
```shell
modprobe kvm
lsmod | grep kvm
```
Nếu kết quả trả về xuất hiện module kvm thì chứng tỏ kvm module đã hoạt động. Ví dụ:
```shell
kvm_intel             212992  0
kvm                   598016  1 kvm_intel
irqbypass              16384  1 kvm
```
**Cài Đặt các gói**

Các gói cần thiết cài đặt bao gồm:

* qemu-kvm : Gói qemu tùy biến hỗ trợ kvm
* libvirt-bin : Gói libvirt để hỗ trợ quản trị máy ảo
* virtinst : Một tool trong libvirt để hỗ trợ cài đặt máy ảo
* virt-manager : Một tool trong libvirt để hỗ trợ quản lý máy ảo
* bridge-utils : Một tool dùng để cấu hình mạng cho máy ảo

Lệnh cài đặt trong Ubuntu
```shell
sudo apt-get install qemu-kvm libvirt-bin virtinst virt-manager bridge-utils
```
Lệnh này yêu cầu nhập mật khẩu để thực thi.

<virt-host-validate kvm master tr 71>

## 2. Quản Lý KVM bằng libvirt virt-manager

Như đã trình bày từ trước, việc quản lý KVM được thực hiện một cách đơn giản và trực quan nhất thông qua virt-manager. virt-manager cung cấp giao diện cửa sổ người dùng thân thiện. Sau khi cài đặt thành công các gói như trình bày ở phần trên, ta khởi chạy virt-manager bằng cách gõ trong màn hình terminal lệnh

```shell
virt-manager
```
Màn hình khởi động của virt-manager có dạng:

![.](src-image/w4_1.png)

### 2.1. Cài đặt máy ảo

Từ màn hình chính của virt-manager, chọn Create a new virtual machine

![.](src-image/w4_2.png)

Một cửa sổ mới hiện ra cho phép lựa chọn các phương pháp cài đặt máy ảo khác nhau

![.](src-image/w4_3.png)

**Local install media (ISO Image or CDROM)**

Phương pháp cài đặt đầu tiên là thông qua file cài đặt. Chọn Local install media và click forward.

![.](src-image/w4_4.png)

Tại đây ta sẽ lựa chọn file iso hoặc ổ đĩa CD chứa bản cài hệ điều hành. Lưu ý, nếu lựa chọn cài hệ điều hành cho máy ảo từ file iso tải xuống trong ổ cứng. Khi chọn Browse.., ở màn hình bên dưới cần chọn Browse Local để tìm đến file iso trong ổ cứng.

![.](src-image/w4_5.png)

File ISO cho các hệ điều hành mã nguồn mở phổ biến có thể tải từ các nguồn:

Official Ubuntu images: https://www.ubuntu.com/download/alternative-downloads

Official CentOS images: https://centos.org/download/

Official Debian images: https://www.debian.org/CD/

Official Fedora images: https://getfedora.org/

Official openSUSE images: https://software.opensuse.org/

Sau khi lựa chọn file iso thành công, virt-manager sẽ tự động phát hiện hệ điều hành, công việc tiếp theo là ấn forward để chuyển sang màn hình cài đặt CPU và RAM. Việc lựa chọn kích thước RAM ảo và số lượng CPU ảo phải dựa vào yêu cầu sử dụng và tài nguyên sẵn có của hệ thống.

![.](src-image/w4_6.png)

Sau khi cài đặt CPU và RAM, ấn forward sẽ chuyển sang màn hình cài đặt kích thước bộ nhớ.

![.](src-image/w4_7.png)

Việc lựa chọn bộ nhớ cho máy ảo kết thúc, ấn forward chuyển sang màn hình cài đặt cuối cùng. Ở đây, ta cần đặt tên cho máy ảo và thay đỗi thiết lập mạng nếu cần. Cuối cùng, ấn finish để hoàn tất việc thiết lập máy ảo.

![.](src-image/w4_8.png)

Việc cài đặt hệ điều hành hoàn tất và có thể sử dụng bình thường

![.](src-image/w4_9.png)


### 1.2 Tạo Máy Ảo

### 1.3 Quản lý Network và Storage

### 1.4 Template và Snapshot

### 1.5 Migrate Virtual Machine



## 2. Hướng Dẫn Sử Dụng KimChi

