from manim import *
import numpy as np
from manim import config
config.tex_template.add_to_preamble(r"\usepackage{amsmath}")

class Clasificadores(Scene):
    def construct(self):
        write_speed = 5

        # ========== SLIDE 1==========
        t0 = Tex("Clasificadores generativos", font_size=52)
        t0.set_color_by_tex("Clasificadores generativos", BLUE)
        self.play(Write(t0, run_time=write_speed)); self.wait(0.8); self.play(FadeOut(t0))

        # ========== SLIDE 2  ==========
        p2 = Tex(
            r"El enfoque generativo modela \textbf{densidades condicionales de clase} \( p(\mathbf{x}|C_k) \) "
            r"y las \textbf{probabilidades previas} \( p(C_k) \), para luego calcular las probabilidades "
            r"posteriores mediante el teorema de Bayes:",
            font_size=36
        ).set_color(WHITE)

        bayes = MathTex(
            r"p(C_k|\mathbf{x}) = \frac{p(\mathbf{x}|C_k)p(C_k)}{\sum_j p(\mathbf{x}|C_j)p(C_j)}",
            font_size=40
        )
        bayes.set_color(WHITE)
        bayes.set_color_by_tex(r"\mathbf{x}", PURPLE)
        bayes.set_color_by_tex("C_k", PURPLE)
        bayes.set_color_by_tex("C_j", PURPLE)

        g2 = VGroup(p2, bayes).arrange(DOWN, buff=0.55)
        g2.move_to(ORIGIN)
        self.play(Write(p2, run_time=write_speed))
        self.play(Write(bayes, run_time=write_speed))
        note = Tex(
            r"Se llaman generativos porque modelan cómo se generan los datos en cada clase:"
            r" primero \(C \sim p(C)\) y luego \( \mathbf{x} \sim p(\mathbf{x}\mid C)\);"
            r" con eso Bayes da \( p(C\mid \mathbf{x}) \).",
            font_size=32
        ).set_color(WHITE)
        note.next_to(bayes, DOWN, buff=0.45).set_x(0)
        self.play(Write(note, run_time=write_speed))
        self.wait(1.0) 
        self.play(FadeOut(VGroup(g2, note)))
    
          # ========== SLIDE 3 ==========
        p3 = Tex(
            r"\vskip 10pt",
            r"Para el caso de dos clases, la probabilidad posterior de la clase \( C_1 \) puede reescribirse de la forma:",
            font_size=36
        ).set_color(WHITE)

        post_bin = MathTex(
            r"p(C_1|\mathbf{x}) = \frac{p(\mathbf{x}|C_1)p(C_1)}{p(\mathbf{x}|C_1)p(C_1) + p(\mathbf{x}|C_2)p(C_2)} = \sigma(a(\mathbf{x}))",
            font_size=40
        )
        post_bin.set_color(WHITE)
        post_bin.set_color_by_tex(r"\mathbf{x}", BLUE)
        post_bin.set_color_by_tex("C_1", RED)
        post_bin.set_color_by_tex("C_2", RED)
        post_bin.set_color_by_tex(r"\sigma",PINK)

        g3 = VGroup(p3, post_bin).arrange(DOWN, buff=0.55)
        g3.move_to(ORIGIN)
        self.play(Write(p3, run_time=write_speed))
        self.play(Write(post_bin, run_time=write_speed))
        self.wait(0.9)
        self.play(FadeOut(g3))

        # ========== SLIDE 4 ==========
        p4 = Tex(
            r"donde \( \sigma(a) \) es la \textbf{función sigmoide logística}:",
            font_size=36
        ).set_color(WHITE)

        sigma_def = MathTex(
            r"\sigma(a) = \frac{1}{1 + \exp(-a)}",
            font_size=40
        )
        sigma_def.set_color(WHITE)
        sigma_def.set_color_by_tex(r"\sigma", BLUE)

        g4 = VGroup(p4, sigma_def).arrange(DOWN, buff=0.55).move_to(UP*1.3)
        self.play(Write(p4, run_time=write_speed))
        self.play(Write(sigma_def, run_time=write_speed))

        axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[0, 1.05, 0.2],
            tips=False,
            axis_config={"color": BLUE}
        )

        labels = axes.get_axis_labels(
            x_label=Tex("a", font_size=32),
            y_label=MathTex(r"\sigma(a)", font_size=32).set_color(ORANGE)
        )

        sig = axes.plot(lambda a: 1/(1+np.exp(-a)), color=ORANGE, stroke_width=6)

        asym0 = DashedLine(axes.c2p(-6, 0), axes.c2p(6, 0), color=GRAY)
        asym1 = DashedLine(axes.c2p(-6, 1), axes.c2p(6, 1), color=GRAY)
        asym_grp = VGroup(asym0, asym1)

        a_tracker = ValueTracker(-6)
        sigma = lambda x: 1/(1+np.exp(-x))

        vline = always_redraw(
            lambda: Line(
                axes.c2p(a_tracker.get_value(), 0.001),
                axes.c2p(a_tracker.get_value(), sigma(a_tracker.get_value())),
                color=GREEN
            ).set_stroke(width=4)
        )

        dot = always_redraw(
            lambda: Dot(
                axes.c2p(a_tracker.get_value(), sigma(a_tracker.get_value())),
                color=YELLOW, radius=0.07
            )
        )

        sigma_label = always_redraw(
            lambda: MathTex(r"\sigma(a)", font_size=30).set_color(ORANGE).next_to(dot, UP, buff=0.18)
        )

        anim_grp = VGroup(axes, labels, sig, asym_grp, vline, dot, sigma_label)

        max_graph_height = 3.0
        anim_grp.set_height(max_graph_height)
        anim_grp.to_edge(DOWN, buff=0.6)

        self.play(Create(axes), Write(labels))
        self.play(Create(asym_grp), run_time=0.6)
        self.play(Create(sig), run_time=1.0)
        self.play(FadeIn(vline, shift=UP*0.1), FadeIn(dot, scale=1.05), FadeIn(sigma_label), run_time=0.6)
        self.play(a_tracker.animate.set_value(6), run_time=3.0, rate_func=linear)
        self.play(dot.animate.scale(1.4), rate_func=there_and_back, run_time=0.45)
        self.wait(0.5)
        self.play(FadeOut(VGroup(g4, anim_grp), shift=DOWN*0.3))

       # ========== SLIDE 5  ==========
        p5 = Tex(
            r"y \( a(\mathbf{x}) \) es el \textbf{log-odds}:",
            font_size=36
        ).set_color(WHITE)

        a_def = MathTex(
            r"a(\mathbf{x}) = ",
            r"\ln",
            r"\frac{p(\mathbf{x}|C_1)p(C_1)}{p(\mathbf{x}|C_2)p(C_2)}",
            font_size=40
        )
        a_def.set_color(WHITE)
        a_def[2].set_color(BLUE)
        a_def[0].set_color(WHITE)

        g5_head = VGroup(p5, a_def).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        g5_head.to_edge(UP).shift(DOWN*0.6)

        self.play(Write(p5, run_time=write_speed))
        self.play(Write(a_def, run_time=write_speed))

        note5 = Tex(
            r"La sigmoide \( \sigma(a) \) transforma un puntaje real \(a\) (log-odds) en una probabilidad en \([0,1]\).",
            font_size=32
        ).set_color(WHITE)
        note5.next_to(g5_head, DOWN, buff=0.45).set_x(0)
        self.play(Write(note5, run_time=write_speed*0.6))

        a_val = 1.4
        p_val = 1.0 / (1.0 + np.exp(-a_val))

        def bmatrix_scalar(v, nd=2):
            return MathTex(r"\begin{bmatrix} " + f"{v:.{nd}f}" + r" \end{bmatrix}",
                        font_size=44).set_color(WHITE)

        left_title = Tex(r"log-odds \(a\)", font_size=30).set_color(WHITE)
        left_vec   = bmatrix_scalar(a_val, nd=1)
        left_grp   = VGroup(left_title, left_vec).arrange(DOWN, buff=0.3, aligned_edge=ORIGIN)

        center_title = Tex(r"Función sigmoide", font_size=30).set_color(WHITE)
        box_w, box_h = 4.8, 2.6
        center_box   = RoundedRectangle(corner_radius=0.12, width=box_w, height=box_h).set_stroke(WHITE, 2)
        center_tex   = MathTex(r"\displaystyle \sigma(a)=\frac{1}{1+e^{-a}}", font_size=48).set_color(WHITE)
        center_tex.move_to(center_box.get_center())
        center_core  = VGroup(center_box, center_tex)
        center_grp   = VGroup(center_title, center_core).arrange(DOWN, buff=0.3, aligned_edge=ORIGIN)

        right_title = Tex("Probabilidad", font_size=30).set_color(WHITE)
        right_vec   = bmatrix_scalar(p_val, nd=2)
        right_grp   = VGroup(right_title, right_vec).arrange(DOWN, buff=0.3, aligned_edge=ORIGIN)

        pipeline = VGroup(left_grp, center_grp, right_grp).arrange(RIGHT, buff=1.4)
        pipeline.next_to(note5, DOWN, buff=0.6)

        arr_lc = Arrow(left_vec.get_right()+RIGHT*0.10, center_box.get_left()-RIGHT*0.10, stroke_width=4, buff=0.2)
        arr_cr = Arrow(center_box.get_right()+RIGHT*0.10, right_vec.get_left()-RIGHT*0.10, stroke_width=4, buff=0.2)

        self.play(FadeIn(left_grp, shift=UP*0.2), run_time=0.8)
        self.play(GrowArrow(arr_lc), run_time=0.5)
        self.play(FadeIn(center_title, shift=UP*0.2), FadeIn(center_box, shift=UP*0.1), run_time=0.6)
        self.play(Write(center_tex, run_time=0.9))
        self.play(GrowArrow(arr_cr), run_time=0.5)
        self.play(FadeIn(right_grp, shift=UP*0.2), run_time=0.8)
        self.wait(0.6)

        slide5_all = VGroup(g5_head, note5, pipeline, arr_lc, arr_cr)
        self.play(FadeOut(slide5_all, shift=UP*0.8), run_time=0.9)

        # ========== SLIDE  ==========
        p6 = Tex(
            r"La sigmoide logística tiene propiedades importantes:",
            font_size=36
        ).set_color(WHITE)

        prop1 = MathTex(
            r"\sigma(-a) = 1 - \sigma(a)",
            font_size=40
        )
        prop1.set_color(WHITE)
        prop1.set_color_by_tex(r"\sigma", GREEN)

        prop2 = MathTex(
            r"a = \ln\left(\frac{\sigma}{1-\sigma}\right) \quad \text{(función logit)}",
            font_size=40
        )
        prop2.set_color(WHITE)
        prop2.set_color_by_tex(r"\sigma", PINK)

        g6 = VGroup(p6, prop1, prop2).arrange(DOWN, buff=0.45)
        g6.move_to(ORIGIN)
        self.play(Write(p6, run_time=write_speed))
        self.play(Write(prop1, run_time=write_speed))
        self.play(Write(prop2, run_time=write_speed))
        self.wait(0.9)
        self.play(FadeOut(g6))

        # ---------- SLIDE 7 ----------
        p7 = Tex(
            r"\vskip 15pt",
            r"Para \( K > 2 \) clases, generalizamos usando la función \textbf{softmax}:",
            font_size=36
        ).set_color(WHITE)
        soft_hdr = MathTex(
            r"p(C_k|\mathbf{x}) = \frac{\exp(a_k)}{\sum_{j} \exp(a_j)}",
            font_size=40
        ).set_color(WHITE)
        soft_hdr.set_color_by_tex(r"\mathbf{x}", BLUE).set_color_by_tex("C_k", BLUE)
        g7_head = VGroup(p7, soft_hdr).arrange(DOWN, buff=0.45, aligned_edge=ORIGIN)
        g7_head.to_edge(UP).shift(DOWN*0.6)

        self.play(Write(p7, run_time=write_speed))
        self.play(Write(soft_hdr, run_time=write_speed))
        self.wait(0.2)

        a_vals = np.array([1.3, 5.1, 2.2, 0.7, 1.1])
        K = len(a_vals)

        def softmax_np(x):
            x = x - np.max(x)
            e = np.exp(x)
            return e / e.sum()

        p_vals = softmax_np(a_vals)

        def col_bmatrix(vals, nd=1):
            body = r" \\ ".join([f"{v:.{nd}f}" for v in vals])
            return MathTex(r"\begin{bmatrix} " + body + r" \end{bmatrix}", font_size=44).set_color(WHITE)

        left_title = Tex(r"log-odds \(a\)", font_size=30).set_color(WHITE)
        left_vec   = col_bmatrix(a_vals, nd=1)
        left_grp   = VGroup(left_title, left_vec).arrange(DOWN, buff=0.3, aligned_edge=ORIGIN)

        center_title = Tex("Función softmax", font_size=30).set_color(WHITE)
        box_w, box_h = 4.8, 3.0
        center_box   = RoundedRectangle(corner_radius=0.12, width=box_w, height=box_h).set_stroke(WHITE, 2)
        center_tex   = MathTex(
            r"\displaystyle \frac{e^{a_k}}{\sum_{j=1}^{"+str(K)+r"} e^{a_k}}",
            font_size=48
        ).set_color(WHITE).move_to(center_box.get_center())
        center_core  = VGroup(center_box, center_tex)
        center_grp   = VGroup(center_title, center_core).arrange(DOWN, buff=0.3, aligned_edge=ORIGIN)

        right_title = Tex("Probabilidades", font_size=30).set_color(WHITE)
        right_vec   = col_bmatrix(p_vals, nd=2)
        right_grp   = VGroup(right_title, right_vec).arrange(DOWN, buff=0.3, aligned_edge=ORIGIN)

        pipeline = VGroup(left_grp, center_grp, right_grp).arrange(RIGHT, buff=1.4)
        pipeline.next_to(g7_head, DOWN, buff=0.7)

        arr_lc = Arrow(
            left_vec.get_right()+RIGHT*0.10, center_box.get_left()-RIGHT*0.10,
            stroke_width=4, buff=0.2
        )
        arr_cr = Arrow(
            center_box.get_right()+RIGHT*0.10, right_vec.get_left()-RIGHT*0.10,
            stroke_width=4, buff=0.2
        )

        self.play(FadeIn(left_grp, shift=UP*0.2), run_time=0.8)
        self.play(GrowArrow(arr_lc), run_time=0.5)
        self.play(FadeIn(center_title, shift=UP*0.2), FadeIn(center_box, shift=UP*0.1), run_time=0.6)
        self.play(Write(center_tex, run_time=0.9))
        self.play(GrowArrow(arr_cr), run_time=0.5)
        self.play(FadeIn(right_grp, shift=UP*0.2), run_time=0.8)
        self.wait(0.6)

        slide7_all = VGroup(g7_head, pipeline, arr_lc, arr_cr)
        self.play(FadeOut(slide7_all, shift=UP*0.8), run_time=0.9)

        # ========== SLIDE 8 ==========
        p8 = Tex(
            r"donde:",
            font_size=36
        ).set_color(WHITE)

        ak = MathTex(
            r"a_k = \ln[p(\mathbf{x}|C_k)p(C_k)]",
            font_size=40
        )
        ak.set_color(WHITE)
        ak.set_color_by_tex(r"\mathbf{x}", BLUE)
        ak.set_color_by_tex("C_k", RED)

        note = Tex(
            r"La softmax suaviza la función máximo: si \( a_k \gg a_j \) para todo \( j \neq k \), entonces \( p(C_k|\mathbf{x}) \approx 1 \) y \( p(C_j|\mathbf{x}) \approx 0 \)  .",
            font_size=36
        ).set_color(WHITE)

        g8 = VGroup(p8, ak, note).arrange(DOWN, buff=0.5)
        g8.move_to(ORIGIN)
        self.play(Write(p8, run_time=write_speed))
        self.play(Write(ak, run_time=write_speed))
        self.play(Write(note, run_time=write_speed))
        self.wait(1.0)
        self.play(FadeOut(g8))

# manim -pqh Clasificadores.py Clasificadores
