from manim import *
from manim import config
config.tex_template.add_to_preamble(r"\usepackage{amsmath}")

C_X = BLUE
C_T = RED
C_F = YELLOW
C_H = GREEN
C_E = ORANGE
C_D = PURPLE
C_P = TEAL

class SesgoVarianza(Scene):
    def construct(self):
        write_speed = 3

        # ------------------------------------------------------------------
        # Slide Título
        # ------------------------------------------------------------------
        title = Tex("El equilibrio Sesgo–Varianza", font_size=52).set_color(BLUE)
        self.play(Write(title, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(title))

        # ------------------------------------------------------------------
        # Slide 1
        # ------------------------------------------------------------------
        s1_title = Tex(r"¿Qué problema resolvemos en regresión?", font_size=46)
        s1_title.set_color_by_tex("¿Qué problema resolvemos en regresión?", ORANGE)
        s1_a = Tex(
            r"Observamos pares $(x,t)$ generados por una distribución desconocida.",
            font_size=32,
            substrings_to_isolate=[r"$(x,t)$"]
        )
        s1_a.set_color_by_tex(r"$(x,t)$", PINK) 
    
        s1_a_parts = VGroup(
            Tex(r"Observamos pares ", font_size=32),
            MathTex(r"(x,t)", font_size=36).set_color_by_tex("x", PINK).set_color_by_tex("t", PINK),
            Tex(r" generados por una distribución desconocida,", font_size=32),
        ).arrange(RIGHT, buff=0.08)

        s1_b = Tex(
            r"donde el objetivo es predecir $t$ a partir de $x$ con el menor error posible.",
            font_size=32,
            substrings_to_isolate=[r"$t$", r"$x$"]
        )
        s1_b.set_color_by_tex(r"$t$", GREEN)
        s1_b.set_color_by_tex(r"$x$", YELLOW)

        s1_c = Tex(
            r"Con datos finitos, cualquier modelo aprendido dependerá de la muestra.",
            font_size=32
        )

        s1_group = VGroup(
            s1_title,
            s1_a_parts, 
            s1_b,
            s1_c
        ).arrange(DOWN, buff=0.38).move_to(ORIGIN)

        for mob in s1_group:
            self.play(Write(mob, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(s1_group))

        # ------------------------------------------------------------------
        # Slide 2
        # ------------------------------------------------------------------
        s2_title = Tex("Mejor predictor con pérdida cuadrática", font_size=40).set_color(ORANGE)
        s2_line = Tex("Si usamos pérdida cuadrática, el mejor predictor de $t$ dado $x$ es:", font_size=32,
                      substrings_to_isolate=[r"$t$", r"$x$"])
        s2_line.set_color_by_tex(r"$t$", C_T)
        s2_line.set_color_by_tex(r"$x$", C_X)

        s2_eq = MathTex(r"h(x)=\mathbb{E}[t\mid x]=\int t\,p(t\mid x)\,dt", font_size=44)
        s2_eq.set_color_by_tex("h(x)", C_H)
        s2_eq.set_color_by_tex(r"\mathbb{E}", C_E)
        s2_eq.set_color_by_tex("x", C_X)
        s2_eq.set_color_by_tex("t", C_T)
        s2_eq.set_color_by_tex("p", C_P)

        s2_group = VGroup(s2_title, s2_line, s2_eq).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        for mob in s2_group:
            self.play(Write(mob, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(s2_group))

        # ------------------------------------------------------------------
        # Slide 3
        # ------------------------------------------------------------------
        s3_title = Tex("Pérdida esperada", font_size=40).set_color(ORANGE)
        s3_a = Tex("La pérdida esperada se puede escribir como:", font_size=32)

        s3_eq = MathTex(
            r"\mathbb{E}[L] \;=\; \int \big(f(x)-h(x)\big)^{2} p(x)\,dx"
            r"\;+\; \iint \big(h(x)-t\big)^{2} p(x,t)\,dx\,dt",
            font_size=40
        )
        s3_eq.set_color_by_tex("f(x)", BLUE)
        s3_eq.set_color_by_tex("h(x)", BLUE)
        s3_eq.set_color_by_tex("x", BLUE)
        s3_eq.set_color_by_tex("t", BLUE)
        s3_eq.set_color_by_tex("p", BLUE)
        s3_eq.set_color_by_tex(r"\mathbb{E}", BLUE)

        s3_b = Tex("El segundo término es el ruido irreducible; no depende de $f(x)$.",
                   font_size=32, substrings_to_isolate=[r"$f(x)$"])
        s3_b.set_color_by_tex(r"$f(x)$", C_F)

        s3_group = VGroup(s3_title, s3_a, s3_eq, s3_b).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        for mob in s3_group:
            self.play(Write(mob, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(s3_group))

        # ------------------------------------------------------------------
        # Slide 4
        # ------------------------------------------------------------------
        s4_title = Tex("Con datos finitos, el modelo aprendido varía", font_size=40).set_color(ORANGE)

        s4_a = Tex(
            r"Entrenamos con un conjunto $\mathcal{D}$ y obtenemos $f(x;\mathcal{D})$,",
            font_size=32,
            substrings_to_isolate=[r"$\mathcal{D}$", r"$f(x;\mathcal{D})$"]
        )
        s4_a.set_color_by_tex(r"$\mathcal{D}$", RED)
        s4_a.set_color_by_tex(r"$f(x;\mathcal{D})$", C_F)

        s4_b = Tex(
            r"con otro conjunto $\mathcal{D}'$ obtendríamos otra función.",
            font_size=32,
            substrings_to_isolate=[r"$\mathcal{D}'$"]
        )
        s4_b.set_color_by_tex(r"$\mathcal{D}'$", RED)

        s4_c = Tex(
            r"Para evaluar el modelo, miramos el error medio sobre conjuntos $\mathcal{D}$:",
            font_size=32,
            substrings_to_isolate=[r"$\mathcal{D}$"]
        )
        s4_c.set_color_by_tex(r"$\mathcal{D}$", RED)

        s4_eq = MathTex(r"\mathbb{E}_{\mathcal{D}}\!\big[(f(x;\mathcal{D})-h(x))^{2}\big]", font_size=44)
        s4_eq.set_color_by_tex(r"\mathcal{D}", C_D)
        s4_eq.set_color_by_tex("f(x", C_F)
        s4_eq.set_color_by_tex("h(x)", C_H)
        s4_eq.set_color_by_tex("x", C_X)

        s4_group = VGroup(s4_title, s4_a, s4_b, s4_c, s4_eq).arrange(DOWN, buff=0.42).move_to(ORIGIN)
        for mob in s4_group:
            self.play(Write(mob, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(s4_group))

        # ------------------------------------------------------------------
        # Slide 5
        # ------------------------------------------------------------------
        s5_title = Tex("Derivación: Sesgo–Varianza", font_size=40)
        s5_eq = MathTex(
            r"\begin{aligned}"
            r"\mathbb{E}_{\mathcal{D}}\!\big[(f(x;\mathcal{D})-h(x))^{2}\big]"
            r"&=\;\mathbb{E}_{\mathcal{D}}\!\Big[\big(f-\mathbb{E}_{\mathcal{D}}[f]+\mathbb{E}_{\mathcal{D}}[f]-h\big)^{2}\Big] \\[4pt]"
            r"&=\;\underbrace{\big(\mathbb{E}_{\mathcal{D}}[f(x;\mathcal{D})]-h(x)\big)^{2}}_{\text{sesgo}^{2}}"
            r"\;+\;\underbrace{\mathbb{E}_{\mathcal{D}}\!\Big[\big(f(x;\mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(x;\mathcal{D})]\big)^{2}\Big]}_{\text{varianza}}"
            r"\end{aligned}",
            font_size=38
        )
        for token, col in [(r"\mathcal{D}", RED), ("f(x", RED), ("h(x)", RED), ("x", RED), (r"\mathbb{E}", RED)]:
            s5_eq.set_color_by_tex(token, col)

        s5_group = VGroup(s5_title, s5_eq).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        for mob in s5_group:
            self.play(Write(mob, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(s5_group))

        # ------------------------------------------------------------------
        # Slide 6:
        # ------------------------------------------------------------------
        s6_title = Tex("Resultado integrado sobre $x$", font_size=40).set_color(ORANGE)
        s6_eq1 = MathTex(
            r"\text{error esperado} \;=\; (\text{sesgo})^{2} \;+\; \text{varianza} \;+\; \text{ruido}",
            font_size=42
        )
        s6_eq2 = MathTex(
            r"\begin{aligned}"
            r"(\text{sesgo})^{2} \;&=\; \int \big(\mathbb{E}_{\mathcal{D}}[f(x;\mathcal{D})]-h(x)\big)^{2}\,p(x)\,dx \\[2pt]"
            r"\text{varianza} \;&=\; \int \mathbb{E}_{\mathcal{D}}\!\Big[(f(x;\mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(x;\mathcal{D})])^{2}\Big]\,p(x)\,dx \\[2pt]"
            r"\text{ruido} \;&=\; \iint \big(h(x)-t\big)^{2}\,p(x,t)\,dx\,dt"
            r"\end{aligned}",
            font_size=36
        )
        for token, col in [(r"\mathcal{D}", GREEN), ("f(x", GREEN), ("h(x)", GREEN), ("x", GREEN), ("t", GREEN), ("p", GREEN), (r"\mathbb{E}", GREEN    )]:
            s6_eq2.set_color_by_tex(token, col)

        s6_group = VGroup(s6_title, s6_eq1, s6_eq2).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        for mob in s6_group:
            self.play(Write(mob, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(s6_group))

        # ------------------------------------------------------------------
        # Slide 7:
        # ------------------------------------------------------------------
        s7_title = Tex("Interpretación de los términos", font_size=40).set_color(ORANGE)
        s7_a = Tex(
            r"\textbf{Sesgo:} diferencia sistemática entre la predicción promedio y la función ideal $h(x)$.",
            font_size=32, substrings_to_isolate=[r"$h(x)$"]
        ).set_color_by_tex(r"$h(x)$", C_H)

        s7_b = Tex(
            r"\textbf{Varianza:} sensibilidad de la predicción al cambiar de conjunto de entrenamiento.",
            font_size=32
        )

        s7_c = Tex(
            r"\textbf{Ruido:} variación intrínseca de $t$ dada $x$; ningún método puede eliminarla.",
            font_size=32, substrings_to_isolate=[r"$t$", r"$x$"]
        )
        s7_c.set_color_by_tex(r"$t$", C_T)
        s7_c.set_color_by_tex(r"$x$", C_X)

        s7_group = VGroup(s7_title, s7_a, s7_b, s7_c).arrange(DOWN, buff=0.38).move_to(ORIGIN)
        for mob in s7_group:
            self.play(Write(mob, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(s7_group))

        # ------------------------------------------------------------------
        # Slide 8
        # ------------------------------------------------------------------
        s8_title = Tex("Consecuencia práctica", font_size=40).set_color(ORANGE)
        s8_a = Tex("Modelos muy simples suelen tener alto sesgo y baja varianza.", font_size=32)
        s8_b = Tex("Modelos muy flexibles tienden a bajo sesgo y alta varianza.", font_size=32)
        s8_c = Tex("El buen desempeño surge de equilibrar ambos para minimizar el error esperado.", font_size=32)

        s8_group = VGroup(s8_title, s8_a, s8_b, s8_c).arrange(DOWN, buff=0.38).move_to(ORIGIN)
        for mob in s8_group:
            self.play(Write(mob, run_time=write_speed))
        self.wait(2)
        self.play(FadeOut(s8_group))



#manim -pqh SesgoVarianza.py SesgoVarianza