## MỤC LỤC

- [1. Cấu trúc rules](#1)
- [2. Test rules (emerging-dns.rules)](#2)

## NỘI DUNG

### 1. Cấu trúc rules

### 1.1 Action

Action là một thuộc tính của signatures giúp xác định điều gì xảy ra khi signatures matches. Có 4 kiểu action.

1. Pass: Nếu signature matches và bao gồm pass, Suricata dừng quét các gói tin và bỏ qua tất cả các rules (chỉ đối với gói tin hiện tại)

2. Drop: Chỉ quan tâm tới IPS/inline mode. Nếu chương trình tìm thấy signature matches, chứa drop nó dừng ngay lập tức. Các gói tin sẽ không được gửi tiếp. Hạn chế: the receiver không nhận được thông báo điều gì đang diễn ra, dẫn đến cần time-out. **Suricata tạo một alert cho gói tin này**.

3. Reject: là từ chối hoạt động của một gói tin. Cả receiver và sender nhận một gói tin từ chối. Có 2 kiểu gói tin từ chối được lựa chọn một cách tự động. Nếu gói tin đang vi phạm liên quan đến TCP, nó sẽ là Reset-packet. Đói với tất cả các giao thức khác nó là ICMP-error packet. **Suricata cũng tạo ra alert**. Trong inline/ÍPS mode, gói tin vi phạm sẽ bị drop giống như drop action.

4. Alert: Nếu signature matches và chứa alert, các gói tin sẽ được đối xử như bất kỳ các gói không đe dọa khác, ngoại trừ việc gói này sẽ được alert bởi suricata.


#### Protocol

Các giao thức mà suricata quan tâm: 4 giao thức cơ bản: tcp, udp, icmp, ip.

Ngoài ra còn một số giao thức lớp ứng dụng: http, ftp, tls, dns, ssh, ...

Các giao thức này đều được cấu hình trong suricata.yaml

#### Source and Destination

Source và Destination IP, thông thường sử dụng 2 biến HOME_NET và EXTERNAL_NET. chúng ta có thể sử dụng các IP và khoảng IP cụ thể.

#### Port

Gói tin được gửi đi hoặc đến cổng nào ví dụ giao thức ftp port 21, http port 80, dns port 53, ... any là tất cả các port.

### 2 Rule options:

### 2.1 Meta keywords

- msg (message): từ khóa msg đưa thông tin văn bản của dấu hiệu và cảnh báo có thể.

- sid(signature ID): id của signature

- rev: từ khóa sid đi kèm với rev. rev biểu diễn phiên bản của signature

- gid (group ID): gid sử dung các nhóm signature

- classtype: Thông tin của rules và cảnh báo. được định nghĩa trong classification.config

- reference: hướng tới nơi có thông tìn về signature

### 2.2 IP keywords

- ttl (time-to-live): Kiểm tra giá trị time-to-live trong header của packet. ttl xác định thời gian của gói tin trong hệ thống mạng. 

### 2.3 TCP keywords

- seq: kiểm tra TCP sequence number cụ thể.

- ack: báo nhận của các byte dữ liệu được gửi từ trước

- window: TCP window size cụ thể

### 2.4 Payload Keywords

- content: Từ khóa quan trọng nhất của một signature. Nội dung của signature trùng với content suricata sẽ thực hiện action tương ứng.

- nocase: từ khóa bổ nghĩa cho content. khi có từ khóa nocase nội dung signature so sánh với content trong rules không phân biệt viết hoa.

![](./Image/suri-rule1.png)

- depth: từ khóa bổ nghĩa cho content, mô tả số byte bắt đầu từ offset (đầu payload + offset) sẽ được check, depth và offset thường đi với nhau

![](./Image/suri-rule2.png)

- distance: từ khóa chỉ ra sự liên hệ giữa các content. distance được tính bằng số byte các content cách nhau.

- isdataat: xem xét dữ liệu vẫn còn 1 phần nào đó ở payload

### 2.5 Prefiltering keywords

- fast_pattern: bổ nghĩa cho content trước nó. nội dung kiểm tra nhanh.

### 2.6 flow keywords

- 