from manim import *
import numpy as np
from manim import config
config.tex_template.add_to_preamble(r"\usepackage{amsmath}")

class FuncionesDiscriminantes(Scene):
    def construct(self):
        write_speed = 5
        subtitle_gap = 0.60
        body_gap     = 0.30

        # ================= Slide 1: Título =================
        title = Tex("Funciones Discriminantes", font_size=52)
        title.set_color_by_tex("Funciones Discriminantes", BLUE)
        self.play(Write(title, run_time=write_speed))
        self.wait(1.2)
        self.play(FadeOut(title))

        # ================= Diagrama centrado: x -> g -> {C1,...,Ck} =================
        frase = Tex(
            r"Un discriminante es una función que toma un vector de entrada ",
            r"$x$",
            r" y lo asigna a una de las ",
            r"$K$",
            r" clases, denotada como ",
            r"$C_k$",
            r".",
            font_size=36
        ).to_edge(UP)
        frase[1].set_color(BLUE)
        frase[3].set_color(PURPLE)
        frase[5].set_color(ORANGE)
        self.play(Write(frase, run_time=2.0))

        g_box   = RoundedRectangle(corner_radius=0.28, width=3.6, height=1.4, color=TEAL_B)
        g_label = MathTex(r"y", color=YELLOW).scale(1.6).move_to(g_box.get_center())
        g_group = VGroup(g_box, g_label)

        x_sym = MathTex(r"\mathbf{x}", color=BLUE).scale(1.2)
        clases = VGroup(
            MathTex(r"C_1"),
            MathTex(r"C_2"),
            MathTex(r"\cdots"),
            MathTex(r"C_k").set_color(ORANGE)
        ).arrange(RIGHT, buff=0.6)

        row = VGroup(x_sym, g_group, clases).arrange(RIGHT, buff=1.0)
        row.move_to(ORIGIN)

        a1 = Arrow(x_sym.get_right(), g_group.get_left(), buff=0.12, color=GREY_B)
        a2 = Arrow(g_group.get_right(), clases.get_left(), buff=0.12, color=GREY_B)

        self.play(FadeIn(x_sym, shift=LEFT*0.2))
        self.play(Create(g_box), Write(g_label))
        self.play(FadeIn(clases, shift=RIGHT*0.2))
        self.play(Create(a1), Create(a2))

        ck_slot      = Dot(radius=0).next_to(clases[-1], LEFT,  buff=0.28).get_center()
        x_right_ck   = MathTex(r"\mathbf{x}", color=BLUE).scale(1.0).next_to(clases[-1], RIGHT, buff=0.20)

        x_token = x_sym.copy()
        self.play(TransformFromCopy(x_sym, x_token), run_time=0.5)
        self.play(x_token.animate.move_to(g_group.get_center()), run_time=0.8)
        self.play(x_token.animate.move_to(ck_slot), run_time=0.8)
        self.play(ReplacementTransform(x_token, x_right_ck), Indicate(clases[-1], color=ORANGE), run_time=0.8)

        self.wait(0.4)

        self.play(FadeOut(VGroup(frase,row, a1, a2, x_right_ck)))

        # ================= Slide 2B: Ítem 1 — "Dos casos" =================
        i1_title = Tex(r"\textbf{Dos casos:}\\", font_size=40)
        i1_title.set_color(ORANGE)

        i1_text1 = Tex(
            r"La representación más simple de una función lineal discriminante es obtenida tomando una función lineal del vector de entrada:",
            font_size=33
        )
        i1_eq = MathTex(r"y(x) = w^T x+w_0", font_size=42)
        i1_eq.set_color_by_tex("y", YELLOW)
        i1_eq.set_color_by_tex("x", BLUE)
        i1_eq.set_color_by_tex("w", GREEN)
        i1_eq.set_color_by_tex("w_0", GREEN)

        i1_text2 = Tex(
            r"donde ", r"$w$", r" es llamado vector de ponderación y ", r"$w_0$", r" es un  sesgo. Un vector ",
            r"$x$", r" es asignado a la clase ", r"$C_1$", r" si ", r"$y(x)\geq 0$", r" y a la clase ",
            r"$C_2$", r" en otro caso. El límite de decisión correspondiente se define por la relación ",
            r"$y(x)=0$", r", que corresponde a un hiperplano de dimensión ", r"$(D-1)$",
            r" dentro de un espacio de entrada ", r"$D$", r"-dimensional.",
            font_size=32
        )
        for idx, col in [(1, GREEN), (3, GREEN), (5, BLUE), (7, ORANGE), (9, YELLOW),
                         (11, ORANGE), (13, YELLOW), (15, PURPLE), (17, PURPLE)]:
            i1_text2[idx].set_color(col)

        body2b  = VGroup(i1_text1, i1_eq, i1_text2).arrange(DOWN, buff=body_gap)
        body2b.move_to(ORIGIN)
        i1_title.next_to(body2b, UP, buff=subtitle_gap).align_to(body2b, LEFT)

        slide2b = VGroup(i1_title, body2b)
        for m in slide2b:
            self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(slide2b))

        # ================= Mini-demo simbólica mejorada =================
        g_box   = RoundedRectangle(corner_radius=0.28, width=3.6, height=1.4, color=TEAL_B)
        g_label = MathTex(r"y", color=YELLOW).scale(1.6).move_to(g_box.get_center())
        g_group = VGroup(g_box, g_label)

        x_sym  = MathTex(r"\mathbf{x}", color=BLUE).scale(1.2)
        c1     = MathTex(r"C_1")
        c2     = MathTex(r"C_2")
        y_expr = MathTex(r"y(x)=w^T x + w_0")
        y_expr.set_color_by_tex("y", YELLOW)
        y_expr.set_color_by_tex("x", BLUE)
        y_expr.set_color_by_tex("w", GREEN)
        y_expr.set_color_by_tex("w_0", GREEN)

        right_col = VGroup(c1, c2).arrange(DOWN, buff=1.0)
        row = VGroup(x_sym, g_group, right_col).arrange(RIGHT, buff=1.0)
        row.move_to(ORIGIN)
        y_expr.next_to(row, UP, buff=0.6)

        cond_ge = MathTex(r"y(x)\ge 0", color=GREEN).next_to(c1, DOWN, buff=0.15)
        cond_lt = MathTex(r"y(x)<0",   color=RED  ).next_to(c2, UP,   buff=0.15)

        ring1 = Circle(radius=0.22, color=WHITE, stroke_width=3).next_to(cond_ge, RIGHT, buff=0.35)
        dot1  = Dot(radius=0.18, color=GREEN).move_to(ring1.get_center())
        ring2 = Circle(radius=0.22).next_to(cond_lt, RIGHT, buff=0.35)
        dot2  = Dot(radius=0.18).move_to(ring2.get_center())

        c1_slot = Dot(radius=0).next_to(c1, LEFT,  buff=0.28).get_center()
        c2_slot = Dot(radius=0).next_to(c2, LEFT,  buff=0.28).get_center()
        x_right_c1 = MathTex(r"\mathbf{x}", color=BLUE).scale(0.95).next_to(c1, RIGHT, buff=0.18)
        x_right_c2 = MathTex(r"\mathbf{x}", color=BLUE).scale(0.95).next_to(c2, RIGHT, buff=0.18)

        a_in = Arrow(x_sym.get_right(), g_group.get_left(), buff=0.12, color=GREY_B)
        a_c1 = Arrow(g_group.get_right()+UP*0.4,   c1_slot, buff=0.12, color=GREY_B)
        a_c2 = Arrow(g_group.get_right()+DOWN*0.4, c2_slot, buff=0.12, color=GREY_B)

        self.play(Write(y_expr, run_time=0.9))
        self.play(FadeIn(x_sym), Create(g_box), Write(g_label))
        self.play(FadeIn(c1), FadeIn(c2))
        self.play(Create(a_in), Create(a_c1), Create(a_c2))

        t1 = x_sym.copy()
        self.play(TransformFromCopy(x_sym, t1), run_time=0.4)
        self.play(t1.animate.move_to(g_group.get_center()), run_time=0.6)
        self.play(t1.animate.move_to(c1_slot), run_time=0.7)
        self.play(Write(cond_ge), FadeIn(ring1), GrowFromCenter(dot1), Indicate(c1, color=GREEN), run_time=0.8)
        self.play(ReplacementTransform(t1, x_right_c1))
        self.wait(0.2)

        self.play(
            TransformMatchingTex(cond_ge, cond_lt),
            ring1.animate.move_to(ring2.get_center()),
            dot1.animate.move_to(dot2.get_center()).set_fill(RED),
            run_time=0.9
        )

        t2 = x_sym.copy()
        self.play(TransformFromCopy(x_sym, t2), run_time=0.4)
        self.play(t2.animate.move_to(g_group.get_center()), run_time=0.6)
        self.play(t2.animate.move_to(c2_slot), run_time=0.7)
        self.play(Indicate(c2, color=RED), run_time=0.6)
        self.play(ReplacementTransform(t2, x_right_c2))
        self.wait(0.2)

        self.play(FadeOut(VGroup(y_expr, row, a_in, a_c1, a_c2, cond_lt, ring1, dot1, x_right_c1, x_right_c2)))

        # ================= Slide 3: Item 2 (todo junto, centrado) =================
        i2_title = Tex(r"\textbf{Múltiples casos:}\\", font_size=40)
        i2_title.set_color(ORANGE)
        i2_text1 = Tex(
            r"En este caso consideramos un único discriminante de ",
            r"$K$", r"-clases comprimido en ", r"$K$",
            r" funciones lineales de la forma:",
            font_size=33
        )
        i2_text1[1].set_color(PURPLE)
        i2_text1[3].set_color(PURPLE)

        i2_eq = MathTex(r"y_k(x) = w_k^Tx + w_{k_0}", font_size=42)
        for tok, col in [(r"y_k", YELLOW), (r"x", BLUE), (r"w_k", GREEN), (r"w_{k_0}", GREEN)]:
            i2_eq.set_color_by_tex(tok, col)

        i2_text2 = Tex(
            r"que asigna un punto ", r"$x$", r" a la clase ", r"$C_k$", r" si ",
            r"$y_k(x) > y_j(x)$", r" para todo ", r"$j\neq k$", r". El límite de decisión esta entre la clase ",
            r"$C_j$", r" y ", r"$C_k$", r", por lo tanto viene dado por ", r"$y_k(x)= y_j(x)$", r"\\",
            font_size=32
        )
        for idx, col in [(1, BLUE), (3, ORANGE), (5, YELLOW), (7, YELLOW),
                         (9, ORANGE), (11, ORANGE), (13, YELLOW)]:
            i2_text2[idx].set_color(col)

        i2_text3 = Tex(r"(regiones de decisión convexas)", font_size=30)

        body3  = VGroup(i2_text1, i2_eq, i2_text2, i2_text3).arrange(DOWN, buff=body_gap)
        body3.move_to(ORIGIN)
        i2_title.next_to(body3, UP, buff=subtitle_gap).align_to(body3, LEFT)

        slide3 = VGroup(i2_title, body3)
        for m in slide3:
            self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(slide3))

        # ================= K>2: asignación por máximo =================
        eq_top = MathTex(r"y_k(x) = w_k^T x + w_{k_0}", font_size=42)
        for tok, col in [(r"y_k", YELLOW), (r"x", BLUE), (r"w_k", GREEN), (r"w_{k_0}", GREEN)]:
            eq_top.set_color_by_tex(tok, col)
        eq_top.to_edge(UP)
        self.play(Write(eq_top), run_time=1.0)

        box   = RoundedRectangle(corner_radius=0.28, width=3.8, height=1.5, color=TEAL_B)
        lbl   = MathTex(r"y_k", color=YELLOW).scale(1.4).move_to(box.get_center())
        group = VGroup(box, lbl)

        x_sym = MathTex(r"\mathbf{x}", color=BLUE).scale(1.2)
        c1    = MathTex(r"C_1")
        c2    = MathTex(r"C_2")
        cdots = MathTex(r"\cdots")
        ck    = MathTex(r"C_k").set_color(ORANGE)

        col_right = VGroup(c1, c2, cdots, ck).arrange(DOWN, buff=0.6)
        row = VGroup(x_sym, group, col_right).arrange(RIGHT, buff=1.0)
        row.move_to(ORIGIN)

        a_in  = Arrow(x_sym.get_right(), group.get_left(), buff=0.12, color=GREY_B)

        pos_yk_below_ck = lambda: MathTex(r"y_k(x)").scale(1.0).next_to(ck, DOWN, buff=0.15).get_center()
        x_right_ck = MathTex(r"\mathbf{x}", color=BLUE).scale(1.0).next_to(ck, RIGHT, buff=0.20)

        rule_head = Tex(r"asigna $x$ a $C_k$ si", font_size=36).next_to(col_right, RIGHT, buff=1.0, aligned_edge=UP)
        cond_main  = MathTex(r"y_k(x) > y_j(x)", font_size=36).next_to(rule_head, DOWN, buff=0.25)
        cond_quant = MathTex(r"\forall\, j \neq k", font_size=34).next_to(cond_main, DOWN, buff=0.15)

        self.play(FadeIn(x_sym), Create(box), Write(lbl))
        self.play(FadeIn(col_right))
        self.play(Create(a_in))

        x_tok = x_sym.copy()
        self.play(TransformFromCopy(x_sym, x_tok), run_time=0.5)
        self.play(x_tok.animate.move_to(group.get_center()), run_time=0.7)

        yk_tok = MathTex(r"y_k(x)", color=YELLOW).move_to(group.get_right()+RIGHT*0.25)
        self.play(Write(yk_tok), run_time=0.4)
        self.play(yk_tok.animate.move_to(pos_yk_below_ck()), run_time=0.7)

        self.play(Write(rule_head), Write(cond_main), Write(cond_quant), run_time=0.9)

        p_start = group.get_right() + RIGHT*0.15 + UP*0.45
        p_c1    = c1.get_left() + LEFT*0.15
        p_c2    = c2.get_left() + LEFT*0.15
        p_ck    = ck.get_left() + LEFT*0.15

        path = VMobject().set_points_as_corners([p_start, p_c1, p_c2, p_ck])
        runner = Triangle(fill_color=GREY_B, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI)
        runner.move_to(path.get_start())

        self.play(MoveAlongPath(runner, path), run_time=1.6, rate_func=smooth)
        self.play(Indicate(ck, color=ORANGE), run_time=0.5)
        final_arrow = Arrow(group.get_right(), ck.get_left(), buff=0.12, color=GREY_B)
        self.play(FadeIn(final_arrow), FadeOut(runner), run_time=0.5)

        self.play(ReplacementTransform(x_tok, x_right_ck), run_time=0.6)
        self.wait(0.4)

        self.play(FadeOut(VGroup(eq_top, row, a_in, final_arrow, yk_tok, rule_head, cond_main, cond_quant, x_right_ck)))

        # ================= Slide 4: Item 3 (todo junto) =================
        i3_title = Tex(r"\textbf{Codificación 1 de $K$}\\", font_size=40)
        i3_title.set_color(ORANGE)

        i3_p1 = Tex(
            r"La codificación \textit{1-de-K} es un método utilizado para representar etiquetas en problemas de clasificación con ",
            r"$K$", r" clases.  ",
            font_size=33
        )
        i3_p1[1].set_color(PURPLE)

        i3_p2 = Tex(
            r"Consiste en asignar a cada observación un vector de longitud ",
            r"$K$", r", cuyos elementos son cero salvo en la posición correspondiente a la clase verdadera, donde toma el valor uno.  ",
            font_size=33
        )
        i3_p2[1].set_color(PURPLE)

        i3_p3 = Tex(
            r"Por ejemplo, si existen cinco clases y la observación pertenece a la clase 2, el vector objetivo será:  ",
            font_size=33
        )
        i3_eq = MathTex(r"t = (0,1,0,0,0)^T .", font_size=42)
        i3_eq.set_color_by_tex("t", RED)

        i3_p4 = Tex(
            r"De esta manera, cada componente ", r"$t_k$", r" puede interpretarse como la probabilidad de que la observación pertenezca a la clase ",
            r"$C_k$", r",  ",
            font_size=33
        )
        i3_p4[1].set_color(BLUE)
        i3_p4[3].set_color(GREEN)

        i3_p5 = Tex(r"aunque en este esquema los valores posibles son únicamente $0$ o $1$.", font_size=33)

        body4  = VGroup(i3_p1, i3_p2, i3_p3, i3_eq, i3_p4, i3_p5).arrange(DOWN, buff=body_gap)
        body4.move_to(ORIGIN)
        i3_title.next_to(body4, UP, buff=subtitle_gap).align_to(body4, LEFT)

        slide4 = VGroup(i3_title, body4)
        for m in slide4:
            self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(slide4))

        # ================= Slide 5: Item 4 (parte 1) =================
        i4_title = Tex(r"\textbf{Mínimos cuadrados para clasificación.}\\", font_size=40)
        i4_title.set_color(ORANGE)

        i4_p1 = Tex(
            r"Considera un problema de clasificación general con ", r"$K$", r" clases y un esquema de codificación 1 de ",
            r"$K$", r" para el valor objetivo ", r"$t$", r". Cada clase ", r"$C_k$",
            r" se describe mediante su propio modelo lineal de modo que:",
            font_size=33
        )
        for idx, col in [(1, PURPLE), (3, PURPLE), (5, RED), (7, ORANGE)]:
            i4_p1[idx].set_color(col)

        i4_eq1 = MathTex(r"y_k (x) = w_k^T x + w_{k0}", font_size=42)
        for tok, col in [(r"y_k", YELLOW), (r"x", BLUE), (r"w_k", GREEN), (r"w_{k0}", GREEN)]:
            i4_eq1.set_color_by_tex(tok, col)

        i4_p2 = Tex(r"donde $k=1,...,K$, en notación vectorial:", font_size=33)
        i4_eq2 = MathTex(r"y(x) = \widetilde{W}^T\widetilde{x}", font_size=42)
        i4_eq2.set_color_by_tex(r"y", YELLOW)
        i4_eq2.set_color_by_tex(r"\widetilde{W}", GREEN)
        i4_eq2.set_color_by_tex(r"\widetilde{x}", BLUE)

        body5  = VGroup(i4_p1, i4_eq1, i4_p2, i4_eq2).arrange(DOWN, buff=body_gap)
        body5.move_to(ORIGIN)
        i4_title.next_to(body5, UP, buff=subtitle_gap).align_to(body5, LEFT)

        slide5 = VGroup(i4_title, body5)
        for m in slide5:
            self.play(Write(m, run_time=write_speed))
        self.wait(0.6)
        self.play(FadeOut(slide5))

        # ================= Slide 6: Item 4 (parte 2) =================
        i4_p3 = Tex(
            r"donde ", r"$\widetilde{W}$", r" es una matriz cuya columna $k$ comprende vector ",
            r"$(D+1)$", r"-dimensional ", r"$\widetilde{w}_k$", r" = ", r"$(w_{k0},w_k^T)^T$", r" y ",
            r"$\widetilde{x}$", r" = ", r"$(1,x^T)^T$", r" con una entrada ", r"$x_0$", r" = 1\\",
            font_size=32
        )
        for idx, col in [(1, GREEN), (3, PURPLE), (5, GREEN), (9, BLUE), (13, BLUE)]:
            i4_p3[idx].set_color(col)

        i4_p4 = Tex(r"La matriz de parámetros ", r"$\widetilde{W}$", r" se puede obtener de la forma:", font_size=33)
        i4_p4[1].set_color(GREEN)

        i4_eq3 = MathTex(r"\widetilde{W} = (\widetilde{X}^T \widetilde{X})^{-1} \widetilde{X}^TT = \widetilde{W}^{\dag} T", font_size=42)
        i4_eq3.set_color_by_tex(r"\widetilde{W}", PINK)
        i4_eq3.set_color_by_tex(r"\widetilde{X}", PINK)
        i4_eq3.set_color_by_tex(r"T", PINK)

        i4_p5 = Tex(
            r"donde ", r"$\widetilde{W}$", r" es la pseudo-inversa de la matriz ", r"$\widetilde{X}$",
            r"cuya n-ésima fila es el vector ", r"$\widetilde{x}_n^T$", r"  y ", r"$T$",
            r" es una matriz cuya n-ésima fila es el vector ", r"$t_n^T$", r"\\",
            font_size=32
        )
        for idx, col in [(1, GREEN), (3, BLUE), (5, BLUE), (7, RED), (9, RED)]:
            i4_p5[idx].set_color(col)

        i4_p6 = Tex(r"Así se obtiene la función discriminante:", font_size=33)
        i4_eq4 = MathTex(r"y(x)= \widetilde{W}^T \widetilde{x} = T^T (\widetilde{X}^{\dag})^{T}\widetilde{x}", font_size=42)
        i4_eq4.set_color_by_tex(r"y", BLUE)
        i4_eq4.set_color_by_tex(r"\widetilde{W}", BLUE)
        i4_eq4.set_color_by_tex(r"\widetilde{x}", BLUE)
        i4_eq4.set_color_by_tex(r"\widetilde{X}", BLUE)
        i4_eq4.set_color_by_tex(r"T", BLUE)

        i4_p7 = Tex(r"El método de mínimos cuadrados proporciona una solución exacta en forma cerrada para los parámetros de la función discriminante.", font_size=33)

        slide6 = VGroup(i4_p3, i4_p4, i4_eq3, i4_p5, i4_p6, i4_eq4, i4_p7).arrange(DOWN, buff=0.28)
        slide6.move_to(ORIGIN)

        for m in slide6:
            self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(slide6))


#manim -pqh FuncionesDiscriminantes.py FuncionesDiscriminantes

