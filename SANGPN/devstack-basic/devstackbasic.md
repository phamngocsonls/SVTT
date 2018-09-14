# I. HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG DEVSTACK:

## 1. Hướng dẫn cài đặt:

### 1.1. Chuẩn bị:

- Máy ảo Ubuntu Server 18.04 LTS cài đặt trên VMware Workstation.
- RAM cho máy ảo tối thiểu 4GB để sử dụng được cơ bản các dịch vụ.

### 1.2. Cài đặt:

1. Trước tiên cần chắc chắn rằng hệ điều hành đã được cập nhật các package mới nhất bằng việc gõ lệnh sau vào terminal dưới quyền root:

**apt update &amp;&amp; apt dist-upgrade –y**

1. Sau khi đã cập nhật xong, ta tạo một user để chạy Devstack với username là stack:

**sudo useradd –s /bin/bash –d /opt/stack –m stack**

1. User stack sẽ thao tác nhiều với quyền root nên ta thiết lập cấu hình để không cần nhập mật khẩu root khi dùng sudo:

**echo &quot;stack ALL=(ALL) NOPASSWD: ALL&quot; | sudo tee /etc/sudoers.d/stack**

1. Sau đó chuyển sang user stack:

**sudo su – stack**

1. Thực hiện tải Devstack về:

**git clone** [https://git.openstack.org/openstack-dev/devstack](https://git.openstack.org/openstack-dev/devstack) **--branch stables/rocky**

1. Di chuyển vào thư mục Devstack:

**cd devstack**

1. Truy cập vào file local.conf để thêm thông tin về HOST\_IP:

**vi samples/local.conf**

Tìm đến đoạn [[local|localrc]] và thêm vào HOST\_IP phù hợp.

1. Sau đó ta chỉ cần chạy file stack.sh với dòng lệnh:

**./stack.sh**

 Sau đó ngồi chờ quá trình tải và cài đặt Devstack (khoảng 30 - 45 phút). Trong quá trình cài đặt có thể sẽ yêu cầu bạn nhập mật khẩu để cấu hình như: ADMIN\_PASSWORD, DATABASE\_PASSWORD, RABBIT\_PASSWORD, SERVICE\_PASSWORD nếu bạn không fix trong file local.conf tại bước 7.

 Devstack sẽ được cài đặt keystone, glance, nova, cinder, neutron và horizon.

## 2. Sử dụng cơ bản Devstack:

### 2.1. Keystone:

#### 2.1.1. Thêm, sửa, xóa user:

- List User: từ terminal của Ubuntu Server nhập: **openstack user list** hoặc từ Dashboard, trong mục Identity User ta có thể liệt kê được số user hiện tại.

![](https://i.imgur.com/2KOu2Sq.png)

![](https://i.imgur.com/dRgLYMp.png)

- Thêm User:
  - CLI: **openstack user create --project demo --password 1 user1**

(Ví dụ ta tạo một user có username là user1 và password là 1, nằm trong project demo)

![](https://i.imgur.com/1Ngmsl5.png)

![](https://i.imgur.com/oVUss6B.png)

-
  - Dashboard: Ở phần user ta chọn vào Create User và điền một số thông tin vào là xong:

![](https://i.imgur.com/18VkoF5.png)

- Sửa User:
  - CLI: **openstack user set USER\_NAME --name user-new --email** [**new-user@example.com**](mailto:new-user@example.com)
  - Dashboard: ta chọn vào phần Edit trong mục Action của User cần chỉnh sửa thông tin và chỉnh sửa.

![](https://i.imgur.com/4HoCldV.png)

- Xóa User:
  - CLI: **openstack user delete USER\_NAME**
  - Dashboard: Chọn phần mũi tên phía sau User và Delete User.

![](https://i.imgur.com/OWFotGA.png)

#### 2.1.2. Thêm, sửa, xóa group:

- Thêm group:

-
  - CLI: **openstack group create --domain <domain> --description <descripton> <group name>**
  - Dashboard: Identity Group Create Group và điền tên, mô tả cho Group:

![](https://i.imgur.com/ge5CurN.png)

- Sửa Group:
  - CLI: **openstack group set --domain <domain> --name <name> --description <description> <group>**
  - Dashboard: ta vào phần mũi tên Edit Group để chỉnh sửa thông tin Group hoặc vào Manage Members để quản lý user trong Group đó.

![](https://i.imgur.com/Wmq4WMd.png)

- Xóa Group:
  - CLI: **openstack group delete --domain <domain> <group>**
  - Dashboard: ta chọn phần mũi tên sau Group cần xóa và chọn Delete Group:

![](https://i.imgur.com/NS4aPoh.png)

#### 2.1.3. Thêm, sửa, xóa Project:

- Thêm Project:
  - CLI: **openstack project create --description <description> project_name --domain <domain>**
  - Dashboard: Identity Project Create Project và sau đó điền thông tin của Project, chọn Project Members, Project Groups:

![](https://i.imgur.com/ky39BDJ.png)

- Sửa Project:
  - CLI: **openstack project set PROJECT_ID --name <new name> --description <new description>** …
  - Dashboard: Ở phần mũi tên phía sau Project ta chọn Edit Project và chỉnh sửa các thông tin cần thiết:

![](https://i.imgur.com/NnALl5M.png)

- Xóa Project:
  - CLI: **openstack project delete PROJECT_ID**
  - Dashboard: Như ở phần chỉnh sửa Project nhưng ta chọn mục Delete Project.

#### 2.1.4. Gán roles:

- List user và ghi nhớ các user mà muốn gán role: **openstack user list**
- List role ID và ghi nhớ role ID mà muốn gán: **openstack role list**
- List project và ghi nhớ project ID muốn gán role: **openstack project list**
- Gán role cho cặp user-project: **openstack role add --user USER_NAME --project TENANT_ID ROLE_NAME**
- Xác minh việc gán role: **openstack role assignment list --user USER_NAME  --project PROJECT_ID --names**

### 2.2. Glance: Thêm, sửa, xóa các Images.

- Thêm Image:

**openstack image create**

**[--id (id) ]**

**[--store (store)]**         

**[--container-format (container-format)]**

**[--disk-format (disk-format)]**

**[--size (size)]**

**[--min-disk (disk-gb)]**

**[--min-ram (ram-mb)]**

**[--location (image-url)]**

**[--copy-from (image-url)]**

**[--file (file) | --volume (volume)]**

**[--force]**

**[--checksum (checksum)]**

**[--protected | --unprotected]**

**[--public | --private | --community | --shared]**

**[--property (key=value) [...] ]**

**[--tag (tag) [...] ]**

**[--project (project)]**

**[--project-domain (project-domain)]**

**image-name**

Trong đó:

- container-format bao gồm ami, ari, aki, bare, docker, ova, ovf, mặc định bare.

- disk-format: ami, ari, aki, vhd, vmdk, raw, qcow2, vhdx, vdi, iso, và plop, mặc định raw.

- Xóa Image:

**openstack image delete image**

- Sửa Image:

**openstack image set**

**[--name (name)]**

**[--min-disk (disk-gb)]**

**[--min-ram (ram-mb)]**

**[--container-format (container-format)]**

**[--disk-format (disk-format)]**

**[--size (size)]**

**[--protected | --unprotected]**

**[--public | --private | --community | --shared]**

**[--store (store)]**

**[--location (image-url)]**

**[--copy-from (image-url)]**

**[--file (file)]**

**[--volume (volume)]**

**[--force]**

**[--checksum (checksum)]**

**[--stdin]**

**[--property (key=value) [...] ]**

**[--tag (tag) [...] ]**

**[--architecture (architecture)]**

**[--instance-id (instance-id)]**

**[--kernel-id (kernel-id)]**

**[--os-distro (os-distro)]**

**[--os-version (os-version)]**

**[--ramdisk-id (ramdisk-id)]**

**[--deactivate | --activate]**

**[--project (project)]**

**[--project-domain (project-domain)]**

**[--accept | --reject | --pending]**

**image**

Ví dụ ta tạo một Image tên là image1, với disk-format là qcow2 và container-format là bare:

![](https://i.imgur.com/cFW2Ute.png)

![](https://i.imgur.com/BFIoG9D.png)

Sau đó sửa Image này, ví dụ chỉnh lại disk-format từ qcow2 thành iso:

![](https://i.imgur.com/9Ich0yS.png)

![](https://i.imgur.com/lgMYRuw.png)

Xóa image1:

![](https://i.imgur.com/l6rmGJW.png)

![](https://i.imgur.com/CDaqApJ.png)





### 2.3. Neutron: Thêm, sửa, xóa các network.

#### 2.3.1. Thêm, sửa các network:

- Thêm network: **neutron net-create (net-name)**

Ví dụ:

![](https://i.imgur.com/CErAfah.png)

- Tạo thêm subnet cho net1 vừa mới tạo: **neutron subnet-create net1 192.168.1.0/24 --name subnet1**

![](https://i.imgur.com/1c12d5X.png)

![](https://i.imgur.com/mINxNhk.png)

#### 2.3.2. Xóa network: openstack delete (network ID)



### 2.4. Nova:

#### 2.4.1. Thêm VM:
-	Xem danh sách các Image, flavor hiện có:
![](https://i.imgur.com/tP5KO9I.png)
-	Tạo SSH Key:
o	ssh-keygen -q -f -ssh-key Sau đó nhập password 2 lần.
o	nova keypair-add novakey --pub-key ssh-key.pub
-	Xem danh sách các network và tạo Instance:
![](https://i.imgur.com/qwSWRVE.png)
![](https://i.imgur.com/oKmvSiJ.png)
Ngoài ra ta có thể thêm Instance bằng Dashboard trong Project/Compute/Instances, chọn Launch Instance và chọn các thông số cho Instance.
- Note: Quá trình tạo Instance của em bị lỗi, tạo xong Instance thì status là error. Có thể do trong quá trình cài đặt devstack bị thiếu file gì đó, em sẽ thử cài lại xem sao =((
![](https://i.imgur.com/HtfR9Tt.png)
#### 2.4.2. Sửa, xóa VM:
-	Chúng ta có thể chỉnh sửa Instance trong phần Actions  Edit Instance hoặc chọn mũi tên.
-	Xóa Instance: Cũng trong phần Action, chọn mũi tên và chọn Delete Instance.

