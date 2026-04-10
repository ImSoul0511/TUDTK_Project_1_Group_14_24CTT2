from manim import *
import numpy as np

class Scene2(ThreeDScene):
    def construct(self):
        # ==========================================
        # PHẦN 1: GIỚI THIỆU CÔNG THỨC SVD (TOÀN MÀN HÌNH, KHÔNG KHUNG)
        # ==========================================
        svd_title = Text("Phân rã Giá trị Kỳ dị (SVD)", color=GOLD, font_size=40)
        svd_title.to_edge(UP, buff=0.8)

        svd_eq = MathTex("A", "=", "U", "\\Sigma", "V^T", font_size=90)
        svd_eq.set_color_by_tex("U", BLUE)
        svd_eq.set_color_by_tex("\\Sigma", YELLOW)
        svd_eq.set_color_by_tex("V^T", RED)
        svd_eq.move_to(UP * 0.5)

        # Nhãn giải thích dàn trải ra 3 hướng
        desc_U = Text("U: Vector kỳ dị trái\n(Không gian đầu ra)", font_size=20, color=BLUE)
        desc_U.move_to(LEFT * 4.5 + DOWN * 1.5)

        desc_Sigma = Text("Σ: Ma trận đường chéo\n(Kéo giãn & Khử chiều)", font_size=20, color=YELLOW, line_spacing=0.8)
        desc_Sigma.move_to(DOWN * 2.8)

        desc_V = Text("Vᵀ: Vector kỳ dị phải\n(Không gian đầu vào)", font_size=20, color=RED)
        desc_V.move_to(RIGHT * 4.5 + DOWN * 1.5)

        # Mũi tên cong mượt mà (giống phiên bản MovingCameraScene)
        arrow_U = CurvedArrow(
            start_point=svd_eq[2].get_bottom() + DOWN * 0.1,
            end_point=desc_U.get_top() + RIGHT * 0.5,
            angle=TAU / 8, color=BLUE, stroke_width=3
        )
        arrow_Sigma = Arrow(
            start=svd_eq[3].get_bottom() + DOWN * 0.1,
            end=desc_Sigma.get_top() + UP * 0.1,
            color=YELLOW, buff=0.1, stroke_width=4
        )
        arrow_V = CurvedArrow(
            start_point=svd_eq[4].get_bottom() + DOWN * 0.1,
            end_point=desc_V.get_top() + LEFT * 0.5,
            angle=-TAU / 8, color=RED, stroke_width=3
        )

        # Khóa tất cả 2D vào khung hình (bắt buộc vì ThreeDScene)
        all_2d_part1 = [svd_title, svd_eq, desc_U, desc_Sigma, desc_V,
                        arrow_U, arrow_Sigma, arrow_V]
        for mob in all_2d_part1:
            self.add_fixed_in_frame_mobjects(mob)

        self.play(Write(svd_title))
        self.play(DrawBorderThenFill(svd_eq))
        self.play(
            LaggedStart(
                AnimationGroup(FadeIn(desc_U, shift=UP), Create(arrow_U)),
                AnimationGroup(FadeIn(desc_Sigma, shift=UP), Create(arrow_Sigma)),
                AnimationGroup(FadeIn(desc_V, shift=UP), Create(arrow_V)),
                lag_ratio=0.4
            )
        )
        self.wait(3)

        # Dọn dẹp phần 1 hoàn toàn
        self.play(FadeOut(*all_2d_part1))
        self.wait(0.5)

        # ==========================================
        # PHẦN 2: DEMO 3D (CÓ KHUNG BAO QUANH KHÔNG GIAN)
        # ==========================================

        # --- Tạo khung chỉ bao quanh vùng hiển thị không gian ---
        frame_box = Rectangle(width=12, height=5, color=WHITE, stroke_width=2)
        frame_box.move_to(UP * 1.0)
        frame_box.set_z_index(20)

        mask_top   = Rectangle(width=32, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, UP, buff=0)
        mask_bot   = Rectangle(width=32, height=8,  color=BLACK, fill_opacity=1).next_to(frame_box, DOWN, buff=0)
        mask_left  = Rectangle(width=10, height=6,  color=BLACK, fill_opacity=1).next_to(frame_box, LEFT, buff=0)
        mask_right = Rectangle(width=10, height=6,  color=BLACK, fill_opacity=1).next_to(frame_box, RIGHT, buff=0)
        masks = VGroup(mask_top, mask_bot, mask_left, mask_right).set_z_index(15)

        self.add_fixed_in_frame_mobjects(frame_box, masks)

        # --- Tiêu đề nằm TRÊN khung ---
        title_3d = Text("Minh họa: Hình cầu → Hình Elip (SVD)", font_size=26, color=GOLD)
        title_3d.next_to(frame_box, UP, buff=0.15)
        title_3d.set_z_index(25)
        self.add_fixed_in_frame_mobjects(title_3d)

        # --- Nhãn Σ nằm DƯỚI khung ---
        sigma_label = Text("Σ: Kéo giãn & Khử chiều", font_size=22, color=YELLOW)
        sigma_label.next_to(frame_box, DOWN, buff=0.3)
        sigma_label.set_z_index(25)
        self.add_fixed_in_frame_mobjects(sigma_label)

        # Hiệu ứng xuất hiện khung + tiêu đề
        self.play(FadeIn(frame_box), FadeIn(masks), Write(title_3d), FadeIn(sigma_label))

        # --- Tạo axes + sphere 3D ---
        axes = ThreeDAxes(
            x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3],
            axis_config={"stroke_width": 2}
        )
        sphere = Sphere(radius=1.2, resolution=(24, 24))
        sphere.set_fill(BLUE_B, opacity=0.5)
        sphere.set_stroke(BLUE_A, width=0.5, opacity=0.8)

        # Xoay camera vào góc nhìn 3D
        self.move_camera(phi=70 * DEGREES, theta=45 * DEGREES, run_time=2)
        self.play(Create(axes), Create(sphere))
        self.wait(1)

        # Áp dụng ma trận Sigma (kéo giãn + ép phẳng Z)
        sigma_matrix = np.array([[1.5, 0, 0],
                                  [0, 0.8, 0],
                                  [0,   0, 0]])

        step_label = Text("Áp dụng Σ lên hình cầu...", font_size=20, color=YELLOW)
        step_label.next_to(sigma_label, DOWN, buff=0.2)
        step_label.set_z_index(25)
        self.add_fixed_in_frame_mobjects(step_label)
        self.play(FadeIn(step_label))

        self.play(ApplyMatrix(sigma_matrix, sphere), run_time=3)
        self.wait(1)

        # Trả camera về phẳng để nhìn rõ elip 2D
        result_label = Text("Kết quả: Hình Elip 2D — chiều Z bị triệt tiêu!", font_size=20, color=GREEN)
        result_label.next_to(step_label, DOWN, buff=0.15)
        result_label.set_z_index(25)
        self.add_fixed_in_frame_mobjects(result_label)

        self.move_camera(phi=10 * DEGREES, theta=-90 * DEGREES, run_time=2)
        self.play(FadeOut(step_label), FadeIn(result_label))
        self.wait(2)

        # ==========================================
        # PHẦN 3: KẾT LUẬN (XÓA KHUNG, TOÀN MÀN HÌNH)
        # ==========================================
        self.play(FadeOut(axes, sphere, frame_box, masks, title_3d, sigma_label, result_label))
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=1)

        formula_final = MathTex(
            "\\Sigma", "=",
            "\\begin{bmatrix} 1.5 & 0 & 0 \\\\ 0 & 0.8 & 0 \\end{bmatrix}",
            font_size=54
        )
        formula_final.set_color_by_tex("\\Sigma", YELLOW)
        formula_final.move_to(UP * 0.5)

        final_note = Text(
            "Σ vừa kéo giãn theo trục, vừa loại bỏ không gian thừa!",
            font_size=24, color=GREEN
        )
        final_note.next_to(formula_final, DOWN, buff=0.8)

        self.add_fixed_in_frame_mobjects(formula_final, final_note)
        self.play(Write(formula_final))
        self.play(FadeIn(final_note, shift=UP))
        self.wait(4)