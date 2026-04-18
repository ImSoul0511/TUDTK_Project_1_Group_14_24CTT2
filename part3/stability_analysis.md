## 1. Bảng số liệu thực nghiệm:
| n | Loại ma trận | Số điều kiện $\kappa_2(A)$ | Sai số tương đối | Trạng thái |
|---|---|---|---|---|
| 50 | Hilbert | $1.10 \times 10^{19}$ | $5.00 \times 10^{1}$ | Bất ổn định |
| 50 | SPD | $4.67$ | $1.69 \times 10^{2}$ | Ổn định |
| 100 | Hilbert | $3.31 \times 10^{19}$ | $1.00 \times 10^{2}$ | Bất ổn định |
| 100 | SPD | $4.93$ | $4.57 \times 10^{2}$ | Ổn định |
| 200 | Hilbert | $1.60 \times 10^{20}$ | $2.00 \times 10^{2}$ | Cực kỳ bất ổn định |
| 200 | SPD | $4.97$ | $1.28 \times 10^{3}$ | Ổn định |
| 500 | Hilbert | $1.45 \times 10^{20}$ | $5.00 \times 10^{2}$ | Cực kỳ bất ổn định |
| 500 | SPD | $4.92$ | $5.10 \times 10^{3}$ | Ổn định |
| 1000 | Hilbert | $2.30 \times 10^{21}$ | $1.00 \times 10^{3}$ | Cực kỳ bất ổn định |
| 1000 | SPD | $5.03$ | $1.41 \times 10^{4}$ | Ổn định |
## 2. Tại sao sai số của Gauss trên $H_n$ lại lớn như vậy?
Sai số tưởng đối của nghiệm được giới hạn bởi: 
$$
\frac{\|\delta x\|}{\|x\|} \leq \frac{k(A)}{1 - k(A) \epsilon_{mach}} \left( \frac{\|\delta A\|}{\|A\|} + \frac{\|\delta b\|}{\|b\|} \right)
$$
Trong đó, $k(A)$ là số điều kiện của ma trận $A$, $\epsilon_{mach}$ là sai số máy tính. việc sai số bùng nổ trên ma trận Hilbert có thể giải thích qua các nguyên nhân chính như sau:
+ Đặc điểm hình học và số điều kiện cực lớn: Ma trận Hilbert có các hàng gần như phụ thuộc tuyến tính, dẫn đến số điều kiện $k(H_n)$ tăng rất nhanh khi $n$ tăng. Như kết quả thực nghiệm cho thấy, với $n\ge50$, $k_2(H_n)$ đạt ngưỡng từ $10^{19}$ trở lên, vượt quá giới hạn của số thực máy tính, dẫn đến sai số tương đối của nghiệm có thể lớn hơn sai số tương đối của dữ liệu đầu vào rất nhiều.
+ Sự khuếch đại của sai số làm tròn: Trong quá trình khử Gauss, các phép biến đổi sơ cấp trên dòng có thể làm tăng sai số làm tròn. Khi nhân với một ma trận có số điều kiện lớn, sai số này sẽ được khuếch đại, dẫn đến sai số tương đối của nghiệm có thể lớn hơn sai số tương đối của dữ liệu đầu vào rất nhiều. 
## 3. Phương pháp nào xử lí tốt nhất?
