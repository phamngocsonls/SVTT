# Lab phân giải tên meienf sử dụng Bind9

##Mục lục

- [1. Cấu hình trên Primary DNS server](#1)
- [2. Cấu hình trên Secondary DNS server](#2)
- [3. Cấu hình trên Client](#3)


# Các tham số sử dụng trong bài lab này

- `huong.com`: domain name được sử dụng
- 172.16.69.0/24 là dải private sử dụng trong bài lab này

# Mô hình cụ thể

|**Host**|**FQDN**          |**IP Address**    |**Ghi chú**          |
|--------|:----------------:|:----------------:|--------------------:|
| ns1    | ns1.huong.com    | 172.16.69.141    | Primary DNS server  |
| ns2    | ns2.huong.com    | 172.16.69.142    | Secondary DNS server|
| host1  | host1.huong.com  | 172.16.69.143    | client              |

<a name="1"></a>

## 1. Cấu hình trên Primary DNS server

Đầu tiên, cấu hình IP tĩnh cho Primary DNS server theo mô hình bài lab có địa chỉ `172.16.69.141`

Thực hiện sửa hosts file có nội dung như sau:

```
vi /etc/hosts
```

```
127.0.0.1       localhost
127.0.1.1       ubuntu

# Dong ta moi them vao
172.16.69.141   ns1.huong.com ns1


# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

### Cài đặt Bind9

- Cài đặt gói Bind9

```
apt-get -y install bind9 bind9utils bind9-doc
```

Thực hiện cấu hình BIND chạy trong chế độ IPv4. Thêm `-4` vào trong biến OPTIONS

```
vi /etc/default/bind9
```

```
# run resolvconf?
RESOLVCONF=no

# startup options for the server
OPTIONS="-4 -u bind"  
```

- Sau khi cài đặt thành công, tất cả các file cài đặt nằm tại `/etc/bind`

### Cấu hình options file

Đầu tiên, chúng ta định nghĩa một access control list có tên là `trusted`, nó cho phép ta xác định clients nào sẽ được phép truy vấn tới DNS server. ACL này có thể định nghĩa theo 1 IP cụ thể hoặc có thể là 1 dải subnet nào đó.

```
// Define subnet
acl "trusted" {
        172.16.69.0/24;   # lab network
};
```

Trong `options`, thực hiện thêm 1 vài thông số như sau:

```
        recursion yes;                 # co phép gửi lại truy vấn
        allow-recursion { trusted; };  # cho phép truy vấn từ các client mà đã được định nghĩa
        listen-on { 172.16.69.141; };  # địa chỉ của Primary DNS server
        allow-transfer { none; };      # disable zone transfers by default 

        forwarders {
                8.8.8.8;
                8.8.4.4;
        };
```

### Cấu hình Local DNS Zones

Tại đây, thực hiện cấu hình forward và reverse DNS zones trong file `named.conf.local`

```
vi /etc/bind/named.conf.local
```

- Thêm forward zone có tên là `huong.com`

```
zone "huong.com" {
    type master;
    file "/etc/bind/zones/db.huong.com";       # đường dẫn định nghĩa file zone
    allow-transfer { 172.16.69.142; };         # ns2 private IP address – secondary
};
```

Thêm reverse zone cho subnet 172.16.69.0/24

```
zone "69.16.172.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/db.172.16.69";   # đường dẫn định nghĩa file zone
    allow-transfer { 172.16.69.142; };     # ns2 private IP address – secondary
};
```

### Khởi tạo forward zone file

Hai zone file chúng ta cần cấu hình nằm tại đường dẫn `/etc/bind/zones`

Trước hết cần khởi tạo `zones` directory trong `/etc/bind`

![Imgur](https://i.imgur.com/2SLyHcQ.png)

Thực hiện copy file cấu hình mẫu `db.local` vào file `db.huong.com` nằm tại `/etc/bind/zones`

Nội dung file cấu hình mẫu như sau:

```
;
; BIND data file for local loopback interface
;
$TTL    604800
@       IN      SOA     localhost. root.localhost. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      localhost.
@       IN      A       127.0.0.1
@       IN      AAAA    ::1
```

Thực hiện chỉnh sửa file cấu hình mẫu, ta có file cấu hình `db.huong.com` hoàn chỉnh như sau:

```
;
; BIND data file for local loopback interface
;
$TTL    604800
@       IN      SOA     ns1.huong.com. admin.huong.com. (
                              3         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;

; name servers - NS records
        IN      NS      ns1.huong.com.    // tên miền phân giải cho DNS server(Primary DNS server)
        IN      NS      ns2.huong.com.    // tên miền phân giải cho DNS server(Secondary DNS server)
;

; name servers - A records
ns1.huong.com.  IN      A       172.16.69.141   // địa chỉ của Primary DNS server
ns2.huong.com.  IN      A       172.16.69.142   // địa chỉ của Secondary DNS server
;


; 172.16.69.0/24 - A records

host1.huong.com.        IN      A       172.16.69.143
```

- Trong đó

```
- ns1.huong.com. : Là địa chỉ mà dns phân giải cho DNS server
- admin.huong.com. : Là địa chỉ email
```

### Cấu hình Reverse zone file

Copy file cấu hình mẫu `db.127` vào file cấu hình nghịch `db.172.16.69`

Nội dung file cấu hình mẫu như sau:

```
;
; BIND reverse data file for local loopback interface
;
$TTL    604800
@       IN      SOA     localhost. root.localhost. (
                              1         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      localhost.
1.0.0   IN      PTR     localhost.
```

Thực hiện chỉnh sửa file cấu hình mẫu, ta có được reverse zone file như sau:

```
;
; BIND reverse data file for local loopback interface
;
$TTL    604800
@       IN      SOA     ns1.huong.com. admin.huong.com. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;

; name servers - NS records
        IN      NS      ns1.huong.com.
        IN      NS      ns2.huong.com.
;

; PTR Records
41      IN      PTR     ns1.huong.com.          ;địa chỉ gán với ns1.huong.com, Secondary DNS server
42      IN      PTR     ns2.huong.com.          ;địa chỉ gán với ns2.huong.com, Secondary DNS server
43      IN      PTR     host1.huong.com.        ;địa chỉ của client để thực hiện tets
```

### Kiểm tra các file cấu hình đã thực hiện

- Kiểm tra cú pháp file cấu hình

```
named-checkconf
```

Nếu các file cấu hình đúng, ta sẽ không thấy có kết quả gì tra về

![Imgur](https://i.imgur.com/EWd9Ej4.png)

- Thực hiện kiểm tra forward zone và file cấu hình của forward đó

```
named-checkzone /etc/bind/named.conf.local db.huong.com
```

Kết quả trả về như sau, có nghĩa là các file cấu hình đã được thực hiện đúng

![Imgur](https://i.imgur.com/HJJGfQd.png)


- Thực hiện kiểm tra reverse zone và file cấu hình

```
named-checkzone /etc/bind/named.conf.local db.172.16.69
```

Kết quả trả về báo các file đã được cấu hình đúng

![Imgur](https://i.imgur.com/gl2DTIE.png)


### Restart BIND

```
service bind9 restart
```


<a name="3"></a>

## 2. Cấu hình trên Client

- Thực hiện chỉnh sửa `head` file trên client, thêm các dòng như private domain, địa chỉ của DNS server như sau:

```
vi /etc/resolvconf/resolv.conf.d/head
```

```
search huong.com
nameserver 172.16.69.141
nameserver 172.16.69.142
```

- Run `resolvconf` để tạo file mới `resolv.conf`.

```
resolvconf -u
```

## Test forward lookup

```
nslookup host1
```

- Kết quả trả về

![Imgur](https://i.imgur.com/ZxPbnc1.png)


## Query ns1 sử dụng DIG

```
dig huong.com any @ns1.huong.com
```

- Kết quả trả về như sau:

```
; <<>> DiG 9.10.3-P4-Ubuntu <<>> huong.com any @ns1.huong.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 31484
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;huong.com.                     IN      ANY

;; ANSWER SECTION:
huong.com.              604800  IN      SOA     ns1.huong.com. admin.huong.com. 3 604800 86400 2419200 604800
huong.com.              604800  IN      NS      ns2.huong.com.
huong.com.              604800  IN      NS      ns1.huong.com.

;; ADDITIONAL SECTION:
ns1.huong.com.          604800  IN      A       172.16.69.141
ns2.huong.com.          604800  IN      A       172.16.69.142

;; Query time: 0 msec
;; SERVER: 172.16.69.141#53(172.16.69.141)
;; WHEN: Sun Oct 28 18:15:22 PDT 2018
;; MSG SIZE  rcvd: 148
```


# Tài liệu tham khảo
- https://techpolymath.com/2015/02/16/how-to-setup-a-dns-server-for-a-home-lab-on-ubuntu-14-04/
- https://linuxtechlab.com/configuring-dns-server-using-bind/
- https://www.howtoforge.com/two_in_one_dns_bind9_views
- https://www.digitalocean.com/community/tutorials/how-to-configure-bind-as-a-private-network-dns-server-on-ubuntu-14-04