# Tìm hiểu cơ bản về OpenStack

## Mục lục

* [1. Openstack là gì?](#1)
    * [1.1 Khái niệm](#1.1)
    * [1.2 Một số đặc điểm về Openstack](#1.2)
* [2. Các thành phần trong Openstack](#2)



<a name="1"></a>
# 1. Openstack là gì?

<a name="1.1"></a>

## 1.1 Khái niệm

Openstack là một platform điện toán đám mây nguồn mở hỗ trợ cả public cloud và private cloud. Nó cung cấp giải pháp xây dựng hạ tầng điện toán đám mây, có khả năng mở rộng và nhiều tính năng phong phú.

![Imgur](https://i.imgur.com/vWbSoOb.png)

<a name="1.2"></a>

## 1.2 Một số đặc điểm về Openstack

- Openstack được phát triển bởi NASA và Rackspace, phiên bản đầu tiên ra đời vào năm 2010. Định hướng của họ từ khi mới bắt đầu là tạo ra một dự án mã nguồn mở mà mọi người có thể sử dụng hoặc đóng góp.
- Openstack chuẩn Apache License 2.0, vì thế phiên bản đầu tiên đã phát triển rộng rãi trong cộng đồng với sự hỗ trợ bởi hơn 1200 công tác viên trên 130 quốc gia.
- Đên nay có rất nhiều phiên bản Openstack đã ra đời, kể đến như: Austin, Bexar, Cactus, Diablo, Essex, Folsom,Grizzly.... Các bản ra đời với chu kì 6 tháng 1 lần và tuần theo bảng chữ cái A B C...


<a name="2"></a>

# 2. Các thành phần chính trong Openstack

Openstack không phải là một dự án đơn lẻ mà là một nhóm các dự án mã nguồn mở nhằm mục đích cung cấp các dịch vụ cloud hoàn chỉnh. Openstack chứa nhiều thành phần như: Nova, Glance, Swift, Neutron, Cinder, Heat, Ceilometer

![Imgur](https://i.imgur.com/CXv81p5.png)

* Nova-Compute: module quản lý và cung cấp máy ảo. Nó hỗ trợ hiều hypervisors như KVM, QEMU, LXC, XenServer... Compute là một cung cụ mạnh mà có thể điều khiển toàn bộ các công việc: tạo, xóa bỏ máy ảo, security, access control. Bạn có thể điều khiển tất cả bằng lệnh hoặc từ giao diện dashboard trên web.

* Glance: là Openstack Imgae Service, quản lý các disk image ảo. Glance hỗ trợ các ảnh Raw, Hyper-V (VHD), VirtualBox (VDI), Qemu(qcow2), VMWare (VMDK, OVF)
    
* Keystone-Identity: quản lý xác thực cho user và projects

* Neutron-Networking: thành phần quản lý network cho các máy ảo. Cung cấp chức năng network as a service.

* Cinder: Là một Block Storage service trong Openstack. Nó thực thiết kế nhằm cho người dùng cuối và được sử dụng bởi project Nova-compute.

* Horizon-Dashboard: Là giao diện web mà qua đó ngườ dùng có thể thao tác trực tiếp như tạo máy ảo, xóa máy ảo... mà không cần thông qua dòng lệnh CLI.

