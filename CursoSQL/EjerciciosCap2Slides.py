from manim import *
from pathlib import Path
from manim.utils.tex_templates import TexTemplate, TexTemplateLibrary

# ===================== Config =====================

config.background_color = WHITE
config.pixel_width  = 1920
config.pixel_height = 1080
config.frame_rate   = 60

WRITE_MEDIUM_RT = 3.0
TITLE_IN_RT     = 1.5

Tex.set_default(font_size=44, color=BLACK)
MathTex.set_default(font_size=44, color=BLACK)
Text.set_default(font_size=44, color=BLACK)

# ====== LaTeX template (sin babel para evitar clashes) + UTF-8 y listings ======

tex_template: TexTemplate = TexTemplateLibrary.simple.copy()
tex_template.add_to_preamble(r"""
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, mathtools}
\usepackage{xcolor}
\usepackage{array, booktabs, multirow, tabularx}
\usepackage{siunitx}
\usepackage{graphicx}
\usepackage{upquote}
\usepackage{inconsolata}
\usepackage{listings}

\definecolor{myPurple}{HTML}{7B3FBC}
\definecolor{kw}{HTML}{005CC5}
\definecolor{str}{HTML}{D73A49}
\definecolor{com}{HTML}{6A737D}

\lstdefinelanguage{SQLcustom}{
sensitive=false,
morekeywords=[1]{SELECT,FROM,WHERE,ORDER,BY,GROUP,HAVING,JOIN,INNER,LEFT,RIGHT,OUTER,ON,COUNT,AS,AND,OR,NOT,IN,LIKE,TOP,LIMIT,FETCH,FIRST,ROWS,ONLY,DATE,DESC,ASC},
morekeywords=[2]{DATABASE,TABLE},
morecomment=[l][\color{green!50!black}]{--},      % ← línea-comentario (verde) domina sobre keywords
morecomment=[s][\color{green!50!black}]{/*}{*/},  % ← bloque-comentario (verde) domina sobre keywords
morestring=[b]',
morestring=[b]"
}

\lstdefinestyle{sqlBlue}{
backgroundcolor=\color{white},
basicstyle=\ttfamily\small,
keywordstyle=\color{kw}\bfseries,
stringstyle=\color{str},
commentstyle=\color{com},
showstringspaces=false,
frame=none,
keepspaces=true,
columns=fullflexible,
breaklines=true
}

% Acentos UTF-8 dentro de lstlisting
\lstset{literate=
{á}{{'a}}1 {é}{{'e}}1 {í}{{'i}}1 {ó}{{'o}}1 {ú}{{'u}}1
{Á}{{'A}}1 {É}{{'E}}1 {Í}{{'I}}1 {Ó}{{'O}}1 {Ú}{{'U}}1
{ñ}{{~n}}1 {Ñ}{{~N}}1 {ü}{{"u}}1 {Ü}{{"U}}1
}
""")

# ===================== Contenido (Slides 1) =====================

TITLE_MAIN = r"\section*{\textcolor{myPurple}{Fundamentos de Consultas SQL: \textbf{Ejercicios}}}"


# ===================== Única clase =====================

class FundamentosSQL_Ejercicios(Scene):
    FRAME_COLOR  = PURPLE_E
    FRAME_STROKE = 20  # marco “un poco más grueso”

    # ---------- utils ----------
    def _write_block(self, tex_str, scale=1.0):
        m = Tex(tex_str, tex_template=tex_template)
        if scale != 1.0:
            m.scale(scale)
        m.move_to(ORIGIN)
        return m

    def _appear(self, mob, direction=DOWN, rt=0.9):
        self.play(FadeIn(mob, shift=0.6*direction, run_time=rt)); self.wait(0.05)

    def _disappear(self, *mobs, rt=0.6):
        targets = [m for m in mobs if m is not None]
        if targets:
            self.play(*[FadeOut(m) for m in targets], run_time=rt); self.wait(0.05)

    def _first_existing(self, *cands: str) -> str | None:
        for p in cands:
            if p and Path(p).exists():
                return p
        return None

    def _ensure_logo(self, animate=False):
        if not hasattr(self, "_logo"):
            p = self._first_existing(
                "LogoAicraft.png", "images/LogoAicraft.png",
                "/mnt/data/LogoAicraft.png", r"C:\Users\rolg0\Downloads\LogoAicraft.png"
            )
            if p:
                lg = ImageMobject(p)
                lg.height = 0.8
                lg.to_corner(UL, buff=0)   # EXACTO en la esquina
                self._logo = lg
                if animate: self._appear(self._logo, direction=DOWN, rt=0.6)
                else: self.add(self._logo)
        else:
            self._logo.height = 0.8
            self._logo.to_corner(UL, buff=0)
            self.add(self._logo)
        if hasattr(self, "_logo"): self.bring_to_front(self._logo)

    def _ensure_frame(self):
        if not hasattr(self, "_frame"):
            fr = Rectangle(
                width=config.frame_width, height=config.frame_height,
                stroke_color=self.FRAME_COLOR, stroke_width=self.FRAME_STROKE,
                fill_opacity=0.0
            ).move_to(ORIGIN)
            self._frame = fr
        if self._frame not in self.mobjects:
            self.add(self._frame)
        self.bring_to_front(self._frame)
        if hasattr(self, "_logo"): self.bring_to_front(self._logo)

    def _fit_group_center(self, *mobs, pad_x=1.0, pad_y=0.8):
        g = Group(*mobs)
        frame_w, frame_h = config.frame_width, config.frame_height
        allowed_w = frame_w - 2*pad_x
        allowed_h = frame_h - 2*pad_y
        sw = allowed_w / g.width  if g.width  > allowed_w else 1.0
        sh = allowed_h / g.height if g.height > allowed_h else 1.0
        sf = min(sw, sh, 1.0)
        if sf < 1.0: g.scale(sf)
        g.move_to(ORIGIN)
        return g

    # ---------------- construct ----------------
    def construct(self):
            # ===== SLIDE 1 (portada tipo hero, SIN marco) =====
        self._ensure_logo(animate=True)

        # --- assets ---
        p_footer = self._first_existing(
            "footer_portada.png", "images/footer_portada.png",
            r"C:\Users\rolg0\Downloads\SS\ImagesSQL_Slides\PiePortada.png"
        )
        p_aj = self._first_existing(
            "AjoloteAicraft.png", "images/AjoloteAicraft.png",
            "/mnt/data/AjoloteAicraft.png", r"C:\Users\rolg0\Downloads\AjoloteEjercicios.png"
        )

        # --- elementos base ---
        title = self._write_block(TITLE_MAIN)  # ya tienes este string
        footer = ImageMobject(p_footer) if p_footer else None
        aj     = ImageMobject(p_aj) if p_aj else None

        # --- layout numérico (márgenes hero) ---
        frame_w, frame_h = config.frame_width, config.frame_height
        left_pad   = 0.8    # separación del borde izquierdo
        right_pad  = 0.8    # separación del borde derecho
        gap_lr     = 1.0    # separación horizontal entre título y ajolote
        safe_top   = 0.9    # zona segura por el logo (ajuste fino)
        footer_hf  = 0.28   # fracción de alto para el pie
        aj_hf      = 0.55   # fracción de alto para el ajolote

        # --- footer: ocupa todo el ancho y se pega abajo ---
        if footer:
            footer.set_height(footer_hf * frame_h)
            footer.to_edge(DOWN, buff=0)
            footer.set_width(frame_w)  # asegurar ancho completo
            self._appear(footer, direction=UP, rt=0.6)

        # --- ajolote: a la derecha, sobre el footer ---
        if aj:
            # alto cómodo, limitado por el espacio libre sobre el footer
            max_h = (frame_h * (1.0 - footer_hf) - 0.6)
            aj.set_height(min(aj_hf * frame_h, max_h))
            if footer:
                aj.next_to(footer, UP, buff=0.25)
            else:
                aj.to_edge(DOWN, buff=1.0)
            aj.to_edge(RIGHT, buff=right_pad)
            self._appear(aj, direction=LEFT, rt=0.8)

        # --- título: a la izquierda, alineado y sin encimar el footer ---
        # ancho máximo disponible a la izquierda del ajolote
        if aj:
            left_max_w = aj.get_left()[0] - (-frame_w/2 + left_pad) - gap_lr
        else:
            left_max_w = frame_w/2 - left_pad

        if left_max_w > 0 and title.width > left_max_w:
            title.scale(left_max_w / title.width)

        # posición base del título (columna izquierda)
        title.to_edge(LEFT, buff=left_pad)

        # alinearlo verticalmente para que quede por encima del footer
        if footer:
            min_y = footer.get_top()[1] + 0.35
            dy = min_y - title.get_bottom()[1]
            if dy > 0:
                title.shift(UP * dy)

        # evitar choque con el logo (bajarlo si queda muy arriba)
        if hasattr(self, "_logo"):
            top_limit = self._logo.get_bottom()[1] - 0.35
            if title.get_top()[1] > top_limit:
                title.shift(DOWN * (title.get_top()[1] - top_limit))

        self.play(Write(title, run_time=TITLE_IN_RT)); self.wait(0.2)

        # asegurar capas (ajolote arriba del footer, logo siempre al frente)
        if aj: self.bring_to_front(aj)
        if hasattr(self, "_logo"): self.bring_to_front(self._logo)

        # pequeña pausa y salida para dar lugar a la Slide 2
        self.wait(0.6)
        self._disappear(title, aj, footer)

    # manim -pql EjerciciosCap2Slides.py FundamentosSQL