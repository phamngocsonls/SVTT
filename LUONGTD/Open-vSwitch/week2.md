# Kiến trúc của OpenvSwitch
## [1. Kiến trúc tổng quan](#general)
## [1.1. Các thành phần của OpenvSwitch](#component)
## [1.2. OVS Packet Handling](#handle)
## [2. vswitchd](#vswitchd) // inprogress
## [3. OVSDB](#ovsdb)	// TODO
## [4. Datapath](#datapath)	//TODO
---
## <a name="general"></a> 1. Kiến trúc tổng quan
![Fig1.1: OVS Architecture](images/2-OVS-Architecture/ovs_arch.jpg)	
- Nhắc lại là OVS thường được sử dụng để kết nối các máy ảo (VM/container) trong một host. OVS quản lý cả các port vật lý (eth0, eth1) và các port ảo (ví dụ như các port của VMs).
- Ba khối cấu trúc chính của OVS:
	- __vswitchd__: Là daemon chạy trên user space.
	- __ovsdb-server__: Là database server của OVS chạy trên user space
	- __kernel module__ (data path): Là module thuộc kernel space, thực hiện công việc chuyển tiếp gói tin.		
- **ovs-vswitchd** nhận các gói tin OpenFlow từ **OpenFlow Controller**, giao thức **OVSDB** sẽ định dạng (format) các gói tin từ **ovsdb-server**. Giao tiếp giữa **ovs-vswtichd** và **datapath** thông qua **netlink** (một họ socket tương tự như Unix Domain Socket). 

## <a name="component"></a> 1.1. Các thành phần quan trọng của OpenvSwitch
Các thành phần này tưong ứng nằm trong 3 khối cấu trúc chính đã đề cập ở trên.
### 1.1.1. OVS Daemon
- **ovs-vswitchd** là daemon của OpenvSwitch chạy trên userspace. Nó đọc cấu hình của OVS từ **ovsdb-server** thông qua kênh IPC (Inter Process Communication) và đẩy cấu hình xuống OSV bridge (là các instance của thư viện **ofproto**). Nó cũng đẩy trạng thái và thông tin thống kê từ các OVS bridge vào trong database.

!["Fig2.1: vswitchd - OVS main daemon"](images/2-OVS-Architecture/vswitchd.png)

### 1.1.2. OVSDB
- Nếu như những cấu hình tạm thời (transient configurations) ví dụ như flows được lưu trong **datapath** và **vswitchd** thì các cấu hình bền vững sẽ được lưu trong **ovsdb** và vẫn được lưu giữ sau khi khởi động lại hệ thống. Các cấu hình này bao gồm cấu hình về bridge, port, interface, địa chỉ của OpenFlow controller (nếu dùng),...
- **ovsdb-server** cung cấp giao diện RPC (Remote Procedure Call) tới **ovsdb**. Nó hỗ trợ trình khách JSON-RPC kết nối tới thông qua passive TCP/IP hoặc Unix Domain sockets.
- **obsdb-server** chạy như một backup server hoặc như một active server. Tuy nhiên chỉ có active server mới xử lý giao dịch làm thay đổi **ovsdb**.

![Fig2.2: **ovsdb core table**](images/2-OVS-Architecture/ovsdb_tables.jpg)

### 1.1.3. Datapath
- Datapath là module chính chịu trách nhiệm chuyển tiếp gói tin (packets) trong OVS. Datapath được triển khai (implemented) trong kernelspace nhằm mục đích đạt hiệu năng cao. Nó caches lại các OpenFlow flows và thực thi các action trên các gói tin nhận được nếu các gói tin đó match với một flow đã tồn tại (specific flows). Nếu gói tin không khớp với bất cứ flow nào thì gói tin sẽ đưọc chuyển lên userspace program **ovs-vswitchd**. Nếu flow matching tại **vswitch** thành công thì nó sẽ gửi gói tin lại cho **kernel datapath** kèm theo các action tương ứng để xử lý gói tin đồng thời thực hiện cache lại flow đó vào datapath để datapath xử lý những gói tin cùng loại này đến tiếp sau. Hiệu năng cao đạt được ở đây là bởi thực tế hầu hết các gói tin sẽ match flow thành công tại datapath và do đó được xử lý trực tiếp tại kernelspace.
- Phân loại datapath mà OVS hỗ trợ:
	- Linux upstream: là datapath triển khai bởi module 	của nhân đi cùng với bản phát hành Linux.
	- Linux OVS tree: là datapath triển khai bởi module của nhân phát hành cùng với cây mã nguồn của OVS. Một số tính năng của module này có thể không hỗ trợ các kernel phiên bản cũ, trong trường hợp này, Linux kernel version tối thiếu sẽ được đưa ra để tránh bị biên dịch lỗi. 
	- Userspace datapath: là datapath cho phép xử lý và chuyển tiếp gói tin ở userspace, điển hình là DPDK.
	- Hyper-V: hay còn gọi là Windows datapath.

### <a name="handle"></a> 1.2. OVS Packet Handling
Đầu tiên hãy xem một gói tin đi qua OVS như thế nào:
![Fig2.2: **ovsdb core table**](images/2-OVS-Architecture/ovs_packet_flow.jpg)

- Ta nhắc lại rằng, OVS là một phần mềm switch hỗ trợ OpenFlow.
- Openflow controller chịu trách nhiệm đưa ra các hướng dẫn (hay còn gọi là **flow**) cho datapath biết làm sao xử lý các loại gói khác nhau. Một **flow** mô tả hành động (hay còn gọi là **action**) mà datapath thực hiện để xử lý các gói tin của cùng một loại như thế nào. Các kiểu **action** bao gồm chuyển tới (forwarding) pỏt khác, thay đổi vlan tag,... Quá trình tìm kiếm flow khớp với gói tin được gọi là **flow matching**.
- Nhằm mục đích đạt được hiệu năng tốt (như đã đề cập ở trên), một phần của flows được cache trong **datapath** và phần còn lại nằm ở **vswitchd**.
- Một gói tin đi vào OVS datapath sau khi nó đưọc nhận trên một card mạng (NIC - Network Interface Card). Nếu gói tin khớp với flow nào đó trong datapath thì datapath sẽ thực thi các action tương ứng mô tả trong flow entry. Nếu không (flow missing), datapath sẽ gửi gói tin lên ovs-vswitchd và tiến trình flow matching khác được xử lý tại đây. Sau khi ovs-vswitchd xác định làm sao để xử lý gói tin, nó gửi trả gói tin lại cho datapath cùng với yêu cầu xử lý. Đồng thời, vswitchd cũng yêu cầu datapath cache lại flow để xử lý các gói tin tương tự sau đó.

Ở những phần tiếp theo ta sẽ phân tích lần lượt 3 khối cấu trúc của OVS.
## <a name="vswitchd"></a> 2. vswitchd
### 2.0. Overview
Đầu tiên, ta điểm qua một vài điểm quan trọng của **vswitchd**.

![Fig1.1: OVS Architecture](images/2-OVS-Architecture/ovs_arch.jpg)	

Ta có thể thấy, **ovs-vswitchd** nằm ở vị trí trọng yếu của OVS, vị trí cần phải tương tác với OpenFlow Controller, OVSDB và kernel module.
1. **ovs-vswitchd** giao tiếp với:
	- **Môi trường ngoài** (outside world): sử dụng giao thức OpenFlow
	- **ovsdb-server**: sử dụng giao thức OVSDB
	- **kernel**: thông qua **netlink** (tương tự như Unix socket domain)
	- **system**: thông qua abstract interface là **netdev**
2. **ovs-vswitchd** triển khai (implement) miroring, bonding và VLANs
3. CLI Tools: ovs-ofctl, ovs-appctl
Ta xem xét kiến trúc mức cao (high-level architecture) của OVS (from porter's perspective):

![](images/2-OVS-Architecture/vswitchd-overview.png)	

Ta có thể thấy, module **vswitchd** được chia ra nhỏ hơn thành các submodules/libraries sau:
- **ovs-vswitchd**: vswitchd daemon, như đã đề cập, nó đọc cấu hình của OVS từ **ovsdb-server** thông qua kênh IPC (Inter Process Communication) và đẩy cấu hình xuống OSV bridge (là các instance của thư viện **ofproto**)
- **ofproto**: thư viện trừu tượng hóa ovs bridge (OpenFlow switch)
- **ofproto-provider**: interface để điều khiển một loại OpenFlow switch cụ thể
- **netdev**: thư viện trừu tượng hóa các tương tác với các thiết bị mạng
- **netdev-provider**: interface của hệ điều hành và phần cứng với các thiết bị mạng

Như vậy, ta đã xác định được 4 thành phần chính của **vswitchd**. Ở những phần sau ta sẽ tìm hiểu cấu trúc dữ liệu mô tả các thành phần đó (hoặc các bộ phận của chúng).

### 2.1. ofproto
```struct ofproto``` trừu tượng hóa (abstract) OpenFlow switch. Một thực thể ofproto (ofproto instance) là một OpenFlow switch (bridge).
Code của các cấu trúc dữ liệu nằm ở địa chỉ ```ofproto/ofproto-provider.h``` trong OVS project clone về từ github. Ta sẽ đi phân tích các cấu trúc dữ liệu quan trọng trong file **ofproto-provider.h**:
(Xin phép được lược bớt một số dòng code chỉ để lại outline chính để quan sát đưọc kiến trúc tổng quan của cấu trúc dữ liệu.)
- ```struct ofproto```: biểu diễn một OpenFlow switch (ovs bridge), tất cả các hoạt động của flow/port được thực hiện trên ofproto

![](images/2-OVS-Architecture/ofproto1.png)

- ```struct ofport```: biểu diễn một port trong một ofprotp

![](images/2-OVS-Architecture/ofport.png)

- ```struct rule```: biểu diễn một OpenFlow flow (instruction) trong một ofproto

![](images/2-OVS-Architecture/rule.png)

- ```struct ofgroup```: biểu diễn một group OpenFlow phiên bản 1.1+ trong một ofproto

![](images/2-OVS-Architecture/ofgroup.png)

### 2.2. ofproto-provider
Mỗi thực thi (implementation) ofproto (ovs bridge) cần phải định nghĩa một cấu trúc ofproto_class để tạo ra một **ofproto-provider**. **ofproto** sử dụng **ofproto-provider** để trực tiếp quản lý và điều khiển một OpenFlow switch. ```struct ofproto_class``` trong ```ofproto/ofproto-provider.h```, định nghĩa các interface để thực thi một ofproto-provider cho phần cứng hoặc phần mềm mới. 

![](images/2-OVS-Architecture/ofproto_class.png)

Open vSwitch có một built-in ofproto-provider gọi là **ofproto-dpif**, nó được xây dựng trên đỉnh của thư viện **dpif**(thư viện **dpif** dùng để thao tác với datapath). Tương tự như **ofproto**, **dpif** cũng "ủy quyền" cho **dpif-provider** để thực hiện các chức năng quản lý. Cụ thể như sau: 

![](images/2-OVS-Architecture/ofproto_providers.png)

Một datapath là một bảng (lưu lại các) flow, nó chỉ phục vụ các exact-match flows. Khi một gói tin đến trên một thiết bị mạng, datapath thực hiện quá trình tìm kiếm matching flow. Nó thực thi các action trên các gói tin nhận được nếu các gói tin đó match với một flow đã tồn tại (specific flows). Nếu gói tin không khớp với bất cứ flow nào thì gói tin sẽ đưọc chuyển lên **ofproto-dpif**, nơi lưu giữ bảng OpenFlow đầy đủ (còn nhớ ở mục 1.1, ta đã nói rằng trong trường hợp không xảy ra matching, gói tin sẽ được chuyển lên **vswitchd**, vậy, **ofproto-dpif** là bộ phận chính xác mà ta đã đề cập tới). Nếu flow matching tại bảng này thành công thì **ofproto-dpif** sẽ thực hiện action tương ứng và thêm flow entry mới vào bảng flow của **dpif**. ( Nếu flow matching không xảy ra, **ofproto-dpif** sẽ gửi gói tin cho **ofproto** để chuyển đến OpenFlow Controller.)
Đến đây, ta có thể xây dựng lại sơ đồ kiến trúc đầy đủ hơn như sau:

![](images/2-OVS-Architecture/vswitchd-internal.png)

Như vậy, một OVS birdge quản lý 2 loại tài nguyên:
- forwarding plane mà nó quản lý (datapath)
- các thiết bị mạng (cả thiết bị vật lý và thiết bị ảo) gắn với nó (netdev) 
Cấu trúc dữ liệu chính:
- triển khai OVS bridge: **ofproto**, **ofproto-provider**
- quản lý datapath: **dpif**, **dpif-provider**
- quản lý các thiết bị mạng: **netdev**, **netdev-provider**
Ta đã có được một một bức tranh khá hoàn chỉnh về cách quản lý datapath của **vswitchd**. Phần tiếp theo, ta sẽ tìm hiểu về chức năng quản lý các thiết bị mạng (**netdev** và **netdev-provider**).

### 2.2. netdev
**netdev** là một thư viện được định nghĩa trong ```lib/netdev-provider.h```, được thực thi trong ```lib/netdev.c```, **netdev** trừu tượng hóa (abstract) tương tác với các thiết bị mạng (qua các giao diện là Ethernet).
Mỗi cổng trên một switch phải có một netdev tương ứng và phải hỗ trợ tối thiểu một vài thao tác, chẳng hạn như khả năng đọc MTU (Maximum Transmission Unit) của netdev, nhận được số lượng của hàng đợi RX và TX.

### 2.3. netdev-provider
**netdev-provider** triển khai giao diện hệ điều hành và phần cứng cụ thể cho các "thiết bị mạng", ví dụ: eth0 trên Linux. OVS phải có khả năng mở mỗi cổng trên một switch như một netdev, vì vậy ta sẽ cần phải thực hiện một **netdev-provider** hoạt động với switch cứng và mềm.

![](images/2-OVS-Architecture/netdev_providers.png)

```struct netdev_class```, trong ```lib/netdev-provider.h```, định nghĩa các giao diện cần thiết để thực thi một netdev.

![](images/2-OVS-Architecture/netdev_class.png)

Các loại netdev được định nghĩa gồm có:
- linux netdev (```lib/netdev-linux.c``` cho platform linux)
- bsd netdev (```lib/netdev-bsd.c``` cho platform bsd)
- windows netdev (```lib/netdev-window.c``` cho platform window)
- dummy netdev (```lib/netdev-dummy.c```)
- vport netdev (```lib/netdev-vport.c```)
- dpdk netdev (```lib/netdev-dpdk.c```)

Ví dụ, ta muốn thử nghiệm chạy OVS trên DPDK, để xử lý gói tin hiệu năng cao trong userspace. Trong giải pháp này, kernel module của OVS sẽ được thay thế bằng các thành phần tương ứng trong DPDK. Điều đó có nghĩa là một netdev DPDK phải được thực hiện như là netdev provider cho platform này. Nhìn vào source code trong ```lib/netdev-dpdk.c```, ta có thể kiểm chứng điều này, trong đoạn cuối của code khởi tạo dpdk, nó tiến hành "đăng kí" (register) các class netdev provider:

![](images/2-OVS-Architecture/dpdk.png)

### 2.4. Call Flows
Entrypoint của ```vswitchd``` nằm ở ```vswitchd/ovs-vswitchd.c```.
Sơ đồ điều khiển logic của ```ovs-vswitchd``` được mô tả như sau:

![](images/2-OVS-Architecture/vswitch_flow_diagram.jpg)

- Khi bắt đầu, nó khởi tạo bridge module, được thực hiện trong ```vswitchd/bridge.c```. Module bridge sẽ lấy một số tham số cấu hình từ **ovsdb**. 
- ```ovs-vswitchd``` đi vào vòng lặp chính. Trong lần lặp đầu tiên của vòng lặp này, nó khởi tạo một số thư viện, bao gồm thư viện quan trọng nhất ```ofproto``` và ví dụ như DPDK (nếu được cấu hình). 
Lưu ý rằng các tài nguyên này chỉ cần khởi tạo một lần. 
- Mỗi datapath sẽ thực hiện công việc của mình bằng cách chạy ```ofproto_type_run()```, nó sẽ gọi vào kiểu thực thi ```type_run()``` cụ thể của kiểu dữ liệu đó. 
- Mỗi bridge sẽ thực hiện công việc của nó bằng cách chạy ```ofproto_run()```, nó sẽ gọi vào hàm ```run()``` cụ thể của class ofproto. 
- ```ovs-vswitchd``` sẽ xử lý các thông điệp IPC (JSON-RPC), từ dòng lệnh (```ovs-appctl```) và ```ovsdb-server```. 
- ```netdev_run()``` được gọi để xử lý tất cả các loại netdev khác nhau. 
- Sau khi tất cả các công việc trên được thực hiện, các mô-đun bridge, unixctl và netdev sẽ đi vào trạng thái block cho đến khi các tín hiệu mới kích hoạt. 

Pseudo code tương ứng được hiển thị bên dưới:

![](images/2-OVS-Architecture/example.png)

Ta sẽ tìm hiểu một số procedures quan trọng.

## <a name="ovsdb"></a> 3. OVSDB		// TODO
## <a name="datapath"></a> 4. Datapath 	// TODO
