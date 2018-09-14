# MỤC LỤC:

# I. TÌM HIỂU CƠ BẢN VỀ CLOUD:

## 1. Khái niệm về Cloud:

- Theo Viện Tiêu chuẩn và Công nghệ Quốc gia Mỹ (NIST), Cloud Computing – Điện toán đám mây, là mô hình cho phép truy cập qua mạng để lựa chọn và sử dụng tài nguyên  có thể được tính toán (ví dụ: mạng, máy chủ, lưu trữ, ứng dụng và dịch vụ) theo nhu cầu một cách thuận tiện và nhanh chóng; đồng thời cho phép kết thúc sử dụng dịch vụ, giải phóng tài nguyên dễ dàng, giảm thiểu các giao tiếp với nhà cung cấp.

- Theo tổ chức IEEE &quot;Nó là hình mẫu trong đó thông tin được lưu trữ thường trực tại các máy chủ trên Internet và chỉ được được lưu trữ tạm thời ở các máy khách, bao gồm máy tính cá nhân, trung tâm giải trí, máy tính trong doanh nghiệp, các phương tiện máy tính cầm tay,...&quot;

-Thuật ngữ &quot;đám mây - Cloud&quot; ở đây là lối nói ẩn dụ chỉ mạng Internet (dựa vào cách được bố trí của nó trong sơ đồ mạng máy tính) và như một liên tưởng về độ phức tạp của các cơ sở hạ tầng chứa trong nó.

 ![](https://upload.wikimedia.org/wikipedia/commons/b/b5/Cloud_computing.svg)

## 2. Phân loại Cloud:

### 2.1. Theo các mô hình dịch vụ:

 ![](https://upload.wikimedia.org/wikipedia/commons/3/3c/Cloud_computing_layers.png)

- Infrastructure as a service (IaaS) - Cơ sở hạ tầng như một dịch vụ:

 IaaS cung cấp cho người dùng hạ tầng thô (thường dưới hình thức các máy ảo) như một dịch vụ. Người dùng có thể triển khai và chạy phần mềm trên các máy ảo như trên một máy chủ thực hay có thể đưa dữ liệu cá nhân lên &quot;đám mây&quot; và lưu trữ. Người dùng không có quyền kiểm soát hạ tầng thực bên trong &quot;đám mây&quot; tuy nhiên họ có toàn quyền quản lý và sử dụng tài nguyên mà họ được cung cấp, cũng như yêu cầu mở rộng lượng tài nguyên họ được phép sử dụng.

 Các đám mây IaaS thường cung cấp các tài nguyên bổ sung như thư viện ảnh đĩa ảo, lưu trữ khối thô, lưu trữ tệp hoặc đối tượng, tường lửa, cân bằng tải, địa chỉ IP, mạng cục bộ ảo (VLAN) và gói phần mềm.

- Platform as a service (PaaS) – Nền tảng như một dịch vụ:

 PaaS cung cấp cách thức cho phát triển ứng dụng trên một nền tảng trừu tượng. Các người dùng PaaS không quản lý hoặc kiểm soát cơ sở hạ tầng đám mây cơ bản bao gồm mạng, máy chủ, hệ điều hành hoặc bộ nhớ, nhưng có quyền kiểm soát các ứng dụng được triển khai và cài đặt cấu hình cho môi trường lưu trữ ứng dụng.

- Software as a Service (SaaS) - Phần mềm như một dịch vụ:

 Cung cấp cho người dùng việc sử dụng các ứng dụng của nhà cung cấp chạy trên cơ sở hạ tầng đám mây. Các ứng dụng có thể truy cập từ các thiết bị khách khác nhau thông qua trình duyệt web hoặc giao diện chương trình. Người dùng có quyền truy cập vào phần mềm ứng dụng và cơ sở dữ liệu. Các nhà cung cấp đám mây quản lý cơ sở hạ tầng và nền tảng chạy các ứng dụng.

### 2.2. Theo các mô hình triển khai:

 ![](https://upload.wikimedia.org/wikipedia/commons/8/87/Cloud_computing_types.svg)

- Public Cloud: là các dịch vụ trên nền tảng Cloud Computing để cho các cá nhân và tổ chức thuê, họ dùng chung tài nguyên. Đây là mô hình triển khai được sử dụng phổ biến nhất hiện nay của cloud computing.
- Private Cloud: dùng trong một doanh nghiệp và không chia sẻ với người dùng ngoài doanh nghiệp đó.
- Comminity Cloud: là các dịch vụ trên nền tảng Cloud computing do các công ty cùng hợp tác xây dựng và cung cấp các dịch vụ cho cộng đồng.
- Hybrid Cloud: là thành phần của 2 hoặc nhiều các cloud khác (private, community hay public cloud) mà vẫn là các thực thể riêng biệt nhưng được liên kết với nhau, mang lại lợi ích của nhiều mô hình triển khai.

## 3. Các đặc điểm của Cloud Computing:

- Khả năng thu hồi và cấp phát tài nguyên (Rapid elasticity – tính đàn hồi nhanh).
- Truy nhập qua các chuẩn mạng (Broad network access).
- Dịch vụ sử dụng đo đếm được (Measured service), hay là chi trả theo mức độ sử dụng - pay as you go.
- Khả năng tự phục vụ (On-demand self-service).
- Chia sẻ tài nguyên (Resource pooling).

# II. TÌM HIỂU CƠ BẢN VỀ OPENSTACK:

## 1. Khái niệm về Openstack:

OpenStack là một phần mềm mã nguồn mở, dùng để triển khai Cloud Computing, bao gồm private cloud và public cloud. Công nghệ này bao gồm một nhóm các dự án liên quan đến nhau mà kiểm soát xử lý,lưu trữ và tài nguyên mạng thông qua một trung tâm dữ liệu - trong đó người sử dụng quản lý thông qua một bảng điều khiển dựa trên nền web,các công cụ dòng lệnh,hoặc thông qua một API RESTful. OpenStack.org phát hành nó theo các điều khoản của Giấy phép Apache.

 ![](https://vmokshagroup.com/wp-content/uploads/2015/07/OpenStack.png)

## 2. Một số thông tin về Openstack:

- Tính đến nay có 18 phiên bản của OpenStack bao gồm: Austin, Bexar, Cactus, Diablo, Essex, Folsom, Grizzly, Havana, Icehouse, Juno, Kilo, Liberty, Mitaka, Newton, Ocata, Pike, Queens và mới nhất là bản Rocky (30/8/2018).
- OpenStack là một dự án  mã nguồn mở  dùng để triển khai private cloud và public cloud, nó bao gồm nhiều thành phần (tài liệu tiếng anh gọi là project con) do các công ty, tổ chức ,lập trình viên tự nguyện xây dựng và phát triển. Có 3 nhóm chính tham gia: Nhóm điều hành, nhóm phát triển và nhóm người dùng.
- OpenStack bắt đầu vào năm 2010 như là một dự án chung của Rackspace Hosting và của NASA.

## 3. Các thành phần chính của Openstack:

 ![](https://upload.wikimedia.org/wikipedia/en/d/dd/OpenStack_main_services.svg)

- Compute (Nova)
- Networking (Neutron)
- Block storage (Cinder)
- Identity (Keystone)
- Image (Glance)
- Object storage (Swift)
- Dashboard (Horizon)
- Orchestration (Heat)
- Workflow (Mistral)
- Telemetry (Ceilometer)
- Database (Trove)
- Data processing (Sahara)
- Bare metal (Ironic)
- Messaging (Zaqar)
- Shared file system (Manila)
- DNS (Designate)
- Search (Searchlight)
- Key manager (Barbican)
- Container orchestration (Magnum)
- Root Cause Analysis (Vitrage)
- Rule-based alarm actions (Aodh)

# III. TÌM HIỂU MỘT SỐ DỊCH VỤ CHÍNH CỦA OPENSTACK:

## 1. Identity (Keystone):

### 1.1.Chức năng chính:

- Quản lý user và những quyền mà user được phép làm.
- Cung cấp các dịch vụ nhận dạng và xác thực.
- Tạo các chính sách giữa user và dịch vụ.

### 1.2. Các dịch vụ thành phần:

- Identity: cung cấp xác thực và dữ liệu về người dùng và nhóm.
- Token: xác thực và quản lý các token để xác thực yêu cầu khi thông tin đăng nhập của người dùng đã được xác minh.
- Catalog: cho phép các API client tự động phát hiện và điều hướng đến các dịch vụ đám mây. Cung cấp các endpoint đăng kí, sử dụng cho endpoint tìm kiếm.
- Policy: Cung cấp các chính sách của Keystone. Mỗi dịch vụ OpenStack định nghĩa các chính sách truy cập cho các tài nguyên của nó trong một tệp policy liên quan.

### 1.3. Một số luồng hoạt động chính:

#### 1.3.1. Các khái niệm user, group, project, domain, roles:

- User: Người dùng đại diện cho một người dùng API cá nhân. Bản thân người dùng phải thuộc sở hữu của một domain cụ thể và do đó tất cả tên người dùng không phải là duy nhất toàn cầu, nhưng chỉ duy nhất cho domain của họ.
- Group: là một vùng chứa đại diện cho một tập hợp người dùng. Bản thân nhóm phải được sở hữu bởi một domain cụ thể và do đó tất cả các tên nhóm không phải là duy nhất trên toàn cầu, nhưng chỉ duy nhất cho domain của chúng.
- Project: đại diện cho đơn vị cơ sở sở hữu trong OpenStack, trong đó tất cả các tài nguyên trong OpenStack phải thuộc sở hữu của một project cụ thể. Bản thân một project phải được sở hữu bởi một domain cụ thể và do đó tất cả các tên project không phải là duy nhất trên toàn cầu, nhưng duy nhất cho domain của họ. Nếu domain của project không được chỉ định, thì domain đó sẽ được thêm vào domain mặc định.
- Domain: Miền là vùng chứa cấp cao cho các project, người dùng và nhóm. Mỗi miền được sở hữu bởi chính xác một tên miền. Keystone cung cấp miền mặc định, được đặt tên là &quot;Default&quot;.
- Roles: quyết định mức độ ủy quyền mà người dùng cuối có thể có được. Roles có thể được cấp ở cấp domain hoặc cấp project.

#### 1.3.2. Các cơ chế quản lý token: fernet, UUID, PKI:

- Fernet: bao gồm các thông tin: userid, projectid, domainid, methods, expiresat, và các thông tin khác. Nó sử dụng một thư viện mã hoá cân xứng (Mã hóa, Giải mã sử dụng chung key) mã hóa token (AES-CBC và SHA256). Fernet được thiết kế cho Token nhẹ, bảo mật thông tin, không cần lưu trữ trong database làm giảm IO của ổ đĩa, cải thiện hiệu năng.
- UUID(Universally Unique Identifier): UUID được đại diện bởi 32 chữ, số là các số hexa ngẫu nhiên. UUID không mang thông tin gì về User. Keystone phải thực hiện việc xác thực token và lưu trữ.
- PKI: PKI (Public Key Infrastructure) Token bản chất dựa trên chữ ký điện tử. Keystone sẽ dùng private key cho việc ký nhận và các Openstack API sẽ có public key để xác nhận thông tin đó.

#### 1.3.3. Luồng xác thực và phân quyền khi user sử dụng dịch vụ (ví dụ khi user tạo 1 máy ảo).
![](https://i.imgur.com/684Wq5Z.png)
1. User gửi thông tin chứng thực đến Keystone (Username và Password).
2. Keystone kiểm tra thông tin. Nếu đúng, nó sẽ gửi về user một token.
3. User gửi token và yêu cầu đến Nova.
4. Nova và Keystone tương tác với nhau để xác nhận token có hợp lệ hay không, user có những quyền hạn gì...
5. Nếu token hợp lệ và đủ quyền thì Nova gửi token và yêu cầu Image đến Glance.
6. Glance gửi token về Keystone để xác thực và kiểm tra xem user này có quyền với Image này hay không. Keystone sẽ trả lời lại cho Nova.
7. Nova gửi token và yêu cầu mạng đến Neutron.
8. Neutron gửi token đến Keystone. Keystone sẽ trả lời cho Neutron là user này có đủ quyền hạn hay không.
9. Neutron trả lời cho Nova.
10.Nova trả lời cho user.

## 2. Compute (Nova):

### 2.1. Chức năng chính:

-	Nova hỗ trợ tạo các máy ảo, máy chủ từ xa và hỗ trợ giới hạn cho các container hệ thống.
-	Là phần chính của hệ thống IaaS. Nó được thiết kế để quản lý và tự động hóa các nhóm tài nguyên máy tính và có thể làm việc với các công nghệ ảo hóa rộng rãi, cũng như các cấu hình máy tính hiệu suất cao. KVM, VMware và Xen là những lựa chọn có sẵn cho công nghệ hypervisor…

### 2.2. Các dịch vụ thành phần:

![](https://docs.openstack.org/nova/queens/_images/architecture.svg)

-	Nova-api: là một RESTful API web service, nhận các yêu cầu HTTP, chuyển đổi các lệnh và giao tiếp với các thành phần khác thông qua hàng đợi oslo.messaging hoặc HTTP.
-	Nova-compute: quản lý giao tiếp với hypervisor và các máy ảo.
- Nova-scheduler: Lấy một yêu cầu về máy ảo ở hàng đợi và quyết định máy chủ sẽ chạy nó.
-	Nova-conductor: cung cấp các dịch vụ cho nova-compute, là trung gian giữa nova-compute và dữ liệu.
- Nova database: sql database cho lưu trữ dữ liệu.
-	Nova-network: quản lý chuyển tiếp IP, cầu nối và các VLAN.

### 2.3. Tìm hiểu luồng quản lý máy ảo: tạo, xóa.

![](https://ilearnstack.files.wordpress.com/2013/04/request-flow1.png)

1. Dashboard/CLI lấy thông tin chứng thực người dùng và gọi REST tới Keystone để xác thực.
2. Keystone xác thực thông tin người dung và tạo ra một token xác thực gửi trở lại, để dùng cho việc gửi yêu cầu đến các dịch vụ khác qua REST.
3. Dashboard/CLI chuyển yêu cầu tạo áy ảo được chỉ định trong &quot;launch instance&quot; hoặc &quot;nova-boot&quot;, thực hiện REST API request và sau đó gửi yêu cầu tới nova-api.
4. Nova-api nhận yêu cầu và gửi yêu cầu cho keystone để kiểm tra tính hợp lệ của token xác thực, quyền truy cập của người dùng.
5. Keystone xác nhận token và gửi headers xác thực  bổ sung với các roles và quyền truy cập cho nova-api.
6. Nova-api tương tác với nova-database.
7. Nova-database tạo ra entry lưu thông tin máy ảo mới.
8. Nova-api gửi rpc.call request đến nova-scheduler cho phép cập nhật entry của máy ảo mới với một host ID xác định.
9. Nova-scheduler lấy yêu cầu từ hàng đợi.
10. Nova-scheduler tương tác với nova-database để tìm host thích hợp thông qua việc sàng lọc và cân nhắc.
11. Nova-database cập nhật lại entry của máy ảo mới với host ID phù hợp sau khi sàng lọc và cân nhắc.
12. Nova-scheduler gửi rpc.cast request tới nova-compute cho yêu cầu tạo máy ảo với host thích hợp.
13. Nova-compute lấy yêu cầu từ hàng đợi.
14. Nova-compute gửi rpc.call request tới nova-conductor để tìm nạp thông tin máy ảo như host ID, các thông tin như RAM, CPU, Disk…
15. Nova-conductor lấy yêu cầu từ hàng đợi.
16. Nova-conductor tương tác với nova-database.
17. Tiếp tục quay vòng lại, nova-database trả lại thông tin của máy ảo mới cho nova-conductor, nova condutor gửi thông tin máy ảo vào hàng đợi.
18. Nova-compute lấy thông tin máy ảo từ hàng đợi.
19. Nova-compute thực hiện lời gọi REST bằng việc gửi token xác thực tới glance-api để lấy Image URI bằng Image ID từ khối Glance và upload Image từ Image Store.
20. Glance-api xác thực token xác thực với keystone.
21. Nova-compute lấy metadata (Siêu dữ liệu) của Image.
22. Nova-compute thực hiện cuộc gọi REST bằng việc gửi token xác thực tới Network API để xin IP và cấu hình mạng cho máy ảo.
23. Neutron server xác thực token xác thực với keystone.
24. Nova-compute lấy thông tin về network.
25. Nova-compute thực hiện Rest call mang theo token xác thực tới Volume API để gắn volumes vào máy ảo.
26. Cinder-api xác thực token xác thực với keystone.
27. Nova-compute lấy thông tin block storage cấp cho máy ảo.
28. Nova-compute tạo dữ liệu cho hypervisor driver và thực thi yêu cầu tạo máy ảo trên Hypervisor (thông qua libvirt hoặc api).

## 3. Networking (Neutron):

### 3.1. Chức năng chính:

-	Quản lý mạng và địa chỉ IP, đảm bảo mạng không bị nút cổ chai và đem đến cho người dùng khả năng tự phục vụ.
-	Cung cấp một framework mở rộng có thể triển khai và quản lý các dịch vụ mạng bổ sung — chẳng hạn như hệ thống phát hiện xâm nhập (IDS), cân bằng tải, tường lửa và mạng riêng ảo (VPN)…

### 3.2. Các dịch vụ thành phần:

![](https://docs.openstack.org/security-guide/_images/sdn-connections.png)
-	Neutron server (neutron-server và neutron-*-plugin): chạy trên các node mạng để phục vụ Networking API và các mở rộng của nó. Ngoài ra nó cũng thực thi các dịch vụ mạng và đánh địa chỉ IP cho mỗi port. Nó yêu cầu truy cập gián tiếp vào cơ sở dữ liệu liên tục. Điều này được thực hiện thông qua các plugin, giao tiếp với cơ sở dữ liệu bằng cách sử dụng giao thức AMPQ (Advanced Message Queuing Protocol).
-	Plugin agent (neutron-*-agent): Chạy trên mỗi compute node để quản lý cấu hình chuyển mạch ảo cục bộ (vswitch). Dịch vụ này yêu cầu truy cập hàng đợi tin nhắn và phụ thuộc vào plugin được sử dụng. Một số plugin như OpenDaylight (ODL) và Open Virtual Network (OVN) không yêu cầu bất kỳ tác nhân python nào trên các compute node.
-	DHCP agent (neutron-dhcp-agent): Cung cấp dịch vụ DHCP cho các tenant network. Tác nhân này giống nhau trên tất cả các plugin và chịu trách nhiệm duy trì cấu hình DHCP. Neutron-dhcp-agent yêu cầu truy cập hàng đợi thông báo. Tùy chọn tùy thuộc vào plugin.
-	L3 agent (neutron-l3-agent): Cung cấp chuyển tiếp L3 / NAT cho truy cập mạng bên ngoài của các máy ảo trên các mạng thuê. Yêu cầu quyền truy cập hàng đợi tin nhắn. Tùy chọn tùy thuộc vào plugin.
-	Network provider services (SDN server/services): Cung cấp các dịch vụ mạng bổ sung cho các mạng thuê. Các dịch vụ SDN này có thể tương tác với nơtron-máy chủ, trình cắm nơtron và các tác nhân bổ trợ thông qua các kênh truyền thông như API REST.

### 3.3. Tìm hiểu, phân biệt về provider network, self service network:

#### 3.3.1. Provider network:

-	Cung cấp khả năng kết nối layer 2 đến các instance có hỗ trợ tùy chọn cho các dịch vụ DHCP và metadata. Các mạng này kết nối hoặc ánh xạ tới các mạng layer 2 hiện có trong trung tâm dữ liệu, thường sử dụng thẻ VLAN (802.1q) để xác định và tách chúng.
-	Thường cung cấp sự đơn giản, hiệu suất và độ tin cậy với chi phí linh hoạt. Chỉ quản trị viên mới có thể quản lý mạng của provider network vì họ yêu cầu cấu hình cơ sở hạ tầng mạng vật lý. Ngoài ra, provider network chỉ xử lý kết nối layer 2 cho các trường hợp, do đó thiếu hỗ trợ cho các tính năng như bộ định tuyến và địa chỉ IP nổi.
-	Nói chung, các thành phần phần mềm Mạng OpenStack xử lý các hoạt động layer 3 tác động đến hiệu suất và độ tin cậy cao nhất. Để cải thiện hiệu suất và độ tin cậy, các network provider di chuyển các hoạt động layer 3 đến cơ sở hạ tầng mạng vật lý.

#### 3.3.2. Self service network:

-	Self-service network chủ yếu cho phép các dự án chung (non-privileged) quản lý mạng mà không cần liên quan đến quản trị viên. Các mạng này hoàn toàn ảo và yêu cầu các bộ định tuyến ảo tương tác với nhà cung cấp và các mạng bên ngoài như Internet. Self-service network cũng thường cung cấp các dịch vụ DHCP và siêu dữ liệu cho các cá thể.
-	Sử dụng các giao thức VXLAN hoặc GRE.
-	Self-service network  IPv4 thường sử dụng các dải địa chỉ IP riêng (RFC1918) và tương tác với các mạng của nhà cung cấp thông qua NAT nguồn trên các bộ định tuyến ảo.
## 4. Block storage (Cinder):
### 4.1. Chức năng chính:
-	Cung cấp các thiết bị lưu trữ khối (Block Storage) để sử dụng cùng với khối Compute, dùng để lưu trữ cơ sở dữ liệu, hệ thống tệp có thể mở rộng…
-	Ảo hóa việc quản lý các thiết bị lưu trữ khối và cung cấp cho người dùng cuối API tự phục vụ để yêu cầu và tiêu thụ các tài nguyên đó mà không yêu cầu bất kỳ kiến thức nào về nơi lưu trữ của họ thực sự được triển khai hoặc trên loại thiết bị nào.
- Quản lý việc tạo, gắn và tách các thiết bị khối với các máy chủ. Block Storage Volume được tích hợp đầy đủ vào Compute và Dashboard cho phép người dùng đám mây quản lý nhu cầu lưu trữ của riêng họ.
### 4.2. Các dịch vụ thành phần:
![](https://varchitectthoughts.files.wordpress.com/2013/11/screen-shot-2013-11-18-at-11-00-24-am.png)
- Cinder-api: Nhận API request và định tuyến chúng đến cinder-volume để hành động.
-	Cinder-volume: Tương tác trực tiếp với dịch vụ Lưu trữ khối và các tiến trình như cinder-scheduler. Nó cũng tương tác với các tiến trình này thông qua một hàng đợi thông báo (message queue). Cinder-volume  phản hồi các yêu cầu đọc và ghi được gửi tới Block Storage để duy trì trạng thái. Nó có thể tương tác với nhiều backup storage provider thông qua trình điều khiển.
-	Cinder-scheduler: Dựa trên request được điều hướng tới, cinder-scheduler chuyển request tới Cinder Volume Service thông qua giao thức AMQP (Advanced Message Queue Protocol). Cinder-scheduler chọn nơi cung cấp bộ nhớ tối ưu để tạo volume. Nó tương tự như nova-scheduler.
-	 Cinder-backup: cung cấp khả năng sao lưu cho bất kỳ loại nào cho backup storage provider.
-	Messaging queue: chuyển tiếp thông tin giữa các tiến trình trong block storage.
### 4.3. Tìm hiểu luồng tạo volume, gắn volume vào VM:
#### 4.3.1. Luồng tạo Volume:
![]( https://netapp.github.io/openstack-deploy-ops-guide/liberty/content/figures/3/a/images/cinder_create_volume_process.png)
1.	Client yêu cầu tạo volume thông qua việc gọi REST API.
2.	Cinder-api xác nhận yêu cầu, thông tin người dùng. Khi đã được xác thực, đưa thông báo lên hàng đợi AMPQ để xử lý.
3.	Cinder-volume lấy thông báo từ hàng đợi và gửi đến Cinder-scheduler để xác định backend cho việc cung cấp volume.
4.	Cinder-scheduler  lấy thông báo khỏi hàng đợi, tạo danh sách thích hợp dựa trên trạng thái hiện tại và yêu cầu volume (kích thước, loại volume…).
5.	Cinder-volume đọc thông tin phản hồi từ Cinder-scheduler, lặp lại danh sách ứng viên bằng việc gọi các phương thức backend driver cho đến khi thành công.
6.	Trình điều khiển NetApp Cinder tạo ra volume yêu cầu thông qua các tương tác với hệ thống con lưu trữ (phụ thuộc vào cấu hình và giao thức).
7.	Cinder-volume tập hợp volume metadata từ hàng đợi, kết nối thông tin và chuyển message trả lời đến hàng đợi AMQP.
8.	Cinder-api đọc thông tin phản hồi từ hàng đợi và trả lời client.
9.	Client nhận được thông tin bao gồm trạng thái của yêu cầu tạo volume: volume UUID, etc.
#### 4.3.2. Luồng gắn volume vào VM:
![]( https://netapp.github.io/openstack-deploy-ops-guide/liberty/content/figures/3/a/images/nova_volume_attach_process.png)
1.	Client yêu cầu gắn volume qua việc gọi Nova REST API.
2.	Nova-api xử lý yêu cầu chứng thực, thông tin người dùng. Khi đã xác nhận là hợp lệ, gọi REST API để lấy thông tin về volume cụ thể.
3.	Cinder-api xác nhận yêu cầu, thông tin người dùng. Khi đã xác thực, gửi thông điệp đến trình quản lý volume qua AMPQ.
4.	Cinder-volume đọc thông điệp từ hàng đợi, gọi trình điều khiển Cinder tương ứng với volume được đính kèm.
5.	Trình điều khiển NetApp Cinder chuẩn bị volume Cinder để chuẩn bị cho việc đính kèm (các bước cụ thể phụ thuộc vào giao thức lưu trữ được sử dụng)
6.	Cinder-volume gửi thông tin phản hồi đến cinder-api qua hàng đợi AMPQ.
7.	Cinder-api đọc thông tin phản hồi từ cinder-volume từ hàng đợi, chuyển thông tin kết nối trong RESTful response đến Nova caller.
8.	Nova tạo kết nối tới kho lưu trữ với thông tin được trả về từ Cinder.
9.	Nova chuyển thiết bị/tập tin volume đến hypervisor, nơi thực hiện việc gắn volume vào máy ảo.
## 5. Image (Glance):
### 5.1. Chức năng chính:
-	Cho phép người dùng khám phá, đăng ký và truy xuất các VM image. 
-	Cung cấp API REST cho phép ta truy vấn VM image metadata và truy xuất một image thực tế.
## 5.2. Các dịch vụ thành phần:
![]( http://www.sparkmycloud.com/blog/wp-content/uploads/2016/01/Untitled-drawing2.png)
-	Glance-api: Nhận REST call cho việc tìm kiếm, tiếp nhận và lưu trữ các image.
-	Glance-registry: lưu trữ, thực thi và thu thập metadata về các image.
-	Database: là cơ sở dữ liệu lưu trữ image metadata.
-	Storage repository: tích hợp với các thành phần OpenStack khác nhau bên ngoài như hệ thống tệp thông thường, Amazon S3 và HTTP cho kho lưu trữ hình ảnh…
## 5.3. Luồng tạo Images:
Glance Image Status: Sau đây là các trạng thái của Image khi upload:
![](https://i.imgur.com/27Ldmq9.png)
-	queued: Không có dữ liệu hình ảnh nào được tải lên Glance và kích thước hình ảnh không được thiết lập rõ ràng về 0 khi tạo.
-	saving: Raw data của Image đang được tải lên Glance.
-	uploading: Biểu thị rằng một cuộc gọi nhập dữ liệu đã được thực hiện (import data-put call).
-	importing: Cuộc gọi nhập dữ lệu đã được thực hiện nhưng hình ảnh chưa sẵn sàng để sử dụng.
-	active: Image đã được tải lên và sẵn sàng ở Glance.
-	deactivated: quyền truy cập vào dữ liệu Image không được cho phép đối với bất kỳ người dùng không phải quản trị viên nào.
-	killed: Đã xảy ra lỗi khi tải lên dữ liệu của Image và không thể đọc được.
-	deleted: Glance đã giữ lại thông tin về Image, nhưng nó không còn có sẵn để sử dụng.
-	pending_delete: Tương tự như deleted. Tuy nhiên Image trong trạng thái này không thể khôi phục được.
Tạo Image:
+	Tạo Image-status object.
+	Lấy dữ liệu từ nơi được chỉ định.
+	Xác minh dữ liệu.
+	Nếu thành công, tạo Image.
+	Ghi lại kết quả trong  image-import object, đặt trạng thái thích hợp và đặt expiration date. 

## 6. Dashboard (Horizon):
### 6.1. Chức năng chính:
-	Cung cấp cho quản trị viên và người dùng một giao diện đồ họa dựa trên web để truy cập, cung cấp và tự động triển khai các tài nguyên dựa trên đám mây.
### 6.2. Các dịch vụ thành phần:


