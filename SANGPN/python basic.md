# TÌM HIỂU PYTHON CƠ BẢN

# I. Tìm hiểu cơ bản:

## 1.1. Python cơ bản:

- Python là một ngôn ngữ lập trình bậc cao cho các mục đích lập trình đa năng, do Guido van Rossum tạo ra và lần đầu ra mắt vào năm 1991.

![](https://upload.wikimedia.org/wikipedia/en/d/d0/Guido-portrait-2014-curvves.jpg)

- Cú pháp của Python là khá dễ dàng để học và ngôn ngữ này cũng mạnh mẽ và linh hoạt không kém các ngôn ngữ khác trong việc phát triển các ứng dụng. Python hỗ trợ mẫu đa lập trình, bao gồm lập trình hướng đối tượng, lập trình hàm và mệnh lệnh hoặc là các phong cách lập trình theo thủ tục…

## 1.2. Các đặc điểm của Python:

- Đẹp đẽ tốt hơn xấu xí.
- Minh bạch tốt hơn che đậy.
- Đơn giản tốt hơn phức tạp.
- Phức tạp tốt hơn rắc rối.
- Dễ đọc.

## 1.3. Cú pháp cơ bản:

### 1.3.1. Các từ khóa trong Python:

- and, assert, break, class, continue, def, del, elif, else, except, exec, finally, for, from, global, if, import, in, is, lambda, not, or, pass, print, raise, return, try, while, with, yield.

### 1.3.2. Khối lệnh:

- Các khối code trong Python được nhận biết bởi độ thụt dòng code (indentation) trong Python và đây là điều bắt buộc.
- Số khoảng trống trong độ thụt dòng là biến đổi, nhưng tất cả các lệnh bên trong khối phải được thụt cùng một số lượng khoảng trống như nhau.

### 1.3.3. Lệnh trên nhiều dòng, trích dẫn, comment:

- Sử dụng ký tự \ để chỉ rõ sự liên tục dòng.
- Có trích dẫn đơn (&#39;), kép (&quot;) và trích dẫn tam (&#39;&#39;&#39;), các trích dẫn này miễn là có cùng kiểu mở và đóng.
- Trong Python, một dấu #, mà không ở bên trong một hằng chuỗi nào, là bắt đầu một comment đơn dòng.

### 1.3.4. Toán tử:

- Trong Python, các toán tử cũng giống như các toán tử ở C/C++, ngoài ra còn có một số toán tử khác như là:  // (chia lấy phần nguyên), \*\* (mũ)…

### 1.3.5. Cấu trúc rẽ nhánh và lặp:

- Cấu trúc rẽ nhánh:
  - if điều\_kiện:
        lệnh
  - if điều\_kiện:
        lệnh
else:
        lệnh
  - if điều\_kiện\_1:
        lệnh1 (điều\_kiện\_1 đúng)
elif điều\_kiện\_2:
        lệnh2 (điều\_kiện\_1 sai và điều\_kiện\_2 đúng)
else:
        lệnh3
- Cấu trúc lặp: Cũng giống như C/C++, Python cung cấp cho bạn các kiểu vòng lặp như vòng lặp while, vòng lặp for, cấu trúc lồng vòng lặp. Bên cạnh đó, để hỗ trợ cho trình thực thi của vòng lặp, Python cũng hỗ trợ một số lệnh điều khiển vòng lặp như lệnh break, lệnh continue và lệnh pass.

# II. Một số ví dụ:

## 2.1. Chương trình cơ bản:

- Chương trình in ra màn hình đơn giản:

![](https://i.imgur.com/7gl5hwQ.png)

- Chương trình in ra màn hình host name và IP của máy đang dùng:

![](https://i.imgur.com/o3ccxs2.png)

- Tính diện tích tam giác biết độ dài 3 cạnh:

![](https://i.imgur.com/v9Q5wSG.png)

## 2.2. Socket trong Python:

- Socket là các endpoint của một kênh giao tiếp hai chiều.
- Các Socket có thể giao tiếp bên trong một tiến trình, giữa các tiến trình trên cùng một thiết bị...
- Module socket trong Python sẽ giúp chúng ta thực hiện các kết nối cần thiết. Để sử dụng socket trong Python, ta cần phải import module socket vào chương trình (import socket).
- Khởi tạo socket: **socket.socket(AddressFamily, socketType, Protocol)**
Trong đó:
        socket\_family: AF\_UNIX,  AF\_INET hoặc AF\_INET6.
        socket\_type: SOCK\_STREAM (TCP) hoặc SOCK\_DGRAM (UDP).
        protocol: Thường được để trống, mặc định là 0.
- Các phương thức trong socket:
  - bind(address, port): Phương thức này gắn kết địa chỉ (address, port number) tới socket.
  - listen(backlog): Phương thức này thiết lập mở kết nối trên server, với tham số truyền vào là số kết nối được phép.
  - accept():Phương thức này chấp nhận một cách thụ động kết nối TCP Client, đợi cho tới khi kết nối tới.
  - connect(address): Phương thức này thiết lập một kết nối từ client đến server.
  - recv(bufsize, flag): Phương thức này dùng để nhận dữ liệu qua giao thức TCP.
  - send(byte,flag): Phương thức này gửi dữ liệu thông qua giao thức TCP.
  - recvfrom(bufsize, flag): Phương thức này dùng để nhận dữ liệu qua giao thức UDP.
  - sendto(bytes, address): Phương thức này dùng để gửi dữ liệu qua giao thức UDP.
  - close():Phương thức này dùng để đóng một kết nối.
