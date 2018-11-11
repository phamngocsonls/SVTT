# Tìm hiểu về Cloudflare

# Mục lục
- [1. Cloudflare là gì?](#1)
- [2. Ưu và nhược điểm của việc sử dụng Cloudflare](#2)
    - [2.1 Ưu điểm](#21)
    - [2.2 Nhược điểm](#22)
- [3. Hướng dẫn sử dụng Cloudflare](#3)

<a name="1"></a>

## 1. Cloudflare là gì?
**Cloudflare** được biết đến là một dịch vụ DNS trung gian, giúp điều phối lưu lượng truy cập qua lớp bảo vệ Cloudflare. Hay nói mọt cách dễ hiểu thì thay vì bạn truy cập trực tiếp vào website thông qua máy chủ phân giải tên miền DNS thì bạn sẽ sử dụng máy chủ phân giải tên miền của Cloudflare. Các truy vấn sẽ phải đi qua máy chủ của Cloudflare để xem dữ liệu website thay vì truy cập trực tiếp.

![Imgur](https://i.imgur.com/sJQLWC2.png)

<a name="2"></a>

## 2. Uưu và nhược điểm của việc sử dụng Cloudflare

<a name="21"></a>

### 2.1 Ưu điểm
- Giups website của bạn tăng tốc độ truy cập bằng cách Cloudflare sẽ lưu một bản bộ nhớ đếm(cache) của website trên máy chủ của CDN của họ. Từ đó phân phối cho người dùng truy cập ở gần máy chủ đó nhất. Chẳng hạn nếu máy chủ đặt ở TP.HCM thì người dùng ở NewYork sẽ truy cập chậm vì máy chủ vật lý ở xa và ngược lại. Bên cạnh đó, những dữ liệu tĩnh như hình ảnh, CSS, các tập tin... cũng được Cloudflare nén zip lại nên tốc độ tải nhanh hơn.
- Giups tiết kiệm được băng thông cho máy chủ vì hạn chế truy cập trực tiếp vào máy chủ. Lúc này, băng thông sử dụng giảm hẳn chỉ còn 1/2 - 1/3 so với trước khi dùng.
- Giúp website tăng khẳ năng bảo mật, hạn chế được sự tấn công của DDoS, spam bình luận trên blog và một số phương thức tấn công cơ bản khác. Bạn có thể cải thiện bảo mật website bằng cách sử dụng Cloudflare như sử dụng SSL, miễn phí để thêm giao thức HTTPS cho website; hạn chế truy cập từ các quốc gia chỉ định, cấm truy cập với các IP nhất định, công nghệ tưởng lửa ứng dụng website, bảo vệ các trang có tính chất đăng nhập(gói Pro).

<a name="22"></a>

### 2.2 Nhược điểm
- Nếu website của bạn nằm trên hosting có máy chủ đặt tại Việt Nam, khách hàng chủ yếu đến từ Việt Nam thì việc sử dụng Cloudflare làm chậm đi tốc độ tải trang vì chất lượng đường truyền quốc tế tại Việt Nam. Nguyên nhân được cho là lúc này truy cập sẽ đi vòng từ Việt Nam đến DNS server của Cloudflare rồi mới trả kết quả về Việt Nam.
- Thời gian uptime website phụ thuộc vào thời gian uptime của server Cloudflare nếu bạn sử dụng. Tức là nếu server Cloudflare bị down thì khả năng truy xuất vào website của bạn sẽ bị gián đoạn vì không phân giải được tên miền website đang sử dụng.
- Không ai biết được IP của máy chủ của bạn là một điều tốt. Nhưng vấn đề nằm ở chỗ, nếu website bảo mật không kĩ thì sẽ rất bị tấn công bằng nheieuf cách khác nhau. Tất nhiên, người dùng cũng sẽ không bao giờ biết được IP thực sự của khách hàng truy cập vào website của mình.
- Đôi lúc Firewall của hosting mà website bạn đang đặt hiểu lầm dải IP của Cloudflare là địa chỉ tấn công. Rất có thể website của bạn bị offline. 

<a name="3"></a>

### 3. Hướng dẫn sử dụng Cloudflare

