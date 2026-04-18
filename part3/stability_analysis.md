## 1. Bảng số liệu thực nghiệm:
### a. Ma trận Hilbert
| Kích thước (n) | Thuật toán | Số điều kiện κ2​(A) | Sai số tương đối | Trạng thái |
|---|---|---|---|---|
| 5 | GAUSS | $4.77×10^{05}$ | $1.68×10^{−12}$ | Ổn định |
| 5 | SVD | $4.77×10^{05}$ | $4.41×10^{−12}$ | Ổn định |
| 5 | GAUSS_SEIDEL | $4.77×10^{05}$ | FAILED | Sụp đổ |
| 10 | GAUSS | $1.60×10^{13}$ | $8.67×10^{−05}$ | Kém ổn định |
| 10 | SVD | $1.60×10^{13}$ | $2.07×10^{−04}$ | Kém ổn định |
| 10 | GAUSS_SEIDEL | $1.60×10^{13}$ | FAILED | Sụp đổ |
| 15 | GAUSS | $3.68×10^{17}$ | $4.93×10^{00}$ | Kém ổn định |
| 15 | SVD | $3.68×10^{17}$ | $1.35×10^{−03}$ | Kém ổn định |
| 15 | GAUSS_SEIDEL | $3.68×10^{17}$ | FAILED | Sụp đổ |
| 20 | GAUSS | $1.32×10^{18}$ | $7.01×10^{01}$ | Kém ổn định |
| 20 | SVD | $1.32×10^{18}$ | $1.62×10^{−03}$ | Kém ổn định |
| 20 | GAUSS_SEIDEL | $1.32×10^{18}$ | FAILED | Sụp đổ |
| 50 | GAUSS | $1.10×10^{19}$ | $2.25×10^{01}$ | Kém ổn định |
| 50 | SVD | $1.10×10^{19}$ | $1.59×10^{−03}$ | Kém ổn định |
| 50 | GAUSS_SEIDEL | $1.10×10^{19}$ | FAILED | Sụp đổ |
### b. Ma trận SPD
| Kích thước (n) | Thuật toán | Số điều kiện κ2​(A) | Sai số tương đối | Trạng thái |
|---|---|---|---|---|
| 5 | GAUSS | $6.24×10^{01}$ | $1.96×10^{−15}$ | Ổn định |
| 5 | SVD | $6.24×10^{01}$ | $2.91×10^{−15}$ | Ổn định |
| 5 | GAUSS_SEIDEL | $6.24×10^{01}$ | FAILED | Sụp đổ |
| 10 | GAUSS | $8.70×10^{01}$ | $1.18×10^{−15}$ | Ổn định |
| 10 | SVD | $8.70×10^{01}$ | $7.28×10^{−15}$ | Ổn định |
| 10 | GAUSS_SEIDEL | $8.70×10^{01}$ | FAILED | Sụp đổ |
| 15 | GAUSS | $9.47×10^{01}$ | $1.39×10^{−15}$ | Ổn định |
| 15 | SVD | $9.47×10^{01}$ | $4.71×10^{−15}$ | Ổn định |
| 15 | GAUSS_SEIDEL | $9.47×10^{01}$ | FAILED | Sụp đổ |
| 20 | GAUSS | $1.28×10^{02}$ | $1.46×10^{−15}$ | Ổn định |
| 20 | SVD | $1.28×10^{02}$ | $6.99×10^{−15}$ | Ổn định |
| 20 | GAUSS_SEIDEL | $1.28×10^{02}$ | FAILED | Sụp đổ |
| 50 | GAUSS | $1.14×10^{02}$ | $2.26×10^{−15}$ | Ổn định |
| 50 | SVD | $1.14×10^{02}$ | $8.11×10^{−15}$ | Ổn định |
| 50 | GAUSS_SEIDEL | $1.14×10^{02}$ | FAILED | Sụp đổ |

## 2. Nhận xét: 
+ Ma trận SPD (Well-conditioned): Hệ số điều kiện thấp ($k_2(A) \approx 10^2$). Các phương pháp trực tiếp như Gauss và SVD cho kết quả cực kỳ chính xác với sai số xấp xỉ sai số máy tính. 
+ Ma trận Hilbert (Ill-conditioned): Hệ số điều kiện cao ($k_2(A) \approx 10^{19}$) bùng nổ theo hàm mũ. Các phương pháp trực tiếp như Gauss và SVD cho kết quả kém chính xác với sai số lớn hơn sai số máy tính rất nhiều. 
### a. Tại sao sai số của Gauss trên $H_n$ lại lớn như vậy?
Sai số tưởng đối của nghiệm được giới hạn bởi: 
$$
\frac{\|\delta x\|}{\|x\|} \leq \frac{k(A)}{1 - k(A) \epsilon_{mach}} \left( \frac{\|\delta A\|}{\|A\|} + \frac{\|\delta b\|}{\|b\|} \right)
$$
Trong đó, $k(A)$ là số điều kiện của ma trận $A$, $\epsilon_{mach}$ là sai số máy tính. việc sai số bùng nổ trên ma trận Hilbert có thể giải thích qua các nguyên nhân chính như sau:
+ Số điều kiện cực lớn: Ma trận Hilbert có các hàng gần như phụ thuộc tuyến tính, dẫn đến số điều kiện $k(H_n)$ tăng rất nhanh khi $n$ tăng. Như kết quả thực nghiệm cho thấy, với $n\ge50$, $k_2(H_n)$ đạt ngưỡng từ $10^{19}$ trở lên, vượt quá giới hạn của số thực máy tính, dẫn đến sai số tương đối của nghiệm có thể lớn hơn sai số tương đối của dữ liệu đầu vào rất nhiều.
+ Sự khuếch đại của sai số làm tròn: Trong quá trình khử Gauss, các phép biến đổi sơ cấp trên dòng có thể làm tăng sai số làm tròn. Khi nhân với một ma trận có số điều kiện lớn, sai số này sẽ được khuếch đại, dẫn đến sai số tương đối của nghiệm có thể lớn hơn sai số tương đối của dữ liệu đầu vào rất nhiều. 
### b. Phương pháp nào xử lí tốt nhất?
Phương pháp SVD là phương pháp tối ưu nhất trong các phương pháp đã thử nghiệm vì:
+ Tính trực giao: SVD sử dụng các ma trận trực giao U và V, giúp giảm thiểu sai số làm tròn (Điều mà trong Gauss không làm được).
+ Khả năng xử lý ma trận gần suy biến: SVD phân tính ma trận dựa trên các trị số suy biến nên ngay khi ma trận Hilbert gần như suy biến, SVD vẫn có thể cho kết quả tốt bằng các kiểm soát các trị số suy biến nhỏ.
Tuy vậy, SVD có chi phí tính toán cao hơn so với Gauss, Gauss-Seidel.

