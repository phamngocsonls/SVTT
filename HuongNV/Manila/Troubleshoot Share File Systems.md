# Troubleshoot Shared File Systems service

# 1. Failure in Share File Systems service during a share creation

## Problem

New shares có thể xảy ra lỗi trong quá trình khởi tạo

## Solution

    1. Chắn chắn rằng share services đang chay ở debug mode. Nếu debug mode is not set, ta phải đọc logs để có thể fix vấn đề này
    2. Sử dụng commnad `manila show <share_id_or_name>` để heienr thị tất cả các share đã create và coi được share service nào đang hoạt động hay là bị broken
    3. Khi gặp bất kì một vấn đề gì đó, truy cập tại đường dẫn `/etc/vả/log/manila-share.log` để có thể hiểu rõ hơn về vấn đề mà đang gặp phải


# 2. No valid host was found

## Problem

Nếu một share type chứa một vài thông số không hợp lệ, manila-scheduler không thể xác định được vị trí host mà lưu trữ các share này

## Solution

- Kiểm tra lại các thông số đã set khi thực hiện khởi tạo a share
- Kiểm tra log tại `/etc/var/log/manila-scheduler.log`

# 3. Created share is unreachable

## Problem

Mặc định, a new share không có bất kì access rules nào cả

## Solution

To provide access to new share, ta cần khởi tạo quy tắc access với giá trị thích hợp

# 4. Service becomes unavailble after upgrade

## Problem

Khi thực hiện upgrade Shared File Systems service từ v1 lên v2.x, ta phải update service endpoint tại Openstack Identity service, Khi đó dịch vụ Shared File có thể không hoạt động

## Solution

- Get the service type related to the Shared File Systems service

```
# openstack endpoint list
# openstack endpoint show <share-service-type>
```
- Chắn chắn rằng endpoints đã được update, xóa bỏ các endpoints đã hết hạn và thực hiện khởi tạo một endpoint mới


## Tài liệu tham khảo

- https://docs.openstack.org/manila/pike/admin/shared-file-systems-troubleshoot.html



