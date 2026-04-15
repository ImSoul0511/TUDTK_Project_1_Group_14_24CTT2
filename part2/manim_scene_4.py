import numpy as np
import math
from manim import *
from part2.utils import matrix_transpose, matrix_multiply

"""
Flow (Scene4_SVD — 1 scene duy nhất):
    Phase 1 : Hiển thị rainbow cube 3D + phương trình SVD đầy đủ A = U · Σ · V^T
    Phase 2 : Áp dụng V^T — quay right singular vectors về cơ sở chuẩn (3D)
    Phase 3 : Tách Σ = D · I_rect
      3a: Áp dụng I₂ₓ₃ (khử chiều R³→R²), camera → top-down 2D
      3b: Áp dụng D = diag(5, 3) (kéo giãn trong 2D)
    Phase 4 : Áp dụng U — quay kết quả trên mặt phẳng 2D
    Phase 5 : So sánh — kết quả ≡ A tác động trực tiếp
    Phase 6 : FadeOut

    Σ (2×3) = D (2×2) × I_rect (2×3)
    Trong đó:
        I_rect = [[1,0,0],[0,1,0]]  → khử chiều (R³ → R²)
        D      = [[5,0],[0,3]]      → kéo giãn

Render:
    manim -pql part2/manim_scene_4.py Scene4_SVD
"""

# ── Data Preparation ─────────────────────────────────────────────────────────
A_mat = [[3, 2, 2], [2, 3, -2]]
At_mat = matrix_transpose(A_mat)

B_mat = matrix_multiply(A_mat, At_mat)   # 2×2 symmetric
C_mat = matrix_multiply(At_mat, A_mat)   # 3×3 symmetric

SQRT2  = math.sqrt(2)
SQRT18 = math.sqrt(18)

# ── Numerical matrices ───────────────────────────────────────────────────────
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

# ── LaTeX entries ─────────────────────────────────────────────────────────────
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

# ── 3×3 padded matrices for ApplyMatrix ───────────────────────────────────────
Vt_pad = np.array(Vt_mat_num, dtype=float)

# I_rect (2×3) padded to 3×3: kills z-component
I_rect_pad = np.diag([1.0, 1.0, 0.0])

# D = diag(σ₁, σ₂) padded to 3×3: z already dead so z-scale = 1 (no effect)
D_pad = np.diag([5.0, 3.0, 1.0])

# U (2×2) padded to 3×3
U_pad = np.array([
    [U_mat_num[0][0], U_mat_num[0][1], 0.0],
    [U_mat_num[1][0], U_mat_num[1][1], 0.0],
    [0.0,             0.0,             1.0],
], dtype=float)

# A (2×3) padded to 3×3
A_pad = np.array([
    [A_mat[0][0], A_mat[0][1], A_mat[0][2]],
    [A_mat[1][0], A_mat[1][1], A_mat[1][2]],
    [0.0,         0.0,         0.0        ],
], dtype=float)


# ── Helper: build bmatrix LaTeX ───────────────────────────────────────────────
def bmatrix(entries):
    """Render a LaTeX bmatrix from a list of list of LaTeX strings."""
    rows = r" \\ ".join(" & ".join(row) for row in entries)
    return r"\begin{bmatrix} " + rows + r" \end{bmatrix}"


# ── Helper: create rainbow cube ───────────────────────────────────────────────
def create_rainbow_cube(size=1.0, subdivisions=3, opacity=0.55):
    """
    Tạo cube đa sắc gồm 6 mặt, mỗi mặt chia subdivisions×subdivisions ô.
    Mỗi ô là một Polygon 3D có màu khác nhau.
    """
    palette = [BLUE_B, TEAL_B, GREEN_B, YELLOW_B, ORANGE, RED_B, PINK, PURPLE_B]
    step = size / subdivisions
    half = size / 2.0
    cells = VGroup()
    ci = 0

    # 6 mặt: (trục cố định, giá trị, trục biến thiên 1, trục biến thiên 2)
    face_defs = [
        (2, +half, 0, 1),  # front  z=+half, vary x,y
        (2, -half, 0, 1),  # back   z=-half, vary x,y
        (1, +half, 0, 2),  # top    y=+half, vary x,z
        (1, -half, 0, 2),  # bottom y=-half, vary x,z
        (0, +half, 1, 2),  # right  x=+half, vary y,z
        (0, -half, 1, 2),  # left   x=-half, vary y,z
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


# ── Helper: Arrow3D from ORIGIN ───────────────────────────────────────────────
def svd_arrow(direction, scale=1.5, color=WHITE):
    d = direction / np.linalg.norm(direction) * scale
    return Arrow3D(start=ORIGIN, end=d, color=color, resolution=8)


# ==============================================================================
# SCENE 4_SVD
# ==============================================================================
class Scene4_SVD(ThreeDScene):
    def construct(self):
        # ── Title Slide ──────────────────────────────────────────────────────
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

        # ── Frame & masks (giống Scene3) ─────────────────────────────────────
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

        # ── 3D Axes ──────────────────────────────────────────────────────────
        axes = ThreeDAxes(
            x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4],
            axis_config={"stroke_width": 2},
        ).move_to(ORIGIN)
        origin = axes.get_origin()

        # ── Reusable fixed-in-frame helpers ──────────────────────────────────
        def _fix(mob):
            """Add to fixed-in-frame, remove from scene (to control appearance)."""
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

        # ── Pre-build SVD full equation ──────────────────────────────────────
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

        # ════════════════════════════════════════════════════════════════════
        # PHASE 1: Rainbow cube + phương trình SVD
        # ════════════════════════════════════════════════════════════════════
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

        # ════════════════════════════════════════════════════════════════════
        # PHASE 1b: Biến đổi trực tiếp qua A
        # ════════════════════════════════════════════════════════════════════
        self.play(FadeOut(t1, svd_eq), run_time=0.4)

        t1b = title_text("Ảnh hưởng trực tiếp của A lên không gian", GOLD, 19)

        # Ma trận A label ở dưới
        bot_a_mat = MathTex(
            r"A = ", bmatrix(A_tex), font_size=22, color=YELLOW,
        )
        bottom_mob(bot_a_mat)

        self.play(FadeIn(t1b, bot_a_mat), run_time=0.6)
        self.wait(0.5)

        # Áp dụng A trực tiếp → cube bị biến dạng + dẹt (A: 2×3 → triệt tiêu z)
        self.play(ApplyMatrix(A_pad, cube), run_time=3)
        self.wait(1)

        # Lưu bản sao cube đã biến dạng bởi A (để dùng so sánh cuối)
        cube_A_result = cube.copy()

        # Chuyển camera về 2D top-down khi hình đã dẹt
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=2)
        self.wait(1.5)

        # Kết luận ngắn
        t1b_result = title_text("→ A biến hình hộp 3D thành hình dẹt trên mặt phẳng 2D", GREEN, 17)
        self.play(FadeOut(t1b), FadeIn(t1b_result), run_time=0.5)
        self.wait(2)

        # Dọn dẹp cube biến dạng, tạo cube mới cho SVD breakdown
        self.play(FadeOut(t1b_result, bot_a_mat, cube), run_time=0.6)

        cube = create_rainbow_cube(size=0.5, subdivisions=3, opacity=0.55)
        cube.move_to(origin)

        # Reset camera về 3D cho phần SVD
        self.move_camera(phi=65 * DEGREES, theta=45 * DEGREES, run_time=1.5)

        t_svd_intro = title_text(
            "Bây giờ hãy phân rã A = U · Σ · Vᵀ theo từng bước", GOLD, 19
        )
        self.play(FadeIn(cube), FadeIn(t_svd_intro), run_time=0.8)
        self.wait(1.5)

        # ════════════════════════════════════════════════════════════════════
        # PHASE 2: V^T — Quay không gian 3D
        # ════════════════════════════════════════════════════════════════════
        self.play(FadeOut(t_svd_intro), run_time=0.4)

        t2 = title_text("Bước 1: Vᵀ — Quay các vector kì dị phải về cơ sở chuẩn", RED, 17)

        # V^T matrix + description at bottom
        bot_vt_mat  = MathTex(r"V^T = ", bmatrix(Vt_tex), font_size=22, color=RED)
        bot_vt_desc = Text(
            "Quay các vector kì dị phải\nvề cơ sở chuẩn",
            font_size=14, color=RED_B, line_spacing=0.6,
        )
        bot_vt = VGroup(bot_vt_mat, bot_vt_desc).arrange(RIGHT, buff=0.5)
        bottom_mob(bot_vt)

        self.play(FadeIn(t2, bot_vt), run_time=0.6)

        # Right singular vectors (hàng của V^T = cột của V)
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

        # ════════════════════════════════════════════════════════════════════
        # PHASE 3a: I₂ₓ₃ — Khử chiều R³ → R²
        # ════════════════════════════════════════════════════════════════════
        self.play(FadeOut(t2, bot_vt), run_time=0.4)

        # Hiển thị Sigma trước khi tách
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

        # Hiển thị phân tách: Σ = D · I_rect
        sig_decomp = MathTex(
            r"\Sigma", "=",
            bmatrix(D_tex),          # index 2 → D
            r"\cdot",
            bmatrix(I_rect_tex),     # index 4 → I_rect
            font_size=22,
        ).set_z_index(25)
        sig_decomp[0].set_color(YELLOW)
        sig_decomp[2].set_color(YELLOW)
        sig_decomp[4].set_color(TEAL)
        
        # Position it, but don't add to fixed_in_frame yet to avoid duplicate rendering/glitch
        sig_decomp.next_to(frame_box, DOWN, buff=0.18)

        self.play(
            FadeOut(t3_intro), 
            ReplacementTransform(sig_full, sig_decomp), 
            run_time=0.8
        )
        self.add_fixed_in_frame_mobjects(sig_decomp) # Ensure it's now fixed
        self.wait(0.5)

        t3a = title_text(
            "Bước 2a: I₂ₓ₃ — Loại bỏ chiều dư (R³ → R²)", TEAL, 17
        )
        self.play(FadeIn(t3a), run_time=0.6)

        # Highlight I_rect trong phương trình
        hl_irec = SurroundingRectangle(
            sig_decomp[4], color=TEAL, buff=0.08
        ).set_z_index(25)
        _fix(hl_irec)
        self.play(Create(hl_irec), run_time=0.4)

        # Áp dụng I_rect → triệt tiêu z
        self.play(ApplyMatrix(I_rect_pad, cube), run_time=2)
        self.wait(0.5)

        # Camera chuyển về top-down 2D
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=2.5)
        self.wait(1)

        self.play(FadeOut(hl_irec), run_time=0.3)

        # ════════════════════════════════════════════════════════════════════
        # PHASE 3b: D = diag(5, 3) — Kéo giãn trong 2D
        # ════════════════════════════════════════════════════════════════════
        self.play(FadeOut(t3a), run_time=0.3)

        t3b = title_text(
            "Bước 2b: D = diag(5, 3) — Kéo giãn theo giá trị kì dị", YELLOW, 17
        )

        # Highlight D trong phương trình
        hl_d = SurroundingRectangle(
            sig_decomp[2], color=YELLOW, buff=0.08
        ).set_z_index(25)
        _fix(hl_d)

        self.play(FadeIn(t3b), Create(hl_d), run_time=0.5)

        # Áp dụng D → kéo giãn x*5, y*3 (đã trong 2D view)
        self.play(ApplyMatrix(D_pad, cube), run_time=2.5)
        self.wait(1)

        self.play(FadeOut(t3b, sig_decomp, hl_d), run_time=0.4)

        # ════════════════════════════════════════════════════════════════════
        # PHASE 4: U — Quay trên mặt phẳng 2D
        # ════════════════════════════════════════════════════════════════════
        t4 = title_text(
            "Bước 3: U — Quay không gian 2D theo các vector kì dị trái", BLUE, 17
        )

        # U matrix + description at bottom
        bot_u_mat  = MathTex(r"U = ", bmatrix(U_tex), font_size=22, color=BLUE)
        bot_u_desc = Text(
            "Quay không gian 2D\ntheo các vector kì dị trái",
            font_size=14, color=BLUE_B, line_spacing=0.6,
        )
        bot_u = VGroup(bot_u_mat, bot_u_desc).arrange(RIGHT, buff=0.5)
        bottom_mob(bot_u)

        self.play(FadeIn(t4, bot_u), run_time=0.6)

        # Left singular vectors (cột của U)
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

        # ════════════════════════════════════════════════════════════════════
        # PHASE 5: So sánh side-by-side (giữ nguyên 2D, không xoay camera)
        # ════════════════════════════════════════════════════════════════════
        self.play(FadeOut(t4, bot_u), run_time=0.4)

        t5 = title_text(
            "Kết luận: Ảnh hưởng của A  ≡  U · Σ · Vᵀ", GREEN, 19
        )

        # Dời kết quả SVD (axes + cube) sang bên phải
        self.play(
            axes.animate.shift(RIGHT * 3),
            cube.animate.shift(RIGHT * 3),
            FadeIn(t5),
            run_time=1.5,
        )

        # Tạo trục bên trái + đặt bản sao cube đã biến dạng bởi A
        axes_left = ThreeDAxes(
            x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4],
            axis_config={"stroke_width": 2},
        ).shift(LEFT * 3)

        cube_A_display = cube_A_result.copy().shift(LEFT * 3)

        self.play(FadeIn(axes_left, cube_A_display), run_time=1)

        # Labels (fixed in frame)
        lbl_a = Text("Ảnh hưởng của A", font_size=18, color=YELLOW).set_z_index(25)
        lbl_a.move_to(LEFT * 3 + DOWN * 2.7)
        _fix(lbl_a)

        lbl_svd = Text("Ảnh hưởng của U·Σ·Vᵀ", font_size=18, color=TEAL).set_z_index(25)
        lbl_svd.move_to(RIGHT * 3 + DOWN * 2.7)
        _fix(lbl_svd)

        # Dấu bằng ở giữa
        eq_sign = MathTex(r"\equiv", font_size=48, color=GREEN).set_z_index(25)
        eq_sign.move_to(ORIGIN + DOWN * 0.3)
        _fix(eq_sign)

        self.play(FadeIn(lbl_a, lbl_svd, eq_sign), run_time=0.8)
        self.wait(4)

        # ════════════════════════════════════════════════════════════════════
        # PHASE 6: FadeOut
        # ════════════════════════════════════════════════════════════════════
        self.play(
            FadeOut(cube, axes, axes_left, cube_A_display,
                    frame_box, masks, lbl_a, lbl_svd, eq_sign, t5),
            run_time=1.5,
        )
        self.wait(0.5)