# Một vài tìm hiểu về Keystone

## Mục lục

* [1. Giới thiệu Keystone](#1)
* [2. Một số chức năng của Keystone](#2)
* [3. Lợi ích của Keystone](#3)


<a name="1"></a>

# 1. Giới thiệu về Keystone

Keystone hay còn gọi là Openstack identity, là dịch vụ được phát triển nhằm xác thực người dùng và quyền hạn của người dùng đó trong môi cloud Openstack. Keystone cung cấp cho chúng ta một mã xác thực hay còn gọi là `token` để cho phép `user` truy cập và sử dụng các dịch vụ trong môi trường cloud.


![Imgur](https://i.imgur.com/fCGE307.png)


<a name="2"></a>

# 2.Một số chức năng của Keystone

* Identity: 
    * `Identity` nhằm xác định rằng ai đang truy cập vào hệ thống cloud hay cụ thể là người dùng nào đang muốn truy cập vào hệ thống. 
    * Trong môi trường thử nghiệm thì danh tính người dùng có thể được lưu trong cơ sở dữ liệu của Keystone
    * Trong môi trường production, có thể có một phương pháp xác thực thứ 3 nào đó nhằm năng cao tính bảo mật cho hệ thống.


* Authentication: Xác thực người dùng
    * Xác định danh tính người dùng với username và password. Trong môi trường production thì không khuyến khích dùng password vì nó dễ dàng bị đánh cắp qua Internet. Giải pháp ở đây là ta sẽ dùng một mã code hay còn gọi là `token`. Token có tính an toàn hơn và nó có sự giới hạn về thời gian sử dụng khi được cung cấp cho user. 

* Access Management (Authorization): Quản lý truy cập
    * Qúa trình xác thực hoàn tất, người dùng có thể truy cập và sử dung nguồn tài nguyên mà hệ thống cung cấp nhưng quyền hạn bị kiểm soát bởi hệ thống. Ví dụ khi user muốn tạo, sửa hoặc xóa 1 `virtual machine` thì Keystone sẽ kiểm tra rằng user đó có các quyền đó hay không. 
    * Trong Openstack, Keystone ánh xạ các user tới các project và domain thông qua các role mà hệ thống đã gán cho người dùng. 


<a name="3"></a>

# 3. Lợi ích của Keystone

* Quản lý thông tin người dùng, bao gồm user và password. Mỗi user sẽ được map tới từng dịch vụ cụ thể nào đó.
* Keystone cung cấp các registry để chưa các project nhằm tách biệt các nguồn tài nguyên trong hệ thống như server, images...
* A registry role được sử dụng được sử dụng để ủy quyền giữa Keystone và các file thiết lập `policy` cho từng dịch vụ
* Một danh mục lưu trữ các Openstack service, các endpoints, regions, cho phép các user truy cập và sử dụng nó.
