# Tìm hiểu về GlusterFS và GlusterFS Native Driver

## Mục lục

- [1. GlusterFS](#1)
- [2. GlusterFS Native Driver](#2)

<a name="1"></a>

# 1. GlusterFS

GlusterFS là phần mềm mã nguồn mở cho phép mở rộng hệ thống lưu trữ file len tới peta-byte và xử lý cùng lúc cho hàng ngàn client, nó tập hợp các server lưu trữ khác nhau trên Ethernet hoặc RDMA (Remote Direct Memory Access) kết nối thành một hệ thống lưu trữ tập tin lớn và song song. Trong một số trường hợp, GlusterFS được lựa chọn như một giải pháp mềm và ít tốn kém chi phí thay thế cho SAN.

Kiến trúc của GlusterFS dựa trên 4 yếu tố chính:

- **Node**: Các máy chủ lưu trưc được cài đặt Gluster
- **Brick**: Là một folder/mount point/file system tren một node Để chia sẻ với các node tin cậy khác trong hệ thống. Trên một node có thể có nhiều Brick, Brick được dùng để gán vào các vùng dữ liệu (volume), các brick trong một volume nên có dung lượng lưu trữ bằng nhau

![Imgur](https://i.imgur.com/lK4Love.png)

- **Volume**: Là một khối logic chứa nhiều Brick, Gluster đóng vai trò như một LVM (Logical Volume Manager) bằng cách quản lý các brick phân tán trên các máy chủ như là một điểm kết nối lưu trữ duy nhất trên mạng

![Imgur](https://i.imgur.com/B5i2Axy.jpg)

- **Client**: Là các máy tính kết nối với hệ thống lưu trữ của Gluster. Đó có thể là các window client chuẩn (thông qua CIFS), NFS client hay sử dụng Gluster client cải tiến hơn so với NFS đặc biệt là có tính sẵn sàng cao

## Các dạng Volume khác nhau của GlusterFS

**1. Distributed Volume**

Với kĩ thuật này, các files sẽ được phân tán, lưu trữ rời rạc trong các brick khác nhau. Ví dụ có 100 file: file1, file2...file 100 thì file 1, file 2 lưu ở brick1, file 3, file 4 lưu ở brick2. Việc phân bố các file trên brick dựa vào thuật toán hash

![Imgur](https://i.imgur.com/6CB7j7U.png)

Ưu điểm: Mở rộng dung lượng lưu trữ nhanh chóng và dễ dàng, tổng dung lượng lưu trữ của volume bằng tổng dung lượng của các brick

Nhược điểm: Khi một trong các brick bị ngắt kết nối hoặc bị lỗi thì dữ liệu bị mất hoặc không truy vấn được

**2. Replicated Volume**

Với kĩ thuật này, dữ liệu sẽ được copy sang các brick khác trong cùng một volume. Như trong hình vẽ, chúng ta thấy rõ ưu điểm đó là dữ liệu sẽ có tính sẵn sàng cao và luôn trong tình trạng dự phòng

![Imgur](https://i.imgur.com/qRENOwg.png)

**3. Striped Volume**

Với kĩ thuật này, dữ liệu được chia nhỏ thành những thành phần khác nhau và lưu trữ ở những brick khác nhau trong volume.

![Imgur](https://i.imgur.com/mIT8GSp.png)

Uư điểm: Phù hợp với việc lưu trữ mà dữ liệu cần truy xuất với hiệu năng cao, đặc biệt là truy cập vào những tệp tin lớn

Nhược điểm: Khi một trong những brick trong volume bị lỗi thì volume đó không thể hoạt động được

**5. Distributed Replicated Volume**

Kĩ thuật này là sự kết hợp giữ kĩ thuật Distributed Volume và Replicated Volume. Các file được phân tán trên các brick trong cùng 1 volume

![Imgur](https://i.imgur.com/s98QCQY.png)

Ưu điểm: Dữ iệu có tính sẵn sàng cao tuy nhiên nhược điểm là khi 1 volume có lỗi thì dữ liệu sẽ bị ảnh hưởng

**5. Distributed Striped Volume**

Là sự kết hợp giữ kĩ thuật Distributed Volume và Strip Volume. Các file được phân tán trên các brick nằm ở các Volume khác nhau. Kĩ thuật này không có tính sẵn sàng của dữ liệu mà chỉ có tác dụng phân tán dữ liệu với tốc đọ truy xuất nhanh

![Imgur](https://i.imgur.com/giD14MM.png)


<a name="2"></a>

# 2. GlusterFS Native Driver

Một vài điểm lưu ý với GlusterFS Native Driver
- Support Certificate based access type of Manila
- Sử dụng giao thức `glusterfs`
- Instances directly talk with GlusterFS storage backend
- GlusterFS Native Driver cung cấp `secure access`
- Multi-tenant
    - Separation using tenant specific certificates
- Support certificate chaining ang cipher lists

## GlusterFS Native Driver supported operations

- Create a share, delete a share, allow share access (chỉ support `rw` access), deny share access
- Create snapshot, delete snapshot, create share from snapshot

## Requirements

- Install glussterfs-server, version >= 3.6 trên storage backend node
- Install glusterfs và glusterfs-fuse, version >= 36 trên manila host
- Thiết lập kết nối giữa manila host và storage backend

Với backend là GlusterFS việc quản lý truy cập vào share file trên manila sẽ thông qua certificate, do vậy ta cần cấu hình SSL cho client và server

```
cd /etc/ssl
openssl genrsa -out glusterfs.key 1024
openssl req -new -x509 -key glusterfs.key -subj /CN=huongngo -out glusterfs.pem
cp glusterfs.pem glusterfs.ca
```

Ta đã thực hiện tạo key và CA trên server. Thực hiện copy key và ca tới tất cả server glussterfs

Ở đây ta tạo CA có `CN=huongngo` trên manila ta sẽ tạo access-allow cho CA của `huongngo` manila-share

Cáu hình manila-share tại /etc/manila/manila.conf

Enable backend glusternative và protocol GLUSSTERFS tại secssion [DEFAULT]

```
enabled_share_backends = GlusterFSNative           # Tên backend
enabled_share_protocols = NFS,CIFS,GLUSTERFS,HDFS  # Tên các giao thức
```

Cấu hình backend glusterfs native như sau

```
[GlusterFSNative]
share_backend_name = GlusterFSNative    # Tên backend
glusterfs_servers = <username>@<glusterfs server hostname>  # Khai báo user và hostname của gluster server
glusterfs_server_password = <password>  # Khai báo password để manila-host ssh vào gluster server
glusterfs_volume_pattern = manila-#{size}-.* # pattern volume trên manila khi tạo share mapping với volume trên glusterfs 
share_driver = manila.share.drivers.glusterfs_native.GlusterfsNativeShareDriver
driver_handles_share_servers = False
```

Trên node `controller` cần phải anable protocol `GLUSSTERFS` vì mặc định chỉ enable `NFS` và `CIFS`

```
enabled_share_protocols=NFS, CIFS, GLUSTERFS
```

Sau khi cấu hình các dịch vụ xong, tiến hành khởi động lại dịch vụ

```
service manila-api restart
service manila-scheduler restart
```

Thực hiện tạo share-type

```
manila type-create glussterfsnative_test False  # DHSS=False
manila type-key glusterfsnative_test set share_backend_name=GlusterFSNative    # Khai báo backend cho type này
```

Khởi tạo manila-share

```
manila create glusterfs 2 --name gluster_test --share-type glusterfsnative
```

```
Thực hiện tạo 1 share với kích thước là 2GB, tên là gluster_test
```

Tạo access-allow cho client

```
manila access-allow <share-id> cert <client_host>

# Ở đây share-id là gluster_test
# client_host là hostname của client với CNlà `huongngo`
```

Thực hiện show share-type vừa khởi tạo để kiểm tra đường dẫn của share vừa tạo để có thể mount tới client

```
manila show gluster_test
```

Sau khi thực hiện các bước xong, ta truy cập tới client để mount share tới. Trên client phải thực hiện cài gói glusterfs-client

```
add-apt-repository ppa:gluster/glusterfs-3.7 -y
apt-get update
apt-get install glusterfs-client -y
```

Client cần CA có `CN=huongngo` và server phải biết CA này. Thực hiện copy key và CA trên server đã thưc hiện tạo ở trên về client, sau đó thực hiện mount

```
cd /etc/ssl
openssl genrsa -out glusterfs.key 1024
openssl req -new -x509 -key glusterfs.key -subj /CN=huongngo -out glusterfs.pem
cp glusterfs.key glusterfs.ca
scp <glusterfs_server>:/etc/ssl/glusterfs.ca /etc/ssl/glusterfs_server.ca
cat /etc/ssl/glusterfs_server.ca >> /etc/ssl/glusterfs.ca
```

Sau khi đã có đưỡng dẫn của volume, thực hiện mount volume trên client

```
mount -t glusterfs HOSTNAME-OR-IPADDRESS:/VOLNAME MOUNTDIR
```

```
HOSTNAME-OR-IPADDRESS:/VOLNAME MOUNTDIR: Đường dẫn path của volume khi thực hiện show volume-share
```

# Tài liệu tham khảo
- https://www.slideshare.net/dpkshetty/gluster-meetup-openstackdeepakcs
- https://qiita.com/makisyu/items/0a84e8f905fddd8fd074
- https://docs.openstack.org/manila/pike/contributor/glusterfs_native_driver.html
- http://dcshetty.blogspot.com/2015/01/using-glusterfs-native-driver-in.html