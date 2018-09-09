---
title: Tổng quan về Ceph Storage
date: 2018-09-08
---

## Tổng quan về Ceph Storage

## Mục lục
- [1. Ceph - Hệ thống lưu trữ phân tán có thể mở rộng](#1)
- [2. Các thành phần của một Ceph storage cluster](#2)

## Nội dung

<a name="1"></a>

### 1. Ceph - Hệ thống lưu trữ phân tán có thể mở rộng

Ceph là một giải pháp mã nguồn mở để xây dựng hạ tầng lưu trữ phân tán, ổn định, hiệu năng cao. Triển khai [object storage](#object-storage) trên một cụm máy tính phân tán thống nhất và cung cấp các dạng lưu trữ object-, block- và file-based storage có khả năng mở rộng được.

#### Tính năng:
- Không gặp phải "single point of failure"
- Có khả năng mở rộng tới mức exabyte (1EB = 10^18 bytes)
- Sử dụng thuật toán Controlled Replication Under Scalable Hashing (CRUSH) đảm bảo dữ liệu được phân tán như nhau tới các cụm và tất cả các node cụm có thể lấy lại dữ liệu một cách nhanh chóng mà không có bất kỳ một sự tắc nghẽn nào.
- Hoàn toàn miễn phí

### 2. Các thành phần của một Ceph storage cluster

<a name="2"></a>

Một Ceph storage cluster yêu cầu ít nhất một Ceph Monitor, Ceph Manager và Ceph OSD (Object Storage [Daemon](/VINHNT/nodes.md/#daemon)) và Ceph Metadata Server cũng được yêu cầu khi chay Ceph Filesystem clients.

1. **Monitors**: một Ceph Monitor (ceph-mon) duy trì bản đồ trạng thái các cụm, bao gồm monitor map, manager map, OSD map, và CRUSH map. Các bản đồ này là trạng thái cụm quan trọng cần thiết cho các Ceph daemons liên kết toạ độ với nhau. Monitor cũng chịu trách nhiệm cho việc quản lý sự uỷ quyền giữa các daemons và clients. Thường có ít nhất 3 monitors được yêu cầu cho dự trữ và sẵn sàng dụng cao.
2. **Managers**: (Ceph manager daemon - ceph-mgr) theo dõi các thông số thời gian chạy và trạng thái hiện tại của Ceph cluster, bao gồm: việc sử dụng bộ nhớ, các thông số hiệu suất hiện tại, và tải hệ thống. Thông thường cần ít nhất 2 managers cho tính sẵn sàng cao.
3. **Ceph OSDs**: (Object Storage Daemon, ceph-osd) Một Ceph OSD lưu trữ, xử lý, phục hồi, tái cân bằng, và cung cấp một vài monitoring information to Ceph Monitors và Managers bằng việc kiểm tra một tín hiệu (heartbeat) từ Ceph OSD Daemon khác. Cần 3 ceph OSD cho dự trữ và tính sẵn sàng cao.
4. MDSs: (MDS, ceph-mds) lưu trữ metadata trên danh nghĩa của Ceph Filesystem (Ceph block devices và Ceph Object Storage không sử dụng MDS). Ceph Metadata Servers cho phép người dùng [POSIX](nodes.md/#POSIX) file system thực thi các câu lệnh cơ bản (vd: ls, find,...) mà không đặt gánh nặng lên Ceph Storage Cluster.


## Các khái niệm

<a name="object-storage"></a>

Object-storage (object-based storage) là một kiến trúc lưu trữ dữ liệu máy tính mà quản lý dữ liệu như là các objects.

Block-storage là một kiến trúc lưu trữ dữ liệu máy tính mà quản lý dữ liệu như các blocks bên trong sectors và tracks.

Filesystem cũng là một kiến trúc lưu trữ dữ liệu máy tính nhưng quản lý dữ liệu như một hệ thống cấp bậc các thư mục.

<a name="daemon"></a>

Daemon trong linux là một tiến trình chạy nền không chịu kiểm soát trực tiếp từ người dùng và có thể bật tắt mà không ảnh hưởng đến giao diện người dùng.

<a name="POSIX"></a>

POSIX (The Portable Operating System Interface) duy trì khả năng tương thích giữa các hệ điều hành. POSIX định nghĩa các API cùng với các command shells và tiện ích cho khả năng tương tác với các biến thể của Unix và các hệ điều hành khác.

## Tham khảo

[1. http://docs.ceph.com/docs/master/start/intro/](http://docs.ceph.com/docs/master/start/intro/)
[2. https://en.wikipedia.org/wiki/Ceph_(software)](https://en.wikipedia.org/wiki/Ceph_(software))