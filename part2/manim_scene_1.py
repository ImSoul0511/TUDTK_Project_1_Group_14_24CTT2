from manim import *
import numpy as np
from diagonalization import diagonalize

class Scene_1(Scene):
    """
    Giải thích thuật toán chéo hóa ma trận từng bước
    """
    def construct(self):
        intro_title = Text("Thuật toán chéo hóa ma trận", font_size=56, color=GOLD)
        self.play(Write(intro_title))
        self.wait(3)
        self.play(FadeOut(intro_title))

        title = Text("Chi tiết thuật toán: Chéo hóa Ma trận", font_size=36, color=GOLD)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(2)

        mat_A = MathTex(
            r"A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}"
        ).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(mat_A, shift=DOWN))
        self.wait(2)

        step1_title = Text("Bước 1: Tìm Trị riêng (Eigenvalues)", font_size=24, color=TEAL)
        step1_title.next_to(mat_A, DOWN, buff=0.5).align_to(title, LEFT).shift(RIGHT*0.5)
        
        step1_eq1 = MathTex(r"\det(A - \lambda I) = 0", font_size=32)
        step1_eq2 = MathTex(r"\det \left( \begin{bmatrix} 3-\lambda & 1 \\ 0 & 2-\lambda \end{bmatrix} \right) = 0", font_size=32)
        step1_eq3 = MathTex(r"(3-\lambda)(2-\lambda) = 0", font_size=32)
        step1_result = MathTex(r"\Rightarrow \lambda_1 = 3, \lambda_2 = 2", font_size=36, color=YELLOW)

        step1_group = VGroup(step1_eq1, step1_eq2, step1_eq3, step1_result)
        step1_group.arrange(DOWN, buff=0.2).next_to(step1_title, DOWN, buff=0.2).align_to(step1_title, LEFT).shift(RIGHT*0.5)

        self.play(Write(step1_title))
        self.play(FadeIn(step1_eq1))
        self.wait(1.5)
        self.play(TransformMatchingTex(step1_eq1.copy(), step1_eq2))
        self.wait(1.5)
        self.play(TransformMatchingTex(step1_eq2.copy(), step1_eq3))
        self.wait(1.5)
        self.play(FadeIn(step1_result, scale=1.2))
        self.wait(3)

        self.play(
            FadeOut(step1_eq1, step1_eq2, step1_eq3),
            step1_result.animate.next_to(step1_title, DOWN, buff=0.2).align_to(step1_title, LEFT).shift(RIGHT*0.5)
        )

        step2_title = Text("Bước 2: Tìm Vector riêng (Eigenvectors)", font_size=24, color=TEAL)
        step2_title.next_to(step1_result, DOWN, buff=0.5).align_to(step1_title, LEFT)

        step2_sub1 = VGroup(
            Text("Với", font_size=24),
            MathTex(r"\lambda_1 = 3: (A - 3I)x = 0 \Rightarrow v_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}", font_size=32)
        ).arrange(RIGHT, buff=0.2)
        
        step2_sub2 = VGroup(
            Text("Với", font_size=24),
            MathTex(r"\lambda_2 = 2: (A - 2I)x = 0 \Rightarrow v_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}", font_size=32)
        ).arrange(RIGHT, buff=0.2)
        
        step2_group = VGroup(step2_sub1, step2_sub2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        step2_group.next_to(step2_title, DOWN, buff=0.2).align_to(step2_title, LEFT).shift(RIGHT*0.5)

        self.play(Write(step2_title))
        self.play(FadeIn(step2_sub1, shift=RIGHT))
        self.wait(1.5)
        self.play(FadeIn(step2_sub2, shift=RIGHT))
        self.wait(3)

        step3_title = Text("Bước 3: Lập ma trận P (chứa vector riêng) và D (chứa trị riêng)", font_size=24, color=TEAL)
        
        self.play(FadeOut(step1_title, step1_result, step2_title, step2_group))
        
        step3_title.next_to(mat_A, DOWN, buff=0.6)
        
        mat_P = MathTex(
            r"P = \begin{bmatrix} v_1 & v_2 \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 0 & -1 \end{bmatrix}", color=BLUE
        )
        mat_D = MathTex(
            r"D = \text{diag}(\lambda_1, \lambda_2) = \begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix}", color=GREEN
        )
        
        step3_group = VGroup(mat_P, mat_D).arrange(RIGHT, buff=1.0)
        step3_group.next_to(step3_title, DOWN, buff=0.5)

        self.play(Write(step3_title))
        self.play(FadeIn(mat_P, shift=UP), FadeIn(mat_D, shift=UP))
        self.wait(4)

        final_eq = MathTex(r"A = P \cdot D \cdot P^{-1}", font_size=44)
        final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.2)
        final_group = VGroup(final_eq, final_box).next_to(step3_group, DOWN, buff=1.0)

        self.play(Write(final_eq))
        self.play(Create(final_box))
        self.wait(5)

        self.play(FadeOut(title, mat_A, step3_title, mat_P, mat_D, final_group))
        self.wait(2)

class Scene_2(MovingCameraScene):
    """
    Trực quan hóa thuật toán chéo hóa ma trận
    """
    def construct(self):
        A_list = [[3.0, 1.0], [0.0, 2.0]]
        P_list, D_list, P_inv_list = diagonalize(A_list)
        
        A = np.array(A_list, dtype=float).reshape(2, 2)
        P = np.array(P_list, dtype=float).reshape(2, 2)
        D = np.array(D_list, dtype=float).reshape(2, 2)
        P_inv = np.array(P_inv_list, dtype=float).reshape(2, 2)

        self.camera.frame.shift(DOWN * 1.5)
        
        plane = NumberPlane(x_range=[-15, 15], y_range=[-15, 15], background_line_style={"stroke_opacity": 0.5})
        
        unit_circle = Circle(radius=0.6, color=YELLOW, fill_opacity=0.3)
        basis_vectors = VGroup(Vector(RIGHT, color=GREEN), Vector(UP, color=RED))
        
        geometry_area = VGroup(plane, unit_circle, basis_vectors)
        
        frame_box = Rectangle(width=13, height=4.5, color=WHITE).move_to(ORIGIN)
        frame_box.set_z_index(11) 
        
        mask_top = Rectangle(width=30, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, UP, buff=0)
        mask_bottom = Rectangle(width=30, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, DOWN, buff=0)
        mask_left = Rectangle(width=10, height=4.5, color=BLACK, fill_opacity=1).next_to(frame_box, LEFT, buff=0)
        mask_right = Rectangle(width=10, height=4.5, color=BLACK, fill_opacity=1).next_to(frame_box, RIGHT, buff=0)
        
        masks = VGroup(mask_top, mask_bottom, mask_left, mask_right)
        masks.set_z_index(10) 

        title_txt = Text("Chéo hóa Ma trận: ", font_size=28)
        title_math = MathTex("A = P^{-1} D P", color=YELLOW).scale(1.1)
        title_group = VGroup(title_txt, title_math).arrange(RIGHT)

        math_A = MathTex(r"\begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}")
        math_eq = MathTex("=")
        math_P = MathTex(r"\begin{bmatrix} 1 & 1 \\ 0 & -1 \end{bmatrix}", color=BLUE)
        math_D = MathTex(r"\begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix}", color=GREEN)
        math_Pi = MathTex(r"\begin{bmatrix} 1 & 1 \\ 0 & -1 \end{bmatrix}", color=RED)
        
        formula = VGroup(math_A, math_eq, math_P, math_D, math_Pi).arrange(RIGHT, buff=0.15).scale(0.65)
        
        math_area = VGroup(title_group, formula).arrange(DOWN).move_to(np.array([0, -3.8, 0]))
        math_area.set_z_index(12)

        self.play(FadeIn(geometry_area), FadeIn(masks), FadeIn(frame_box))
        self.play(Write(title_group), FadeIn(formula))
        self.wait(1)

        geometry_area.save_state()

        label_A = Text("Tác động trực tiếp của A", font_size=22, color=YELLOW).next_to(frame_box.get_corner(UL), DR, buff=0.2).set_z_index(12)
        
        box_A = SurroundingRectangle(math_A, color=YELLOW, buff=0.1).set_z_index(12)
        
        self.play(Write(label_A))
        self.wait(0.5)
        
        self.play(
            Create(box_A),
            ApplyMatrix(A, geometry_area), 
            run_time=3
        )
        self.wait(2)

        self.play(Restore(geometry_area), FadeOut(label_A), Uncreate(box_A))
        self.wait(1)

        label_PDP = Text("Tác động lần lượt: P⁻¹ -> D -> P", font_size=22, color=BLUE).next_to(frame_box.get_corner(UL), DR, buff=0.2).set_z_index(12)
        self.play(Write(label_PDP))

        box_Pi = SurroundingRectangle(math_Pi, color=RED, buff=0.1).set_z_index(12)
        self.play(Create(box_Pi), ApplyMatrix(P_inv, geometry_area), run_time=2)
        self.play(FadeOut(box_Pi))
        self.wait(0.5)

        box_D = SurroundingRectangle(math_D, color=GREEN, buff=0.1).set_z_index(12)
        self.play(Create(box_D), ApplyMatrix(D, geometry_area), run_time=2)
        self.play(FadeOut(box_D))
        self.wait(0.5)

        box_P = SurroundingRectangle(math_P, color=BLUE, buff=0.1).set_z_index(12)
        self.play(Create(box_P), ApplyMatrix(P, geometry_area), run_time=2)
        self.play(FadeOut(box_P))
        self.wait(2)

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