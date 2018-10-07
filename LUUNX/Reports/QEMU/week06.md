# Tìm Hiểu QEMU

## Giới thiệu chung

QEMU (viết tắt của Quick Emulator) là một phần mềm mã nguồn mở cho phép phỏng tạo và ảo hóa máy ảo.

Các chế độ của QEMU

* User-mode emulation

Trong chế độ này, QEMU cho phép chạy các chương trình được biên dịch cho một kiểu kiến trúc sang một kiểu kiến trúc khác. Ví dụ, một chương trình trên windows chạy trên linux.

* System emulation

Trong chế độ này, QEMU phỏng tạo (Emulator) một hệ thống máy tính hoàn chỉnh, bao gồm các thiết bị ngoại vi. Nó có thể được dụng để tạo ra nhiều máy tính ảo trên một máy tính thật. QEMU có thể chạy nhiều hệ điều hành khách, bao gồm Linux, Solaris, Microsoft Windows, DOS và BSD. Nó hỗ trợ tập lệnh nhiều kiểu kiến trúc, bao gồm x86, MIPS, ARMv7, ARMv8, PowerPC, SPARC, ETRAX CRIS và MicroBlaze.

* KVM Hosting

Khi kết hợp cùng KVM, QEMU hỗ trợ phỏng tạo các thiết bị ngoại vi cho máy ảo, đồng thời, phần chạy các guest code của máy ảo sẽ được QEMU  gọi tới sự hỗ trợ của KVM.

* Xen Hosting

Đối với Xen, QEMU chỉ đảm nhiệm việc phỏng tạo phần cứng cho máy ảo. Việc thực thi các guest code của máy ảo hoàn toàn do XEN quản lý.


Các máy ảo thông qua sự hỗ trợ của QEMU có thể giao tiếp với các phần cứng vật lý của máy chủ, bao gồm hard disk, CD-ROM drives, network cards, audio interfaces và USB. Các thiết bị USB có thể được phỏng tạo hoàn toàn hoặc các thiết bị USB của máy chủ cũng có thể được sử dụng với các quyền của quản trị viên và không hoạt động với tất cả các loại thiết bị.

Các máy ảo có thể được lưu trữ ở định dạng đặc biệt ( qcow hoặc qcow2 ) ở bộ nhớ máy chủ. Chúng chỉ chiếm dung lượng đĩa mà máy ảo thực sự sử dụng. Bằng cách này, một ổ đĩa được mô phỏng cho máy ảo có kích thước 120 GB có thể chỉ chiếm cỡ vài trăm MB trên máy chủ. Định dạng QCOW2 cũng cho phép ghi lại sự khác biệt của file máy ảo hoạt động so với file máy ảo (chưa sửa đổi) trước khi cài đặt. Điều này cung cấp khả năng khôi phục nội dung của file máy ảo về trạng thái ban đầu. Ví dụ: khi máy ảo bị lỗi, do virus hoặc sự cố khác, thông qua định dạng file qcow2, máy ảo có thể khôi phục lại trạng thái trước đó. Đồng thời, QEMU có thể lưu và khôi phục trạng thái của máy ảo và tất cả các chương trình đang chạy trên máy ảo. Các hệ điều hành máy ảo không cần chỉnh sửa để chạy được bên trong QEMU.

QEMU có thể mô phỏng các card mạng và chia sẻ kết nối mạng của hệ thống máy chủ tới máy ảo bằng cách thực hiện dịch địa chỉ mạng, cho phép máy ảo sử dụng cùng một mạng với máy chủ. Các card mạng ảo cũng có thể kết nối với nhau để tạo một mạng ảo cục bộ.

QEMU không phụ thuộc vào các phương thức hiển thị đồ họa đầu vào đầu ra trên hệ thống máy chủ. Thay vào đó, nó có thể cho phép một người truy cập vào màn hình của hệ điều hành máy ảo thông qua một máy chủ VNC tích hợp.

## Cài đặt QEMU trên Ubuntu 16.04

Cài đặt QEMU từ source code

Mở terminal, gõ lệnh

```shell
sudo apt install zlib1-dev flex bison libcanberra-gtk*
wget https://download.qemu.org/qemu-3.0.0.tar.xz
tar xvJf qemu-3.0.0.tar.xz
cd qemu-3.0.0
mkdir build
cd build
../configure --enable-debug
time sudo make
sudo make install
```



## Kiến trúc QEMU

Tìm hiểu về chế độ system emulation của QEMU.

### High Level Overview

QEMU là một phần mềm, khi hoạt động nó chạy như một tiến trình trên máy chủ. Mỗi máy ảo khi được ảo hóa bằng QEMU sẽ tương ứng với một tiến trình QEMU chạy độc lập.

![.](../src-image/w6_1.PNG)

Khi một tiến trình QEMU khởi chạy, nó sẽ tạo trường cho máy ảo, khởi động hệ điều hành máy ảo. Đồng thời khi máy ảo tắt (do shutdown, poweroff), tiến trình QEMU sẽ bị hủy theo. Tuy nhiên trong trường hợp máy ảo reboot, tiến trình QEMU sẽ tiếp tục hoạt động.

QEMU là một tiến trình, nó sẽ được cấp phát không gian địa chỉ nhớ (RAM) riêng. Máy ảo chạy trên tiến trình QEMU sẽ xem RAM của QEMU như physical RAM.

![.](../src-image/w6_2.PNG)

Từ góc nhìn hệ thống , qemu là một tiến trình được chạy và lên lịch thông thường. Các máy ảo chạy trên một máy chủ thông qua các tiến trình QEMU không biết nhau và hệ điều hành máy chủ cũng không thể can thiệp sâu vào dữ liệu và các tiến trình bên trong máy ảo. Tiến trình QEMU đảm nhiệm hai nhiệm vụ chính là thực thi guest code và ảo hóa các thiết bị. Để thực hiện được các công việc này, qemu sẽ được xây dựng dựa trên một kiến trúc định hướng sự kiện kèm theo các luồng chạy song song.



### Source Code
* Địa chỉ source code QEMU:
```
https://github.com/qemu/qemu
```
Source code của QEMU có kích thước lớn, do cộng đồng đóng góp từ năm 2006 và có khoảng hơn 6000 file code. 

Các file quan trọng trong quá trình chạy QEMU bao gồm /vl.c, /cpus.c, /execall.c, /exec.c, /cpu-exec.c. Trong đó file vl.c chứa hàm main của QEMU. Hàm này chịu trách nhiệm khởi tạo tài nguyên cho máy ảo như kích thước RAM, số các CPU, số thiết bị,... 

QEMU thực hiện phỏng tạo các phần cứng ảo cho máy ảo. Các file source code đảm nhận nhiệm vụ này nằm trong thư mục /hw của source code.

Kế đến, thực hiện việc dịch động (Dynamic Translation) từ guest code sang host code, QEMU sử dụng Tiny Code Generator. Để thực hiện công việc, TCG cần nắm rõ kiến trúc tập lệnh của máy chủ (host) và máy ảo (target). Các source code phục vụ công việc này nằm trong các thư mục /target và /tcg. Trong đó /target/xxx là thư mục lưu source code phục vụ kiểu kiến trúc máy đích xxx . Ví dụ /target/i386 . Còn thư mục /tcg lưu trữ các file source của TCG và source code kiến trúc tập lệnh máy chủ. 


### Internal
Việc chạy một máy ảo bao gồm thực thi guest code, điều khiển bộ định thời, chạy các I/O, và phản hồi lại các lệnh giám sát hệ thống. Thực hiện tất cả điều này yêu cầu một kiến trúc phù hợp. Có hai kiến trúc phù hợp cho câc chương trình cần phản hồi sự kiện đến từ nhiều tài nguyên:

* Parallel Architecture: Chia công việc thành các tiến trình (processes) hoặc các luồng (threads) và thực thi song song.
* Event-driven Architecture: Phản hồi sự kiện bằng cách chạy một vòng lặp chính để nhận và xử lý sự kiện.

QEMU sử dụng kiến trúc hybrid bao gồm event-driven đi cùng các luồng. Điều này là hợp lý vì một vòng lặp sự kiện đơn không phù hợp với kiểu CPU đa lõi của máy chủ khi nó chỉ có một luồng thực thi đơn. Thêm vào đó, thi thoảng, sẽ đơn giản hơn nếu viết các luồng riêng cho việc thực thi các công việc riêng biệt hơn là tích hợp tất cả vào một kiến trúc event-driven. Tuy nhiên, lõi của QEMU là kiến trúc event-driven và phần lớn code thực thi theo kiểu kiến trúc đó.

![.](../src-image/w6_5.PNG)

#### Main Loop

Kiến trúc event-driven tập trung vào một vòng lặp sự kiện chính, tại đó, các sự kiện sẽ được điều hướng tới thủ tục giải quyết nó.

Vòng lặp chính của QEMU gọi là main_loop_wait().

Hàm main_loop_wait() này được khai báo trong source code tại
```
include/qemu/main-loop.h
utils/main-loop.c
```

Nhiệm vụ của main_loop_wait() bao gồm:

* Đợi các file descriptor chuyển trạng thái có thể đọc hoặc có thể ghi. Các file decriptor chiếm vai trò cốt yếu vì các file, các cổng và vô số các tài nguyên khác đều là các file descriptor. 
* Chạy các bộ định thời
* Chạy các Bottom-Half (BH)

Khi một file descriptor trở nên sẵn sàng, một bộ định thời hết hạn hoặc một BH được lên lịch chạy, vòng lặp sẽ khởi tạo một lời gọi để phản hồi lại sự kiện trên. Để thực hiện điều này, qemu sử dụng các loại system call như select(2), pool(2) hoặc epool(2).


Trong tài liệu Improve the QEMU Event Loop, Fam Zheng, KVM Forum 2015, hoạt động của main_loop_wait() được trình bày giản lược. Các sự kiện đến bao gồm 3 nhóm:

* các IOthread thông thường
* nhóm các dispatched fd events
  * aio: block I/O, ioeventfd
  * iohandler: net, nbd, audio, ui, vfio, ... 
  * slirp: -net user 
  * chardev
* nhóm non-fd services
  * timers
  * bottom halves
  
Vòng main_loop_wait() sẽ thực hiện lặp 3 công việc:

* Prepare: nạp các file descriptor cho system call poll
* Poll: Gọi system call poll
* Dispatch: Thực thi lệnh tương ứng cho file descriptor ready (phản hồi từ poll) hoặc timer-expired, BH 

![.](../src-image/w6_3.PNG)

Cụ thể, thông qua quá trình debug source code, các hàm được gọi lần lượt khi chạy máy ảo bao gồm

Lệnh khởi chạy máy ảo với file DOS.iso chứa hệ điều hành DOS

```
time qemu-system-x86_64 -cdrom DOS.iso
```

Các hàm được gọi

```

call main

  call mainloop time 1
         call main_loop_should_exit
         exit main_loop_should_exit return true 
  exit mainloop

  call mainloop time 2
         call main_loop_should_exit
         exit main_loop_should_exit return false


         call main_loop_wait time 1
                  call os_host_main_loop_wait
                  exit os_host_main_loop_wait
         exit main_loop_wait


         call main_loop_wait time 2
                  call os_host_main_loop_wait
                  exit os_host_main_loop_wait
         exit main_loop_wait
.
.
.


         call main_loop_wait time n
                  call os_host_main_loop_wait
                  exit os_host_main_loop_wait
         exit main_loop_wait

  exit mainloop
  
exit main

```

Mô hình vòng lặp main loop
![.]()

```c

main() /* file vl.c */
{

/* Khởi tạo các biến */
/* Đọc yêu cầu từ lệnh chạy máy ảo. Ví Dụ: qemu-system-x86_64 -cdrom DOS.iso -hda image.qcow2 */
/* Khởi tạo các thiết bị phần cứng ảo hóa gồm RAM, CPU, VGA, Accelerator, Timers, Bluetooth, 
*  USB, sound hardware,... */

mainloop(); 

/* Sau khi thoát khỏi vòng lặp main_loop, tiến hành làm sạch bộ nhớ trước khi đóng tiến trình QEMU */


}

mainloop() /* file vl.c */
{
/* Kiểm tra điều kiện dừng trước khi lặp vòng lặp tạo main_loop_wait*/
while (!main_loop_should_exit()) 
				{
        main_loop_wait(false);
    }

}

main_loop_should_exit() /* file vl.c */
{
/* Kiểm tra điều kiện dừng vòng lặp main_loop_wait()*/
/* Các lý do dừng vòng lặp
*
* Khởi chạy mainloop lần đầu khi đang cấu hình máy ảo preconfig_exit_requested = true
* Yêu cầu shutdown từ qemu_shutdown_requested()
*/

/* Thực thi các công việc khác khi nhận các request khác với điều kiện dừng*/
/*
* qemu_debug_requested()
* qemu_suspend_requested()
* qemu_reset_requested()
* qemu_wakeup_requested()
* qemu_powerdown_requested()
* qemu_vmstop_requested()
*
*/

}

main_loop_wait() /* file util/m.c */
{


}

```

### Accelerator : KVM




