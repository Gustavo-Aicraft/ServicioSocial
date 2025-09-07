from manim import *
from manim import config
import numpy as np
config.ffmpeg_executable = r"C:\ffmpeg\bin\ffmpeg.exe"
config.tex_template.add_to_preamble(r"\usepackage{amsmath}")

class TeoriaDecision(Scene):
    def construct(self):
        write_speed = 5  

        # -------------------------------
        #Título
        # -------------------------------
        title = Tex("Teoría de Decisión", font_size=52)
        title.set_color_by_tex("Teoría de Decisión", BLUE)
        self.play(Write(title, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(title))

        # ===============================
        # Slide 1A
        # ===============================
        s1_line1 = Tex(
            r"Una de las formas de entender un modelo de Regresión Lineal es mediante",
            font_size=32
        )
        s1_line2 = Tex(r"una distribución de probabilidad condicional:", font_size=32)

        s1_eq_ptx = MathTex(r"p(t\mid x)", font_size=44)
        s1_eq_ptx.set_color_by_tex("t", PINK)
        s1_eq_ptx.set_color_by_tex("x", PINK)

        s1_line3 = Tex(r"Una forma concreta es mediante una Gaussiana:", font_size=32)

        s1_eq_gauss_form = MathTex(r"p(t\mid x,\mathbf{w},\sigma^2)", font_size=44)
        s1_eq_gauss_form.set_color_by_tex(r"\mathbf{w}", GREEN)
        s1_eq_gauss_form.set_color_by_tex(r"\sigma^2", PURPLE)
        s1_eq_gauss_form.set_color_by_tex("t", RED)
        s1_eq_gauss_form.set_color_by_tex("x", BLUE)

        s1_group = VGroup(
            s1_line1, s1_line2, s1_eq_ptx, s1_line3, s1_eq_gauss_form
        ).arrange(DOWN, buff=0.38).move_to(ORIGIN)

        for mob in s1_group:
            self.play(Write(mob, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(s1_group))

        # ------------------------
        # Slide 2
        # ------------------------
        lineA = Tex(
            r"El objetivo de la teoría de decisiones es convertir una distribución predictiva",
            font_size=32
        )

        lineB_left = Tex(
            r"completa en una predicción puntual óptima", font_size=32
        )
        fx = MathTex(r"f(\mathbf{x})", font_size=42, color=YELLOW)
        rowB = VGroup(lineB_left, fx).arrange(RIGHT, buff=0.18)

        lineC_left = Tex(
            r"Este proceso se formaliza mediante la minimización de la", font_size=32
        )
        loss = Tex(r"pérdida esperada", font_size=32).set_color(ORANGE)
        dot2 = Tex(".", font_size=32)
        rowC = VGroup(lineC_left, loss, dot2).arrange(RIGHT, buff=0.18)

        slide2_intro = VGroup(lineA, rowB, rowC).arrange(DOWN, buff=0.40).move_to(ORIGIN)

        self.play(LaggedStart(*[Write(m) for m in slide2_intro], lag_ratio=0.05, run_time=write_speed))
        self.wait(3)
        self.play(FadeOut(slide2_intro))

        # -----------------
        # Slide 3: 
        # -----------------
        p1 = Tex(
            r"Denotamos a la \textbf{función de pérdida} como $L(t, f(\mathbf{x}))$ que cuantifica el coste "
            r"de predecir $f(\mathbf{x})$ cuando el valor real es $t$. "
            r"La pérdida esperada, o riesgo, se define como la esperanza de esta función de pérdida sobre "
            r"la distribución conjunta de todos los datos posibles:",
            font_size=28
        )
        eq1 = MathTex(
            r"\mathbb{E}[L] = \iint L(t, f(\mathbf{x})) \, p(\mathbf{x}, t) \, d\mathbf{x} \, dt",
            font_size=40
        )
        eq1.set_color_by_tex(r"f(\mathbf{x})", YELLOW)
        eq1.set_color_by_tex(r"\mathbf{x}", BLUE)
        eq1.set_color_by_tex(r"t", RED)
        eq1.set_color_by_tex(r"L", ORANGE)

        slide3_formal = VGroup(p1, eq1).arrange(DOWN, buff=0.6).move_to(ORIGIN)
        for mob in slide3_formal:
            self.play(Write(mob, run_time=write_speed))
        self.wait(3)
        self.play(FadeOut(slide3_formal))

        # ------------------
        # Slide 4
        # ------------------
        p2 = Tex(
            r"Para la función de pérdida cuadrática $L(t, f(\mathbf{x})) = \{f(\mathbf{x}) - t\}^2$, "
            r"podemos resolver el problema de minimización utilizando el \textbf{cálculo de variaciones}. "
            r"Tomamos la derivada funcional de $\mathbb{E}[L]$ con respecto a $f(\mathbf{x})$ y la igualamos a cero:",
            font_size=28
        )
        eq2 = MathTex(
            r"\frac{\delta\mathbb{E}[L]}{\delta f(\mathbf{x})} = "
            r"2\int\{f(\mathbf{x})-t\}\,p(\mathbf{x},t)\, dt = 0",
            font_size=38
        )
        eq2.set_color_by_tex(r"f(\mathbf{x})", YELLOW)
        eq2.set_color_by_tex(r"\mathbf{x}", BLUE)
        eq2.set_color_by_tex(r"t", GREEN)
        eq2.set_color_by_tex(r"L", GREEN)
        eq2.set_color_by_tex(r"p(\mathbf{x},t)", GREEN)

        p3 = Tex(
            r"Resolver esta ecuación lleva al resultado fundamental: la predicción que minimiza la pérdida "
            r"cuadrática esperada es la \textbf{media de la distribución condicional} $p(t|\mathbf{x})$, "
            r"también conocida como la \textbf{función de regresión}.",
            font_size=28
        )
        eq3 = MathTex(
            r"f^*(\mathbf{x}) = \int t \, p(t|\mathbf{x}) \, dt = \mathbb{E}_t[t|\mathbf{x}]",
            font_size=40
        )
        eq3.set_color_by_tex(r"f^*(\mathbf{x})", GREEN)
        eq3.set_color_by_tex(r"\mathbf{x}", GREEN)
        eq3.set_color_by_tex(r"t", GREEN)
        eq3.set_color_by_tex(r"p(t|\mathbf{x})", GREEN)

        slide4_quad = VGroup(p2, eq2, p3, eq3).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        for mob in slide4_quad:
            self.play(Write(mob, run_time=write_speed))
        self.wait(3)
        self.play(FadeOut(slide4_quad))

        # --------------
        # Slide 4.5
        # --------------
        nota_es = VGroup(
            Tex("La función de regresión", font_size=28),
            MathTex(r"f^{\star}(x)", font_size=36, color=RED),
            Tex("minimiza la pérdida cuadrática esperada,", font_size=28),
            Tex("y es la media de la distribución condicional", font_size=28),
            MathTex(r"p(t\mid x)", font_size=34, color=BLUE),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).to_edge(LEFT, buff=0.9)

        axes3 = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 3, 1],
            x_length=6.4, y_length=4.0,
            tips=True,
            axis_config={"color": BLUE}
        )
        x_lbl = MathTex("x", color=BLUE)
        y_lbl = MathTex("t", color=RED)
        labels3 = axes3.get_axis_labels(x_label=x_lbl, y_label=y_lbl)

        def fstar(x):
            return 0.9 * np.tanh(0.9*(x-2.2)) + 0.22*(x-2.2) + 1.0

        fcurve = axes3.plot(lambda x: fstar(x), x_range=[0, 6], color=RED, stroke_width=5)

        x_pos = 5.2
        f_tag = MathTex(r"f^{\star}(x)", color=RED, font_size=32)
        f_tag.move_to(axes3.c2p(x_pos, fstar(x_pos)) + UP*0.60 + RIGHT*0.10)

        x0 = 3.2
        vline = DashedLine(
            axes3.c2p(x0, 0),
            axes3.c2p(x0, axes3.y_range[1]),
            color=GRAY, stroke_width=3, dash_length=0.18
        )

        mu, sigma, wmax = fstar(x0), 0.35, 0.55
        t0, t1 = mu - 2.4*sigma, mu + 2.4*sigma
        band_right = ParametricFunction(
            lambda t: axes3.c2p(x0 + wmax*np.exp(-0.5*((t-mu)/sigma)**2), t),
            t_range=[t0, t1], color=BLUE, stroke_width=5
        )

        pdf_lbl = MathTex(r"p(t\mid x_0,\mathbf{w},\sigma^2)", font_size=30)
        pdf_lbl.set_color_by_tex(r"x_0", BLUE)
        pdf_lbl.set_color_by_tex(r"\mathbf{w}", BLUE)
        pdf_lbl.set_color_by_tex(r"\sigma^2", BLUE)
        pdf_lbl.set_color_by_tex(r"t", BLUE)
        pdf_lbl.next_to(band_right, RIGHT, buff=0.24)

        plot_grp = VGroup(axes3, labels3, fcurve, f_tag, vline, band_right, pdf_lbl)
        plot_grp.scale(0.92).to_edge(RIGHT, buff=0.75)

        self.play(LaggedStart(*[Write(m) for m in nota_es], lag_ratio=0.10, run_time=1.1))
        self.play(Create(axes3), Write(labels3))
        self.play(Create(fcurve), run_time=write_speed)
        self.play(Create(vline))
        self.play(Create(band_right))
        self.play(Write(pdf_lbl), Write(f_tag))
        self.wait(2)
        self.play(FadeOut(VGroup(nota_es, plot_grp)))

        # ----------------
        # Slide 5
        # ----------------
        subtitle3 = Tex(r"Descomposición del Error:", font_size=38, color=ORANGE)
        p4 = Tex(
            r"Al descomponer $f(\mathbf{x}) - t$ de la forma "
            r"$f(\mathbf{x}) - t =(f(\mathbf{x}) - \mathbb{E}[t|\mathbf{x}]) + (\mathbb{E}[t|\mathbf{x}] - t)$ "
            r"y expandir el cuadrado dentro de la integral de la pérdida esperada. "
            r"Tras resolver las integrales, se obtiene:",
            font_size=28
        )
        eq4 = MathTex(
            r"\mathbb{E}[L] = "
            r"\underbrace{\int \left\{ f(\mathbf{x}) - \mathbb{E}[t|\mathbf{x}] \right\}^2 p(\mathbf{x}) \, d\mathbf{x}}_{\text{Error del Modelo}}"
            r"+"
            r"\underbrace{\int \mathrm{Var}[t|\mathbf{x}] \, p(\mathbf{x}) \, d\mathbf{x}}_{\text{Ruido Irreducible}}",
            font_size=34
        )
        eq4.set_color_by_tex(r"f(\mathbf{x})", YELLOW)
        eq4.set_color_by_tex(r"\mathbb{E}[t|\mathbf{x}]", PURPLE)
        eq4.set_color_by_tex(r"\mathbf{x}", BLUE)
        eq4.set_color_by_tex(r"t", RED)
        eq4.set_color_by_tex(r"p(\mathbf{x})", ORANGE)
        eq4.set_color_by_tex(r"\mathrm{Var}[t|\mathbf{x}]", GREEN)

        bullet1 = Tex(
            r"\textbf{Error del Modelo:} Cuantifica cuánto se desvía nuestra predicción $f(\mathbf{x})$ "
            r"de la predicción ideal $\mathbb{E}[t|\mathbf{x}]$. Este término se puede reducir eligiendo un buen modelo.",
            font_size=28
        )
        bullet2 = Tex(
            r"\textbf{Ruido Irreducible:} Representa la varianza intrínseca de la variable objetivo $t$. "
            r"Es el error mínimo inevitable, inherente a los propios datos, y ningún modelo puede eliminarlo.",
            font_size=28
        )
        bullets = VGroup(bullet1, bullet2).arrange(DOWN, buff=0.35)

        slide5_error = VGroup(subtitle3, p4, eq4, bullets).arrange(DOWN, buff=0.6).move_to(ORIGIN)
        for mob in slide5_error:
            self.play(Write(mob, run_time=write_speed))
        self.wait(3)
        self.play(FadeOut(slide5_error))




        
#manim -pql TeoriaDecision.py TeoriaDecision