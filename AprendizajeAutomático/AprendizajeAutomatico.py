from manim import *
from manim import config
import numpy as np
import math
config.tex_template.add_to_preamble(r"\usepackage{amsmath, amsthm, bm}")
config.tex_template.add_to_preamble(r"\newtheorem{teorema}{Teorema}")
config.tex_template.add_to_preamble(r"\newtheorem{definicion}{Definición}")

TOKEN_COLORS_TEX = {
    r"\mathcal{S}": TEAL_B,
    r"\mathcal{F}": PURPLE,
    r"\mathcal{A}": GREEN,
    r"\ell": YELLOW,
    r"\mathbb{E}": PINK,
}
TOKEN_COLORS_MATH = {
    r"\mathcal{S}": TEAL_B,
    r"\mathcal{F}": PURPLE,
    r"\mathcal{A}": GREEN,
    r"\ell": YELLOW,
    r"\mathbb{E}": PINK,
    r"\mathbf{x}": BLUE, r"\bm{x}": BLUE,
    r"x": BLUE,  
    r"y": ORANGE,  
    r"\operatorname{Kern}": BLUE,
    r"\operatorname{Im}": GREEN,
    r"\mathcal{M}_2": ORANGE, r"\mathcal{D}_0": TEAL_B,
}

def colorize(mobj, extra=None):
    if not isinstance(mobj, (Tex, MathTex)):
        return mobj
    mobj.set_color(WHITE)
    if isinstance(mobj, MathTex):
        mapping = {
            r"\mathcal{S}": TEAL_B,
            r"\mathcal{F}": PURPLE,
            r"\mathcal{A}": GREEN,
            r"\ell": YELLOW,
            r"\mathbb{E}": PINK,
            r"\mathbf{x}": BLUE, r"\bm{x}": BLUE,
            r"x": BLUE,
            r"y": PINK,
            r"y_n": BLUE,
            r"y_{n}": BLUE,
            r"y_{N}": BLUE,
            r"y_N": BLUE, 
            r"\operatorname{Kern}": BLUE,
            r"\operatorname{Im}": GREEN,
            r"\mathcal{M}_2": BLUE, r"\mathcal{D}_0": TEAL_B,
        }
        if extra: mapping.update(extra)
        for tok, col in mapping.items():
            mobj.set_color_by_tex(tok, col)
    return mobj

def slide(scene, title_tex, blocks, write_speed=5, subtitle_gap=0.60, body_gap=0.30):
    title = Tex(title_tex, font_size=40).set_color(ORANGE)
    body  = VGroup(*blocks).arrange(DOWN, buff=body_gap)
    body.move_to(ORIGIN)
    title.next_to(body, UP, buff=subtitle_gap).align_to(body, LEFT)
    group = VGroup(title, body)
    for m in group:
        scene.play(Write(m, run_time=write_speed))
    scene.wait(0.6)
    scene.play(FadeOut(group))

def build_mackay_graph():
    axes = Axes(
        x_range=[0, 10, 1],
        y_range=[0, 1.05, 0.2],
        x_length=8.0, y_length=3.6,
        axis_config={"color": GRAY_B, "include_ticks": False, "include_tip": True,
                     "stroke_width": 2.8, "tip_width": 0.16, "tip_height": 0.16},
    )
    ylab = MathTex(r"p(\mathcal{D})", color=GRAY_A).scale(0.7)
    ylab.next_to(axes.y_axis.get_end(), LEFT, buff=0.18).shift(UP*0.08)
    xlab = MathTex(r"D", color=GRAY_A).scale(0.7)
    xlab.next_to(axes.x_axis.get_end(), DOWN, buff=0.18)

    def sig(x, k=8, x0=0): return 1/(1+np.exp(-k*(x-x0)))
    D0_x, Dg_x = 4.0, 9.0
    def y_blue(x):  return 0.95*(1 - sig(x, k=8, x0=D0_x))
    def y_red(x):   return 0.65*(1 - sig(x, k=8, x0=D0_x+0.6))
    def y_green(x): return 0.36*(1 - sig(x, k=8, x0=Dg_x))
    blue  = axes.plot(y_blue,  x_range=[0,10], color=BLUE_D,  stroke_width=5.5)
    red   = axes.plot(y_red,   x_range=[0,10], color=RED_D,   stroke_width=5.5)
    green = axes.plot(y_green, x_range=[0,10], color=GREEN_D, stroke_width=5.5)

    D0_bottom = axes.c2p(D0_x, 0); y_D0_red = y_red(D0_x); D0_top = axes.c2p(D0_x, y_D0_red)
    dash = DashedLine(D0_bottom, D0_top, dash_length=0.12, color=RED_D, stroke_width=2.6)
    dot  = Dot(D0_top, radius=0.06, color=RED_D)

    M1 = MathTex(r"\mathcal{M}_1", color=GRAY_A).scale(0.7).move_to(axes.c2p(1.1, 0.92)).shift(DOWN*0.12)
    M2 = MathTex(r"\mathcal{M}_2", color=GRAY_A).scale(0.7).move_to(axes.c2p(D0_x+0.35, y_D0_red+0.06))
    M3 = MathTex(r"\mathcal{M}_3", color=GRAY_A).scale(0.7).move_to(axes.c2p(7.6, 0.30))
    D0 = MathTex(r"D_0", color=GRAY_A).scale(0.7).next_to(D0_bottom, DOWN, buff=0.16)
    return VGroup(axes, ylab, xlab, blue, red, green, dash, dot, M1, M2, M3, D0)

class MachineLearning(Scene):
    def construct(self):
        write_speed = 8; subtitle_gap = 0.60; body_gap = 0.30

        # ===== Slide 0 
        t0 = Tex("-Aprendizaje Automático-", font_size=52)
        t0.set_color_by_tex("Aprendizaje Automático", BLUE)
        self.play(Write(t0, run_time=write_speed)); self.wait(0.8); self.play(FadeOut(t0))

        # ===== Slide 1 
        txt1 = Tex(r"Los elementos del aprendizaje automático son:", font_size=36)

        eqS = MathTex(r"\mathcal{S}=\{(x_1,y_1),\dots,(x_N,y_N)\}", font_size=40); colorize(eqS)

        F_sym  = MathTex(r"\mathcal{F}:", font_size=40); colorize(F_sym)
        F_text = Tex(r"Espacio de funciones (hipótesis)", font_size=36)
        eqF = VGroup(F_sym, F_text).arrange(RIGHT, buff=0.28).align_to(eqS, LEFT)

        A_sym  = MathTex(r"\mathcal{A}:", font_size=40); colorize(A_sym)
        A_text = Tex(r"Algoritmo de aprendizaje", font_size=36)
        eqA = VGroup(A_sym, A_text).arrange(RIGHT, buff=0.28).align_to(eqS, LEFT)

        L_sym  = MathTex(r"\ell\!\big(A_{\mathcal{F}}(\mathcal{S}) ,\, x ,\, y\big):", font_size=40); colorize(L_sym)
        L_text = Tex(r"función de pérdida", font_size=36)
        eqL = VGroup(L_sym, L_text).arrange(RIGHT, buff=0.28).align_to(eqS, LEFT)

        body1 = VGroup(txt1, eqS, eqF, eqA, eqL).arrange(DOWN, buff=0.22).move_to(ORIGIN)
        for t in (txt1, F_text, A_text, L_text): colorize(t) 
        self.play(Write(body1, run_time=write_speed)); self.wait(0.6); self.play(FadeOut(body1))

       # ===== Slide 2
        l1 = VGroup(
            Tex(r"Donde ", font_size=32).set_color(WHITE),
            MathTex(r"\mathcal{S}", font_size=32).set_color(TEAL_B),
            Tex(r" es un conjunto de datos, ", font_size=32).set_color(WHITE),
            MathTex(r"\mathcal{F}", font_size=32).set_color(PURPLE),
            Tex(r" es un espacio de funciones, donde se ", font_size=32).set_color(WHITE),
            Tex(r"busca la solución,", font_size=32).set_color(WHITE),
        ).arrange(RIGHT, buff=0.12)

        l2 = VGroup(
            Tex(r"la tarea del algoritmo de aprendizaje ", font_size=32).set_color(WHITE),
            MathTex(r"\mathcal{A}", font_size=32).set_color(GREEN),
            Tex(r" es buscar en ", font_size=32).set_color(WHITE),
            MathTex(r"\mathcal{F}", font_size=32).set_color(PURPLE),
            Tex(r" y la función de pérdida toma la instancia de una hipótesis", font_size=32).set_color(WHITE),
        ).arrange(RIGHT, buff=0.12)

        l3 = VGroup(
            Tex(r"que ha sido encontrada por ", font_size=32).set_color(WHITE),
            MathTex(r"\mathcal{A}", font_size=32).set_color(GREEN),
            Tex(r" en un conjunto ", font_size=32).set_color(WHITE),
            MathTex(r"\mathcal{S}", font_size=32).set_color(TEAL_B),
            Tex(r".", font_size=32).set_color(WHITE),
        ).arrange(RIGHT, buff=0.12)

        p_donde = VGroup(l1, l2, l3).arrange(DOWN, buff=0.16)

        SAFE_W = 0.88 * config.frame_width   
        SAFE_H = 0.80 * config.frame_height  
        if p_donde.width > SAFE_W:
            p_donde.set_width(SAFE_W)
        if p_donde.height > SAFE_H:
            p_donde.set_height(SAFE_H)


        p_donde.move_to(ORIGIN)

        self.play(Write(p_donde, run_time=write_speed))
        self.wait(0.6)
        self.play(FadeOut(p_donde, run_time=0.6))

        # ===== Slide 3 
        intro_ml = Tex(
            r"En Machine Learning lo que se busca es realizar una buena hipótesis, "
            r"este se encuentra minimizando el error esperado en todos los datos posibles:",
            font_size=32
        ).set_color(WHITE)

        e1 = MathTex(
            r"e(\mathcal{S}, \mathcal{A}, \mathcal{F}) = \mathbb{E}_{P(\{X,Y\})}"
            r"\big[\ell(\mathcal{A}_{\mathcal{F}}(\mathcal{S}),x,y)\big]",
            font_size=38
        )
        e2 = MathTex(
            r" = \int \ell \!\left(\mathcal{A}_{\mathcal{F}}(\mathcal{S}),x,y\right)\, p(\{x,y\})\, d\{x,y\}",
            font_size=38
        )
        e3 = MathTex(
            r"\approx \frac{1}{M} \sum\limits_{n=1}^{M} \ell(\mathcal{A}_{\mathcal{F}}(\mathcal{S}),x_n,y_n)",
            font_size=38
        )
        for m in (e1, e2, e3):
            colorize(m)  

        txt_emp = Tex(
            r"donde este ultimo termino es una estimación empírica del error a partir de una muestra de los datos.",
            font_size=32
        ).set_color(WHITE)

        body_err = VGroup(intro_ml, e1, e2, e3, txt_emp).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        self.play(Write(body_err, run_time=write_speed))
        self.wait(0.6)
        self.play(FadeOut(body_err))


        th_title = Tex(r"Teorema (No free lunch).", font_size=34).set_color(WHITE)

        l1a = Tex(r"Podemos encontrar una combinación de ", font_size=34).set_color(WHITE)
        saf_inline = MathTex(r"\{S, A, F\}", font_size=34).set_color(WHITE)
        saf_inline.set_color_by_tex("S", TEAL_B)
        saf_inline.set_color_by_tex("A", GREEN)
        saf_inline.set_color_by_tex("F", PURPLE)
        l1b = Tex(r" que haga que ", font_size=34).set_color(WHITE)
        e_inline = MathTex(r"e(S, A, F)", font_size=34).set_color(WHITE)
        l1c = Tex(r" tome un valor arbitrario.", font_size=34).set_color(WHITE)
        th_line = VGroup(l1a, saf_inline, l1b, e_inline, l1c).arrange(RIGHT, buff=0.08)

        exp1 = Tex(
            r"Esto nos dice que si tenemos un numero infinito de posibles datos, entonces se",
            font_size=32
        ).set_color(WHITE)
        exp2 = Tex(
            r"tiene un espacio muestral infinito, donde solo se ve un conjunto finito de datos",
            font_size=32
        ).set_color(WHITE)
        exp3 = Tex(
            r"a partir de esto, entonces es posible llegar a una combinación de algoritmos,",
            font_size=32
        ).set_color(WHITE)
        exp4 = Tex(
            r"conjunto de datos e hipótesis que le da a este error un valor arbitrario.",
            font_size=32
        ).set_color(WHITE)

        txt_sig = Tex(
            r"Lo que sigue es hacer suposiciones, sin estas es imposible aprender",
            font_size=32
        ).set_color(WHITE)

        th_block = VGroup(th_title, th_line).arrange(DOWN, buff=0.20)
        exp_block = VGroup(exp1, exp2, exp3, exp4, txt_sig).arrange(DOWN, buff=0.10)
        blk = VGroup(th_block, exp_block).arrange(DOWN, buff=0.28)

        SAFE_W = 0.88 * config.frame_width   
        SAFE_H = 0.80 * config.frame_height  

        if blk.width > SAFE_W:
            blk.set_width(SAFE_W)
        if blk.height > SAFE_H:
            blk.set_height(SAFE_H)
        blk.move_to(ORIGIN)
        
        self.play(Write(blk, run_time=write_speed))
        self.wait(0.6)
        self.play(FadeOut(blk))

        # Slide 6
        sup = Tex(
            r"La técnica del Machine Learning no es mas que ajustar curvas sobre supuestos: datos indenticamente distribuidos ya sean independientes o correlacionados, ruido gaussiano. etc. ; para abordar esto, se utilza el siguiente definición:",
            font_size=34
        ).set_color(WHITE)

     
        df_l1  = Tex(r"(Proceso Gaussiano): “Es una colección infinita de variables aleatorias", font_size=32).set_color(WHITE)
        df_l2  = Tex(r"tal que cualquier subconjunto es conjuntamente gaussiano.”", font_size=32).set_color(WHITE)
        df_block = VGroup(df_l1, df_l2).arrange(DOWN, buff=0.06)


        exp1_a = Tex(r"Esto significa, que en un eje ", font_size=32).set_color(WHITE)
        exp1_x = MathTex(r"x", font_size=32); colorize(exp1_x)
        exp1_b = Tex(r", se pueden tomar diferentes proporciones y en", font_size=32).set_color(WHITE)
        exp_line1 = VGroup(exp1_a, exp1_x, exp1_b).arrange(RIGHT, buff=0.06)

        exp2 = Tex(
            r"cualquiera de estas se toma la colección donde las salidas se alojan conjuntamente.",
            font_size=32
        ).set_color(WHITE)

        exp_block = VGroup(exp_line1, exp2).arrange(DOWN, buff=0.06)

        body_pg = VGroup(sup, df_block, exp_block).arrange(DOWN, buff=0.30)
        SAFE_W = 0.88 * config.frame_width   
        SAFE_H = 0.80 * config.frame_height  

        if body_pg.width > SAFE_W:
            body_pg.set_width(SAFE_W)
        if body_pg.height > SAFE_H:
            body_pg.set_height(SAFE_H)

        body_pg.move_to(ORIGIN)

        self.play(Write(body_pg, run_time=write_speed))
        self.wait(0.6)
        self.play(FadeOut(body_pg))

        # Proceso Gaussiano 
        ax = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1.05, 0.25],
            tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        ).scale(0.9).to_edge(DOWN, buff=0.7)

        x_label = MathTex("x").next_to(ax.x_axis.get_right(), UR, buff=0.2).set_color(TEAL_B)

        self.play(FadeIn(ax, shift=UP), FadeIn(x_label), run_time=0.7)

        # Familia de gaussianas 
        def normal_pdf(mu, sigma):
            c = 1.0 / (sigma * math.sqrt(2 * math.pi))
            inv2s2 = 1.0 / (2 * sigma * sigma)
            return lambda x: c * math.exp(-(x - mu) ** 2 * inv2s2)

        params = [(-2.0, 0.7), (-0.8, 0.9), (0.0, 0.6), (1.2, 1.1), (2.2, 0.8)]
        curves = VGroup()
        for i, (mu, sg) in enumerate(params):
            f = normal_pdf(mu, sg)
            g = ax.plot(
                f, x_range=[-4, 4], use_smoothing=True,
                color=BLUE_B if i % 2 == 0 else PURPLE_B,
                stroke_opacity=0.55, stroke_width=4
            )
            curves.add(g)

        self.play(
            LaggedStart(*[FadeIn(c, shift=0.2*UP, scale=0.98) for c in curves],
                        lag_ratio=0.18, run_time=1.6)
        )
        self.wait(0.2)

        xs = [-2.0, 0.2, 1.6, 2.6]
        dots = VGroup(*[Dot(ax.c2p(x, 0), radius=0.055, color=YELLOW) for x in xs])
        selector = SurroundingRectangle(
            dots, color=YELLOW, buff=0.22, corner_radius=0.12, stroke_opacity=0.8
        )

        self.play(FadeIn(dots, scale=0.8), Create(selector), run_time=0.8)
        self.wait(0.2)

        self.play(
            dots.animate.set_color(TEAL_B).scale(1.12),
            selector.animate.set_stroke(TEAL_B, opacity=0.9),
            rate_func=there_and_back, run_time=0.8
        )
        self.wait(0.1)

        emph = Tex(r"“Cualquier \, subconjunto \, es \, conjuntamente \, \textit{gaussiano}”").scale(0.7)
        emph.set_color_by_tex("gaussiano", YELLOW)
        emph.to_corner(UL).shift(0.25*DOWN + 0.2*RIGHT)

        self.play(Write(emph), run_time=0.8)
        self.play(Indicate(emph.get_part_by_tex("gaussiano"), color=YELLOW, scale_factor=1.07))
        self.wait(0.6)

        fade_grp = VGroup(ax, x_label, curves, dots, selector, emph)
        self.play(FadeOut(fade_grp), run_time=0.8)


        # ===== Slide 7 =====
        comp_title = Tex(r"Una red neuronal es simplemente una composición de funciones:", font_size=34); colorize(comp_title)
        comp_eq = MathTex(r"y = f_k(f_{k-1}(\dots f_0(x))) = f_k \circ f_{k-1} \circ \cdots \circ f_1(x)", font_size=38); colorize(comp_eq)
        head = VGroup(comp_title, comp_eq).arrange(DOWN, buff=body_gap).move_to(ORIGIN)

        self.play(Write(comp_title, run_time=write_speed*0.7))
        self.play(Write(comp_eq, run_time=write_speed)); self.wait(0.4)

        def _func_box(tex, col=GREEN):
            box = RoundedRectangle(corner_radius=0.2, width=1.6, height=1.0, stroke_width=2.6, color=WHITE)
            lab = MathTex(tex).scale(0.9).set_color(col).move_to(box.get_center())
            return VGroup(box, lab)

        x_tok = MathTex(r"\mathbf{x}", color=BLUE).scale(1.05)
        f1 = _func_box(r"f_1"); f2 = _func_box(r"f_2"); fk = _func_box(r"f_k")
        y_tok = MathTex(r"y", color=ORANGE).scale(1.05)
        
        pipe_boxes = VGroup(x_tok, f1, f2, fk, y_tok).arrange(RIGHT, buff=0.6).move_to(DOWN*1.6)

        cd = MathTex(r"\cdots").set_color(GREY_B).scale(1.0)
        cd.move_to(midpoint(f2.get_right(), fk.get_left()))
        fk.shift(0.35*RIGHT); y_tok.shift(0.35*RIGHT); cd.shift(0.12*LEFT)

        a01 = Arrow(x_tok.get_right(), f1.get_left(), buff=0.1, color=GREY_B)
        a12 = Arrow(f1.get_right(),   f2.get_left(), buff=0.1, color=GREY_B)
        a2d = Arrow(f2.get_right(),   cd.get_left(),  buff=0.10, color=GREY_B)   
        adk = Arrow(cd.get_right(),   fk.get_left(),  buff=0.10, color=GREY_B)  
        aky = Arrow(fk.get_right(),   y_tok.get_left(), buff=0.1, color=GREY_B)

        dot = Dot(radius=0.08, color=YELLOW).move_to(x_tok.get_right()+RIGHT*0.05)

        pipe_group = VGroup(x_tok, f1, f2, cd, fk, y_tok, a01, a12, a2d, adk, aky, dot)

        self.play(FadeIn(x_tok), Create(f1), Create(a01))
        self.play(Create(f2), Create(a12))
        self.play(FadeIn(cd), Create(a2d))       
        self.play(Create(fk), Create(adk))
        self.play(FadeIn(y_tok), Create(aky))

        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, a01.copy()), run_time=0.5); self.play(Indicate(f1, color=GREEN), run_time=0.3)
        self.play(MoveAlongPath(dot, a12.copy()), run_time=0.5); self.play(Indicate(f2, color=GREEN), run_time=0.3)
        self.play(MoveAlongPath(dot, a2d.copy()), run_time=0.45)
        self.play(MoveAlongPath(dot, adk.copy()), run_time=0.45)
        self.play(MoveAlongPath(dot, aky.copy()), run_time=0.5); self.play(Flash(y_tok, color=ORANGE, flash_radius=0.5), run_time=0.4)

        comp_chain = MathTex(r"f_k \circ f_{k-1} \circ \cdots \circ f_1", font_size=34)
        colorize(comp_chain, {r"f": GREEN})
        comp_chain.next_to(pipe_group, DOWN, buff=0.35)

        self.play(Write(comp_chain), run_time=0.6); self.wait(0.6)

        container = VGroup(head, pipe_group, comp_chain)
        self.play(container.animate.arrange(DOWN, buff=0.6).move_to(ORIGIN), run_time=0.6)

        self.play(FadeOut(container))

        # ===== Slide 8 =====
        ker_parts = [
            MathTex(r"\operatorname{Kern}(f_1)", font_size=32),
            MathTex(r"\subseteq~\operatorname{Kern}(f_{2}\!\circ f_{1})", font_size=32),
            MathTex(r"\subseteq~\operatorname{Kern}(f_{k}\!\circ\cdots\!\circ f_{1})", font_size=32),
        ]
        im_parts = [
            MathTex(r"\operatorname{Im}(f_{k}\!\circ\cdots\!\circ f_{1})", font_size=32),
            MathTex(r"\subseteq~\operatorname{Im}(f_{k}\!\circ\cdots\!\circ f_{2})", font_size=32),
            MathTex(r"\subseteq~\operatorname{Im}(f_{k})", font_size=32),
        ]
        for m in ker_parts + im_parts:
            colorize(m)

        ker_eq_row = VGroup(*ker_parts).arrange(RIGHT, buff=0.18)
        im_eq_row  = VGroup(*im_parts ).arrange(RIGHT, buff=0.18)

        panel_W, panel_H = 4.8, 1.7
        panel_box_buff   = 0.28

        k_frame1 = Rectangle(width=panel_W-2.0, height=panel_H-1.2, stroke_color=BLUE_D,  stroke_width=3.0)
        k_frame2 = Rectangle(width=panel_W-1.2, height=panel_H-0.8, stroke_color=BLUE_D,  stroke_width=3.2)
        k_frame3 = Rectangle(width=panel_W-0.2, height=panel_H-0.3, stroke_color=BLUE_D,  stroke_width=3.4)
        k_frames = VGroup(k_frame1, k_frame2, k_frame3).move_to(ORIGIN)
        k_panel_box = SurroundingRectangle(k_frames, buff=panel_box_buff, corner_radius=0.16,
                                        stroke_color=GRAY_B, stroke_width=2.4)
        legend_kernel = Tex(
            r"Si $f_1(v)=0$, entonces cualquier composición también da $0$.\\[4pt]"
            r"Por eso el kernel \textit{crece} con la composición.",
            font_size=28, tex_environment="flushleft",
        )

        col_ker = VGroup(ker_eq_row, VGroup(k_panel_box, k_frames), legend_kernel).arrange(DOWN, buff=0.28)

        i_frame1 = Rectangle(width=panel_W-0.2, height=panel_H-0.3, stroke_color=GREEN_D, stroke_width=3.0)
        i_frame2 = Rectangle(width=panel_W-1.2, height=panel_H-0.8, stroke_color=GREEN_D, stroke_width=3.2)
        i_frame3 = Rectangle(width=panel_W-2.0, height=panel_H-1.2, stroke_color=GREEN_D, stroke_width=3.4)
        i_frames = VGroup(i_frame1, i_frame2, i_frame3).move_to(ORIGIN)
        i_panel_box = SurroundingRectangle(i_frames, buff=panel_box_buff, corner_radius=0.16,
                                        stroke_color=GRAY_B, stroke_width=2.4)
        legend_imagen = Tex(
            r"Cada función ``filtra'' salidas posibles; la imágen "
            r"\textit{se reduce} paso a paso.",
            font_size=28
        )

        col_im = VGroup(im_eq_row, VGroup(i_panel_box, i_frames), legend_imagen).arrange(DOWN, buff=0.28)
 
        intro8 = Tex(
            r"El kernel de una función es el número de valores en la entrada que asigna el mismo valor en la salida "
            r"y la imagen son todos los valores que contiene la salida y esto para funciones compuestas:",
            font_size=32
        ).set_color(WHITE)

        row = VGroup(col_ker, col_im).arrange(RIGHT, buff=1.0)
        container = VGroup(intro8, row).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        frame_w = config.frame_width
        frame_h = config.frame_height
        TOP_MARGIN, BOTTOM_MARGIN, SIDE_MARGIN = 0.35, 0.52, 0.40
        max_h = frame_h - (TOP_MARGIN + BOTTOM_MARGIN)
        max_w = frame_w - (2 * SIDE_MARGIN)
        scale = min(1.0, max_h / container.height, max_w / container.width)
        container.scale(scale).move_to(ORIGIN)

        group = VGroup(container) 
        self.play(Write(intro8, run_time=write_speed*0.6))
        self.play(FadeIn(row, shift=UP*0.1), run_time=0.8)
        self.wait(0.2)

        def blink(mobj, col=YELLOW): return Indicate(mobj, color=col, scale_factor=1.03)

        k_frame2.set_stroke(opacity=0.0); k_frame3.set_stroke(opacity=0.0)
        i_frame2.set_stroke(opacity=0.0); i_frame3.set_stroke(opacity=0.0)

        self.play(Create(k_frame1, run_time=0.45)); self.play(blink(ker_parts[0]), run_time=0.35)
        self.play(Create(i_frame1, run_time=0.45)); self.play(blink(im_parts[0]),  run_time=0.35)

        self.play(k_frame2.animate.set_stroke(opacity=1.0), run_time=0.45); self.play(blink(ker_parts[1]), run_time=0.35)
        self.play(i_frame2.animate.set_stroke(opacity=1.0), run_time=0.45); self.play(blink(im_parts[1]),  run_time=0.35)

        self.play(k_frame3.animate.set_stroke(opacity=1.0), run_time=0.45); self.play(blink(ker_parts[2]), run_time=0.35)
        self.play(i_frame3.animate.set_stroke(opacity=1.0), run_time=0.45); self.play(blink(im_parts[2]),  run_time=0.35)

        self.wait(0.6)
        self.play(FadeOut(group))

        # ===== Slide 9 =====
        m1 = Tex(r"El aprendizaje automático se puede representar a través de la gráfica de Mackay:", font_size=32)
        m2 = Tex(
            r"esto nos dice que se debe de elegir el modelo que mas $p(\mathcal{D}_{0},\mathcal{M})$ "
            r"asigna a los datos antes de verlos, en este caso:", font_size=32
        )
        m3 = MathTex(
            r"\mathcal{M}_2 \quad \text{mayor altura en} \quad \mathcal{D}_0 \Rightarrow \text{Mejor capacidad predictiva}",
            font_size=36
        )
        for t in (m2): colorize(t)
        colorize(m3)

        graph = build_mackay_graph().scale(0.95)
    
        body = VGroup(m1, graph, m2, m3).arrange(DOWN, buff=0.30)
        body.move_to(ORIGIN)

        self.play(Write(m1, run_time=write_speed*0.7))

        axes, ylab, xlab, blue, red, green, dash, dot, M1, M2, M3, D0 = graph
        self.play(Create(axes, run_time=1.0))
        self.play(Write(ylab), Write(xlab), run_time=0.6)
        self.play(Create(blue, run_time=0.9))
        self.play(Create(red,  run_time=0.8))
        self.play(Create(green,run_time=0.8))
        self.play(Create(dash), FadeIn(dot), Write(D0), run_time=0.6)
        self.play(Write(M1), Write(M2), Write(M3), run_time=0.8)

        self.play(Write(m2, run_time=write_speed*0.7))
        self.play(Write(m3, run_time=write_speed*0.7))
        self.wait(0.6)

        self.play(FadeOut(VGroup(body)))
        
        # ===== Slide 10 =====
        txt10 = Tex(
            r"Lo cual no aplica para funciones compuestas, ya que estas reorganizan el\\"
            r"espacio de entradas para concentrar los datos en un punto y puede\\"
            r"existir un modelo muy simple que maximice la probabilidad en el mismo\\" 
            r"punto que un modelo más complejo.",
            font_size=32
        ).set_color(WHITE)

        txt10.move_to(ORIGIN)

        self.play(Write(txt10, run_time=write_speed))
        self.wait(0.6)
        self.play(FadeOut(txt10))

        # ===== Slide 11 
        cierre = Tex(
            r"Otro aspecto de la composici\'on de funciones es la incertidumbre, "
            r"aqu\'i est\'a la aplicaci\'on de los procesos Gaussianos",
            font_size=32
        ); colorize(cierre)
        header_pg = VGroup(cierre).arrange(DOWN, buff=subtitle_gap)

        def rect_frame(w, h, stroke=2.5, color=WHITE):
            r = RoundedRectangle(width=w, height=h, corner_radius=0.12)
            r.set_stroke(color=color, width=stroke).set_fill(BLACK, 0)
            return r

        W, H, GAP = 10.5, 1.7, 0.35
        p_top, p_mid, p_bot = rect_frame(W,H), rect_frame(W,H), rect_frame(W,H)
        panels = VGroup(p_top, p_mid, p_bot).arrange(DOWN, buff=GAP)

        MEAN_COLOR, SAMPLE_COLOR, BAND_COLOR = BLUE_B, BLUE_C, BLUE_B
        cap = Tex("ya que define una distribuci\\'on sobre posibles funciones.").scale(0.7).set_color(WHITE)
        cap.next_to(panels, DOWN, buff=0.28)

        body = VGroup(header_pg, panels, cap).arrange(DOWN, buff=body_gap)
        SAFE_W = 0.88 * config.frame_width
        SAFE_H = 0.86 * config.frame_height
        if body.width > SAFE_W:  body.set_width(SAFE_W)
        if body.height > SAFE_H: body.set_height(SAFE_H)
        body.move_to(ORIGIN)
-
        self.play(Write(header_pg, run_time=write_speed))
        self.play(FadeIn(VGroup(panels, cap), shift=0.2*UP), run_time=0.6)

        def make_curve_in_rect(rect, yfun, n=250):
            L, R, T, B = rect.get_left(), rect.get_right(), rect.get_top(), rect.get_bottom()
            x0, x1 = L[0]+0.18, R[0]-0.18
            y0, y1 = B[1]+0.18, T[1]-0.18
            xs = np.linspace(0,1,n)
            pts = []
            for t in xs:
                x = x0 + (x1-x0)*t
                y = (y0+y1)/2 + (y1-y0)*0.5 * np.clip(yfun(t), -1, 1)
                pts.append(np.array([x,y,0]))
            path = VMobject()
            path.set_points_smoothly(pts)  
            return path
        def dashed_copy(vmobj, dash_len=0.18, gap_len=0.12,
                        color=SAMPLE_COLOR, width=3.0, opacity=0.85):
            total = float(dash_len + gap_len)
            ratio = (dash_len / total) if total > 0 else 0.5
            try:
                L = vmobj.get_length()
            except Exception:
                L = 10.0
            num = max(2, int(L / max(total, 1e-3)))
            d = DashedVMobject(vmobj, num_dashes=num, dashed_ratio=ratio)
            d.set_stroke(color=color, width=width, opacity=opacity)
            return d
        
        phi_top, phi_mid, phi_bot = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)

        def y_top_mean(t):   return 0.05 + 0.15*(t-0.5) + 0.06*np.sin(2*np.pi*t)
        def y_top_sample(t, phi):
            return y_top_mean(t) + 0.10*np.sin(2*np.pi*1.2*t + phi) + 0.06*np.sin(2*np.pi*2.4*t + 0.7*phi)
        mean_top = always_redraw(lambda: make_curve_in_rect(p_top, y_top_mean).set_stroke(MEAN_COLOR, 5.5, 1.0))
        s1_top   = always_redraw(lambda: dashed_copy(make_curve_in_rect(p_top, lambda t: y_top_sample(t, phi_top.get_value())), 0.22, 0.14))
        s2_top   = always_redraw(lambda: dashed_copy(make_curve_in_rect(p_top, lambda t: y_top_sample(t, phi_top.get_value()+1.7)), 0.22, 0.14, opacity=0.75))

        def y_mid_mean(t):   return 0.35*np.sin(2*np.pi*(t-0.05))
        def y_mid_sample(t, phi):
            return y_mid_mean(t) + 0.12*np.sin(2*np.pi*1.8*t + phi) + 0.05*np.cos(2*np.pi*3.0*t - 0.4*phi)
        mean_mid = always_redraw(lambda: make_curve_in_rect(p_mid, y_mid_mean).set_stroke(MEAN_COLOR, 5.5, 1.0))
        s1_mid   = always_redraw(lambda: dashed_copy(make_curve_in_rect(p_mid, lambda t: y_mid_sample(t, phi_mid.get_value())), 0.22, 0.14))
        s2_mid   = always_redraw(lambda: dashed_copy(make_curve_in_rect(p_mid, lambda t: y_mid_sample(t, phi_mid.get_value()+1.3)), 0.22, 0.14, opacity=0.75))

        def y_bot_mean(t): return 0.25*np.sin(2*np.pi*2.0*t + 0.2) - 0.02
        def y_bot_upp(t, phi): return y_bot_mean(t) + 0.18 + 0.08*np.sin(2*np.pi*1.4*t + phi)
        def y_bot_low(t, phi): return y_bot_mean(t) - 0.18 + 0.08*np.sin(2*np.pi*1.4*t + phi + np.pi)

        upper_bot = always_redraw(lambda: make_curve_in_rect(p_bot, lambda t: y_bot_upp(t, phi_bot.get_value())).set_stroke(SAMPLE_COLOR, 0))
        lower_bot = always_redraw(lambda: make_curve_in_rect(p_bot, lambda t: y_bot_low(t,  phi_bot.get_value())).set_stroke(SAMPLE_COLOR, 0))

        def band_polygon():
            up, lo = upper_bot.copy(), lower_bot.copy()
            up_pts, lo_pts = up.get_points(), lo.get_points()[::-1]
            poly = Polygon(*list(up_pts)+list(lo_pts)).set_fill(BAND_COLOR, 0.15).set_stroke(BAND_COLOR, 0)
            return poly

        band_bot = always_redraw(band_polygon)
        mean_bot = always_redraw(lambda: make_curve_in_rect(p_bot, y_bot_mean).set_stroke(MEAN_COLOR, 5.5, 1.0))
        s1_bot   = always_redraw(lambda: dashed_copy(make_curve_in_rect(p_bot, lambda t: y_bot_mean(t)+0.10*np.sin(2*np.pi*1.6*t+phi_bot.get_value())), 0.22,0.14, opacity=0.85))
        s2_bot   = always_redraw(lambda: dashed_copy(make_curve_in_rect(p_bot, lambda t: y_bot_mean(t)-0.10*np.sin(2*np.pi*1.6*t-phi_bot.get_value())), 0.22,0.14, opacity=0.75))

        grp_top, grp_mid, grp_bot = VGroup(s1_top, s2_top, mean_top), VGroup(s1_mid, s2_mid, mean_mid), VGroup(band_bot, s1_bot, s2_bot, mean_bot)

        self.play(
            LaggedStartMap(FadeIn, grp_top, shift=0.08*UP, lag_ratio=0.15),
            LaggedStartMap(FadeIn, grp_mid, shift=0.08*UP, lag_ratio=0.15),
            LaggedStartMap(FadeIn, grp_bot, shift=0.08*UP, lag_ratio=0.15),
            run_time=1.2
        )
        T = 5.0
        self.play(
            phi_top.animate.increment_value(2*np.pi),
            phi_mid.animate.increment_value(2*np.pi),
            phi_bot.animate.increment_value(2*np.pi),
            rate_func=there_and_back, run_time=T
        )

        self.play(FadeOut(VGroup(body, grp_top, grp_mid, grp_bot)), run_time=0.8)


# manim -pqh MachineLearning.py MachineLearning
