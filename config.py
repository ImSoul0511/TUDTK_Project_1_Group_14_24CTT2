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
    minus_sign = "-" * 90

    @classmethod
    def print_header(cls, title: str):
        """
        In tiêu đề của phần kiểm thử.
        """
        print(cls.minus_sign)
        print(title)
        print(cls.minus_sign)

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
            print(cls.minus_sign)
            print("All failed")
            print(cls.minus_sign)
            return
        percent = (passed_count / total_count) * 100
        
        if passed_count == total_count:
            print(cls.minus_sign)
            print(f"Kết luận: {passed_count}/{total_count} ({percent:.0f}%) hoàn thành")
            print(cls.minus_sign)
        else:
            print(cls.minus_sign)
            print(f"Kết luận: Chỉ {passed_count}/{total_count} ({percent:.1f}%) đã hoàn thành")
            print(cls.minus_sign)
