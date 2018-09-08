# Tìm hiểu về Nova/Compute

## Mục lục

* [1. Nova overview](#1)
* [2. Nova achitecture](#2)
* [3. Virtual machine creation workflow](#3)



<a name="1"></a>

# 1. Nova overview

- Openstack Compute được sử dụng để quản lý máy ảo trong cloud computing. Openstack Compute là một thành phần chính của hệ thống IaaS.
- Openstack Compute tương tác với Openstack Identity để xác thực. Openstack Image service for disk and server images to launch instances, Openstack Dashboard cung cấp giao diện người dùng cho người sử dụng. Image bị giới hạn bởi từng project và user, quotas bị giới hạn trong mỗi project
- Nova có trách nhiệm quản lý hoạt động của instance như: tạo, lập lịch cũng như ngưng hoạt động của các VM


<a name="2"></a>

# 2. Nova architecture

![Imgur](https://i.imgur.com/mvhlqms.png)




This complicated diagram có thể chia ra thành 3 phần:
* End users, người muốn sử dụng NOva để create compute instances, nó gọi đến *nova-api* cùng với Openstack API or EC2 API requests
* Nova daemons trao đổi thông tin qua hàng đợi queue (actions) và database (information) để mang theo các API requests
* Glance is a completed separate service that Nova interfaces qua Glance API để cung cấp virtual disk image service


* API
*nova-api* là sự sống của Nova. Để accept và xử lý các API request, *nova-api* cung cấp endpoints cho tất cả API queries, initiates most of the orchestation activities như running an instance hoặc thiết lập một số chính sách policy như *quota check*.
Với một vài request, API server sẽ thực hiện bằng cách truy vấn database và trả về reply. Với một số complicated requests, API server sẽ chuyển các massage tới các daemons other để xử lý chúng
Mặc định, *nova-api* listens on port 8733 for EC2 API và 8744 for the Openstack API



* Scheduler
*nova-scheduler* xử lý các request trong hàng đợi queue và xác định compute host để run virtual machine. Việc xác định compute host này gặp nhiều khó khăn trong thực tế, vì nó cần phải biết rõ trạng thái hiện tại của hạ tầng cloud và các thuật toán phức tạp mà nó sử dụng. 

Bảng sau thể hiện một số lựa chọn về scheduler:


| Scheduler | Notes                                              |
| ----------|:--------------------------------------------------:|
| Simple    | Attempts to find least loaded host                 |
| Chance    | Chooses random availabe host from service table    |
| Zone      | Picks random host from within an availability zone |


* Compute Worker
*nova-compute* quản lý các tài nguyên tính toán trên Compute host. Ví dụ, *nova-compute* accept message từ queue nhằm tao một VM, sau đó sử dụng *libvirt* library để start a new KVM instance
Có một vài phương pháp để *nova-compute* có thể quản lý virtual machine. Phương pháp phổ biến nhất là dùng *libvirt*, hoặc có thể sử dụng Xen API, vSphere API, Window Management Interface

* Volume worker
nova-volume quản lý việc create, attaching, detaching volumes to compute instances


* Network Worker
nova-network tương tự như nova-compute và nova-volume. Nova định nghĩa hai loại IP address cho instances là: fix IPs và Floating IPs. Có thể hình dung là fix IPs giống như private IP còn floating IPs là public IP. Floating IPs tự động allocate and associate to a domain nhằm thiết lập kết nối ra bên ngoài


* Queue
queue cung cấp central hub for passing messages between daemons như compute nodes, networking controllers, API endpoints...


* Database
Database lưu trữ các file cấu hình cho hệ thống cloud. Nó gồm instance types mà đang sẵn sàng sử dụng, network available and project
Ví dụ, database chứa một số thông tin như: migrate_version, migrations, auth_tokens, netwroks...



<a name="3"></a>

# Virtual machine creation workflow

