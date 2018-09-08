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

```struct ofproto```