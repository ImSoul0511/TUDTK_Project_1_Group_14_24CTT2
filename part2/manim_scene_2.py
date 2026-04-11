from manim import *
import numpy as np

"""
Flow: 
    1. Intro 3 ô vuông S, V, D
    2. Giới thiệu công thức SVD
    3. Ma trận Sigma
    4. Ma trận đơn vị có nhiệm vụ giữ nguyên không gian
    5. Mở rộng ma trận đơn vị sang ma trận hình chữ nhật (vẫn giữ nguyên không gian)
        - Ví dụ ma trận 2x3 sẽ biến không gian 3D thành 2D bằng cách bỏ đi chiều Z 
        (Hiệu ứng ma trận đơn vị 2x3 tác động lên không gian 3D)
        - Ma trận 3x2 sẽ biến không gian 2D thành 3D bằng cách thêm chiều Z
        (Hiệu ứng ma trận đơn vị 3x2 tác động lên không gian 2D)
    => Gọi là ma trận hiệu chỉnh chiều
    6. Ma trận đường chéo có nhiệm vụ kéo giãn hoặc thu hẹp không gian theo các chiều x, y, z tương ứng trên đường chéo
    => Focus hiệu ứng của ma trận [[2,0], [0,3]] kéo dãn trục Ox 2 lần và trục Oy 3 lần 
    7. Khi kết hợp 2 ma trận hiệu chỉnh chiều và ma trận đường chéo
    => Ta được hiệu ứng thêm hoặc mất chiều đồng thời kéo giãn / thu hẹp không gian
    => Đây là nhiệm vụ của ma trận Sigma

Render order:
    manim -pql part2/manim_scene_2.py Scene2
    manim -pql part2/manim_scene_2.py Scene2_3D
    manim -pql part2/manim_scene_2.py Scene2_Sigma
"""


# ==============================================================================
# SCENE 2: Steps 1-4 (Intro, SVD Formula, Sigma, Identity Matrix)
# ==============================================================================
class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.frame.shift(DOWN * 1.5)
        center_y = -1.5

        # ------------------------------------------
        # STEP 1: INTRO – 3 ô vuông S – V – D
        # ------------------------------------------
        letters = ["S", "V", "D"]
        boxes = VGroup()
        for letter in letters:
            txt = Text(letter, font_size=72, color=WHITE, weight=BOLD)
            box = Square(side_length=1.5, color=WHITE, stroke_width=3)
            group = VGroup(box, txt)
            boxes.add(group)
        boxes.arrange(RIGHT, buff=0.15).move_to(np.array([0, center_y, 0]))

        self.play(
            LaggedStart(
                *[FadeIn(b, shift=DOWN * 0.5) for b in boxes],
                lag_ratio=0.3
            ),
            run_time=1.5
        )
        self.wait(1)

        # Flash viền sáng
        self.play(
            LaggedStart(
                *[Indicate(b[0], color=GOLD, scale_factor=1.05) for b in boxes],
                lag_ratio=0.2
            ),
            run_time=1.2
        )
        self.wait(1.5)
        self.play(FadeOut(boxes))
        self.wait(0.5)

        # ------------------------------------------
        # STEP 2: GIỚI THIỆU CÔNG THỨC SVD
        # ------------------------------------------
        svd_title = Text("Phân rã Giá trị Kỳ dị (SVD)", color=GOLD, font_size=40)
        svd_title.move_to(np.array([0, center_y + 2.5, 0]))

        svd_eq = MathTex("A", "=", "U", "\\Sigma", "V^T", font_size=90)
        svd_eq.set_color_by_tex("U", BLUE)
        svd_eq.set_color_by_tex("\\Sigma", YELLOW)
        svd_eq.set_color_by_tex("V^T", RED)
        svd_eq.move_to(np.array([0, center_y + 0.5, 0]))

        desc_U = Text("U: Vector kỳ dị trái\n(Không gian đầu ra)", font_size=20, color=BLUE)
        desc_U.move_to(np.array([-4.5, center_y - 1.5, 0]))

        desc_Sigma = Text("Σ: Ma trận đường chéo\n(Kéo giãn & Khử chiều)", font_size=20, color=YELLOW, line_spacing=0.8)
        desc_Sigma.move_to(np.array([0, center_y - 2.8, 0]))

        desc_V = Text("Vᵀ: Vector kỳ dị phải\n(Không gian đầu vào)", font_size=20, color=RED)
        desc_V.move_to(np.array([4.5, center_y - 1.5, 0]))

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

        # ------------------------------------------
        # STEP 3: FOCUS VÀO MA TRẬN SIGMA
        # ------------------------------------------
        self.play(
            FadeOut(svd_title, desc_U, desc_V, arrow_U, arrow_V, arrow_Sigma),
            FadeOut(svd_eq[0], svd_eq[1], svd_eq[2], svd_eq[4])
        )

        # Di chuyển Σ và mô tả lên góc trên-trái làm header
        self.play(
            svd_eq[3].animate.scale(0.7).move_to(np.array([-5.5, center_y + 3, 0])),
            desc_Sigma.animate.scale(1.1).move_to(np.array([-2.5, center_y + 3, 0])),
        )
        self.wait(0.5)

        sigma_explain = Text("Sigma (Σ) là tích của 2 loại ma trận:", font_size=28, color=YELLOW)
        sigma_explain.move_to(np.array([0, center_y + 1.5, 0]))

        task1 = Text("① Ma trận hiệu chỉnh chiều (Thêm / Bớt chiều không gian)", font_size=24, color=TEAL)
        task2 = Text("② Ma trận đường chéo (Kéo giãn / Thu hẹp theo từng trục)", font_size=24, color=ORANGE)
        tasks = VGroup(task1, task2).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        tasks.next_to(sigma_explain, DOWN, buff=0.8)

        self.play(Write(sigma_explain))
        self.play(FadeIn(task1, shift=LEFT))
        self.wait(0.5)
        self.play(FadeIn(task2, shift=LEFT))
        self.wait(2)

        transition_txt = Text("Bắt đầu từ nền tảng: Ma trận Đơn vị I", font_size=28, color=GREEN)
        transition_txt.next_to(tasks, DOWN, buff=1)
        self.play(Write(transition_txt))
        self.wait(2)

        self.play(FadeOut(svd_eq[3], desc_Sigma, sigma_explain, tasks, transition_txt))
        self.wait(0.5)

        # ------------------------------------------
        # STEP 4: MA TRẬN ĐƠN VỊ GIỮ NGUYÊN KHÔNG GIAN (2D Demo)
        # ------------------------------------------
        # --- Khung + Masks (style giống Scene1) ---
        frame_box = Rectangle(width=13, height=4.5, color=WHITE, stroke_width=2).move_to(ORIGIN)
        frame_box.set_z_index(11)

        mask_top    = Rectangle(width=30, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, UP, buff=0)
        mask_bottom = Rectangle(width=30, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, DOWN, buff=0)
        mask_left   = Rectangle(width=10, height=4.5, color=BLACK, fill_opacity=1).next_to(frame_box, LEFT, buff=0)
        mask_right  = Rectangle(width=10, height=4.5, color=BLACK, fill_opacity=1).next_to(frame_box, RIGHT, buff=0)
        masks = VGroup(mask_top, mask_bottom, mask_left, mask_right).set_z_index(10)

        title_step4 = Text("Ma trận Đơn vị I — Giữ nguyên không gian", font_size=26, color=GOLD)
        title_step4.next_to(frame_box, UP, buff=0.15).set_z_index(12)

        # --- Vùng hình học ---
        plane = NumberPlane(
            x_range=[-8, 8], y_range=[-8, 8],
            background_line_style={"stroke_opacity": 0.4}
        )
        unit_circle = Circle(radius=1, color=YELLOW, fill_opacity=0.3)
        basis_e1 = Vector(RIGHT, color=GREEN)
        basis_e2 = Vector(UP, color=RED)
        geometry = VGroup(plane, unit_circle, basis_e1, basis_e2)

        # --- Ma trận I bên dưới khung ---
        math_I = MathTex(
            "I", "=",
            r"\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}",
            font_size=48
        ).move_to(np.array([0, -3.8, 0])).set_z_index(12)

        self.play(FadeIn(frame_box, masks), Write(title_step4))
        self.play(FadeIn(geometry))
        self.play(FadeIn(math_I))
        self.wait(1)

        # Áp dụng I — không gian giữ nguyên
        I_matrix = np.array([[1, 0], [0, 1]])

        label_apply = Text("Áp dụng I lên không gian:", font_size=22, color=GREEN)
        label_apply.next_to(frame_box.get_corner(UL), DR, buff=0.2).set_z_index(12)
        box_I = SurroundingRectangle(math_I, color=GREEN, buff=0.1).set_z_index(12)

        self.play(Write(label_apply), Create(box_I))
        self.play(ApplyMatrix(I_matrix, geometry), run_time=2)

        result_txt = Text("→ Không gian giữ nguyên hoàn toàn!", font_size=22, color=GREEN)
        result_txt.next_to(frame_box.get_corner(UR), DL, buff=0.2).set_z_index(12)
        self.play(Write(result_txt))
        self.wait(2)

        # Gợi mở cho step 5
        hint_txt = Text("Nếu I không vuông thì sao? → Hiệu chỉnh chiều!", font_size=22, color=TEAL)
        hint_txt.next_to(math_I, DOWN, buff=0.5).set_z_index(12)
        self.play(FadeOut(box_I), Write(hint_txt))
        self.wait(3)

        self.play(FadeOut(geometry, frame_box, masks, title_step4, math_I,
                          label_apply, result_txt, hint_txt))
        self.wait(1)


# ==============================================================================
# SCENE 2_3D: Step 5 (Ma trận hiệu chỉnh chiều — 3D demos)
# ==============================================================================
class Scene2_3D(ThreeDScene):
    def construct(self):
        # --- Khung + Masks ---
        # frame_box ở ORIGIN để khớp với camera 3D (luôn nhìn vào ORIGIN)
        self.move_camera(frame_center=np.array([0, -0.75, 0]))
        frame_box = Rectangle(width=12, height=5, color=WHITE, stroke_width=2).move_to(ORIGIN)
        frame_box.set_z_index(20)

        mask_top   = Rectangle(width=32, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, UP, buff=0)
        mask_bot   = Rectangle(width=32, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, DOWN, buff=0)
        mask_left  = Rectangle(width=10, height=6,  color=BLACK, fill_opacity=1).next_to(frame_box, LEFT, buff=0)
        mask_right = Rectangle(width=10, height=6,  color=BLACK, fill_opacity=1).next_to(frame_box, RIGHT, buff=0)
        masks = VGroup(mask_top, mask_bot, mask_left, mask_right).set_z_index(15)

        self.add_fixed_in_frame_mobjects(frame_box, masks)

        title = Text("Ma trận Hiệu chỉnh chiều (Dimension Adjustment)", font_size=24, color=GOLD)
        title.next_to(frame_box, UP, buff=0.15).set_z_index(25)
        self.add_fixed_in_frame_mobjects(title)

        self.play(FadeIn(frame_box, masks), Write(title))

        # --- Trục 3D (dùng chung cho 5a và 5b) ---
        # Axes ở ORIGIN — camera 3D mặc định nhìn vào đây
        axes = ThreeDAxes(
            x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3],
            axis_config={"stroke_width": 2}
        )

        # ==========================================
        # STEP 5a: I_{2×3} — Không gian 3D → 2D (Bỏ chiều Z)
        # ==========================================
        subtitle_5a = Text("I₂ₓ₃ : Không gian 3D → 2D (Bỏ chiều Z)", font_size=20, color=TEAL)
        subtitle_5a.next_to(frame_box, DOWN, buff=0.25).set_z_index(25)
        self.add_fixed_in_frame_mobjects(subtitle_5a)
        self.remove(subtitle_5a)

        self.wait(1)
        math_5a = MathTex(
            r"I_{2 \times 3}", "=",
            r"\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}",
            font_size=38
        ).next_to(subtitle_5a, DOWN, buff=0.2).set_z_index(25)
        math_5a[0].set_color(TEAL)
        self.add_fixed_in_frame_mobjects(math_5a)
        self.remove(math_5a)

        # Hình cầu 3D — ở ORIGIN (trùng tâm camera 3D → hiện giữa frame_box)
        sphere = Sphere(radius=1.2, resolution=(24, 24))
        sphere.set_fill(BLUE_B, opacity=0.5)
        sphere.set_stroke(BLUE_A, width=0.5, opacity=0.8)
        group_axes_sphere = VGroup(axes, sphere)
        group_axes_sphere.move_to(np.array([0, -0.5, 0])) 

        self.move_camera(phi=70 * DEGREES, theta=45 * DEGREES, run_time=2)
        self.play(Create(group_axes_sphere))
        self.play(FadeIn(subtitle_5a, shift=UP), FadeIn(math_5a, shift=UP))
        self.wait(1)

        # Highlight ma trận và áp dụng: [[1,0,0],[0,1,0],[0,0,0]] — ép Z = 0
        box_5a = SurroundingRectangle(math_5a[2], color=TEAL, buff=0.1).set_z_index(25)
        self.add_fixed_in_frame_mobjects(box_5a)
        self.remove(box_5a)
        self.play(Create(box_5a))

        crush_z = np.array([[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 0]])
        self.play(ApplyMatrix(crush_z, sphere), run_time=3)
        self.wait(1)

        # Trả camera phẳng để thấy kết quả 2D
        self.move_camera(phi=10 * DEGREES, theta=-90 * DEGREES, run_time=2)

        result_5a = Text("→ Hình cầu 3D bị ép phẳng thành hình tròn 2D!", font_size=18, color=GREEN)
        result_5a.next_to(math_5a, DOWN, buff=0.15).set_z_index(25)
        self.add_fixed_in_frame_mobjects(result_5a)
        self.remove(result_5a)
        self.play(FadeIn(result_5a))
        self.wait(2)

        # Dọn dẹp 5a
        self.play(FadeOut(sphere, subtitle_5a, math_5a, box_5a, result_5a))
        self.wait(0.5)

        # ==========================================
        # STEP 5b: I_{3×2} — Không gian 2D → 3D (Thêm chiều Z = 0)
        # ==========================================
        subtitle_5b = Text("I₃ₓ₂ : Không gian 2D → 3D (Thêm chiều Z = 0)", font_size=20, color=MAROON_B)
        subtitle_5b.next_to(frame_box, DOWN, buff=0.25).set_z_index(25)
        self.add_fixed_in_frame_mobjects(subtitle_5b)
        self.remove(subtitle_5b)

        math_5b = MathTex(
            r"I_{3 \times 2}", "=",
            r"\begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0 & 0 \end{bmatrix}",
            font_size=38
        ).next_to(subtitle_5b, DOWN, buff=0.2).set_z_index(25)
        math_5b[0].set_color(MAROON_B)
        self.add_fixed_in_frame_mobjects(math_5b)
        self.remove(math_5b)

        # Bắt đầu từ nhìn thẳng (2D) — hình tròn phẳng
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=1)

        flat_circle = Circle(radius=1.2, color=YELLOW, fill_opacity=0.3)
        flat_circle.set_stroke(YELLOW_A, width=1)
        flat_circle.move_to(np.array([0, -0.5, 0]))

        self.play(Create(flat_circle))
        self.play(FadeIn(subtitle_5b), FadeIn(math_5b))
        self.wait(1)

        # Highlight ma trận
        box_5b = SurroundingRectangle(math_5b[2], color=MAROON_B, buff=0.04).set_z_index(25)
        self.add_fixed_in_frame_mobjects(box_5b)
        self.remove(box_5b)
        self.play(Create(box_5b))
        # "Nhúng" vào 3D bằng cách xoay camera → lộ trục Z
        embed_label = Text("→ Hình tròn 2D được nhúng vào không gian 3D (z = 0)", font_size=18, color=GREEN)
        embed_label.next_to(frame_box, DOWN, buff=0.15).set_z_index(25)
        self.add_fixed_in_frame_mobjects(embed_label)
        self.remove(embed_label)

        self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, run_time=3)
        self.wait(1)
        self.play(FadeOut(subtitle_5b, math_5b, box_5b))
        self.play(FadeIn(embed_label))
        self.wait(2)

        # Dọn dẹp 5b
        self.play(FadeOut(embed_label))
        self.play(FadeOut(axes, flat_circle))
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=1)

        # --- Kết luận Step 5 ---
        conclude = Text("→ Đây được gọi là Ma trận Hiệu chỉnh chiều", font_size=28, color=GOLD)
        conclude.set_z_index(25)
        self.add_fixed_in_frame_mobjects(conclude)
        self.play(Write(conclude))
        self.wait(2)
        self.play(FadeOut(conclude, frame_box, masks, title))


# ==============================================================================
# SCENE 2_SIGMA: Steps 6-7 (Diagonal Matrix + Kết hợp → Sigma)
# ==============================================================================
class Scene2_Sigma(MovingCameraScene):
    def construct(self):
        self.camera.frame.shift(np.array([0, -0.5, 0]))
        center_y = -1.5

        # ------------------------------------------
        # STEP 6: MA TRẬN ĐƯỜNG CHÉO KÉO GIÃN (2D Demo)
        # ------------------------------------------
        frame_box = Rectangle(width=13, height=4.5, color=WHITE, stroke_width=2).move_to(ORIGIN)
        frame_box.set_z_index(11)

        mask_top    = Rectangle(width=30, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, UP, buff=0)
        mask_bottom = Rectangle(width=30, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, DOWN, buff=0)
        mask_left   = Rectangle(width=10, height=4.5, color=BLACK, fill_opacity=1).next_to(frame_box, LEFT, buff=0)
        mask_right  = Rectangle(width=10, height=4.5, color=BLACK, fill_opacity=1).next_to(frame_box, RIGHT, buff=0)
        masks = VGroup(mask_top, mask_bottom, mask_left, mask_right).set_z_index(10)

        title_diag = Text("Ma trận Đường chéo — Kéo giãn theo trục", font_size=26, color=GOLD)
        title_diag.next_to(frame_box, UP, buff=0.15).set_z_index(12)

        # --- Vùng hình học (thu nhỏ 0.5x để sau khi giãn [[2,0],[0,3]] vẫn nằm trong khung) ---
        plane = NumberPlane(
            x_range=[-8, 8], y_range=[-8, 8],
            background_line_style={"stroke_opacity": 0.4}
        )
        unit_circle = Circle(radius=1, color=YELLOW, fill_opacity=0.3)
        basis_e1 = Vector(RIGHT, color=GREEN)
        basis_e2 = Vector(UP, color=RED)
        geometry = VGroup(plane, unit_circle, basis_e1, basis_e2)
        geometry.scale(0.5)

        # --- Ma trận D bên dưới khung ---
        math_D = MathTex(
            "D", "=",
            r"\begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}",
            font_size=48
        ).move_to(np.array([0, -3.8, 0])).set_z_index(12)
        math_D[0].set_color(ORANGE)

        self.play(FadeIn(frame_box, masks), Write(title_diag))
        self.play(FadeIn(geometry))
        self.play(FadeIn(math_D))
        self.wait(1)

        # Áp dụng D = [[2,0],[0,3]]
        D_matrix = np.array([[2, 0], [0, 3]])

        label_D = Text("Ox × 2,  Oy × 3", font_size=22, color=ORANGE)
        label_D.next_to(frame_box.get_corner(UL), DR, buff=0.2).set_z_index(12)
        box_D = SurroundingRectangle(math_D, color=ORANGE, buff=0.1).set_z_index(12)

        self.play(Write(label_D), Create(box_D))
        self.play(ApplyMatrix(D_matrix, geometry), run_time=3)
        self.wait(1)

        result_D = Text("Hình tròn đơn vị → Hình elip!", font_size=22, color=GREEN)
        result_D.next_to(frame_box.get_corner(UR), DL, buff=0.2).set_z_index(12)
        self.play(Write(result_D))
        self.wait(2)

        # Dọn dẹp step 6
        self.play(FadeOut(geometry, frame_box, masks, title_diag, math_D,
                          label_D, box_D, result_D))
        self.wait(0.5)

        # ------------------------------------------
        # STEP 7: KẾT HỢP → MA TRẬN SIGMA
        # ------------------------------------------
        title_sigma = Text("Kết hợp: Σ = Đường chéo × Hiệu chỉnh chiều", font_size=30, color=GOLD)
        title_sigma.move_to(np.array([0, center_y + 2.8, 0]))
        self.play(Write(title_sigma))

        # Phần derivation: tách từng thành phần để highlight
        sigma_eq = MathTex(r"\Sigma", "=", font_size=48)
        sigma_eq[0].set_color(YELLOW)
        mat_diag = MathTex(
            r"\begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}",
            font_size=48, color=ORANGE
        )
        mat_dim = MathTex(
            r"\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}",
            font_size=48, color=TEAL
        )

        derivation = VGroup(sigma_eq, mat_diag, mat_dim).arrange(RIGHT, buff=0.2)
        derivation.move_to(np.array([0, center_y + 0.8, 0]))

        self.play(FadeIn(derivation))
        self.wait(1)

        # Highlight từng thành phần (label căn giữa dưới ma trận tương ứng)
        box_diag = SurroundingRectangle(mat_diag, color=ORANGE, buff=0.05)
        label_diag = Text("Kéo giãn", font_size=15, color=ORANGE)
        label_diag.next_to(mat_diag, DOWN, buff=0.4)

        box_dim = SurroundingRectangle(mat_dim, color=TEAL, buff=0.05)
        label_dim = Text("Hiệu chỉnh chiều", font_size=15, color=TEAL)
        label_dim.next_to(mat_dim, DOWN, buff=0.4)

        self.play(Create(box_diag), FadeIn(label_diag))
        self.wait(0.8)
        self.play(Create(box_dim), FadeIn(label_dim))
        self.wait(1.5)

        self.play(FadeOut(box_diag, label_diag, box_dim, label_dim))

        # Biến đổi nhân ma trận → kết quả
        sigma_result = MathTex(
            r"\Sigma", "=",
            r"\begin{bmatrix} 2 & 0 & 0 \\ 0 & 3 & 0 \end{bmatrix}",
            font_size=54
        ).move_to(np.array([0, center_y + 0.8, 0]))
        sigma_result[0].set_color(YELLOW)

        self.play(Transform(derivation, sigma_result), run_time=2)
        self.wait(1)

        # Kết luận
        final_note1 = Text(
            "Σ vừa khử chiều (3D → 2D), vừa kéo giãn (Ox × 2, Oy × 3)",
            font_size=24, color=GREEN
        )
        final_note1.next_to(derivation, DOWN, buff=0.8)

        final_note2 = Text(
            "→ Đây chính là nhiệm vụ của Ma trận Σ trong phân rã SVD!",
            font_size=26, color=GOLD
        )
        final_note2.next_to(final_note1, DOWN, buff=0.5)

        self.play(Write(final_note1))
        self.wait(1)
        self.play(Write(final_note2))
        self.wait(4)