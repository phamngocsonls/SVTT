
Workflow chart dưới đây chỉ ra cơ chế authentication khi user muốn create 1 Virtual machine:

![Imgur](https://i.imgur.com/jhA7OfL.png)

- Để có thể access tới 1 service nào đó, user cung cấp thông tin xác thực tới Keystone và nhận lại được token. Token này là một chuỗi nhằm kết nối user tới các project trong Openstack.
- User có được URL service muốn truy cập tới. Ví dụ user có thể có được URL tới Nova project trong list endpoints để có thể tạo 1 VM
- Sau đó Nova sẽ check validation của token trong Keystone và tạo 1 VM và gán cho VM vào 1 network subnets


![Imgur](https://i.imgur.com/uTYrqin.png)