from numpy import ndarray
import numpy as np
from manim import *
from part2.utils import orthogonal_matrix, matrix_transpose, vector_normalize
from part2.diagonalization import eigen_decomposition

"""
Flow: 
    1. Từ đoạn kết của Scene2, ta đi tìm hiểu tính chất của ma trận đối xứng.
    2. Nhận xét: Các vector riêng của ma trận đối xứng luôn vuông góc với nhau.
    3. Không gian 3D, lấy ví dụ ma trận đối xứng 3x3 A = [[2,1,5],[1,3,1],[5,1,4]], sài hàm eigen_decomposition để tìm các trị riêng và các vector riêng tương ứng.
    4. Biểu diễn các vector riêng trên không gian 3D, nhận xét chúng vuông góc với nhau.
    5. Thực hiện trực chuẩn hóa các vector riêng để tạo thành ma trận trực giao Q - sử dụng hàm orthogonal_matrix trong utils.
    6. Từ đây ta thu được ma trận trực giao Q. Mà ảnh hưởng của ma trận trực giao là thực hiện phép quay lên không gian.
    7. Khi lấy ma trận trực giao Q tác động lên không gian, ta thấy các trục chuẩn của không gian được quay về trùng với các vector riêng của ma trận Q.
    (Biểu diễn ảnh hưởng của Q lên không gian).
    8. Khi lấy chuyển vị của Q tác động lên không gian, ta thấy các vector riêng được quay về trùng với các trục chuẩn.
    (Lấy Q^T bằng hàm matrix_transpose rồi biểu diễn ảnh hưởng của Q^T lên không gian).
    9. Nhận xét: Với một ma trận bất kỳ, khi ta nhân bản thân nó với chuyển vị của nó, ta thu được một ma trận đối xứng. 
    10. Suy ra: Việc nhân ma trận A ban đầu với A^T hoặc A^T với A, ta sẽ thu được một ma trận đối xứng có đầy đủ các tính chất mà ta đã đề cập.
Render order:
    manim -pql part2/manim_scene_3.py Scene3
    manim -pql part2/manim_scene_3.py Scene3_Rotation
    manim -pql part2/manim_scene_3.py Scene3_Conclusion
"""

# ---- Dữ liệu dùng chung ----
A_SYM = [[2.0, 1.0, 5.0],
          [1.0, 3.0, 1.0],
          [5.0, 1.0, 4.0]]

def _compute_eigen_data():
    """Tính toán eigenvalues, eigenvectors, Q, Q^T một lần."""
    eigenvalues, V = eigen_decomposition(A_SYM)
    # V trả về dạng cột: V[i][j] = phần tử (i, j) — cột j là vector riêng j
    n = len(eigenvalues)
    eigenvectors = [[V[i][j] for i in range(n)] for j in range(n)]
    
    # Trực chuẩn hóa → ma trận trực giao Q
    Q_rows = orthogonal_matrix(eigenvectors)  # mỗi hàng là 1 vector đã chuẩn hóa
    Q_T_rows = matrix_transpose(Q_rows)
    
    return eigenvalues, eigenvectors, Q_rows, Q_T_rows


def create_rainbow_cube(size=1.0, subdivisions=3, opacity=0.55):
    """Cube đa sắc: 6 mặt, mỗi mặt chia subdivisions×subdivisions ô."""
    palette = [BLUE_B, TEAL_B, GREEN_B, YELLOW_B, ORANGE, RED_B, PINK, PURPLE_B]
    step = size / subdivisions
    half = size / 2.0
    cells = VGroup()
    ci = 0
    for fixed_ax, fixed_val, ax1, ax2 in [
        (2, +half, 0, 1), (2, -half, 0, 1),
        (1, +half, 0, 2), (1, -half, 0, 2),
        (0, +half, 1, 2), (0, -half, 1, 2),
    ]:
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
                    centre - d1 - d2, centre + d1 - d2,
                    centre + d1 + d2, centre - d1 + d2,
                    fill_color=colour, fill_opacity=opacity,
                    stroke_color=colour, stroke_width=0.5, stroke_opacity=0.4,
                )
                cells.add(poly)
    return cells


# ==============================================================================
# SCENE 3: Steps 1–5 (Tính chất ma trận đối xứng + Eigenvectors 3D + Q)
# ==============================================================================
class Scene3(ThreeDScene):
    def construct(self):
        eigenvalues, eigenvectors, Q_rows, Q_T_rows = _compute_eigen_data()
        ev_np = [np.array(v, dtype=float) for v in eigenvectors]
        q_np = [np.array(vector_normalize(v), dtype=float) for v in eigenvectors]

        # --- Masks + Frame (fixed in frame) ---
        self.move_camera(frame_center=np.array([0, -0.5, 0]))
        frame_box = Rectangle(width=12, height=5, color=WHITE, stroke_width=2).move_to(ORIGIN)
        frame_box.set_z_index(20)

        mask_top   = Rectangle(width=32, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, UP, buff=0)
        mask_bot   = Rectangle(width=32, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, DOWN, buff=0)
        mask_left  = Rectangle(width=10, height=6,  color=BLACK, fill_opacity=1).next_to(frame_box, LEFT, buff=0)
        mask_right = Rectangle(width=10, height=6,  color=BLACK, fill_opacity=1).next_to(frame_box, RIGHT, buff=0)
        masks = VGroup(mask_top, mask_bot, mask_left, mask_right).set_z_index(15)

        # ──────────────────────────────────────────
        # STEP 1: Giới thiệu tính chất ma trận đối xứng
        # ──────────────────────────────────────────
        title = Text("Tính chất Ma trận Đối xứng", font_size=28, color=GOLD)
        title.next_to(frame_box, UP, buff=0.15).set_z_index(25)
        self.add_fixed_in_frame_mobjects(title)

        self.play(Write(title))

        # Hiển thị ma trận đối xứng A (2D overlay)
        mat_A = MathTex(
            "A", "=",
            r"\begin{bmatrix} 2 & 1 & 5 \\ 1 & 3 & 1 \\ 5 & 1 & 4 \end{bmatrix}",
            font_size=48
        ).set_z_index(25)
        mat_A[0].set_color(YELLOW)
        self.add_fixed_in_frame_mobjects(mat_A)
        self.remove(mat_A)

        sym_note = Text("A là ma trận đối xứng  (A = Aᵀ)", font_size=22, color=TEAL).set_z_index(25)
        sym_note.next_to(mat_A, DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(sym_note)
        self.remove(sym_note)

        self.play(FadeIn(mat_A, shift=UP))
        self.play(Write(sym_note))
        self.wait(2)

        # ──────────────────────────────────────────
        # STEP 2: Nhận xét — vector riêng vuông góc
        # ──────────────────────────────────────────
        prop_txt = Text(
            "Nhận xét: Các vector riêng của ma trận đối xứng\nluôn vuông góc với nhau!",
            font_size=22, color=GREEN, line_spacing=0.8
        ).set_z_index(25)
        prop_txt.next_to(sym_note, DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(prop_txt)
        self.remove(prop_txt)

        self.play(FadeIn(prop_txt, shift=UP))
        self.wait(2)

        # Dọn text 2D
        self.play(FadeOut(mat_A, sym_note, prop_txt))
        self.wait(0.5)

        # ──────────────────────────────────────────
        # STEP 3: Tìm eigenvalues & eigenvectors bằng eigen_decomposition
        # ──────────────────────────────────────────
        # Hiện kết quả eigen bằng text overlay
        self.add_fixed_in_frame_mobjects(frame_box, masks)
        self.play(FadeIn(frame_box, masks))
        

        subtitle_eigen = Text("Kết quả phân tích trị riêng (Jacobi):", font_size=20, color=GOLD).set_z_index(25)
        subtitle_eigen.next_to(frame_box, DOWN, buff=0.05)
        self.add_fixed_in_frame_mobjects(subtitle_eigen)
        self.remove(subtitle_eigen)

        eigen_lines = VGroup()
        ev_colors = [BLUE, GREEN, RED]
        for i in range(3):
            lam_val = f"{eigenvalues[i]:.2f}"
            vec_str = f"({ev_np[i][0]:.2f}, {ev_np[i][1]:.2f}, {ev_np[i][2]:.2f})"
            line = Text(f"λ{i+1} = {lam_val}    v{i+1} = {vec_str}", font_size=18, color=ev_colors[i])
            eigen_lines.add(line)
        eigen_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.1).set_z_index(25)
        eigen_lines.next_to(subtitle_eigen, DOWN, buff=0.25)

        for line in eigen_lines:
            self.add_fixed_in_frame_mobjects(line)
            self.remove(line)

        # Trục 3D
        axes = ThreeDAxes(
            x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4],
            axis_config={"stroke_width": 2}
        )
        axes.move_to(np.array([0, -0.3, 0]))

        self.move_camera(phi=65 * DEGREES, theta=40 * DEGREES, run_time=2)
        self.play(Create(axes))
        self.play(FadeIn(subtitle_eigen))
        self.wait(0.5)

        # ──────────────────────────────────────────
        # STEP 4: Biểu diễn vector riêng trên 3D
        # ──────────────────────────────────────────
        arrows = VGroup()
        for i in range(3):
            direction = ev_np[i] / np.linalg.norm(ev_np[i]) * 2.5  # scale để dễ nhìn
            arrow = Arrow3D(
                start=axes.get_origin(),
                end=axes.get_origin() + direction,
                color=ev_colors[i],
                resolution=8
            )
            arrows.add(arrow)

        for i, line in enumerate(eigen_lines):
            self.play(
                FadeIn(line, shift=UP),
                Create(arrows[i]),
                run_time=1
            )
            self.wait(0.5)
        self.wait(1)

        # Nhận xét vuông góc
        ortho_note = Text("→ Các vector riêng vuông góc với nhau!", font_size=20, color=GREEN).set_z_index(25)
        ortho_note.next_to(eigen_lines, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(ortho_note)
        self.remove(ortho_note)
        self.play(FadeIn(ortho_note))

        # Quay camera để thấy rõ hơn
        self.move_camera(phi=55 * DEGREES, theta=80 * DEGREES, run_time=3)
        self.wait(1)

        # Thêm kí hiệu vuông góc (Right angle markers)
        def get_3d_corner(v1, v2, origin, length=0.25):
            # v1, v2 are normalized directions
            u1 = v1 / np.linalg.norm(v1)
            u2 = v2 / np.linalg.norm(v2)
            p1 = origin + u1 * length
            p2 = origin + u2 * length
            p3 = origin + (u1 + u2) * length
            return VGroup(
                Line(p1, p3, color=WHITE, stroke_width=2),
                Line(p2, p3, color=WHITE, stroke_width=2)
            )

        origin = axes.get_origin()
        ra_markers = VGroup(
            get_3d_corner(ev_np[0], ev_np[1], origin),
            get_3d_corner(ev_np[1], ev_np[2], origin),
            get_3d_corner(ev_np[0], ev_np[2], origin)
        )

        # ---- HIỆU ỨNG ZOOM CẬN TỪNG CẶP ----
        # 1. Zoom vào origin
        self.move_camera(zoom=1.8, run_time=1.5)
        self.wait(0.5)

        # 2. Biểu diễn từng cặp một
        pair_labels = [
            "(v1, v2)",
            "(v2, v3)",
            "(v1, v3)"
        ]
        
        for i in range(3):
            # Tạo ghi chú tạm thời cho từng cặp (fixed in frame)
            pair_txt = Text(f"Cặp {pair_labels[i]}", font_size=20, color=GOLD).set_z_index(25)
            pair_txt.next_to(ortho_note, DOWN, buff=0.2)
            self.add_fixed_in_frame_mobjects(pair_txt)
            
            self.play(Create(ra_markers[i]), FadeIn(pair_txt, shift=UP))
            self.wait(1)
            self.play(FadeOut(pair_txt))

        self.wait(1)
        
        # 3. Zoom ra lại
        self.move_camera(zoom=1, run_time=1.5)
        self.wait(1)

        # ──────────────────────────────────────────
        # STEP 5: Trực chuẩn hóa → Ma trận trực giao Q
        # ──────────────────────────────────────────
        self.play(FadeOut(subtitle_eigen, eigen_lines, ortho_note, ra_markers))
        self.wait(0.5)

        # Tạo normalized arrows
        norm_arrows = VGroup()
        for i in range(3):
            direction = q_np[i] * 2.0
            n_arrow = Arrow3D(
                start=axes.get_origin(),
                end=axes.get_origin() + direction,
                color=ev_colors[i],
                resolution=8
            )
            norm_arrows.add(n_arrow)

        norm_label = Text("Trực chuẩn hóa (Normalize) các vector riêng:", font_size=20, color=TEAL).set_z_index(25)
        norm_label.next_to(frame_box, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(norm_label)
        self.remove(norm_label)
        self.play(FadeIn(norm_label))

        # Transform arrows → normalized arrows
        self.play(
            *[Transform(arrows[i], norm_arrows[i]) for i in range(3)],
            run_time=2
        )
        self.wait(1)

        # Hiển thị Q
        # Định dạng giá trị Q cho MathTex
        def fmt(x):
            return f"{x:.2f}"

        q_tex_str = (
            r"\begin{bmatrix} "
            + r" \\ ".join(
                " & ".join(fmt(Q_rows[i][j]) for j in range(3))
                for i in range(3)
            )
            + r" \end{bmatrix}"
        )
        q_label = MathTex("Q", "=", q_tex_str, font_size=36).set_z_index(25)
        q_label[0].set_color(BLUE)
        q_label.next_to(norm_label, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(q_label)
        self.remove(q_label)

        self.play(FadeIn(q_label, shift=UP))
        self.wait(1)

        q_prop = Text("Q là ma trận trực giao: Q · Qᵀ = I", font_size=20, color=GREEN).set_z_index(25)
        q_prop.next_to(q_label, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(q_prop)
        self.remove(q_prop)
        self.play(Write(q_prop))
        self.wait(1)

        q_effect = Text("→ Ảnh hưởng của ma trận trực giao: thực hiện phép QUAY không gian!", font_size=18, color=GOLD).set_z_index(25)
        q_effect.next_to(q_prop, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(q_effect)
        self.remove(q_effect)
        self.play(Write(q_effect))
        self.wait(3)

        # Dọn dẹp toàn bộ
        self.play(FadeOut(arrows, axes, norm_label, q_label, q_prop, q_effect, frame_box, masks, title))
        self.wait(0.5)


# ==============================================================================
# SCENE 3_Rotation: Steps 6–8 (Q quay không gian, Q^T quay ngược)
# ==============================================================================
class Scene3_Rotation(ThreeDScene):
    def construct(self):
        # 1. Chuẩn bị dữ liệu
        eigenvalues, eigenvectors, Q_rows, Q_T_rows = _compute_eigen_data()
        # Q_rows: các vector riêng đã chuẩn hóa (v1, v2, v3) theo hàng.
        v_np = [np.array(v) for v in Q_rows]
        
        # Q mat (cột là basis vectors)
        Q_mat = np.array(Q_rows).T
        # QT mat (hàng là basis vectors)
        QT_mat = np.array(Q_rows)

        # 2. Thiết lập khung hình & Masks
        self.move_camera(frame_center=np.array([0,0,-0.9]))
        frame_box = Rectangle(width=12, height=5, color=WHITE, stroke_width=2).move_to(ORIGIN).set_z_index(20)
        frame_box.shift([0, 0.9, 0])
        masks = VGroup(
            Rectangle(width=32, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, UP, buff=0),
            Rectangle(width=32, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, DOWN, buff=0),
            Rectangle(width=10, height=6, color=BLACK, fill_opacity=1).next_to(frame_box, LEFT, buff=0),
            Rectangle(width=10, height=6, color=BLACK, fill_opacity=1).next_to(frame_box, RIGHT, buff=0),
        ).set_z_index(15)
        self.add_fixed_in_frame_mobjects(frame_box, masks)

        axes = ThreeDAxes(axis_config={"stroke_width": 2}).move_to(ORIGIN)
        basis_colors = [RED, GREEN, BLUE]
        
        # ════════════════════════════════════════════════════════════════════
        # PHASE 1: Ảnh hưởng của Q (e_i -> v_i)
        # ════════════════════════════════════════════════════════════════════
        title = Text("Ảnh hưởng của Ma trận Trực giao Q", font_size=24, color=GOLD).set_z_index(25)
        title.next_to(frame_box, UP, buff=0.01) # Sát nóc nhất có thể
        self.add_fixed_in_frame_mobjects(title)

        # Standard basis e1, e2, e3
        e_vectors = VGroup(*[
            Arrow3D(start=axes.get_origin(), end=axes.c2p(*v), color=basis_colors[i], resolution=8)
            for i, v in enumerate([[1,0,0], [0,1,0], [0,0,1]])
        ])
        e_labels = VGroup(*[
            MathTex(f"e_{i+1}", font_size=24, color=basis_colors[i]).next_to(e_vectors[i].get_end(), UP+RIGHT, buff=0.1)
            for i in range(3)
        ])

        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES)
        self.play(FadeIn(frame_box, masks), Create(axes), Write(title))
        self.play(Create(e_vectors), Write(e_labels), run_time=1.5)
        self.wait(1)

        q_expl = Text("Ma trận Q xoay các trục chuẩn (eᵢ) về trùng với các vector riêng (vᵢ)", font_size=18, color=BLUE).set_z_index(25)
        q_expl.next_to(frame_box, DOWN, buff=0.25)
        
        # Matrix Q view (columns)
        q_mat_viz = MathTex(r"Q = \begin{bmatrix} | & | & | \\ v_1 & v_2 & v_3 \\ | & | & | \end{bmatrix}", 
                            font_size=32, color=BLUE).set_z_index(25)
        q_mat_viz.next_to(q_expl, DOWN, buff=0.2)
        
        self.add_fixed_in_frame_mobjects(q_expl, q_mat_viz)
        self.play(FadeIn(q_expl, q_mat_viz, shift=UP))
        self.wait(1)

        # Transform e_i -> v_i
        v_labels = VGroup(*[
            MathTex(f"v_{i+1}", font_size=24, color=basis_colors[i])
            for i in range(3)
        ])

        self.play(
            ApplyMatrix(Q_mat, e_vectors),
            FadeOut(e_labels),
            run_time=3
        )
        
        # Update v_labels position
        for i in range(3):
            v_labels[i].next_to(e_vectors[i].get_end(), UP+RIGHT, buff=0.1)
        
        self.play(Write(v_labels))
        self.wait(2)

        # ════════════════════════════════════════════════════════════════════
        # PHASE 2: Ảnh hưởng của Qᵀ (v_i -> e_i)
        # ════════════════════════════════════════════════════════════════════
        self.play(FadeOut(q_expl, q_mat_viz, title))
        
        title2 = Text("Ảnh hưởng của Ma trận Chuyển vị Qᵀ", font_size=24, color=GOLD).set_z_index(25)
        title2.next_to(frame_box, UP, buff=0.02)
        self.add_fixed_in_frame_mobjects(title2)
        self.play(Write(title2))

        qt_expl = Text("Vì Qᵀ = Q⁻¹, nó xoay các vector riêng về lại hệ trục chuẩn", font_size=18, color=TEAL).set_z_index(25)
        qt_expl.next_to(frame_box, DOWN, buff=0.25)
        
        # Matrix QT view (rows)
        qt_mat_viz = MathTex(r"Q^T = \begin{bmatrix} \rule{1cm}{0.4pt} & v_1^T & \rule{1cm}{0.4pt} \\ \rule{1cm}{0.4pt} & v_2^T & \rule{1cm}{0.4pt} \\ \rule{1cm}{0.4pt} & v_3^T & \rule{1cm}{0.4pt} \end{bmatrix}", 
                             font_size=32, color=TEAL).set_z_index(25)
        qt_mat_viz.next_to(qt_expl, DOWN, buff=0.2)
        
        self.add_fixed_in_frame_mobjects(qt_expl, qt_mat_viz)
        self.play(FadeIn(qt_expl, qt_mat_viz, shift=UP))
        self.wait(2)

        # Transform back v_i -> e_i
        res_e_labels = VGroup(*[
            MathTex(f"e_{i+1}", font_size=24, color=basis_colors[i])
            for i in range(3)
        ])

        self.play(
            ApplyMatrix(QT_mat, e_vectors),
            FadeOut(v_labels),
            run_time=3
        )
        
        # Reset labels to standard axes
        res_e_labels[0].next_to(e_vectors[0].get_end(), RIGHT, buff=0.1)
        res_e_labels[1].next_to(e_vectors[1].get_end(), UP, buff=0.1)
        res_e_labels[2].next_to(e_vectors[2].get_end(), OUT, buff=0.1)
        
        self.play(Write(res_e_labels))
        self.wait(3)

        # Dọn dẹp
        self.play(FadeOut(axes, e_vectors, res_e_labels, frame_box, masks, title2, qt_expl, qt_mat_viz))
        self.wait(1)
        # # self.wait(1)

# ==============================================================================
# SCENE 3_Conclusion: Step 9 (A * A^T = ma trận đối xứng)
# ==============================================================================
class Scene3_Conclusion(MovingCameraScene):
    def construct(self):
        self.camera.frame.shift(DOWN * 1.5)
        center_y = -1.5

        # ──────────────────────────────────────────
        # STEP 9: A · A^T luôn là ma trận đối xứng
        # ──────────────────────────────────────────
        title = Text("Nhận xét:", font_size=36, color=GOLD)
        title.move_to(np.array([0, center_y + 3, 0]))
        self.play(Write(title))

        statement = Text(
            "Với ma trận A bất kỳ, tích  A · Aᵀ  luôn là ma trận đối xứng",
            font_size=26, color=TEAL
        )
        statement.move_to(np.array([0, center_y + 1.8, 0]))
        self.play(Write(statement), run_time=2)
        self.wait(1)

        # Chứng minh nhanh
        proof_title = Text("Chứng minh:", font_size=24, color=WHITE)
        proof_title.move_to(np.array([-4, center_y + 0.6, 0]))

        proof_1 = VGroup(
            Text("Đặt ", font_size=36),
            MathTex(r"B = A \cdot A^T", font_size=36)
        ).arrange(RIGHT)
        proof_2 = MathTex(r"B^T = (A \cdot A^T)^T = (A^T)^T \cdot A^T = A \cdot A^T = B", font_size=36, color=GREEN)

        proof_group = VGroup(proof_1, proof_2).arrange(DOWN, buff=0.5)
        proof_group.move_to(np.array([0, center_y - 0.3, 0]))

        self.play(Write(proof_title))
        self.play(Write(proof_1))
        self.wait(1)
        self.play(Write(proof_2))
        self.wait(1)

        # Box kết quả
        box_result = SurroundingRectangle(proof_2, color=GOLD, buff=0.15)
        result_txt = MathTex(r"\Rightarrow B^T = B", font_size=40, color=GOLD)
        result_txt.next_to(box_result, DOWN, buff=0.3)

        self.play(Create(box_result), Write(result_txt))
        self.wait(2)

        # Ví dụ minh họa
        self.play(FadeOut(proof_title, proof_group, box_result, result_txt))

        example_title = Text("Ví dụ:", font_size=28, color=YELLOW)
        example_title.move_to(np.array([0, center_y + 0.8, 0]))

        mat_example_A = MathTex(
            r"A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}",
            font_size=40
        )
        mat_example_A.move_to(np.array([-3, center_y - 0.5, 0]))

        arrow_mult = MathTex(r"\Rightarrow", font_size=48)
        arrow_mult.move_to(np.array([0, center_y - 0.5, 0]))

        mat_example_B = MathTex(
            r"A \cdot A^T = \begin{bmatrix} 5 & 11 & 17 \\ 11 & 25 & 39 \\ 17 & 39 & 61 \end{bmatrix}",
            font_size=36, color=GREEN
        )
        mat_example_B.move_to(np.array([3.5, center_y - 0.5, 0]))

        self.play(Write(example_title))
        self.play(FadeIn(mat_example_A, shift=RIGHT))
        self.play(Write(arrow_mult))
        self.play(FadeIn(mat_example_B, shift=LEFT))
        self.wait(1)

        # Highlight tính đối xứng
        sym_highlight = Text("→ Ma trận kết quả đối xứng qua đường chéo", font_size=22, color=GOLD)
        sym_highlight.move_to(np.array([0, center_y - 2.2, 0]))
        self.play(Write(sym_highlight))
        self.wait(2)

        # Kết luận — cầu nối sang SVD
        self.play(FadeOut(example_title, mat_example_A, arrow_mult, mat_example_B, sym_highlight))

        final_note = Text(
            "Tính chất này là nền tảng quan trọng\n         để xây dựng phân rã SVD!",
            font_size=30, color=GOLD, line_spacing=0.8
        )
        final_note.move_to(np.array([0, center_y + 0.5, 0]))

        # Kết luận chi tiết về mối quan hệ SVD
        v_line = VGroup(
            MathTex(r"A^T A \rightarrow V", font_size=32, color=TEAL),
            Text(": chứa các vector kì dị phải", font_size=24, color=TEAL)
        ).arrange(RIGHT, buff=0.2)
        
        u_line = VGroup(
            MathTex(r"A A^T \rightarrow U", font_size=32, color=TEAL),
            Text(": chứa các vector kì dị trái", font_size=24, color=TEAL)
        ).arrange(RIGHT, buff=0.2)
        
        svd_obs = Text("Nhận xét: U và V có cùng số lượng các giá trị kì dị", font_size=24, color=GOLD)
        
        sigma_line = VGroup(
            Text("Giá trị kì dị: ", font_size=24, color=BLUE),
            MathTex(r"\sigma_i = \sqrt{\lambda_i}", font_size=32, color=BLUE)
        ).arrange(RIGHT, buff=0.2)

        svd_summary = VGroup(v_line, u_line, svd_obs, sigma_line).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        svd_summary.next_to(final_note, DOWN, buff=0.6)

        self.play(Write(final_note))
        self.wait(1)
        
        for line in svd_summary:
            self.play(FadeIn(line, shift=UP), run_time=0.8)
            self.wait(0.5)
            
        self.wait(4)
