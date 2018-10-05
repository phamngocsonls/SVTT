# OVS LABS (cont)
## [0. Giới thiệu về Mininet](#tongquan)
### [0.1. Một số topo cơ bản](#basic)
### [0.2. Kiểm tra Flow Table](#flowtb)
---
## <a name="tongquan"></a> 0. Giới thiệu về Mininet
Mininet là phần mềm giả lập mạng cho phép tạo switch, host và kết nối giữa chúng để phục vụ mục đích kiểm thử.

### Cài đặt Mininet
#### Clone source code:
```sh
git clone git://github.com/mininet/mininet
```

#### Install:
```sh
mininet/util/install.sh [options]
```
Các options cụ thể như sau:
- ```a```: cài đặt mọi thứ được chứa trong máy ảo Mininet, gồm cả các phụ thuộc (dependencies) như Open vSwitch cũng như các phần bổ sung như trình giải mã (dissector) OpenFlow Wireshark và POX. (Mặc định, các công cụ này sẽ được build trong các thư mục được tạo trong thư mục chính của bạn.)
- ```nfv```: cài đặt Mininet, OpenFlow reference switch và Open vSwitch 

#### Tạo một topology mặc định với command ```sudo mn```

![](images/Labs/Mininet/0_1.png)

#### Mininet cho phép sử dụng một số command từ trình shell mặc định của Linux. Để thực hiện điều đó, thêm ```sh``` vào trước mỗi lệnh trên trình shell của mininet

![](images/Labs/Mininet/0_2.png)

#### Kiểm tra cấu hình các OVS bridge sau khi có được topo mặc định ( 2 host và 1 switch)

![](images/Labs/Mininet/0_3.png)

#### Kiểm tra topo mặc định
- Kiểm tra các node, ở đây topo mặc định sẽ bao gồm hai host **h1**, **h2**, một switch **s1** kết nối với hai host và kết nối với controller **c0**.

![](images/Labs/Mininet/0_4.png)

- Kiểm tra chi tiết hết về mỗi thành phần trong topo. Sử dụng command ```dump```

![](images/Labs/Mininet/0_5.png)

- Kiểm tra kết nối giữa các node. Sử dụng command ```net```

![](images/Labs/Mininet/0_6.png)

- Ping thử giữa hai host

![](images/Labs/Mininet/0_7.png)

- Thử command trên một host

![](images/Labs/Mininet/0_8.png)

- Kiểm tra kết nối giữa toàn bộ các hót. Sử dụng command ```pingall```

![](images/Labs/Mininet/0_9.png)

- Thoát khỏi mininet

![](images/Labs/Mininet/0_10.png)

- Xóa bỏ toàn bộ các zombie process liên quan đến các thao tác với mininet ở trên

![](images/Labs/Mininet/0_11.png)

### <a name="basic"></a> 0.1. Một số topo cơ bản
#### 0.1.1. Tạo topo với 4 host và 1 switch
- Tạo topo: ```sudo mn --topo=single,4```

![](images/Labs/Mininet/1_0.png)

- Kiểm tra trạng thái của OVS bridge: ```sh ovs-vsctl show``` 

![](images/Labs/Mininet/1_1.png)

- Kiểm tra số lượng node: command ```nodes```, kiểm tra liên kết giữa các node: ```net```

![](images/Labs/Mininet/1_2.png)

#### 0.1.2. Tạo topo tuyến tính với 4 nodes
- Tạo topo: ```sudo mn --topo=linear,4```

![](images/Labs/Mininet/1_3.png)

- Kiểm tra trạng thái của OVS bridge: ```sh ovs-vsctl show```

```sh 
mininet> sh ovs-vsctl show
42af9da6-8f90-4895-b686-52a37c917e4e
    Bridge "s4"
        Controller "ptcp:6657"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: secure
        Port "s4-eth2"
            Interface "s4-eth2"
        Port "s4-eth1"
            Interface "s4-eth1"
        Port "s4"
            Interface "s4"
                type: internal
    Bridge "s3"
        Controller "ptcp:6656"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: secure
        Port "s3-eth3"
            Interface "s3-eth3"
        Port "s3-eth1"
            Interface "s3-eth1"
        Port "s3"
            Interface "s3"
                type: internal
        Port "s3-eth2"
            Interface "s3-eth2"
    Bridge "s2"
        Controller "ptcp:6655"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: secure
        Port "s2-eth3"
            Interface "s2-eth3"
        Port "s2"
            Interface "s2"
                type: internal
        Port "s2-eth2"
            Interface "s2-eth2"
        Port "s2-eth1"
            Interface "s2-eth1"
    Bridge "s1"
        Controller "ptcp:6654"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: secure
        Port "s1-eth1"
            Interface "s1-eth1"
        Port "s1"
            Interface "s1"
                type: internal
        Port "s1-eth2"
            Interface "s1-eth2"
    ovs_version: "2.9.2"
```

- Kiểm tra liên kết giữa các nodes: ```links```

![](images/Labs/Mininet/1_4.png)

- Topo tuyến tính sẽ có dạng như sau:
```sh

                   h2     h3
                   +       +
                   |       |
                   +       +
     h1-----s1-----s2-----s3-----s4-----h4
            +      +       +      +
            |      |       |      |
            |      +-------+      |
            +-------+ c0 +--------+
                    +----+

```

#### 0.1.3. Tạo topo dạng tree với 4 host và 3 switch

- Tạo topo với command ```sudo mn -topo=tree,2,2```

![](images/Labs/Mininet/1_5.png)

- Kiểm tra status của OVS

```sh
mininet> sh ovs-vsctl show
42af9da6-8f90-4895-b686-52a37c917e4e
    Bridge "s1"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        Controller "ptcp:6654"
        fail_mode: secure
        Port "s1"
            Interface "s1"
                type: internal
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1-eth1"
            Interface "s1-eth1"
    Bridge "s2"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        Controller "ptcp:6655"
        fail_mode: secure
        Port "s2-eth2"
            Interface "s2-eth2"
        Port "s2"
            Interface "s2"
                type: internal
        Port "s2-eth1"
            Interface "s2-eth1"
        Port "s2-eth3"
            Interface "s2-eth3"
    Bridge "s3"
        Controller "ptcp:6656"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: secure
        Port "s3"
            Interface "s3"
                type: internal
        Port "s3-eth3"
            Interface "s3-eth3"
        Port "s3-eth2"
            Interface "s3-eth2"
        Port "s3-eth1"
            Interface "s3-eth1"
    ovs_version: "2.9.2"
```

- Kiểm tra số node, thông tin IP và kết nối của chúng

![](images/Labs/Mininet/1_6.png)

- Topo dạng tree sẽ có dạng như sau

```sh
                        s1
                         +
h1+---------+            |          +----------+h4
            |            |          |
            |            |          |
            +            |          +
h2+--------+s2           |         s3+----------+h3
             +--------+  |  +-------+
                      +--+--+
                      | c0  |
                      +-----+

```

### <a name="flowtb"></a> 0.2. Kiểm tra Flow Table
#### Tạo topo gồm 4 host nối vào 1 switch, sử dụng tùy chọn ```--mac``` để giữ địa chỉ MAC cho các host

![](images/Labs/Mininet/2_0.png)

#### Thực hiện dump cấu hình của các port trên OVS bridge. Các host kết nối với các port riêng biệt của switch.
Command ```sh ovs-ofctl dump-ports-desc s1``` cho phép match số hiệu port với tên port. (Trong các flow table, ta chỉ thấy được số hiệu port, do đó command này sẽ hữu ích để tiện theo dõi hơn)

![](images/Labs/Mininet/2_1.png)

- Kiểm tra thông tin thống kê của mỗi port. Sử dụng command: ```sh ovs-ofctl dump-ports s1```

![](images/Labs/Mininet/2_2.png)

- In ra flow table do **ovs-vswitchd** quản lý: ```sh ovs-ofctl dump-flows s1```

```sh
mininet> sh ovs-ofctl dump-flows s1
mininet> 
```

Chưa có entry nào do chưa có bất kì kết nối nào giữa các host.

Thử kiểm tra controller điều khiển vswitch **s1**: ```sh ovs-vsctl get-controller s1```

![](images/Labs/Mininet/2_3.png)

#### Tạo traffic đơn giản bằng cách ping giữa host **h1** và **h2**: ```h1 ping -c5 h2```

![](images/Labs/Mininet/2_4.png)

Ta thấy rằng, gói tin đầu tiên có RTT (Round Trip Time) lâu hơn do đó là gói tin đầu tiên của flow mới từ **host 1** gửi tới switch **s1**, switch chưa xử lý được nên sẽ gửi lên controller xử lý rồi mới gửi lại switch để chuyển tiếp sang **host 2**. Những gói tin tiếp theo do cùng flow nên thực hiện **flow matching** thành công ngay tại switch và chuyển trực tiếp sang **host 2** mà không cần lên hỏi controller nên RTT sẽ ngắn hơn.

- Thử dump-flow table lại: ```sh ovs-ofctl dump-flows s1```

![](images/Labs/Mininet/2_5.png)

Ta thấy, ARP rule đã được đưa thêm vào flow table. Output port là các port mà gói tin sẽ được forward ở đầu ra của pipeline trên switch. Số hiệu port tương ứng với các port dump ở command ```sh ovs-ofctl dump-ports-desc s1```.

#### Xóa các flow entry hiện tại trên flow table của switch

![](images/Labs/Mininet/2_6.png)

#### Sử dụng Wireshark để bắt gói tin ping từ h1 sang h2
- Khởi động Wireshark trên trình shell chính của Linux, lắng nghe trên cổng loopback.
Command: ```sudo wireshark```

- ping từ **h1** sang **h2** trên shell của mininet: ```h1 ping -c5 h2```

![](images/Labs/Mininet/2_8.png)

#### Dump flow table của switch

![](images/Labs/Mininet/2_10.png)

#### Quan sát các gói tin wireshark đã bắt được

![](images/Labs/Mininet/ws1.png)

Ta thấy các frame 316, 320, 331, 334, 337, 341 là các bản tin tương ứng hành động add-flow của controller để tạo ra 6 flow entry như kết quả dump-flow table ở trên.

- Mở frame 316 - là frame đã add entry đầu tiên vào switch.

![](images/Labs/Mininet/ws2.png)

#### Đợi sau hơn 60s ping lại từ h1 sang h2

- Thời gian reply đầu tiên (một lần nữa) mất nhiều thời gian hơn bởi vì gói tin đã đi theo đường (h1–> s1–> c1–> s1–> h2) giống như đã trình bày ở trên.
- Giá trị ```Idle time-out``` (60s), cho biết thời gian bao lâu kể từ khi bắt được gói tin thì flow sẽ bị inactive. Vì vậy, khi ta ping lại giữa hai host sau 60s thì flow phải được thiết lập lại.
- Thử ping lại ngay sau thao tác ping trên:

![](images/Labs/Mininet/2_12.png)

Thời gian reply đầu tiên không quá lâu như lần ping trước đó vì flow trên vẫn còn "hiệu lực".


