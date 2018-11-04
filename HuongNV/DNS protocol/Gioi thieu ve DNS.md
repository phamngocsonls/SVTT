# Một vài ghi chép về DNS

# Mục lục

- [1. DNS là gì?](#1)
- [2. Chức năng của DNS](#2)
- [3. Nguyên tắc làm việc của DNS](#3)
- [4. Cách sử dụng DNS](#4)
- [5. Cấu trúc hệ thống tên miền DNS](#5)
    - [5.1 DNS namespace](#51)
    - [5.2 DNS server](#52)
    - [5.3 Zone](#53)
- [6. Phân loại DNS server](#6)
    - [6.1 Primary server](#61)
    - [6.2 Secondary server](#62)
    - [6.3 Caching Name server](#63)
- [7. Đồng bộ dữ liệu giữa các DNS server](#7)
    - [7.1 Truyền toàn bộ zone](#71)
    - [7.2 Truyền phần thay đổi](#72)

<a name="1"></a>

## 1. DNS là gì?

DNS Server (Domain Name System) là 1 hệ thống phân giải tên được phát minh vào những năm 1984 dành cho Internet, chỉ cho phép một hệ thống thiết lập tương ứng giữa địa chỉ IP và tên miền. Hệ thống tên miền DNS là 1 hệ thống được đặt tên theo thứ tự các máy tính hay bất kì nguồn lực đã tham gia vào mạng Internet. Nó sẽ liên kết nhiều thông tin đa dạng với các tên miền được gán cho những người dùng tham gia. Quan trọng nhất là nó chuyển tên miền có ý nghĩa cho con người vào số định danh(nhị phân), liên kết với các trang thiết bị mạng cho các mục đích định vị và địa chỉ hóa các thiết bị khắp thế giới

![Imgur](https://i.imgur.com/Jxjh92I.png)

<a name="2"></a>

## 2. Chức năng của DNS

Mỗi Website có một tên (là tên miền hay đường dẫn ỦL: Universal Resource Locator) và một địa chỉ IP. Địa chỉ IP gồm 4 nhóm cách nhua bằng dấu chấm. Khi mở một trình duyệt Web và nhập tên Website, trình duyệt sẽ đến thẳng website mà không cần phải thông qua việc nhập địa chỉ IP của trang web. Qúa trình `dịch` tên miền thành địa chỉ IP để cho trình duyệt hiểu và truy cập được vào website là công việc của một DNS server. Các DNS trợ giúp qua lại với nhau để dịch địa chỉ `IP` thành `tên` và ngược lại. Người sử dụng chỉ cần nhớ tên, không cần nhớ địa chỉ IP vì nó rất khó nhớ 

<a name=="3"></a>

## 3. Nguyên tắc làm việc của DNS

Mỗi nhà cung cấp dịch vụ vận hành và duy trì DNS server riêng của mình gồm các máy bên trong phần riêng của mỗi nhà cung cấp dịch vụ đó trong Internet. Tức là nếu một trình duyệt tìm kiếm địa chỉ của một website thì DNS server phân giải tên website này phải là DNS server của chính tổ chức quản lý website đó chứ không phải là của một tổ chức nào khác

INTERNIC (Internet Network Information Center) chịu trách nhiệm theo dõi các tên miền và các DNS server tương ứng. INTERNIC là một tổ chức được thành lập bởi NFS(National Science Foundation), AT&T và Network Solution, chịu trách nhiệm đăng kí các tên miền của Internet. INTERNIC chỉ có nhiệm vụ quản lý tất cả các DNS server trên Internet chứ không có nhiệm vụ phân giải tên miền cho từng địa chỉ

Tại Việt Nam, VNNIC là đơn vị trực thuộc Bộ Thông tin và Truyền Thông thực hiện chức năng quản lý và thúc đẩy việc sử dụng tài nguyên Internet ở Việt Nam: thiết lập, quản lý và khai thác hệ thống DNS quốc gia.

DNS có khả năng tra vấn các DNS server khác để có được một cái tên đã được phân giải. DNS server của mỗi tên miền thường có hai khác biệt. Thứ nhất chịu trách nhiệm phân giải tên từ các máy bên trong miền về các địa chỉ Internet, cả bên trong lẫn bên ngoài miền nó quản lý. Thứ hai, chúng trả lời các DNS server bên ngoài đang cố gắng phân giải những cái tên bên trong miền nó quản lý.

DNS server có khả năng ghi nhớ lại những tên vừa được phân giải để dùng cho những yêu cầu phân giải về sau. Số lượng những tên phân giải được lưu lại tùy thuộc vào quy mô của từng DNS

<a name="4"></a>

## 4. Cách sử dụng DNS

Do DNS có tốc độ biên dịch khác nhau, có thể nhanh hoặc có thể chậm, do đó người sử dụng có thể chọn DNS server để sử dụng cho riêng mình. Có các cách lựa chọn cho người sử dụng như sau:
- Sử dụng địa chỉ DNS mặc định của nhà cung cấp dịch vụ internet, trường hợp này không cần điền địa chỉ DNS vào network connections trong máy host
- Sử dụng DNS server khác (miễn phí hoặc tính phí) thì phải điền địa chỉ DNS server vào network connections.

<a name="5"></a>

## 5. Cấu trúc hệ thống tên miền DNS

<a name="51"></a>

### 5.1 DNS namespace

- Hệ thống tên trong DNS được sắp xếp theo mô hình phân cấp và cấu trúc cây logic được gọi là DNS namespace

![Imgur](https://i.imgur.com/PFzxvrN.jpg)

### Cấu trúc hệ thống tên miền

- Hệ thống tên miền được phân thành nhiều cấp:
    - Gốc(Domain root): Nó là đỉnh của nhánh cây tên miền. Nó có thể biểu diễn đơn giản chỉ là dấu chấm
    - Tên miền cấp 1(Top-level-domain): gồm một vài kí tự xác định một nước, khu vực hoạc tổ chức, nó có thể là `.com`, `.edu`
    - Tên miền cấp hai(Second-level-domain): Nó rất đa dạng, có thể là tên một công ty, tổ chức hoặc một cá nhân
    - Tên miền cấp nhỏ hơn(Subdomain): Chia thêm ra của tên miền cấp 2 trở xuống, thường được sử dụng như chi nhánh, phòng ban của cơ quan tổ chức

### Phân loại tên miền

- com: Tên miền dùng cho các tổ chức thương mại
- edu: Tên miền dùng cho cơ quan giáo dục, trường học
- net: Tên miền dùng cho các tổ chức mạng lớn
- gov: Tên miền dùng cho các tổ chức chính phủ

<a name="52"></a>

### 5.2 DNS Server

- Là một máy tính chạy chương trình DNS Server như là DNS service
- DNS server là một cơ sở dữ liệu chứa thông tin về vị trí của các DNS domain và phân giải các truy vấn xuất phát từ client
- DNS có thể cung cấp các thông tin mà client yêu cầu, và chuyển đến một DNS server khác để nhờ phân giải hộ trong trường hợp nó không thể trả lời được các truy vấn về những tên miền không thuộc quyền quản lý của nó.
- Lưu thông tin của zone, truy vấn và trả kết quả của DNS client

<a name="53"></a>

### 5.3 Zone

Hệ thống tên miền(DNS) cho phép phân chia tên miền để quản lý và nó chia hệ thống tên miền thành zone và trong zone quản lý tên miền được phân chia đó.Các Zone chứa thông tin vê miền cấp thấp hơn, có khả năng chia thành các zone cấp thấp hơn và phân quyền cho các DNS server khác quản lý.
Ví dụ : Zone “.vn” thì do DNS server quản lý zone “.vn” chứa thông tin về các bản ghi có đuôi là “.vn” và có khả năng chuyển quyền quản lý (delegate) các zone cấp thấp hơn cho các DNS khác quản lý như “.fpt.vn” là vùng (zone) do fpt quản lý.

<a name="6"></a>

## 6. Phân loại DNS server

Có 2 loại DNS server như sau:
- Primary server
- Secondary server

<a name="61"></a>

### 6.1 Primary server

- Nguồn xác thực thông tin chính thức cho các domain mà nó được phép quản lý.
- Thông tin về tên miền được phân cấp quản lý thì được lưu trữ tại đây và sau đó có thể chuyển cho các secondary server
- Các tên miền do primary server quản lý thì được tạo ra và sửa đổi tại primary server và được cập nhật đến các secondary server
- Primary server nên đặt gần các client để có thể phục vụ truy vấn tên miền một cách dễ dàng và nhanh hơn.

<a name="62"></a>

### 6.2 Secondary server

DNS được khuyến nghị nên sử dụng ít nhất là 2 DNS server để lưu cho mỗi một zone. Primary DNS server quản lý các zone và secondary sử dụng để lưu trữ dự phòng cho primary server. Secondary server được khuyến nghị dùng nhưng không nhất thiết phải có. Secondary server được phép quản lý domain, secondary không tạo ra các bản ghi về tên miền mà nó lấy từ primary server.

Khi lượng truy vấn zone tăng cao tại primary server thì nó sẽ chuyển bớt tải sang cho secondary server. Hoặc khi primary server gặp sự cố không hoạt động được thì secondary server sẽ hoạt động thay thế cho đến khi primary server hoạt động trở lại.

Secondary server nên được đặt gần với primary server và client để có thể phục vụ cho việc truy vấn tên miền dễ dàng hơn. Nhưng không nên cài đặt secondary server trên cùng một mạng con hoặc cùng một kết nối với primary server. Mục đích là để khi primary gặp sự cố thì sẽ không ảnh hưởng tới secondary server.

Primary server thường xuyên thay đổi hoặc thêm vào các zone mới nên DNS server sử dụng cơ chế cho phép secondary lấy thông tin từ primary server và lưu trữ nó. Có 2 giải pháp lấy thông tin về các zone mới là lấy toàn bộ hoặc chỉ lấy phần thay đổi.

Khi secondayr server được khởi động, nó sẽ tìm primary server nào mà nó đươc phép lấy dữ liệu về máy. Nó sẽ copy lại toàn bộ cơ sở dữ liệu của primary server mà nó được phép transfer. theo 1 chu kì nào đó người quản trị quy định thì secondary server sẽ sao chép và cập nhật CSDL từ primary server. Qúa trình zone transfer được minh họa bằng hình dưới đây:


![Imgur](https://i.imgur.com/YXpMg2b.png)


<a name="63"></a>

### 6.3 Caching Name server

Tất cả các DNS server đều có khả năng lưu trữ dữ liệu trên bộ nhớ cache của một máy để trả lời truy vấn một cách nhanh chóng. Nhưng hệ thống DNS còn có một loại caching-only server. Loại này chỉ sử dụng cho việc truy vấn, lưu trữ câu trả lời dựa trên thông tin có trên cache của máy và cho kết quả truy vấn. Chúng không hề quản lý một domain nào và thông tin mà nó chỉ giới hạn những gì được lưu trên cache của server.

Lúc ban đầu khi server bắt đầu chạy thì nó không lưu thông tin nào trong cache. Thông tin sẽ được cập nhật theo thời gian khi các client server truy vấn dịch vụ DNS. Nếu bạn sử dụng kết nối mạng WAN tốc độ thấp thì việc sử dụng caching-only server là giải pháp hữu hiệu cho phép giảm lưu lượng thông tin truy vấn trên đường truyền.

Caching-only có khả năng trả lời các câu truy vấn đến client. Nhưng không chứa zone nào và cũng không có quyền quản lý bất kì domain nào. Nó sử dụng bộ cache của mình để lưu các truy vấn của DNS của client. Thông tin sẽ được lưu trong cache để trả lời các tủy vấn đến client để làm tăng tốc độ phân giải và giảm gánh nặng phân giải tên máy.

<a name="7"></a>

## 7. Đồng bộ dữ liệu giữa các DNS server

Do đề phòng rủi ro khi DNS server không hoạt động hoặc kết nối bị đứt, người ta khuyến nghị nên dùng hơn một DNS server để quản lý một zone nhằm tránh trục trặc đường truyền. Do vậy ta phải có cơ chế chuyển dữ liệu giữa các zone và đông bộ dữ liệu giữa chúng với nhau. Có 2 cách để đồng bộ dữ liệu giữa các DNS server với nhau:
- Truyền toàn bộ zone
- Truyền phần thay đổi

<a name="71"></a>

### 7.1 Truyền toàn bộ zone

Khi một DNS server mới được thêm vào mạng thì nó được cấu hình như một secondary server mới cho một zone đã tồn tại. Nó sẽ tiến hành nhân toàn bộ dữ liệu từ primary server. Đối với các DNS server phiên bản ddaauff tiên thường sử dụng giải pháp lấy toàn bộ các CSDL khi có các thay đổi trong zone.

<a name="72"></a>

### 7.2 Truyền phần thay đổi

Giari pháp này chỉ là truyền những dữ liệu thay đổi của zone. Đồng bộ dữ liệu này được miêu tả chi tiết trong tiêu chuẩn RFC 1995. Nó cung cấp giải pháp hiệu quả cho việc đồng bộ những thay đổi thêm, bớt của 1 zone.

## Cớ chế đồng bộ dữ liệu giữa các DNS server

Với việc trao đổi IXFR zone thì sư khác nhau giữa số serial của nguồn dữ liệu và bản sao của nó. Nếu cả hai đều co cùng số serial thì việc truyền dữ liệu của zone sẽ không thực hiện.

Nếu truy vấn IXFR thực hiện không thành công và các thay đổi được gửi lại thì tại DNS server nguồn của zone phải được lưu giữ các phần thay đổi để sử dụng truyền đến nơi yêu cầu truy vấn IXFR. Incremental sẽ cho phép lưu lượng truyền dữ liệu ít và nhanh hơn.

Zone transfer sẽ xảy ra khi có những hành động sau xảy ra:
- Khi quá trình làm mới của zone đã kết thúc
- Khi secondary server được thông báo zone đã thay đổi tại nguồn quản lý zone
- Khi thêm mới secondary server
- Tại secondary server yêu cầu chueyenr zone

Các bước yêu cầu chuyển dữ liệu từ secondary server đến DNS server chứa zone để yêu cầu lấy dữ liệu về zone mà nó quản lý:
- Khi cấu hình DNS server mới thì nó sẽ gửi truy vân yêu cầu toàn bộ zone đến DNS server chính mà quản lý dữ liệu của zone.
- DNS server chính trả lời và chuyển toàn bộ dữ liệu về zone cho secondary server mới cáu hình

Để xác định có chuyển dữ liệu hay không thì nó dựa vào số serial được khai báo bằng bản ghi SOA.
- Khi thời gian làm mới của zone đã hết, thì DNS server nhận dữ liệu sẽ truy vân yêu cầu làm mới zone tới DNS server chính chứa dữ liệu zone
- DNS server chính trả lời truy vấn và gửi lại dữ liệu. Trả lời truy vấn dữ liệu gồm số serial của zone tại DNS server chính.
- DNS server nhận dữ liệu về zone và sẽ kiểm tra số serial trong bản tin reply và quyết định xem có cần truyền dữ liệu không.
    - Nếu giá trị số serial của Primary server bằng số serial lưu tại nó thì sẽ kết thúc luôn, và nó sẽ thiết lập lại với các thông số cũ lưu trong máy.
    - Nếu giá trị số serial tại Primary server lớn hơn giá trị serial hiện tại DNS nhận dữ liệu thì nó kết luận zone cần được update và đồng bộ dữ liệu