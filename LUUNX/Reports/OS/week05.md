# Tìm Hiểu về Operating System

* Nguyễn Xuân Lưu

* Modern Operating System 4th

# 1.5 Operating System Concepts

## 1.5.1 Processes

Process là một khái niệm cơ bản của tất cả các hệ điều hành. Một Process là một chương trình được thực thi. Chúng được lưu trữ trong bộ nhớ.

## 1.5.2 Address Space

Mỗi máy tính có một bộ nhớ chính lưu giữ các chương trình được thực thi. Các chương trình có thể được thực thi đồng thời với nhau. Việc quản lý địa chỉ nhớ và bộ nhớ vật lý là một trong những công việc quan trọng của hệ điều hành

## 1.5.3 Files

Trên máy tính, dữ liệu ở bộ nhớ ngoài được lưu trữ và trừu tượng với khái niệm file. Chúng được tổ chức thành sơ đồ cây.

## 1.5.4 Input/ Output

Mỗi máy tính sẽ chứa các thiết bị vào ra. Hệ điều hành sẽ quản lý chúng.

## 1.5.5 Protection

Máy tính chứa rất nhiều thông tin của người dùng cần được bảo mật. Do vậy, mỗi file trong máy tính có một cơ chế đòi hỏi quyền truy cập hợp lệ mới có thể truy cập.

## 1.5.6 The Shell

Các hệ điều hành luôn cung cấp một shell để người dùng thực hiện các tác vụ khác nhau bên cạnh việc sử dụng giao diện đồ họa người dùng.

# 1.6 System Calls

Chúng ta đã biết hệ điều hành có hai nhiệm vụ chính: cung cấp sự trừu tượng cho chương trình ứng dụng người dùng và quản lý tài nguyên máy tính. Phần lớn những tương tác giữa chương trình người dùng và hệ điều hành sẽ yêu cầu các system call để thực hiện  các tác vụ với tài nguyên máy tính.

Cách thức để thực hiện system call của chương trình người dùng sẽ là cung cấp các tham số và loại system call và bộ nhớ, sau đó gọi lệnh Trap, hệ điều hành sẽ đọc dữ liệu yêu cầu, thực hiện yêu cầu và cuối cùng là trở về chương trình người dùng ban đầu.

Để thống nhất việc sử dụng system call, các hệ điều hành có nguồn gốc từ UNIX sử dụng một bộ các system call chuẩn hóa gọi là POSIX system call. Khi các chương trình người dùng sử dụng các POSIX system call cho yêu cầu tới hệ điều hành nơi chúng đang hoạt động thì sẽ được chấp nhận. Tức là một chương trình người dùng có thể tương thích với nhiều hệ điều hành, nếu chúng sử dụng POSIX system call và hệ điều hành ấy hỗ trợ.

Có khoảng 100 POSIX system call được phân vào 4 nhóm chức năng.

Nhóm thứ nhất là Process system call, các POSIX ở đây thực hiện nhiệm vụ liên quan đến tương tác giữa các process. Các lệnh ví dụ như fork, exit, execve, waitpid,...

Nhóm thứ hai là File Management, các POSIX ở đây thực hiện nhiệm vụ đọc ghi các file theo bytes. Điển hình như open, close, read, write, stat, lseek, ...

Nhóm thứ ba là Directory and File-system Management, các POSIX ở đây thực hiện nhiệm vụ quản lý các thư mục, mount/unmount và link file. Ví dụ như rmdir, mkdir, mount, unmount, link, unlink,...

Nhóm cuối cùng là Miscellaneuos, các POSIX ở đây thực hiện một số tác vụ khác. Ví dụ chdir, kill, time, chmod, ...

Hệ điều hành windows có cách cư xử khác với UNIX, chúng tập chung vào hướng sự kiện. Chương trình người dùng đợi sự kiện xảy ra và gọi thủ tục để xử lý nó.

# 1.7  Operating System Structure

## 1.7.1 Monolithic Systems

Hệ điều hành cấu trúc kiểu khối, chỉ có một chương trình chạy trong kernel mode.

## 1.7.2 Layerde System

Hệ điều hành cấu trúc chia nhiều lớp, mỗi lớp một tác vụ.

Ví dụ hệ điều hành THE. Nó có 5 lớp. Lớp 0 quản lý việc một cpu chạy nhiều chương trình phân chia theo thời gian. Lớp 1 quản lý bộ nhớ cho các chương trình. Lớp 3 quản lý các I/O. Lớp 4 là lớp của chương trình người dùng. Lớp thứ 5 đặt các chương trình hoạt động của hệ thống. 

## 1.7.3 Microkernels

Ở dạng thiết kế hệ điều hành thứ 2, chúng ta thấy sự phân chia giữa user mode và kernel mode, tuy nhiên vậy là chưa đủ. Theo tính toán, cứ 1000 dòng lệnh kernel thì sẽ xuất hiện từ 2 đến 10 lỗi. Và số lượng lỗi của 5 triệu dòng lệnh sẽ là 10000 đến 50000. Tuy những lỗi này hiếm xảy ra nhưng chúng không an toàn. Ý tưởng của Microkernel là làm cho chương trình chạy trong kernel nhỏ xuống, đơn giản xuống và chỉ thực hiện điều hướng các tác vụ cần thiết. Phần còn lại sẽ chạy ở user mode.

## 1.7.4 client -server system

Từ ý tưởng của microkernel, người ta đã đưa ra hai đối tượng client và server. Client và server sẽ liên lạc với nhau qua message. Client gửi yêu cầu tới server, server phản hồi lại yêu cầu của client. Client và server có thể chạy ở những máy tính phân biệt, kết nối với nhau qua mạng LAN hoặc internet.

## 1.7.5 Virtual Machine

Ý tưởng về hệ điều hành máy ảo đã có từ rất lâu dưới sự nỗ lực của IBM.

Tuy nhiên, phải đến cuối thể kỉ 20, những dự án như Disco và Xen được phát triển và sự ra đời của KVM mới khiến cho chủ đề ảo hóa được ưu tiên quan tâm.

Có hai dạng mô hình ảo hóa hệ điều hành. Loại thứ nhất, hypervisor sẽ là lớp trung gian giữa các máy ảo và phần cứng vật lý. Nói cách khác hypervisor sẽ đảm nhiệm luôn vai trò quản lý các tài nguyên phần cứng. Loại thứ 2, hypervisor sẽ hoạt động dựa trên một hệ điều hành và nhờ hệ điều hành này quản lý các tài nguyên phần cứng vật lý. Công nghệ để các máy ảo chạy được là binary translation. Về cơ bản đó là công nghệ chuyển đỗi các lệnh thực thi của máy ảo chạy dựa trên CPU ảo hóa do hypervisor mô phỏng thành các lệnh thực thi của CPU vật lý. 

## 1.7.6 Exokernels

Exokernels là một chương trình chạy ở kernel mode chuyên đảm nhiệm việc quản lý tài nguyên lưu trữ trong ở đĩa của của các máy ảo, tránh cho chúng sử dụng các vùng lưu trữ đè lên nhau và giảm thời gian dịch block giữa vùng nhớ cấp cho máy ảo và vùng nhớ thật.

# 1.8 The World According To C



