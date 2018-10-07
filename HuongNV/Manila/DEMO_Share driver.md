# Một vài tìm hiểu về Share Drivers trong Manila projects

## Mục lục

- [1. LVM share driver](#1)
    - [1.1 Vai trò của LVM](#11)
    - [1.2 Các thành phần trong LVM](#12)
    - [1.3 Cấu hình manila-share với LVM](#13)
- [2. Generic driver](#2)


<a name="1"></a>

# 1. LVM share driver

LVM - Logical Volume Manager là phương pháp cho phép ấn định không gian đĩa cứng thành nhiều logical volume, làm cho việc thay đổi kích thước trở nên dễ dàng hơn so với `partition`. Với kĩ thuật Logical Volume Manager(LVM) bạn có thể thay đổi kích thước mà không cần phải sửa lại table của OS. Điều này thật hữu ích với những trường hợp sử dụng hết phần bộ nhớ còn trống của partition và muốn mở rộng dung lượng của nó.

<a name="11"></a>

## 1.1 Vai trò của LVM

LVM là kĩ thuật quản lý việc thay đổi kích thước lưu trữ của ổ cứng
- Không để hệ thống bị gián đoạn hoạt động
- Không làm hỏng dịch vụ
- Có thể kết hợp Host Swapping(thao tác thay thế nóng các thành phần bên trong máy tính)

<a name="12"></a>

## 1.2 Các thành phần trong LVM

**Mô hình câc thành phần trong LVM**

![Imgur](https://i.imgur.com/VlNpGD9.jpg)

**Hard drives - Drives**

Thiết bị lưu trữ dữ liệu, ví dụ như trong linux là `/dev/sda`

**Partition**

Partitions là các phân vùng của Hard drives, mỗi Hard drives có 4 parttition trong đó bao gồm 2 loại là primary partition và extended partition

- **Primary partition:**
    - Phân vùng chính, có thể khởi động
    - Mỗi đĩa cứng có thể có tối đa 4 phân vùng này
- **Extended partition:**
    - Phân vùng mở rộng, có thể tạo những vùng luân lý

**Physical Volumes**

Là một cách gọi khác của partition trong kĩ thuật LVM, nó là những thành phần cơ bản được sử dụng bởi LVM. Một physical volume không thể mở rộng ra ngoài phạm vi một ổ đĩa.

**Volume Group**

Nhiều Physical Volume trên những ổ đĩa khác nhau được kết hợp lại thành một Volume Group

![Imgur](https://i.imgur.com/9pcbJQe.png)

Volume Group được sử dụng để tạo ra các Logical Volume, trong đó người dùng có thể tạo ra, thay đổi kích thước, lưu trữ, gỡ bỏ và sử dụng

**Logical Volume**

Volume Group được chia nhỏ thành nhiều Logical Volume, mỗi Logical Volume có ý nghĩa tương tự như partition. Nó được dùng cho các mount point và được format với những định dạng khác nhau như ext2, ext3, ext4..

![Imgur](https://i.imgur.com/hXMOFnk.png)

Khi dung lượng của Logical Volume được sử dụng hết ta có thể đưa thêm ỏ đĩa mới bổ sung cho Volume Group và do đó tăng được dung lượng của Logical Volume.


**File Systems**

- Tổ chức và keiemr soát các tập tin
- Được lưu trữ trên ổ đĩa cho phép truy cập nhanh chóng và an toàn
- Sắp xếp dữ liệu trên đĩa cứng máy tính
- Quản lý vị trí vật lý của mọi thành phần dữ liệu

<a name="13"></a>

## 1.3 Cấu hình manila-share với LVM

Trên node cài manila-share phải cài thêm các gói package
- NFS server
- Samba server >= 3.2.0
- LVM2 >= 2.02.66

Với backend là LVM, ta cần tạo ra một Volume Group và khai báo Volume Group này cho manila-share

- Install LVM và NFS server

```
# apt-get install lvm2 nfs-kernel-server
```

- Tạo LVM physical volume **dev/sdc**

```
# pvcreate /dev/sdc
Physical volume "/dev/sdc" successfully created     # Tạo physical volume thành công
```
`Lưu ý: LVM driver phải cài đặt trên một node empty local block storage để tránh xung đột với Block Storage service`

- Tạo LVM volume group **manila-volumes**

```
# vgcreate manila-volumes /dev/sdc
Volume group "manila-volumes" successfully created     # Tên volume group là `manila-volumes`
```

- Cấu hình co LVM. Mặc định LVM sẽ scan trong thư mục `/dev` của các thiết bị block storage device bao gồm các volume. Nếu các project sử dụng LVM trên những volume của họ, tool scan sẽ phát hiện những volume đó và cố gắng cache chúng, do vậy nó có thể gây ra nhiều vấn đề với cả OS và project volume. Cấu hình để LVM chỉ scan ổ có `manila-volumes` và `volume-group`

Mờ file `/etc/lvm/lcm.conf` để chỉnh sửa cài đặt

```
devices {
...
filter = [ "a/sdb/", "a/sdc", "r/.*/"]
```

*Lưu ý: `a` là cho phéo scan trên `/dev/sdb` và `/dev/sdc`, còn `r` là reject tất cả các device còn lại*

## Cấu hình manila-share

1. Mở file `/etc/manila/manila.conf` và cấu hình như sau
- Trong [DEFAULT] session, enable LVM driver và NFS protocol

```
[DEFAULT]
...
enabled_share_backends = lvm     # lvm là tên backend
enabled_share_protocols = NFS,CIFS    # giao thức cho phép là NFS và CIFS
```

- Tạo backend trong [lvm] session

```
[lvm]
share_backend_name = LVM                               # tên backend
share_driver = manila.share.drivers.lvm.LVMShareDriver # driver sử dụng
driver_handles_share_servers = False  # driver không xử lý share server
lvm_share_volume_group = manila-volumes  # tên volume group vừa tạo
lvm_share_export_ip = MANAGEMENT_INTERFACE_IP_ADDRESS # địa chỉ IP trên storage node
```

2. Restart manila-share

```
service manila-share restart
```

3. Tiến hành kiểm tra service manila-share đã được up hay chưa

```
manila service-list
```

4. Tạo share-type với DHSS = False

```
manila type-create lvm False
```

```
# lvm: Tên share-type mà chúng ta muốn tạo
# False: Disable driver_handles_share_server
```

5. Gán share-type tới một backend cụ thể

```
manila type-key lvm set share_backend_name=LVM
```

```
# lvm: Là share-type vừa tạo ở trên
# LVM: Backend vừa tạo ở trên
```

6. Kiểm tra để xem việc gán thành công hay chưa

```
manila extra-specs-list
```

7. Tạo một share dùng giao thưc NFS kích thước 4GB, sử dụng backend `lvm` và đặt tên là `share-lvm-1`

```
manila create nfs 4 --name share1 --share-type lvm
```

```
    - nfs là giao thức
    - 4 là kích thước share, tính bằng GB
    - --name tên của share muốn đặt
    - --share-type là type-share ta tạo ở trên
```

8. Thực hiện kiểm tra đường dẫn của share vừa tạo để có thể mount tới VM, đường dẫn tại mục `path`

```
manila show share1

# share1 là tên của share vừa create ở trên

```
![Imgur](https://i.imgur.com/2n9bqBt.png)


Kiểm tra các share vừa tạo

```
manila list
```

![Imgur](https://i.imgur.com/ifT02N7.png)

# Allow access to the share

Để VM có thể mount được, ta cần cầu hính `access-allow` dựa theo địa chỉ IP của instance

```
manila access-allow share1 ip INSTANCE_IP
```

![Imgur](https://i.imgur.com/9sMJlqv.png)


# Mount the share on a compute instance

Login vào instance và create 1 folder

```
mkdir ~/test_folder
```

Mount NFS share,, sử dụng đường dẫn path như ở trên đề cập

```
mount -vt nfs 10.0.0.41:/var/lib/manila/mnt/share-8e13a98f-c310-41df-ac90-fc8bce4910b8 ~/test_folder
```

<a name="2"></a>

# 2. Generic driver

Yêu cầu khi sử dụng Generic driver là phải cấu hình nova, neutron và cinder trong file cấu hình `/etc/manila/manila.conf` trên node manila-share, trên node manila-share phải cài đặt L2 Agent

Trước khi create share với Generic driver, DHSS(driver_handles_share_servers) phải được enabled, phải define ít nhất 1 image, 1 network và 1 share-network để sử dụng cho việc create a share-server

- 1. Thực hiện khởi tạo một share-type với DHSS=True

![Imgur](https://i.imgur.com/rvb9KKZ.png)

```
default_share_type là tên share-type 
```

- 2. Thực hiện khởi tạo một share server image, image này chứa share service với NFS packages

![Imgur](https://i.imgur.com/G8YNGJK.png)

- 3. Thực hiện liệt kê các network

![Imgur](https://i.imgur.com/mOi4cDI.png)

- 4. Thực hiện khởi tạo share-network

![Imgur](https://i.imgur.com/HquRPa6.png)

```
- Net-id và subnet-id có thể dễ dàng lấy được qua mục liệt kê network ở trên bằng câu lệnh neutron net-list
- Khi khởi tạo share-network thành công, sẽ có một mạng và subnet mới được tạo ra, chúng ta có thể kiểm tra bằng cách sử dụng neutron net-list
```

- 5. Chính sửa file cấu hình `/etc/manila/manila.conf` như sau:

```
enabled_share_backends= generic1 #generic1 là tên phần backend  
enabled_share_protocols=NFS,CIFS #giao thức cho phép
default_share_type = generic     # Driver sử dụng là Generic
```

Khai báo cấu hình backend như sau:

```
[generic1]
share_backend_name = GENERIC-1  
share_driver = manila.share.drivers.generic.GenericShareDriver  
driver_handles_share_servers = True  
service_instance_flavor_id = 100  
service_image_name = manila-service-image  
service_instance_user = manila  
service_instance_password = manila
connect_share_server_to_tenant_network = True
#interface_driver = manila.network.linux.interface.BridgeInterfaceDriver # nếu sử dụng LinuxBridge thì uncomment
interface_driver = manila.network.linux.interface.OVSInterfaceDriver  
```

Thực hiện restart lại dịch vụ manila-share và kiểm tra lại list các service

```
# service manila-share restart
# manila service-list
```

- 6. Thực hiện Khởi tạo share server sử dụng giao thức NFS, có tên là demo-share1 và có kích thước là 1GB

![Imgur](https://i.imgur.com/N3II2ta.png)

- 7. Thực hiện access-allow tới instance

![Imgur](https://i.imgur.com/67tEvqX.png)

- 8. Xác định đường dẫn để có thể mount share, sử dụng `manila show demo-share1`

![Imgur](https://i.imgur.com/geeM02F.png)

- 9. Truy cập tới instance và thực hiện mount share

```
mount -vt nfs 10.254.0.6:/shares/share-0bfd69a1-27f0-4ef5-af17-7cd50bce6550
```


# Tài liệu tham khảo

- https://qiita.com/tksarah/items/3368b6e502ce5092340b
- https://docs.openstack.org/project-install-guide/shared-file-systems/newton/post-install.html#post-install
- https://qiita.com/makisyu/items/0a84e8f905fddd8fd074
- http://alesnosek.com/blog/2016/05/22/test-driving-openstack-manila/