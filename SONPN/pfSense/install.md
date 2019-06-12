
# Cài đặt thử nghiệm pfSense

## Chuẩn bị
> File ISO tải tại trang chủ: https://www.pfsense.org/download/
>  Virtual Box

## Cài đặt

Cấu hình:
* CPU: 2 core
* Disk: 5GB
* Ram 1GB
* Network Interface: 2 ( 1 Bridge, 1 Host only network)


Tạo máy ảo mới:

![1](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/1.png?raw=true)

Thêm file ISO vào đĩa khởi động:

![2](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/2.png?raw=true)

Cấu hình network interfaces như hình

 ![3](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/3.png?raw=true)
![4](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/4.png?raw=true)

Tiếp tục cấu hình tương tự như hình ( Enter liên tục nếu muôn cấu hình mặc định)

![5](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/5.png?raw=true)

![6](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/6.png?raw=true)

![7](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/7.png?raw=true)

![8](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/8.png?raw=true)

![9](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/9.png?raw=true)

Khi hiện màn hình yêu cầu Reboot, tắt máy ảo đi:

![10](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/10.png?raw=true)

Xóa đĩa khởi động, sau đó mở lại máy ảo pfSense:

![11](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/11.png?raw=true)

Đây là màn hình khi pfSense khởi xong:

![12](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/12.png?raw=true) 

Tiêp tục cấu hình mạng Wan. Đây là mạng đầu vào của pfSense, do máy host đang sử dụng ip 192.168.2.53, hiện tại 192.168.2.54 đang trống và ban đầu để chế độ Bridge nên lấy địa chỉ này cho Wan:

![13](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/13.png?raw=true)

Cấu hình như hình:

![14](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/14.png?raw=true)

Tiếp tuc kiểm tra địa chỉ mạng của card host only là 192.168.56.1. Chọn địa chỉ ip của LAN là 192.168.56.101. Có tùy chọn DHCP nếu muốn

![15](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/15.png?raw=true)

Cài đặt các tham số như hình:

![16](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/16.png?raw=true)

![17](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/17.png?raw=true)

Sau khi cài đặt thành công, truy cập vào địa chỉ 192.168.56.101 để đăng nhập GUI của pfSense. 
> account: admin
> password: pfsense

![18](https://github.com/phamngocsonls/SVTT/blob/phamngocsonls/SONPN/pfSense/image/18.png?raw=true)

