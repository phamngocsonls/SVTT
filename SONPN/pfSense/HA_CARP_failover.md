# Cài đặt HA và CARP failover cho hệ thống 2 pfsense

Bài viết này sẽ hướng dẫn sử dụng tính năng High Availability Sync để thiêt lập và đồng bộ nhanh hệ thống sử dụng 2 pfsense để backup sử dụng CARP failover.

Tính năng `High Availability Sync` cho phép đồng bộ nhanh thiết lâp giữa 2 hệ thống pfsense cùng một mạng, đây là tính năng giúp tiết kiệm thời gian khi người dùng muốn xây dựng hệ thống backup như CARP failover.

### Thiết lập High Availability Sync
Để thiết lập `High Availability Sync` cần chuẩn bị 2 máy chạy pfsense, thiết lập 1 máy sẽ mặc định làm `Master` còn máy còn lại sẽ làm `Backup`. 

Mô hình mạng: 192.168.2.72, 192.168.69.50 sẽ là đường mạng ảo chung.
![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a11.png?raw=true)


* Truy cập vào giao diện web của pfSense1 chọn `System` -> `High Availability Sync` sau đó chọn vào Synchronize states và thiết lâp Sysnc đối vào mạng LAN. Tiếp tục điền vào mục pfsync Synchronize Peer IP địa chỉ IP LAN của máy pfSense 2 và Synchronize Config to IP cũng điền địa chỉ IP LAN của máy pfSense 2: 192.168.69.3

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a1.png?raw=true)
 
Trong mục Select optitons to syns tích hết và bỏ lựa chọn DHCP Server settings, vì chưa gộp đường mạng LAN cho mạng nên 2 máy pfSense sẽ tranh chấp việc cấp IP bằng DHCP server.

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a12.png?raw=true)


* Tạo đường mạng ảo: Tiến hành tạo 2 đường mạng ảo dành cho WAN và LAN. Phải tạo đường mạng chung vì trường hợp 1 trong 2 đường LAN chết, VM không biết phải đi qua đường 192.168.69.2 hay 192.168.69.3. Việc gộp chung 1 đường giúp khắc phục tình trạng này.
Vào Firewall / Virtual IPs tạo mạng ảo cho WAN mới với thiết lập như hình. Mục Type chọn CARP. 

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a2.png?raw=true)


* Tương tự tạp tiếp mạng đường mạng ảo mơi cho mạng LAN: 192.168.69.50
![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a3.png?raw=true)


* Đây là kết quả sau khi tạo 2 mạng ảo. Do bậy HA sync nên bên pfSense2 tự tạo Virtual IPs tương tự.
![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a4.png?raw=true)


* Chọn mục  `Available Widgets` và thêm CARP status để theo dõi trạng thái của 2 máy pfSense. Như hình máy 192.168.69.2 đang ở trạng thái `MASTER` còn 192.168.69.3 là `BACKUP` 
![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a5.png?raw=true)


* Thiết lập lại DHCP Server cho hệ thống. Vào `Services` -> `DHCP Server`. Ở `Gateway` điền IP của đường mạng LAN ảo vừa tạo. Mục `Failover peer IP` điền IP LAN của pfSense 2: 192.168.69.3

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a6.png?raw=true)


* Truy cập lại vào mục `System` -> `High Availability Sync` và tích chọn vào `DHCP server settings` để sysnc lại với máy pfSense2 sau đó Save lại

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a7.png?raw=true)


* Tiến hành test hệ thống. Hệ thống trước khi test:

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a8.png?raw=true)


* Tắt pfSense1. Như hình pfSense1 đã down, pfSense2 tự chuyển về chế độ `MASTER`:

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a9.png?raw=true)


* Tiến hành bật lại pfSense1, khoảng 5s pfSense1 và pfSense2 trở về trạng thái ban đầu:

![mw-ad-net.png](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/a10.png?raw=true)




Source: https://www.youtube.com/watch?v=FnZOT-7CKvQ&t=713s
