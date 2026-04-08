from manim import *
import numpy as np
import sys
import os

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from decomposition import householder_qr_v1
from diagonalization import diagonalize

def get_text_table(data):
    # Create a 2D list of Text objects
    mobjects = []
    for row in data:
        m_row = []
        for val in row:
            if abs(val) < 1e-10: val = 0.0
            m_row.append(Text(f"{val:.2f}", font_size=16))
        mobjects.append(m_row)
    
    # Use MobjectTable to avoid LaTeX issues
    table = MobjectTable(mobjects, include_outer_lines=False)
    
    # Add custom brackets (Lines)
    h = table.height
    l_line = Line(UP * h/2, DOWN * h/2).next_to(table, LEFT, buff=0.1)
    r_line = Line(UP * h/2, DOWN * h/2).next_to(table, RIGHT, buff=0.1)
    # Using Group instead of VGroup for maximum compatibility
    return Group(table, l_line, r_line)

class MatrixProject(Scene):
    def construct(self):
        # 1. Introduction
        title = Text("Đồ án 1: Phân rã Ma trận & Chéo hóa", color=YELLOW, font_size=32).to_edge(UP)
        self.add(title)
        
        intro = Text("Phần 2: Phân rã QR và Chéo hóa", font_size=24).shift(UP * 2)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        # Data
        A_data = [[4.0, 2.0, 2.0], [2.0, 4.0, 2.0], [2.0, 2.0, 4.0]]
        
        # 2. QR Analysis
        sub1 = Text("1. Phân rã QR (Householder)", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(sub1))
        
        A_mat = get_text_table(A_data)
        A_label = Text("A =", font_size=20).next_to(A_mat, LEFT)
        A_group = Group(A_label, A_mat).center()
        
        self.play(FadeIn(A_group))
        self.wait(1)
        self.play(A_group.animate.to_edge(LEFT).scale(0.8))
        
        # Calculate QR
        Q_data, R_data = householder_qr_v1(A_data)
        
        Q_mat = get_text_table(Q_data).scale(0.6).shift(RIGHT * 3 + UP * 1)
        R_mat = get_text_table(R_data).scale(0.6).next_to(Q_mat, DOWN, buff=0.5)
        
        Q_label = Text("Q =", font_size=20).next_to(Q_mat, LEFT)
        R_label = Text("R =", font_size=20).next_to(R_mat, LEFT)
        
        self.play(FadeIn(Group(Q_label, Q_mat)))
        self.play(FadeIn(Group(R_label, R_mat)))
        self.wait(3)
        
        self.play(FadeOut(A_group), FadeOut(Q_label), FadeOut(Q_mat), FadeOut(R_label), FadeOut(R_mat), FadeOut(sub1))

        # 3. Diagonalization
        sub2 = Text("2. Chéo hóa Ma trận", font_size=20, color=GREEN).next_to(title, DOWN)
        self.play(Write(sub2))
        
        # Calculate Diagonalization
        P_data, D_data = diagonalize(A_data)
        
        P_mat = get_text_table(P_data).scale(0.6).shift(RIGHT * 3 + UP * 1)
        D_mat = get_text_table(D_data).scale(0.6).next_to(P_mat, DOWN, buff=0.5)
        
        P_label = Text("P =", font_size=20).next_to(P_mat, LEFT)
        D_label = Text("D =", font_size=20).next_to(D_mat, LEFT)
        
        self.play(FadeIn(Group(P_label, P_mat)))
        self.play(FadeIn(Group(D_label, D_mat)))
        
        evals = [D_data[i][i] for i in range(3)]
        val_info = Text(f"Giá trị riêng: {evals[0]:.1f}, {evals[1]:.1f}, {evals[2]:.1f}", font_size=18).shift(DOWN * 3)
        self.play(Write(val_info))
        self.wait(3)
        
        # End
        self.play(FadeOut(Group(*self.mobjects)))
        self.play(Write(Text("Hoàn thành!", font_size=32)))
        self.wait(2)
