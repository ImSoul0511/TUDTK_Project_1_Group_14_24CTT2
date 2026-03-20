# Hướng dẫn cài đặt môi trường (Environment Setup Guide)

Dưới đây là các bước để cài đặt và kích hoạt môi trường ảo cho project. Các bạn làm theo các lệnh dưới đây trên terminal để thiết lập môi trường làm việc nhé:

### 1. Kiểm tra phiên bản Python
Đảm bảo máy tính của bạn đã được cài đặt Python. Để kiểm tra, chạy lệnh sau:
```bash
py --version
```

### 2. Tạo môi trường ảo (Virtual Environment)
Tại thư mục gốc của dự án, chạy lệnh sau để tạo một môi trường ảo có tên là `venv`:
```bash
py -m venv venv
```

### 3. Kích hoạt môi trường ảo
Sau khi tạo xong, bạn cần kích hoạt môi trường ảo. Việc này giúp các thư viện dự án được cài đặt biệt lập, không ảnh hưởng đến hệ thống máy tính.
```bash
.\venv\Scripts\activate
```
*(Nếu kích hoạt thành công, bạn sẽ thấy chữ `(venv)` hiển thị ở đầu dòng lệnh của terminal).*

### 4. Cài đặt các thư viện (Dependencies)
Cuối cùng, tiến hành cài đặt tất cả các thư viện/gói cần thiết cho project đã được liệt kê sẵn trong file `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

> **Lưu ý quan trọng**: Lệnh tạo môi trường ảo và cài đặt thư viện (bước 2 và bước 4) chỉ cần chạy **một lần duy nhất** khi clone source code về. Tuy nhiên, ở các lần làm việc tiếp theo hoặc mỗi khi bạn mở một terminal mới, bạn **LUÔN PHẢI** kích hoạt lại môi trường ảo bằng lệnh ở bước 3 (`.\venv\Scripts\activate`).
