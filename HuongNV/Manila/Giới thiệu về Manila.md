# Tìm hiểu về Manila

## Mục lục

- [1. Giới thiệu về Manila](#1)
    - [1.1 How Manila work](#11)
- [2. Các thành phần trong Manila](#2)
    - [2.1 Share Creation Workflow with share server](#21)
    - [2.2 Share Creation Workflow without share server](#22)
- [3. Key concept](#3)
    - [3.1 Share](#31)
    - [3.2 Share Access Rules](#32)
    - [3.3 Snapshot](#33)
    - [3.4 Share Networks](#34)
    - [3.5 Security Services](#35)
    - [3.6 Storage Pool](#36)
    - [3.7 Share types](#37)
    - [3.8 Share servers](#38)
- [4. Networking](#4)


<a name="1"></a>

# 1. Giới thiệu về Manila

The Openstack Shared File Systems service (Manila )là một project về chia sẻ file trong Openstack. Manila ban đầu được hình thành như là một extension cho Block Storage service (Cinder), nhưng giờ nó phát triển thành một project độc lập.

![Imgur](https://i.imgur.com/2Emyfro.png)

Với Shared File Systems service, ta có thể tạo hệ thống tệp từ xa, mount file system vào các instance. Manila có từ bản Kilo được phát hành vào năm 2015. Manila mang đến sự bổ sung các dịch vụ lưu trữ hiện có, mở rộng và cải thiện khả năng tiêu thụ tài nguyên lưu trữ dùng chung bên ngoài.

Ví dụ sau đây miêu tả 2 file share giữa các VM với nhau. `Marketing file` share file giữa VM 6 và 8, còn `R&D file` share giữa VM 1 và 7.

![Imgur](https://i.imgur.com/1W0mccx.png)


<a name="11"><?a>

## 1.1 How Manila work

Nhiệm vụ chính của Manila là cho phép Nova compute instances truy cập tới storage dựa trên shared-file, các storage ở đây có thể là các external storage như `Ceph` hoặc `GlusterFS`

Dịch vụ Openstack Shared File Systems cung cấp file storage cho một máy ảo. Dịch vụ Shared File Systems cung cấp một cơ sở hạ tầng để quản lý và cung cấp các file chia sẻ. Dịch vụ cũng cho phép quản lý các kiểu chia sẻ cũng như các share snapshot nếu driver hỗ trợ chúng.


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

<a name="21"></a>

## 2.1 Share Creation Workflow with share server

![Imgur](https://i.imgur.com/iNtiMnl.png)

1. Clients request to create share through REST API hoặc sử dụng python-manilaclient:
Qúa trình xử lý request như sau:
    a. `manila-api` xác thực request, xác thực user và gửi message tới AMQP queue chờ xử lý
    b. `manila-share` xử lý message từ queue, gửi message tới `manila-scheduler` để xác định backend share
    c. `manila-scheduler` lập lịch, chuyển các request với share service thích hợp
    d. `manila-share` quản lý các backend cung cấp share file system
2. Share manager liên kết với backend và chọn ra một network plugin(standalone plugin, Neutron hoặc Nova network, được định nghịa trong file manila.conf)
3. NetApp's Manila driver create request share qua một kết nối tới storage subsysstem
4. `manila-share` process create share metadata và post response mesgae tới AMQP queue
    `manila-api` xử lý message từ queue và responds tới clients with share ID information
5. Sau khi create share, clients sử dụng ID information to request updated share details to mount share

<a name="2.2"></a>

## 2.2 Share Creation Workflow without share server 

![Imgur](https://i.imgur.com/mMIkKOb.png)

1. Clients request to create share through REST API hoặc sử dụng python-manilaclient:
Qúa trình xử lý request như sau:
    a. `manila-api` xác thực request, xác thực user và gửi message tới AMQP queue chờ xử lý
    b. `manila-share` xử lý message từ queue, gửi message tới `manila-scheduler` để xác định backend share
    c. `manila-scheduler` lập lịch, chuyển các request với share service thích hợp
    d. `manila-share` quản lý các backend cung cấp share file system
2. NetApp's Manila driver create request share thông qua kết nối tới storage subsystem
3. `manila-share` process create share metadata và post response mesgae tới AMQP queue
    `manila-api` xử lý message từ queue và responds tới clients with share ID information
4. Sau khi create share, clients sử dụng ID information to request updated share details to mount share

<a name="3"></a>

# 3. Key concept

<a name="31"></a>

## 3.1 Share 

Là một đơn vụ của storage với một giao  thức, một kích thước và một danh sách được phép truy cập. Tất cả các share tồn tại trên một backend. Một vài share tương tác với share networ và share server. Các giao thức chính được hỗ trợ là NFS và CIFS, ngoài ra còn có các giao thức khác được hỗ trợ như GLUSTERFS

<a name="32"></a>

## 3.2 Share Access Rules
- Thiết lập clients nào có thể truy cập vào `share` file system
- Việc thiết lập này có thể dựa trên IP address

<a name="33"></a>

## 3.3 Snapshot 

Snapshot là một bản copy của share. Snapshot có thể được sử dụng để tạo một share mới. Share không thể bị xóa nếu có các snapshot tạo ra trên share đó (ta phải xóa hết snapshot của share đó rồi mới xóa được share)

<a name="34"></a>

## 3.4 Share Networks

Một share network là một đối tượng được định nghĩa bởi một project mà báo cho Manila về security và cấu hình mạng cho một nhóm của các share. Share network chỉ thích hợp cho backend quản lý share server. Một share network bao gồm các dịch vụ bảo mật, network và subnet.

<a name="35"></a>

## 3.5 Security Services
- Định nghĩa, thiết lập rules cho việc xác thực, truy cập vào file share(ví dụ: Có thể khai báo các rules thông qua các external service: LDAP, Active Directory, Kerberos)
- Có thể khai báo Shares với multiple security services

<a name="36"></a>

## 3.6 Storage Pool
Từ bản Kilo trở đi, Shared File Systems có thể sử dụng `storage pool`. Storage pool là một hoặc một nhóm tài nguyên lưu trữ mà dịch vụ Shared File Systems chọn làm lưu trữ khi cấp phép chia sẻ.

<a name="37"></a>

## 3.7 Share types

A share type cho phép ta lọc và chọn backends trước khi create a share và set data cho nó. A share type hoạt động tương tự như Block Storage volume type

Để tạo một share type, sử dụng **manila type-create** command:

```
manila type-create [--snapshot_support <snapshot_support>]
                   [--is_public <is_public>]
                   <name> <spec_driver_handles_share_servers>
```

Trông câu lệnh, **name** để thiết lập tên cho share type, **is_public** defines the level of the visibility for share type, **snapshot_support** và **spec_driver_handles_share_servers** là các thông số bổ sung để filter backends. Các thông số bổ sung có thể được thiết lập như sau:

- **driver_handles_share_servers**. Required. Xác định driver mode để quản lý vòng đời share server. Gía trị thiết lập có thể là **true/1** và **false/0**. Thiết lập True khi share driver có thể quản lý hoặc xử lý vòng đời share server. Thiết lập False khi admin quản lý chứ không phải là share driver như trên
- **snapshot_support**. Default là **True**. Set True để tìm 1 backends support share snapshots, set False thì ngược lại với False.

<a name="38"></a>

## 3.8 Share servers

A share server là một thực thể nhằm quản lý các chia sẻ trên một mạng cụ thể. 


<a name="4"></a>

# 4. Networking 

Khác với Openstack Block Storage service, Shared File Systems service cần kết nối tới Networking service. The share service required the option to self-manage share servers. Để xác thực và ủy quyền cho client, ta có thể cấu hình dịch vụ Shared File Systems service làm việc với các dịch vụ xác thực như LDAP, Kerberos hay là Microsoft Active Directory

## Share network

Một share network là một đối tượng được định nghĩa bởi một project mà báo cho Manila về security và cấu hình mạng cho một nhóm của các share. Share network chỉ thích hợp cho backend quản lý share server. Một share network bao gồm các dịch vụ bảo mật, network và subnet.

## How to create share network

Liệt kê các networks trong project

![Imgur](https://i.imgur.com/exW2iO8.png)

A share network chứa toàn bộ thông tin mà share server sử dụng để share giữa các host với nhau. Có thể khởi tạo và gán mối share với một share network cụ thể dựa trên ID của share network, qua đó instance có thể truy cập tới share mà ta vừa tạo

Khi thực hiện khởi tạo một share network, ta có thể chỉ định một loại mạng cụ thể
- Openstack Networking(neutron), chỉ định cụ thể network ID và subnet ID
    - Plugin sử dụng `manila.network.nova_network_plugin.NeutronNetworkPlugin`
- Legacy networking(nova-network), chỉ định cụ thể network ID
    - Plugin sử dụng `manila.network.nova_network_plugin.NovaNetworkPlugin`

Tham khảo thêm Network Plugin tại [Network plug-ins](https://docs.openstack.org/manila/pike/admin/shared-file-systems-network-plugins.html#shared-file-systems-network-plugins)

A share network chứa một số thông tin như sau:
- IP block in CIDR notation from which to allocate the network
- IP version
- Network type, ví dụ `vlan, vxlan, gre hoặc flat`

Ví dụ khởi tạo một share network

![Imgur](https://i.imgur.com/10LfYJv.png)

```
Segmentation_id, cidr, ip_version và network_type của share network vừa khởi tạo được set value tự động dựa theo network provider
```

Để check network list, run

![Imgur](https://i.imgur.com/ei6ol4P.png)

Nếu sử dụng generic driver với DHSS=True, trong topo network sẽ xuất hiện thêm một `manila_service_network` như sau

![Imgur](https://i.imgur.com/9FrdLA8.png)

Sử dụng commnand line để liệt kê các network hiện có, trong đó có manila_service_network vừa khởi tạo

![Imgur](https://i.imgur.com/tTSfjHT.png)

Xem thông tin chi tiết về share network vừa khởi tạo, run

![Imgur](https://i.imgur.com/Bckei5B.png)

<a name="5"></a>

# 5. Security services
