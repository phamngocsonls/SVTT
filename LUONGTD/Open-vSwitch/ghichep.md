# General
## [A. Linux Basic](#linuxbasic)
---
## <a name="linuxbasic"><>/a A. Linux Basic
### 1. Linux Architecture

![](images/ghichep/linux_architecture.jpg)

Kiến trúc hệ thống Linux bao gồm 4 tầng chính:
- Tầng **Application**: vòng tròn ngoài cùng, bao gồm các chương trình người dùng, compiler và các tiện ích hệ thống (vi, cd, grep, date,...)
- Tầng **Shell**: Shell là một chương trình thông dịch, có tác dụng dịch các user request thành các chương trình thực thi dưới kernel và trả về kết quả cho user. Shell nhận request từ stdin, xuất kết quả ra stdout và stderr, thể hiện qua màn hình terminal vì thế còn gọi là **CLI-Command Line Interfaces**. Như trên hình có **vi**, **cd**, **grep** hay **date** là các chương trình shell.
- Tầng **Kernel**: Là tầng làm nhiệm vụ quản lý các tác vụ, quản lý bộ nhớ, quản lý hệ thống file, quản lý hardware,...

![](images/ghichep/linux_kernel.jpg) 

- Tầng **hardware**: gồm tất cả các thành phần phần cứng như CPU, GPU, Memory, I/O,...

### 2. User space and Kernel space
- Tầng Application và Shell được gọi chung là user space, vì nó tương tác trực tiếp với user
- Tầng Kernel được gọi là Kernel space

### 3. Các thành phần Software
Hệ thống nhúng Linux có 3 thành phần software chính được biểu diễn như sau:

![](images/ghichep/software.png)

1. **Bootloader**: Bootloader được đặt ở phân vùng đầu tiên của MBR - Master Boot Record, có tác dụng khởi chạy một số thành phần phần cứng, load và chạy Kernel. Các thông số cài đặt cách mà Bootloader khởi chạy kernel được đặt trong Boot parameters.

![](images/ghichep/soft2.png)

Với máy tính Linux thì Bootloader thường thấy nhất là GRUB.

![](images/ghichep/software1.png)

2. **Kernel**: Kernel là nhân hệ điều hành, có tác dụng quản lý tác vụ, lập lịch, quản lý memory, quản lý hardware, ...
- Các thành phần kernel bao gồm:
	- uImage hoặc zImage (tùy kiểu nén): gồm nhân hệ điều hành và các thành phần gọi là module được build và tích hợp vào kernel (gọi là build-in, các module này được khởi tạo cùng kernel)
	- Các module khác không được tích hợp sẫn vào kernel, chỉ được load khi user muốn
Module là các khối thực hiện một chức năng nào đó, hoặc có thể là một driver của một thiết bị ngoại vi nào đó.
Kernel Linux được thiết kế theo dạng module nên user có thể tự phát triển các module và tích hợp sâu vào hệ thống.

3. **Root Filesystem**
Root File System - Rootfs là hệ thống file, thể hiện một cách trực quan nhất với người dùng. Tất cả các file, các thư mục bạn duyệt qua đều nằm trong Rootfs.
Cấu trúc hệ thống Rootfs trên PC:

![](images/ghichep/hierarchy.jpg)

### 4. Library
Thư viện là thành phần quan trọng đối với bất kì hệ điều hành nào, chúng là một tập hợp các function được viết sẵn để tái sử dụng trong nhiều chương trình khác nhau. 

![](images/ghichep/gnu-lib.jpg)

Trong Root File System, lib được đưa vào các thư mục:
- /lib
- /usr/lib
- /usr/local/lib
1. **Phân loại**:
**Static Libraries**:
- Có đuôi mở rộng .a
- Các function trong lib được đưa vào trực tiếp trong app source (gọi là linked) trong lúc compile source, vì thế khi chạy app (run time) có thể  chạy độc lập mà không cần thiết một liên kết nào đến lib nữa.

**Shared Libraries**:
- Có đuôi mở rộng là .so
- Được chia nhỏ thành hai loại nữa là:
	- Dynamic linking: Các function không được đưa trực tiếp vào app source mà chỉ là tham chiếu, khi chạy app thì cần có một môi trường liên kết đến lib để app có thể tìm kiếm và khởi chạy các function đó trong lib theo thời gian.
	- Dynamic loading:  

# Handout for week1
---
## 0.0 OVS:
- Wireless base stations generally only allow packets with the source MAC address of NIC that completed the initial handshake. Therefore, without MAC rewriting, only a single device can  communicate over a single wireless link.
This isn't specific to Open vSwitch, it's enforced by the access point, so the same problems will show up with the Linux bridge or any other way to do bridging. 

# Handout for week2
---
## 0.0. daemon
- Daemon là chương trình chạy nền giống như các service trên Window, có thể tắt mở tự động mà không ảnh hưởng đến giao diện người dùng. Các daemon process thường gặp như là web server hay là database.

## 0.1. kernel
- Kernel là khái niệm chỉ những phần mềm, ứng dụng mức thấp (low-level) trong hệ thống, có khả năng thay đổi linh hoạt để phù hợp với phần cứng. Chúng tương tác với tất cả các ứng dụng và hoạt động trong chế độ usermode, cho phép các quá trình khác - hay còn gọi là server, nhận thông tin từ các thành phần khác qua Inter-Process-Communication (IPC).
- Các file kernel này, trong Ubuntu chúng đưọc lưu trữ tại thư mục /boot/ và đặt tên theo vmlinuz-version. Khi bộ nhớ ảo bắt đầu được phát triển để thực hiện các tác vụ đa luồng, tiền tố vm sẽ được đặt vào đầu các file kernel để phân biệt khả năng hỗ trợ công nghệ ảo hóa. Kể từ đó, Linux kernel được gọi là vmlinux, nhưng hệ thống kernel này đã phát triển quá nhanh, lớn hơn so với dung lượng bộ nhớ boot chuẩn của hệ điều hành, vì vậy những kernel này đã được nén theo chuẩn zlib,... chúng được gọi chung là zImage.

## 0.2. Socket
- Một socket là một điểm cuối của một giao tiếp 2 chiều giữa hai chương trình chạy trên mạng. Socket được ràng buộc với một cổng (1 số cụ thể) để các tầng TCP có thể định danh ứng dụng mà dữ liệu sẽ được gửi tới. 
- Minh họa:
	- Server side: Thông thường một chương trình server chạy trên một máy tính cụ thể, chương trình này có một socket (Server Socket), socket được "ràng buộc" bởi một cổng (Port number) cụ thể. Các chương trình phục vụ (Server program) chỉ chờ đợi, lắng nghe tại Server Socket các client request để thực hiện một yêu cầu kết nối.
	- Client side: Các client biết tên máy của máy tính mà trên đó chương trình chủ (server) đang chạy và Port number mà chương trình chủ lắng nghe. Để thực hiện một yêu cầu kết nối, client cố gắng tạo ra "cuộc gọi" với máy chủ trên máy tính của chương trình chủ và cổng (ví dụ: ping). Các client cũng cần phải tự định danh chính nó với server (xác định một cổng đang trống để "gắn" với, cổng mà sẽ được sử dụng trong suốt quá trình kết nối này, thông thường hệ điều hành sẽ thực hiện chức năng gán cổng). 
	-  Nếu mọi việc suôn sẻ, chương trình chủ (server program) chấp nhận kết nối của clinet. Khi chấp nhận, máy chủ có một **socket mới** bị ràng buộc với local port của client. Thông tin đầu cuối (remote endpoint) của nó chính là địa chỉ và cổng của client. Nó đã tạo ra một socket mới để "chăm sóc" client và tiếp tục lắng nghe tại tại socket ban đầu (ServerSocket) cho các yêu cầu kết nối khác.
	- Về phía client, nếu kết nối đưọc chấp nhận, một socket sẽ đưọc tạo ra (thành công) và client có thể sử dụng socket để giao tiếp với chương trình trên server.
	- Các client và server có thể giao tiếp bằng cách ghi hay đọc từ socket của chúng. Dữ liệu ghi vào luồng đầu ra trên socket của client sẽ nhận đưọc trên luồng đầu vào của socket tại server và ngược lại.


// TODO:
## 0.4. Create makefile

## 0.5. DPDK

## 0.6. Datapath and kernel deep dive

## 0.7. Các công cụ chính tương tác với OVS

https://github.com/openvswitch/ovs/blob/master/Documentation/topics/porting.rst
