# Đồ án 1: Toán ứng dụng và thống kê

> **Môn học:** Toán ứng dụng và thống kê (Applied Mathematics and Statistics)  
> **GVHD:** ThS. Lê Nhựt Nam, ThS. Võ Nam Thục Đoan   
> **Nhóm thực hiện:** Nhóm 14 (24CTT2)

## **Mục lục**

1. **[Tổng quan dự án](#tổng-quan-dự-án)**
2. **[Cấu trúc thư mục](#cấu-trúc-thư-mục)**
3. **[Cơ sở lý thuyết](#cơ-sở-lý-thuyết)**
4. **[Chi tiết các phần thực hiện](#chi-tiết-các-phần-thực-hiện)**
    - [Phần 1: Nền tảng Đại số](#phần-1-nền-tảng-đại-số)
    - [Phần 2: Chéo hóa & Phân rã SVD](#phần-2-chéo-hóa--phân-rã-svd)
    - [Phần 3: Benchmark & Phân tích ổn định](#phần-3-benchmark--phân-tích-ổn-định)
5. **[Thư viện đã dùng](#thư-viện-đã-dùng)**
6. **[File config.py](#file-configpy)**
7. **[Hướng dẫn cài đặt môi trường](#hướng-dẫn-cài-đặt-môi-trường)**
8. **[Cách chạy thử nghiệm](#cách-chạy-thử-nghiệm)**
9. **[Tác giả & Đóng góp](#tác-giả--đóng-góp)**

---

## **Tổng quan dự án**

Dự án này là **Đồ án môn Toán Ứng Dụng và Thống Kê (FIT-HCMUS)**, tập trung vào việc lập trình từ đầu (*from scratch*) các thuật toán cốt lõi của đại số tuyến tính số bằng Python mà không sử dụng các hàm giải toán có sẵn từ các thư viện như NumPy hay SciPy.

Dự án xoay quanh 3 mục tiêu chính:
- **Phép khử Gauss và Ứng dụng:** Cài đặt phép khử Gauss có chọn phần tử chốt (Partial Pivoting) để giải hệ phương trình tuyến tính, tính định thức, tìm ma trận nghịch đảo, hạng và cơ sở của ma trận.
- **Phân rã ma trận & Trực quan hóa:** Triển khai thuật toán chéo hóa và một kỹ thuật phân rã ma trận (nhóm chọn LU, QR, SVD, hoặc Cholesky). Sử dụng thư viện Manim để lập trình video trực quan hóa ý nghĩa hình học của quá trình phân rã này.
- **Phân tích hiệu năng & Ổn định số học:** Thực nghiệm đo lường thời gian chạy (Đồ thị Log-Log) và đánh giá tính ổn định số học (Condition Number) của các thuật toán trực tiếp so với phương pháp lặp (Gauss-Seidel) khi đối mặt với ma trận nhiễu như ma trận Hilbert.

---

## **Cấu trúc thư mục**

```text
Singular-Value-Decomposition/
├── part1/                          # Phép khử Gauss & Nền tảng
│   ├── __init__.py                 # Khai báo package Part 1
│   ├── gaussian.py                 # Thuật toán khử Gauss & Thế ngược
│   ├── determinant.py              # Thuật toán tính định thức (det)
│   ├── inverse.py                  # Thuật toán tìm ma trận nghịch đảo
│   ├── rank_basis.py               # Tính hạng & các không gian con
│   ├── verification.py             # Hệ thống kiểm chứng (NumPy)
│   ├── test_case.py                # Dữ liệu kiểm thử mẫu
│   └── part1_demo.ipynb            # Notebook trình diễn Part 1
├── part2/                          # Chéo hóa & SVD
│   ├── __init__.py                 # Khai báo package Part 2
│   ├── decomposition.py            # Cài đặt SVD Scratch
│   ├── diagonalization.py          # Thuật toán Jacobi & QR
│   ├── verification_part2.py       # Kiểm chứng Part 2 bằng NumPy
│   ├── test_case_part2.py          # Dữ liệu kiểm thử Part 2
│   ├── utils.py                    # Tiện ích toán học cho Part 2
│   ├── manim_scene_1.py            # Cảnh 1: Thuật toán chéo hóa và trực quan hóa 
│   ├── manim_scene_2.py            # Cảnh 2: Ma trận Sigma trong SVD
│   ├── manim_scene_3.py            # Cảnh 3: Ma trận U và V^T trong SVD
│   ├── manim_scene_4.py            # Cảnh 4: Thuật toán SVD và trực quan hóa
│   ├── manim_scene_5.py            # Cảnh 5: Ứng dụng nén ảnh của SVD
│   ├── data.json                   # Dữ liệu cấu hình phụ cho Manim
│   └── movie.py                    # Script ghép nối video Manim
├── part3/                          # Benchmark & Thực nghiệm
│   ├── __init__.py                 # Khai báo package Part 3
│   ├── benchmark.py                # Thực nghiệm hiệu năng & ổn định
│   ├── solvers.py                  # Gauss-Seidel & Solver router
│   ├── generate_data.py            # Sinh dữ liệu Hilbert & SPD
│   ├── utils.py                    # Tính sai số chuẩn L2
│   ├── analysis.ipynb              # Phân tích thực nghiệm & Đồ thị
│   └── benchmark_results.json      # Lưu trữ dữ liệu thực nghiệm thô
├── report/                         # Thư mục báo cáo (Typst)
│   ├── report.pdf                  # File báo cáo PDF chính thức
│   ├── report.typ                  # File nguồn Typst
│   └── assets/                     # Thư mục chứa hình ảnh minh họa
├── config.py                       # Cấu hình hệ thống (EPSILON, Logger)
├── requirements.txt                # Danh sách thư viện dự án
└── README.md                       # Hướng dẫn dự án
```


---

## **Cơ sở lý thuyết**

### **1. Phép khử Gauss (Gaussian Elimination)**
Phương pháp biến đổi ma trận $A$ về dạng tam giác trên (upper triangular) thông qua các phép biến đổi sơ cấp trên dòng. Dự án sử dụng chiến lược **Partial Pivoting** để hạn chế sai số dấu phẩy động bằng cách hoán đổi dòng để đưa phần tử có trị tuyệt đối lớn nhất lên làm chốt (pivot).

### **2. Phân rã SVD**
Mọi ma trận $A \in \mathbb{R}^{m \times n}$ đều có thể phân rã thành:
$$ A = U \Sigma V^T $$
Trong đó $U$ và $V$ là các ma trận trực giao, $\Sigma$ là ma trận đường chéo chứa các giá trị kỳ dị (singular values) giảm dần. SVD là công cụ mạnh mẽ nhất để giải quyết các hệ phương trình tuyến tính cực kỳ bất ổn định mà phương pháp Gauss thường thất bại.

### **3. Phương pháp lặp Gauss-Seidel**
Một thuật toán lặp để giải hệ phương trình tuyến tính $Ax = b$. Thuật toán hội tụ nhanh nếu ma trận hệ số $A$ có tính **chéo trội chặt hàng** (strictly diagonally dominant) hoặc ma trận đối xứng xác định dương (SPD).

### **4. Số điều kiện (Condition Number)**
Số điều kiện $\kappa(A)$ của một ma trận đo lường mức độ nhạy cảm của nghiệm hệ phương trình tuyến tính đối với các nhiễu/sai số trong dữ liệu đầu vào. Với chuẩn $L_2$, số điều kiện được tính bằng tỉ số giữa giá trị kỳ dị lớn nhất và nhỏ nhất:
$$ \kappa_2(A) = \frac{\sigma_{max}}{\sigma_{min}} $$
Ma trận có số điều kiện lớn được gọi là **ma trận kém điều kiện (ill-conditioned)**.

### **5. Tính ổn định số học (Numerical Stability)**
Tính ổn định số học phản ánh khả năng của thuật toán duy trì độ chính xác khi đối mặt với sai số làm tròn (round-off error) trong tính toán dấu phẩy động. Đồ án tập trung chứng minh tính ổn định vượt trội của SVD so với phép khử Gauss khi xử lý các ma trận có số điều kiện lớn như ma trận Hilbert.

---

## **Chi tiết các phần thực hiện**

### **Phần 1: Nền tảng Đại số**
Tập trung vào các thuật toán biến đổi dòng cơ bản và hệ thống kiểm chứng kết quả.

| **Module** | **Hàm chính** | **Mô tả** |
| :--- | :--- | :--- |
| `gaussian.py` | `gaussian_eliminate`, `back_substitution` | Khử Gauss và thế ngược để giải hệ $Ax=b$. |
| `determinant.py` | `determinant(A)` | Tính định thức ma trận vuông. |
| `inverse.py` | `inverse(A)` | Tìm ma trận nghịch đảo $A^{-1}$ bằng Gauss-Jordan. |
| `rank_basis.py` | `rank_and_basis(A)` | Xác định hạng và các không gian con. |
| `verification.py` | `verify_solution`, `verify_determinant_numpy`, `verify_inverse_numpy`, `verify_rank_and_basis_numpy` | Dùng NumPy để xác minh tính đúng đắn của giải thuật Scratch (Ax=b, Det, Inverse, Rank/Basis). |
| `test_case.py` | `GAUSSIAN_ELIMINATE_TEST_CASES`, v.v. | Danh sách các bộ dữ liệu mẫu (Ma trận suy biến, Chéo trội, Hilbert...) dùng cho kiểm thử. |

**Xử lý các trường hợp đặc biệt:**
- **Hệ vô nghiệm:** Tự động phát hiện khi xuất hiện dòng có vế trái toàn zero nhưng vế phải khác zero.
- **Hệ vô số nghiệm:** Tìm nghiệm riêng $x_p$ và cơ sở không gian nghiệm (null basis) để biểu diễn nghiệm tổng quát dưới dạng $x = x_p + c_1 v_1 + ... + c_k v_k$.
- **Ma trận hình chữ nhật ($m \neq n$):** Thuật toán khử Gauss vẫn hoạt động bình thường, hỗ trợ tính toán cho các hệ phương trình thừa ẩn hoặc thiếu phương trình.
- **Chọn chốt (Partial Pivoting):** Luôn chọn phần tử có trị tuyệt đối lớn nhất làm chốt để tránh chia cho 0 và giảm thiểu sai số làm tròn.

### **Phần 2: Chéo hóa & Phân rã SVD**
Triển khai các phương pháp tìm trị riêng và giá trị kỳ dị.

| **Module** | **Hàm chính** | **Mô tả** |
| :--- | :--- | :--- |
| `diagonalization.py` | `diagonalize` | Tìm toàn bộ trị riêng bằng phương pháp Jacobi (đối xứng) hoặc QR Iteration (tổng quát). |
| `decomposition.py` | `svd(A)` | Toàn bộ tiến trình phân rã SVD (A = UΣVᵀ) từ trị riêng của $A^TA$. |
| `verification_part2.py` | `verify_svd_numpy`, `verify_diagonalize_numpy` | Kiểm chứng kết quả thuật toán phân rã với NumPy. |
| `test_case_part2.py` | `SVD_TEST_CASES`, `DIAGONALIZATION_TEST_CASES` | Các bộ dữ liệu mẫu dùng để kiểm thử phần 2. |
| `utils.py` | `matrix_multiply`, `vector_normalize`, v.v. | Thư viện hỗ trợ tính toán ma trận, tích vô hướng và trực giao hóa Gram-Schmidt. |
| `manim_scene_1.py` | `Scene` | Cảnh 1: Giải phẫu sự hỗn loạn (Anatomy of Chaos). |
| `manim_scene_2.py` | `Scene2`, `Scene2_3D` | Cảnh 2: Trực quan hóa hình học 2D/3D & ma trận Sigma. |
| `manim_scene_3.py` | `Scene3`, `Rotation` | Cảnh 3: Thuật toán và Toán học phía sau SVD. |
| `manim_scene_4.py` | `Scene4_SVD` | Cảnh 4: So sánh SVD vs Chéo hóa (Diagonalization). |
| `data.json` | `JSON` | File chứa một số tham số cấu hình tĩnh cho Manim. |
| `movie.py` | `concatenate_videoclips` | Script hậu kỳ ghép nối các cảnh quay thành video demo hoàn chỉnh. |

**Chi tiết giải thuật Phân rã:**
- **Jacobi Method:** Thực hiện các phép quay Givens liên tiếp để triệt tiêu các phần tử ngoại biên, đưa ma trận đối xứng về dạng đường chéo.
- **QR Algorithm:** Sử dụng phân rã Householder QR liên tiếp cho đến khi ma trận hội tụ về dạng tam giác trên chứa các trị riêng.
- **SVD Construction:** Tính ma trận $V$ từ vector riêng của $A^TA$, trích xuất giá trị kỳ dị $\sigma$ từ căn bậc hai của trị riêng, và xác định $U$ thông qua mối liên hệ $u_i = Av_i / \sigma_i$.

### **Phần 3: Benchmark & Phân tích ổn định**
Đánh giá sức mạnh của thuật toán trên các hệ thống thực tế.

| **Module** | **Hàm chính** | **Mô tả** |
| :--- | :--- | :--- |
| `solvers.py` | `solve_system`, `gauss_seidel_iteration` | Bộ điều hướng giải hệ phương trình và cài đặt phương pháp lặp Gauss-Seidel. |
| `benchmark.py` | `measure_execution_time`, `measure_condition_stability` | Đo lường hiệu năng (O(n³)) và so sánh sai số ổn định trên ma trận Hilbert. |
| `generate_data.py` | `generate_hilbert_matrix`, `generate_spd_matrix` | Sinh dữ liệu ma trận kém điều kiện (Hilbert) và ma trận ổn định (SPD). |
| `utils.py` | `compute_l2_error` | Tính toán sai số tương đối chuẩn L2 phục vụ đánh giá độ chính xác. |
| `analysis.ipynb` | `Visualization` | Phân tích dữ liệu, vẽ đồ thị Log-Log và chứng minh Định lý 3.1. |
| `benchmark_results.json` | `Metric Storage` | Lưu trữ kết quả thực nghiệm thô để phục vụ phân tích. |

**Mô tả thực nghiệm Benchmark:**
- **Execution Metrics:** So sánh thời gian thực thi của 3 phương pháp (Gauss, SVD, Gauss-Seidel) trên dải kích thước $n$ từ 50 đến 1000. Kết quả được biểu diễn qua đồ thị Log-Log để xác định hệ số góc thực tế.
- **Stability Test (Định lý 3.1):** Kiểm chứng sự sụp đổ của phương pháp giải trực tiếp (Gauss) khi số điều kiện $\kappa(A)$ tăng theo hàm mũ (ma trận Hilbert). SVD cho thấy khả năng "sinh tồn" tốt hơn nhờ việc xử lý trực tiếp các giá trị kỳ dị nhỏ.
- **Convergence Analysis:** Đánh giá điều kiện chéo trội và tính xác định dương của ma trận ảnh hưởng đến tốc độ hội tụ của phương pháp lặp.

---

## **Thư viện đã dùng**

Hệ thống sử dụng các thư viện bổ trợ cho việc vẽ đồ thị, trực quan hóa và kiểm chứng:
- **Xác minh & Toán học**: `numpy`, `scipy`, `sympy`
- **Video & Trực quan**: `manim`, `pycairo`
- **Phân tích dữ liệu**: `matplotlib`, `pandas`
- **Notebook & Trình bày**: `ipykernel`, `jinja2`

---

## **File config.py**

File cấu hình hệ thống đóng vai trò thiết lập các thông số kỹ thuật chung cho toàn bộ dự án:

- **Sai số EPSILON ($10^{-15}$):** Ngưỡng sai số dùng để nhận diện các giá trị gần bằng 0, giúp xử lý các bài toán dấu phẩy động chính xác hơn.
- **Tiện ích xử lý số thực:** Cung cấp các hàm `is_zero` và `make_zero` để chuẩn hóa dữ liệu sau tính toán.
- **AutoTestReporter:** Một lớp tiện ích hỗ trợ định dạng kết quả kiểm thử ra Terminal (màu sắc ANSI, bảng tổng kết), giúp quá trình chấm bài và gỡ lỗi (debug) trực quan hơn.

---

## **Hướng dẫn cài đặt môi trường**

Để đảm bảo các thư viện được cài đặt biệt lập và không xung đột với hệ thống, vui lòng thực hiện các bước sau:

### **1. Tạo môi trường ảo (Virtual Environment)**
Chạy lệnh sau tại thư mục gốc của dự án để tạo thư mục `venv`:
```bash
python -m venv venv
```

### **2. Kích hoạt môi trường ảo**
Việc kích hoạt giúp máy tính nhận diện và sử dụng các thư viện trong môi trường ảo.
- **Windows:**
  ```bash
  .\venv\Scripts\activate
  ```
- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

### **3. Cài đặt các thư viện cần thiết**
Tiến hành cài đặt danh sách các thư viện (NumPy, Manim, Matplotlib...) từ file `requirements.txt`:
```bash
pip install -r requirements.txt
```

> **Lưu ý quan trọng:** Bạn chỉ cần thực hiện bước 1 và 3 trong lần đầu tiên tải dự án về. Tuy nhiên, mỗi khi mở một Terminal mới để làm việc, bạn **bắt buộc phải thực hiện bước 2** để kích hoạt lại môi trường ảo.

---


## **Cách chạy thử nghiệm**

Để kiểm chứng và chạy thử nghiệm các thành phần của dự án, bạn có thể chạy các script Python và Jupyter Notebook tương ứng cho từng phần. Đảm bảo bạn đã **kích hoạt môi trường ảo** (như hướng dẫn ở trên) trước khi chạy bất kỳ lệnh nào.

### **Phần 1: Nền tảng Đại số**
Mỗi thuật toán đều được tích hợp sẵn các bộ Test Case (lấy từ `part1/test_case.py`). Bạn có thể chạy kiểm thử từng module riêng lẻ:
```bash
python part1/gaussian.py
python part1/determinant.py
python part1/inverse.py
python part1/rank_basis.py
```
Hoặc mở file `part1/part1_demo.ipynb` bằng Jupyter Notebook/VSCode để xem phần trình diễn từng bước.

### **Phần 2: Chéo hóa & Phân rã SVD (Trực quan hóa Manim)**
**1. Kiểm thử thuật toán phân rã:**
Tương tự Phần 1, bạn có thể chạy kiểm thử các thuật toán phân rã và tìm trị riêng trực tiếp:
```bash
python part2/diagonalization.py
python part2/decomposition.py
```

**2. Video Manim:**
Link video:
```

```

### **Phần 3: Benchmark & Phân tích ổn định**
Để chạy tập dữ liệu thực nghiệm đo lường hiệu năng (thời gian chạy) và độ ổn định:
```bash
python part3/benchmark.py
```
Kết quả thực nghiệm thô sẽ được tự động lưu vào file `part3/benchmark_results.json`.

Sau đó, hãy mở file Jupyter Notebook `part3/analysis.ipynb` để xem đồ thị phân tích chi tiết:
- Đồ thị Log-Log về tốc độ thực thi O(n³).
- Đồ thị so sánh độ chính xác giải hệ phương trình khi số điều kiện (Condition Number) tăng cao trên ma trận nhiễu.

---

## **Tác giả & Đóng góp**

| **MSSV** | **Họ và Tên** | **GitHub** |
| :--- | :--- | :--- |
| 24120394 | Nguyễn Đặng Khôi Nguyên | [@ImSoul0511](https://github.com/ImSoul0511) |
| 24120331 | Lê Quốc Khải | [@QuocKhai](https://github.com/QuocKhai1004) |
| 24120384 | Phan Nhật Minh | [@MintFan1607](https://github.com/MintFan1607) |
| 24120370 | Trần Thị Lợi | [@Lowen-here](https://github.com/Lowen-here) |
| 24120474 | Trịnh Vỹ Triết | [@TrinhVyTriet](https://github.com/TrinhVyTriet) |

---

*Dự án được thực hiện trong khuôn khổ môn học, năm học 2025–2026.*
