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

        self.add_fixed_in_frame_mobjects(frame_box, masks)

        # ──────────────────────────────────────────
        # STEP 1: Giới thiệu tính chất ma trận đối xứng
        # ──────────────────────────────────────────
        title = Text("Tính chất Ma trận Đối xứng", font_size=28, color=GOLD)
        title.next_to(frame_box, UP, buff=0.15).set_z_index(25)
        self.add_fixed_in_frame_mobjects(title)

        self.play(FadeIn(frame_box, masks), Write(title))

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
        eigen_lines = VGroup()
        ev_colors = [BLUE, GREEN, RED]
        for i in range(3):
            lam_val = f"{eigenvalues[i]:.2f}"
            vec_str = f"({ev_np[i][0]:.2f}, {ev_np[i][1]:.2f}, {ev_np[i][2]:.2f})"
            line = Text(f"λ{i+1} = {lam_val}    v{i+1} = {vec_str}", font_size=18, color=ev_colors[i])
            eigen_lines.add(line)
        eigen_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.25).set_z_index(25)
        eigen_lines.next_to(frame_box, DOWN, buff=0.25)

        for line in eigen_lines:
            self.add_fixed_in_frame_mobjects(line)
            self.remove(line)

        subtitle_eigen = Text("Kết quả phân tích trị riêng (Jacobi):", font_size=20, color=GOLD).set_z_index(25)
        subtitle_eigen.next_to(frame_box, DOWN, buff=0.05)
        self.add_fixed_in_frame_mobjects(subtitle_eigen)
        self.remove(subtitle_eigen)

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
        eigenvalues, eigenvectors, Q_rows, Q_T_rows = _compute_eigen_data()
        ev_np = [np.array(v, dtype=float) for v in eigenvectors]
        q_np = [np.array(vector_normalize(v), dtype=float) for v in eigenvectors]
        Q_mat = np.array(Q_rows, dtype=float)
        QT_mat = np.array(Q_T_rows, dtype=float)
        ev_colors = [BLUE, GREEN, RED]

        # --- Frame + Masks ---
        self.move_camera(frame_center=np.array([0, -0.75, 0]))
        frame_box = Rectangle(width=12, height=5, color=WHITE, stroke_width=2).move_to(ORIGIN)
        frame_box.set_z_index(20)

        mask_top   = Rectangle(width=32, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, UP, buff=0)
        mask_bot   = Rectangle(width=32, height=10, color=BLACK, fill_opacity=1).next_to(frame_box, DOWN, buff=0)
        mask_left  = Rectangle(width=10, height=6,  color=BLACK, fill_opacity=1).next_to(frame_box, LEFT, buff=0)
        mask_right = Rectangle(width=10, height=6,  color=BLACK, fill_opacity=1).next_to(frame_box, RIGHT, buff=0)
        masks = VGroup(mask_top, mask_bot, mask_left, mask_right).set_z_index(15)

        self.add_fixed_in_frame_mobjects(frame_box, masks)

        title = Text("Ảnh hưởng của Ma trận Trực giao Q lên Không gian", font_size=22, color=GOLD)
        title.next_to(frame_box, UP, buff=0.15).set_z_index(25)
        self.add_fixed_in_frame_mobjects(title)

        self.play(FadeIn(frame_box, masks), Write(title))

        # --- Trục 3D ---
        axes = ThreeDAxes(
            x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3],
            axis_config={"stroke_width": 2}
        )
        axes.move_to(np.array([0, -0.3, 0]))
        origin = axes.get_origin()

        self.move_camera(phi=65 * DEGREES, theta=35 * DEGREES, run_time=2)
        self.play(Create(axes))

        # Hiển thị eigenvector arrows (mờ hơn, dùng làm tham chiếu)
        eigen_arrows = VGroup()
        for i in range(3):
            direction = q_np[i] * 2.0
            arrow = Arrow3D(
                start=origin, end=origin + direction,
                color=ev_colors[i], resolution=8
            )
            arrow.set_opacity(0.4)
            eigen_arrows.add(arrow)

        eigen_label = Text("Mờ: vector riêng (đã chuẩn hóa)", font_size=16, color=GREY_B).set_z_index(25)
        eigen_label.next_to(frame_box, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(eigen_label)
        self.remove(eigen_label)

        self.play(Create(eigen_arrows), FadeIn(eigen_label))
        self.wait(1)

        # Tạo basis vectors chuẩn (đậm)
        std_arrows = VGroup()
        std_colors = [YELLOW, TEAL, MAROON_B]
        std_labels_text = ["e₁(x)", "e₂(y)", "e₃(z)"]
        std_dirs = [np.array([2, 0, 0], dtype=float),
                    np.array([0, 2, 0], dtype=float),
                    np.array([0, 0, 2], dtype=float)]

        for i in range(3):
            arrow = Arrow3D(
                start=origin, end=origin + std_dirs[i],
                color=std_colors[i], resolution=8
            )
            std_arrows.add(arrow)

        self.play(Create(std_arrows))
        self.wait(1)

        # ──────────────────────────────────────────
        # STEP 7: Áp dụng Q lên không gian
        # ──────────────────────────────────────────
        self.play(FadeOut(eigen_label))

        step7_label = Text("Áp dụng Q: Trục chuẩn QUAY về trùng vector riêng", font_size=18, color=TEAL).set_z_index(25)
        step7_label.next_to(frame_box, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(step7_label)
        self.remove(step7_label)
        self.play(FadeIn(step7_label))

        # Nhóm trục chuẩn + axes để áp dụng biến đổi
        space_group = VGroup(axes, std_arrows)
        space_group.save_state()

        self.play(ApplyMatrix(Q_mat, space_group), run_time=3)
        self.wait(1)

        result7 = Text("→ Trục chuẩn (đậm) trùng vector riêng (mờ)!", font_size=18, color=GREEN).set_z_index(25)
        result7.next_to(step7_label, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(result7)
        self.remove(result7)
        self.play(FadeIn(result7))

        # Quay camera để thấy rõ
        self.move_camera(phi=50 * DEGREES, theta=75 * DEGREES, run_time=2)
        self.wait(2)

        # Khôi phục
        self.play(FadeOut(step7_label, result7))
        self.play(Restore(space_group), run_time=2)
        self.wait(1)

        # ──────────────────────────────────────────
        # STEP 8: Áp dụng Q^T lên không gian — quay ngược
        # ──────────────────────────────────────────
        self.play(FadeOut(std_arrows))

        # Bây giờ tạo eigenvector arrows ĐẬM (sẽ bị Q^T tác động)
        eigen_arrows_bold = VGroup()
        for i in range(3):
            direction = q_np[i] * 2.0
            arrow = Arrow3D(
                start=origin, end=origin + direction,
                color=ev_colors[i], resolution=8
            )
            eigen_arrows_bold.add(arrow)
        self.play(Create(eigen_arrows_bold))

        # Tạo trục chuẩn mờ làm tham chiếu
        std_ref = VGroup()
        for i in range(3):
            arrow = Arrow3D(
                start=origin, end=origin + std_dirs[i],
                color=std_colors[i], resolution=8
            )
            arrow.set_opacity(0.4)
            std_ref.add(arrow)
        self.play(Create(std_ref))
        self.play(FadeOut(eigen_arrows))  # bỏ eigenvector mờ cũ

        step8_label = Text("Áp dụng Qᵀ: Vector riêng QUAY về trùng trục chuẩn", font_size=18, color=MAROON_B).set_z_index(25)
        step8_label.next_to(frame_box, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(step8_label)
        self.remove(step8_label)
        self.play(FadeIn(step8_label))

        space_group_2 = VGroup(axes, eigen_arrows_bold)
        self.play(ApplyMatrix(QT_mat, space_group_2), run_time=3)
        self.wait(1)

        result8 = Text("→ Vector riêng (đậm) trùng trục chuẩn (mờ)!", font_size=18, color=GREEN).set_z_index(25)
        result8.next_to(step8_label, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(result8)
        self.remove(result8)
        self.play(FadeIn(result8))

        self.move_camera(phi=60 * DEGREES, theta=120 * DEGREES, run_time=2)
        self.wait(3)

        # Dọn dẹp
        self.play(FadeOut(
            axes, eigen_arrows_bold, std_ref,
            step8_label, result8, frame_box, masks, title
        ))
        self.wait(0.5)


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
        title = Text("Nhận xét quan trọng", font_size=36, color=GOLD)
        title.move_to(np.array([0, center_y + 3, 0]))
        self.play(Write(title))

        statement = Text(
            "Với MA TRẬN BẤT KỲ A, tích  A · Aᵀ  luôn là ma trận đối xứng!",
            font_size=26, color=TEAL
        )
        statement.move_to(np.array([0, center_y + 1.8, 0]))
        self.play(Write(statement), run_time=2)
        self.wait(1)

        # Chứng minh nhanh
        proof_title = Text("Chứng minh:", font_size=24, color=WHITE)
        proof_title.move_to(np.array([-4, center_y + 0.6, 0]))

        proof_1 = MathTex(r"\text{Đặt } B = A \cdot A^T", font_size=36)
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
        sym_highlight = Text("→ Ma trận kết quả ĐỐI XỨNG qua đường chéo!", font_size=22, color=GOLD)
        sym_highlight.move_to(np.array([0, center_y - 2.2, 0]))
        self.play(Write(sym_highlight))
        self.wait(2)

        # Kết luận — cầu nối sang SVD
        self.play(FadeOut(example_title, mat_example_A, arrow_mult, mat_example_B, sym_highlight))

        final_note = Text(
            "Tính chất này là nền tảng quan trọng\nđể xây dựng phân rã SVD!",
            font_size=30, color=GOLD, line_spacing=0.8
        )
        final_note.move_to(np.array([0, center_y + 0.5, 0]))

        svd_hint = MathTex(
            r"A^T A \rightarrow V, \quad A A^T \rightarrow U, \quad \sigma_i = \sqrt{\lambda_i}",
            font_size=40, color=TEAL
        )
        svd_hint.next_to(final_note, DOWN, buff=0.8)

        self.play(Write(final_note))
        self.wait(1)
        self.play(FadeIn(svd_hint, shift=UP))
        self.wait(4)
