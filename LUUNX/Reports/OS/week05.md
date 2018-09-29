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

Các hệ điều hành thông thường được viết dưới ngôn ngữ C.

# 2. Process and Thread

# 2.1 Processes

## 2.1.1 Process Model

Mỗi chương trình thông thường được thực hiện tuần tự, tuy nhiên, một máy tính khi hoạt động lại yêu cầu nhiều tác vụ được thực hiện cùng lúc. Để giải quyết bài toán này. Các tiến trình sẽ được chạy song song bằng các lát cắt thời gian.

Nhìn chung, mỗi tiến trình độc lập sẽ chạy với một CPU ảo, nó có chứa các thông tin về program counter, các giá trị thanh ghi, các biến và các file đã mở. Nếu chỉ xét một máy tính có 1 CPU thực. Tại mỗi thời điểm, CPU chỉ chạy một tiến trình. Tuy nhiên, sự phối hợp về mặt thời gian giúp nó chạy lần lượt các tiến trình khác nhau. Sự chuyển đỗi nhanh chóng tới mức con người không thể nhận ra. 

Một sự phân biệt cần thiết là tiến trình (process) và chương trình (program). Một chương trình ý chỉ file chứa nội dung các lệnh được thực thi. Một tiến trình thì hơn thế, nó bao gồm việc đọc file thực thi, nạp các dữ liệu đầu vào, thực thi và xuất dữ liệu đầu ra.

## 2.1.2 Process Creation

Có nhiều cách để khởi tạo một tiến trình.

Thứ nhất, khi một hệ điều hành được khởi động, nó sẽ khởi tạo nhiều tiến trình đi kèm. Một số thì có giao diện tương tác với người dùng. Ngược lại, một số thì không, chúng chạy ngầm dưới nền, thực hiện những tác vụ cần thiết, chúng gọi là daemons.

Thứ hai, mỗi tiến trình khi đang hoạt động có thể yêu cầu hệ điều hành tạo ra một tiến trình mới để thực thi nhiệm vụ của tiến trình hiện tại giao phó. Lệnh fork() trong UNIX là một ví dụ điển hình.

Thứ ba, người dùng hoàn toàn có thể khởi tạo một tiến trình thông qua việc click một icon, hãy gõ lệnh thông qua shell. Tất cả sẽ khởi tạo tiến trình phù hợp với yêu cầu của người dùng.

## 2.1.3 Process Termination

Việc kết thúc các tiến trình luôn xảy ra đi cùng việc tạo ra các tiến trình.

Lý do kết thúc các tiến trình thường gặp như sau.

Đầu tiên, khi một tiến trình kết thúc công việc, nó sẽ gọi system call exit đối với UNIX hoặc ExitProcess đối với Windows để tự hủy.

Thứ hai, tiến trình bị kết thúc khi nó có lỗi bên trong. Ví dụ như chia cho không, truy cập vùng nhớ không tồn tại, sử dụng lệnh không được phép. 

Thứ ba, tiến trình sẽ bị kết thúc nếu tập dữ liệu đầu vào bị lỗi. Ví dụ tiến trình có đầu vào là một file không tồn tại.

Cuối cùng, lệnh kill từ hệ điều hành có thể kết thúc ngay một tiến trình đang chạy.

## 2.1.4 Process Hierarchies

Việc phân cấp các tiến trình được thực hiện khác nhau ở UNIX và Windows.

Nhìn chung, một tiến trình có một hoặc không tiến trình cha nhưng có thể có rất nhiều tiến trình con. Đối với hệ điều hành UNIX, tiến trình init được khởi chạy lúc hệ điều hành khởi động và là cha của tất cả các tiến trình sau đó. Đối với hệ điều hành Windows, các tiến trình là ngang hàng và không phân cấp.

## 2.1.5 Process State

Các tiến trình khi hoạt động sẽ có trạng thái. Cụ thể, có ba trạng thái của một tiến trình là Running, Blocked và Ready.

Một tiến trình đang chạy trên CPU có trạng thái Running.

Một tiến trình sẵn sàng khởi chạy nhưng không có sẵn CPU rảnh sẽ có trạng thái Ready

Một tiến trình bị dừng để đợi một sự kiện kích thích bên ngoài sẽ có trạng thái Blocked.

Các trạng thái này sẽ thường được chuyển đỗi cho nhau trong suốt vòng đời của tiến trình.

## 2.1.6 Implementation of Process

Hệ điều hành quản lý các process thông qua một process table. Các tiến trình sẽ được lưu thông tin trong table này, bao gồm tất cả các thông tin về program counter, memory, stack, trạng thái các file, các tính toán và lịch chạy. Thông tin này cần thiết khi một tiến trình chuyển từ trạng thái ready sang running và running sang blocked.

