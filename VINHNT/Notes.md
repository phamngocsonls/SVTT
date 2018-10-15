---
title: Ghi chép các khái niệm
---

## Các khái niệm

<a name="object-storage"></a>

**Object-storage** (object-based storage) là một kiến trúc lưu trữ dữ liệu máy tính mà quản lý dữ liệu như là các objects.

Block-storage là một kiến trúc lưu trữ dữ liệu máy tính mà quản lý dữ liệu như các blocks bên trong sectors và tracks.

Filesystem cũng là một kiến trúc lưu trữ dữ liệu máy tính nhưng quản lý dữ liệu như một hệ thống cấp bậc các thư mục.

<a name="daemon"></a>

**Daemon** trong linux là một tiến trình chạy nền không chịu kiểm soát trực tiếp từ người dùng và có thể bật tắt mà không ảnh hưởng đến giao diện người dùng.

<a name="POSIX"></a>

**POSIX (The Portable Operating System Interface)** là tập các tiêu chuẩn duy trì khả năng tương thích giữa các hệ điều hành. POSIX định nghĩa các API cùng với các command shells và tiện ích cho phần mềm khả năng tương tác với các biến thể của Unix.

<a name="socket"></a>

**Socket** là một endpoint của liên kết giao tiếp hai chiều giữa 2 chương trình đang chạy trên mạng. Endpoint là một tổ hợp của một địa chỉ IP và một port

<a name="RADOS"></a>

**RADOS (Reliable Autonomic Distributed Object Store)** là dịch vụ lưu trữ object mã nguồn mở - một phần không thể thiếu trong hệ thống lưu trữ phân tán Ceph. RADOS có khả năng mở rộng đến hàng nghìn thiết bị phần cứng bằng việc sử dụng phần mềm quản lý chạy riêng biệt trên mỗi node lưu trữ. Cung cấp các đặc tính lưu trữ như: thin provisioning, snapshots và replication. Sử dụng thuật toán CRUSH để có thể sao chép và ánh xạ dữ liệu tới các node riêng lẻ.

<a name="thin-provisioned"></a>

**thin-provisioning** (TP) là phương thức tối ưu việc sử dụng hiệu quả không gian có sẵn được sử dụng trong storage area network. TP hoạt động bằng cách phân bổ không gian lưu trữ đĩa một cách linh hoạt giữa nhiều người dùng dựa vào việc tối thiểu hoá khoảng trống được yêu cầu từ mỗi user tại bất kỳ thời điểm nào (at any given time)

<a name="snapshots"></a>

**Snapshot** là tính năng bảo toàn trạng thái và có thể quay lại trạng thái tương tự nhiều lần. 
Đối với máy ảo snapshot captures toàn bộ trạng thái của máy ảo tại thời điểm snapshot bao gồm:
- Trạng thái tất cả ổ đĩa của máy ảo
- Nội dung bộ nhớ của máy ảo
- Cài đặt của máy ảo

<a name="amazons3"></a> 
**Amazon S3 - Amazon Simple Storage Service** là một dịch vụ web cloud computing được đề xuất bởi Amazon. Amazon S3 cung cấp **object storage** qua web services interfaces (REST, SOAP, và bitTorrent). Có thể dùng để lưu trữ và truy xuất dữ liệu tại bất kỳ thời điểm nào trên web.

<a name="openstack-swift"></a> 

<a name="disk-image"></a>

**Disk image** là một file máy tính bao gồm nội dung và cấu trúc của một ổ đĩa hoặc một thiết bị lưu trữ dữ liệu.

<a name="raid"></a>

**RAID (Redundant Array of Independent Disks)**: là một công nghệ ảo hóa lưu trữ dữ liệu kết hợp nhiều ổ đĩa vật lý thành một hoặc nhiều đơn vị lưu trữ logic cho mục đích *data redundancy (dữ liệu bổ sung phục vụ cho dữ liệu chính và cho phép sửa lỗi trong khi dữ liệu chính bị lỗi)* 

<a name="nfs"></a>

**Network File System (NFS)** là một distributed file system protocol (giao thức file system phân tán) cho phép user trên máy client có thể truy cập files trên một computer network (mạng máy tính) giống như việc truy cập một file local

<a name="virtio"></a>

**VirtIO - An I/O virtualization framework for linux** là một chuẩn ảo hóa cho các thiết bị mạng và đĩa cứng. Virtio làm cho máy ảo biết nó là máy ảo và vì thế sẽ hợp tác với trình ảo hóa để tăng tốc các thiết bị mạng và ổ cứng(bình thường nó chạy như một máy thật sử dụng các thiết bị ảo, các thiết bị này rất phức tạp, khiến cho tốc độ chậm)

<a name="san"></a>

**SAN - Storage Area Network** Có thể hiểu như là một phương pháp truy cập dữ liệu dựa trên nền tảng mạng mà quá trình truyền dữ liệu trên mạng tương tự như quá trình truyền dữ liệu từ các thiết bị quen thuộc trên máy chủ như Disks Drivers.

Trong một storage network máy chủ sử dụng một yêu cầu cho một gói dữ liệu cụ thể hay một dữ liệu cụ thể từ một đĩa lưu trữ và các yêu cầu được đáp ứng.Các thiết bị được làm vvieecj như một thiết bị lưu trữ bên trong máy chủ và được truy cập một cách bình thường thông qua các yêu cầu cụ thể và quá trình đáp ứng bằng cách gửi các yêu cầu và nhận được trên môi trường mạng.