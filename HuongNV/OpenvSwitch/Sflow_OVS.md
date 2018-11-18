# Tìm hiểu về Sflow

## Mục lục
- [1. Mô hình](#1)
- [2. Cài đặt](#2)
    - [2.1 Trên host1](#21)
    - [2.2 Trên host2](#22)
- [3. Tài liệu tham khảo](#3)

Bài hướng dẫn này mô tả cách sử dụng OpenvSwitch và sFlow collector để theo dõi lưu lượng mạng giữa các VM với nhau. Các máy ảo này được kết nối tới software bridge, là OpenvSwitch.

<a name="1"></a>

## 1. Mô hình

Mô hình ở đây gồm 2 host:
- Host1: Máy ảo ubuntu desktop bản 16.04, cài OvS và KVM, có 1 card đi ra Internet là card ens33. 
- Host2: Là máy ảo trên đó cài sFlow Trend, sFlow nhận được các traffix từ host1 gửi tới và hiển thị các thông số dưới dạng biểu đồ như thông tin về memory, số lượng packet gửi và nhận, 

<a name="2"></a>

## 2. Cài đặt 

### 2.1 Trên host1

- Thực hiện tạo 1 bridge mới, tên là br1

```
ovs-vsctl add-br br1
```

- Gán port ens33 vào br1. Lưu ý sau khi gán xong, remove đi ip của card eth1 và thực hiện update lại ip cho br1

```
ovs-vsctl add-port br1 ens33
ifconfig ens33 0       # remove ip hiện tại của card ens33
dhclient br1           # update lại ip cho br1
```

![Imgur](https://i.imgur.com/SkAzrGO.png)

- Kiểm tra kết quả

```
ovs-vsctl show
```

![Imgur](https://i.imgur.com/gi850Ca.png)

- Tiếp theo, thực hiện tạo 2 máy ảo trên Virt-manager, ta dùng 2 image cirros cho nhẹ.

![Imgur](https://i.imgur.com/qoZovyB.png)

Hai máy ảo này đều kết nối tới br1, máy thứ nhất là kvm1 có địa chỉ IP là `20.20.20.219`, máy thứ 2 là kvm2 có IP là `20.20.20.215`. Hai máy ảo này thuộc dải NAT 20.20.20.0/24 và được NAT tới br1 và đi ra ngoài Internet.

![Imgur](https://i.imgur.com/ZAG6Pfk.png)

![Imgur](https://i.imgur.com/V7Q3p8r.png)


### 2.1.1 Cấu hình sFlow trên host1

Sử dụng command line sau để thực hiện add sflow vào br1 và forward trafic tới host2 có địa chỉ IP là 192.168.1.64

```
ovs-vsctl -- --id=@sflow create sflow agent=${AGENT_IP} target=\"${COLLECTOR_IP}:${COLLECTOR_PORT}\" header=${HEADER_BYTES} sampling=${SAMPLING_N} polling=${POLLING_SECS} -- set bridge br0 sflow=@sflow

ovs-vsctl -- --id=@sflow create sflow agent=ens33 target=\"192.168.1.64:6343\" header=128 sampling=64 polling=10 -- set bridge br1 sflow=@sflow
```

Trong đó: 
- COLLECTOR_IP: Địa chỉ của máy cài sFlow-RT, thực hiện thu thập các dữ liệu để monitor
- COLLECTOR_PORT: 6343 - là port mặc định dành riêng cho sFlow-RT
- AGENT_IP: Chỉ định port để gửi traffic 


Kiểm tra sFlow vừa tạo

```
ovs-vsctl list sflow
```

![Imgur](https://i.imgur.com/JkXI6Gp.png)


Remove sflow khỏi bridge, sử dụng:

```
ovs-vsctl remove bridge bridge_name sflow UUID
```

Trong đó
```
bridge_name: bridge muốn remove đi sflow
UUID: Là tên định danh cho sflow, có thể lấy UUID bằng cách liệt kê các sflow 
```
<a name="22"></a>

### 2.2 Trên host2

Thực hiện cài đặt sFlow-RT

```
wget http://www.inmon.com/products/sFlow-RT/sflow-rt.tar.gz
tar -xvzf sflow-rt.tar.gz
cd sflow-rt
./start.sh
```

Truy cập giao diện dashboard trên host2. Tại giao diện, chúng ta có thể quan sát rất nhiều thông số như lưu lượng của từng interface, traffic flow của các interface, tỉ lệ lỗi, bit error trên từng interface..

![Imgur](https://i.imgur.com/c5v6UDM.png)


- Ví dụ sau thực hiện ping kiểm tra kết nối internet của 2 VM, biểu đồ thể hiện lưu lượng in/out, các bản tin Unicast, Multicast, Broadcast, erorr được tính bằng bit/s, hiển thị rõ ràng cụ thể qua từng khung giờ

![Imgur](https://i.imgur.com/Qw7DijB.png)


Trên giao diện còn có các lựa chọn khác như: WAP erorr counter, WAP QoS counter...

![Imgur](https://i.imgur.com/OLBnGXV.png)


Biểu đồ sau thể hiện dưới dạng cột, có các lựa chọn như TOP sources, TOP destinations, TOP clients..

![Imgur](https://i.imgur.com/NnirFes.png)


Trên giao diện, có 1 tab gọi là `Circles`, tại đây thể hiện traffic flow của các VM qua 1 sơ đồ topology 

![Imgur](https://i.imgur.com/GGH2Z6V.png)


<a name="3"></a>

# 3. Tài liệu tham khảo
- https://adelnadjarantoosi.wordpress.com/2017/10/16/open-vswitch-network-monitoring-using-sflow-and-sflow-rt/
- http://docs.openvswitch.org/en/latest/howto/sflow/
- http://temp123.tistory.com/25



