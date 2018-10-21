# Lab phân giải tên meienf sử dụng Bind9


# Các tham số sử dụng trong bài lab này

- `huong.com`: domain name được sử dụng
- 172.16.69.0/24 là dải private sử dụng trong bài lab này

# Mô hình cụ thể

|**Host**|**FQDN**          |**IP Address**    |**Ghi chú**         |
|ns1     |ns1.huong.com     |172.16.69.141     |Primary DNS server  |
|ns2     |ns2.huong.com     |172.16.69.142     |Secondary DNS server|
|host1   |host1.huong.com   |172.16.69.143     |client              |

////