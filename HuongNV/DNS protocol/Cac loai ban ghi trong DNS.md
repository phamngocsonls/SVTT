# Các loại bản ghi trong DNS

## Mục lục

- [1. Khái niệm DNS Resource Record](#1)
- [2. Các kiểu Reource Record](#2)
    - [2.1 2.1 SOA (Start of Authority)](#21)
    - [2.2 NS (Name Server)](#22)
    - [2.3 A (Address) và CNAME(Canonical Name)](#23)
        - [2.3.1 Bản ghi kiểu A](#231)
        - [2.3.2 Bản ghi CNAME](#232)
    - [2.4 AAAA](#24)
    - [2.5 SRV](#25)
    - [2.6 Mail Exchange](#26)
    - [2.7 PTR(Pointer)](#27)

<a name="1"></a>

# 1. Khái niệm DNS Resource Record

- RR -  Resource Record là mẫu thông tin dùng để mô tả các thông tin về cơ sở dữ liệu DNS, các mẫu thông tin này được lưu trong file cơ sở dữ liệu DNS

- Có rất nhiều loại RR khác nhau. Khi một zone mới được tạo ra, DNS tự động thêm 2 RR vào zone đó: `Start of Authority(SOA)` và `Name Server(NS)`

<a name="2"></a>

# 2. Các kiểu Resource Record

<a name="21"></a>

## 2.1 SOA (Start of Authority)

- Trong mỗi tập tin cơ sỡ dữ liệu DNS phải có một và chỉ một record SOA. Bao gồm các thông tin về DNS server, thông tin về zone transfer

- Cú pháp:
```
[tên miền] IN SOA [tên-server-dns] [địa-chỉ-email] (serial number;refresh number;retry number;experi number;time-to-live number)
```

```
- tên miền: Là tên mà DNS quản lý
- tên server dns: Tên server quản lý miền
- Refresh number: Chỉ ra khoảng thời gian máy chủ Secondary kiểm tra dữ liệu zone trên máy Primary để cập nhật nếu cần
- TTL: Gía trị này áp dụng cho mọi record trong zone và được đính kèm thông tin trả lười một truy vấn. Mục đích của nó là chỉ ra thời gian mà các máy chủ name server khác cache lại thông tin trả lời
```

<a name="22"></a>

## 2.2 NS (Name Server)

Bản ghi NS dùng để khai báo máy chủ tên miền cho một tên miền. Nó cho biết các thông tin về tên miền quản lý, do đó yêu ccaauf có tối thiểu hai bản ghi NS cho mỗi tên miền

- Cú pháp:

```
[domain_name] IN NS [DNS-Server_name]
```

- Ví dụ:

```
vnnic.net.vn       IN      NS      dns1.vnnic.net.vn
vnnic.net.vn       IN      NS      dns2.vnic.net.vn
```

Với khai báo trên, tên miền vnnic.net.vn sẽ do máy chủ tên miền có tên dns.vnnic.net.vn quản lý.

<a name="23"></a>

## 2.3 A (Address) và CNAME(Canonical Name)

Record A ánh xạ tên vào địa chỉ. Record CNAME tạo tên bí danh alias trỏ vào một tên canonical. Tên canonical là tên host trong record A hoặc trỏ vào 1 tên canonical khác.

<a name="231"></a>

### 2.3.1 Bản ghi kiểu A

A record - Address record: Dùng để phân giải host ra một địa chỉ IPv4, dùng để trỏ tên website như www.domain.com đến một server hosting website đó

Bản ghi kiểu A có cú pháp như sau:

```
[Domain]       IN       A      <dịa chỉ IP của máy>

home.vnn.vn    IN       A        203.162.0.12
```

Teho ví dụ trên, tên miền `home.vnn.vn` được khai với bản ghi kiểu A trỏ đến địa chỉ 203.162.0.12 sẽ là tên của máy tính này. Một tên miền có thể được khai báo nhiều bản ghi kiểu A khác nhau để trỏ đến các địa chỉ IP khác nhau. Như vậy có thể có nhiều máy tính có cùng tên trên mạng. Ngược lại một máy tính có một địa chỉ IP có thể có nhiều tên miền trỏ đến, truy nhiên chỉ có duy nhất một tên miền được xác định là tên của máy, đó chính là tên miền được khai với bản ghi kiểu A trỏ đến địa chỉ của máy. 

<a name="232"></a>

### 2.3.2 Bản ghi CNAME

Record CNAME: Tạo tên bí danh (alias) trỏ vào Server Hosting website đó.Thông thường thì máy tính trên Internet có nhiều dịch vụ như Web Server, FTP Server, Chat Server, …. Để lọc hay nói nôm na là kiểm soát, CNAME Records đã được sử dụng.

Bản ghi CNAME có cú pháp như sau:

```
alias-domain    IN         CNAME       canonical domain

www.vnn.vn      IN         CNAME       home.vnn.vn
```

Tên miền `www.vnn.vn` sẽ là tên bí danh của tên miền `home.vnn.vn`, cả 2 tên này đều trỏ đến địa chỉ IP 203.16.0.12

<a name="24"></a>

## 2.4 AAAA

- Dùng để phân giải host ra một địa chỉ 128 bit IPv6

<a name="25"></a>

## 2.5 SRV

Cung cấp cơ chế định vị dịch vụ, Active Directory sử dụng resource record này để xác định domain controllers, global catalog servers, Lightweight Directory Access Protocol (LDAP) servers. Các trường trong record SVR :
- Tên dịch vụ service
- Giao thức sử dụng
- Tên miền domain name
- TTL và class
- Priority
- weight (hỗ trợ load balancing)
- Port của dịch vụ
- Target chỉ định FQDN cho host hỗ trợ dịch vụ

```
Lưu ý: FQDN (Fully Qualified Domain Name) là một địa chỉ tên miền đầy đủ, bao gồm cả tên máy chủ lưu trữ tên miền (hostname) và tên miền cấp cao hơn nhất để xác định một máy tính.
```

<a name="26"></a>

## 2.6 MX (Mail Exchange)

Dùng để xác định Mail Server cho một domain. Ví dụ khi bạn gởi email tới support@matbao.com, mail server sẽ xem xét MX Record matbao.com xem nó được điểu khiển chính xác bởi mail server nào (mail.matbao.com chẳng hạn) rồi tiếp đến sẽ xem A Record để chuyển tới IP đích. Để tránh việc gởi mail bị lặp lại, record MX có thêm một giá trị bổ sung ngoài tên miền của Mail Exchange là một số thứ tự tham chiếu. Đây là giá trị nguyên không dấu 16-bit (0-65535) chỉ ra thứ tự ưu tiên của các mail exchanger.

- Cú pháp:
```
[domain_name] IN MX [priority] [mail-host]
```

- Ví dụ:
    - matbao.com. IN MX 10 mail.matbao.com.
    - Chỉ ra máy chủ mail.matbao.com là 1 Mail Exchanger cho Domain matbao.com với độ ưu tiên là 10.

<a name="27"></a>

## 2.7 PTR(Pointer)

Phân giải địa chỉ IP sang host name

- Cú pháp:

```
[Host-ID.{Reverse_Lookup_Zone}] IN PTR [tên-máy-tính]
```

- Ví dụ:
```
112.2.78.100.in-addr.arpa. IN PTR matbao.com.
```
Bản ghi PTR trên cho phép tìm tên miền `matbao.vn` khi biết địa chỉ IP 112.2.78.100 mà tên miền trỏ tới


# Tài liệu tham khảo
- https://wiki.matbao.net/kb/mot-so-dinh-nghia-ve-cac-dns-record/
- http://servergiarenhat.com/dns-server-la-gi-cac-kie%CC%89u-ba%CC%89n-ghi-dns/