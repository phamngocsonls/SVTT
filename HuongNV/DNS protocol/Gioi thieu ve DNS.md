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

<a name="1"></a>

## 1. DNS là gì?

DNS Server (Domain Name System) là 1 hệ thống phân giải tên được phát minh vào những năm 1984 dành cho Internet, chỉ cho phép một hệ thống thiết lập tương ứng giữa địa chỉ IP và tên miền. Hệ thống tên miền DNS là 1 hệ thống được đặt tên theo thứ tự các máy tính hay bất kì nguồn lực đã tham gia vào mạng Internet. Nó sẽ liên kết nhiều thông tin đa dạng với các tên miền được gán cho những người dùng tham gia. Quan trọng nhất là nó chuyển tên miền có ý nghĩa cho con người vào số định danh(nhị phân), liên kết với các trang thiết bị mạng cho các mục đích định vị và địa chỉ hóa các thiết bị khắp thế giới

![Imgur](https://i.imgur.com/Jxjh92I.png)

<a name="2"></a>

## 2. Chức năng của DNS

Mỗi Website có một tên (là tên miền hay đường dẫn ỦL: Universal Resource Locator) và một địa chỉ IP. Địa chỉ IP gồm 4 nhóm cách nhua bằng dấu chấm. Khi mở một trình duyệt Web và nhập tên Website, trình duyệt sẽ đến thẳng website mà không cần phải thông qua việc nhập địa chỉ IP của trang web. Qúa trình `dịch` tên miền thành địa chỉ IP để cho trình duyệt hiểu và truy cập được vào website là công việc của một DNS server. Các DNS trợ giúp qua lại với nhau để dịch địa chỉ `IP` thành `tên` và ngược lại. Người sử dụng chỉ cần nhớ tên, không cần nhớ địa chỉ IP vì nó rất khó nhớ 

<a name="3"></a>

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

### 6.1 Primary server

- Nguồn xác thực thông tin chính thức cho các domain mà nó được phép quản lý
- Thông tin về tên miền được phân cấp quản lý thì được lưu trữ tại đây và sau đó có thể được chuyển sang cho các secondary server
- Primary server nên đặt gần các client để có thể phục vụ truy vấn tên miền một cách dễ dàng và nhanh hơn

### 6.2 Secondary server

DNS được khuyến nghị nên sử dụng ít nhất là hai DNS server để lưu cho mỗi một zone. Primary DNS server quản lý các zone và secondary server sử dụng để lưu trữ dự phòng cho primary server.

Khi lượng truy vấn zone tăng cao tại primary thì nó sẽ chuyển bớt tải sang cho secondary server hoặc khi primary server gặp lỗi thì secondary đứng lên hoạt động thay thế
