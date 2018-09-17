# Một vài thực hành về Nova trên Devstack

## Mục lục

- [1. Nova flavor](#1)
- [3. Nova security-group](#3)


<a name="1"></a>

# 1. Nova flavor

- Flavors định nghĩa memory và phân vùng lưu trữ storage capacity cho nova computing instances. Hiểu một cách đơn giản, flavor là cấu hình giống như một máy chủ ảo, kích thước của máy chủ ảo này được định nghĩa bằng các thông số bởi flavor

- Một flavor bao gồm các thành phần như sau:
    - **Flavor ID**: Định danh cho flavor
    - **Name**: Tên đặt cho flavor
    - **VCPUs**: Chỉ định số virtual CPUs sử dụng, thông số này bắt buộc
    - **Memory MB**: Chỉ định dung lượng RAM cho flavor, thông số này bắt buộc
    - **Root Disk GB**: Dung lượng của ổ đĩa disk, thông số này bắt buộc


<a name="2"></a>

# 2. Nova security-group

- Security-group thiết lập các IP filter rules cho tất cả các instances.
- Tất cả các projects đều có một `default` security-group và được áp dụng cho tất cả các instances trong project đó
- Mặc định `default` seciruty group cho phép traffic của instances đi ra ngài internet và deny tất cả các traffic từ bên ngoài vào instances
- Một vài command line hay sử dụng:
    - Liệt kê tất cả các security-group
    ```
    openstack security group list
    ```
    - Xem chi tiết về 1 security group nào đó
    ```
    openstack security group rule list <GROUP_NAME>
    ```
    - Tạo mới 1 security-group
    ```
    openstack security group create GroupName --description Description
    ```
    - Tạo mới rule
    ```
    openstack security group rule create SEC_GROUP_NAME protocol PROTOCOL --dst-port FROM_PORT:TO_PORT --remote-ip CIDR
    ```
    - Xóa một security-group
    ```
    openstack security group delete GROUPNAME
    ```

