import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

EPSILON = 1e-15

def is_zero(x):
    return abs(x) < EPSILON

def make_zero(x):
    return 0.0 if is_zero(x) else x

class AutoTestReporter:
    """
    Lớp hỗ trợ in kết quả kiểm thử (Test Results) ra Terminal.
    Tính năng: Định dạng màu sắc ANSI, căn lề thẳng hàng tự động và tính toán tỷ lệ tổng kết.
    """
    # Bảng màu ANSI cho Terminal
    COLOR_HEADER = '\033[95m'  
    COLOR_BLUE = '\033[94m'    
    COLOR_CYAN = '\033[96m'    
    COLOR_GREEN = '\033[92m'   
    COLOR_WARNING = '\033[93m' 
    COLOR_RED = '\033[91m'     
    STYLE_RESET = '\033[0m'    
    STYLE_BOLD = '\033[1m'      

    @classmethod
    def print_suite_header(cls, suite_name: str):
        """
        In ra khung tiêu đề của một bộ test để ngăn cách các phần (vd: Định thức, Khử Gauss).
        """
        border = f"{cls.COLOR_CYAN}{cls.STYLE_BOLD}={'='*75}{cls.STYLE_RESET}"
        title = f"{cls.COLOR_CYAN}{cls.STYLE_BOLD} BỘ KIỂM THỬ: {suite_name.upper()}{cls.STYLE_RESET}"
        
        print(f"\n{border}")
        print(title)
        print(border)

    @classmethod
    def print_result(cls, test_name: str, passed: bool, details: str = ""):
        """
        In kết quả Pass/Fail của một test case. 
        Tự động căn lề để hộp trạng thái nằm thẳng hàng.
        """
        max_len = 45 
        
        if len(test_name) > max_len:
            name_padded = f"{test_name[:42]}..."
        else:
            name_padded = f"{test_name:<{max_len}}"
        
        if passed:
            status = f"{cls.COLOR_GREEN}{cls.STYLE_BOLD}[PASS]{cls.STYLE_RESET}"
            detail_str = f"{cls.COLOR_GREEN}{details}{cls.STYLE_RESET}" if details else ""
        else:
            status = f"{cls.COLOR_RED}{cls.STYLE_BOLD}[FAIL]{cls.STYLE_RESET}"
            detail_str = f"{cls.COLOR_RED}{details}{cls.STYLE_RESET}" if details else ""
            
        print(f" {name_padded} {status}  {detail_str}")
 
    @classmethod
    def print_summary(cls, passed_count: int, total_count: int):
        """
        In ra dòng tổng kết: Số test thành công / Tổng số test, tỷ lệ % và nhận xét.
        """
        print(f"{cls.COLOR_CYAN}{'-'*75}{cls.STYLE_RESET}")
        
        if total_count == 0:
            print(f"{cls.COLOR_WARNING}{cls.STYLE_BOLD}  CẢNH BÁO: KHÔNG CÓ TEST CASE NÀO ĐƯỢC CHẠY!{cls.STYLE_RESET}\n")
            return
        percent = (passed_count / total_count) * 100
        
        if passed_count == total_count:
            print(f"{cls.COLOR_GREEN}{cls.STYLE_BOLD}  TỔNG KẾT: {passed_count}/{total_count} ({percent:.0f}%) HOÀN HẢO!{cls.STYLE_RESET}\n")
        else:
            print(f"{cls.COLOR_RED}{cls.STYLE_BOLD}  TỔNG KẾT: {passed_count}/{total_count} ({percent:.1f}%) PASSED - CẦN DEBUG LẠI CODE!{cls.STYLE_RESET}\n")


