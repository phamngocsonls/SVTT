# Tìm hiểu về Cinder

## Mục lục

* [1. Giới thiệu về Cinder](#1)
* [2. Key concepts](#2)
    * [2.1 Volume](#2.1)
    * [2.2 Snapshot](#2.2)
    * [2.3 Backend](#2.3)
    * [2.4 Driver](#2.4)
    * [2.5 Volume Type](#2.5) 
* [3. Process Structure](#3)
    * [3.1 Volume Creation Workflow](#3.1)
    * [3.2 Volume Attach Workflow](#3.2)




<a name="1"></a>

# 1. Giới thiệu về Cinder

- Openstack Block Storage cung cấp quản lý tài nguyên lưu trữ theo khối. 
- Block Storage cung cấp hạ tầng để quản lý volumes và tương tác với Nova project nhằm cung cấp volumes cho instances. Block Storage còn hỗ trợ quản lý volumes snapshot and volume types.
- Với Block Storage, ta có thể write images to Cinder nhằm phục vụ boot for instances.

Hình dưới đây mô tả Cinder and Nova Architecture:

![Imgur](https://i.imgur.com/yfU7s3S.png)


<a name="2"></a>

# 2. Key concepts

<a name="2.1"></a>

## 2.1 Volume

- Cinder Volume là tài nguyên cơ bản được cung cấp bởi Block Storage service
- Nó đại diện cho phân bổ lưu trữ khối liên tục, có thể làm root disk for compute instance hoặc secondary storage mà có thể attached/detached from compute instances.

<a name="2.2"></a>

## 2.2 Snapshot

- Cinder snapshoe là một read-only copy of a Cinder volume.
- Cinder snapshot có thể đóng vài trò là content source cho Cinder volume khi Cinder volume được chỉ định create từ một Cinder snapshot cụ thể nào đó.

<a name="2.3"></a>

## 2.3 Backend

- Cinder backend là một configuration object đại diện cho một single provider of block storage.
- Cinder backend communicate với storage system qua Cinder driver


<a name="3"></a>

# 3. Process Structure

Có 4 quy trình để tạo nên một Cinder service:
* **Cinder-api**:
    * Là ứng dụng WSGI có vài trò là chấp nhận và xác nhận các yêu cầu REST request
* **Cinder-scheduler:**
    * Xác định backend nào là đích khi thực hiện creation volume
* **Cinder-volume:**
    * Kết nối trực tiếp tới các khối lưu trữ backend và quản lý chúng
* **cinder-backup:**
    * Phục vụ nhu cầu backup volumes

![Imgur](https://i.imgur.com/YyMmzV3.png)

<a name="3.1"></a>

## 3.1 Volume Creation Workflow

Các bước cụ thể khi user request to create a new volume từ Cinder

![Imgur](https://i.imgur.com/ZFlC0nb.png)


1. Client request to create volume qua REST API hoặc có thể sử dụng qua CLI `python-cinderclient`
2. `cinder-api` xử lý tính xác thực của request, nếu xác thực thành công, nó send messages tới AMQP queue chờ lần xử lý kế tiếp
3. `cinder-volume` xử lý message từ AMQP queue và gửi một message tới `cinder-scheduler` để xác định backend volume
4. `cinder-scheduler` xử lý message từ queue, tạo ra 1 list candidate dự trên trạng thái hiện tại và tiêu chí yêu cầu như: size, availability zone, volume type)
5. `cinder` volume xử lý response từ cinder-scheduler, lặp qua list candidate bằng cách gọi các backend driver cho tới khi thành công.
6. NetApp Cinder driver tạo một request volumes qua một kết nối tới system storage
7. `cinder-volume` xử lý các volume metadata, các thông tin evef kết nối và gửi response về queue
8. `cinder-api` xử lý message từ AMQP queue và gửi response về clients
9. Clients nhận đầy đủ thông tin về trạng thái của volume request, UUID volume


<a name="3.2"></a>

## 3.2 Volume Attach Workflow

Các bước cụ thể khi user request Cinder volume to attach a Nova compute instances:

![Imgur](https://i.imgur.com/sHYgw7o.png)


1. Client gửi request to attach volume qua Nova REST API hoặc qua CLI sử dụng python-novaclient
2. **nova-api** xử lý thông tin xác thực của request, nếu xác thực hợp lệ, gọi tới Cinder API để lấy thông tin kết nối cho một volume cụ thể
3. **inder-api** xử lý request từ nova-api, nếu hợp lệ, gửi một mesage tới AMQP queue
4. **cinder-volume** đọc message từ queue, gọi tới Cinder driver nhằm xác dịnh volume to ve attach
5. NetApp Cinder driver chuẩn bị volume cho việc attachment 
6. **cinder-volume** gửi response information tới cinder-api qua AMQP queue
7. **cinder-api** xử lý thông tin từ cinder-volume, passess connection information in RESTful response tới NOVA caller
8. Nova thiết lập kết nối tới storage với information nhận được từ Cinder
9. Nova passes the volume device/file to hypervisor in Nova, sau đó attach volume tới VM như là một actual hoặc virtualized block device

![Imgur](https://i.imgur.com/c2jTTMK.png)

