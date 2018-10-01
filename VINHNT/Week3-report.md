---
---

## MỤC LỤC



## Nội dung

### 1. Các Sevices chính của Ceph

Ceph cung cấp 4 giao diện khác nhau, mỗi một thiết kế cho một kiểu trường hợp sử dụng (úe case) khác nhau.

#### 1.1 RADOS Block Device (RBD)

RBD biểu diễn một block lưu trữ với các ổ đĩa truyền thống HDD/SSD, các ứng dụng có thể sử dụng với một ít hoặc không có một sự điều chỉnh nào. RBD là vốn dĩ có sẵn tự nhiên cho nhiều máy chủ trên mạng.

Khi có thể xây dựng một hệ thống filesystem trực tiếp trên RBD. thường là một máy ảo trong trường hợp hypervisor là client của RBD service và biểu diễn volume tới guest operating system thông qua [virtio](Notes.md/#virtio) hoặc emulation driver. Một cách khác bao gồm trực tiếp raw sử dụng bằng cơ sở dữ liệu, tham gia trực tiếp tới một phần vật lý hay qua máy ảo thông qua một kernel driver. Một số người sử dụng tìm gía trị sử dụng trong việc xây dựng một ổ đĩa vật lý trong hệ điều hành của họ trên đỉnh của nhiều ổ RBD để đạt được hiệu suất hay mục tiêu mở rộng.

Block storage là thích hợp khi mà một disk-like resource là được mong muốn và cung cấp hiệu suất và latency đáng tin cậy. Dung lưọng được cung cấp một cách riêng lẻ, chunk rời rạc do đó scaling up, down có thể bất tiện và khó khăn do đó một ứng dụng với một lưọng dữ liệu biến lớn, sự thay đổi biên độ lớn thíc hợp với model object storage hơn.

RBD volume hoạt động bao gồm các việc đọc ghi dữ liệu cũng như tạo hay xóa. khả năng sao chép dữ liệu của RBD volumes giữa các cluster đáp ứng high availability và disaster recovery.

RBD volume thường được sử dụng trong suốt bằng máy ảo và trừu tượng, bao gồm openStack cinder và Glance. tuy nhiên các người dùng và ứng dụng có thể khai thác chúng cũng thông qua rbd command line và lập trình một các tự động thông qua librbd.

Ví dụ usecase: một người dùng muốn triển khai một hệ thống  yum repo mirrors trong khoảng thời gian OpenStack clouds cho người thuê sử dụng. CPU và RAM yêu cầu thấp. Nhưng lưọng trung bình lưu trữ là cần thiết để phản ánh bộ sưu tập ngày càng tăng rpm và metadata files cho nhiều phiên bản của 2 phân phối linux

### 1.2 RADOS Gateway (RGW)

RGW hỗ trợ đặc điểm của OpenStack Swift và Âmazon S3 service. Khi sử dụng thì RGW tận dụng một hoặc nhiều pool chuyên dụng và không truy cập được RBD volumes hoặc các kiểu dữ liệu khác mà có trong cluster. RGW được cung cấp RÉSTfully với giao thức HTTP/HTTPS quen thuộc.

Ceph RGW service có thể ở trên cùng cac server như là một OSD và thiết bị của chúng trong một kiến trúc hội tụ. Tuy nhiên là phổ biến hơn là phân biệt riêng rẽ các server thậm chí là các máy ảo đối với RGW service. Các môi trường với mức sử dụng nhẹ có thể colocate chúng với MON daemon trên một Ceph server vật lý nhưng khó thực hiện

Điển hình, sử dụng **haproxy** hoặc một gỉai pháp cân bằng tải khác có thể kết hợp với **keepalived** để tạo ra một dịch vụ có tính cân bằng tải và high availability qua nhiều RGW instances. Số lưọng RGW có thể scale up dơn theo như lượng công việc mà nó yêu cầu một các độc lập của nguồn tài nguyên từ Ceph khác bao gồm ÓSD và MON. Tính linh hoạt này là một trong những thuận lợi nổi bật nhất của Ceph so với các gỉai pháp lưu trũ truyền thống, bao gồm các ứng dụng. 

RGW được cung cấp một daemon riêng biệt để tương tác với cluster. kết hợp với Apache/http nhu một client frontend.

Object storage thì không có các tính chất latency và predictable performance nhưng dung lượng có thể scale up, down một cách dễ dàng.

Usecase tiềm năng có thể là một loạt webserver sử dụng một **Conten Management System CMS** ddeer lưu trữ một mix không có cấu trúc giữa HTML, JavaScript, image, và nhiều nội dung khác có thể phát triển.

### 1.3 CephFS

Use case đầu tiên là lưu trữ back-end ceph. CephFS có giống vơi NFS tuy nhiên không hoàn toàn. thậm chí có thể chạy NFS trên top của CephFS. CephFS được thiết kế dùng vào well-behaved server, và không dự định là được mount vào user desktop. có thể vận hành driver kernel hệ thống để mount CephFS như là một local device hoặc Gluster network filesystem. cũng có thể sử dụng FUSE driver dễ update hơn nhưng hiệu suất kém hơn.

Client mount là trực tiếp tới Cluster's Ceph servers, nhưng CephFS yêu cầu một hoặc nhiều MDS instance để lưu trữ tên file, thư mục, và các metadata truyền thống khác, cũng như quản lý truy cập tới Ceph's ÓSD. Vì với RGW server, các cài đặt nhỏ và được sử dụng nhẹ có thể chọn chạy các trình tiện ích MDS trên các máy ảo, mặc dù hầu hết sẽ chọn các máy chủ vật lý chuyên dụng, hiệu suất ổn định và quản lý phụ thuộc đơn giản.

Use case tiềm năng là thiết lập một hệ thống lưu trữ xây dựng xung quanh một fileserver cũ mà yêu cầu POSIX filesystem permission va behavior. fileserver kế thừa có thể được thay thế bằng CephFS mount với một chút hoặc không sự điều chỉnh nào.

### 1.4 Librados

Librados là một nền tảng cho các ceph service. Nó cũng có thể cho app tương tác trực tiếp với RADOS trong cách cách không lý tưởng với RBD, RGW, CephFS. tuy nhiên muốn khai thác khả năng mở rộng, networking, và bảo vệ dữ liệu thì nên sử dung các dịch vụ trước đó. 

Use case tiềm năng là Vaultaire Time Series Database (TSDB). Vaultaire là mô tả như một massively scalable metrics database. 

## 2. Ceph-deploy toolkit - Tạo một Ceph cluster đơn giản.

- 1 admin node
- 1 monintor 
- 3 OSD      

cấu hình mạng:

192.168.1.25 adminNode
192.168.1.26 node1
192.168.1.27 node2
192.168.1.28 node3
192.168.1.29 node4