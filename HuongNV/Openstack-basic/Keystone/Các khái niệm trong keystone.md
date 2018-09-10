# Một số khái niệm trong Keystone

## Mục lục

* [1. User and User group](#1)
* [2. Project](#2)
* [3. Roles](*3)
* [4. Domain](#4)
* [5. Assignment](#5)
* [6. Targets](#6)
* [7. Tokens](#7)
* [8. Catalogs](#8)


<a name="a"></a>

# 1. User
- User and User group là nhóm các thực thể được cấp quyền truy cập các bộ phận được cô lập trong Domain hoặc Project.
- Một thực thể nhận dạng API v3. Groups là một tập hợp các `users` cùng thuộc một domain. Một `group role` được cấp cho một domain hoặc một project và sẽ được áp dụng cho tất cả các user nằm trong đó.

    * 1.1 Graphical representation 
        - Mối quan hệ giữa domain, projects, users and groups được thể hiện như hình dưới. Users, groups and projects luôn nằm trong một `domains`. 
        - Mỗi cá thể sẽ có một số hiệu định danh UUID là duy nhất. Tuy nhiên giữa các domain với nhau, định danh cúa cá thể có thể giống nhau, vì vậy việc cung cấp `domains` kèm theo sẽ giúp việc tìm kiếm các tài nguyên một cách dễ dàng hơn.

    ![Imgur](https://i.imgur.com/VnRQELZ.png)

<a name="2"></a>

# 2. Projects
* Trong Keystone, một `project` là một khái niệm trừu tượng được sử dụng vởi các service trong Openstack nhằm nhóm và tách biệt các tài nguyên với nhau( ví dụ servers, images..)
* Trong những phiên bản đầu, project còn gọi là `tenants` và về sau nó được thay đổi thành `projects`, một cái tên nghe có vẻ trực quan và gần gũi hơn.
* Mục đích của Keystone là tạo ra các project và phân cấp xem những ai có thể truy cập vào project đó.
* Bản thân các projects không chứa các Users hoặc Users groups, thay vào đó User và Users group sẽ sử dụng một khái niệm là `roles` để có thể truy cập vào projects đó.
    

<a name="3"></a>

# 3. Roles

Roles được sử dụng trong Keystone có nghĩa là truyền đạt sự cho phép. Một hành động có thể có nhiều role và cùng thực hiện một target.

<a name="4"></a>

# 4. Domain

- Trong môi trường Openstack, domains là tập hợp của các user và projects, nó có nhiệm vụ tách biệt các nguồn tài với nhau.
- Mỗi domains có thể hiểu như là từng bộ phận trong một enterprise hoặc có thể là từng enterprise riêng rẽ với nhau.
- Lợi ích củ việc sử dụng Domains:
    - Khả năng kiểm soát dựa trên vài trò chức năng, Role Based Access Controll(RBAC)
    - Tạo ra cloud adminitrastors với khả năng phân quyền tác vụ cho người dùng
    - Support các nguồn tài nguyên có thể trùng lặp, ví dụ `username` giữa các domain với nhau
    - The ability for separate oranizations to leverage different backends.



<a name="5"></a>

# 5. Assignments

- Role assignment là sự kết hợp giữa một hành động, một mục tiêu và một role với nhau.
- Role asignment được cấp và thu hồi và có thể được kế thừa giữa groups và users hoặc giữa projects với domains

<a name="Targets">

# 6. Targets

Projects và Domain rất giống nhau ở chỗ cả hai đều là các thực thế có trong đó vai trò là `assigned on`. Nói một cách khác, một Users hoặc Users Group đưcọ cấp quyền truy cập vào một Projects hoặc Domain bằng một giá trị gọi là Role value. Chính vì những điểm tương đồng như vậy nên chúng ta gọi chúng chung là `Targets`


<a name="7"></a>

# 7. Tokens

 - Để có thể gọi tới bất kì một Openstack API nào đó, user cần phải xác thực rằng họ là ai và có quyền hạn gì
 - Cái cách để thực hiện điều này là sẽ truyền `token` vào mỗi lần truy cập thông qua API mà Keystone đóng vai trò là bộ phần tạo ra các chuỗi `token` này và cung cấp tới cho user.
 - Các token mang theo tính authorizations. Nó chứa sự ủy quyền mà mỗi user có trong môi trường cloud. Mỗi token đều có `ID` và `prayload`
 - ID của mỗi token được đảm bảo là duy nhất trên mỗi miền cloud và prayload chứa dữ liệu về người dùng.


# Hình dưới đây mô tả ví dụ về 1 token

![Imgur](https://i.imgur.com/VJIaTSj.png)


- Một prayload token chứa rất nhiều data như:
    - issue at: Thời gian tạo ra token
    - expire at: Thời gian hết hạn
    - project ID, project name
    - domain ID, domain name


<a name="8"></a>

# 8. Catalogs

- Danh mục dịch vụ (service catalogs) là cần thiết cho môi trường cloud Openstack. Nó chứa các URL và end-points của mỗi different sirvice trong Openstack. Không có Catalogs, user và application sẽ không rõ nới nào để gửi đi các request tạo ra các VM hoặc store objects. 
- Mỗi service catalog được chia thành các end-points, mỗi endpoints được chia thành URL admin, URL internal và public URL

![Imgur](https://i.imgur.com/kW1repu.png)