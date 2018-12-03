# Cài đặt Gitlab sử dụng Docker

# Mục lục
- [1. Pull images](#1)
- [2. Run images](#2)

<a name="1"></a>

## 1. Pull images

Bản hướng dẫn cài đặt Gitlab CE. Thực hiện pull image về tại đưỡng dẫn sau:[Gitlab CE](https://hub.docker.com/r/gitlab/gitlab-ce/)

Sử dụng command line để pull image
```
docker pull gitlab/gitlab-ce
```

Thực hiện kiểm tra image sau khi đã pull thành công:

![Imgur](https://i.imgur.com/Xwua3Xb.png)

<a name="2"></a>

## 2. Run images

Sử dụng command line như sau:
```
docker run -it -d --hostname gitlab.example.com \ 
        --publish 443:443 --publish 8080:80 --publish 8822:22 \
        --name gitlab \
        --restart always \
        --volume /srv/gitlab/config/:/etc/gitlab \
        --volume /srv/gitlab/logs/:/var/log/gitlab \ --volume/srv/gitlab/data/:/var/opt/gitlab \
        gitlab/gitlab-ce
```

Trong đó:
- port 443, 8080, 8822: Truy cập Gitlab qua HTTPS, HTTP và SSH
- restart: Khởi động lại gitlab khi host khởi động lại
- volume: Định danh location để lưu trữ dữ liệu 

| Local location   | Container location | Mục đích                   |
| ---------------- |:------------------:| --------------------------:|
|/srv/gitlab/data  | /var/opt/gitlab    |Lưu trữ dữ liệu của ứng dụng|
|/srv/gitlab/logs  | /var/log/gitlab    |Thư mực quản lý log         |
|/srv/gitlab/config| /etc/gitlab        |Lưu trữ các cài đặt Gitlab  |

Thực hiện run image thành công, tiến hành kiểm tra:

![Imgur](https://i.imgur.com/w1HNyd8.png)

