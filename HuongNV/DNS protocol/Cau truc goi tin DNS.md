# Cấu trúc gói tin DNS

`ID QR Opcode AA TC RD RA Z Rcode`
`QDcount ANcount NScount ARcount`

**ID**: Là một trường 16 bits, chứa mã nhận dạng, nó được tạo ra bởi một chương trình để thay cho truy vấn. Gói tin hồi đáp sẽ dựa vào mã nhận dạng này để hồi đáp lại. Chính vì vậy mà truy vấn và hồi đáp có thể phù hợp với nhau.

**QR**: Là một trường 1 bit. Bít này sẽ được thiết lập là 0 nếu là gói tin truy vấn, được thiết lập là một nếu là gói tin hồi đáp.

**Opcode**: Là một trường 4 bits, được thiết lập là 0 cho cờ hiệu truy vấn, được thiết lập là 1 cho truy vấn ngược, và được thiết lập là 2 cho tình trạng truy vấn.

**AA**: Là trường 1 bit, nếu gói tin hồi đáp được thiết lập là 1, sau đó nó sẽ đi đến một server có thẫm quyền giải quyết truy vấn.

**TC**: Là trường 1 bit, trường này sẽ cho biết là gói tin có bị cắt khúc ra do kích thước gói tin vượt quá băng thông cho phép hay không.

**RD**: Là trường 1 bit, trường này sẽ cho biết là truy vấn muốn server tiếp tục truy vấn một cách đệ qui.

**RA**: Trường 1 bit này sẽ cho biết truy vấn đệ qui có được thực thi trên server không .

**Z**: Là trường 1 bit. Đây là một trường dự trữ, và được thiết lập là 0.

**Rcode**: Là trường 4 bits, gói tin hồi đáp sẽ có thể nhận các giá trị sau :

- 0: Cho biết là không có lỗi trong quá trình truy vấn.
- 1: Cho biết định dạng gói tin bị lỗi, server không hiểu được truy vấn.
- 2: Server bị trục trặc, không thực hiện hồi đáp được.
- 3: Tên bị lỗi. Chỉ có server có đủ thẩm quyền mới có thể thiết lập giá trị náy.
- 4: Không thi hành. Server không thể thực hiện chức năng này .
- 5: Server từ chồi thực thi truy vấn.

**QDcount**: Số lần truy vấn của gói tin trong một vấn đề.

**ANcount**: Số lượng tài nguyên tham gia trong phần trả lời.

**NScount**: Chỉ ra số lượng tài nguyên được ghi lại trong các phẩn có thẩm quyền của gói tin.

**ARcount**: Chỉ ra số lượng tài nguyên ghi lại trong phần thêm vào của gói tin.