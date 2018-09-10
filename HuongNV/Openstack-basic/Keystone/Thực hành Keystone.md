# Thực hành Keystone căn bản trên Devstack


## Mục lục


* [1. Getting token](#1)
* [2. Listing user](#2)
* [3. Listing projects](#3)
* [4. Listing groups](#4)
* [5. Listing roles](#5)
* [6. Listing domains](#6)
* [7. Thêm user with domain](#7)
* [8. Sử dụng Dashboard horizon](#8)


# Khởi tạo môi trường
```
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=123test
export OS_AUTH_URL=http://172.16.69.131/identity
export OS_IDENITY_API_VERSION=2
export OS_IMAGE_API_VERSION=2
```


<a name="1"></a>

# 1. Getting token

Để lấy thông tin về token, sử sụng Openstack Client:

```
openstack token issue
```

![Imgur](https://i.imgur.com/CiSX9hq.png)
<a name="2"></a>

# 2. Listing user

- Các user này được tạo tự động khi cài Devstack. Mỗi service sẽ có một user như Nova, Neutron, Cinder...
- Sử dụng Openstack Client: 

```
openstack user list
```

![Imgur](https://i.imgur.com/w2cKTXb.png)
<a name="3"></a>

# 3. Listing projects

- Mặc định cài Devstack, sẽ có một vài project được tạo như: demo, admin, service...
- Sử dụng Openstack Client để liệt kê các project:

```
openstack project list
```

![Imgur](https://i.imgur.com/dIGLrW1.png)

## Add project within domain

- với domain `huong` vừa tạo, ta tiến hành add new project trong domain đó

```
openstack project create huong --domain huong --description "add new project within domain huong"
```
![Imgur](https://i.imgur.com/UAG4XRT.png)
<a name="4"></a>

# 4. Listing groups

- Sử dụng Openstack Client để liệt kê các groups:

```
opensack group list
```

![Imgur](https://i.imgur.com/O1Eh1Tm.png)

<a name="5"></a>

# 5. Listing roles

- Sử dụng Openstack Client

```
openstack role list
```

![Imgur](https://i.imgur.com/6R6RZAM.png)

## Tạo mới một role

```
openstack role create huong
```

![Imgur](https://i.imgur.com/Tl4p4vJ.png)

## Assign new role within user

```
openstack role add huong --project huong --project-domain huong --user huong --user-domain huong
```

![Imgur](https://i.imgur.com/hW00jnr.png)

<a name="6"></a>

# 6. Listing domains

- Sử dụng Openstack Client

```
openstack domain list
```

![Imgur](https://i.imgur.com/1muetgi.png)
## Create new domain

```
openstack domain create huong
```

![Imgur](https://i.imgur.com/DHzE2s3.png)

<a name="7"></a>

# 7. Thêm user within domain

- Sử dụng Openstack Client

```
openstack user create huong --domain Default --email huong.0496@gmail.com --description "test add user" --password huong
```
![Imgur](https://i.imgur.com/JkYWC5O.png)

<a name="8"></a>

# 8. Sử dụng Dashboard horizon

- Sử dụng Dashboard để liệt kê tất cả các projects, user, domains và roles...

![Imgur](https://i.imgur.com/WxlyPL9.png)


![Imgur](https://i.imgur.com/Oi04Yv9.png)


![Imgur](https://i.imgur.com/SiwPPZ3.png)

