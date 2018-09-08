# Kiến trúc của OpenvSwitch
## [1. Kiến trúc tổng quan](#general)
## [2. Các thành phần của OpenvSwitch](#component)
## [3. OVS Packet Handling](#handle)
## [4. OVS code walk through](#code)
### [4.1. vswitchd](#vswitchd)
### [4.2. OVSDB](#ovsdb)
### [4.3. Datapath](#datapath)
---
## <a name="general"></a> 1. Kiến trúc tổng quan
![Fig1.1: OVS Architecture](images/2-OVS-Architecture/ovs_arch.jpg)	
- Nhắc lại là OVS thường được sử dụng để kết nối các máy ảo (VM/container) trong một host. OVS quản lý cả các port vật lý (eth0, eth1) và các port ảo (ví dụ như các port của VMs).
- Ba khối thành phần chính của OVS:
	- __ovsswitchhd__: Là daemon chạy trên user space.
	- __ovsdb-server__: Là database server của OVS chạy trên user space
	- __kernel module__ (data path): Là module thuộc kernel space, thực hiện công việc chuyển tiếp gói tin.		
- **ovs-vswitchd** nhận các gói tin OpenFlow từ **OpenFlow Controller**, giao thức **OVSDB** sẽ định dạng (format) các gói tin từ **ovsdb-server**. Giao tiếp giữa **ovs-vswtichd** và **datapath** thông qua **netlink** (một họ socket tương tự như Unix Domain Socket). 

## <a name="component"></a> 2. Các thành phần của OpenvSwitch
### 2.1. vswitchd (OVS Daemon)
- **ovs-vswitchd** là daemon của OpenvSwitch chạy trên userspace. Nó đọc cấu hình của OVS từ **ovsdb-server** thông qua kênh IPC (Inter Process Communication) và đẩy cấu hình xuống OSV bridge (là các instance của thư viện **ofproto**). Nó cũng đẩy trạng thái và thông tin thống kê từ các OVS bridge vào trong database.
- **ovs-vswitchd** giao tiếp với:
	- Môi trường ngoài (outside world): sử dụng giao thức OpenFlow
	-  **ovsdb-server**: sử dụng giao thức OVSDB
	- **kernel**: thông qua **netlink** (tương tự như Unix socket domain)
	- **system**: thông qua abstract interface là **netdev**
- **ovs-vswitchd** triển khai miroring, bonding và VLANs
![Fig2.1: vswitchd - OVS main daemon](images/2-OVS-Architecture/vswitchd.png)

### 2.2. OVSDB
- Nếu như những cấu hình tạm thời (transient configurations) ví dụ như flows được lưu trong **datapath** và **vswitchd** thì các cấu hình bền vững sẽ được lưu trong **ovsdb** và vẫn được lưu giữ sau khi khởi động lại hệ thống. Các cấu hình này bao gồm cấu hình về bridge, port, interface, địa chỉ của OpenFlow controller (nếu dùng),...
- **ovsdb-server** cung cấp giao diện RPC (Remote Procedure Call) tới **ovsdb**. Nó hỗ trợ trình khách JSON-RPC kết nối tới thông qua passive TCP/IP hoặc Unix Domain sockets.
- **obsdb-server** chạy như một backup server hoặc như một active server. Tuy nhiên chỉ có active server mới xử lý giao dịch làm thay đổi **ovsdb**.

![Fig2.2: **ovsdb core table**](images/2-OVS-Architecture/ovsdb_tables.jpg)

### 2.3 Datapath (OVS Kernel Module)
- Datapath là module chính chịu trách nhiệm chuyển tiếp gói tin (packets) trong OVS. Datapath được triển khai (implemented) trong kernelspace nhằm mục đích đạt hiệu năng cao. Nó caches lại các OpenFlow flows và thực thi các action trên các gói tin nhận được nếu các gói tin đó match với một flow đã tồn tại (specific flows). Nếu gói tin không khớp với bất cứ flow nào thì gói tin sẽ đưọc chuyển lên userspace program **ovs-vswitchd**. Nếu flow matching tại **vswitch** thành công thì nó sẽ gửi gói tin lại cho **kernel datapath** kèm theo các action tương ứng để xử lý gói tin đồng thời thực hiện cache lại flow đó vào datapath để datapath xử lý những gói tin cùng loại này đến tiếp sau. Hiệu năng cao đạt được ở đây là bởi thực tế hầu hết các gói tin sẽ match flow thành công tại datapath và do đó được xử lý trực tiếp tại kernelspace.
- Phân loại datapath mà OVS hỗ trợ:
	- Linux upstream: là datapath triển khai bởi module 	của nhân đi cùng với bản phát hành Linux.
	- Linux OVS tree: là datapath triển khai bởi module của nhân phát hành cùng với cây mã nguồn của OVS. Một số tính năng của module này có thể không hỗ trợ các kernel phiên bản cũ, trong trường hợp này, Linux kernel version tối thiếu sẽ được đưa ra để tránh bị biên dịch lỗi. 
	- Userspace datapath: là datapath cho phép xử lý và chuyển tiếp gói tin ở userspace, điển hình là DPDK.
	- Hyper-V: hay còn gọi là Windows datapath.

## <a name="handle"></a> 3. OVS Packet Handling
Đầu tiên hãy xem một gói tin đi qua OVS như thế nào:
![Fig2.2: **ovsdb core table**](images/2-OVS-Architecture/ovs_packet_flow.jpg)
- Ta nhắc lại rằng, OVS là một phần mềm switch hỗ trợ OpenFlow.
- Openflow controller chịu trách nhiệm đưa ra các hướng dẫn (hay còn gọi là **flow**) cho datapath biết làm sao xử lý các loại gói khác nhau. Một **flow** mô tả hành động (hay còn gọi là **action**) mà datapath thực hiện để xử lý các gói tin của cùng một loại như thế nào. Các kiểu **action** bao gồm chuyển tới (forwarding) pỏt khác, thay đổi vlan tag,... Quá trình tìm kiếm flow khớp với gói tin được gọi là **flow matching**.
- Nhằm mục đích đạt được hiệu năng tốt (như đã đề cập ở trên), một phần của flows được cache trong **datapath** và phần còn lại nằm ở **vswitchd**.
- Một gói tin đi vào OVS datapath sau khi nó đưọc nhận trên một card mạng (NIC - Network Interface Card). Nếu gói tin khớp với flow nào đó trong datapath thì datapath sẽ thực thi các action tương ứng mô tả trong flow entry. Nếu không (flow missing), datapath sẽ gửi gói tin lên ovs-vswitchd và tiến trình flow matching khác được xử lý tại đây. Sau khi ovs-vswitchd xác định làm sao để xử lý gói tin, nó gửi trả gói tin lại cho datapath cùng với yêu cầu xử lý. Đồng thời, vswitchd cũng yêu cầu datapath cache lại flow để xử lý các gói tin tương tự sau đó.

## <a name="code"></a> 4. OVS code walk through
### <a name="vswitchd"></a> 4.1. vswitchd
#### 4.1.1. Overview
Trước khi deep dive ta nhắc lại một vài điểm quan trọng của **vswitchd**.

### <a name="ovsdb"></a> 4.2. OVSDB 
### <a name="datapath"></a> 4.3. Datapath
