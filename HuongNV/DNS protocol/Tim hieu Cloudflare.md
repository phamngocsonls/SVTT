# Tìm hiểu về Cloudflare

# Mục lục
- [1. Cloudflare là gì?](#1)
- [2. Ưu và nhược điểm của việc sử dụng Cloudflare](#2)
    - [2.1 Ưu điểm](#21)
    - [2.2 Nhược điểm](#22)
- [3. Hướng dẫn sử dụng Cloudflare](#3)
- [4. Tìm hiểu về Cloudflare Argo Smart Routing](#4)
- [5. Argo Tunnel](#5)
- [6. Tài liệu tham khảo](#6)

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

<a name="4"></a>

## 4. Tìm hiểu Cloudflare Argo Smart Routing
Internet vốn không tin cậy, nó là một tập hợp các mạng kết nối với nhau bằng sợi quang học, cáp đồng hoặc qua sóng cao tần. Mọi thứ trên Internet có thể bị phá vỡ bất cứ lúc nào, cáp có thể bị đứt, bộ định tuyến có thể bị lỗi. Điều này dẫn tới việc trải nghiệm người dùng gặp nhiều khó khăn và phiền toái.

![Imgur](https://i.imgur.com/auanOxW.png)

Để có thể khắc phục các vấn đề này, Cloudflare đã giới thiệu `Arrgo`, một `virtual backbone` cho mạng internet hiện đại hiện nay. Argo phân tích, tối ưu hóa các bản tin định tuyến trên toàn cầu trong thời gian thực. Hay nói cách khác, Cloudflare Argo là dịch vụ định tuyến thông minh có trả phí nhằm tối ưu hóa việc phân phối nội dung từ máy chủ tới người dùng cuối.

Thay vì kết nối hai vị trí ở xa một cách trực tiếp, Cloudflare Argo tối ưu hóa đường truyền dẫn giữa hai điểm đó bằng cách chọn đường tốt nhất thay vì sử dụng định tuyến tĩnh truyền thống đang được áp dụng hiện nay. Kết quả là Argo có thể truyền tải nội dung trên mạng với độ trễ giảm đáng kể, độ tin cậy tăng lên, thông tin được mã hóa bảo vệ, chi phí vận hành được giảm đáng kể. 

Kết quả nghiên cứu chỉ ra rằng, với Argo sẽ cho độ trung bình giảm tới 35% về độ trễ, giảm 27% về lỗi kết nối và giảm tới 60% các vấn đề liên quan tới bộ nhớ cache. Các website, API và ứng dụng sử dụng Argo đều cho thấy tốc độ trải nghiệm người dùng cải thiện rõ rêt, băng thông giảm một nwuar so với trước khi dùng Argo.

Argo là một hệ thống thần kinh trung ương cho Internet, Xử lý thông tin từ mọi yêu cầu mà nó nhận được để xác định tuyến đường nào chạy nhanh, đường nào chạy chậm, đường nào tối ưu để cho trải nghiệm tốt nhất. Thông qua 115 PoP - Points of Presence của Cloudflare và 6 triệu tên miền, Argo biết được các ISP và các user đi qua nó, từ đó nó biết được các thông tin về node mạng, các node bị lỗi, mất gói.

Một số lợi ích phải kể đến khi sử dụng Cloudflare Argo như:
- Thời gian tải nhanh hơn nhờ tối ưu hóa các tuyến đường kết nối
- Tăng độ tin cậy, làm giảm tắc nghẽn và mất gói
- Tăng cường bảo mật khi các dữ liệu đã được Cloudflare mã hóa
- Hiệu năng cao hơn khi nội dung đã được tối ưu hóa

Argo có hai chức năng chính là: Smart Routing và Tiered Cache. Người sử dụng có thể mở tính năng này thông qua `Traffic app` trên dashboard. Argo có gí là 5$ mỗi tháng, cộng với 0.10$ mỗi GB dữ liệu truyền từ Clouflare tới người sử dụng.

![Imgur](https://i.imgur.com/wRS4VUZ.png)


# Argo Smart Routing

Argo Smart Routing giảm được độ trễ trung bình trên Internet khoảng 35%, tỉ lệ lỗi kết nối khoảng 27%. 

Nội dung được phân phối từ máy chủ khách hàng dựa trên chất lượng của đường dẫn mạng đã thiết lập để có hiệu suất nhanh. Các công nghệ mạng truyền thống sử dụng thông tin định tuyến tĩnh có thể gửi nội dung qua các đường dẫn có tốc độ chậm và xảy ra tắc nghẽn. Thời gian tải chậm và thời gian chờ kết nối làm giảm đi trải nghiệm người dùng, có thể làm giảm doanh thu và giá trị thương hiệu của nhà cung cấp dịch vụ.

Cloudflare định tuyến 10% tất cả lưu lượng truy cập Internet HTTP/HTTPS, cung cấp cho Argo thời gian thực về tốc độ của đường dẫn mạng. Thuật toán định tuyến thông minh của Argo sử dụng thông tin này để định tuyến lưu lượng truy cập trên các đường dẫn nhanh nhất hiện có và duy tri các kết nối mở, an toàn để loại bỏ độ trễ do thiết lập kết nối. Công nghệ lưu trữ theo tầng của rgo sử dụng các trung tâm dữ liệu Cloudflare cấp 1 khu vực để truyền bá nội dung tới 155 trung tâm dữ liệu của Cloudflare, giảm thiểu yêu cầu tới máy chủ và giảm chi phí.

Với gần một nửa số khách hàng trực tuyến chỉ ra rằng, họ sẽ từ bỏ một trang mất hơn 2s để tải dữ liệu. Argo cải thiện hiệu suất bằng cách định tuyến lưu lượng truy cập thong qua các đường dẫn ít bị tắc nghẽn và đáng tin cậy nhất bằng cách sử dụng mạng riêng của Cloudflare.
- Congrestion Avoidance: Định tuyến sử dụng điều kiện mạng thười gian thực
- Persistent Connections: Giam thiểu độ trễ được áp đặt bởi thiết lập kết nối TCP
- Private Network: Lưu lượng được định tuyến thông qua mạng riêng của Cloudflare thay vì mạng Internet
- Tiered Caching: Trung tâm dữ liệu cấp 1 truyền bá thông tin nội dung tới mạng lưới toàn cầu gồm 155 trung tâm dữ liệu.

![Imgur](https://i.imgur.com/ez2YW5u.png)


# Argo Tiered Cache

Argo Tiered Cache uses the size of our network to reduce requests to customer origins by dramatically increasing cache hit ratios. Với 115 PoP trên khắp thế giới, Cloudflare lưu tữ nội dung rất gần với người dùng cuối, nhưng nếu một phần nội dung không có trong bộ nhớ cache thì PoP Cloudflare phải liên hệ với máy chủ gốc để nhận nội dung có thể lưu vào bộ nhớ cache. Điều này có thể chậm và tải trên máy chủ gốc so với việc phân phát trực tiếp từ bộ nhớ cache.

![Imgur](https://i.imgur.com/eGWgK1s.jpg)

Argo Tiered Cache làm giảm tải gốc, tăng tỉ lệ truy cập bộ nhớ cache, cải thiện trải nghiệm người dùng cuối bằng cách trước tiên hỏi các PoP Cloudflare khác nếu chúng có nội dung được yêu cầu. Điều này dẫn đến hiệu suất được cải thiện cho khách truy cập, bởi vì khoảng cách và liên kết đi qua giữa các Cloudflare PoP thường ngắn hơn và nhanh hơn so với liên kết giữa PoP và trạm gốc.

# Những lợi ích khác

Ngoài hiệu suất và độ tin cậy, Argo còn mang lại sự an toàn hơn. Tất cả lưu lượng truy cập giữa các trung tâm dữ liệu Cloudflare được bảo vệ bởi TLS và được xác thực lẫn nhau, nó đảm bảo bất kì lưu lượng truy cập nào đi qua Argo backbone đều được bảo vệ và chống giả mạo.

Cloudflare ra đời, nhằm giải quyết rất nheieuf cơn đau đầu trên Internet hiện nay.

![Imgur](https://i.imgur.com/Tuzw5FW.jpg)


## Cloudflare Argo Cost

Bảng biểu sau mô tả chi phí khi sử dụng Argo:

![Imgur](https://i.imgur.com/gdhFLxa.png)


<a name="5"></a>

# 5. Argo Tunnel

Có chức năng bảo vệ máy chủ khỏi các cuộc tấn công. Thay vì phải cấu hình ACL, rotating IP address thì thay vào đó, sử dụng GRE tunnels để bảo vệ web servers khỏi những cuộc tấn công.

///

<a name="6"></a>

# Tài liệu tham khảo
- https://blog.cloudflare.com/argo/
- https://www.cloudflare.com/products/argo-smart-routing/
