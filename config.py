EPSILON = 1e-15

def is_zero(x):
    """
    Kiểm tra một số có gần bằng 0 hay không dựa trên giá trị EPSILON.

    Args:
        x: Giá trị cần kiểm tra.

    Returns:
        bool: True nếu x coi như bằng 0, ngược lại False.
    """
    return abs(x) < EPSILON

def make_zero(x):
    """
    Làm tròn một số về 0.0 nếu nó được coi là số 0.

    Args:
        x: Giá trị đầu vào.

    Returns:
        float: 0.0 nếu là số 0, ngược lại trả về chính nó.
    """
    return 0.0 if is_zero(x) else x

class AutoTestReporter:
    """
    Lớp tiện ích (Utility Class) hỗ trợ in kết quả kiểm thử (Test Results) ra Terminal.
    """
    minus_sign = "-" * 90

    @classmethod
    def print_header(cls, title: str):
        """
        In tiêu đề phần kiểm thử.

        Args:
            title: Tên tiêu đề.

        Returns:
            None
        """
        print(cls.minus_sign)
        print(title)
        print(cls.minus_sign)

    @classmethod
    def print_result(cls, test_name: str, passed: bool, details: str = ""):
        """
        In kết quả của một ca kiểm thử.

        Args:
            test_name: Tên của ca kiểm thử.
            passed: Trạng thái thành công hay thất bại.
            details: Thông tin chi tiết (tùy chọn).

        Returns:
            None
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
        In tổng kết quả sau khi chạy xong tất cả kiểm thử.

        Args:
            passed_count: Số ca kiểm thử thành công.
            total_count: Tổng số ca kiểm thử.

        Returns:
            None
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
