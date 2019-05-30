# OpenStack Networking

**Provider networks**

Provider network cung cấp kết nối layer-2 cho các máy ảo với các phiên bản có hỗ trợ dịch vụ DHCP và metadat. Các mạng này kêt nối hoặc được map với các mạng layer-2 có trong data center, thường sử dụng VLAN (802.1q) để xác định và phân tách nhau.
Provider networks cung cấp giải pháp đơn giản, hiệu quả và độ tin cậy với chi phí linh hoạt. Mặc định, chỉ có quản trị viên mới có thể tạo hoặc cập nhập provider networks vì nó yêu cầu cơ sở hạ tầng mạng vật lý. Bạn có thể thay đổi người dùng quản trị cho phép tạo tạo hoặc cập nhập provider network bằng cách thay đổi tham số cua fil epolicy.json:
``` sh
create_network:provider:physical_network
update_network:provider:physical_network
```
**Warning**

Việc tạo và sửa đổi provider networks cho phép sử dụng các tài nguyên mạng vật lý (Vd: Vlan-s). Cho phép những thay đổi trên chỉ dành cho những người thuê đáng tin cậy.

Ngoài ra, provider networks chỉ xử lý kết nối ở layer-2 cho các máy ảo, do đó không hỗ trợ cho các tính năng của bộ đinh tuyến và floating IP.

Trong nhiều trường hợp, các đơn vị khai thác đã quen thuộc với kiến trúc mạng ảo dựa trên nền tảng mạng vật lý cho layer-2, layer3 hoặc các dịch vụ khác có thể triển khai OpenStack Networking service. Provider networks khiến các đơn vị khai thác muốn chuyển từ Compute networking service (nova-network) sang  OpenStack Networking service. Theo thời gian, các đơn vị khai thác có thể xây dựng trên kiến trúc tối thiểu để có nhiều tính năng trên cloud networking.

Vì các thành phần chịu trách nhiệm cho việc vận hành kết nối layer 3 sẽ ảnh hưởng tới hiệu năng và tính tin cậy nên provider networks chuyển các kết nối này xuống tầng vật lí.
Trong một số trường hợp, triển khai Openstack nằm trong môi trường gồm các máy chủ ảo hóa và bare-metal hosts, thường sử dụng cơ sở hạ tầng mạng vật lý khác lớn. Các ứng dụng chạy bên trong OpenStack deployment có thể yêu cầu truy cập trực tiếp layer-2, thường là dùng Vlans.

<img src="https://camo.githubusercontent.com/bd61ac32e5ef2ebd5c557271c7c129aa30ea5e20/687474703a2f2f692e696d6775722e636f6d2f514d67786171642e706e67">

**Routed provider networks**

Routed provider networks cung cấp kết nối ở layer 3 cho các máy ảo. Các network này map với những networks layer 3 đã tồn tại. Cụ thể hơn, các layer-2 segments của provider network sẽ được gán các router gateway giúp chúng có thể được định tuyến ra bên ngoài chứ thực chất Networking service không cung cấp khả năng định tuyến. Routed provider networks tất nhiên sẽ có hiệu suất thấp hơn so với provider networks.
**Self-service networks**

Self-service networks chủ yếu sử dụng ở các project chung để quản lý mạng mà không liên quan đến quản trị viên. Các networks này đều là ảo và yêu cầu routers ảo để giao tiếp với provider và external networks. Self-service networks cũng cung cấp dịch vụ DHCP và metadata services cho máy ảo.

Trong hầu hết các trường hợp self-service networks sử dụng các giao thức như VXLAN hoặc GRE vì chúng hỗ trợ nhiều networks hơn là layer-2 segmentation sử dụng VLAN tagging (802.1q). Vlan thường yêu cầu cầu hình bổ sung ở tầng vật lý.
Với IPv4, self-service networks thường sử dụng dải mạng riêng(RFC1918)  và tương tác với provider networks thông qua cơ chế NAT trên router ảo. Floating IP cho phép truy cập vào các máy ảo từ provider networks thông qua cơ chế NAT trên router ảo. IPv6 self-service networks luôn sử dụng dải public IP  và tương tác với provider networks bằng giao thức định tuyến tĩnh qua router ảo.

Trái ngược lại với provider networks, self-service networks buộc phải đi qua layer-3 agent. Vì thế việc gặp sự cố ở một node có thể ảnh hưởng tới rất nhiều các máy ảo sử dụng chúng.

Các user có thể tạo các project networks cho các kết nối bên trong project. Mặc định thì các kết nối này là riêng biệt và không được chia sẻ giữa các project. OpenStack Networking hỗ trợ các công nghệ dưới đây cho project network:
- **Flat** 

Tất cả các instances nằm trong cùng một mạng, và có thể chia sẻ với hosts. Không hề sử dụng VLAN tagging hay hình thức tách biệt về network khác.
- **VLAN**

Kiểu này cho phép các users tạo nhiều provider hoặc project network sử dụng VLAN IDs(chuẩn 802.1Q tagged) tương ứng với VLANs trong mạng vật lý. Điều này cho phép các instances giao tiếp với nhau trong môi trường cloud. Chúng có thể giao tiếp với servers, firewalls, load balancers vật lý và các hạ tầng network khác trên cùng một VLAN layer 2.
- **GRE and VXLAN**

VXLAN và GRE là các giao thức đóng gói tạo nên overlay networks để kích hoạt và kiểm soát việc truyền thông giữa các máy ảo (instances). Một router được yêu cầu để cho phép lưu lượng đi ra luồng bên ngoài tenant network GRE hoặc VXLAN. Router cũng có thể yêu cầu để kết nối một tenant network với mạng bên ngoài (ví dụ Internet). Router cung cấp khả năng kết nối tới instances trực tiếp từ mạng bên ngoài sử dụng các địa chỉ floating IP

<img src="http://i.imgur.com/He8ttC7.png">

component and connectivity:
<img src="https://docs.openstack.org/newton/networking-guide/_images/deploy-ovs-selfservice-compconn1.png">




