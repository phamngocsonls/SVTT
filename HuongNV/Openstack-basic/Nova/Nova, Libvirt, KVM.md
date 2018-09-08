# Tìm hiểu về Nova, libvirt, KVM

## Mục lục

* [1. Overview](#1)
    * [1.1. QEMU(KVM)](#11)
    * [1.2. Libvirt](#12)
* [2. Nova, Libvirt, QEMU trong việc quản lý máy ảo](#2)
    * [2.1 Nova Compute Workflow](#21)
    * [2.2 Spawn](#22)
    * [2.3 Reboot](#23)
    * [2.4 Suspend](#24)
    * [2.5 Live Migaration](#25)
    * [2.6 Resize/Migrate](#26)
    * [2.7 Snapshot](#27)



<a name="1"></a>

# 1. Overview


<a name="11"></a>

## 1.1 QEMU(KVM)

- KVM là giải pháp ảo hóa toàn diện nhất trên phần cứng x86 và hỗ trợ hầu hết các hệ điều hành của Linux và Windows. 
- KVM chuyển đổi một nhân Linux thành một bare metal hypervisor, cung cấp giải pháp ảo hóa full virtualization
- Nó sử dựng libvirt làm giao diện tương tác giữa QEMU và KVM


<a name="12"></a>

## 1.2 Libvirt

- Xử lý các thao tác quản lý và tương tác với QEMU
- Instances(VMs) được định nghĩa trong libvirt bằng XML file
- Translate XML file thành command line và gọi đến QEMU
- Thực hiện quản lý các VMs bằng `virsh` command line


<a name="2"></a>

# 2. Nova, Libvirt, QEMU trong việc quản lý máy ảo

<a name="21"></a>

## Nova Compute Workflow

* Compute Manager
Quản lý các VMs trong 2 file:
  - File: nova/compute/api.py
  - File: nova/compute/manager.py

* Nova Libvirt Driver
    - File: nova/virt/libvirt/driver.py
    - File: nova/virt/libvirt/*.py


<a name="22"></a>

## 2.1 Spawn

* Nova CLI action: `nova boot` thể hiện rằng VMs đnag trong quá trình boot
* Các request từ user gửi tới `API` chuyển tới `Scheduler` -> Compute và cuối cùng gửi tới Libvirt Driver. Compute thực hiện quản lý việc cấp phát tài nguyên network
* Nova sẽ thực hiện create disk file:
    * Đầu tiên, sẽ tải image từ Glance into instance_dir/_bare và chuyển đổi định dạng file thành RAW
    * Tạo instance_dir/uuid/{disk, disk.local, disk.swap}
        * Create QCOW2 disk file từ _base image
        * Create QCOW2 disk.local và disk.swap
* Create XML file và tạo bản copy instance_dir
    * instance_dir/libvirt.xml không bao giờ được sử dụng vởi Nova
* Thiết lập kết nối volume ( dành cho việc boot from volume)
* Build network cho instance
    * Thiết lập bridges/VLANs 
    * Create security group cho instance
* Định nghĩa domain với Libvirt, sử dụng XML file
    * Sử dụng command line: virsh define instance_dir/<uuid>/libvirt.xml
* Start instance
    * Sử dụng: virsh start <uuid> hoặc virsh start <domain name>


<a name="23"></a>

## 2.3 Reboot
- Là quá trình restart lại instance
- Có 2 laoij reboot qua API: hard và soft reboot
    * Soft reboot phụ thuộc vào guest Ó và ACPI qua QEMU
    * Hard reboot tương ứng ở mức hypervisor
    * Sử dụng command line: `nova reboot` or `nova reboot-hard`
- Hard reboot is the sledge-o-matic of just fix it operations

### Hard Reboot Workflow
* Destroy domain
    * tương đương với virsh destroy
    * không destroy data, chỉ destroy QEMU process
* Thiết lập lại all volume connections
* Định nghĩa lại XML file
* Kiểm tra, tìm kiếm và cài đặt lại các file còn thiếu
* Recreate VIFs như bridge, VLAN
* Recreate và apply iptables rules


<a name="24"></a>

## 2.4 Suspend

- tương đương với: virsh managed-save
- Một số vấn đề tại trạng thái này như:
    - lưu giữ trạng thái bộ nhớ tiêu thụ trên disk giống như memory của instance
    - disk space không được hiển thị rõ qua quota
    

<a name="25"></a>

## 2.5 Live Migration

- có 2 loại live migartion với largely different code paths: normal và block migrations
- `normal migration` yêu cầu về source và target của hypervisor cũng như có thể truy cập tới instance data như các shared storage, NAS
- `block migration` không yêu cầu gì đặc biêt, instance disk được migrate như 1 tiến trình process

### Live Migration Workflow
- kiểm tra hệ thống storage backend có phù hợp với loại migate không
- Tại destination host:
    - tạo volume connections
    - nếu là block migration, cần tạo instance directory, theiets lập các file còn thiêu từ Glance image và tạo 1 empty instance disk
- Tại source host, khởi tạo quá trình migrate
- Khi quá trình migrate hoàn tất, tạo lại XML file và định nghĩa lại VMs


<a name="26"></a>

## 2.6 Resize/Migrate

- Migrate khác với live migrate ở chỗ chỉ thực hiện được khi tắt máy ảo, tức là Libvirt không chạy
- Nó yêu cầu SSH key đối với các user đang chạy nova-compute với mọi hypervisor
- resize không cho phép chia lại ổ đĩa vì nó k an toàn

### Resize/Migrate Workflow

- shutdown instance, tương đương với virsh destroy, ngắt kết nối tới volume
- di chuyển tất cả các thư mục hiện tại của instance (instance_dir -> instance_dir_resize)
- nếu sử dụng QCOW2, cần convert image snag flat. quá trình này tốn thời gian
- với shared storage, chueyenr new instance_dir vào hoặc có thể copy toàn bộ qua SCP


<a name="27"></a>

## 2.7 Snapshots 

- có 2 loại snapshot là: live snapshot và cold snapshot
- Live snapshot không yêu cầu config gì cả, Nova sẽ thực hiện tự động

### Live snapshot workflow
- kiểm tra hypervisor có đảm bảo live snapshot không
- Instance phải ở trạng thái running
- Tạo empty QCOW2 image trong thư mục tạm thời
- Qua libvirt, thiết lập sao chép từ instance hiện tại sang empty disk đã tạo ở trên
- Kiểm tra trạng thái của block, nếu không còn byte dữ liệu nào để sao chép thì ta đã có 1 bản sao chép của instance disk
- Sử dụng qemu-img, convert bản copy image sang định dạng file khác nào đó.
- Upload image to Glance


### Cold Snapshot workflow
- Máy ảo phải ở trạng thái shutdown
- Khi máy ảo đã shutdown, sử dụng qemu-img convert 1 bản copy có định dạng giống với image gốc từ Glance
- Trả lại trạng thái gốc của instance
- Upload abnr copy/converted image to Glance


# Tài liệu tham khảo
- https://www.openstack.org/assets/presentation-media/OSSummitAtlanta2014-NovaLibvirtKVM2.pdf
- https://github.com/ngohuongbn/thuctap012017/tree/master/XuanSon/OpenStack/Nova/docs
