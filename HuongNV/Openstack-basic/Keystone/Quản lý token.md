# Một vài tìm hiểu về Token


## Mục lục

* [1. History Tokens of Format](#1)
* [2. UUID tokens](#2)
    * [2.1 Token Generation Workflow](#2.1)
* [3. PKI tokens](#3)
    * [3.1 Token Generation Workflow](#3.1)
* [4. Fernet token](#4)
    * [4.1 Fernet Key](#4.1)
    * [4.2 Where put key repository](#4.2)

<a name="1"></a>

# 1. History Tokens of Format

Keystone cung cấp một vài định dạng `token` và người dùng có thể thắc mắc tại sao lại có nhiệu định dạng về token đến như vậy. Để đi tìm câu trả lời, chúng ta sẽ đi tìm hiểu một chút về lịch sử token format. Trong những ngày đầu, Keystone cung cấp `UUID` token. UUID hỗ trợ tối đa 32 kí tự nhằm hỗ trợ cho việc xác thực user cũng như phân quyền người dùng. Lợi ích lớn nhất là nó mạng lợi là rất nhỏ gọn và dễ sử dụng. Nhược điểm của mã token này là không mang kèo theo đủ thông tin để có thể ủy quyền trong cục bộ. Các services trong Openstack luôn phải gửi kèm theo token tới Keystone server để có thể xác định quyền hạn của chúng và nó gấy thắt nút cổ chai trong môi trường Openstack cloud.

Để có thể khắc phục những nhược điểm maf UUID token gặp phải, Keystone sử dụng một mã token mới gọi là `PKI` token. Mã token này chứa đầy đủ thông tin để có thể ủy quyền trong cục bộ và nó còn chứa một danh mục service kèm theo. Ngoài ra, mã token PKI được đăng kí, nó có thể lưu vào bộ nhớ `cache` và có thể sử dụng nó bất kì đâu cho đến khi hết hạn cũng như bị thu hồi. Điều đáng tiếc nhất khi sử dụng PKI token là kích thước lớn, nó chiếm tới `8KB` trong bộ nhớ và rất khó có thể chèn chúng trong bản tin HTTP header. Ngoài ra, PKI token khó sử dụng hơn khi dùng `cURL` command và gây đôi chút khó khăn cho người mới sử dụng. Keystone team cố gắng cải thiện PKI thành một mã mới gọi là PKIz nhưng kích thước của nó vẫn rất lớn.

Nhằm khác phục nhược điểm của PKI, Keystone team tạo ra một mã token mới, đó là `Fernet` token. Fernet token nhỏ gọn, nó chứa tối đa 255 kí tự, mang đầy đủ thông tin để có thể ủy quyền cục bộ, từ đó Keystone không cần phải lưu dữ liệu của token trong database của nó. 

Một trong những điều gấy nhức nhối nhất trong những ngày đầu là mọi dữ liieeuj về token đều lưu giữ trong database của Keystone. Khi database đầy, nó sẽ gấy tắc nghẽn và làm giảm hiệu năng của hệ thống. Fernet token có khó khăn là cặp khóa đối xứng cần được phân phối và xoay vòng. Các nhầ vận hành Keystone đã làm việc với nhau với mong muốn sử dụng nhiều hơn mã `fernet` token này so với các mã token khác và sẽ chịu trách nhiệm về việc xóa database trong Keystone.


Dưới đây là một bản khảo sát về mức độ sử dụng của các loại token trong phiên bản Juno. Cuộc khảo sát này không kèm theo Fernet token cho tới khi bản Kilo phát hành.

![Imgur](https://i.imgur.com/zaGIipF.png)




<a name="2"></a>

# 2. UUID tokens

* Mã token đầu tiên của Keystone là UUID. UUID là một mã ngẫu nhiên 32 kí tự, được sử dụng bởi dịch vụ identity service. Phương thức hexdigest() được sử dụng, đảm bảo các mã token này hiển thị dưới dạng thập lạng phân. 
* Mã UUID token thường được lưu tại một database backend để có thể dử dụng cho lần xác thực tiếp theo.
* UUID token có thể thu hồi dễ dàng với bản tin DELETE reuqest kèm theo đó là token ID. Các mã token này sẽ không bị removed khỏi database backend và được đánh dâu là mã token này đã được thu hồi.

## Ví dụ dơn giản về UUID token như sau: `468da447bd1c4821bbc5def0498fd441`, một chuỗi dài 32 kí tự

![Imgur](https://i.imgur.com/rySD53n.png)

- UUID token nhỏ gọn, dễ dàng sử dụng trong cURL command. Nhược điểm là Keystone sẽ trở thành nút thắt cổ chai khi một lượng lớn communication xảy ra trong quá trình yêu cầu Keystone xác thực.



<a name="2.1"></a>

## 2.1 Token Generation Workflow

![Imgur](https://i.imgur.com/zxGaHMX.png)

<a name="3"></a>

# 3. PKI tokens

- Loại token thứ 2 mà Keystone hỗ trợ đó là PKI token. PKI token chứa rất nhiều thông tin trong đó như: token được tạo khi nào, khi nào hết hạn, user identicafication, project, domain, role information for user, a service catalog. Những thông tin này được hiển thị dưới dạng JSON prayload.
- Ví dụ về một PKI token như sau:

![Imgur](https://i.imgur.com/ZOAC2Du.png)

```
{
    "token": {
        "domain": {
            "id": "default",
            "name": "Default"
        },
        "methods": [
            "password"
        ],
        "roles": [
            {
                "id": "c703057be878458588961ce9a0ce686b",
                "name": "admin"
            }
        ],
        "expires_at": "2014-06-10T21:52:58.852167Z",
        "catalog": [
    {
        "endpoints": [
            {
                "url": "http://localhost:35357/v2.0",
                "region": "RegionOne",
                "interface": "admin",
                "id": "29beb2f1567642eb810b042b6719ea88"
            },
            {
                "url": "http://localhost:5000/v2.0",
                "region": "RegionOne",
                "interface": "internal",
                "id": "87057e3735d4415c97ae231b4841eb1c"
            },
            {
                "url": "http://localhost:5000/v2.0",
                "region": "RegionOne",
                "interface": "public",
                "id": "ef303187fc8d41668f25199c298396a5"
            }
        ],
        "type": "identity",
        "id": "bd7397d2c0e14fb69bae8ff76e112a90",
        "name": "keystone"
    }
],
"extras": {},
"user": {
    "domain": {
        "id": "default",
        "name": "Default"
    },
        "id": "3ec3164f750146be97f21559ee4d9c51",
        "name": "admin"
    },
    "audit_ids": [
        "Xpa6Uyn-T9S6mTREudUH3w"
    ],
    "issued_at": "2014-06-10T20:52:58.852194Z"
    }
}
```
<a name="3.1"></a>


## 3.1 Token Generation Workflow

![Imgur](https://i.imgur.com/puM05pC.png)


- So sánh PKI và PKIz:

![Imgur](https://i.imgur.com/RPLfT4m.png)
![Imgur](https://i.imgur.com/voI5ZbZ.png)


<a name="4"></a>

# 4. Ferner Token

- Fernet token là mã token mới nhất. Nó có độ dài 255 kí tự, kích thước lớn hơn UUID toke và nhỏ hơn PKI token.
- Fernet token chuwqas một số thông tin như: user identifier, a project identifier, token expiration và một số thông tin khác.
- Fernet token được đăng kí bằng cách sử dụng cặp khóa đối xứng để ngăn chặn việc mạo danh token.

Fernet token sử dụng cặp khóa đối xứng, chúng được phân phối tới các Openstack regions và xoay vòng. Fernet đang được cải thiện và cập nhật trong việc phân phối, xoay vòng các cặp khóa đối xứng.

- A typical Fernet token look like:

```
gAAAAABU7roWGiCuOvgFcckec-0ytpGnMZDBLG9hA7Hr9qfvdZDHjsak39YN98HXxoYLIqVm19Egku5YR
3wyI7heVrOmPNEtmr-fIM1rtahud
```

<a name="4.1"></a>

## 4.1 Fernet key

- Fernet key được dùng để mã hóa và giải mã token.
- Mỗi key sẽ được chia làm 2 phần: phần thứ nhất 128 bit dùng để mã hóa AES và 128 bit SHA256 dùng cho việc HMAC singing key.
- Có 3 loại key đó là: Primary key, Secondary key và Staged key
    * Primary key:
        * Nó được dùng để mã hóa và giải mã token. 
        * Khóa này luôn được đặt tên là chỉ mục cao nhất trong kho lưu trữ

    * Sencondary key:
        * Secondary là 1 kháo chính nhưng đã bị giáng cấp so với Primary key.
        * Nó chỉ có thể giả mã token

    * Staged key:
        * Là loại key đặc biệt, cũng giống như Secondary key, chỉ có thể giải ãm token.
        * Staged key sẽ trờ thành Primary key tiếp theo và Staged key luôn được đặt tên là `0` ở trong key repository

<a name="4.2"></a>

## 4.2 Where put key repository

Key repository được chỉ định cụ thể vị trí lưu trong keystone configuration. Keystone chỉ hỗ trợ lưu trữ key duy nhất dưới dạng `file-backed`

```
[fernet_tokens]
key_repository = /etc/keystone/fernet-keys/
```

