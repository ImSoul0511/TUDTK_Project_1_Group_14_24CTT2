import numpy as np
import math
from manim import *
from utils import matrix_transpose, matrix_multiply

A_mat = [[3, 2, 2], [2, 3, -2]]
At_mat = matrix_transpose(A_mat)

B_mat = matrix_multiply(A_mat, At_mat)
C_mat = matrix_multiply(At_mat, A_mat)

SQRT2  = math.sqrt(2)
SQRT18 = math.sqrt(18)

U_mat_num = [
    [1 / SQRT2, -1 / SQRT2],
    [1 / SQRT2,  1 / SQRT2],
]
Sig_mat_num = [
    [5.0, 0.0, 0.0],
    [0.0, 3.0, 0.0],
]
Vt_mat_num = [
    [ 1 / SQRT2,   1 / SQRT2,  0.0        ],
    [-1 / SQRT18,  1 / SQRT18, -4 / SQRT18],
    [ 2 / 3,      -2 / 3,      -1 / 3     ],
]

U_tex = [
    [r"\frac{1}{\sqrt{2}}", r"-\frac{1}{\sqrt{2}}"],
    [r"\frac{1}{\sqrt{2}}",  r"\frac{1}{\sqrt{2}}"],
]
Sig_tex = [
    [r"5", r"0", r"0"],
    [r"0", r"3", r"0"],
]
Vt_tex = [
    [r"\frac{1}{\sqrt{2}}",   r"\frac{1}{\sqrt{2}}",   r"0"],
    [r"-\frac{1}{\sqrt{18}}", r"\frac{1}{\sqrt{18}}",  r"-\frac{4}{\sqrt{18}}"],
    [r"\frac{2}{3}",          r"-\frac{2}{3}",          r"-\frac{1}{3}"],
]
A_tex = [
    [r"3", r"2",  r"2"],
    [r"2", r"3", r"-2"],
]
D_tex = [
    [r"5", r"0"],
    [r"0", r"3"],
]
I_rect_tex = [
    [r"1", r"0", r"0"],
    [r"0", r"1", r"0"],
]

Vt_pad = np.array(Vt_mat_num, dtype=float)

I_rect_pad = np.diag([1.0, 1.0, 0.0])

D_pad = np.diag([5.0, 3.0, 1.0])

U_pad = np.array([
    [U_mat_num[0][0], U_mat_num[0][1], 0.0],
    [U_mat_num[1][0], U_mat_num[1][1], 0.0],
    [0.0,             0.0,             1.0],
], dtype=float)

A_pad = np.array([
    [A_mat[0][0], A_mat[0][1], A_mat[0][2]],
    [A_mat[1][0], A_mat[1][1], A_mat[1][2]],
    [0.0,         0.0,         0.0        ],
], dtype=float)


def bmatrix(entries):
    """Render a LaTeX bmatrix from a list of list of LaTeX strings."""
    rows = r" \\ ".join(" & ".join(row) for row in entries)
    return r"\begin{bmatrix} " + rows + r" \end{bmatrix}"


def create_rainbow_cube(size=1.0, subdivisions=3, opacity=0.55):
    """
    Tạo cube đa sắc gồm 6 mặt, mỗi mặt chia subdivisions x subdivisions ô.
    Mỗi ô là một Polygon 3D có màu khác nhau.
    """
    palette = [BLUE_B, TEAL_B, GREEN_B, YELLOW_B, ORANGE, RED_B, PINK, PURPLE_B]
    step = size / subdivisions
    half = size / 2.0
    cells = VGroup()
    ci = 0

    face_defs = [
        (2, +half, 0, 1),  
        (2, -half, 0, 1),  
        (1, +half, 0, 2),  
        (1, -half, 0, 2), 
        (0, +half, 1, 2), 
        (0, -half, 1, 2), 
    ]

    for fixed_ax, fixed_val, ax1, ax2 in face_defs:
        for i in range(subdivisions):
            for j in range(subdivisions):
                colour = palette[ci % len(palette)]
                ci += 1

                centre = np.zeros(3)
                centre[fixed_ax] = fixed_val
                centre[ax1] = -half + step * (i + 0.5)
                centre[ax2] = -half + step * (j + 0.5)

                d1 = np.zeros(3); d1[ax1] = step / 2
                d2 = np.zeros(3); d2[ax2] = step / 2

                poly = Polygon(
                    centre - d1 - d2,
                    centre + d1 - d2,
                    centre + d1 + d2,
                    centre - d1 + d2,
                    fill_color=colour, fill_opacity=opacity,
                    stroke_color=colour, stroke_width=0.5, stroke_opacity=0.4,
                )
                cells.add(poly)

    return cells


def svd_arrow(direction, scale=1.5, color=WHITE):
    d = direction / np.linalg.norm(direction) * scale
    return Arrow3D(start=ORIGIN, end=d, color=color, resolution=8)

class Scene_9(Scene):
    """
    Giải thích thuật toán phân rã SVD từng bước
    """
    def construct(self):
        title = Text("Chi tiết thuật toán: Phân rã SVD", font_size=36, color=GOLD)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(2)

        mat_A = MathTex(
            r"A = \begin{bmatrix} 3 & 2 & 2 \\ 2 & 3 & -2 \end{bmatrix}"
        ).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(mat_A, shift=DOWN))
        self.wait(2)

        step1_title = Text("Bước 1: Tìm ma trận vuông đối xứng", font_size=24, color=TEAL)
        step1_title.next_to(mat_A, DOWN, buff=0.5)

        step1_eq1 = MathTex(
            r"AA^T = \begin{bmatrix} 17 & 8 \\ 8 & 17 \end{bmatrix}", font_size=32
        )
        step1_eq2 = MathTex(
            r"A^TA = \begin{bmatrix} 13 & 12 & 2 \\ 12 & 13 & -2 \\ 2 & -2 & 8 \end{bmatrix}", font_size=32
        )
        
        step1_group = VGroup(step1_eq1, step1_eq2).arrange(DOWN, buff=0.4)
        step1_group.next_to(step1_title, DOWN, buff=0.3)

        self.play(Write(step1_title))
        self.play(FadeIn(step1_group))
        self.wait(3)

        self.play(FadeOut(step1_title, step1_group))
        
        step2_title = Text("Bước 2: Tìm Trị riêng của hình dạng bé hơn (AAᵀ)", font_size=24, color=TEAL)
        step2_title.next_to(mat_A, DOWN, buff=0.5)

        step2_eq1 = MathTex(r"\det(AA^T - \lambda I) = 0", font_size=32)
        step2_res = MathTex(r"\Rightarrow \lambda_1 = 25,\ \lambda_2 = 9", font_size=36, color=YELLOW)
        
        step2_group = VGroup(step2_eq1, step2_res).arrange(DOWN, buff=0.4)
        step2_group.next_to(step2_title, DOWN, buff=0.3)

        self.play(Write(step2_title))
        self.play(FadeIn(step2_eq1))
        self.wait(1.5)
        self.play(FadeIn(step2_res, scale=1.1))
        self.wait(3)

        self.play(FadeOut(step2_title, step2_group))

        step3_title = Text("Bước 3: Suy ra Giá trị kỳ dị (Singular Values)", font_size=24, color=TEAL)
        step3_title.next_to(mat_A, DOWN, buff=0.5)
        
        step3_eq = MathTex(r"\sigma_i = \sqrt{\lambda_i} \Rightarrow \sigma_1 = 5,\ \sigma_2 = 3", font_size=32, color=GOLD)
        mat_Sigma = MathTex(r"\Sigma = \begin{bmatrix} 5 & 0 & 0 \\ 0 & 3 & 0 \end{bmatrix}", font_size=36)
        
        step3_group = VGroup(step3_eq, mat_Sigma).arrange(DOWN, buff=0.4)
        step3_group.next_to(step3_title, DOWN, buff=0.3)

        self.play(Write(step3_title))
        self.play(FadeIn(step3_eq))
        self.wait(1.5)
        self.play(FadeIn(mat_Sigma))
        self.wait(3)

        self.play(FadeOut(step3_title, step3_group))

        step4_title = Text("Bước 4: Tính vector riêng V từ AᵀA, và suy ra U", font_size=24, color=TEAL)
        step4_title.next_to(mat_A, DOWN, buff=0.4)
        self.play(Write(step4_title))

        v1_math = MathTex(r"v_1 = \begin{bmatrix} " + Vt_tex[0][0] + r" \\ " + Vt_tex[0][1] + r" \\ " + Vt_tex[0][2] + r" \end{bmatrix}", font_size=28)
        v2_math = MathTex(r"v_2 = \begin{bmatrix} " + Vt_tex[1][0] + r" \\ " + Vt_tex[1][1] + r" \\ " + Vt_tex[1][2] + r" \end{bmatrix}", font_size=28)
        v3_math = MathTex(r"v_3 = \begin{bmatrix} " + Vt_tex[2][0] + r" \\ " + Vt_tex[2][1] + r" \\ " + Vt_tex[2][2] + r" \end{bmatrix}", font_size=28)
        
        vectors_group = VGroup(v1_math, v2_math, v3_math).arrange(RIGHT, buff=0.5)
        vectors_group.next_to(step4_title, DOWN, buff=0.2)
        
        self.play(FadeIn(vectors_group, shift=UP))
        self.wait(2)

        V_tex = [
            [Vt_tex[0][0], Vt_tex[1][0], Vt_tex[2][0]],
            [Vt_tex[0][1], Vt_tex[1][1], Vt_tex[2][1]],
            [Vt_tex[0][2], Vt_tex[1][2], Vt_tex[2][2]],
        ]
        mat_V = MathTex(r"V = \begin{bmatrix} v_1 & v_2 & v_3 \end{bmatrix} = " + bmatrix(V_tex), font_size=32, color=ORANGE)
        mat_V.next_to(step4_title, DOWN, buff=0.2)
        
        self.play(ReplacementTransform(vectors_group, mat_V))
        self.wait(2)

        mat_Vt = MathTex(r"V^T = " + bmatrix(Vt_tex), font_size=32, color=RED)
        mat_Vt.next_to(step4_title, DOWN, buff=0.2)
        
        self.play(ReplacementTransform(mat_V, mat_Vt))
        self.wait(2)

        mat_U_eq_text = Text("Dùng công thức: ", font_size=24, color=YELLOW)
        mat_U_eq_math = MathTex(r"u_i = \frac{1}{\sigma_i} A v_i", font_size=32, color=YELLOW)
        mat_U_eq = VGroup(mat_U_eq_text, mat_U_eq_math).arrange(RIGHT, buff=0.2)
        mat_U = MathTex(r"U = " + bmatrix(U_tex), font_size=32, color=BLUE)
        
        step4_u_group = VGroup(mat_U_eq, mat_U).arrange(DOWN, buff=0.4)
        step4_u_group.next_to(mat_Vt, DOWN, buff=0.3)

        self.play(FadeIn(mat_U_eq))
        self.wait(1.5)
        self.play(FadeIn(mat_U))
        self.wait(4)

        self.play(FadeOut(step4_title, mat_Vt, step4_u_group))

        final_eq = MathTex(r"A = U \cdot \Sigma \cdot V^T", font_size=44)
        final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.2)
        final_group = VGroup(final_eq, final_box).next_to(mat_A, DOWN, buff=1.0)

        self.play(Write(final_eq))
        self.play(Create(final_box))
        self.wait(3)

        self.play(FadeOut(final_group))

        explicit_eq = MathTex(
            r"A = ", bmatrix(U_tex), bmatrix(Sig_tex), bmatrix(Vt_tex),
            font_size=40
        )
        explicit_eq[1].set_color(BLUE)
        explicit_eq[2].set_color(YELLOW)
        explicit_eq[3].set_color(RED)
        explicit_eq.next_to(mat_A, DOWN, buff=1.0)

        self.play(FadeIn(explicit_eq, shift=UP))
        self.wait(5)

        self.play(FadeOut(title, mat_A, explicit_eq))
        self.wait(2)

class Scene_10(ThreeDScene):
    """
    Trực quan hóa thuật toán SVD 3D
    """
    def construct(self):
        intro_title = Text("Trực quan hóa với ví dụ mẫu:", font_size=32, color=GOLD)
        intro_matrix = MathTex(
            r"A = " + bmatrix(A_tex),
            font_size=48
        )
        intro_group = VGroup(intro_title, intro_matrix).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        
        self.play(Write(intro_title))
        self.play(FadeIn(intro_matrix, shift=UP))
        self.wait(2)
        self.play(FadeOut(intro_group))

        self.move_camera(frame_center=ORIGIN)

        frame_box = (
            Rectangle(width=12, height=5, color=WHITE, stroke_width=2)
            .move_to(ORIGIN)
            .set_z_index(20)
        )
        masks = VGroup(
            Rectangle(width=32, height=10, color=BLACK, fill_opacity=1)
                .next_to(frame_box, UP, buff=0),
            Rectangle(width=32, height=10, color=BLACK, fill_opacity=1)
                .next_to(frame_box, DOWN, buff=0),
            Rectangle(width=10, height=6, color=BLACK, fill_opacity=1)
                .next_to(frame_box, LEFT, buff=0),
            Rectangle(width=10, height=6, color=BLACK, fill_opacity=1)
                .next_to(frame_box, RIGHT, buff=0),
        ).set_z_index(15)

        self.add_fixed_in_frame_mobjects(frame_box, masks)

        axes = ThreeDAxes(
            x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4],
            axis_config={"stroke_width": 2},
        ).move_to(ORIGIN)
        origin = axes.get_origin()

        def _fix(mob):
            self.add_fixed_in_frame_mobjects(mob)
            self.remove(mob)
            return mob

        def title_text(content, color=WHITE, fs=17):
            t = Text(content, font_size=fs, color=color).set_z_index(25)
            t.next_to(frame_box, UP, buff=0.15)
            return _fix(t)

        def bottom_mob(mob):
            mob.next_to(frame_box, DOWN, buff=0.18).set_z_index(25)
            return _fix(mob)

        svd_eq = MathTex(
            bmatrix(A_tex), "=",
            bmatrix(U_tex),
            bmatrix(Sig_tex),
            bmatrix(Vt_tex),
            font_size=22,
        )
        svd_eq[2].set_color(BLUE)    # U
        svd_eq[3].set_color(YELLOW)  # Σ
        svd_eq[4].set_color(RED)     # V^T
        bottom_mob(svd_eq)

        t1 = title_text("Phân rã SVD trực quan: A = U · Σ · Vᵀ", GOLD, 21)

        cube = create_rainbow_cube(size=0.5, subdivisions=3, opacity=0.55)
        cube.move_to(origin)

        self.move_camera(phi=65 * DEGREES, theta=45 * DEGREES, run_time=0.1)
        self.play(
            FadeIn(frame_box, masks),
            Write(t1),
            Create(axes),
            FadeIn(cube),
            run_time=1.5,
        )
        self.play(FadeIn(svd_eq), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(t1, svd_eq), run_time=0.4)

        t1b = title_text("Ảnh hưởng trực tiếp của A lên không gian", GOLD, 19)

        bot_a_mat = MathTex(
            r"A = ", bmatrix(A_tex), font_size=22, color=YELLOW,
        )
        bottom_mob(bot_a_mat)

        self.play(FadeIn(t1b, bot_a_mat), run_time=0.6)
        self.wait(0.5)

        self.play(ApplyMatrix(A_pad, cube), run_time=3)
        self.wait(1)

        cube_A_result = cube.copy()

        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=2)
        self.wait(1.5)

        t1b_result = title_text("→ A biến hình hộp 3D thành hình dẹt trên mặt phẳng 2D", GREEN, 17)
        self.play(FadeOut(t1b), FadeIn(t1b_result), run_time=0.5)
        self.wait(2)

        self.play(FadeOut(t1b_result, bot_a_mat, cube), run_time=0.6)

        cube = create_rainbow_cube(size=0.5, subdivisions=3, opacity=0.55)
        cube.move_to(origin)

        self.move_camera(phi=65 * DEGREES, theta=45 * DEGREES, run_time=1.5)

        t_svd_intro = title_text(
            "Bây giờ hãy phân rã A = U · Σ · Vᵀ theo từng bước", GOLD, 19
        )
        self.play(FadeIn(cube), FadeIn(t_svd_intro), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(t_svd_intro), run_time=0.4)

        t2 = title_text("Bước 1: Vᵀ — Quay các vector kì dị phải về cơ sở chuẩn", RED, 17)

        bot_vt_mat  = MathTex(r"V^T = ", bmatrix(Vt_tex), font_size=22, color=RED)
        bot_vt_desc = Text(
            "Quay các vector kì dị phải\nvề cơ sở chuẩn",
            font_size=14, color=RED_B, line_spacing=0.6,
        )
        bot_vt = VGroup(bot_vt_mat, bot_vt_desc).arrange(RIGHT, buff=0.5)
        bottom_mob(bot_vt)

        self.play(FadeIn(t2, bot_vt), run_time=0.6)

        v_colors = [RED_B, GREEN_B, BLUE_B]
        rs_arrows = VGroup(*[
            svd_arrow(np.array(Vt_mat_num[i], dtype=float), scale=1.6, color=v_colors[i])
            for i in range(3)
        ]).shift(origin)

        self.play(Create(rs_arrows), run_time=1)
        self.wait(0.5)

        self.play(
            ApplyMatrix(Vt_pad, cube),
            ApplyMatrix(Vt_pad, rs_arrows),
            run_time=3,
        )
        self.wait(1.5)
        self.play(FadeOut(rs_arrows), run_time=0.4)

        self.play(FadeOut(t2, bot_vt), run_time=0.4)

        sig_full = MathTex(
            r"\Sigma", "=", bmatrix(Sig_tex),
            font_size=22, color=YELLOW
        )
        bottom_mob(sig_full)

        t3_intro = title_text(
            "Bước 2: Σ — Kết hợp hiệu chỉnh chiều và kéo giãn", YELLOW, 17
        )
        self.play(FadeIn(t3_intro, sig_full), run_time=0.6)
        self.wait(1.5)

        sig_decomp = MathTex(
            r"\Sigma", "=", "{}",
            bmatrix(D_tex),
            r"\cdot",
            bmatrix(I_rect_tex),
            font_size=22,
        ).set_z_index(25)
        sig_decomp[0].set_color(YELLOW)
        sig_decomp[3].set_color(YELLOW)
        sig_decomp[5].set_color(TEAL)
        
        sig_decomp.next_to(frame_box, DOWN, buff=0.18)
        self.add_fixed_in_frame_mobjects(sig_decomp)
        self.remove(sig_decomp) 

        self.play(
            FadeOut(t3_intro), 
            FadeOut(sig_full),
            FadeIn(sig_decomp),
            run_time=1.5
        )


        self.wait(0.5)

        t3a = title_text(
            "Bước 2a: I₂ₓ₃ — Loại bỏ chiều dư (R³ → R²)", TEAL, 17
        )
        self.play(FadeIn(t3a), run_time=0.6)

        hl_irec = SurroundingRectangle(
            sig_decomp[5], color=TEAL, buff=0.08
        ).set_z_index(25)   
        _fix(hl_irec)
        self.play(Create(hl_irec), run_time=0.4)

        self.play(ApplyMatrix(I_rect_pad, cube), run_time=2)
        self.wait(0.5)

        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=2.5)
        self.wait(1)

        self.play(FadeOut(hl_irec), run_time=0.3)

        self.play(FadeOut(t3a), run_time=0.3)

        t3b = title_text(
            "Bước 2b: D = diag(5, 3) — Kéo giãn theo giá trị kì dị", YELLOW, 17
        )

        hl_d = SurroundingRectangle(
            sig_decomp[3], color=YELLOW, buff=0.08
        ).set_z_index(25)
        _fix(hl_d)

        self.play(FadeIn(t3b), Create(hl_d), run_time=0.5)

        self.play(ApplyMatrix(D_pad, cube), run_time=2.5)
        self.wait(1)

        self.play(FadeOut(t3b, sig_decomp, hl_d), run_time=0.4)

        t4 = title_text(
            "Bước 3: U — Quay không gian 2D theo các vector kì dị trái", BLUE, 17
        )

        bot_u_mat  = MathTex(r"U = ", bmatrix(U_tex), font_size=22, color=BLUE)
        bot_u_desc = Text(
            "Quay không gian 2D\ntheo các vector kì dị trái",
            font_size=14, color=BLUE_B, line_spacing=0.6,
        )
        bot_u = VGroup(bot_u_mat, bot_u_desc).arrange(RIGHT, buff=0.5)
        bottom_mob(bot_u)

        self.play(FadeIn(t4, bot_u), run_time=0.6)

        ls_arrows = VGroup(
            svd_arrow(
                np.array([U_mat_num[0][0], U_mat_num[1][0], 0.0]),
                scale=1.8, color=BLUE_B,
            ),
            svd_arrow(
                np.array([U_mat_num[0][1], U_mat_num[1][1], 0.0]),
                scale=1.8, color=TEAL_B,
            ),
        ).shift(origin)

        self.play(Create(ls_arrows), run_time=0.8)

        self.play(
            ApplyMatrix(U_pad, cube),
            ApplyMatrix(U_pad, ls_arrows),
            run_time=2.5,
        )
        self.wait(1)
        self.play(FadeOut(ls_arrows), run_time=0.4)

        self.play(FadeOut(t4, bot_u), run_time=0.4)

        t5 = title_text(
            "Kết luận: Ảnh hưởng của A  ≡  U · Σ · Vᵀ", GREEN, 19
        )

        self.play(
            axes.animate.shift(RIGHT * 3),
            cube.animate.shift(RIGHT * 3),
            FadeIn(t5),
            run_time=1.5,
        )

        axes_left = ThreeDAxes(
            x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4],
            axis_config={"stroke_width": 2},
        ).shift(LEFT * 3)

        cube_A_display = cube_A_result.copy().shift(LEFT * 3)

        self.play(FadeIn(axes_left, cube_A_display), run_time=1)

        lbl_a = Text("Ảnh hưởng của A", font_size=18, color=YELLOW).set_z_index(25)
        lbl_a.move_to(LEFT * 3 + DOWN * 2.7)
        _fix(lbl_a)

        lbl_svd = Text("Ảnh hưởng của U·Σ·Vᵀ", font_size=18, color=TEAL).set_z_index(25)
        lbl_svd.move_to(RIGHT * 3 + DOWN * 2.7)
        _fix(lbl_svd)

        eq_sign = MathTex(r"\equiv", font_size=48, color=GREEN).set_z_index(25)
        eq_sign.move_to(ORIGIN + DOWN * 0.3)
        _fix(eq_sign)

        self.play(FadeIn(lbl_a, lbl_svd, eq_sign), run_time=0.8)
        self.wait(4)

        self.play(
            FadeOut(cube, axes, axes_left, cube_A_display,
                    frame_box, masks, lbl_a, lbl_svd, eq_sign, t5),
            run_time=1.5,
        )
        self.wait(0.5)


class Scene_11(Scene):
    """
    Tổng kết toàn bộ thuật toán SVD
    """
    def construct(self):
        title = Text("Tổng kết về phân rã SVD", font_size=40, color=GOLD)
        title.to_edge(UP, buff=0.8)

        intro_txt = (
            "Như vậy, từ bất kỳ ma trận ban đầu nào, ta có thể tách nó thành 3 ma trận\n"
            "có các ảnh hưởng đặc biệt lên không gian:"
        )
        intro = Text(intro_txt, font_size=20, line_spacing=1.2).next_to(title, DOWN, buff=1)

        
        v_part = VGroup(
            Text("- Ma trận ", font_size=20),
            MathTex("V^T", color=RED, font_size=38),
            Text(": xoay các vector riêng về cơ sở chuẩn của không gian.", font_size=20)
        ).arrange(RIGHT, buff=0.1)

        s_part = VGroup(
            Text("- Ma trận ", font_size=20),
            MathTex(r"\Sigma", color=YELLOW, font_size=38),
            Text(": hiệu chỉnh chiều và kéo giãn theo các trục chính.", font_size=20)
        ).arrange(RIGHT, buff=0.1)

        u_part = VGroup(
            Text("- Ma trận ", font_size=20),
            MathTex("U", color=BLUE, font_size=38),
            Text(": xoay không gian về lại theo hướng của vector riêng.", font_size=20)
        ).arrange(RIGHT, buff=0.1)

        summary_bullets = VGroup(v_part, s_part, u_part).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        summary_bullets.next_to(intro, DOWN, buff=1)

        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(intro, shift=UP))
        self.wait(1)

        for part in summary_bullets:
            self.play(FadeIn(part, shift=RIGHT))
            self.wait(2)

        self.wait(3)
        
        self.play(FadeOut(VGroup(title, intro, summary_bullets)))
        self.wait(1)

