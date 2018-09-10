# Tìm hiểu về Glance

## Mục lục

* [1. Giới thiệu về Glance](#1)
* [2. Glance Achitecture](#2)
* [3. Glance Image Status]()
* [4. Disk format](#4)



<a name="1"></a>

# 1. Giới thiệu về Glance

- Glance là 1 thành phần quản lý image trong Openstack, nó là một component simple và very stable trong Openstack. Mục đích của Glance là lưu giữ image, khi cần ta sẽ có thể create VM 1 cách dễ dàng.
- Khi uplpad image trong Glance, nó sẽ chỉ rõ vị trí lưu trữ image cụ thể, mark the location, attributes và permissions in database. Khi sử dụng Nova để create VM, nó sẽ check location, permission và pull down image from Glance

![Imgur](https://i.imgur.com/T19T2vS.png)


<a name="2"></a>

# 2. Glance Architecture

- Openstack Glance has a client-server architecture that provides a REST API to the user through requests to the server
- A Glance Domain Controller manages hoạt động của internal server that is divided into layers. Từng tasks cụ thể được thực hiển bởi mỗi layer
- All the file operations được thực hiện tại `glance_store library`, nó chịu trách nhiệm thiết lập kết nối với eexternal storage back end và local filesystem. `glace_store library` cung cấp uniform interface to access the backend stores.
- Glance sử dụng central database (Glance DB), nó shared với tất cả các components in the system.


![Imgur](https://i.imgur.com/10CdZwC.png)


- Following components are present in the Glance architectute:
    * `A client`: bất kì application nào mà sử dụng Glance server
    * `REST API`: tiếp nhận và gửi request tới Glance
    * `Database Abstraction Layer(DAL)-an application programming interface`: API that unifies the comminicate giữa Glance và databases
    * `Glance Domain Controller-middleware that implements the main`: thực hiện một số chức năng như ủy quyền, thông báo, thiết lập các policies và database connections
    * `Glance Store-use to organize interations beetween Glance and various`: data stores
    * `Registry Layer-optical layer that is used to organize secure`: thiết lập kết nối giữa domain và DAL by using a separate service


<a name="3"></a>

# 3. Glance Image Status

Sơ đồ sau mô tả trạng thái của Image trong quá trình Upload:


![Imgur](https://i.imgur.com/n1WqbPX.png)


- queued
Image identifier được reversed for an imaged in the Glance registry. Không có image data nào được upload lên Glance, image size được set zero khi khởi tạo

- saving
Image raw data đang trong trạng thái upload lên Glance. Khi image được registered, no gọi đến phương thức POST/images và có *x-image-meta-location* header present

- uploading
Chỉ thị rằng import data-put call được thực hiện. Khi ở trang thái này, phương thức PUT/file is disallowed

- importing
Image đã được import nhưng chưa sẵn sàng sử dụng

- active 
Image đã được upload thành công lên Glance.

- deactivated
Việc access to image data is not allowed to any non-admin user

- killed
Hiển thị lỗi xảy ra trong quá tình upload image, image không sẵn sàng sử dụng

- deleted
Glance giữ lại thông tin về image, image không sẵn sàng được sử dụng, nó sẽ bị removed tự động vào 1 thời gian sau

- pending_delete
Giống như *deleted* state nhưng Glance sẽ không removed image dât, các image ở trạng thai này sẽ không thể phục hồi được


<a name=""4>></a>

# 4. Disk format

The disk format of a virtual machine image is the forrmat of the underlying disk image

- raw
Disk image format in an unstructured

- vhd
VHD disk format được sử dụng trong ảo hóa VMWare, Xen, Microsoft, VirtualBox

- vhdx
Phiên bản nâng cao của `vhd`, hỗ trợ larger disk sizes

- vdi
Disk format support by VirtualBox virtual machine và QEMU emulator

- iso
An format for the data contents of an typical disc

- qcow2
A disk format supported by QEMU
