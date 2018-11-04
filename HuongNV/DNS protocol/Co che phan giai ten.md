# Cơ chế phân giải tên

# Mục lục
- [1. Phân giải tên thành IP](#1)
- [2.Phân giải IP thành tên máy](#2)

<A name="1"></a>

Root name server là máy chủ quản lý các nameserver ở mức top-level domain. Khi có truy vấn về một tên miền nào đó thì Root name server phải cung cấp tên và địa chỉ IP của nameserver quản lý top-level domain(thực tế là hầu hết các root server cũng chính là máy chủ quản lý top-level domain) và đến lượt các name server của top-levle domain cung cấp danh sách các name server có quyền trên các second-levle domain mà tên miền này thuộc vào. Cứ như thế đến khi nào tìm được máy chủ quản lý tên miền cần truy cập tới. Từ đó ta có thể thây được vai trò rất quan trọng của root server trong quá trình phân giải tên miền. Nếu mọi root name server trên mạng internet không liên lạc được với nhau thì nơi yêu cầu phân giải đều không thực hiện được. Hình vẽ dưới đây mô tả quá trình phân giải grigiri.gbrmpa.au trên mạng Internet.

![Imgur](https://i.imgur.com/ti2Tb3O.png)

Client sẽ gửi yêu cầu cần phân giải địa chỉ IP của máy tính có tên miền grigiri.gbrmpa.gov.au đến name server cục bộ. Khi nhận được yêu cầu từ resolver, nameserver cục bộ sẽ phân tích tên này và xem xét tên miền này có do mình quản lý hay không. Nếu như tên miền này do server cục bộ quản lý, nó sẽ trả lời địa chỉ IP của tên máy đó cho resolver. Ngược lại server cục bộ sẽ truy vấn đến một Root name server gần nhất mà nó biết được. Root name server sẽ trả lời địa chỉ IP của naemserver quản lý miền au. Máy chủ nameserver cục bộ laijh ỏi tiếp nameserver quản lý miền au và được tham chiếu đến máy chủ quản lý miền `gov.au`. Máy chủ `gov.au` chỉ dẫn máy nameserver cục bộ tham chiếu đến máy chủ quản lý miền `gbrmpa.gov.au` và nhận được câu trả lời lại

Truy vấn có 2 loại:
- Truy vấn đề quy: Khi name server nhận được truy vấn dạng này, nó bắt buộc phải trả về kết quả tìm được hoặc thông báo lỗi nếu như truy vấn này không phân giải được. Nameserver không thể tham chiếu tới server khác, nameserver có thể gửi truy vấn dạng đệ quy hoặc tương tác đến nameserver khác nhưng nó phải thực hiện cho đến khi nào có kết quả mới thôi
- Truy vấn tương tác: Khi nameserver nhận được truy vấn dạng này, nó trả lời resolver với thông tin tốt nhất mà nó có được vào thời điểm đó. Bản thân nameserver không thực hiện được bất cứ một truy vấn nào thêm. Thông tin tốt nhất trả về có thể lấy dữ liệu từ dữ liệu cục bộ. Trong trường hợp nameserver không tìm thấy trong dữ liệu cục bộ, nó sẽ trả về tên miền và địa chỉ IP của nameserver gần nhất mà nó biết được.

Hình vẽ sau minh họa sơ đồ truy vấn tương tác:

![Imgur](https://i.imgur.com/nnTXaiF.png)


<a name="2"></a>

## 2. Phân giải IP thành tên máy

Anha xạ địa chỉ IP thành tên máy tính được dùng để diễn dịch các tập tin log cho dễ đọc hơn. Nó còn được dùng trong một số trường hợp chứng thực trên hệ thống UNIX. Trong không gian tên miền đã nói wor trên, dữ liệu bao gồm địa chỉ IP được thiết lập chỉ mục theo tên miền. Do đó việc tìm địa chỉ IP ứng với 1 tên miền khá là dễ dàng.

Để có thể phân giải tên máy thành của một địa chỉ IP, trong không gian tên miền người ta bổ sung thêm một nhành tên miền mà được thiết lập chỉ mục theo địa chỉ IP. Phần không gian này có tên miền là `in-arpa.arpa`.

Mỗi nút trong miền `in-arpa.arpa` có một tên nhãn là chỉ số thập phân của địa chỉ IP.

Ví dụ: Miền `in-arpa.arpa` có thể có 256 subdomain, tương ứng với 256 giá trị từ 0 đến 255 của byte dầu tiên trong địa chỉ IP. Trong mõi subdoman lại có 256 subdomain ưng với byte thứ 2. Cứ như thế và đến byte thứ 4 có các bản ghi cho tên miền đầy đủ của các máy tính hoặc các mạng có địa chỉ IP tương ứng

Hình vẽ sau minh họa sơ đồ phân giải tên thành địa chỉ IP

![Imgur](https://i.imgur.com/n0OsvrR.png)
