# Tìm hiểu KVM
* Tuần 4
* Người tạo: Nguyễn Xuân Lưu

# [Hướng Dẫn Sử Dụng KVM](#1)
## [2. Quản Lý KVM bằng giao diện người dùng](#1.2)

### 2.3 Di chuyển, Back up, Clone và Xóa máy ảo

**Di chuyển**

Việc di chuyển một máy ảo từ phần cứng vật lý này tới phần cứng vật lý khác sẽ cần thiết trong công tác bảo trì bảo dưỡng, thay thế, nâng cấp phần cứng vật lý của hệ thống.

Để thực hiện di chuyển, ta cần thiết lập kết nối từ virt-manager của máy nguồn tới máy đích. Công việc được thực hiện qua việc add connect từ cửa sổ chính của virt-manager, ở đây, ta sử dụng giao thức SSH.

<img>

Sau khi hoàn tất việc thiết lập kết nối. Chọn chuột phải và máy ảo muốn di chuyển, chọn migrate và chọn địa chỉ đích đã tạo ở phía trên. Do hạn chế về thiết bị, em không thể thực hiện bước này.

<img>

**Back up**




### 2.4 Quản lý chi tiết các tài nguyên phần cứng ảo hóa

//TODO

## 3. Quản lý KVM bằng giao diện dòng lệnh với virsh và các công cụ liên quan

//TODO

## 4. Quản lý KVM bằng giao diện dòng lệnh với nhóm công cụ hỗ trợ từ QEMU

//TODO

