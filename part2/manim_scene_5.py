from manim import *
import numpy as np
from PIL import Image

class Scene_12(Scene):
    """
    Giới thiệu tính chất sắp xếp giảm dần của giá trị kỳ dị
    """
    def construct(self):
        intro_title = Text("Ứng dụng của SVD: Nén ảnh", font_size=48, color=GOLD)
        self.play(Write(intro_title), run_time=2.0)
        self.wait(3.0)
        self.play(FadeOut(intro_title), run_time=1.0)

        center_y = 0  # Re-centered for this scene

        ordering_title = Text(
            "Giá trị kỳ dị luôn được sắp xếp giảm dần:", 
            font_size=32, color=GOLD
        )
        ordering_title.move_to(np.array([0, center_y + 3.2, 0]))

        ineq = MathTex(
            r"\sigma_1", r"\geq", r"\sigma_2", r"\geq", 
            r"\cdots", r"\geq", r"\sigma_n", r"\geq", r"0",
            font_size=44
        )
        ineq[0].set_color(YELLOW)       # σ₁
        ineq[2].set_color(GOLD)         # σ₂  
        ineq[4].set_color(GREY)         # ...
        ineq[6].set_color(RED_B)        # σₙ
        ineq[8].set_color(WHITE)        # 0
        ineq.move_to(np.array([0, center_y + 2.2, 0]))

        self.play(Write(ordering_title), run_time=2.0)
        self.play(Write(ineq), run_time=2.5)
        self.wait(3.0)

        sigma_values = [120, 45, 12, 3, 0.8, 0.1]
        sigma_labels_tex = [r"\sigma_1", r"\sigma_2", r"\sigma_3", r"\sigma_4", r"\sigma_5", r"\sigma_6"]
        bar_colors = [YELLOW, GOLD, ORANGE, RED_B, RED_D, GREY]
        
        max_bar_height = 3.0
        bar_width = 0.7
        bar_spacing = 0.3
        
        total_width = len(sigma_values) * bar_width + (len(sigma_values) - 1) * bar_spacing
        chart_left_x = -total_width / 2 + bar_width / 2  # -2.5 for 6 bars
        
        chart_bottom_y = center_y - 3.0

        bars = VGroup()
        bar_labels_grp = VGroup()
        bar_value_labels = VGroup()

        for i, (val, label, color) in enumerate(zip(sigma_values, sigma_labels_tex, bar_colors)):
            h = max(val / sigma_values[0] * max_bar_height, 0.05)
            bar = Rectangle(
                width=bar_width, height=h,
                fill_color=color, fill_opacity=0.85,
                stroke_color=WHITE, stroke_width=1
            )
            x_pos = chart_left_x + i * (bar_width + bar_spacing)
            bar.move_to(np.array([x_pos, chart_bottom_y + h / 2, 0]))
            bars.add(bar)

            lbl = MathTex(label, font_size=22, color=color)
            lbl.next_to(bar, DOWN, buff=0.1)
            bar_labels_grp.add(lbl)

            val_lbl = Text(f"{val}", font_size=16, color=WHITE)
            val_lbl.next_to(bar, UP, buff=0.08)
            bar_value_labels.add(val_lbl)

        chart_title = Text("Ví dụ về độ lớn của các giá trị kỳ dị (σᵢ):", font_size=24, color=TEAL)
        chart_title.move_to(np.array([0, center_y + 1.2, 0]))

        self.play(Write(chart_title), run_time=1.5)
        
        for i in range(len(bars)):
            self.play(
                GrowFromEdge(bars[i], DOWN),
                FadeIn(bar_labels_grp[i]),
                FadeIn(bar_value_labels[i]),
                run_time=0.8
            )
        self.wait(3.0)

        important_box = SurroundingRectangle(
            VGroup(*bars[0:3], *bar_labels_grp[0:3], *bar_value_labels[0:3]),
            color=GREEN, buff=0.05, corner_radius=0.1
        )
        important_text = Text(
            "Chứa phần lớn thông tin!", 
            font_size=22, color=GREEN
        )
        important_text.next_to(important_box, UP, buff=0.15)

        self.play(Create(important_box), Write(important_text), run_time=1.5)
        self.wait(3.0)

        negligible_box = SurroundingRectangle(
            VGroup(*bars[3:6], *bar_labels_grp[3:6], *bar_value_labels[3:6]),
            color=RED_B, buff=0.05, corner_radius=0.1
        )
        negligible_text = Text(
            "Ít thông tin → Có thể bỏ qua khi nén", 
            font_size=22, color=RED_B
        )
        negligible_text.next_to(negligible_box, DOWN, buff=0.15)

        self.play(Create(negligible_box), Write(negligible_text), run_time=1.5)
        self.wait(4.0)

        self.play(
            FadeOut(important_box, important_text, negligible_box, negligible_text),
            run_time=1.0
        )

        conclusion = Text(
            "→ Ứng dụng: Chỉ cần giữ lại k giá trị kỳ dị lớn nhất để nén ảnh!",
            font_size=28, color=GOLD
        )
        conclusion.move_to(np.array([0, center_y + 1.2, 0]))

        self.play(
            FadeOut(chart_title),
            Write(conclusion),
            run_time=2.0
        )
        self.wait(4.0)

        self.play(
            FadeOut(ordering_title, ineq, bars, bar_labels_grp, bar_value_labels, conclusion),
            run_time=2.0
        )
        self.wait(1)
class Scene_13(Scene):
    """
    Ứng dụng thuật toán SVD để nén ảnh
    """
    def construct(self):
        intro_title = Text("Ứng dụng SVD: Nén ảnh", font_size=40, color=GOLD).to_edge(UP)
        formula = MathTex(
            r"A_k = \sum_{i=1}^{k} \sigma_i u_i v_i^T",
            font_size=48, color=YELLOW
        ).next_to(intro_title, DOWN, buff=0.5)
        
        desc = Text(
            "Mỗi lớp (rank-1) bổ sung thêm chi tiết cho bức ảnh",
            font_size=24
        ).next_to(formula, DOWN, buff=0.5)
        
        self.play(Write(intro_title))
        self.play(FadeIn(formula, shift=UP))
        self.play(Write(desc))
        self.wait(2)
        self.play(FadeOut(intro_title, formula, desc))

        import os
        img_path = 'image_test.jpg'
        if not os.path.exists(img_path):
            img_path = os.path.join('part2', 'image_test.jpg')
            
        try:
            img = Image.open(img_path).convert('RGB')
            img = img.resize((250, 250)) 
            A = np.array(img, dtype=float) 
        except FileNotFoundError:
            self.add(Text(f"Không tìm thấy file '{img_path}'!", color=RED))
            return

        h, w, _ = A.shape
        total_pixels = h * w
        
        channels = [A[:, :, i] for i in range(3)]
        svd_data = [np.linalg.svd(ch, full_matrices=False) for ch in channels]
        
        total_energy = sum([np.sum(s**2) for _, s, _ in svd_data])

        def get_image_mob(matrix_rgb):
            matrix_uint8 = np.clip(matrix_rgb, 0, 255).astype(np.uint8)
            mob = ImageMobject(matrix_uint8).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            mob.height = 4.5
            return mob

        title = Text("SVD Image Compression (RGB)", font_size=32).to_edge(UP, buff=0.2)
        self.add(title)
        
        orig_img_mob = get_image_mob(A).shift(LEFT * 3 + UP * 0.1)
        orig_label = Text("Ảnh Gốc", font_size=20).next_to(orig_img_mob, DOWN, buff=0.3)
        size_label = Text("250x250", font_size=18, color=GREY).next_to(orig_img_mob, UP, buff=0.2)
        
        self.play(FadeIn(orig_img_mob), Write(orig_label), FadeIn(size_label))

        recon_placeholder = Rectangle(width=4.6, height=4.6, color=WHITE, stroke_width=1).shift(RIGHT * 3 + UP * 0.1)
        self.add(recon_placeholder)
        
        k_values = [1, 5, 10, 20, 50, 100]
        
        current_recon_mob = None
        k_text = Text("k = 0", font_size=24, color=YELLOW).next_to(recon_placeholder, UP, buff=0.2)
        ratio_text = Text("Lưu trữ: 0%", font_size=24, color=TEAL).to_edge(DOWN, buff=0.8)
        
        self.add(k_text, ratio_text)

        for k in k_values:
            recon_channels = []
            for i in range(3):
                u, s, vt = svd_data[i]
                ak_i = u[:, :k] @ np.diag(s[:k]) @ vt[:k, :]
                recon_channels.append(ak_i)
            
            Ak = np.stack(recon_channels, axis=-1)
            new_recon_mob = get_image_mob(Ak).move_to(recon_placeholder.get_center())
            
            compressed_data = k * (h + w + 1) * 3
            ratio = (compressed_data / (total_pixels * 3)) * 100
            
            new_k_text = Text(f"k = {k}", font_size=24, color=YELLOW).move_to(k_text)
            new_ratio_text = Text(f"Dung lượng lưu trữ: {ratio:.1f}%", font_size=22, color=TEAL).move_to(ratio_text)
            
            if current_recon_mob is None:
                self.play(
                    FadeIn(new_recon_mob),
                    Transform(k_text, new_k_text),
                    Transform(ratio_text, new_ratio_text),
                    run_time=1
                )
                current_recon_mob = new_recon_mob
            else:
                self.play(
                    Transform(current_recon_mob, new_recon_mob),
                    Transform(k_text, new_k_text),
                    Transform(ratio_text, new_ratio_text),
                    run_time=1.5
                )
            
            self.wait(1)

        self.play(Indicate(ratio_text, color=GREEN, scale_factor=1.1))
        self.wait(1)
        
        final_msg = Text("SVD giúp giảm dung lượng đáng kể mà vẫn giữ được chi tiết!", 
                         font_size=22, color=GREEN).to_edge(DOWN, buff=0.4)
        self.play(FadeOut(ratio_text), Write(final_msg))
        self.wait(3)