from manim import *
import numpy as np
from part2.diagonalization import diagonalize_with_qr

class Scene(MovingCameraScene):
    def construct(self):
        # ==========================================
        # 1. SETUP DỮ LIỆU
        # ==========================================
        A_list = [[3.0, 1.0], [0.0, 2.0]]
        P_list, D_list, P_inv_list = diagonalize_with_qr(A_list)
        
        # Chuyển sang Numpy Array 2D chuẩn
        A = np.array(A_list, dtype=float).reshape(2, 2)
        P = np.array(P_list, dtype=float).reshape(2, 2)
        D = np.array(D_list, dtype=float).reshape(2, 2)
        P_inv = np.array(P_inv_list, dtype=float).reshape(2, 2)

        # ==========================================
        # 2. THỦ THUẬT CAMERA VÀ TẠO KHUNG (MASKING)
        # ==========================================
        self.camera.frame.shift(DOWN * 1.5)
        
        # --- VÙNG HÌNH HỌC ---
        plane = NumberPlane(x_range=[-15, 15], y_range=[-15, 15], background_line_style={"stroke_opacity": 0.5})
        
        # Giảm kích thước hình tròn ban đầu (radius = 0.6)
        unit_circle = Circle(radius=0.6, color=YELLOW, fill_opacity=0.3)
        basis_vectors = VGroup(Vector(RIGHT, color=GREEN), Vector(UP, color=RED))
        
        geometry_area = VGroup(plane, unit_circle, basis_vectors)
        
        # --- KHUNG HIỂN THỊ VÀ MÀN CHE ---
        frame_box = Rectangle(width=13, height=4.5, color=WHITE).move_to(ORIGIN)
        frame_box.set_z_index(11) 
        
        mask_top = Rectangle(width=30, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, UP, buff=0)
        mask_bottom = Rectangle(width=30, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, DOWN, buff=0)
        mask_left = Rectangle(width=10, height=4.5, color=BLACK, fill_opacity=1).next_to(frame_box, LEFT, buff=0)
        mask_right = Rectangle(width=10, height=4.5, color=BLACK, fill_opacity=1).next_to(frame_box, RIGHT, buff=0)
        
        masks = VGroup(mask_top, mask_bottom, mask_left, mask_right)
        masks.set_z_index(10) 

        # ==========================================
        # 3. VÙNG TOÁN HỌC (ĐÃ TÁCH A VÀ DẤU BẰNG ĐỂ HIGHLIGHT ĐẸP HƠN)
        # ==========================================
        title_txt = Text("Chéo hóa Ma trận: ", font_size=28)
        title_math = MathTex("A = P^{-1} D P", color=YELLOW).scale(1.1)
        title_group = VGroup(title_txt, title_math).arrange(RIGHT)

        # Tách riêng A và dấu "="
        math_A = MathTex(r"\begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}")
        math_eq = MathTex("=")
        math_P = MathTex(r"\begin{bmatrix} 1 & 1 \\ 0 & -1 \end{bmatrix}", color=BLUE)
        math_D = MathTex(r"\begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix}", color=GREEN)
        math_Pi = MathTex(r"\begin{bmatrix} 1 & 1 \\ 0 & -1 \end{bmatrix}", color=RED)
        
        formula = VGroup(math_A, math_eq, math_P, math_D, math_Pi).arrange(RIGHT, buff=0.15).scale(0.65)
        
        math_area = VGroup(title_group, formula).arrange(DOWN).move_to(np.array([0, -3.8, 0]))
        math_area.set_z_index(12)

        # ==========================================
        # 4. HIỂN THỊ VÀ ANIMATION (CÓ HIGHLIGHT)
        # ==========================================
        self.play(FadeIn(geometry_area), FadeIn(masks), FadeIn(frame_box))
        self.play(Write(title_group), FadeIn(formula))
        self.wait(1)

        geometry_area.save_state()

        # --- Cảnh: Tác động của A ---
        label_A = Text("Tác động trực tiếp của A", font_size=22, color=YELLOW).next_to(frame_box.get_corner(UL), DR, buff=0.2).set_z_index(12)
        
        # Tạo viền sáng quanh ma trận A
        box_A = SurroundingRectangle(math_A, color=YELLOW, buff=0.1).set_z_index(12)
        
        self.play(Write(label_A))
        self.wait(0.5)
        
        # Play đồng thời việc vẽ viền và biến đổi không gian
        self.play(
            Create(box_A),
            ApplyMatrix(A, geometry_area), 
            run_time=3
        )
        self.wait(2)

        # Xóa viền và khôi phục không gian
        self.play(Restore(geometry_area), FadeOut(label_A), Uncreate(box_A))
        self.wait(1)

        # --- Cảnh: Tác động của P^-1, D, P ---
        label_PDP = Text("Tác động lần lượt: P⁻¹ -> D -> P", font_size=22, color=BLUE).next_to(frame_box.get_corner(UL), DR, buff=0.2).set_z_index(12)
        self.play(Write(label_PDP))

        # Step 1: P⁻¹
        box_Pi = SurroundingRectangle(math_Pi, color=RED, buff=0.1).set_z_index(12)
        self.play(Create(box_Pi), ApplyMatrix(P_inv, geometry_area), run_time=2)
        self.play(FadeOut(box_Pi))
        self.wait(0.5)

        # Step 2: D
        box_D = SurroundingRectangle(math_D, color=GREEN, buff=0.1).set_z_index(12)
        self.play(Create(box_D), ApplyMatrix(D, geometry_area), run_time=2)
        self.play(FadeOut(box_D))
        self.wait(0.5)

        # Step 3: P
        box_P = SurroundingRectangle(math_P, color=BLUE, buff=0.1).set_z_index(12)
        self.play(Create(box_P), ApplyMatrix(P, geometry_area), run_time=2)
        self.play(FadeOut(box_P))
        self.wait(2)

        # ==========================================
        # 5. KẾT LUẬN & ĐIỂM YẾU/SVD
        # ==========================================
        self.play(FadeOut(geometry_area, frame_box, masks, math_area, label_PDP))
        
        center_y = -1.5 
        
        weakness_title = Text("Điểm yếu của thuật toán Chéo hóa:", color=RED, font_size=36).move_to(np.array([0, center_y + 1.5, 0]))
        weakness_points = VGroup(
            Text("• Chỉ áp dụng được lên ma trận vuông.", font_size=28),
            Text("• Một số ma trận sẽ KHÔNG THỂ được chéo hóa.", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(weakness_title, DOWN, buff=0.8)
        
        self.play(Write(weakness_title))
        self.play(FadeIn(weakness_points))
        self.wait(3)
        self.play(FadeOut(weakness_title, weakness_points))

        svd_title = Text("Ý tưởng cốt lõi của SVD", color=YELLOW, font_size=40).move_to(np.array([0, center_y + 1.5, 0]))
        
        svd_desc = Text(
            "Bất kỳ ma trận nào, dù đối xứng hay không, có hình dáng ra sao,\nđều có thể được phân rã thành tích của 3 ma trận đặc biệt.", 
            font_size=28
        ).next_to(svd_title, DOWN, buff=1)
        
        svd_advantage = Text("Ưu thế: Ma trận đầu vào không nhất thiết phải là ma trận vuông.", font_size=28, color=GREEN).next_to(svd_desc, DOWN, buff=0.8)

        self.play(Write(svd_title))
        self.play(FadeIn(svd_desc))
        self.wait(2)
        self.play(Write(svd_advantage))
        self.wait(4)