# Cách cài đặt Manila

## Mục lục
- [1. Cài đặt Manila với Devstack](#1)
- [2. Cài đặt Manila](#2)

<a name="1"></a>

# 1. Cài đặt Manila với Devstack

Ta cài đặt Devstack theo hướng dẫn sau:
[Cài đặt Devstack](https://github.com/CLOUDRITY/SVTT/blob/master/HuongNV/C%C3%A0i%20%C4%91%E1%BA%B7t%20v%C3%A0%20s%E1%BB%AD%20d%E1%BB%A5ng%20Devstack/C%C3%A0i%20%C4%91%E1%BA%B7t%20Devstack.md)

Chỉnh sửa file local.conf để enable plugin manila kèm theo đó, nội dung file local.conf như sau:

```
[[local|localrc]]
############################################################
# Customize the following HOST_IP based on your installation
############################################################
HOST_IP=172.16.69.137

ADMIN_PASSWORD=test123
DATABASE_PASSWORD=test123
MYSQL_HOST=127.0.0.1
MYSQL_PASSWORD=test123
RABBIT_PASSWORD=test123
SERVICE_PASSWORD=test123
SERVICE_TOKEN=test123

KEYSTONE_TOKEN_FORMAT=fernet

############################################################
# Customize the following section based on your installation
############################################################

# Logging
LOGFILE=/opt/stack/logs/stack.sh.log
VERBOSE=True
LOG_COLOR=True
SCREEN_LOGDIR=/opt/stack/logs
ENABLE_DEBUG_LOG_LEVEL=True
ENABLE_VERBOSE_LOG_LEVEL=True


# Manila
enable_plugin manila https://github.com/openstack/manila

# Neutron ML2 with OpenVSwitch
Q_PLUGIN=ml2
Q_AGENT=openvswitch

# Disable security groups
Q_USE_SECGROUP=False
LIBVIRT_FIREWALL_DRIVER=nova.virt.firewall.NoopFirewallDriver


enable_service n-novnc
enable_service n-cauth

no_proxy=127.0.0.1,172.16.69.137

disable_service tempest
disable_service etcd3

[[post-config|/etc/neutron/dhcp_agent.ini]]
[DEFAULT]
enable_isolated_metadata = True
```

<a name="2"></a>

# 2. Cài đặt Manila

Manila có thể cấu hình trên một node hoặc nhiều node. Khi cài đặt Manila sẽ cho ta hai lựa chọn. Đó là cấu hình có hoặc không có việc xử lý của share server. Và lựa chọn này dựa trên driver ta sử dụng.

- Lựa chọn 1: Cấu hình không có việc xử lý của share server. Trong module này dịch vụ không can thiệp tới network. Admin phải chắc chắn việc kết nối các instance và share server. Với lựa chọn này, ta sử dụng driver LVM, GLUSTERFS

- Lựa chọn 2: Triển khai dịch vụ với sự hỗ trợ của driver cho việc quản lý các share. Trong module này, các service yêu cầu là nova, neutron và cinder cho việc quản lý share server. Thông tin được sử dụng cho việc tạo share server là share network. Option này sử dụng `generic driver` với việc xử lý các share server.

**Chú ý**: Với lựa chọn 2 ta có thể hình dung đơn giản như sau. Ddể sử dụng option này ta cần phải tạo ra một share-network dựa trên cấu hình neutron. Share network này được gắn với router của tenant và thông tới tenant-network.

Sau khi có một yêu cầu tạo share, yêu cầu này sẽ được chuyển tới một backend có cấu hình `Generic Driver` trên node cài manila-share, manila-share được cấu hình sử dụng nova để tạo một instance(image được cài sẵn nfs-server), đồng thời 1 volume tạo ra trên cinder có kích thước bằng kích thước của share tạo ra volume này gắn với instance trên. Các dữ liệu share được lưu tại volume này.

Mô hình mạng như sau:

![Imgur](https://i.imgur.com/Gf1vpyP.png)