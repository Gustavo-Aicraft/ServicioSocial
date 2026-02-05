from manim import *
import numpy as np
from manim import config
config.tex_template.add_to_preamble(r"\usepackage{amsmath}")

class TeoriaDecision(Scene):
    def construct(self):
        write_speed = 5
        body_gap    = 0.32

        # ================= Slide 1
        title = Tex("Teoría de Decisión", font_size=52)
        title.set_color_by_tex("Teoría de Decisión", BLUE)
        self.play(Write(title, run_time=write_speed))
        self.wait(1.2)
        self.play(FadeOut(title))

        # ============== Slide 2A
        s2a_title = Tex(r"Tasa de clasificación errónea\\", font_size=44).to_edge(UP)
        s2a_title.set_color(ORANGE)

        s2a_l1 = Tex(
            r"El objetivo es simplemente realizar la menor cantidad posible de clasificaciones erróneas.",
            font_size=34
        )
        s2a_l2 = Tex(
            r"Un error se produce cuando un vector de entrada que pertenece a la clase $C_1$ es asignado a la clase $C_2$ y viceversa:",
            font_size=34,
            substrings_to_isolate=[r"$C_1$", r"$C_2$"]
        )
        for token, col in [(r"$C_1$", GREEN), (r"$C_2$", GREEN)]:
            for m in s2a_l2.get_parts_by_tex(token): m.set_color(col)

        s2a_eq1 = MathTex(
            r"\mathbb{P}(error) = \mathbb{P}(x \in R_1, C_2) + \mathbb{P}(x \in R_2, C_1)",
            font_size=40
        )
        s2a_eq1.set_color_by_tex(r"\mathbb{P}", YELLOW)
        s2a_eq1.set_color_by_tex(r"x", BLUE)
        s2a_eq1.set_color_by_tex(r"R_1", ORANGE)
        s2a_eq1.set_color_by_tex(r"R_2", ORANGE)
        s2a_eq1.set_color_by_tex(r"C_1", GREEN)
        s2a_eq1.set_color_by_tex(r"C_2", GREEN)

        s2a_body = VGroup(s2a_l1, s2a_l2, s2a_eq1).arrange(DOWN, buff=body_gap).move_to(ORIGIN)

        self.play(Write(s2a_title, run_time=write_speed))
        for m in s2a_body: self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(s2a_title, s2a_body)))

        # ============== Slide 2B
        axes = Axes(x_range=[-4,4,1], y_range=[0,1.2,0.2],
                    tips=False, axis_config={"color": BLUE}).scale(0.9)
        g1 = axes.plot(lambda x: np.exp(-((x+1.4)**2)/1.2), color=GREEN)   
        g2 = axes.plot(lambda x: np.exp(-((x-1.4)**2)/1.2), color=PURPLE) 

        th = 0.0
        vline = axes.get_vertical_line(axes.c2p(th,0), color=ORANGE)
        r1 = MathTex(r"R_1").set_color(YELLOW).scale(0.9).move_to(axes.c2p(-3.2, 0.85))
        r2 = MathTex(r"R_2").set_color(PINK).scale(0.9).move_to(axes.c2p( 3.2, 0.85))

        plot_grp = VGroup(axes, g1, g2, vline, r1, r2).move_to(ORIGIN)

        self.play(Create(axes), Create(g1), Create(g2), run_time=write_speed)
        self.play(Create(vline), FadeIn(r1), FadeIn(r2), run_time=write_speed*0.6)

        A1 = axes.get_area(g2, x_range=[-4, th], color=YELLOW, opacity=0.35) 
        A2 = axes.get_area(g1, x_range=[th, 4], color=PINK, opacity=0.35)  
        self.play(FadeIn(A1), run_time=0.6)
        self.play(FadeIn(A2), run_time=0.6)

        term1 = MathTex(r"\mathbb{P}(x\in R_1, C_2)").next_to(A1, UP, buff=0.3)
        term2 = MathTex(r"\mathbb{P}(x\in R_2, C_1)").next_to(A2, UP, buff=0.3)
        self.play(Write(term1, run_time=write_speed*0.6))
        self.play(Write(term2, run_time=write_speed*0.6))

        eq = MathTex(
            r"\mathbb{P}(\text{error})", "=", r"\mathbb{P}(x\in R_1, C_2)", "+", r"\mathbb{P}(x\in R_2, C_1)",
            font_size=46
        ).to_edge(DOWN, buff=0.6)
        eq.set_color_by_tex(r"\mathbb{P}", YELLOW)
        eq.set_color_by_tex(r"x", BLUE)
        eq.set_color_by_tex(r"R_1", ORANGE)
        eq.set_color_by_tex(r"R_2", ORANGE)
        eq.set_color_by_tex(r"C_1", GREEN)
        eq.set_color_by_tex(r"C_2", GREEN)

        self.play(Write(eq[0], run_time=write_speed*0.5))
        self.play(Write(eq[1], run_time=write_speed*0.3))
        self.play(TransformFromCopy(term1, eq[2]), run_time=0.9)
        self.play(Write(eq[3], run_time=0.3))  # el "+"
        self.play(TransformFromCopy(term2, eq[4]), run_time=0.9)
        self.play(Indicate(A1, scale_factor=1.02), Indicate(A2, scale_factor=1.02), Indicate(eq), run_time=1.0)

        self.play(FadeOut(VGroup(term1, term2)), run_time=0.5)
        self.play(FadeOut(eq), run_time=0.5)
        self.play(FadeOut(VGroup(A1, A2)), run_time=0.5)
        self.play(FadeOut(VGroup(g1, g2, r1, r2, vline)), run_time=0.6)
        self.play(FadeOut(VGroup(axes)), run_time=0.5)

        # ============== Slide 2C
        s2b_l3 = Tex(
            r"Para el caso más general de $K$ clases, es ligeramente más fácil maximizar la probabilidad de acertar:",
            font_size=34,
            substrings_to_isolate=[r"$K$"]
        )
        for m in s2b_l3.get_parts_by_tex(r"$K$"): m.set_color(TEAL)

        s2b_eq2 = MathTex(
            r"\mathbb{P} (correcto) = \sum\limits_{k=1}^{K} \mathbb{P}(x \in R_k, C_k )",
            font_size=40
        )
        s2b_eq2.set_color_by_tex(r"\mathbb{P}", YELLOW)
        s2b_eq2.set_color_by_tex(r"\sum", PURPLE)
        s2b_eq2.set_color_by_tex(r"K", TEAL)
        s2b_eq2.set_color_by_tex(r"x", BLUE)
        s2b_eq2.set_color_by_tex(r"R_k", ORANGE)
        s2b_eq2.set_color_by_tex(r"C_k", GREEN)

        s2b_l4 = Tex(
            r"que se maximiza cuando las regiones $R_k$ se eligen de tal manera que cada $x$ se asigna a la clase para la que $p(x,C_k)$ es mayor.",
            font_size=34,
            substrings_to_isolate=[r"$R_k$", r"$x$", r"$p(x,C_k)$"]
        )
        for token, col in [(r"$R_k$", ORANGE), (r"$x$", BLUE), (r"$p(x,C_k)$", YELLOW)]:
            for m in s2b_l4.get_parts_by_tex(token): m.set_color(col)

        s2b_body = VGroup(s2b_l3, s2b_eq2, s2b_l4).arrange(DOWN, buff=body_gap).move_to(ORIGIN)
        for m in s2b_body: self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(s2b_body)), run_time=0.6)

        # ============== Slide 2D
        K = 4                     
        cell_w, cell_h = 1.3, 0.9 

        grid = VGroup().move_to(ORIGIN)

        col_labels = VGroup(*[MathTex(rf"R_{j+1}").set_color(ORANGE).scale(0.9) for j in range(K)])
        row_labels = VGroup(*[MathTex(rf"C_{i+1}").set_color(TEAL).scale(0.9)   for i in range(K)])  

        cells = []
        rects = VGroup()
        for i in range(K):
            row = []
            for j in range(K):
                r = RoundedRectangle(width=cell_w, height=cell_h, corner_radius=0.07,
                                    color=BLUE, stroke_width=2)
                row.append(r); rects.add(r)
            cells.append(row)

        for i in range(K):
            for j in range(K):
                rects[i*K+j].move_to(
                    RIGHT*(j-(K-1)/2)*cell_w*1.05 + DOWN*(i-(K-1)/2)*cell_h*1.15
                )

        for j, lab in enumerate(col_labels):
            lab.next_to(rects[j], UP, buff=0.70)      
        for i, lab in enumerate(row_labels):
            lab.next_to(rects[i*K], LEFT, buff=0.60) 

        grid.add(rects, col_labels, row_labels)

        self.play(LaggedStart(Create(rects), lag_ratio=0.06, run_time=0.9))
        self.play(FadeIn(col_labels), FadeIn(row_labels), run_time=0.6)
        rng = np.array([
            [0.20, 0.04, 0.02, 0.01],
            [0.03, 0.18, 0.05, 0.01],
            [0.02, 0.04, 0.16, 0.03],
            [0.01, 0.01, 0.04, 0.15],
        ])[:K,:K].astype(float)
        rng = rng / rng.sum()

        fills = VGroup()
        for i in range(K):
            for j in range(K):
                f = rects[i*K+j].copy().set_fill(WHITE, opacity=0.15 + 0.6*rng[i,j]).set_stroke(width=0)
                fills.add(f)
        self.play(FadeIn(fills), run_time=0.7)

        diag_glows = VGroup()
        terms = VGroup()
        for k in range(K):
            cell = rects[k*K + k]
            glow = SurroundingRectangle(cell, color=YELLOW, buff=0.04)
            diag_glows.add(glow)

            t = MathTex(rf"\mathbb{{P}}(x\in R_{k+1}, C_{k+1})").scale(0.68)
            t.set_color_by_tex(r"\mathbb{P}", YELLOW)
            t.set_color_by_tex(r"x", BLUE)
            t.set_color_by_tex(r"R_", ORANGE)
            t.set_color_by_tex(r"C_", GREEN)
            t.move_to(cell.get_center())
            t.set_fill(opacity=1)
            try:
                t.set_background_stroke(color=BLACK, width=6, opacity=1)
            except Exception:
                bg = BackgroundRectangle(t, fill_color=BLACK, fill_opacity=0.85, stroke_width=0, buff=0.04)
                self.add(bg)

            terms.add(t)

        self.play(LaggedStart(*[Create(g) for g in diag_glows], lag_ratio=0.12, run_time=0.8))
        self.bring_to_front(terms)
        for t in terms:
            self.play(Write(t, run_time=write_speed*0.45))

        eqK = MathTex(
            r"\mathbb{P}(\text{correcto})", "=", rf"\sum_{{k=1}}^{{{K}}} \mathbb{{P}}(x\in R_k, C_k)",
            font_size=46
        ).to_edge(DOWN, buff=0.6)
        eqK.set_color_by_tex(r"\mathbb{P}", YELLOW)
        eqK.set_color_by_tex(r"\sum", PURPLE)
        eqK.set_color_by_tex(r"x", BLUE)
        eqK.set_color_by_tex(r"R_k", ORANGE)
        eqK.set_color_by_tex(r"C_k", GREEN)
        eqK.set_color_by_tex(rf"{K}", TEAL)

        self.play(Write(eqK[0], run_time=write_speed*0.5))
        self.play(Write(eqK[1], run_time=write_speed*0.3))
        self.play(TransformFromCopy(terms, eqK[2]), run_time=1.0)
        self.play(Indicate(diag_glows, scale_factor=1.02), Indicate(eqK), run_time=1.0)
        
        self.play(FadeOut(terms), run_time=0.5)
        self.play(FadeOut(eqK), run_time=0.5)
        self.play(FadeOut(diag_glows), run_time=0.4)
        self.play(FadeOut(VGroup(fills, rects, col_labels, row_labels)), run_time=0.6)


        # ============== Slide 3A
        s3a_title = Tex(r"Pérdida esperada\\", font_size=44).to_edge(UP)
        s3a_title.set_color(ORANGE)

        s3a_a = Tex(
            r"Supóngase que, para un nuevo valor $x$, la verdadera clase es $C_k$ y se asigna $x$ a la clase $C_j$, aquí incurrimos en un nivel de pérdida que denotamos por $L_{kj}$.",
            font_size=34,
            substrings_to_isolate=[r"$x$", r"$C_k$", r"$C_j$", r"$L_{kj}$"]
        )
        for token, col in [(r"$x$", BLUE), (r"$C_k$", GREEN), (r"$C_j$", GREEN), (r"$L_{kj}$", RED)]:
            for m in s3a_a.get_parts_by_tex(token): m.set_color(col)

        s3a_b = Tex(
            r"La solución óptima es la que minimiza la función de pérdida, esta depende de la clase verdadera, que es desconocida.",
            font_size=34
        )
        s3a_c = Tex(
            r"Para un vector de entrada $x$, la incertidumbre en la clase verdadera se expresa a través de la distribución de probabilidad conjunta $p(x,C_k)$, y por lo tanto, buscamos minimizar la pérdida promedio:",
            font_size=34,
            substrings_to_isolate=[r"$x$", r"$p(x,C_k)$"]
        )
        for token, col in [(r"$x$", BLUE), (r"$p(x,C_k)$", YELLOW)]:
            for m in s3a_c.get_parts_by_tex(token): m.set_color(col)

        s3a_eq1 = MathTex(
            r"\mathbb{E}[L]= \sum_{k}\sum_j \int_{R_j} L_{kj}p(x,C_k) dx",
            font_size=42
        )
        s3a_eq1.set_color_by_tex(r"\mathbb{E}", YELLOW)
        s3a_eq1.set_color_by_tex(r"\sum", PURPLE)
        s3a_eq1.set_color_by_tex(r"\int", TEAL)
        s3a_eq1.set_color_by_tex(r"R_j", ORANGE)
        s3a_eq1.set_color_by_tex(r"L_{kj}", RED)
        s3a_eq1.set_color_by_tex(r"x", BLUE)
        s3a_eq1.set_color_by_tex(r"C_k", GREEN)

        s3a_body = VGroup(s3a_a, s3a_b, s3a_c, s3a_eq1).arrange(DOWN, buff=body_gap).move_to(ORIGIN)

        self.play(Write(s3a_title, run_time=write_speed))
        for m in s3a_body: self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(s3a_title, s3a_body)))

        # ============== Slide 3B
        s3b_d = Tex(
            r"Cada $x$ se puede asignar independientemente a una de las regiones de decisión $R_{j}$. La regla de decisión que minimiza la pérdida esperada asigna cada nueva $x$ a la clase $j$ para la cual la cantidad:",
            font_size=34,
            substrings_to_isolate=[r"$x$", r"$R_{j}$", r"$x$", r"$j$"]
        )
        for token, col in [(r"$x$", BLUE), (r"$R_{j}$", ORANGE), (r"$j$", GREEN)]:
            for m in s3b_d.get_parts_by_tex(token): m.set_color(col)

        s3b_eq2 = MathTex(
            r"\sum_{k} L_{kj} p(C_k,x)",
            font_size=44
        )
        s3b_eq2.set_color_by_tex(r"\sum", PURPLE)
        s3b_eq2.set_color_by_tex(r"L_{kj}", RED)
        s3b_eq2.set_color_by_tex(r"C_k", GREEN)
        s3b_eq2.set_color_by_tex(r"x", BLUE)

        s3b_e = Tex(r"es un mínimo", font_size=34)

        s3b_body = VGroup(s3b_d, s3b_eq2, s3b_e).arrange(DOWN, buff=body_gap).move_to(ORIGIN)

        for m in s3b_body: self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(s3b_body)))

        # ============== Slide 4A
        s4a_title = Tex(r"La opción de rechazo\\", font_size=44).to_edge(UP)
        s4a_title.set_color(ORANGE)

        s4a_p1 = Tex(
            r"Los errores de clasificación aparecen donde las probabilidades posteriores $p(C_k \mid x)$ son significativamente menores a 1. "
            r"Para disminuir el error en las entradas $x$ donde el clasificador no está seguro, se permite no decidir (rechazar) cuando la confianza es baja. "
            r"Esto se conoce como opción de rechazo.",
            font_size=34,
            substrings_to_isolate=[r"$p(C_k \mid x)$", r"$x$"]
        )
        for token, col in [(r"$p(C_k \mid x)$", YELLOW), (r"$x$", BLUE)]:
            for m in s4a_p1.get_parts_by_tex(token): m.set_color(col)

        s4a_body = VGroup(s4a_p1).arrange(DOWN, buff=body_gap).move_to(ORIGIN)

        self.play(Write(s4a_title, run_time=write_speed))
        self.play(Write(s4a_body, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(s4a_title, s4a_body)))

        r0_title  = Tex(r"Inferencia y decisión", font_size=44).to_edge(UP)
        r0_title.set_color(ORANGE)
        r0_l1 = Tex(
            r"La clasificación puede verse en dos etapas: \textbf{inferencia}, donde aprendemos con datos de entrenamiento un modelo probabilístico, y \textbf{decisión}, donde usamos ese modelo para asignar una clase minimizando el riesgo (o la tasa de error).",
            font_size=34
        )
        r0_l2 = Tex(
            r"Hay tres enfoques, de mayor a menor complejidad.",
            font_size=34
        )
        r0_body = VGroup(r0_l1, r0_l2).arrange(DOWN, buff=body_gap).move_to(ORIGIN)
        self.play(Write(r0_title, run_time=write_speed))
        for m in r0_body: self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(r0_title, r0_body)), run_time=0.6)

        # Slide R1 
        r1_title = Tex(r"(a) Enfoque generativo", font_size=44).to_corner(UL)
        r1_title.set_color(BLUE)
        r1_l1 = Tex(
            r"Se modelan por separado las densidades condicionales de cada clase $p(x\mid C_k)$ y los \textbf{priores} $p(C_k)$. "
            r"Luego se obtienen las \textbf{posteriores} con la regla de Bayes:",
            font_size=34,
            substrings_to_isolate=[r"$p(x\mid C_k)$", r"$p(C_k)$"]
        )
        for token, col in [(r"$p(x\mid C_k)$", YELLOW), (r"$p(C_k)$", YELLOW)]:
            for m in r1_l1.get_parts_by_tex(token): m.set_color(col)
        r1_eq = MathTex(
            r"p(C_k\mid x)=\frac{p(x\mid C_k)\,p(C_k)}{\sum_j p(x\mid C_j)\,p(C_j)}",
            font_size=44
        )
        r1_eq.set_color_by_tex("p", YELLOW)
        r1_eq.set_color_by_tex("x", BLUE)
        r1_eq.set_color_by_tex("C_k", GREEN)
        r1_eq.set_color_by_tex("C_j", GREEN)
        r1_body = VGroup(r1_l1, r1_eq).arrange(DOWN, buff=body_gap).move_to(ORIGIN)
        self.play(Write(r1_title, run_time=write_speed))
        for m in r1_body: self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(r1_title, r1_body)), run_time=0.6)

        # Slide R2 
        r2_l1 = Tex(
            r"Equivalente: modelar el conjunto $p(x,C_k)$ y normalizar.",
            font_size=34,
            substrings_to_isolate=[r"$p(x,C_k)$"]
        )
        for m in r2_l1.get_parts_by_tex(r"$p(x,C_k)$"): m.set_color(YELLOW)
        r2_l2 = Tex(
            r"Ventajas: con este modelo también se puede calcular la \textbf{marginal} $p(x)$, útil para \textit{detección de novedades/outliers} (puntos con baja probabilidad global). "
            r"Desventaja: es el más exigente en datos y cómputo, especialmente si $x$ es de alta dimensión.",
            font_size=34,
            substrings_to_isolate=[r"$p(x)$", r"$x$"]
        )
        for token, col in [(r"$p(x)$", YELLOW), (r"$x$", BLUE)]:
            for m in r2_l2.get_parts_by_tex(token): m.set_color(col)
        r2_body = VGroup(r2_l1, r2_l2).arrange(DOWN, buff=body_gap).move_to(ORIGIN)
        for m in r2_body: self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(r2_body)), run_time=0.6)

        # Slide R3 
        r3_title = Tex(r"(b) Enfoque discriminativo", font_size=44).to_corner(UL)
        r3_title.set_color(BLUE)
        r3_l1 = Tex(
            r"En lugar de modelar $p(x\mid C_k)$, se estima directamente $p(C_k\mid x)$ y luego se aplica teoría de decisión. "
            r"Suele ser más eficiente cuando solo interesa clasificar.",
            font_size=34,
            substrings_to_isolate=[r"$p(x\mid C_k)$", r"$p(C_k\mid x)$"]
        )
        for token, col in [(r"$p(x\mid C_k)$", YELLOW), (r"$p(C_k\mid x)$", YELLOW)]:
            for m in r3_l1.get_parts_by_tex(token): m.set_color(col)
        r3_body = VGroup(r3_l1).arrange(DOWN, buff=body_gap).move_to(ORIGIN)
        self.play(Write(r3_title, run_time=write_speed))
        for m in r3_body: self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(r3_title, r3_body)), run_time=0.6)

        # Slide R4 
        r4_title = Tex(r"(c) Función discriminante", font_size=44).to_corner(UL)
        r4_title.set_color(BLUE)
        r4_l1 = Tex(
            r"Se aprende una función $f(x)$ que mapea entradas a etiquetas directamente (por ejemplo, $f=0$ para $C_1$, $f=1$ para $C_2$). "
            r"Es el planteamiento más simple porque \textbf{fusiona} inferencia y decisión, pero \textbf{pierde} probabilidades posteriores calibradas.",
            font_size=34,
            substrings_to_isolate=[r"$f(x)$", r"$C_1$", r"$C_2$"]
        )
        for token, col in [(r"$f(x)$", TEAL), (r"$C_1$", GREEN), (r"$C_2$", GREEN)]:
            for m in r4_l1.get_parts_by_tex(token): m.set_color(col)
        r4_body = VGroup(r4_l1).arrange(DOWN, buff=body_gap).move_to(ORIGIN)
        self.play(Write(r4_title, run_time=write_speed))
        self.play(Write(r4_body, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(r4_title, r4_body)), run_time=0.6)

        # Slide R5 
        r5_title = Tex(r"¿Por qué usar posteriores?", font_size=44).to_corner(UL)
        r5_title.set_color(GREEN)
        r5_intro = Tex(
            r"Aunque (c) puede bastar para predecir etiquetas, hay razones fuertes para preferir disponer de \textbf{posteriores} (vía (a) o (b)):",
            font_size=34
        )
        r5_b1 = Tex(
            r"\textemdash{} \textbf{Minimizar riesgo.} Si cambia la matriz de pérdidas, basta con reoptimizar la regla de decisión usando las mismas $p(C_k\mid x)$; "
            r"con solo $f(x)$ habría que \textit{reentrenar}.",
            font_size=34,
            substrings_to_isolate=[r"$p(C_k\mid x)$", r"$f(x)$"]
        )
        for token, col in [(r"$p(C_k\mid x)$", YELLOW), (r"$f(x)$", TEAL)]:
            for m in r5_b1.get_parts_by_tex(token): m.set_color(col)
        r5_b2 = Tex(
            r"\textemdash{} \textbf{Opción de rechazo.} Las posteriores permiten abstenerse en casos inciertos y controlar la fracción rechazada minimizando pérdida esperada.",
            font_size=34
        )
        r5_body = VGroup(r5_intro, r5_b1, r5_b2).arrange(DOWN, buff=body_gap).move_to(ORIGIN)
        self.play(Write(r5_title, run_time=write_speed))
        for m in r5_body: self.play(Write(m, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(r5_title, r5_body)), run_time=0.6)
        
        # Slide R7 
        r7_l1 = Tex(
            r"\textbf{En síntesis:} el enfoque generativo es el más rico (permite $p(x)$ y detección de outliers) pero costoso; "
            r"el discriminativo ofrece buenas clasificaciones con menos esfuerzo; la función discriminante es la más simple pero la menos flexible. "
            r"Contar con probabilidades posteriores abre la puerta a decisiones óptimas bajo cambios de coste, rechazo controlado y correcciones por priores.",
            font_size=34,
            substrings_to_isolate=[r"$p(x)$"]
        )
        for m in r7_l1.get_parts_by_tex(r"$p(x)$"): m.set_color(YELLOW)
        r7_body = VGroup(r7_l1).arrange(DOWN, buff=body_gap).move_to(ORIGIN)
        self.play(Write(r7_body, run_time=write_speed))
        self.wait(0.8)
        self.play(FadeOut(VGroup(r7_body)), run_time=0.6)


#manim -pqh TeoriaDecision.py TeoriaDecision
