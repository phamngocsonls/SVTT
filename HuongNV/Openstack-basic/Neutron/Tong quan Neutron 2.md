# Neutron Networking

## Mục lục
- [1. Features](#1)
- [2. Neutron vs Nova Networks](#2)
- [3. Architecture vs Internals](#3)
    - [3.1 Neutron server](#31)
    - [3.2 L2 Agents](#32)
    - [3.3 L3 Agents](#33)


<a name="1"></a>

# 1. Features

*Neutron là một dự án thuộc Openstack để cung cấp kết nối mạng như một dịch vụ giữa các interface device với nhau và được quản lý bởi các giao dịch vụ Opnestack khác*

Neutron cung cấp một tập các API và giao diện plugin được phát triển bởi bên thứ 3 nhằm xây dựng một cơ sở hạ tầng mạng mạnh mẽ với khả năng mở rộng. 

Một vài tính năng cốt lõi như:
- **Has a Unified API & Core**: Networking can be complex because of multiple device support. Keeping API’s small make it much easier to accommodate and maintain many types of devices. 
- **Overlapping IP stack**: As we will find, neutron can provide isolated tenant networks within a project. This is because of overlapping IP stack.
- **Floating IPs**: Cho phép ánh xạ địa chỉ IP public và gắn chúng vào các virtual interface của các VM
- **Pluggable Open Arch**: Many ways to achieve L2 connectivity. This type of pluggable Open Architecture allows to create such architecture.
- **Extensible**: Cung cấp extension định tuyến mở rộng, các extensions liên quan tới bảo mật, các extensions liên quan tới LoadBlance
- **Security Groups**: Đóng vai trò là tường lửa ảo nhằm keiemr soát lưu lượng vào ra trên từng instances

<a name="2"></a>

# 3. Neutron vs Nova Networks
Neutron là một plugin được thiết kế để có thể mở rộng. Hầu hết các tính năng mở rộng được cung cấp bởi các tác nhân có thể xếp chồng lên nhau một cách tuyến tính để mở rộng quy mô. Điều này làm cho nó rất dễ dàng để duy trì các tính năng cốt lõi, đồng thời dễ dàng thêm các tính năng bổ sung.

Biểu đồ dưới đây trình bày các thành phần bên trong Neutron. Neutron bao gồm 3 thành phần, một máy chủ Neutron server, một lớp cơ sở dữ liệu, các plugin như L2 agent, L3 agent, DHCP agent. Cơ sở dữ liệu này được kết nối với một Neutron server.

![Imgur](https://i.imgur.com/8HeWdPN.png)

## 3.1 Neutron server
Neutron server được chia nhỏ thành 3 phần chính. Hai phần đầu tiên của lõi API khá rõ ràng. Một dịch vụ cung cấp giao diện API, các dịch vụ khác nói chuyện với message queue. 

![Imgur](https://i.imgur.com/aw5YVOI.png)

Third party Plugins là một thành phần cốt lõi và đóng vai trò rất quan trọng của Neutron.

### ML2 Plugin
Plugin này có thể là một plugin cốt lõi nguyên khối, là tùy chọn mặc định, sử dụng một số lượng lớn các giải pháp mạng L2 hiện có. Nó hỗ trợ OVS, linux bridge và Hyper V. 

### Type Driver
Dựa trên loại mạng như local, flat, VLAN, GRE hoặc VXLAN, TypeDrivers cung cấp trình điều khiển cho loại mạng cụ thể đó. TypeDrivers cung cấp trạng thái mạng cho từng loại cụ thể và cấp cấp tính xác thực.

<a name="32"></a>

# 3.2 L2 Agents
L2 agents chạy trên compute node. Nhiệm vụ chính của nó là cấu hình các virtual bridge trên mỗi node compute đó. Nó theo dõi việc thêm, bớt các device gán vào các virtual bridge đó. Ngoài ra nó cũng xử lý các nhóm quy tắc bảo mật security groups. 

Biểu đồ dưới đây giúp ta hiểu rõ hơn về L2 agents. Khi một instance được khởi tạo, nova compute sẽ add một tap interface(một card ảo) và gửi một request tới Neutron với yêu cầu cấp phát một địa chỉ IP.

![Imgur](https://i.imgur.com/q3WayWc.png)

<a name="33"></a>

# 3.3 L3 Agents
Trong khi L2 agents cho phép các virtual machine được kết nối tới các mạng thì L3 agents sẽ kết nối các bộ định tuyến với nhau, cung cấp các tài nguyên sẵn sàng cho mạng. L3 agents chạy trên Network node

Ngoài ra, neutron còn cung cấp floating IP, nó cho phép các virtual machine kết nối ra bên ngoài internet và ngược lại. Ví dụ sau giúp chúng ta hiểu rõ hơn chức năng của floating IP:

![Imgur](https://i.imgur.com/iVvcRnj.png)

Các VM được khởi tạo với địa chỉ lần lượt là 10.10.10.5, 10.10.10.6 và 10.10.10.7. Vấn đề xảy ra tại đây là các VM có thể ping được ra internet. nhưng chiều ngược lại thì lại không được. 

Ví dụ, gửi một gói tin từ VM1 ra bên ngoài internet có destination address là `56.57.58.59`. Gói tin có địa chỉ nguồn là `10.10.10.5`, địa chỉ đích là `56.57.58.59` đi tới router ảo có tên là EXT_VR, tại đây EXT_VR sẽ thay đổi địa chỉ nguồn của gói tin thành `192.168.0.19` và gửi gói tin tới địa chỉ đích là 56.57.58.59

Chiều ngược lại, gói tin từ bên ngoài với địa chỉ nguồn là IP public đi tới virtual router, dựa trên các thông tin của packets đó, virtual router không thể xác định được destination của gói tin đó đi tới VM nào và gói tin sẽ bị drop.



