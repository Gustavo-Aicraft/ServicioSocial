from manim import *
import numpy as np
from manim import config
config.tex_template.add_to_preamble(r"\usepackage{amsmath}")

class RegresionLineal(Scene):
    def construct(self):
        write_speed = 5  
      # --- Slide 1: Título ---
        title = Tex("REGRESIÓN LINEAL", font_size=52)
        title.set_color_by_tex("REGRESIÓN LINEAL", BLUE)
        self.play(Write(title, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(title))
        p1 = Tex(
            r"El objetivo de la regresión es predecir el valor de una o más "
            r"variables objetivo dado un vector de variables de entrada.",
            font_size=36    
        )

        eq =MathTex(
            r"y = w_0 + w_1 x_1",
            font_size=40
        )
        eq.set_color_by_tex(r"y", YELLOW)
        eq.set_color_by_tex(r"x_1", BLUE)
        eq.set_color_by_tex(r"w_0", GREEN)
        eq.set_color_by_tex(r"w_1", GREEN)

        p2 = Tex(
            r"Denotamos ",
            r"$y(x,w)$",
            r" cuyos valores para las nuevas entradas ",
            r"$x$",
            r" constituyen las predicciones para los valores correspondientes de ",
            r"$t$",
            r" y donde ",
            r"$w$",
            r" representa un vector de parámetros que se pueden aprender de los datos de entrenamiento.",
            r" Así, generalizando el modelo simple: ",
            font_size=36
        )
        p2[1].set_color(YELLOW) 
        p2[3].set_color(BLUE)   
        p2[5].set_color(RED)    
        p2[7].set_color(GREEN)  

        eq2 = Tex(
            r"$y(\mathbf{x}, \mathbf{w}) = w_0 + w_1 x_1 + \ldots + w_D x_D$",
            font_size=40,
            color=PURPLE
        )

        p1.move_to(ORIGIN + UP*1.8)
        eq.next_to(p1, DOWN, buff=0.5)
        p2.next_to(eq, DOWN, buff=0.5)
        eq2.next_to(p2, DOWN, buff=0.8)

        self.play(Write(p1, run_time=write_speed))
        self.play(Write(eq, run_time=write_speed))
        self.play(Write(p2, run_time=write_speed))
        self.play(Write(eq2, run_time=write_speed))

        self.wait(6)
        self.play(FadeOut(VGroup(p1, eq, p2, eq2)))


        # --- Slide 2 B
        axes = Axes(x_range=[0,6], y_range=[0,10], axis_config={"color": BLUE}).scale(0.8).to_edge(DOWN)
        labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(labels))

        puntos = [(1,2), (2,3), (3,4.2), (4,6), (5,7.8)]
        dots = VGroup(*[Dot(axes.c2p(x,y), color=YELLOW) for x,y in puntos])
        self.play(FadeIn(dots, shift=UP))

        linea = axes.plot(lambda x: 1.2*x + 0.5, color=RED)
        self.play(Create(linea))
        self.wait(1)

        formula1 = MathTex(
            r"y=w_0 + w_1x_1",
            font_size=42
        ).next_to(linea, UP, buff=1)
        self.play(TransformFromCopy(linea, formula1))
        self.wait(1)

        self.play(FadeOut(VGroup(axes, labels, dots, linea, formula1)))

        # --- Slide 3: Funciones Base
        basis_title = Tex("Funciones base", font_size=44).to_edge(UP)
        basis_title.set_color_by_tex("Funciones base", ORANGE)
        self.play(Write(basis_title, run_time=write_speed))

        p4 = Tex(
            r"El modelo lineal simple se puede extender considerando combinaciones "
            r"lineales de funciones no lineales fijas de las variables de entrada de la forma:",
            font_size=32
        )
        p4.set_line_spacing(1)
        p4.next_to(basis_title, DOWN, buff=0.7)
        self.play(Write(p4, run_time=write_speed))

        formula2 = MathTex(
            r"y(x,w) = w_0 + \sum\limits_{j=1}^{M-1} w_j \phi_j(x)",
            font_size=44
        ).next_to(p4, DOWN, buff=0.7)
        self.play(Write(formula2, run_time=write_speed))

        p5 = MathTex(
            r"\text{donde } \phi_j(x) \text{ es conocido como función base.}",
            font_size=32
        ).next_to(formula2, DOWN, buff=0.7)
        self.play(Write(p5, run_time=write_speed))

        p6 = Tex(
            r"Estas permiten transformar las variables originales en nuevas "
            r"representaciones que permiten capturar relaciones más complejas "
            r"entre las entradas y las salidas.",
            font_size=32
        )
        p6.set_line_spacing(1)
        p6.next_to(p5, DOWN, buff=0.5)
        self.play(Write(p6, run_time=write_speed))

        self.wait(4)
        self.play(FadeOut(VGroup(basis_title, p4, formula2, p5, p6)))

        axes2 = Axes(x_range=[-3,3], y_range=[-1,3], axis_config={"color": BLUE})\
            .scale(0.8).to_edge(DOWN).shift(LEFT*3.0)  

        labels2 = axes2.get_axis_labels(x_label="x", y_label=MathTex(r"\phi(x)"))
        self.play(Create(axes2), Write(labels2))

        mu_s, s_s = 0.0, 2.0     # sigmoidal
        mu_g, s_g = 0.0, 1.2     # gaussiana

        phi1 = axes2.plot(lambda x: x**2/4, color=GREEN)                                    # Polinomio
        phi2 = axes2.plot(lambda x: 1/(1+np.exp(-((x-mu_s)/s_s))), color=ORANGE)            # Sigmoidal
        phi3 = axes2.plot(lambda x: np.exp(-((x-mu_g)**2)/(2*(s_g**2))), color=PURPLE)      # Gaussiana

        leg1 = MathTex(r"\phi_1(x)=x^2/4", font_size=32, color=GREEN)
        leg2 = MathTex(r"\phi_2(x)=\sigma\!\left(\frac{x-\mu}{s}\right)", font_size=32, color=ORANGE)
        sigma_def = MathTex(r"\sigma(a)=\frac{1}{1+e^{-a}}", font_size=26, color=ORANGE)
        leg3 = MathTex(
            r"\phi_3(x)=\exp\!\left(-\frac{(x-\mu)^2}{2s^2}\right)",
            font_size=32, color=PURPLE
        )

        legend = VGroup(leg1, leg2, sigma_def, leg3).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.scale(0.9)
        legend.to_corner(UR, buff=0.55).shift(LEFT*0.2 + DOWN*0.05)

        legend_bg = BackgroundRectangle(
            legend, fill_opacity=0.88, fill_color=BLACK, stroke_width=0, buff=0.18
        )

        self.play(Create(phi1), run_time=write_speed); self.play(Write(leg1))
        self.play(Create(phi2), run_time=write_speed); self.play(Write(leg2))
        self.play(FadeIn(sigma_def, shift=UP*0.1))
        self.play(Create(phi3), run_time=write_speed); self.play(Write(leg3))

        self.play(FadeIn(legend_bg), run_time=0.2)
        self.bring_to_front(legend)

        formula_general = MathTex(
            r"y(x,w) = w_0 + \sum\limits_{j=1}^{M-1} w_j \phi_j(x)",
            font_size=44
        ).next_to(axes2, UP, buff=0.8)
        self.play(Write(formula_general, run_time=write_speed))
        self.wait(2)

        self.play(FadeOut(VGroup(axes2, labels2, phi1, phi2, phi3, legend, formula_general)))

        self.wait(0.3)

        left_x = -3.8
        top_y  = 1.8
        vgap   = 1.4
        radius = 0.45
        out_node2 = Circle(radius=radius, color=BLUE, stroke_width=4).set_fill("#90CAF9", opacity=0.35)
        out_node2.move_to(RIGHT*3.2 + UP*0.2)
        out_label2 = MathTex(r"y(\mathbf{x},\mathbf{w})").scale(0.9)
        out_label2.next_to(out_node2, RIGHT, buff=0.35)
        out_label2.set_color(WHITE)
        out_label2.set_color_by_tex("y", YELLOW)
        out_label2.set_color_by_tex(r"\mathbf{x}", BLUE)
        out_label2.set_color_by_tex(r"\mathbf{w}", GREEN)

        node_top2    = Circle(radius=radius, color=BLUE, stroke_width=4).set_fill("#90CAF9", opacity=0.35).move_to([left_x, top_y, 0])
        node_mid2    = Circle(radius=radius, color=BLUE, stroke_width=4).set_fill("#90CAF9", opacity=0.35).move_to([left_x, top_y - vgap, 0])
        node_bottom2 = Circle(radius=radius, color=BLUE, stroke_width=4).set_fill("#0D47A1", opacity=1.0).move_to([left_x, top_y - 2*vgap, 0])

        phi_top2 = MathTex(r"\phi_{M-1}(\mathbf{x})").scale(0.9).next_to(node_top2, LEFT, buff=0.35)
        phi_mid2 = MathTex(r"\phi_{1}(\mathbf{x})").scale(0.9).next_to(node_mid2, LEFT, buff=0.35)
        phi_bot2 = MathTex(r"\phi_{0}(\mathbf{x})").scale(0.9).next_to(node_bottom2, LEFT, buff=0.35)

        vdots2 = MathTex(r"\vdots").move_to([left_x, (node_top2.get_y()+node_mid2.get_y())/2, 0])

        a_top2 = Arrow(node_top2.get_right(),    out_node2.get_left(), buff=0.05, stroke_width=6)
        a_mid2 = Arrow(node_mid2.get_right(),    out_node2.get_left(), buff=0.05, stroke_width=6)
        a_bot2 = Arrow(node_bottom2.get_right(), out_node2.get_left(), buff=0.05, stroke_width=6)

       
        def label_for_arrow(arrow, tex, *, t=0.58, dn=0.62, side=1):
            """
            Coloca una etiqueta MathTex en la flecha 'arrow' a la altura 't' (0..1),
            separada 'dn' en la dirección perpendicular. side=+1 arriba, -1 abajo.
            """
            lab = MathTex(tex, color=GREEN).scale(0.9)
            p = arrow.point_from_proportion(t)
            v = arrow.get_end() - arrow.get_start()
            v = v / np.linalg.norm(v)
            n = np.array([-v[1], v[0], 0.0]) * side  # normal 90°
            lab.move_to(p + dn * n)
            bg = BackgroundRectangle(lab, fill_color=BLACK, fill_opacity=1.0, stroke_width=0, buff=0.02)
            return VGroup(bg, lab)

        w_top2 = label_for_arrow(a_top2, r"w_{M-1}", t=0.44, dn=0.64, side=+1)
        w_mid2 = label_for_arrow(a_mid2, r"w_{0}",    t=0.54, dn=0.66, side=-1)
        w_bot2 = label_for_arrow(a_bot2, r"w_{1}",    t=0.64, dn=0.68, side=+1)

        eq_basis2 = MathTex(
            r"y(\mathbf{x},\mathbf{w}) =",
            r"w_{0}\,\phi_{0}(\mathbf{x})",
            r"+\,w_{1}\,\phi_{1}(\mathbf{x})",
            r"+\,\cdots",
            r"+\,w_{M-1}\,\phi_{M-1}(\mathbf{x})",
        ).scale(0.90).to_edge(DOWN, buff=0.55)

        eq_basis2[0].set_color_by_tex_to_color_map({
            r"y": YELLOW, r"\mathbf{x}": BLUE, r"\mathbf{w}": GREEN
        })
        for i in (1, 2, 4):
            eq_basis2[i].set_color(WHITE)
            eq_basis2[i].set_color_by_tex_to_color_map({
                r"w_{": GREEN, r"\phi": YELLOW, r"\mathbf{x}": BLUE
            })
        eq_basis2_bg = BackgroundRectangle(eq_basis2, fill_color=BLACK, fill_opacity=1.0, stroke_width=0, buff=0.08)

        self.play(LaggedStart(Create(node_top2), Create(node_mid2), Create(node_bottom2),
                              lag_ratio=0.15, run_time=1.0))
        self.play(Write(phi_top2), Write(phi_mid2), Write(phi_bot2), run_time=0.9)
        self.play(FadeIn(vdots2, scale=0.9), run_time=0.4)

        self.play(Create(out_node2), Write(out_label2), run_time=0.8)
        self.play(LaggedStart(GrowArrow(a_top2), GrowArrow(a_mid2), GrowArrow(a_bot2),
                              lag_ratio=0.12, run_time=1.0))
        self.play(FadeIn(w_top2), FadeIn(w_mid2), FadeIn(w_bot2), run_time=0.6)
        self.bring_to_front(w_top2, w_mid2, w_bot2)

        self.play(FadeIn(eq_basis2_bg), Write(eq_basis2), run_time=0.9)
        self.bring_to_front(eq_basis2)

        dot2 = Dot(radius=0.07, color=YELLOW).move_to(a_bot2.get_start())
        self.add(dot2)
        self.play(MoveAlongPath(dot2, a_bot2), run_time=0.8)
        self.play(FadeOut(dot2, scale=1.4), run_time=0.2)

        self.wait(2)

        self.play(FadeOut(VGroup(
            node_top2, node_mid2, node_bottom2,
            phi_top2, phi_mid2, phi_bot2, vdots2,
            a_top2, a_mid2, a_bot2, w_top2, w_mid2, w_bot2,
            out_node2, out_label2, eq_basis2, eq_basis2_bg
        )))

         # --- Slide: Múltiples salidas---
        title_mout = Tex("Múltiples salidas", font_size=44).to_edge(UP)
        title_mout.set_color_by_tex("Múltiples salidas", ORANGE)

        intro = Tex(
            r"En algunas aplicaciones podríamos desear predecir $K>1$ variables que denotamos "
            r"colectivamente por el vector objetivo:",
            font_size=32
        )
        eq_tvec = MathTex(r"t=(t_1,\ldots,t_K)^{T}", font_size=44)
        eq_tvec.set_color_by_tex("t", GREEN)

        approach = Tex(
            r"El enfoque es utilizar el mismo conjunto de funciones base para modelar todos los "
            r"componentes del vector objetivo, de modo que:",
            font_size=32
        )

        eq_model_mo = MathTex(r"y(x,w) = W^{T}\,\phi(x)", font_size=44)
        eq_model_mo.set_color_by_tex("y", GREEN)
        eq_model_mo.set_color_by_tex("x", GREEN)
        eq_model_mo.set_color_by_tex("w", GREEN)
        eq_model_mo.set_color_by_tex("W", GREEN)
        eq_model_mo.set_color_by_tex(r"\phi", GREEN)

        def1 = Tex(
            r"donde ", r"$y$", r" es un vector columna de dimensión ", r"$K$", r", ",
            r"$W$", r" es una matriz de parámetros de dimensión ", r"$M\times K$", r" y ",
            r"$\phi(x)$", r" es un vector columna de dimensión ", r"$M$", r";",
            font_size=32
        )
        def1[1].set_color(BLUE)  
        def1[5].set_color(BLUE)   
        def1[9].set_color(BLUE)   

        def2 = Tex(
            r"sus elementos son ", r"$\phi_j(x)$", r" con ", r"$\phi_0(x)=1$", r".",
            font_size=32
        )
        def2[1].set_color(YELLOW)
        def2[3].set_color(YELLOW)

        note = Tex(
            r"Esto puede ser representado por una red neuronal de una sola capa de parámetros:",
            font_size=32
        )

        content = VGroup(intro, eq_tvec, approach, eq_model_mo, def1, def2, note).arrange(DOWN, buff=0.35)
        content.next_to(title_mout, DOWN, buff=0.6).set_x(0)

        self.play(Write(title_mout, run_time=write_speed))
        for m in content:
            self.play(Write(m, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(VGroup(title_mout, content)))

          # --- Slide B: Múltiples salidas
        left_x, right_x = -4.2, 3.6
        top_y, mid_y, bot_y = 1.6, 0.1, -1.4
        radius = 0.45

        in_top = Circle(radius=radius, color=BLUE, stroke_width=4).set_fill("#90CAF9", 0.35).move_to([left_x, top_y, 0])
        in_mid = Circle(radius=radius, color=BLUE, stroke_width=4).set_fill("#90CAF9", 0.35).move_to([left_x, mid_y, 0])
        in_bot = Circle(radius=radius, color=BLUE, stroke_width=4).set_fill("#0D47A1", 1.0).move_to([left_x, bot_y, 0])

        phi_top = MathTex(r"\phi_{M-1}(x)", font_size=36).next_to(in_top, LEFT, buff=0.35)
        phi_mid = MathTex(r"\phi_{1}(x)",  font_size=36).next_to(in_mid, LEFT, buff=0.35)
        phi_bot = MathTex(r"\phi_{0}(x)",  font_size=36).next_to(in_bot, LEFT, buff=0.35)
        vdots_L = MathTex(r"\vdots").move_to([left_x, (top_y+mid_y)/2, 0])

        out_top = Circle(radius=radius, color=BLUE, stroke_width=4).set_fill("#90CAF9", 0.35).move_to([right_x, top_y, 0])
        out_mid = Circle(radius=radius, color=BLUE, stroke_width=4).set_fill("#90CAF9", 0.35).move_to([right_x, mid_y, 0])

        yK = MathTex(r"y_{K}(x,w)", font_size=36).next_to(out_top, RIGHT, buff=0.35)
        y1 = MathTex(r"y_{1}(x,w)", font_size=36).next_to(out_mid, RIGHT, buff=0.35)
        for ylab in (yK, y1):
            ylab.set_color_by_tex("y", YELLOW)
            ylab.set_color_by_tex("x", BLUE)
            ylab.set_color_by_tex("w", GREEN)

        vdots_R = MathTex(r"\vdots").scale(1.0)
        vdots_R.next_to(VGroup(out_top, out_mid), LEFT, buff=0.18)

        conns = VGroup(
            Arrow(in_top.get_right(), out_top.get_left(), buff=0.05, stroke_width=6),
            Arrow(in_mid.get_right(), out_top.get_left(), buff=0.05, stroke_width=6),
            Arrow(in_bot.get_right(), out_top.get_left(), buff=0.05, stroke_width=6),
            Arrow(in_top.get_right(), out_mid.get_left(), buff=0.05, stroke_width=6),
            Arrow(in_mid.get_right(), out_mid.get_left(), buff=0.05, stroke_width=6),
            Arrow(in_bot.get_right(), out_mid.get_left(), buff=0.05, stroke_width=6),
        )
        self.play(LaggedStart(Create(in_top), Create(in_mid), Create(in_bot), lag_ratio=0.15, run_time=1.0))
        self.play(Write(phi_top), Write(phi_mid), Write(phi_bot), run_time=0.8)
        self.play(FadeIn(vdots_L, scale=0.9), run_time=0.3)

        self.play(LaggedStart(Create(out_top), Create(out_mid), lag_ratio=0.15, run_time=0.8))
        self.play(Write(yK), Write(y1), run_time=0.8)

        vdots_R.move_to((out_top.get_center() + out_mid.get_center())/2 + LEFT*0.8)
        self.play(FadeIn(vdots_R, scale=0.9), run_time=0.3)

        self.play(LaggedStart(*[GrowArrow(a) for a in conns], lag_ratio=0.08, run_time=1.0))
        self.wait(2)
        self.play(FadeOut(VGroup(
            in_top, in_mid, in_bot, phi_top, phi_mid, phi_bot, vdots_L,
            out_top, out_mid, yK, y1, vdots_R, conns
        )))

#manim -pqh RegresiónLineal.py RegresionLineal
