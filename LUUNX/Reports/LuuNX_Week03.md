# Tìm Hiểu KVM
* Tuần 3
* Người Thực Hiện: Nguyễn Xuân Lưu
* Tìm hiểu sách Modern Operating System 4th
## 1. Introduce

Mỗi hệ thống máy tính có chứa rất nhiều thành phần phần cứng như bộ vi xử lý, bộ nhớ chính, card mạng, màn hình, ổ đĩa, ... Nếu những lập trình viên khi lập trình phải hiểu tất cả các thành phần phần cứng thì sẽ không thể nào có chương trình phần cứng nào xuất hiện. Vì vậy, để giải quyết vấn đề trên, khái niệm hệ điều hành (operating system) ra đời. Hệ điều hành là một lớp phần mềm trung gian giữa các phần cứng và phần mềm ứng dụng, nó cung cấp cài tài nguyên cần thiết cho các phần mềm chạy trên nó hoạt động.
<image>
Hầu hết hệ thống máy tính hiện tại đều có hai chế độ hoạt động: kernel mode và user mode. Hệ điều hành là một phần mềm chạy ở kernel mode. Với kernel mode, hệ điều hành có toàn quyền truy cập và quản lý phần cứng. Ngược lại, các phần mềm chạy dựa trên hệ điều hành sẽ chạy ở user mode. Với user mode, các phần mềm sẽ không thế truy cập và thao tác trực tiếp phần cứng, chúng cần xin được sự hỗ trợ từ hệ điều hành.

Một hệ điều hành thì khác những phần mềm ứng dụng chạy trên nó về nhiều thứ, không chỉ vị trí nằm của nó (kernel mode). Hệ điều hành lớn, phức tạp và chạy lâu dài. Kích thước mã nguồn của một hệ điều hành như linux hay windows cỡ 5 triệu dòng lệnh hoặc hơn thế. Dễ dàng tưởng tượng được, sẽ cần tới 100 cuốn sách, mỗi cuốn có 1000 trang, mỗi trang 50 dòng để lưu giữ source code của một hệ điều hành. Điều này còn chưa chỉ rõ sự phức tạp, 5 triệu dòng lệnh chỉ là những phần chạy ở kernel mode, chưa tính đến những thư viện cần thiết để cung cấp sự hoạt động cho các ứng dụng chạy trên nền hệ điều hành. Nếu kể cả chúng, đối với windows, chúng ta sẽ cần sẽ cần tới 70 triệu dòng lệnh.

### 1.1 Hệ điều hành là gì?
Nhiệm vụ của của hệ điều hành gồm 2 công việc. Thứ nhất, hệ điều hành cung cấp những đối tượng tài nguyên trừu tượng cho các ứng dụng chạy trên nó. Thứ hai, hệ điều hành quản lý các tài nguyên phần cứng.

Hệ điều hành cung cấp các tài nguyên trừu tượng. Một hệ thống máy tính thì chứa nhiều thành phần phần cứng. Các thành phần này yêu cầu điều khiển bằng ngôn ngữ máy, rất phức tạp. Việc hiểu và sử dụng ngôn ngữ máy của một thiết bị phần cứng sẽ cũng chẳng có ý nghĩa gì nếu thiết bị đó được nâng cấp hoặc thay thế. Giải pháp là hệ điều hành sẽ trừu tượng hóa phần cứng thành các đối tượng dễ thao tác để người phát triển phần mềm ứng dụng sử dụng. Ví dụ điển hình nhất là file. file là đối tượng được trữu tượng hóa từ phần cứng SATA disk. Sẽ thật tồi tệ nếu làm việc trực tiếp trên SATA disk.

<img>

Hệ điều hành sẽ quản lý tài nguyên phần cứng. Nếu là hệ điều hành đơn nhiệm đơn người dùng việc quản lý tài nguyên sẽ đơn giản. Tuy nhiên, một hệ thống có nhiều phần mềm chạy, nhiều người dùng cùng đăng nhập hoạt động, việc quản lý ưu tiên, phân phối tài nguyên sẽ phải đến tay hệ điều hành. Cách thức hệ điều hành xử lý công việc này là phân kênh. Kiểu phân kênh thứ nhất là phân kênh theo thời gian. Mỗi chương trình sẽ chạy trong một đoạn thời gian ngắn. Kiểu thứ hai là phân kênh theo không gian. Mỗi chương trình sẽ chạy trên một phần của phần cứng vật lý trong cùng một thời điểm.
