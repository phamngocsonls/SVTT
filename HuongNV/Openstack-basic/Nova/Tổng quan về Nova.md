# Tìm hiểu về Nova/Compute

## Mục lục

* [1. Giới thiệu Nova](#1)
* [2. Nova achitecture](#2)
* [3. Virtual machine creation workflow](#3)
    * [3.1 Các thành phần tham gia trong quá trình khởi tạo Virtual machine](#31)
    * [3.2 Luồng khởi tạo Virtual machine](#32)



<a name="1"></a>

# 1. Giới thiệu Nova

- Openstack Compute được sử dụng để quản lý máy ảo trong cloud computing. Openstack Compute là một thành phần chính của hệ thống IaaS.
- Openstack Compute tương tác với Openstack Identity để xác thực. Openstack Image service for disk and server images to launch instances, Openstack Dashboard cung cấp giao diện người dùng cho người sử dụng. Image bị giới hạn bởi từng project và user, quotas bị giới hạn trong mỗi project
- Nova có trách nhiệm quản lý hoạt động của instance như: tạo, lập lịch cũng như ngưng hoạt động của các VM


<a name="2"></a>

# 2. Các thành phần trong Nova

![Imgur](https://i.imgur.com/mvhlqms.png)

Biểu đồ sau chỉ ra các thành phần trong Openstack Compute:
* End users, người muốn sử dụng Nova để create compute instances, nó gọi đến *nova-api* cùng với Openstack API or EC2 API requests
* Nova daemons trao đổi thông tin qua hàng đợi queue (actions) và database (information) để mang theo các API requests
* Glance is a completed separate service that Nova interfaces qua Glance API để cung cấp virtual disk image service

* **nova-api**: 
    - Là sự sống của Nova. Để accept và xử lý các API request, *nova-api* cung cấp endpoints cho tất cả API queries, initiates most of the orchestation activities như running an instance hoặc thiết lập một số chính sách policy như *quota check*.
    - Mặc định, *nova-api* listens on port 8733 for EC2 API và 8744 for the Openstack API



* **Scheduler:**
*nova-scheduler* xử lý các request trong hàng đợi queue và xác định compute host để run virtual machine. Việc xác định compute host này gặp nhiều khó khăn trong thực tế, vì nó cần phải biết rõ trạng thái hiện tại của hạ tầng cloud và các thuật toán phức tạp mà nó sử dụng. 


* **Compute Worker:**
    - *nova-compute* quản lý các tài nguyên tính toán trên Compute host. Ví dụ, *nova-compute* accept message từ queue nhằm tao một VM, sau đó sử dụng *libvirt* library để start a new KVM instance
    - Có một vài phương pháp để *nova-compute* có thể quản lý virtual machine. Phương pháp phổ biến nhất là dùng *libvirt*, hoặc có thể sử dụng Xen API, vSphere API, Window Management Interface

* **Volume worker:**
nova-volume quản lý việc create, attaching, detaching volumes to compute instances


* **Network Worker:**
nova-network tương tự như nova-compute và nova-volume. Nova định nghĩa hai loại IP address cho instances là: fix IPs và Floating IPs. Có thể hình dung là fix IPs giống như private IP còn floating IPs là public IP. Floating IPs tự động allocate and associate to a domain nhằm thiết lập kết nối ra bên ngoài


* **Queue:**
Trung tâm trung chuyển các thông điệp giữa các daemons. Thường sử dụng RabbitMQ, cũng có thể thực hiện một AMQP message queue khác là ZeroMQ.


* **Database:**
    - Database lưu trữ các file cấu hình cho hệ thống cloud. Nó gồm instance types mà đang sẵn sàng sử dụng, network available and project
    - Ví dụ, database chứa một số thông tin như: migrate_version, migrations, auth_tokens, netwroks...


<a name="3"></a>

# 3. Virtual machine creation workflow

Sơ đồ dưới đây miểu tả Request Flow for Provisioning Insstance in Openstack


![Imgur](https://i.imgur.com/xR8Lmyj.png)


<a name="31"></a>

## 3.1 Các thành phần tham gia trong quá trình khởi tạo Virtual machine

* **CLI**: Command line dòng lệnh trong Openstack Compute
* **Dashboard**: Cung cấp giao diện web cho người sử dụng
* **Compute**: Truy xuất virtual disk images(Glance), attach flow flavor và metadata tới end user API
* **Network**: Cung cấp virtual networking cho các VM trong Compute có theeg giao tiếp với nhau và đi ra ngoài Internet
* **Block Storage**: Cung cấp persistent storage volume cho Compute servcies
* **Image**: Lưu giữ virtual disk file
* **Identity**: Cung cấp tính xác thực và ủy quyền cho tất cả các dịch vụ trong Openstack
* **Message Queue(RabbitMQ)**: Thực hiện các giao tiếp giữa các components trong Openstack như Nova, Neutron, Cinder


<a name="32"></a>

## 3.2 Luồng khởi tạo Virtual machine

1. **Dashboard or CLI**: Nhận thông tin người dùng và thực hiện REST call chuyển tới Keystone để xác thực
2. **Keystone**: Xác thực thông tin người dùng, tạo ra và gửi token tới end user để có thể request tới các thành phần khác bằng REST call
3. **Dashboard or CLI**: Chuyển đổi request cụ thể như `launch instance` or `nova-boot`  tới `nova-api`
4. **nova-api**: Nhận request và gửi lời request kèm theo tính xác thực của token và quyền hạn của người dùng đó tới keystone
5. **Keystone**: Xác thực token và gửi các updated auth headers với roles avf quyền hạn permissions
6. **nova-api**: Tương tác với `nova-database`
7. Database tạo ra entry lưu thông tin về new instance
8. **nova-api**: Gửi `rpc.call` request tới `nova-scheduler` để cập nhật instance với host ID cụ thể
9. **nova-scheduler**: Lấy các request từ `queue`
10. **nova-scheduler**: Thao tác với `nova-database` để tìm host muốn launch instance
11. Trả về tin updated với ID của host Compute
12. **nova-scheduler**: Gửi `rpc.cast` request tới `nova-compute` để có thể launch instance trên host ID đã xác định
13. **nova-compute**: Lấy các request từ queue
14. **nova-compute**: Gửi `rpc.call` request tới `nova-conductor` để lấy thông tin về instance như host ID, flavor (RAM, CPU, Disk)
15. **nova-conductor**: Lấy các request từ queue
16. **nova-conductor**: Thao tác với `nova-database`
17. Trả về instance information
18. **nova-compute**: Lấy thông tin về instance từ queue
19. **nova-compute**: Thực hiện REST call kèm theo auth-token tới `glance-api` để lấy Image URL với Image ID và upload Image từ image store
20. **glance-api**: Xác thực với keystone
21. **nova-compute**: Get the image metadata
22. **nova-compute**: Thực hiện REST call kèm theo auth-token tới `Network API` để cung cấp và config network cho instance
23. **quantum-server**: Xác thực auth-token với keystone
24. **nova-compute**: Lấy thông tin về network
25. **nova-compute**: REST call được gọi đến gửi auth-token tới `Volume API` nhằm attach volumes tới instance
26. **cinder-api**: chứng thực auth-token với keystone
27. **nova-compute**: Lấy thông tin từ block storage
28. **nova-compute**: Tạo data cho hypervisor drivervà tạo máy ảo virtual machine trên Hypervisor(qua libvirt or api)
