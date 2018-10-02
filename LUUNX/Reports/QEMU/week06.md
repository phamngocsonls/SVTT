---------------
QEMU (viết tắt của Quick Emulator [ cần dẫn nguồn ]] là một trình giả lập mã nguồn mở và miễn phí thực hiện ảo hóa phần cứng .

QEMU là trình giám sát máy ảo được lưu trữ : nó mô phỏng bộ xử lý của máy thông qua dịch nhị phân động và cung cấp một bộ các mô hình phần cứng và thiết bị khác nhau cho máy, cho phép nó chạy nhiều hệ điều hành khách . Nó cũng có thể được sử dụng với KVM để chạy các máy ảo ở tốc độ gần như nguyên gốc (bằng cách tận dụng các phần mở rộng phần cứng như IntelVT ). QEMU cũng có thể làm mô phỏng cho các quy trình mức người dùng, cho phép các ứng dụng được biên dịch cho một kiến trúc để chạy trên một cấu trúc khác.

Chế độ hoạt động 
QEMU có nhiều chế độ hoạt động: [3]

Mô phỏng chế độ người dùng
Trong chế độ này, QEMU chạy các chương trình Linux hoặc Darwin / macOS đơn được biên dịch cho một tập lệnh khác . Các cuộc gọi hệ thống được chia nhỏ cho endianness và 32/64 bit không khớp. Biên dịch chéo nhanh và gỡ lỗi chéo là các mục tiêu chính cho mô phỏng chế độ người dùng.
Thi đua hệ thống
Trong chế độ này, QEMU mô phỏng một hệ thống máy tính đầy đủ, bao gồm cả các thiết bị ngoại vi . Nó có thể được sử dụng để cung cấp lưu trữ ảo của một số máy tính ảo trên một máy tính duy nhất. QEMU có thể khởi động nhiều hệ điều hành khách , bao gồm Linux , Solaris , Microsoft Windows , DOS và BSD ; [4] nó hỗ trợ mô phỏng một số tập lệnh, bao gồm x86 , MIPS , 32-bit ARMv7 , ARMv8 , PowerPC , SPARC , ETRAX CRIS và MicroBlaze .

QEMU có thể lưu và khôi phục trạng thái của máy ảo bằng tất cả các chương trình đang chạy. Các hệ điều hành khách không cần vá để chạy bên trong QEMU.

QEMU hỗ trợ mô phỏng các kiến trúc khác nhau, bao gồm:

Máy tính cá nhân IA-32 (x86)
máy tính x86-64
MIPS64 Release 6 [5] và các phiên bản trước đó
Sun SPARC của Sun4m
Sun SPARC của Sun4u
Ban phát triển ARM (Bộ tích hợp / CP và Đa năng / PB)
SH4 SHIX board
PowerPC ( PReP và Power Macintosh )
ETRAX CRIS
MicroBlaze
RISC-V
Máy ảo có thể giao tiếp với nhiều loại phần cứng máy chủ vật lý, bao gồm ổ đĩa cứng của người dùng, ổ đĩa CD-ROM, thẻ mạng, giao diện âm thanh và thiết bị USB. Các thiết bị USB có thể được mô phỏng hoàn toàn hoặc các thiết bị USB của máy chủ có thể được sử dụng, mặc dù điều này yêu cầu các đặc quyền của quản trị viên và không hoạt động với tất cả các thiết bị.

Hình ảnh đĩa ảo có thể được lưu trữ ở định dạng đặc biệt ( qcow hoặc qcow2 ) chỉ chiếm dung lượng đĩa mà hệ điều hành khách thực sự sử dụng. Bằng cách này, một đĩa 120 GB được mô phỏng có thể chỉ chiếm vài trăm megabyte trên máy chủ. Định dạng QCOW2 cũng cho phép tạo hình ảnh lớp phủ ghi lại sự khác biệt so với tệp hình ảnh cơ bản (chưa sửa đổi) khác. Điều này cung cấp khả năng hoàn nguyên nội dung của mô phỏng đĩa về trạng thái trước đó. Ví dụ: hình ảnh cơ sở có thể chứa cài đặt mới của hệ điều hành được biết là hoạt động và hình ảnh lớp phủ được sử dụng. Nếu hệ thống khách trở nên không sử dụng được (thông qua tấn công virus, phá hủy hệ thống ngẫu nhiên, vv), người dùng có thể xóa lớp phủ và tạo lại phiên bản hình ảnh đĩa được mô phỏng trước đó.

QEMU có thể mô phỏng các card mạng (của các mô hình khác nhau) chia sẻ kết nối của hệ thống máy chủ bằng cách thực hiện dịch địa chỉ mạng, cho phép khách sử dụng cùng một mạng với máy chủ. Các card mạng ảo cũng có thể kết nối với các card mạng của các trường hợp khác của QEMU hoặc tới các giao diện TAP cục bộ . Kết nối mạng cũng có thể đạt được bằng cách bắc cầu một giao diện TUN / TAP được QEMU sử dụng với giao diện Ethernet không ảo trên hệ điều hành chủ sử dụng các tính năng nối tiếp của hệ điều hành máy chủ.

QEMU tích hợp một số dịch vụ để cho phép các máy chủ và hệ thống khách liên lạc; ví dụ, một máy chủ SMB tích hợp và chuyển hướng cổng mạng (để cho phép các kết nối đến máy ảo). Nó cũng có thể khởi động hạt nhân Linux mà không có bộ nạp khởi động.

QEMU không phụ thuộc vào sự hiện diện của các phương thức đầu ra đồ họa trên hệ thống máy chủ. Thay vào đó, nó có thể cho phép một người truy cập vào màn hình của hệ điều hành khách thông qua một máy chủ VNC tích hợp . Nó cũng có thể sử dụng một dòng nối tiếp mô phỏng, không có bất kỳ màn hình nào, với các hệ điều hành thích hợp.

Mô phỏng nhiều CPU chạy SMP là có thể.

QEMU không yêu cầu quyền quản trị để chạy, trừ khi các mô-đun hạt nhân bổ sung để cải thiện tốc độ được sử dụng (như KQEMU ), hoặc khi một số chế độ mô hình kết nối mạng của nó được sử dụng.

Trình tạo mã nhỏ 
Tiny Code Generator (TCG) nhằm mục đích loại bỏ thiếu sót dựa vào một phiên bản GCC cụ thể hoặc bất kỳ trình biên dịch nào, thay vì kết hợp trình biên dịch (trình tạo mã) vào các nhiệm vụ khác do QEMU thực hiện tại thời gian chạy. Toàn bộ nhiệm vụ dịch thuật bao gồm hai phần: khối mã mục tiêu ( TB ) được viết lại trong các khung TCG - một loại ký pháp trung gian độc lập với máy, và sau đó ký hiệu này được biên dịch cho kiến ​​trúc của máy chủ bởi TCG. Vé tối ưu hóa tùy chọn được thực hiện giữa chúng.

TCG yêu cầu mã chuyên dụng được viết để hỗ trợ mọi kiến ​​trúc mà nó chạy trên đó. Nó cũng yêu cầu bản dịch lệnh mục tiêu được viết lại để tận dụng lợi thế của các ops TCG, thay vì các ops dyngen đã sử dụng trước đó .

Bắt đầu với phiên bản QEMU 0.10.0, TCG phát hành với bản phát hành ổn định QEMU. [6]

Accelerator 
KQEMU là một mô-đun hạt nhân Linux , cũng được viết bởi Fabrice Bellard , trong đó đáng chú ý thúc đẩy thi đua của khách x86 hoặc x86-64 trên các nền tảng có cùng kiến ​​trúc CPU. Điều này làm việc bằng cách chạy mã chế độ người dùng (và tùy chọn một số mã nhân) trực tiếp trên CPU của máy chủ, và bằng cách sử dụng bộ vi xử lý và mô phỏng ngoại vi chỉ cho chế độ lõi và mã chế độ thực . KQEMU có thể thực thi mã từ nhiều hệ điều hành khách ngay cả khi CPU chủ không hỗ trợ ảo hóa phần cứng hỗ trợ . KQEMU là ban đầu một nguồn đóng sản phẩm hoàn toàn miễn phí, nhưng bắt đầu từ phiên bản 1.3.0pre10, [7] đó làđược cấp phép theo Giấy phép Công cộng GNU . Các phiên bản QEMU bắt đầu với 0.12.0 (tính đến tháng 8 năm 2009 ) hỗ trợ bộ nhớ lớn khiến chúng không tương thích với KQEMU. [8] Các bản phát hành mới hơn của QEMU đã hoàn toàn loại bỏ hỗ trợ cho KQEMU.

QVM86 là một thay thế được cấp phép GNU GPLv2 được cấp phép cho KQEMU nguồn đóng sau đó. Các nhà phát triển QVM86 đã ngừng phát triển vào tháng 1 năm 2007.

Máy ảo dựa trên hạt nhân ( KVM ) chủ yếu được dùng làm giải pháp ảo hóa phần cứng dựa trên Linux để sử dụng với QEMU sau sự thiếu hỗ trợ cho KQEMU và QVM86. [ cần dẫn nguồn ]

Trình quản lý thực thi tăng tốc phần cứng của Intel ( HAXM ) là một giải pháp thay thế mã nguồn mở [9] cho KVM cho ảo hóa dựa trên phần cứng dựa trên x86 trên Windows và macOS. Tính đến năm 2013, Intel chủ yếu sử dụng QEMU để phát triển Android. [10] Bắt đầu với phiên bản 2.9.0, QEMU chính thức bao gồm hỗ trợ cho HAXM.

-----------------------------------------

QEMU Internals: Big picture overview
Last week I started the QEMU Internals series to share knowledge of how QEMU works. I dove straight in to the threading model without a high-level overview. I want to go back and provide the big picture so that the details of the threading model can be understood more easily.

The story of a guest

A guest is created by running the qemu program, also known as qemu-kvm or just kvm. On a host that is running 3 virtual machines there are 3 qemu processes:

When a guest shuts down the qemu process exits. Reboot can be performed without restarting the qemu process for convenience although it would be fine to shut down and then start qemu again.

Guest RAM

Guest RAM is simply allocated when qemu starts up. It is possible to pass in file-backed memory with -mem-path such that hugetlbfs can be used. Either way, the RAM is mapped in to the qemu process' address space and acts as the "physical" memory as seen by the guest:


QEMU supports both big-endian and little-endian target architectures so guest memory needs to be accessed with care from QEMU code. Endian conversion is performed by helper functions instead of accessing guest RAM directly. This makes it possible to run a target with a different endianness from the host.

KVM virtualization

KVM is a virtualization feature in the Linux kernel that lets a program like qemu safely execute guest code directly on the host CPU. This is only possible when the target architecture is supported by the host CPU. Today KVM is available on x86, ARMv8, ppc, s390, and MIPS CPUs.

In order to execute guest code using KVM, the qemu process opens /dev/kvm and issues the KVM_RUN ioctl. The KVM kernel module uses hardware virtualization extensions found on modern Intel and AMD CPUs to directly execute guest code. When the guest accesses a hardware device register, halts the guest CPU, or performs other special operations, KVM exits back to qemu. At that point qemu can emulate the desired outcome of the operation or simply wait for the next guest interrupt in the case of a halted guest CPU.

The basic flow of a guest CPU is as follows:
open("/dev/kvm")
ioctl(KVM_CREATE_VM)
ioctl(KVM_CREATE_VCPU)
for (;;) {
     ioctl(KVM_RUN)
     switch (exit_reason) {
     case KVM_EXIT_IO:  /* ... */
     case KVM_EXIT_HLT: /* ... */
     }
}

The host's view of a running guest

The host kernel schedules qemu like a regular process. Multiple guests run alongside without knowledge of each other. Applications like Firefox or Apache also compete for the same host resources as qemu although resource controls can be used to isolate and prioritize qemu.

Since qemu system emulation provides a full virtual machine inside the qemu userspace process, the details of what processes are running inside the guest are not directly visible from the host. One way of understanding this is that qemu provides a slab of guest RAM, the ability to execute guest code, and emulated hardware devices; therefore any operating system (or no operating system at all) can run inside the guest. There is no ability for the host to peek inside an arbitrary guest.

Guests have a so-called vcpu thread per virtual CPU. A dedicated iothread runs a select(2) event loop to process I/O such as network packets and disk I/O completion. For more details and possible alternate configuration, see the threading model post.

The following diagram illustrates the qemu process as seen from the host:


------------------------

QEMU Internals: Overall architecture and threading model
This is the first post in a series on QEMU Internals aimed at developers. It is designed to share knowledge of how QEMU works and make it easier for new contributors to learn about the QEMU codebase.

Running a guest involves executing guest code, handling timers, processing I/O, and responding to monitor commands. Doing all these things at once requires an architecture capable of mediating resources in a safe way without pausing guest execution if a disk I/O or monitor command takes a long time to complete. There are two popular architectures for programs that need to respond to events from multiple sources:
Parallel architecture splits work into processes or threads that can execute simultaneously. I will call this threaded architecture.
Event-driven architecture reacts to events by running a main loop that dispatches to event handlers. This is commonly implemented using the select(2) or poll(2) family of system calls to wait on multiple file descriptors.

QEMU actually uses a hybrid architecture that combines event-driven programming with threads. It makes sense to do this because an event loop cannot take advantage of multiple cores since it only has a single thread of execution. In addition, sometimes it is simpler to write a dedicated thread to offload one specific task rather than integrate it into an event-driven architecture. Nevertheless, the core of QEMU is event-driven and most code executes in that environment.

The event-driven core of QEMU

An event-driven architecture is centered around the event loop which dispatches events to handler functions. QEMU's main event loop is main_loop_wait() and it performs the following tasks:

Waits for file descriptors to become readable or writable. File descriptors play a critical role because files, sockets, pipes, and various other resources are all file descriptors. File descriptors can be added using qemu_set_fd_handler().
Runs expired timers. Timers can be added using qemu_mod_timer().
Runs bottom-halves (BHs), which are like timers that expire immediately. BHs are used to avoid reentrancy and overflowing the call stack. BHs can be added using qemu_bh_schedule().

When a file descriptor becomes ready, a timer expires, or a BH is scheduled, the event loop invokes a callback that responds to the event. Callbacks have two simple rules about their environment:
No other core code is executing at the same time so synchronization is not necessary. Callbacks execute sequentially and atomically with respect to other core code. There is only one thread of control executing core code at any given time.
No blocking system calls or long-running computations should be performed. Since the event loop waits for the callback to return before continuing with other events, it is important to avoid spending an unbounded amount of time in a callback. Breaking this rule causes the guest to pause and the monitor to become unresponsive.

This second rule is sometimes hard to honor and there is code in QEMU which blocks. In fact there is even a nested event loop in qemu_aio_wait() that waits on a subset of the events that the top-level event loop handles. Hopefully these violations will be removed in the future by restructuring the code. New code almost never has a legitimate reason to block and one solution is to use dedicated worker threads to offload long-running or blocking code.

Offloading specific tasks to worker threads

Although many I/O operations can be performed in a non-blocking fashion, there are system calls which have no non-blocking equivalent. Furthermore, sometimes long-running computations simply hog the CPU and are difficult to break up into callbacks. In these cases dedicated worker threads can be used to carefully move these tasks out of core QEMU.

One example user of worker threads is posix-aio-compat.c, an asynchronous file I/O implementation. When core QEMU issues an aio request it is placed on a queue. Worker threads take requests off the queue and execute them outside of core QEMU. They may perform blocking operations since they execute in their own threads and do not block the rest of QEMU. The implementation takes care to perform necessary synchronization and communication between worker threads and core QEMU.

Another example is ui/vnc-jobs-async.c which performs compute-intensive image compression and encoding in worker threads.

Since the majority of core QEMU code is not thread-safe, worker threads cannot call into core QEMU code. Simple utilities like qemu_malloc() are thread-safe but that is the exception rather than the rule. This poses a problem for communicating worker thread events back to core QEMU.

When a worker thread needs to notify core QEMU, a pipe or a qemu_eventfd() file descriptor is added to the event loop. The worker thread can write to the file descriptor and the callback will be invoked by the event loop when the file descriptor becomes readable. In addition, a signal must be used to ensure that the event loop is able to run under all circumstances. This approach is used by posix-aio-compat.c and makes more sense (especially the use of signals) after understanding how guest code is executed.

Executing guest code

So far we have mainly looked at the event loop and its central role in QEMU. Equally as important is the ability to execute guest code, without which QEMU could respond to events but would not be very useful.

There are two mechanism for executing guest code: Tiny Code Generator (TCG) and KVM. TCG emulates the guest using dynamic binary translation, also known as Just-in-Time (JIT) compilation. KVM takes advantage of hardware virtualization extensions present in modern Intel and AMD CPUs for safely executing guest code directly on the host CPU. For the purposes of this post the actual techniques do not matter but what matters is that both TCG and KVM allow us to jump into guest code and execute it.

Jumping into guest code takes away our control of execution and gives control to the guest. While a thread is running guest code it cannot simultaneously be in the event loop because the guest has (safe) control of the CPU. Typically the amount of time spent in guest code is limited because reads and writes to emulated device registers and other exceptions cause us to leave the guest and give control back to QEMU. In extreme cases a guest can spend an unbounded amount of time without giving up control and this would make QEMU unresponsive.

In order to solve the problem of guest code hogging QEMU's thread of control signals are used to break out of the guest. A UNIX signal yanks control away from the current flow of execution and invokes a signal handler function. This allows QEMU to take steps to leave guest code and return to its main loop where the event loop can get a chance to process pending events.

The upshot of this is that new events may not be detected immediately if QEMU is currently in guest code. Most of the time QEMU eventually gets around to processing events but this additional latency is a performance problem in itself. For this reason timers, I/O completion, and notifications from worker threads to core QEMU use signals to ensure that the event loop will be run immediately.

You might be wondering what the overall picture between the event loop and an SMP guest with multiple vcpus looks like. Now that the threading model and guest code has been covered we can discuss the overall architecture.

iothread and non-iothread architecture

The traditional architecture is a single QEMU thread that executes guest code and the event loop. This model is also known as non-iothread or !CONFIG_IOTHREAD and is the default when QEMU is built with ./configure && make. The QEMU thread executes guest code until an exception or signal yields back control. Then it runs one iteration of the event loop without blocking in select(2). Afterwards it dives back into guest code and repeats until QEMU is shut down.

If the guest is started with multiple vcpus using -smp 2, for example, no additional QEMU threads will be created. Instead the single QEMU thread multiplexes between two vcpus executing guest code and the event loop. Therefore non-iothread fails to exploit multicore hosts and can result in poor performance for SMP guests.

Note that despite there being only one QEMU thread there may be zero or more worker threads. These threads may be temporarily or permanent. Remember that they perform specialized tasks and do not execute guest code or process events. I wanted to emphasise this because it is easy to be confused by worker threads when monitoring the host and interpret them as vcpu threads. Remember that non-iothread only ever has one QEMU thread.

The newer architecture is one QEMU thread per vcpu plus a dedicated event loop thread. This model is known as iothread or CONFIG_IOTHREAD and can be enabled with ./configure --enable-io-thread at build time. Each vcpu thread can execute guest code in parallel, offering true SMP support, while the iothread runs the event loop. The rule that core QEMU code never runs simultaneously is maintained through a global mutex that synchronizes core QEMU code across the vcpus and iothread. Most of the time vcpus will be executing guest code and do not need to hold the global mutex. Most of the time the iothread is blocked in select(2) and does not need to hold the global mutex.

Note that TCG is not thread-safe so even under the iothread model it multiplexes vcpus across a single QEMU thread. Only KVM can take advantage of per-vcpu threads.

Conclusion and words about the future
Hopefully this helps communicate the overall architecture of QEMU (which KVM inherits). Feel free to leave questions in the comments below.

In the future the details are likely to change and I hope we will see a move to CONFIG_IOTHREAD by default and maybe even a removal of !CONFIG_IOTHREAD.
---------------------------------



