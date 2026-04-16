from IPython.display import display, Markdown

EPSILON = 1e-15

def is_zero(x):
    return abs(x) < EPSILON

def make_zero(x):
    return 0.0 if is_zero(x) else x

class AutoTestReporter:
    """
    Lớp tiện ích (Utility Class) hỗ trợ in kết quả kiểm thử (Test Results) ra Terminal.
    """

    @classmethod
    def print_result(cls, test_name: str, passed: bool, details: str = ""):
        """
        In kết quả Pass/Fail của một test case. 
        Tự động căn lề để hộp trạng thái nằm thẳng hàng.
        """
        max_len = 70
        
        if len(test_name) > max_len:
            name_padded = f"{test_name}"
        else:
            name_padded = f"{test_name:<{max_len}}"
        
        if passed:
            status = f"[OK]"
            detail_str = f"{details}" if details else ""
        else:
            status = f"[FAIL]"
            detail_str = f"{details}" if details else ""
            
        print(f"{name_padded} {status}  {detail_str}")
 
    @classmethod
    def print_summary(cls, passed_count: int, total_count: int):
        """
        In ra dòng tổng kết: Số test thành công / Tổng số test, tỷ lệ % và nhận xét.
        """
        if total_count == 0:
            display(Markdown("### All failed\n"))
            return
        percent = (passed_count / total_count) * 100
        
        if passed_count == total_count:
            display(Markdown(f"### Kết luận: {passed_count}/{total_count} ({percent:.0f}%) hoàn thành\n"))
        else:
            display(Markdown(f"### Kết luận: Chỉ {passed_count}/{total_count} ({percent:.1f}%) đã hoàn thành\n"))


def calculate_l2_relative_error(A: list[list[float]], x_hat: list[float], b: list[float]) -> float:
    """Tính sai số tương đối chuẩn L2 bằng NumPy"""