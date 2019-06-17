
# Server Load Balancing

Bài viết này sẽ sử dụng chức năng Server Load Balancing của `pfSense` để đảm bảo cho server hoạt động ổn định.
Mô hình: Lab sẽ thực hiện trên  máy chủ web đặt tại vùng DMZ, 2 web server có địa chỉ IP là:
````
192.168.2.69
192.168.2.70
````

* Vào Services/Load Balancer/Monitors chọn một dịch vụ được định nghĩa sẵn, ở đây là HTTP. Chỉnh sửa như hình, ở đây để host chính của web server là 192.168.2.69

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/l1.png?raw=true)

* Vào mục Pools của Load Balancer, thiết lập như hình. Chú ý để Monitor là HTTP(vừa định nghĩa ở trên). Add 2 địa chỉ IP web server vài Server IP Address. 

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/l2.png?raw=true)

* Vào mục Virtual Servers. Mục đích của phần này là tạo 1 địa chỉ IP ảo để gộp 2 IP web server vào làm 1. Thiết lập như hình dưới. Mục Virtual Server Pool và Fall-back Pool chọn tên  pool vừa tạo ở bước trên.

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/l3.png?raw=true)

* Kết quả:
![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/l4.png?raw=true)
