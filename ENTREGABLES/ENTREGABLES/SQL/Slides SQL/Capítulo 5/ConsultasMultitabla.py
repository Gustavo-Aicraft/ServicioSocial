from manim import *
from pathlib import Path
from manim.utils.tex_templates import TexTemplate, TexTemplateLibrary

config.background_color = WHITE
config.pixel_width  = 1920
config.pixel_height = 1080
config.frame_rate   = 60

WRITE_MEDIUM_RT = 8.0
TITLE_IN_RT     = 4.0

Tex.set_default(font_size=44, color=BLACK)
MathTex.set_default(font_size=44, color=BLACK)
Text.set_default(font_size=44, color=BLACK)

tex_template: TexTemplate = TexTemplateLibrary.simple.copy()
tex_template.add_to_preamble(r"""
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, mathtools}
\usepackage{array, booktabs, multirow, tabularx}
\usepackage[table]{xcolor}      
\usepackage{colortbl}           
\usepackage{siunitx}
\usepackage{graphicx}
\usepackage{upquote}
\usepackage{inconsolata}
\usepackage{listings}
\usepackage{tikz}
\usepackage[most]{tcolorbox}

\definecolor{sqlBlue}{RGB}{0,102,204}
\definecolor{softBlue}{RGB}{232,244,253}
\definecolor{softGreen}{RGB}{235,247,234}
\definecolor{softGray}{RGB}{248,248,248}
\definecolor{headerGray}{RGB}{80,80,80}

\definecolor{myPurple}{HTML}{7B3FBC}
\definecolor{kw}{HTML}{005CC5}
\definecolor{str}{HTML}{D73A49}
\definecolor{com}{HTML}{6A737D}

\lstdefinelanguage{SQLcustom}{
  sensitive=false,
  morekeywords=[1]{SELECT,FROM,WHERE,ORDER,BY,GROUP,HAVING,JOIN,INNER,LEFT,RIGHT,OUTER,ON,COUNT,AS,AND,OR,NOT,IN,LIKE,TOP,LIMIT,FETCH,FIRST,NEXT,ROWS,ROW,ONLY,DATE,DESC,ASC,OFFSET},
  morekeywords=[2]{DATABASE,TABLE},
  morecomment=[l][\color{green!50!black}]{--},
  morecomment=[s][\color{green!50!black}]{/*}{*/},
  morestring=[b]', morestring=[b]"
}
\lstdefinestyle{sqlBlue}{
  backgroundcolor=\color{white},
  basicstyle=\ttfamily,                
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
  {á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'\i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1
  {Á}{{\'A}}1 {É}{{\'E}}1 {Í}{{\'I}}1 {Ó}{{\'O}}1 {Ú}{{\'U}}1
  {ñ}{{\~n}}1 {Ñ}{{\~N}}1 {ü}{{\"u}}1 {Ü}{{\"U}}1
}
""")

TITLE_MAIN = r"\section*{\textcolor{myPurple}{Consultas Multitabla}}"

class ConsultasMultitabla(Scene):
    FRAME_COLOR  = PURPLE_E
    FRAME_STROKE = 20

    def _write_block(self, tex_str, scale=1.0):
        m = Tex(tex_str, tex_template=tex_template)
        if scale != 1.0:
            m.scale(scale)
        m.move_to(ORIGIN)
        return m

    def _appear(self, mob, direction=DOWN, rt=WRITE_MEDIUM_RT):
        def _flatten(m):
            if isinstance(m, (Group, VGroup)):
                for sm in m.submobjects:
                    yield from _flatten(sm)
            else:
                yield m

        if isinstance(mob, (Group, VGroup)):
            anims = []
            for sm in _flatten(mob):
                if isinstance(sm, VMobject):
                    anims.append(Write(sm, run_time=rt))
                else:
                    anims.append(FadeIn(sm, shift=0.6 * direction, run_time=rt))
            if anims:
                self.play(*anims)
                self.wait(0.05)
            return

        if isinstance(mob, VMobject):
            self.play(Write(mob, run_time=rt)); self.wait(0.05)
        else:
            self.play(FadeIn(mob, shift=0.6 * direction, run_time=rt)); self.wait(0.05)

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
                "/home/gustavo/SS/ImagesSQL_Slides/LogoAicraft.png"
            )
            if p:
                lg = ImageMobject(p)
                lg.height = 0.8
                lg.to_corner(UL, buff=0)
                lg.set_z_index(1000) 
                self._logo = lg
                if animate: self._appear(self._logo, direction=DOWN, rt=0.6)
                else: self.add(self._logo)
        else:
            self._logo.height = 0.8
            self._logo.to_corner(UL, buff=0)
            self._logo.set_z_index(1000)  
            self.add(self._logo)

        if hasattr(self, "_logo"):
            self.bring_to_front(self._logo)

    def _ensure_frame(self):
        if not hasattr(self, "_frame"):
            fr = Rectangle(
                width=config.frame_width, height=config.frame_height,
                stroke_color=self.FRAME_COLOR, stroke_width=self.FRAME_STROKE,
                fill_opacity=0.0
            ).move_to(ORIGIN)
            fr.set_z_index(900)  
            self._frame = fr

        self._frame.set_z_index(900) 

        if self._frame not in self.mobjects:
            self.add(self._frame)

        self.bring_to_front(self._frame)
        if hasattr(self, "_logo"):
            self.bring_to_front(self._logo)


    def _fit_group_center(self, *mobs, pad_x=1.0, pad_y=0.9):
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
    def _clip_to_rect(self, mob, clip_rect: VMobject):
        def _flatten(m):
            if isinstance(m, (Group, VGroup)):
                for sm in m.submobjects:
                    yield from _flatten(sm)
            else:
                yield m

        for sm in _flatten(mob):
            if isinstance(sm, VMobject):
                try:
                    sm.set_clip_path(clip_rect)
                except Exception:
                    pass

    def _scroll_code_in_window(
        self,
        tex_str: str,
        *,
        window_w=0.92,
        window_h=0.74,
        down=0.10,
        pad=0.22,
        rt_write=3.0,          
        rt_scroll=14.0,
        rt_out=0.6,
        show_border=False,
        border_width=2.0,
    ):
    
        win = Rectangle(
            width=window_w * config.frame_width,
            height=window_h * config.frame_height,
            stroke_width=(border_width if show_border else 0.0),
            stroke_color=BLACK,
            fill_opacity=0.0,
        ).move_to(ORIGIN).shift(down * DOWN)

        block = self._write_block(tex_str)

        max_w = 0.985 * win.width
        try:
            block.scale_to_fit_width(max_w)
        except Exception:
            pass

        top_y = win.get_top()[1] - pad
        block.move_to(win.get_center())
        block.shift(UP * (top_y - block.get_top()[1]))

        eps = 0.03
        fw = config.frame_width
        fh = config.frame_height
        frame_left, frame_right = -fw / 2, fw / 2
        frame_bottom, frame_top = -fh / 2, fh / 2

        wl = win.get_left()[0]
        wr = win.get_right()[0]
        wt = win.get_top()[1]
        wb = win.get_bottom()[1]

        cover_top = Rectangle(
            width=(frame_right - frame_left) + 2 * eps,
            height=max(0.0, frame_top - wt) + 2 * eps,
            stroke_width=0,
            fill_opacity=1.0,
            fill_color=WHITE,
        ).move_to([0.0, (frame_top + wt) / 2, 0.0])

        cover_bottom = Rectangle(
            width=(frame_right - frame_left) + 2 * eps,
            height=max(0.0, wb - frame_bottom) + 2 * eps,
            stroke_width=0,
            fill_opacity=1.0,
            fill_color=WHITE,
        ).move_to([0.0, (wb + frame_bottom) / 2, 0.0])

        cover_left = Rectangle(
            width=max(0.0, wl - frame_left) + 2 * eps,
            height=(wt - wb) + 2 * eps,
            stroke_width=0,
            fill_opacity=1.0,
            fill_color=WHITE,
        ).move_to([(frame_left + wl) / 2, (wt + wb) / 2, 0.0])

        cover_right = Rectangle(
            width=max(0.0, frame_right - wr) + 2 * eps,
            height=(wt - wb) + 2 * eps,
            stroke_width=0,
            fill_opacity=1.0,
            fill_color=WHITE,
        ).move_to([(wr + frame_right) / 2, (wt + wb) / 2, 0.0])

        win.set_z_index(100)
        block.set_z_index(200, family=True)
        for c in (cover_top, cover_bottom, cover_left, cover_right):
            c.set_z_index(300)

        self.add(win, block, cover_top, cover_bottom, cover_left, cover_right)

        if hasattr(self, "_frame"):
            self._frame.set_z_index(900)
            self.bring_to_front(self._frame)
        if hasattr(self, "_logo"):
            self._logo.set_z_index(1000)
            self.bring_to_front(self._logo)

        self.play(Write(block, run_time=rt_write))
        self.wait(0.4)

        visible_h = win.height - 2 * pad
        scroll_dist = max(0.0, block.height - visible_h)

        if scroll_dist > 0:
            self.play(block.animate.shift(UP * scroll_dist), run_time=rt_scroll, rate_func=linear)
            self.wait(0.4)
        else:
            self.wait(0.8)

        self.play(
            FadeOut(block),
            FadeOut(win),
            FadeOut(cover_top), FadeOut(cover_bottom), FadeOut(cover_left), FadeOut(cover_right),
            run_time=rt_out
        )
        self.wait(0.05)

        if hasattr(self, "_frame"):
            self.bring_to_front(self._frame)
        if hasattr(self, "_logo"):
            self.bring_to_front(self._logo)

    def construct(self):
        def _fit(self, mob, w=0.78, h=0.74, down=0.08):
            max_w = w * config.frame_width
            max_h = h * config.frame_height
            try:
                mob.scale_to_fit_width(max_w)
                if mob.height > max_h:
                    mob.scale_to_fit_height(max_h)
            except Exception:
                pass
            return mob.move_to(ORIGIN).shift(down * DOWN)

        # ===== SLIDE 1 =====
        self._ensure_logo(animate=True)

        p_footer = self._first_existing("/home/gustavo/SS/ImagesSQL_Slides/(Pie)_Portada_Aicraft.png"
        )
        p_aj = self._first_existing("/home/gustavo/SS/ImagesSQL_Slides/(Ajolote)_Portada_Aicraft.png"
        )

        title = self._write_block(TITLE_MAIN)
        footer = ImageMobject(p_footer) if p_footer else None
        aj     = ImageMobject(p_aj) if p_aj else None

        frame_w, frame_h = config.frame_width, config.frame_height
        left_pad   = 0.8
        right_pad  = 0.8
        gap_lr     = 1.0
        footer_hf  = 0.28   
        aj_hf      = 0.55   

        if footer:
            footer.set_height(footer_hf * frame_h)
            footer.to_edge(DOWN, buff=0)
            footer.set_width(frame_w)
            self._appear(footer, direction=UP, rt=0.6)

        if aj:
            max_h = (frame_h * (1.0 - footer_hf) - 0.6)
            aj.set_height(min(aj_hf * frame_h, max_h))
            if footer:
                aj.next_to(footer, UP, buff=0.25)
            else:
                aj.to_edge(DOWN, buff=1.0)
            aj.to_edge(RIGHT, buff=right_pad)
            self._appear(aj, direction=LEFT, rt=0.8)

        if aj:
            left_max_w = aj.get_left()[0] - (-frame_w/2 + left_pad) - gap_lr
        else:
            left_max_w = frame_w/2 - left_pad

        if left_max_w > 0 and title.width > left_max_w:
            title.scale(left_max_w / title.width)

        title.to_edge(LEFT, buff=left_pad)

        if footer:
            min_y = footer.get_top()[1] + 0.35
            dy = min_y - title.get_bottom()[1]
            if dy > 0:
                title.shift(UP * dy)

        if hasattr(self, "_logo"):
            top_limit = self._logo.get_bottom()[1] - 0.35
            if title.get_top()[1] > top_limit:
                title.shift(DOWN * (title.get_top()[1] - top_limit))

        self.play(Write(title, run_time=TITLE_IN_RT)); self.wait(0.2)

        if aj: self.bring_to_front(aj)
        if hasattr(self, "_logo"): self.bring_to_front(self._logo)

        self.wait(0.6)
        self._disappear(title, aj, footer)

        # ===== SLIDE 2 =====
        self._ensure_logo(); self._ensure_frame()

        s2 = self._write_block(r"\subsection*{\textcolor{myPurple}{Joins vs Set Operators}}")
        self.play(Write(s2, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s2)

        # ===== SLIDE 3  =====
        self._ensure_logo(); self._ensure_frame()

        t3_a = self._write_block(r"""
        Todo lo que se ha realizado hasta el momento se ha basado en una sola tabla, pero al trabajar en una base de datos se tiene que emplear más de una tabla u objeto, y como estamos trabajando con bases de datos relacionales esperaríamos tener mecanismos para generar conexiones entre tablas, o incluso entre resultados entre \textit{queries} que nos interesaría combinar.
        """)

        t3_b = self._write_block(r"""
        \textit{SQL} tiene varias herramientas para trabajar con múltiples tablas y todas ellas trabajan con los datos con una perspectiva de conjuntos; las principales son los \textit{joins} y los \textit{Operadores de conjuntos}. Cada una de estas dos categorías aborda el problema desde una perspectiva diferente respecto a cómo manejamos y combinamos tablas.
        """)

        g3a, g3b = t3_a.copy(), t3_b.copy()
        g3a.move_to(0.68*UP).set_x(0)
        g3b.next_to(g3a, DOWN, buff=0.55).set_x(0)
        self._fit_group_center(g3a, g3b, pad_x=1.0, pad_y=0.9)

        t3_a.scale(g3a.width/t3_a.width).move_to(g3a.get_center())
        t3_b.scale(g3b.width/t3_b.width).move_to(g3b.get_center())
        self.play(Write(t3_a, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        self.play(Write(t3_b, run_time=WRITE_MEDIUM_RT)); self.wait(0.6)
        self._disappear(t3_a, t3_b, rt=0.6)

        # ===== SLIDE 4a ( =====
        self._ensure_logo(); self._ensure_frame()

        t4a = self._write_block(r"""
        Con los \textit{joins} se trabaja las tablas de forma horizontal tomando como referencia sus registros, es decir, con un \textit{join} vamos a combinar las columnas de dos o más tablas usando los registros contenidos en una o más de sus columnas como criterio de combinación.
        """)
        g4a = t4a.copy().move_to(0.30*UP).set_x(0)
        if g4a.width > 0.86*config.frame_width:
            g4a.scale((0.86*config.frame_width)/g4a.width)
        t4a.scale(g4a.width/t4a.width).move_to(g4a.get_center())
        self.play(Write(t4a, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        self._disappear(t4a, rt=0.6)

        # ===== SLIDE 4b  =====
        self._ensure_logo(); self._ensure_frame()

        t4b = self._write_block(r"""
        Los \textit{joins} se pueden ver matemáticamente como un producto cartesiano, este está definido para dos conjuntos $A,B$ como:
        """)

        eq4 = self._write_block(r"""
        \[
        \textcolor{blue}{A} \times \textcolor{red}{B} = \{( \textcolor{blue}{a},\textcolor{red}{b}) \mid \textcolor{blue}{a} \in \textcolor{blue}{A} \; \land \; \textcolor{red}{b}\in \textcolor{red}{B}\}
        \]
        """)
        p_img4 = self._first_existing(
            "diagram-20251111.png",
            "ImagesSQL_Slides/diagram-20251111.png",
            "/home/gustavo/SS/ImagesSQL_Slides/diagram-20251111.png",
            "/mnt/data/diagram-20251111.png",
        )
        img4 = ImageMobject(p_img4) if p_img4 else None
        if img4:
            img4.set_width(0.70 * config.frame_width)
            max_h = 0.42 * config.frame_height
            if img4.height > max_h:
                img4.set_height(max_h)

        g4b, g4e = t4b.copy(), eq4.copy()
        g4b.move_to(0.68*UP).set_x(0)
        if g4b.width > 0.86*config.frame_width:
            g4b.scale((0.86*config.frame_width)/g4b.width)

        g4e.next_to(g4b, DOWN, buff=0.50).set_x(0)
        if g4e.width > 0.86*config.frame_width:
            g4e.scale((0.86*config.frame_width)/g4e.width)

        if img4:
            g4img = img4.copy().next_to(g4e, DOWN, buff=0.55).set_x(0)
            self._fit_group_center(g4b, g4e, g4img, pad_x=1.0, pad_y=0.9)
        else:
            self._fit_group_center(g4b, g4e, pad_x=1.0, pad_y=0.9)

        t4b.scale(g4b.width/t4b.width).move_to(g4b.get_center())
        eq4.scale(g4e.width/eq4.width).move_to(g4e.get_center())
        if img4:
            img4.scale(g4img.width/img4.width).move_to(g4img.get_center())

        self.play(Write(t4b, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        self.play(Write(eq4, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        if img4:
            self._appear(img4, direction=DOWN, rt=0.8); self.wait(0.6)

        self._disappear(t4b, eq4, img4 if img4 else None, rt=0.6)

        # ===== SLIDE 5  =====
        self._ensure_logo(); self._ensure_frame()

        t5 = self._write_block(r"""
        Esto, llevado a las bases de datos, es tomar dos tablas \texttt{R} y \texttt{S} y \texttt{R} \( \times \) \texttt{S} corresponde a todas las combinaciones posibles de las filas de \texttt{R} con las filas de \texttt{S}.
        """)

        p_img5 = self._first_existing(
            "TablaJOIN_Ejemplo.png",
            "ImagesSQL_Slides/TablaJOIN_Ejemplo.png",
            "/home/gustavo/SS/ImagesSQL_Slides/TablaJOIN_Ejemplo.png",
            "/mnt/data/TablaJOIN_Ejemplo.png",
        )

        g_t = t5.copy().move_to(0.68*UP).set_x(0)
        if g_t.width > 0.90 * config.frame_width:
            g_t.scale((0.90 * config.frame_width) / g_t.width)

        if p_img5:
            img5 = ImageMobject(p_img5)
            g_img = img5.copy()
            if g_img.width > 0.90 * config.frame_width:
                g_img.set_width(0.90 * config.frame_width)
            g_img.next_to(g_t, DOWN, buff=0.55).set_x(0)

            self._fit_group_center(g_t, g_img, pad_x=1.0, pad_y=0.9)

            t5.scale(g_t.width / t5.width).move_to(g_t.get_center())
            if img5.width != g_img.width:
                img5.scale(g_img.width / img5.width)
            img5.move_to(g_img.get_center())

            self.play(Write(t5, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
            self._appear(img5, direction=DOWN, rt=0.9); self.wait(0.6)
            self._disappear(t5, img5, rt=0.6)
        else:
            self._fit_group_center(g_t, pad_x=1.0, pad_y=0.9)
            t5.scale(g_t.width / t5.width).move_to(g_t.get_center())
            self.play(Write(t5, run_time=WRITE_MEDIUM_RT)); self.wait(0.6)
            self._disappear(t5, rt=0.6)

        # ===== SLIDE 6 =====
        self._ensure_logo(); self._ensure_frame()
        t6 = self._write_block(r"""
        \noindent\begin{minipage}{0.96\linewidth}
        Existen dos formas de especificar un \textit{join} en un comando \texttt{\textcolor{blue}{SELECT}}. La primera corresponde al estándar \textit{SQL-89} de la \textit{ANSI}, en la cual se establece que podemos poner tablas separadas por comas en la cláusula \texttt{\textcolor{blue}{FROM}} y a continuación usar \texttt{\textcolor{blue}{WHERE}} para establecer las condiciones de relación. El problema crucial aquí es que se pueden generar productos cartesianos de manera intencional, lo que puede llegar a consumir mucha memoria y tiempo.
        \end{minipage}

        \vskip 10pt
        \begin{center}
        \begin{minipage}{0.78\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,      % SELECT, FROM, WHERE
        commentstyle=\color{green!50!black},     % comentario en verde
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={[2]AND,OR,NOT}, emphstyle={[2]\color{gray}\bfseries}]
        -- JOIN Syntax: ANSI SQL-89
        SELECT <lista de selección>
        FROM Table1, Table2
        WHERE <condiciones>;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        self._fit_group_center(t6, pad_x=1.0, pad_y=0.9)
        self.play(Write(t6, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t6)

        # ===== SLIDE 7  =====
        self._ensure_logo(); self._ensure_frame()
        t7 = self._write_block(r"""
        \noindent\begin{minipage}{0.96\linewidth}
        Por otro lado el estándar \textit{ANSI SQL-92} establece que se puede modificar un operador \texttt{\textcolor{gray}{JOIN}} en la cláusula \texttt{\textcolor{blue}{FROM}} de forma explícita, junto con condiciones de coincidencia mediante \texttt{\textcolor{blue}{ON}}. Esta es la forma estándar de realizar cualquier \textit{join}. En este caso se usa como tal un operador que realiza el \textit{join} y se hace entre dos tablas a la vez; se especifican las columnas de cada tabla que se usarán como referencia y un operador lógico (como \texttt{'='} o \texttt{'<>'}) para comparar los valores.
        \end{minipage}

        \vskip 10pt
        \begin{center}
        \begin{minipage}{0.78\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,      % SELECT, FROM, WHERE
        commentstyle=\color{green!50!black},     % comentario en verde
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={[2]AND,OR,NOT}, emphstyle={[2]\color{gray}\bfseries}]
        -- JOIN Syntax: ANSI SQL-92
        SELECT <lista de selección>
        FROM Table1
        JOIN Table2
        ON <predicado on>;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        self._fit_group_center(t7, pad_x=1.0, pad_y=0.9)
        self.play(Write(t7, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t7)

        # ===== SLIDE 8 =====
        self._ensure_logo(); self._ensure_frame()
        t8 = self._write_block(r"""
        \noindent\begin{minipage}{0.96\linewidth}
        Por otra parte los \textit{Operadores de conjuntos} trabajan de forma vertical, tomando como referencia las columnas; estos se verán más adelante.
        \end{minipage}
        """)
        self._fit_group_center(t8, pad_x=1.0, pad_y=0.9)
        self.play(Write(t8, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t8)

        # ===== SLIDE 9  =====
        self._ensure_logo(); self._ensure_frame()
        s9 = self._write_block(r"\subsection*{\textcolor{myPurple}{\texttt{INNER JOIN}}}")
        self.play(Write(s9, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s9)

        # ===== SLIDE 10 =====
        self._ensure_logo(); self._ensure_frame()
        t10 = self._write_block(r"""
        \noindent\begin{minipage}{0.96\linewidth}
        El \texttt{\textcolor{gray}{INNER JOIN}} es el tipo de \textit{join} más común; de hecho, en la sintaxis se puede omitir la palabra \texttt{\textcolor{gray}{INNER}} y solo usar \texttt{\textcolor{gray}{JOIN}}, pues el comportamiento por defecto de todo \texttt{\textcolor{gray}{JOIN}} es realizar un \texttt{\textcolor{gray}{INNER JOIN}}. Con este tipo de \textit{join} se regresan solo los registros donde hay una coincidencia entre ambas tablas que se están operando.\\[0.6em]
        Para establecer las condiciones de coincidencia se usa el predicado \texttt{\textcolor{blue}{ON}}; se toman los registros donde ambas tablas cumplen la condición de este predicado, y esos son los que se regresan al final de la tabla.
        \end{minipage}
        """)
        self._fit_group_center(t10, pad_x=1.0, pad_y=0.9)
        self.play(Write(t10, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t10)

        # ===== SLIDE 11 =====
        self._ensure_logo(); self._ensure_frame()

        t11 = self._write_block(r"El diagrama de Venn correspondiente es el siguiente:")
        t11.scale(0.82)                 
        t11.to_edge(UP, buff=0.90)      

        img11 = ImageMobject("/home/gustavo/SS/ImagesSQL_Slides/VENN_INNER.png")
        img11.set_width(0.44 * config.frame_width)  
        img11.next_to(t11, DOWN, buff=0.55)          

        self.play(Write(t11, run_time=WRITE_MEDIUM_RT)); self.wait(0.1)
        self._appear(img11, direction=DOWN, rt=0.9); self.wait(1.5)
        self._disappear(t11, img11, rt=0.6)

        # ===== SLIDE 12 =====
        self._ensure_logo(); self._ensure_frame()

        t12 = self._write_block(r"""
        El uso de alias en los \textit{joins} permite identificar fácilmente las tablas involucradas y evitar ambigüedades cuando varias contienen columnas con el mismo nombre, ayudando a ser más específicos y prevenir errores. Además, los \texttt{\textcolor{blue}{INNER JOIN}} pueden emplearse como filtros, ya que devuelven solo los registros comunes entre tablas; por ejemplo, al analizar países con importaciones y exportaciones, el \texttt{\textcolor{blue}{INNER JOIN}} permite filtrar solo los que cumplen ambos criterios, lo que ilustra la utilidad de esta sintaxis del estándar \textit{ANSI SQL-89}.
        """)
        self._fit_group_center(t12, pad_x=1.0, pad_y=0.9)
        self.play(Write(t12, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t12)

        # ===== SLIDE 13 =====
        self._ensure_logo(); self._ensure_frame()

        t13 = self._write_block(r"""
        Por ejemplo el siguiente \textit{join} une las tablas \texttt{ProductDescription} y \texttt{ProductModelProductDescription} mediante la columna \texttt{ProductDescriptionID}. Como ambas tienen 762 registros sin duplicados, el resultado del cruce también debe tener 762 filas, indicando una relación 1 a 1; si el número fuera mayor, significaría que algún registro se está combinando más de una vez, lo cual no es deseado.
        \vskip 10pt
        \begin{center}
        \begin{minipage}{0.9\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          % SELECT, FROM, ON
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,       % evita desbordes
        emph={SalesLT.ProductDescription,SalesLT.ProductModelProductDescription},
        emphstyle=\color{magenta}\bfseries,          % tablas en magenta
        emph={[2]JOIN}, emphstyle={[2]\color{gray}\bfseries}] % JOIN en gris
        -- Relación 1 a 1 por ProductDescriptionID
        SELECT *
        FROM SalesLT.ProductDescription
        JOIN SalesLT.ProductModelProductDescription
        ON SalesLT.ProductDescription.ProductDescriptionID =
            SalesLT.ProductModelProductDescription.ProductDescriptionID;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        self._fit_group_center(t13, pad_x=1.0, pad_y=0.9)
        self.play(Write(t13, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t13)

        # ===== SLIDE 14  =====
        self._ensure_logo(); self._ensure_frame()
        p = Path("TablaResultadoINNER.png")
        if not p.exists():
            p = Path("ImagesSQL_Slides/TablaResultadoINNER.png")

        img = ImageMobject(str(p)).set_z_index(1)
        max_w = 0.89 * config.frame_width
        max_h = 0.70 * config.frame_height
        img.set_height(max_h)
        if img.width > max_w:
            img.set_width(max_w)

        cap = Tex(r"\texttt{Vista parcial}", tex_template=tex_template).scale(0.70)

        g = Group(img, cap).arrange(DOWN, buff=0.12)
        self._fit_group_center(g, pad_x=1.0, pad_y=0.9)
        self._appear(img, direction=DOWN, rt=0.9); self.wait(0.05)
        self.play(Write(cap, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)

        self._disappear(g, rt=0.6)

        # ===== SLIDE 15  =====
        self._ensure_logo(); self._ensure_frame()
        t15 = self._write_block(r"""
        El \textit{query} combina columnas de ambas tablas según el campo \texttt{ProductDescriptionID}, pero para evitar ambigüedades es necesario indicar de qué tabla proviene cada columna o usar alias. En algunos dialectos de \textit{SQL} puede omitirse el prefijo de tabla si las columnas tienen el mismo nombre, aunque esto no siempre es recomendable. Los alias simplifican el código y evitan errores al referirse a columnas repetidas entre tablas.
        """)

        c15 = self._write_block(r"""
        \begin{center}
        \begin{minipage}{0.95\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,            % SELECT, FROM, ON
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.ProductDescription,SalesLT.ProductModelProductDescription},
        emphstyle=\color{magenta}\bfseries,            % tablas en magenta
        emph={[2]JOIN}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}]
        SELECT PD.ProductDescriptionID, PMPD.ProductModelID,
            PMPD.Culture, PD.Description
        FROM SalesLT.ProductDescription AS PD
        JOIN SalesLT.ProductModelProductDescription AS PMPD
        ON PD.ProductDescriptionID = PMPD.ProductDescriptionID;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)

        gt, gc = t15.copy(), c15.copy()
        gt.move_to(0.65*UP).set_x(0)                       
        if gc.width > 0.86 * config.frame_width:           
            gc.scale((0.86 * config.frame_width)/gc.width)
        gc.next_to(gt, DOWN, buff=0.55).set_x(0)          

        self._fit_group_center(gt, gc, pad_x=1.0, pad_y=0.9)

        t15.scale(gt.width/t15.width).move_to(gt.get_center())
        c15.scale(gc.width/c15.width).move_to(gc.get_center())

        self.play(Write(t15, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        self.play(Write(c15, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)

        self._disappear(t15, c15, rt=0.6)

        # ===== SLIDE 16 =====
        self._ensure_logo(); self._ensure_frame()

        p_s16 = self._first_existing(
            "Tabla4_INNER.png",
            "ImagesSQL_Slides/Tabla4_INNER.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tabla4_INNER.png",
            "/mnt/data/Tabla4_INNER.png"
        )
        if p_s16:
            img16 = ImageMobject(p_s16).set_z_index(1)

            max_w = 0.84 * config.frame_width
            max_h = 0.58 * config.frame_height
            img16.set_height(max_h)
            if img16.width > max_w:
                img16.set_width(max_w)

            cap16 = Tex(r"\texttt{Vista parcial}", tex_template=tex_template).scale(0.70)

            block16 = Group(img16, cap16).arrange(DOWN, buff=0.12)
            self._fit_group_center(block16, pad_x=1.0, pad_y=0.9)

            self._appear(img16, direction=DOWN, rt=0.9); self.wait(0.05)
            self.play(Write(cap16, run_time=WRITE_MEDIUM_RT))
            self.wait(5.0)
            self._disappear(block16, rt=0.6)

        # ===== SLIDE 17  =====
        self._ensure_logo(); self._ensure_frame()

        t17 = self._write_block(r"""
        Y antes de que se seleccione las columnas que se desea, el resultado del \textit{join} funciona como una tabla virtual, y es posible realizar acciones sobre esta tabla y sus columnas (aun cuando no se hayan seleccionado en el \texttt{\textcolor{blue}{SELECT}} final), de la misma forma que se ha hecho previamente con cualquier tabla.
        """)

        c17 = self._write_block(r"""
        \begin{center}
        \begin{minipage}{0.95\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,              % SELECT, FROM, JOIN, ON, WHERE...
        stringstyle=\color{red},                         % 'en', 'fr'
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.ProductDescription,SalesLT.ProductModelProductDescription},
        emphstyle=\color{magenta}\bfseries,              % tablas en magenta
        emph={[2]AND,OR,NOT,IN}, emphstyle={[2]\color{gray}\bfseries}, % operadores lógicos en gris
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries},            % AS en azul
        emph={[4]UPPER,YEAR}, emphstyle={[4]\color{magenta}\bfseries}  % funciones en magenta
        ]
        SELECT PD.ProductDescriptionID, PMPD.ProductModelID,
            UPPER(PD.Description) AS Descripcion,
            YEAR(PD.ModifiedDate) AS MDYear
        FROM SalesLT.ProductDescription AS PD
        JOIN SalesLT.ProductModelProductDescription AS PMPD
        ON PD.ProductDescriptionID = PMPD.ProductDescriptionID
        WHERE PMPD.Culture IN ('en', 'fr');
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)

        gt, gc = t17.copy(), c17.copy()
        gt.move_to(0.65*UP).set_x(0)
        if gc.width > 0.86 * config.frame_width:
            gc.scale((0.86 * config.frame_width)/gc.width)
        gc.next_to(gt, DOWN, buff=0.55).set_x(0)

        self._fit_group_center(gt, gc, pad_x=1.0, pad_y=0.9)

        t17.scale(gt.width/t17.width).move_to(gt.get_center())
        c17.scale(gc.width/c17.width).move_to(gc.get_center())

        # Animación
        self.play(Write(t17, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        self.play(Write(c17, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(t17, c17, rt=0.6)


        # ===== SLIDE 18 =====
        self._ensure_logo(); self._ensure_frame()

        p_s18 = self._first_existing(
            "Tabla5_INNER.png",
            "ImagesSQL_Slides/Tabla5_INNER.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tabla5_INNER.png",
            "/mnt/data/Tabla5_INNER.png"
        )
        if p_s18:
            img18 = ImageMobject(p_s18).set_z_index(1)
            max_w = 0.84 * config.frame_width
            max_h = 0.58 * config.frame_height
            img18.set_height(max_h)
            if img18.width > max_w:
                img18.set_width(max_w)

            cap18 = Tex(r"\texttt{Vista parcial}", tex_template=tex_template).scale(0.70)
            block18 = Group(img18, cap18).arrange(DOWN, buff=0.12)
            self._fit_group_center(block18, pad_x=1.0, pad_y=0.9)

            self._appear(img18, direction=DOWN, rt=0.9); self.wait(0.05)
            self.play(Write(cap18, run_time=WRITE_MEDIUM_RT))
            self.wait(5.0)
            self._disappear(block18, rt=0.6)


        # ===== SLIDE 19  =====
        self._ensure_logo(); self._ensure_frame()

        t19 = self._write_block(r"""
        Como se puede observar, el filtro de \texttt{Culture} se ha aplicado sobre la tabla resultado del \textit{join}, no sobre alguna de las tablas individuales que se han usado. De cierta forma, \texttt{\textcolor{gray}{JOIN}} se vuelve una extensión de \texttt{\textcolor{blue}{FROM}}, y ahora la tabla que resulta de \texttt{\textcolor{gray}{JOIN}} es la que toma \texttt{\textcolor{blue}{FROM}}, y siguiendo el orden de las cláusulas de \textit{SQL} que se han aprendido, todas las demás clausulas se aplicarían sobre esta nueva tabla.
        """)
        self._fit_group_center(t19, pad_x=1.0, pad_y=0.9)
        self.play(Write(t19, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t19)


        # ===== SLIDE 20 =====
        self._ensure_logo(); self._ensure_frame()

        t20 = self._write_block(r"""
        Y se puede seguir construyendo la tabla usando mas \textit{joins}. La regla es que se deben de escribir los \textit{joins} de forma seguida, uno tras otro, pues como se ha comentado, se vuelve una extensión de \texttt{\textcolor{blue}{FROM}}.
        """)

        c20 = self._write_block(r"""
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,              % SELECT, FROM, JOIN, ON, WHERE, ORDER BY
        stringstyle=\color{red},                         % 'en', 'fr'
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.ProductDescription,SalesLT.ProductModelProductDescription,SalesLT.ProductModel},
        emphstyle=\color{magenta}\bfseries,              % tablas en magenta
        emph={[2]AND,OR,NOT,IN,IS}, emphstyle={[2]\color{gray}\bfseries}, % operadores en gris
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries},               % AS en azul
        emph={[4]UPPER,YEAR}, emphstyle={[4]\color{magenta}\bfseries}     % funciones en magenta
        ]
        SELECT PD.ProductDescriptionID, PMPD.ProductModelID,
            PM.Name, UPPER(PD.Description) AS Descripcion,
            YEAR(PD.ModifiedDate) AS MDYear, PM.CatalogDescription
        FROM SalesLT.ProductDescription AS PD
        JOIN SalesLT.ProductModelProductDescription AS PMPD
        ON PD.ProductDescriptionID = PMPD.ProductDescriptionID
        JOIN SalesLT.ProductModel AS PM
        ON PM.ProductModelID = PMPD.ProductModelID
        WHERE PMPD.Culture IN ('en', 'fr')
        AND PM.CatalogDescription IS NOT NULL
        ORDER BY PD.ProductDescriptionID;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)

        gt20, gc20 = t20.copy(), c20.copy()
        gt20.move_to(0.65*UP).set_x(0)
        if gc20.width > 0.86 * config.frame_width:
            gc20.scale((0.86 * config.frame_width)/gc20.width)
        gc20.next_to(gt20, DOWN, buff=0.55).set_x(0)

        self._fit_group_center(gt20, gc20, pad_x=1.0, pad_y=0.9)

        t20.scale(gt20.width/t20.width).move_to(gt20.get_center())
        c20.scale(gc20.width/c20.width).move_to(gc20.get_center())

        self.play(Write(t20, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        self.play(Write(c20, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(t20, c20, rt=0.6)

        # ===== SLIDE 21 =====
        self._ensure_logo(); self._ensure_frame()

        p_s21 = self._first_existing(
            "Tabla6_INNER.png",
            "ImagesSQL_Slides/Tabla6_INNER.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tabla6_INNER.png",
            "/mnt/data/Tabla6_INNER.png"
        )
        if p_s21:
            img21 = ImageMobject(p_s21).set_z_index(1)

            max_w = 0.84 * config.frame_width
            max_h = 0.58 * config.frame_height
            img21.set_height(max_h)
            if img21.width > max_w:
                img21.set_width(max_w)

            cap21 = Tex(r"\texttt{Vista completa}", tex_template=tex_template).scale(0.70)
            block21 = Group(img21, cap21).arrange(DOWN, buff=0.12)
            self._fit_group_center(block21, pad_x=1.0, pad_y=0.9)

            self._appear(img21, direction=DOWN, rt=0.9); self.wait(0.05)
            self.play(Write(cap21, run_time=WRITE_MEDIUM_RT))
            self.wait(5.0)
            self._disappear(block21, rt=0.6)


        # ===== SLIDE 22  =====
        self._ensure_logo(); self._ensure_frame()

        t22 = self._write_block(r"""
        En el \textit{query} anterior, primero se hace un \texttt{\textcolor{gray}{JOIN}} entre \texttt{ProductDescription }\\ y \texttt{ProductModelProductDescription} por \texttt{ProductDescriptionID}, luego otro \texttt{\textcolor{gray}{JOIN}}  con \texttt{ProductModel} por \texttt{ProductModelID}; la tabla resultante de estos dos \texttt{\textcolor{gray}{JOIN}}  es la que aparece en \texttt{\textcolor{blue}{FROM}} y sobre la que actúan \texttt{\textcolor{blue}{WHERE}}, \texttt{\textcolor{blue}{SELECT}} y \texttt{\textcolor{blue}{ORDER BY}}, y cuando se indica la tabla origen de las columnas en esas cláusulas es únicamente para evitar ambigüedades.
        """)
        self._fit_group_center(t22, pad_x=1.0, pad_y=0.9)
        self.play(Write(t22, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t22, rt=0.6)

        # ===== SLIDE 23  =====
        self._ensure_logo(); self._ensure_frame()

        t23 = self._write_block(r"""
        En el cruce, \texttt{ProductModel} tiene 128 registros con \texttt{ProductModelID} únicos, mientras que la tabla resultante del primer \texttt{\textcolor{blue}{JOIN}} tiene 762 filas y varios \texttt{ProductDescriptionID} comparten el mismo \texttt{ProductModelID}; al unirlas, cada fila de \texttt{ProductModel} se repite tantas veces como coincidencias tenga su \texttt{ProductModelID} en la primera tabla, de modo que en el resultado final aparecen varias filas con la misma información de \texttt{ProductModelID} y \texttt{Name}, lo que corresponde a un cruce $n$–$1$ (muchas filas de la primera tabla contra una de \texttt{ProductModel}), y si \texttt{ProductModel} también tuviera registros repetidos con el mismo \texttt{ProductModelID} el cruce pasaría a ser $n$–$n$.
        """)
        self._fit_group_center(t23, pad_x=1.0, pad_y=0.9)
        self.play(Write(t23, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t23, rt=0.6)


        # ===== SLIDE 24  =====
        self._ensure_logo(); self._ensure_frame()

        t24 = self._write_block(r"""
        Si unimos dos tablas de distinto tamaño usando columnas cuyos valores no se repiten, el tamaño máximo del resultado será el mínimo entre ambas tablas. Sin embargo, si alguna columna usada en el cruce contiene valores repetidos, pueden generarse registros duplicados y producir un resultado más grande que las tablas originales, lo cual no es un error siempre que sea el comportamiento esperado.
        """)
        self._fit_group_center(t24, pad_x=1.0, pad_y=0.9)
        self.play(Write(t24, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t24, rt=0.6)


        # ===== SLIDE 25  =====
        self._ensure_logo(); self._ensure_frame()

        t25 = self._write_block(r"""
        Por ello, aunque técnicamente podemos realizar un \textit{join} con cualquier columna compatible, se recomienda usar llaves primarias, llaves secundarias o identificadores únicos para minimizar duplicidades y evitar errores. Usar columnas con valores naturalmente repetidos, como nombres, aumenta la probabilidad de obtener cruces indeseados al aplicar el \textit{join}.
        """)
        self._fit_group_center(t25, pad_x=1.0, pad_y=0.9)
        self.play(Write(t25, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(t25, rt=0.6)


        # ===== SLIDE 26  =====
        self._ensure_logo(); self._ensure_frame()

        t26 = self._write_block(r"""
        También se puede usar más de una columna como referencia, y para esto se puede usar \texttt{\textcolor{gray}{AND}} y \texttt{\textcolor{gray}{OR}}. El primero regresará los cruces que cumplan ambas condiciones, y el segundo los cruces que cumplan al menos una de las condiciones. El siguiente \textbf{query} usa \texttt{ProductModelID} y \texttt{ModifiedDate} como columnas de referencia.
        """)

        c26 = self._write_block(r"""
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,      % SELECT, FROM, Name, etc.
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, breaklines=true, columns=fullflexible,
        emph={SalesLT.ProductModel,SalesLT.ProductModelProductDescription},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,AND}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]Name}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT B.ProductDescriptionID, A.Name, A.ModifiedDate
        FROM   SalesLT.ProductModel A
        JOIN   SalesLT.ProductModelProductDescription B
        ON   A.ProductModelID = B.ProductModelID
        AND  A.ModifiedDate   = B.ModifiedDate;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)

        gt26, gc26 = t26.copy(), c26.copy()
        gt26.move_to(0.65*UP).set_x(0)
        if gc26.width > 0.86 * config.frame_width:
            gc26.scale((0.86 * config.frame_width)/gc26.width)
        gc26.next_to(gt26, DOWN, buff=0.55).set_x(0)

        self._fit_group_center(gt26, gc26, pad_x=1.0, pad_y=0.9)

        t26.scale(gt26.width/t26.width).move_to(gt26.get_center())
        c26.scale(gc26.width/c26.width).move_to(gc26.get_center())

        self.play(Write(t26, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        self.play(Write(c26, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(t26, c26, rt=0.6)

        # ===== SLIDE 27  =====
        self._ensure_logo(); self._ensure_frame()

        p_s27 = self._first_existing(
            "Tabla11_INNER.png",
            "ImagesSQL_Slides/Tabla11_INNER.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tabla11_INNER.png",
            "/mnt/data/Tabla11_INNER.png"
        )
        if p_s27:
            img27 = ImageMobject(p_s27).set_z_index(1)

            max_w = 0.84 * config.frame_width
            max_h = 0.58 * config.frame_height
            img27.set_height(max_h)
            if img27.width > max_w:
                img27.set_width(max_w)

            cap27 = Tex(r"\texttt{Vista parcial}", tex_template=tex_template).scale(0.70)
            block27 = Group(img27, cap27).arrange(DOWN, buff=0.12)
            self._fit_group_center(block27, pad_x=1.0, pad_y=0.9)

            self._appear(img27, direction=DOWN, rt=0.9); self.wait(0.05)
            self.play(Write(cap27, run_time=WRITE_MEDIUM_RT))
            self.wait(5.0)
            self._disappear(block27, rt=0.6)


        # ===== SLIDE 28 =====
        self._ensure_logo(); self._ensure_frame()

        t28 = self._write_block(r"""
        Además del operador \texttt{=}, los \textit{joins} pueden utilizar otros operadores y combinar condiciones mediante \texttt{\textcolor{gray}{AND}} para construir expresiones más complejas en \texttt{\textcolor{blue}{ON}}. Un ejemplo de ello es un \textit{join} que devuelve los \texttt{SalesOrderDetailID} donde el producto registrado en la orden aparece también en la tabla de productos y cuyo \texttt{UnitPrice} es menor que la mitad del \texttt{ListPrice}. Este \textit{query} produce 19 registros.
        """)

        c28 = self._write_block(r"""
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, breaklines=true, columns=fullflexible,
        emph={SalesLT.SalesOrderDetail,SalesLT.Product},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,AND}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT SOD.SalesOrderDetailID, SOD.ProductID,
            SOD.UnitPrice, P.ListPrice
        FROM   SalesLT.SalesOrderDetail AS SOD
        JOIN   SalesLT.Product AS P
        ON   SOD.ProductID = P.ProductID
        AND   SOD.UnitPrice <  P.ListPrice;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)

        gt28, gc28 = t28.copy(), c28.copy()
        gt28.move_to(0.65*UP).set_x(0)
        if gc28.width > 0.86 * config.frame_width:
            gc28.scale((0.86 * config.frame_width)/gc28.width)
        gc28.next_to(gt28, DOWN, buff=0.55).set_x(0)

        self._fit_group_center(gt28, gc28, pad_x=1.0, pad_y=0.9)

        t28.scale(gt28.width/t28.width).move_to(gt28.get_center())
        c28.scale(gc28.width/c28.width).move_to(gc28.get_center())

        self.play(Write(t28, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        self.play(Write(c28, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(t28, c28, rt=0.6)


        # ===== SLIDE 29 =====
        self._ensure_logo(); self._ensure_frame()

        p_s29 = self._first_existing(
            "Tabla12_INNER.png",
            "ImagesSQL_Slides/Tabla12_INNER.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tabla12_INNER.png",
            "/mnt/data/Tabla12_INNER.png"
        )
        if p_s29:
            img29 = ImageMobject(p_s29).set_z_index(1)

            max_w = 0.84 * config.frame_width
            max_h = 0.58 * config.frame_height
            img29.set_height(max_h)
            if img29.width > max_w:
                img29.set_width(max_w)

            cap29 = Tex(r"\texttt{Vista parcial}", tex_template=tex_template).scale(0.70)
            block29 = Group(img29, cap29).arrange(DOWN, buff=0.12)
            self._fit_group_center(block29, pad_x=1.0, pad_y=0.9)

            self._appear(img29, direction=DOWN, rt=0.9); self.wait(0.05)
            self.play(Write(cap29, run_time=WRITE_MEDIUM_RT))
            self.wait(5.0)
            self._disappear(block29, rt=0.6)

        # ===== SLIDE 30  =====
        self._ensure_logo(); self._ensure_frame()

        t30 = self._write_block(r"""
        Agregando ahora la condición de que el precio unitario no solo pueda ser menor que la mitad, sino que los resultados también incluyan a aquellos registros donde el precio unitario es menor que el precio de lista menos 100, se tiene lo siguiente, ahora con 282 registros en los resultados:
        """)

        c30 = self._write_block(r"""
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, breaklines=true, columns=fullflexible,
        % --- Palabras que deben ir en magenta (con negritas)
        emph={SalesLT.Product,SalesLT.SalesOrderDetail,Product},
        emphstyle=\color{magenta}\bfseries,
        % --- JOIN, ON, AND, OR en gris
        emph={[2]JOIN,ON,AND,OR}, emphstyle={[2]\color{gray}\bfseries},
        % --- AS en azul
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT SOD.SalesOrderDetailID, SOD.ProductID,
            SOD.UnitPrice, P.ListPrice
        FROM   SalesLT.SalesOrderDetail AS SOD
        JOIN   SalesLT.Product AS P
        ON   SOD.ProductID = P.ProductID AND
            (SOD.UnitPrice < P.ListPrice / 2 OR 
                SOD.UnitPrice < P.ListPrice - 100);
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)

        gt30, gc30 = t30.copy(), c30.copy()
        gt30.move_to(0.66*UP).set_x(0)
        if gc30.width > 0.86 * config.frame_width:
            gc30.scale((0.86 * config.frame_width)/gc30.width)
        gc30.next_to(gt30, DOWN, buff=0.55).set_x(0)

        self._fit_group_center(gt30, gc30, pad_x=1.0, pad_y=0.9)
        t30.scale(gt30.width/t30.width).move_to(gt30.get_center())
        c30.scale(gc30.width/c30.width).move_to(gc30.get_center())

        self.play(Write(t30, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        self.play(Write(c30, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(t30, c30, rt=0.6)


        # ===== SLIDE 31  =====
        self._ensure_logo(); self._ensure_frame()

        p_s31 = self._first_existing(
            "Tabla13_INNER.png",
            "ImagesSQL_Slides/Tabla13_INNER.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tabla13_INNER.png",
            "/mnt/data/Tabla13_INNER.png"
        )
        if p_s31:
            img31 = ImageMobject(p_s31).set_z_index(1)
            max_w = 0.84 * config.frame_width
            max_h = 0.58 * config.frame_height
            img31.set_height(max_h)
            if img31.width > max_w:
                img31.set_width(max_w)

            cap31 = Tex(r"\texttt{Vista parcial}", tex_template=tex_template).scale(0.70)
            block31 = Group(img31, cap31).arrange(DOWN, buff=0.12)
            self._fit_group_center(block31, pad_x=1.0, pad_y=0.9)

            self._appear(img31, direction=DOWN, rt=0.9); self.wait(0.05)
            self.play(Write(cap31, run_time=WRITE_MEDIUM_RT))
            self.wait(5.0)
            self._disappear(block31, rt=0.6)


        # ===== SLIDE 32  =====
        self._ensure_logo(); self._ensure_frame()

        t32 = self._write_block(r"""
        Note que el resultado es distinto si corremos el siguiente \textit{query}, el cual regresa 80,593 registros:
        """)

        c32 = self._write_block(r"""
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, breaklines=true, columns=fullflexible,
        emph={SalesLT.SalesOrderDetail,SalesLT.PRODUCT,PRODUCT},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,ON,AND,OR}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT SOD.SalesOrderDetailID, SOD.ProductID,
            SOD.UnitPrice, P.ListPrice
        FROM   SalesLT.SalesOrderDetail AS SOD
        JOIN   SalesLT.PRODUCT AS P
        ON   SOD.ProductID = P.ProductID AND
            SOD.UnitPrice < P.ListPrice/2 OR
            SOD.UnitPrice < P.ListPrice-100;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)

        gt32, gc32 = t32.copy(), c32.copy()
        gt32.move_to(0.66*UP).set_x(0)
        if gc32.width > 0.86 * config.frame_width:
            gc32.scale((0.86 * config.frame_width)/gc32.width)
        gc32.next_to(gt32, DOWN, buff=0.55).set_x(0)

        self._fit_group_center(gt32, gc32, pad_x=1.0, pad_y=0.9)
        t32.scale(gt32.width/t32.width).move_to(gt32.get_center())
        c32.scale(gc32.width/c32.width).move_to(gc32.get_center())

        self.play(Write(t32, run_time=WRITE_MEDIUM_RT)); self.wait(0.05)
        self.play(Write(c32, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(t32, c32, rt=0.6)


        # ===== SLIDE 33  =====
        self._ensure_logo(); self._ensure_frame()

        t33 = self._write_block(r"""
        La diferencia entre ambos \textit{queries} radica en la condición escrita en \texttt{\textcolor{blue}{ON}}. En el primero, se exige que el \texttt{ID} sea igual y que el \texttt{UnitPrice} cumpla simultáneamente dos restricciones, por lo que ambas deben ser verdaderas para que el registro aparezca. En el segundo, se combinan condiciones con \texttt{\textcolor{blue}{OR}}, permitiendo que un registro sea válido si cumple cualquiera de ellas; así, incluso cuando los \texttt{ID} no coinciden, el registro puede incluirse si satisface la condición del precio. El uso de paréntesis en el primer \textit{query} fuerza la evaluación conjunta de sus condiciones, mientras que en el segundo ambas expresiones del \texttt{\textcolor{blue}{OR}} tienen el mismo peso.
        """)

        if t33.width > 0.86 * config.frame_width:
            t33.scale((0.86 * config.frame_width)/t33.width)
        self._fit_group_center(t33, pad_x=1.0, pad_y=0.9)

        self.play(Write(t33, run_time=WRITE_MEDIUM_RT))
        self.wait(3.0)
        self._disappear(t33, rt=0.6)

        # ===== SLIDE 34  =====
        self._ensure_logo(); self._ensure_frame()

        t34 = self._write_block(r"""
        La selección de condiciones en \texttt{\textcolor{blue}{ON}} depende del resultado deseado, y puede entenderse como un mecanismo de filtrado donde se emplean valores de una tabla para filtrar otra. Los \textit{joins} que usan operadores de comparación distintos a la igualdad se denominan \textit{theta-joins}, y cuando utilizan exclusivamente el operador \texttt{=} reciben el nombre de \textit{equi-joins}. Si ambas tablas comparten una columna con el mismo nombre y dicha columna se emplea en el cruce, entonces se obtiene un \textit{join} natural, aunque estas denominaciones no son muy comunes en la práctica.
        """)

        if t34.width > 0.86 * config.frame_width:
            t34.scale((0.86 * config.frame_width)/t34.width)
        self._fit_group_center(t34, pad_x=1.0, pad_y=0.9)

        self.play(Write(t34, run_time=WRITE_MEDIUM_RT))
        self.wait(3.0)
        self._disappear(t34, rt=0.6)

        # ===== SLIDE 35 =====
        self._ensure_logo(); self._ensure_frame()
        s35 = self._write_block(r"\subsection*{\textcolor{myPurple}{\texttt{OUTER JOIN (RIGHT, LEFT, FULL JOIN)}}}")
        self.play(Write(s35, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s35)

        # ===== SLIDE 36 =====
        self._ensure_logo(); self._ensure_frame()
        s36 = self._write_block(r"""
        A diferencia del \texttt{\textcolor{gray}{INNER JOIN}} donde se regresa solo los registros que tuvieran una coincidencia entre una tabla \texttt{A} y \texttt{B}, con un \texttt{\textcolor{gray}{OUTER JOIN}} también se revisa la coincidencia entre \texttt{A} y \texttt{B} \textbf{pero} se conservan los registros de la tabla \texttt{A} y se agregan los registros de la tabla \texttt{B} que tengan la misma coincidencia buscada.
        \vskip 10pt
        Los registros donde no se haya encontrado la coincidencia se rellenarán con \texttt{\textcolor{gray}{NULL}}.\\
        Internamente, al realizar un \texttt{\textcolor{gray}{OUTER JOIN}}, \textit{SQL} crea un producto cartesiano y preserva todos los registros de la tabla de referencia, y filtra todos los registros que no se encuentran en la intersección.
        """)
        s36.scale(0.86 * config.frame_width / s36.width); self._fit_group_center(s36, pad_x=1.0, pad_y=0.9)
        self.play(Write(s36, run_time=WRITE_MEDIUM_RT)); self.wait(0.6); self._disappear(s36)

        # ===== SLIDE 37 =====
        self._ensure_logo(); self._ensure_frame()
        s37 = self._write_block(r"""
        Existen tres tipos de \texttt{\textcolor{gray}{OUTER JOIN}}: \texttt{\textcolor{gray}{LEFT OUTER JOIN}}, \texttt{\textcolor{gray}{RIGHT OUTER JOIN}}, y \texttt{\textcolor{gray}{FULL OUTER JOIN}}. La diferencia entre estos tres subtipos de \textit{joins} reside en la importancia a las tablas según el orden en que se especifican.
        """)
        s37.scale(0.86 * config.frame_width / s37.width); self._fit_group_center(s37, pad_x=1.0, pad_y=0.9)
        self.play(Write(s37, run_time=WRITE_MEDIUM_RT)); self.wait(0.6); self._disappear(s37)

        # ===== SLIDE 38 =====
        self._ensure_logo(); self._ensure_frame()
        p38 = self._first_existing("ImagesSQL_Slides/VENN__LEFT_INNER.png","/home/gustavo/SS/ImagesSQL_Slides/VENN__LEFT_INNER.png","/mnt/data/VENN__LEFT_INNER.png")
        if p38:
            img38 = ImageMobject(p38).set_width(0.60 * config.frame_width).move_to(ORIGIN).shift(0.05*DOWN)
            g38 = Group(img38)
            self.play(FadeIn(g38, shift=DOWN, run_time=0.9)); self.wait(5.0); self._disappear(g38, rt=0.6)

        # ===== SLIDE 39 =====
        self._ensure_logo(); self._ensure_frame()
        s39 = self._write_block(r"""
        Un \texttt{\textcolor{gray}{LEFT OUTER JOIN}} preserva siempre las filas de la tabla escrita a la izquierda y solo toma de la tabla derecha las que cumplan la condición del \texttt{\textcolor{blue}{ON}}, rellenando con \texttt{\textcolor{gray}{NULL}} cuando no haya coincidencia; un \texttt{\textcolor{gray}{RIGHT OUTER JOIN}} hace lo mismo pero preservando las filas de la tabla derecha. La palabra \texttt{\textcolor{gray}{OUTER}} es opcional y el orden izquierda/derecha lo determina el orden en que aparecen las tablas en el \textit{query}, no el orden dentro del \texttt{\textcolor{blue}{ON}}. Además, si se comienza a usar \texttt{\textcolor{gray}{LEFT}} o \texttt{\textcolor{gray}{RIGHT OUTER JOIN}} en una cadena de \textit{joins}, debe mantenerse el mismo tipo para no mezclar criterios.
        """)
        s39.scale(0.86 * config.frame_width / s39.width); self._fit_group_center(s39, pad_x=1.0, pad_y=0.9)
        self.play(Write(s39, run_time=WRITE_MEDIUM_RT)); self.wait(0.6); self._disappear(s39)

        # ===== SLIDE 40  =====
        self._ensure_logo(); self._ensure_frame()
        p40 = self._first_existing("ImagesSQL_Slides/VENN__RIGHT_INNER.png","/home/gustavo/SS/ImagesSQL_Slides/VENN__RIGHT_INNER.png","/mnt/data/VENN__RIGHT_INNER.png")
        if p40:
            img40 = ImageMobject(p40).set_width(0.60 * config.frame_width).move_to(ORIGIN).shift(0.05*DOWN)
            g40 = Group(img40)
            self.play(FadeIn(g40, shift=DOWN, run_time=0.9)); self.wait(5.0); self._disappear(g40, rt=0.6)

        # ===== SLIDE 41 =====
        self._ensure_logo(); self._ensure_frame()
        s41 = self._write_block(r"""
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.Customer,SalesLT.CustomerAddress}, 
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,LEFT}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}
        ]
        -- Ejemplo usando LEFT JOIN
        SELECT  C.CustomerID, C.CompanyName,  
                CA.CustomerID, CA.AddressType
        FROM    SalesLT.Customer AS C
        LEFT JOIN SalesLT.CustomerAddress AS CA
        ON    C.CustomerID = CA.CustomerID
        ORDER BY C.CompanyName;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s41.scale(0.86 * config.frame_width / s41.width); self._fit_group_center(s41, pad_x=1.0, pad_y=0.9)
        self.play(Write(s41, run_time=WRITE_MEDIUM_RT)); self.wait(3.0); self._disappear(s41, rt=0.6)

        # ===== SLIDE 42 =====
        self._ensure_logo(); self._ensure_frame()
        p42 = self._first_existing("ImagesSQL_Slides/Tabla1_OUTER.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla1_OUTER.png","/mnt/data/Tabla1_OUTER.png")
        if p42:
            img42 = ImageMobject(p42).set_width(0.50 * config.frame_width)
            cap42 = self._write_block(r"\texttt{Vista parcial}"); cap42.next_to(img42, DOWN, buff=0.12)
            g42 = Group(img42, cap42).move_to(ORIGIN).shift(0.05*DOWN)
            self.play(FadeIn(g42, shift=DOWN, run_time=0.9)); self.wait(5.0); self._disappear(g42, rt=0.6)

        # ===== SLIDE 43 =====
        self._ensure_logo(); self._ensure_frame()
        s43 = self._write_block(r"""
        En el \textit{query} anterior, el \texttt{\textcolor{gray}{LEFT JOIN}} entre las tablas \texttt{Customer} y \texttt{CustomerAddress} produce registros con \texttt{\textcolor{gray}{NULL}} porque ambas tablas no contienen los mismos valores de \texttt{CustomerID}. La tabla \texttt{Customer} tiene 847 filas y \texttt{CustomerAddress} tiene 417, por lo que muchos clientes no tienen dirección asociada y esos registros aparecen con \texttt{\textcolor{gray}{NULL}} después del \texttt{\textcolor{gray}{LEFT JOIN}}. Además, el resultado muestra 857 filas, lo que indica que la condición del \texttt{\textcolor{blue}{ON}} se cumplió más de una vez para ciertos \texttt{CustomerID}, generando duplicados porque algunos valores aparecen varias veces en \texttt{CustomerAddress} o en \texttt{Customer}. El \texttt{\textcolor{gray}{LEFT JOIN}} conserva todas las filas de \texttt{Customer} y solo agrega las coincidencias válidas; cuando no existe coincidencia, se rellenan los campos con \texttt{\textcolor{gray}{NULL}}.
        """)
        s43.scale(0.86 * config.frame_width / s43.width); self._fit_group_center(s43, pad_x=1.0, pad_y=0.9)
        self.play(Write(s43, run_time=WRITE_MEDIUM_RT)); self.wait(0.8); self._disappear(s43, rt=0.6)

        # ===== SLIDE 44 =====
        self._ensure_logo(); self._ensure_frame()
        s44 = self._write_block(r"""
        \noindent Usando \texttt{\textcolor{gray}{RIGHT}}:
        \vskip 10pt
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.Customer,SalesLT.CustomerAddress},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,LEFT,RIGHT}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT  C.CustomerID,  C.CompanyName,  CA.CustomerID, CA.AddressType
        FROM    SalesLT.Customer AS C
        RIGHT JOIN SalesLT.CustomerAddress AS CA
        ON    CA.CustomerID = C.CustomerID
        ORDER BY C.CompanyName;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s44.scale(0.86 * config.frame_width / s44.width); self._fit_group_center(s44, pad_x=1.0, pad_y=0.9)
        self.play(Write(s44, run_time=WRITE_MEDIUM_RT)); self.wait(3.0); self._disappear(s44, rt=0.6)

        # ===== SLIDE 45  =====
        self._ensure_logo(); self._ensure_frame()
        p45 = self._first_existing("ImagesSQL_Slides/Tabla2_OUTER.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla2_OUTER.png","/mnt/data/Tabla2_OUTER.png")
        if p45:
            img45 = ImageMobject(p45).set_width(0.50 * config.frame_width)
            cap45 = self._write_block(r"\texttt{Vista parcial}"); cap45.next_to(img45, DOWN, buff=0.12)
            g45 = Group(img45, cap45).move_to(ORIGIN).shift(0.05*DOWN)
            self.play(FadeIn(g45, shift=DOWN, run_time=0.9)); self.wait(5.0); self._disappear(g45, rt=0.6)

        # ===== SLIDE 46 =====
        self._ensure_logo(); self._ensure_frame()
        s46 = self._write_block(r"""
        En este \texttt{\textcolor{gray}{RIGHT JOIN}} el resultado contiene 417 filas, exactamente el mismo número que \texttt{CustomerAddress}, porque al usar \texttt{\textcolor{gray}{RIGHT}} siempre se preservan los registros de la tabla que aparece a la derecha. No hay incremento en filas porque \texttt{Customer} tiene valores únicos de \texttt{CustomerID}, de modo que desde la perspectiva de la tabla derecha no pueden generarse combinaciones adicionales. Además, como \texttt{CustomerAddress} es la tabla con menos registros, no aparecen \texttt{\textcolor{gray}{NULL}}: todos sus \texttt{CustomerID} encuentran coincidencia dentro de \texttt{Customer}.
        """)
        s46.scale(0.86 * config.frame_width / s46.width); self._fit_group_center(s46, pad_x=1.0, pad_y=0.9)
        self.play(Write(s46, run_time=WRITE_MEDIUM_RT)); self.wait(0.8); self._disappear(s46, rt=0.6)

        # ===== SLIDE 47  =====
        self._ensure_logo(); self._ensure_frame()
        s47 = self._write_block(r"""
        Si hubiera valores sin correspondencia, esos campos se rellenarían con \texttt{\textcolor{gray}{NULL}} en las columnas de \texttt{Customer}. En esencia, el \texttt{\textcolor{gray}{RIGHT JOIN}} respeta todos los registros de la tabla derecha, igual que un \texttt{\textcolor{gray}{LEFT JOIN}} respeta los de la izquierda; y si quisiéramos replicar con \texttt{\textcolor{gray}{RIGHT}} el mismo resultado que antes obtuvimos con \texttt{\textcolor{gray}{LEFT}}, bastaría con poner \texttt{Customer} como la tabla que aparece después del \texttt{\textcolor{gray}{RIGHT JOIN}}.
        \vskip 10pt
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.Customer,SalesLT.CustomerAddress},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]RIGHT,JOIN}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT  C.CustomerID,  C.CompanyName,  CA.CustomerID, CA.AddressType
        FROM    SalesLT.CustomerAddress AS CA
        RIGHT JOIN SalesLT.Customer AS C
            ON  C.CustomerID = CA.CustomerID
        ORDER BY C.CompanyName;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s47.scale(0.86 * config.frame_width / s47.width); self._fit_group_center(s47, pad_x=1.0, pad_y=0.9)
        self.play(Write(s47, run_time=WRITE_MEDIUM_RT)); self.wait(3.0); self._disappear(s47, rt=0.6)

        # ===== SLIDE 48 =====
        self._ensure_logo(); self._ensure_frame()
        p48 = self._first_existing("ImagesSQL_Slides/Tabla3_OUTER.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla3_OUTER.png","/mnt/data/Tabla3_OUTER.png")
        if p48:
            img48 = ImageMobject(p48).set_width(0.50 * config.frame_width)
            cap48 = self._write_block(r"\texttt{Vista parcial}"); cap48.next_to(img48, DOWN, buff=0.12)
            g48 = Group(img48, cap48).move_to(ORIGIN).shift(0.05*DOWN)
            self.play(FadeIn(g48, shift=DOWN, run_time=0.9)); self.wait(5.0); self._disappear(g48, rt=0.6)

        # ===== SLIDE 49 =====
        self._ensure_logo(); self._ensure_frame()
        s49 = self._write_block(r"""
        Supuóngase que nos interesa obtener en los resultados finales el \texttt{Customer ID}, el nombre completo, el nombre de la compañía, el teléfono, y la dirección completa (incluyendo ciudad, estado, país, y código postal).
        \vskip 10pt
        Esta información requerida se encuentra distribuida entre \texttt{Customer} y \texttt{Address}, pero estas tablas no pueden unirse directamente porque \texttt{Address} no contiene la llave primaria de \texttt{Customer} (\texttt{CustomerID}) ni \texttt{Customer} contiene la llave primaria de \texttt{Address} (\texttt{AddressID}). Si \texttt{CustomerID} estuviera en \texttt{Address} sería una llave foránea, pero no es el caso, así que no es posible realizar un \texttt{\textcolor{gray}{JOIN}} directo entre ambas tablas.
        \vskip 5pt
        Esto se puede ver en el siguiente extracto del gráfico de entidad relación.
        """)
        s49.scale(0.86 * config.frame_width / s49.width); self._fit_group_center(s49, pad_x=1.0, pad_y=0.9)
        self.play(Write(s49, run_time=WRITE_MEDIUM_RT)); self.wait(0.8); self._disappear(s49, rt=0.6)

        # ===== SLIDE 50 =====
        self._ensure_logo(); self._ensure_frame()
        p50 = self._first_existing("ImagesSQL_Slides/DiagramaTablas_OUTER.png","/home/gustavo/SS/ImagesSQL_Slides/DiagramaTablas_OUTER.png","/mnt/data/DiagramaTablas_OUTER.png")
        if p50:
            img50 = ImageMobject(p50).set_width(0.66 * config.frame_width).move_to(ORIGIN).shift(0.05*DOWN)
            g50 = Group(img50)
            self.play(FadeIn(g50, shift=DOWN, run_time=0.9)); self.wait(5.0); self._disappear(g50, rt=0.6)

        # ===== SLIDE 51  =====
        self._ensure_logo(); self._ensure_frame()
        s51 = self._write_block(r"""
        Sin embargo, \texttt{CustomerAddress} contiene ambas llaves primarias, es decir, la tabla \texttt{CustomerAddress} relaciona a la tabla \texttt{Customer} con la tabla \texttt{Address}, así que lo que se hará será usar \texttt{CustomerAddress} como intermediaria o puente entre estas dos tablas.
        \vskip 5pt
        Se requiere realizar dos \textit{joins}, uno que cruce a \texttt{Customer} con \texttt{CustomerAddress} y otro que cruce el resultado de este \textit{join} con la tabla \texttt{Address}, el siguiente diagrama sirve para dar una idea de lo que se quiere realizar, visto como pasos:
        """)
        s51.scale(0.86 * config.frame_width / s51.width); self._fit_group_center(s51, pad_x=1.0, pad_y=0.9)
        self.play(Write(s51, run_time=WRITE_MEDIUM_RT)); self.wait(0.8); self._disappear(s51, rt=0.6)

        # ===== SLIDE 52 =====
        self._ensure_logo(); self._ensure_frame()
        p52 = self._first_existing("ImagesSQL_Slides/DiagramaTablas2_OUTER.png","/home/gustavo/SS/ImagesSQL_Slides/DiagramaTablas2_OUTER.png","/mnt/data/DiagramaTablas2_OUTER.png")
        if p52:
            img52 = ImageMobject(p52).set_width(0.5 * config.frame_width).move_to(ORIGIN).shift(0.05*DOWN)
            g52 = Group(img52)
            self.play(FadeIn(g52, shift=DOWN, run_time=0.9)); self.wait(5.0); self._disappear(g52, rt=0.6)

        # ===== SLIDE 53 =====
        self._ensure_logo(); self._ensure_frame()
        s53 = self._write_block(r"""
        El proceso consiste en unir primero \texttt{Customer} con \texttt{CustomerAddress} usando \texttt{\textcolor{gray}{JOIN}} mediante la columna \texttt{CustomerID}, obteniendo una tabla intermedia que contiene columnas de ambas tablas. Como esta tabla ya incluye \texttt{AddressID}, podemos realizar un segundo \texttt{\textcolor{gray}{JOIN}} con \texttt{Address} para incorporar sus columnas. En el \texttt{\textcolor{blue}{SELECT}} final solo usaremos columnas de \texttt{Customer} y \texttt{Address}, pues \texttt{CustomerAddress} sirve únicamente como tabla puente.
        """)
        s53.scale(0.86 * config.frame_width / s53.width); self._fit_group_center(s53, pad_x=1.0, pad_y=0.9)
        self.play(Write(s53, run_time=WRITE_MEDIUM_RT)); self.wait(0.8); self._disappear(s53, rt=0.6)

        # ===== SLIDE 54 =====
        self._ensure_logo(); self._ensure_frame()
        s54 = self._write_block(r"""
        Una vez identificadas las columnas de cruce, debemos elegir el tipo de unión: un \texttt{\textcolor{gray}{INNER JOIN}} conservará únicamente los registros donde la condición se cumpla en ambas tablas, mientras que un \texttt{\textcolor{gray}{OUTER JOIN}} permite preservar los registros de una tabla específica aunque no exista coincidencia. Para el primer resultado usaremos dos \texttt{\textcolor{gray}{INNER JOIN}} para obtener únicamente los registros donde \texttt{CustomerID} coincida en las tres tablas.
        \vskip 10pt
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT *
        FROM SalesLT.Customer AS C
        JOIN SalesLT.CustomerAddress AS CA
        ON C.CustomerID = CA.CustomerID
        JOIN SalesLT.Address AS A
        ON CA.AddressID = A.AddressID;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s54.scale(0.86 * config.frame_width / s54.width); self._fit_group_center(s54, pad_x=1.0, pad_y=0.9)
        self.play(Write(s54, run_time=WRITE_MEDIUM_RT)); self.wait(3.0); self._disappear(s54, rt=0.6)

        # ===== SLIDE 55 =====
        self._ensure_logo(); self._ensure_frame()
        s55 = self._write_block(r"""
        El \textit{query} une las columnas de \texttt{Customer}, \texttt{CustomerAddress} y \texttt{Address} usando dos \texttt{\textcolor{gray}{INNER JOIN}}, lo cual garantiza que solo se conserven los registros que cumplen la condición especificada en \texttt{\textcolor{blue}{ON}}. Como los \texttt{CustomerID} y los \texttt{AddressID} son únicos, el resultado debe contener un número de filas igual al mínimo entre las tres tablas, que en este caso es \texttt{CustomerAddress} con 417 registros.
        \vskip 5PT
        Después del cruce, obtenemos todas las columnas involucradas, y solo queda derivar los datos solicitados para cada \texttt{CustomerID}: nombre completo, compañía, teléfono y dirección completa. Para ello debemos realizar las concatenaciones necesarias, utilizando los separadores adecuados según corresponda.
        \vskip 10pt
        Véase el siguiente extracto:
        """)
        s55.scale(0.86 * config.frame_width / s55.width); self._fit_group_center(s55, pad_x=1.0, pad_y=0.9)
        self.play(Write(s55, run_time=WRITE_MEDIUM_RT)); self.wait(0.8); self._disappear(s55, rt=0.6)

        # ===== SLIDE 56 =====
        self._ensure_logo(); self._ensure_frame()
        p56 = self._first_existing("ImagesSQL_Slides/DiagramaTablas3_OUTER.png","/home/gustavo/SS/ImagesSQL_Slides/DiagramaTablas3_OUTER.png","/mnt/data/DiagramaTablas3_OUTER.png")
        if p56:
            img56 = ImageMobject(p56).set_width(0.35 * config.frame_width).move_to(ORIGIN).shift(0.05*DOWN)
            g56 = Group(img56)
            self.play(FadeIn(g56, shift=DOWN, run_time=0.9)); self.wait(3.0); self._disappear(g56, rt=0.6)

        # ===== SLIDE 57 =====
        self._ensure_logo(); self._ensure_frame()
        s57 = self._write_block(r"""
        En el extracto anterior se muestra la información del contenido de las tablas \texttt{Address} y \texttt{Customer}, donde se puede observar de que entre las columnas que se deben de usar para las concatenaciones solamente \texttt{MiddleName} acepta \textit{nulls} y para solucionar esto se puede usar \textbf{\texttt{\textcolor{magenta}{CONCAT}}}.
        """)
        s57.scale(0.86 * config.frame_width / s57.width); self._fit_group_center(s57, pad_x=1.0, pad_y=0.9)
        self.play(Write(s57, run_time=WRITE_MEDIUM_RT)); self.wait(0.8); self._disappear(s57, rt=0.6)

        # ===== SLIDE 58a  =====
        self._ensure_logo(); self._ensure_frame()
        s58a = self._write_block(r"""
        Para construir el nombre completo usando columnas de \texttt{Customer}, es necesario manejar que \texttt{MiddleName} puede contener \textit{nulls}. Si concatenáramos directamente con espacios, aparecerían separadores duplicados cuando \texttt{MiddleName} sea \texttt{\textcolor{gray}{NULL}}. Para evitarlo, se utiliza \textbf{\texttt{\textcolor{magenta}{IIF}}} indicando que, si \texttt{MiddleName} es \texttt{\textcolor{gray}{NULL}}, no se agregue el espacio adicional, dejando que \textbf{\texttt{\textcolor{magenta}{CONCAT}}} gestione el valor nulo. La expresión quedaría de la siguiente forma:
        """)
        s58a.scale(0.86 * config.frame_width / s58a.width)
        self._fit_group_center(s58a, pad_x=1.0, pad_y=0.9)
        self.play(Write(s58a, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s58a, rt=0.6)


        # ===== SLIDE 58b  =====
        self._ensure_logo(); self._ensure_frame()

        s58b_sql = self._write_block(r"""
        \vskip 5pt
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          
        stringstyle=\color{red},                     
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={CONCAT,IIF}, emphstyle=\color{magenta}\bfseries,
        emph={[2]IS,NULL}, emphstyle={[2]\color{gray}\bfseries}
        ]
        CONCAT(FirstName, ' ', IIF(MiddleName IS NULL, 
        MiddleName, MiddleName + ' '), LastName) AS FullName
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)

        s58b_text = self._write_block(r"""
        \vskip 5pt
        Con ello obtenemos un \texttt{FullName} correctamente formateado. Para la dirección completa aplicamos el mismo principio, usando comas como separadores. Aunque existen funciones más modernas como \textbf{\texttt{\textcolor{magenta}{CONCAT\_WS}}}, esta expresión es suficiente para producir el resultado deseado.
        """)

        g_sql = s58b_sql.copy().move_to(0.20*UP).set_x(0)
        if g_sql.width > 0.86*config.frame_width:
            g_sql.scale((0.86*config.frame_width)/g_sql.width)

        g_txt = s58b_text.copy().next_to(g_sql, DOWN, buff=0.35).set_x(0)
        if g_txt.width > 0.86*config.frame_width:
            g_txt.scale((0.86*config.frame_width)/g_txt.width)

        self._fit_group_center(g_sql, g_txt, pad_x=1.0, pad_y=0.9)

        s58b_sql.scale(g_sql.width/s58b_sql.width).move_to(g_sql.get_center())
        s58b_text.scale(g_txt.width/s58b_text.width).move_to(g_txt.get_center())

        self.play(Write(s58b_sql, run_time=WRITE_MEDIUM_RT)); self.wait(0.3)
        self.play(Write(s58b_text, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s58b_sql, s58b_text, rt=0.6)

        # ===== SLIDE 59a =====
        self._ensure_logo(); self._ensure_frame()
        s59a = self._write_block(r"""
        El resultado solicitado ordenado por nombre completo se obtendría entonces con el siguiente \textit{query}:
        """)
        s59a.scale(0.86 * config.frame_width / s59a.width)
        self._fit_group_center(s59a, pad_x=1.0, pad_y=0.9)
        self.play(Write(s59a, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s59a, rt=0.6)

        # ===== SLIDE 59b  =====
        self._ensure_logo(); self._ensure_frame()
        s59b = self._write_block(r"""
        \vskip 5pt
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={CONCAT,IIF}, emphstyle=\color{magenta}\bfseries,
        emph={[2]SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address},
        emphstyle={[2]\color{magenta}\bfseries},
        emph={[3]JOIN}, emphstyle={[3]\color{gray}\bfseries},
        emph={[4]AS},   emphstyle={[4]\color{blue}\bfseries},
        emph={[5]IS,NULL}, emphstyle={[5]\color{gray}\bfseries}
        ]
        SELECT C.CustomerID,
            CONCAT(FirstName, ' ', IIF(MiddleName IS NULL, '', MiddleName + ' '), LastName) AS FullName,
            CompanyName, Phone,
            CONCAT(AddressLine1, ', ', City, ', ', StateProvince, ', ',
                    CountryRegion, ', ', PostalCode) AS FullAddress
        FROM   SalesLT.Customer AS C
        JOIN   SalesLT.CustomerAddress AS CA
        ON   C.CustomerID = CA.CustomerID
        JOIN   SalesLT.Address AS A
        ON   CA.AddressID = A.AddressID
        ORDER BY FullName;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s59b.scale(0.86 * config.frame_width / s59b.width)
        self._fit_group_center(s59b, pad_x=1.0, pad_y=0.9)
        self.play(Write(s59b, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s59b, rt=0.6)

        # ===== SLIDE 60 =====
        self._ensure_logo(); self._ensure_frame()
        p60 = self._first_existing("ImagesSQL_Slides/Tabla4_OUTER.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla4_OUTER.png","/mnt/data/Tabla4_OUTER.png")
        if p60:
            img60 = ImageMobject(p60).set_width(0.86 * config.frame_width).move_to(ORIGIN).shift(0.05*DOWN)
            cap60 = self._write_block(r"\texttt{Vista parcial}"); cap60.next_to(img60, DOWN, buff=0.12)
            g60 = Group(img60, cap60)
            self.play(FadeIn(g60, shift=DOWN, run_time=0.9)); self.wait(3.0); self._disappear(g60, rt=0.6)

        # ===== SLIDE 61  =====
        self._ensure_logo(); self._ensure_frame()
        s61 = self._write_block(r"""Note que las columnas que no tienen especificado el alias de la tabla son columnas cuyo nombre no aparece más que en su tabla origen, así que no es necesario el alias, pues no hay ambigüedad respecto a qué columna (de qué tabla) nos referimos.""")
        s61.scale(0.86 * config.frame_width / s61.width); self._fit_group_center(s61, pad_x=1.0, pad_y=0.9)
        self.play(Write(s61, run_time=WRITE_MEDIUM_RT)); self.wait(0.8); self._disappear(s61, rt=0.6)

        # ===== SLIDE 62  =====
        self._ensure_logo(); self._ensure_frame()
        s62 = self._write_block(r"""
        Por otro lado, si quisiéramos darles prioridad a los \texttt{CustomerID}, podríamos hacerlo usando \texttt{\textcolor{gray}{LEFT JOIN}} de la siguiente forma: 
        \vskip 5pt
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={CONCAT,IIF}, emphstyle=\color{magenta}\bfseries,
        emph={[2]SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address},
        emphstyle={[2]\color{magenta}\bfseries},
        emph={[3]IS,NULL}, emphstyle={[3]\color{gray}\bfseries},
        emph={[4]JOIN,LEFT}, emphstyle={[4]\color{gray}\bfseries},
        emph={[5]AS}, emphstyle={[5]\color{blue}\bfseries}
        ]
        SELECT C.CustomerID,
            CONCAT(FirstName, ' ', IIF(MiddleName IS NULL, '', MiddleName + ' '), LastName) AS FullName,
            CompanyName, Phone,
            CONCAT(AddressLine1, ', ', City, ', ', StateProvince, ', ', CountryRegion, ', ', PostalCode) AS FullAddress
        FROM SalesLT.Customer AS C
        LEFT JOIN SalesLT.CustomerAddress AS CA
        ON C.CustomerID = CA.CustomerID
        LEFT JOIN SalesLT.Address AS A
        ON CA.AddressID = A.AddressID
        ORDER BY FullName;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s62.scale(0.86 * config.frame_width / s62.width); self._fit_group_center(s62, pad_x=1.0, pad_y=0.9)
        self.play(Write(s62, run_time=WRITE_MEDIUM_RT)); self.wait(3.0); self._disappear(s62, rt=0.6)

        # ===== SLIDE 63  =====
        self._ensure_logo(); self._ensure_frame()
        p63 = self._first_existing("ImagesSQL_Slides/Tabla5_OUTER.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla5_OUTER.png","/mnt/data/Tabla5_OUTER.png")
        if p63:
            img63 = ImageMobject(p63).set_width(0.86 * config.frame_width).move_to(ORIGIN).shift(0.05*DOWN)
            cap63 = self._write_block(r"\texttt{Vista parcial}"); cap63.next_to(img63, DOWN, buff=0.12)
            g63 = Group(img63, cap63)
            self.play(FadeIn(g63, shift=DOWN, run_time=0.9)); self.wait(3.0); self._disappear(g63, rt=0.6)

        # ===== SLIDE 64 =====
        self._ensure_logo(); self._ensure_frame()
        s64 = self._write_block(r"""
        Mediante dos \texttt{\textcolor{gray}{LEFT JOIN}} garantizamos que se preserven los valores de \texttt{CustomerID} y que, cuando no exista cruce, la dirección aparezca como \texttt{\textcolor{gray}{NULL}}; sin embargo, al usar \textbf{\texttt{\textcolor{magenta}{CONCAT}}}, estos \textit{nulls} se sustituyen automáticamente por puntos suspensivos en \texttt{FullAddress}. 
        \vskip 10pt
        Un resultado equivalente podría obtenerse invirtiendo el orden de las tablas y utilizando \texttt{\textcolor{gray}{RIGHT JOIN}}. La diferencia principal es que esta segunda solución devuelve todos los clientes, tengan o no dirección asociada, mientras que la primera solo muestra aquellos con dirección registrada.
        """)
        s64.scale(0.86 * config.frame_width / s64.width); self._fit_group_center(s64, pad_x=1.0, pad_y=0.9)
        self.play(Write(s64, run_time=WRITE_MEDIUM_RT)); self.wait(0.8); self._disappear(s64, rt=0.6)

        # ===== SLIDE 65a  =====
        self._ensure_logo(); self._ensure_frame()
        s65a = self._write_block(r"""
        También es posible combinar \texttt{\textcolor{gray}{INNER JOIN}} con \texttt{\textcolor{gray}{LEFT/RIGHT JOIN}} (en el siguiente \textit{query}): primero se identifican los \texttt{CustomerID} presentes tanto en \texttt{Customer} como en \texttt{CustomerAddress}, y luego se realiza el cruce con \texttt{Address}, esta vez respetando \texttt{AddressID}, para obtener tanto los clientes con dirección como aquellos sin ella. La elección del tipo de \textit{join} depende del resultado deseado; lo importante es definir correctamente el objetivo y las columnas y condiciones de cruce que permitirán obtenerlo.
        """)
        s65a.scale(0.86 * config.frame_width / s65a.width)
        self._fit_group_center(s65a, pad_x=1.0, pad_y=0.9)
        self.play(Write(s65a, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s65a, rt=0.6)

        # ===== SLIDE 65b =====
        self._ensure_logo(); self._ensure_frame()
        s65b = self._write_block(r"""
        \vskip 10pt
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, breaklines=true, columns=fullflexible,
        emph={CONCAT,IIF}, emphstyle=\color{magenta}\bfseries,
        emph={[2]SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address},
        emphstyle={[2]\color{magenta}\bfseries},
        emph={[3]IS,NULL}, emphstyle={[3]\color{gray}\bfseries},
        emph={[4]JOIN,RIGHT}, emphstyle={[4]\color{gray}\bfseries},
        emph={[5]AS}, emphstyle={[5]\color{blue}\bfseries}
        ]
        SELECT C.CustomerID, A.AddressID,
            CONCAT(FirstName, ' ', IIF(MiddleName IS NULL, '', MiddleName + ' '), LastName) AS FullName,
            CompanyName, Phone,
            CONCAT(AddressLine1, ', ', City, ', ', StateProvince, ', ', CountryRegion, ', ', PostalCode) AS FullAddress
        FROM SalesLT.Customer AS C
        JOIN SalesLT.CustomerAddress AS CA
        ON C.CustomerID = CA.CustomerID
        RIGHT JOIN SalesLT.Address AS A
        ON CA.AddressID = A.AddressID
        ORDER BY FullName;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s65b.scale(0.86 * config.frame_width / s65b.width)
        self._fit_group_center(s65b, pad_x=1.0, pad_y=0.9)
        self.play(Write(s65b, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s65b, rt=0.6)


        # ===== SLIDE 66 =====
        self._ensure_logo(); self._ensure_frame()
        s66 = self._write_block(r"""
        Por último, tenemos al \texttt{\textcolor{gray}{FULL OUTER JOIN}}, este tipo de \texttt{\textcolor{gray}{OUTER JOIN}} les da la misma importancia a ambas tablas y preserva los registros de ambas, es decir, regresa los registros que cumplen la coincidencia y a continuación regresa los registros de cada tabla donde no hubo coincidencia y rellena con \textit{nulls} en cada lado. Este es el subtipo de \texttt{\textcolor{gray}{OUTER JOIN}} menos usado.
        """)
        s66.scale(0.86 * config.frame_width / s66.width); self._fit_group_center(s66, pad_x=1.0, pad_y=0.9)
        self.play(Write(s66, run_time=WRITE_MEDIUM_RT)); self.wait(0.8); self._disappear(s66, rt=0.6)

        # ===== SLIDE 67 =====
        self._ensure_logo(); self._ensure_frame()
        p67 = self._first_existing("ImagesSQL_Slides/VENN__FULL_OUTERpng.png","/home/gustavo/SS/ImagesSQL_Slides/VENN__FULL_OUTERpng.png","/mnt/data/VENN__FULL_OUTERpng.png")
        if p67:
            img67 = ImageMobject(p67).set_width(0.50 * config.frame_width).move_to(ORIGIN).shift(0.05*DOWN)
            g67 = Group(img67)
            self.play(FadeIn(g67, shift=DOWN, run_time=0.9)); self.wait(3.0); self._disappear(g67, rt=0.6)
        
        # ===== SLIDE 68  =====
        self._ensure_logo(); self._ensure_frame()
        s68 = self._write_block(r"""
        Supongamos que tenemos una tabla que contiene el \texttt{CustomerID}, el nombre de la compañía, teléfono, y el \texttt{AddressID}. Esta tabla la podemos crear con el siguiente \textit{query}, obteniendo 857 registros: 
        \vskip 5pt
        \begin{center}
        \begin{minipage}{0.96\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, breaklines=true, columns=fullflexible,
        emph={SalesLT.Customer,SalesLT.CustomerAddress},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,LEFT}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT C.CustomerID, CompanyName, Phone, CA.AddressID
        FROM SalesLT.Customer AS C
        LEFT JOIN SalesLT.CustomerAddress AS CA
        ON C.CustomerID = CA.CustomerID
        ORDER BY C.CompanyName;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s68.scale_to_fit_width(0.80*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s68, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s68, rt=0.6)

        # ===== SLIDE 69  =====
        self._ensure_logo(); self._ensure_frame()
        p69 = self._first_existing(
            "Tabla1_FULL_OUTER.png",
            "ImagesSQL_Slides/Tabla1_FULL_OUTER.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tabla1_FULL_OUTER.png",
            "/mnt/data/Tabla1_FULL_OUTER.png"
        )
        if p69:
            img69 = ImageMobject(p69).set_width(0.78 * config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
            cap69 = Tex(r"\texttt{Vista parcial}").next_to(img69, DOWN, buff=0.16)
            g69 = Group(img69, cap69)
            self.play(FadeIn(g69, shift=DOWN, run_time=0.9)); self.wait(5.0)
            self._disappear(g69, rt=0.6)

        # ===== SLIDE 70 =====
        self._ensure_logo(); self._ensure_frame()
        s70 = self._write_block(r"""
        Las tablas \texttt{Customer} y \texttt{Address} no siempre tienen correspondencia porque muchos clientes no cuentan con un \texttt{AddressID}. Si queremos unir ambas de forma que conserven tanto los clientes sin dirección como las direcciones sin cliente asociado, necesitamos un \texttt{\textcolor{gray}{FULL OUTER JOIN}}. Con un \texttt{\textcolor{gray}{LEFT JOIN}} solo preservaríamos los registros de \texttt{Customer}, y con un \texttt{\textcolor{gray}{RIGHT JOIN}} solo los de \texttt{Address}, por lo que perderíamos información.
        """)
        s70.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s70, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s70, rt=0.6)

        # ===== SLIDE 71a =====
        self._ensure_logo(); self._ensure_frame()
        s71a = self._write_block(r"""
        Para este caso utilizamos la tabla virtual generada por el \textit{query} anterior como \texttt{Customers}, y luego aplicamos el \texttt{\textcolor{gray}{FULL OUTER JOIN}} para obtener el cruce completo. Antes de hacer el nuevo \textit{join}, eliminamos el \texttt{\textcolor{blue}{\textbf{ORDER BY}}} del \textit{query} previo, dado que no puede colocarse antes del \textit{join}.
        """)
        s71a.scale(0.86 * config.frame_width / s71a.width)
        self._fit_group_center(s71a, pad_x=1.0, pad_y=0.9)
        self.play(Write(s71a, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s71a, rt=0.6)

        # ===== SLIDE 71b =====
        self._ensure_logo(); self._ensure_frame()
        s71b = self._write_block(r"""
        \vskip 10pt
        \begin{center}
        \begin{minipage}{0.96\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        commentstyle=\color{green!60!black}\bfseries,
        frame=none, breaklines=true, columns=fullflexible,
        emph={CONCAT,IIF}, emphstyle=\color{magenta}\bfseries,
        emph={[2]SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address},
        emphstyle={[2]\color{magenta}\bfseries},
        emph={[3]IS,NULL}, emphstyle={[3]\color{gray}\bfseries},
        emph={[4]JOIN,FULL}, emphstyle={[4]\color{gray}\bfseries},
        emph={[5]AS}, emphstyle={[5]\color{blue}\bfseries}
        ]
        SELECT Customers.*,
            A.AddressID AS AddressID2,
            CONCAT(AddressLine1, ', ', City, ', ', StateProvince, ', ',
                    CountryRegion, ', ', PostalCode) AS FullAddress
        FROM 
        (SELECT C.CustomerID, CompanyName, Phone, CA.AddressID
        FROM SalesLT.Customer AS C
        LEFT JOIN SalesLT.CustomerAddress AS CA
        ON C.CustomerID = CA.CustomerID) AS Customers
        FULL JOIN SalesLT.Address AS A
        ON Customers.AddressID = A.AddressID
        ORDER BY Phone DESC;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s71b.scale_to_fit_width(0.74 * config.frame_width).move_to(ORIGIN).shift(0.10*DOWN)
        self.play(Write(s71b, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s71b, rt=0.6)


        # ===== SLIDE 72 =====
        self._ensure_logo(); self._ensure_frame()
        p72 = self._first_existing(
            "Tabla2_FULL_OUTER.png",
            "ImagesSQL_Slides/Tabla2_FULL_OUTER.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tabla2_FULL_OUTER.png",
            "/mnt/data/Tabla2_FULL_OUTER.png"
        )
        if p72:
            img72 = ImageMobject(p72).set_width(0.78 * config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
            cap72 = Tex(r"\texttt{Vista parcial}").next_to(img72, DOWN, buff=0.16)
            g72 = Group(img72, cap72)
            self.play(FadeIn(g72, shift=DOWN, run_time=0.9)); self.wait(5.0)
            self._disappear(g72, rt=0.6)

        # ===== SLIDE 73 =====
        self._ensure_logo(); self._ensure_frame()
        s73 = self._write_block(r"""
        En este resultado final se observa que el \textit{query} aplicado sobre \texttt{Customers} regresa 890 registros, lo cual muestra que el \texttt{\textcolor{gray}{FULL OUTER JOIN}} preserva tanto los \texttt{CustomerID} de \texttt{Customers} que no tienen un \texttt{AddressID} asociado, como las direcciones que no tienen cliente (identificadas mediante \texttt{AddressID2}).
        """)
        s73.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s73, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s73, rt=0.6)

        # ===== SLIDE 74 =====
        self._ensure_logo(); self._ensure_frame()
        s74 = self._write_block(r"""
        Esto ejemplifica la funcionalidad del \texttt{\textcolor{gray}{FULL OUTER JOIN}}. Además, con este ejemplo se concluye la explicación de los tres tipos de \texttt{\textcolor{gray}{OUTER JOIN}} disponibles en \textit{SQL}. Aunque en la práctica los más comunes son \texttt{\textcolor{gray}{INNER JOIN}} y \texttt{\textcolor{gray}{LEFT JOIN}}, existen otros tipos de \textit{joins} menos utilizados que pueden ser relevantes en situaciones específicas, y sobre ellos se hablará a continuación.
        """)
        s74.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s74, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s74, rt=0.6)

        # ===== SLIDE 75 =====
        self._ensure_logo(); self._ensure_frame()
        s75 = self._write_block(r"\subsection*{\texttt{\textcolor{myPurple}{CROSS JOIN}}}")
        self.play(Write(s75, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s75)

        # ===== SLIDE 76  =====
        self._ensure_logo(); self._ensure_frame()
        s76 = self._write_block(r"""
        Un \texttt{\textcolor{gray}{CROSS JOIN}} es la forma explícita que se tiene para realizar un producto cartesiano, es decir, el resultado será todas las posibles combinaciones entre los registros entre dos tablas, por lo que su generación suele ser lenta y con pocos usos en la práctica (es útil para generar conjuntos de prueba).
        \vskip 10pt
        En un \texttt{\textcolor{gray}{INNER JOIN}}, ese producto cartesiano inicial se filtra mediante la condición escrita en \texttt{\textcolor{blue}{\textbf{ON}}}, mientras que en un \texttt{\textcolor{gray}{OUTER JOIN}} dicho producto cartesiano filtrado se complementa con los registros que no coincidieron, rellenando los faltantes con \texttt{\textcolor{gray}{NULL}}. Por ello, el \texttt{\textcolor{gray}{CROSS JOIN}} muestra el producto cartesiano tal cual, sin filtros ni agregados.
        """)
        s76.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s76, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s76, rt=0.6)

        # ===== SLIDE 77  =====
        self._ensure_logo(); self._ensure_frame()
        s77 = self._write_block(r"""
        \begin{center}
        \begin{minipage}{0.95\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.ProductCategory,Product}, emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,CROSS}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries},
        emph={[4]IS,NOT,NULL}, emphstyle={[4]\color{gray}\bfseries}
        ]
        SELECT ProductCategoryID, Name, Color
        FROM   SalesLT.ProductCategory AS Cat
        CROSS JOIN (SELECT DISTINCT Color
                    FROM  SalesLT.Product
                    WHERE Color IS NOT NULL) AS Col
        ORDER BY Name;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s77.scale_to_fit_width(0.74*config.frame_width).move_to(ORIGIN).shift(0.10*DOWN)
        self.play(Write(s77, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s77, rt=0.6)

        # ===== SLIDE 78  =====
        self._ensure_logo(); self._ensure_frame()
        p78 = self._first_existing(
            "Tabla1_CROSS_JOIN.png",
            "ImagesSQL_Slides/Tabla1_CROSS_JOIN.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tabla1_CROSS_JOIN.png",
            "/mnt/data/Tabla1_CROSS_JOIN.png"
        )
        if p78:
            img78 = ImageMobject(p78).set_width(0.38 * config.frame_width)
            cap78 = self._write_block(r"\texttt{Vista parcial}")
            cap78.next_to(img78, DOWN, buff=0.12)
            g78 = Group(img78, cap78).move_to(ORIGIN).shift(0.07*DOWN)
            self.play(FadeIn(g78, shift=DOWN, run_time=0.9)); self.wait(3.0)
            self._disappear(g78, rt=0.6)

        # ===== SLIDE 79  =====
        self._ensure_logo(); self._ensure_frame()
        s79 = self._write_block(r"""
        Nótese que no se ha usado \texttt{\textcolor{blue}{\textbf{ON}}}, esto se debe a que se están generando todas las combinaciones posibles entre los registros, por lo cual no se necesitan especificar condiciones para el cruce. Aunque este tipo de \textit{join} no es común, pueden existir escenarios en donde se requiera su uso.
        """)
        s79.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s79, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s79, rt=0.6)

        # ===== SLIDE 80  =====
        self._ensure_logo(); self._ensure_frame()
        s80 = self._write_block(r"\subsection*{\textcolor{myPurple}{\texttt{SELF JOIN}}}")
        self.play(Write(s80, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s80)
        
        # ===== SLIDE 81 =====
        self._ensure_logo(); self._ensure_frame()
        s81 = self._write_block(r"""
        Los cinco tipos de \textit{joins} que se han visto hasta ahora, forman parte del estándar \textit{ANSI}: \texttt{\textcolor{gray}{INNER, OUTER (LEFT, RIGHT, FULL)}} y \texttt{\textcolor{gray}{CROSS}}. Pero existe un \textit{join} más que es el producto de estos en el caso de que las dos tablas implicadas en el \textit{join} sea la misma y es el llamado \texttt{\textcolor{gray}{SELF JOIN}}.
        \vskip 5pt
        En un \texttt{\textcolor{gray}{SELF JOIN}} comparamos registros de una misma tabla consigo misma, es decir, creamos dos copias virtuales de la misma tabla mediante \texttt{\textcolor{blue}{FROM}}. A diferencia de otros \textit{joins}, aquí no existe una sintaxis especial: simplemente aplicamos cualquier tipo de \textit{join} usando la misma tabla dos veces, lo cual obliga a usar alias para distinguirlas.
        """)
        s81.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s81, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s81, rt=0.6)

        # ===== SLIDE 82 =====
        self._ensure_logo(); self._ensure_frame()
        s82 = self._write_block(r"""
        Por ejemplo, anteriormente se discutía el uso de \texttt{\textcolor{gray}{CROSS JOIN}} para crear un conjunto de datos de prueba; ahora un uso práctico aparece al combinar nombres de la tabla \texttt{Customer} para generar todas las combinaciones posibles entre nombres y apellidos, creando así una tabla de nombres que se podrían usar en pruebas u otras actividades. Conceptualmente se está realizando un \texttt{\textcolor{gray}{SELF JOIN}}. 
        \vskip 5pt
        El siguiente \textit{query} implementa lo anterior, utilizando \texttt{\textcolor{blue}{DISTINCT}} para evitar duplicados y produce 125{,}370 registros:
        \vskip 5pt
        \begin{center}
        \begin{minipage}{0.95\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.Customer}, emphstyle=\color{magenta}\bfseries,
        emph={CROSS,JOIN}, emphstyle=\color{gray}\bfseries,
        emph={[2]AS}, emphstyle={[2]\color{blue}\bfseries}
        ]
        SELECT DISTINCT C1.FirstName, C2.LastName
        FROM SalesLT.Customer AS C1
        CROSS JOIN SalesLT.Customer AS C2
        ORDER BY C1.FirstName DESC, C2.LastName ASC;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s82.scale_to_fit_width(0.74*config.frame_width).move_to(ORIGIN).shift(0.10*DOWN)
        self.play(Write(s82, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s82, rt=0.6)

        # ===== SLIDE 83 =====
        self._ensure_logo(); self._ensure_frame()
        p83 = self._first_existing(
            "Tabla1_SELF_JOIN.png",
            "ImagesSQL_Slides/Tabla1_SELF_JOIN.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tabla1_SELF_JOIN.png",
            "/mnt/data/Tabla1_SELF_JOIN.png"
        )
        if p83:
            img83 = ImageMobject(p83).set_width(0.30 * config.frame_width).move_to(ORIGIN).shift(0.07*DOWN)
            cap83 = Tex(r"\texttt{Vista parcial}").next_to(img83, DOWN, buff=0.12)
            g83 = Group(img83, cap83)
            self.play(FadeIn(g83, shift=DOWN, run_time=0.9)); self.wait(3.0)
            self._disappear(g83, rt=0.6)

        # ===== SLIDE 84 (subtítulo) =====
        self._ensure_logo(); self._ensure_frame()
        s84 = self._write_block(r"\subsection*{\textcolor{myPurple}{Operadores de conjuntos: \texttt{UNION}, \texttt{INTERSECT} y \texttt{EXCEPT}}}")
        self.play(Write(s84, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s84)

        # ===== SLIDE 85  =====
        self._ensure_logo(); self._ensure_frame()
        s85 = self._write_block(r"""
        A diferencia de los \textit{joins}, donde se trabaja de forma horizontal, los Operadores de conjuntos se trabajan de forma vertical y su implementación en \textit{SQL} sigue las operaciones clásicas de Teoría de conjuntos.
        \vskip 10pt
        El primer operador se conoce como \texttt{\textcolor{blue}{UNION}}, este tiene la función de combinar los registros de dos tablas de manera vertical, así, el número de registros de la tabla final será igual a la suma del número de registros de cada una de las tablas individuales, siempre y cuando no haya duplicados.
        """)
        s85.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s85, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s85, rt=0.6)

        # ===== SLIDE 86  =====
        self._ensure_logo(); self._ensure_frame()
        s86 = self._write_block(r"""
        Por defecto \texttt{\textcolor{blue}{UNION}} elimina los duplicados, pero para hacer esto compara cada registro con los demás para verificar que no haya duplicados, lo cual afectará el rendimiento, más cuando se tienen muchos \texttt{\textcolor{blue}{UNION}} en un solo \textit{query}. Sin embargo, si se quiere conservar los duplicados lo podemos hacer usando \texttt{\textcolor{blue}{UNION}} \texttt{\textcolor{gray}{ALL}}.
        """)
        s86.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s86, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s86, rt=0.6)

        # ===== SLIDE 87  =====
        self._ensure_logo(); self._ensure_frame()
        p87 = self._first_existing("VENN_UNION.png","ImagesSQL_Slides/VENN_UNION.png","/home/gustavo/SS/ImagesSQL_Slides/VENN_UNION.png","/mnt/data/VENN_UNION.png")
        if p87:
            img87 = ImageMobject(p87).set_width(0.48 * config.frame_width).move_to(ORIGIN).shift(0.06*DOWN)
            self.play(FadeIn(img87, shift=DOWN, run_time=0.9)); self.wait(3.0)
            self._disappear(img87, rt=0.6)

        # ===== SLIDE 88  =====
        self._ensure_logo(); self._ensure_frame()
        s88 = self._write_block(r"""
        Las tablas que se unen, son cada una el resultado de un \textit{query} individual. Y para utilizar \texttt{\textcolor{blue}{UNION}} se debe de tener el mismo número de columnas, cuyos tipos de datos entre tablas deben de ser los mismos; para esto pueden ser compatibles para realizar una conversión implícita o se puede realizar una conversión explícita.
        """)
        s88.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s88, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s88, rt=0.6)

        # ===== SLIDE 89  =====
        self._ensure_logo(); self._ensure_frame()
        s89 = self._write_block(r"""
        Véase un ejemplo: Las direcciones de los clientes se clasifican en oficina principal (Main Office) y dirección de entrega (Shipping); como cada compra debe facturarse, se toma como dirección de facturación la de la oficina principal. Para identificar claramente qué dirección registrada corresponde a cada cliente y a su uso, se construye un \textit{query} que primero genera una tabla con las direcciones de la oficina principal marcadas como de facturación (Billing), obteniendo 407 registros:
        """)
        s89.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s89, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s89, rt=0.6)

        # ===== SLIDE 90 =====
        self._ensure_logo(); self._ensure_frame()
        s90 = self._write_block(r"""
        \begin{center}
        \begin{minipage}{0.95\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,AND,OR,NOT,IN,IS}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries},
        emph={[4]CONCAT}, emphstyle={[4]\color{magenta}\bfseries}
        ]
        SELECT  C.CompanyName,
                CONCAT(AddressLine1, ', ', City, ', ',
                    StateProvince, ', ', CountryRegion, ', ', PostalCode) AS FullAddress,
                'Billing' AS AddressType
        FROM    SalesLT.Customer AS C
        JOIN    SalesLT.CustomerAddress AS CA
        ON    C.CustomerID = CA.CustomerID
        JOIN    SalesLT.Address AS A
        ON    CA.AddressID  = A.AddressID
        WHERE   CA.AddressType = 'Main Office';
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s90.scale_to_fit_width(0.74*config.frame_width).move_to(ORIGIN).shift(0.10*DOWN)
        self.play(Write(s90, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s90, rt=0.6)

        # ===== SLIDE 91 =====
        self._ensure_logo(); self._ensure_frame()
        s91 = self._write_block(r"""
        Luego, se obtienen las direcciones usadas para el envío, especificando que son direcciones de envío (Shipping), obteniendo 10 registros:
        \vskip 12pt
        \begin{center}
        \begin{minipage}{0.95\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,AND,OR,NOT,IN,IS}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries},
        emph={[4]CONCAT}, emphstyle={[4]\color{magenta}\bfseries}
        ]
        SELECT  C.CompanyName,
                CONCAT(AddressLine1, ', ', City, ', ',
                    StateProvince, ', ', CountryRegion, ', ', PostalCode) AS FullAddress,
                'Shipping' AS AddressType
        FROM    SalesLT.Customer AS C
        JOIN    SalesLT.CustomerAddress AS CA
        ON    C.CustomerID = CA.CustomerID
        JOIN    SalesLT.Address AS A
        ON    CA.AddressID = A.AddressID
        WHERE   CA.AddressType = 'Shipping';
        \end{lstlisting}
        \end{minipage}
        \end{center}
        \vskip 4pt
        Y el último paso será unir las dos tablas:
        """)
        s91.scale_to_fit_width(0.74*config.frame_width).move_to(ORIGIN).shift(0.10*DOWN)
        self.play(Write(s91, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s91, rt=0.6)

        # ===== Slide 92 ====================
        self._ensure_logo(); self._ensure_frame()
        self._scroll_code_in_window(r"""
        \begin{center}
        \begin{minipage}{0.95\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none,
        breaklines=true,
        columns=fullflexible,
        emph={SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,AND,OR,NOT,IN,IS,UNION}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries},
        emph={[4]CONCAT}, emphstyle={[4]\color{magenta}\bfseries}
        ]
        SELECT  C.CompanyName,
                CONCAT(AddressLine1, ', ', City, ', ',
                    StateProvince, ', ', CountryRegion, ', ', PostalCode) AS FullAddress,
                'Billing' AS AddressType
        FROM    SalesLT.Customer AS C
        JOIN    SalesLT.CustomerAddress AS CA
        ON    C.CustomerID = CA.CustomerID
        JOIN    SalesLT.Address AS A
        ON    CA.AddressID = A.AddressID
        WHERE   CA.AddressType = 'Main Office'
        UNION
        SELECT  C.CompanyName,
                CONCAT(AddressLine1, ', ', City, ', ',
                    StateProvince, ', ', CountryRegion, ', ', PostalCode) AS FullAddress,
                'Shipping' AS AddressType
        FROM    SalesLT.Customer AS C
        JOIN    SalesLT.CustomerAddress AS CA
        ON    C.CustomerID = CA.CustomerID
        JOIN    SalesLT.Address AS A
        ON    CA.AddressID = A.AddressID
        WHERE   CA.AddressType = 'Shipping';
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """,
        window_w=0.92,
        window_h=0.74,
        down=0.10,
        pad=0.22,
        rt_write=WRITE_MEDIUM_RT,
        rt_scroll=22.0,   
        rt_out=0.6,
        show_border=False
        )

        # ===== SLIDE 93 =====
        self._ensure_logo(); self._ensure_frame()
        p93 = self._first_existing("Tabla7_INNER.png","ImagesSQL_Slides/Tabla7_INNER.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla7_INNER.png","/mnt/data/Tabla7_INNER.png")
        if p93:
            img93 = ImageMobject(p93).set_width(0.66 * config.frame_width).move_to(ORIGIN).shift(0.07*DOWN)
            cap93 = Tex(r"\texttt{Vista parcial}").next_to(img93, DOWN, buff=0.12)
            g93 = Group(img93, cap93)
            self.play(FadeIn(g93, shift=DOWN, run_time=0.9)); self.wait(3.0)
            self._disappear(g93, rt=0.6)

        # ===== SLIDE 94 =====
        self._ensure_logo(); self._ensure_frame()
        s94 = self._write_block(r"""
        Se combinan los registros de ambos \textit{queries} mediante \texttt{\textcolor{blue}{UNION}}, obteniendo 417 filas, ilustrando cómo usar \texttt{\textcolor{blue}{UNION}} para unir tablas (por ejemplo, dos CSV cargados a SQL Server). En el ejemplo las filas son distintas, así que \texttt{\textcolor{blue}{UNION}} y \texttt{\textcolor{blue}{UNION}} \texttt{\textcolor{gray}{ALL}} dan el mismo conjunto, pero \texttt{\textcolor{blue}{UNION}} \texttt{\textcolor{gray}{ALL}} es más rápido al no eliminar duplicados; si se quieren quitar duplicados se usa \texttt{\textcolor{blue}{UNION}}. En los \textit{queries} con nombres de productos, \texttt{\textcolor{blue}{UNION}}  \texttt{\textcolor{gray}{ALL}} conserva duplicados y regresa 423 registros, mientras que \texttt{\textcolor{blue}{UNION}} los elimina y regresa 354.
        \vskip 8pt
        \begin{center}
        \begin{minipage}{0.92\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={SalesLT.Product,SalesLT.ProductModel},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]ALL,AND,OR,NOT,IN}, emphstyle={[2]\color{gray}\bfseries}]
        SELECT Name FROM SalesLT.Product
        UNION ALL
        SELECT Name FROM SalesLT.ProductModel;

        SELECT Name FROM SalesLT.Product
        UNION
        SELECT Name FROM SalesLT.ProductModel;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s94.scale_to_fit_width(0.74*config.frame_width).move_to(ORIGIN).shift(0.10*DOWN)
        self.play(Write(s94, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s94, rt=0.6)

        # ===== SLIDE 95 =====
        self._ensure_logo(); self._ensure_frame()
        s95 = self._write_block(r"""
        Pero si se quisieran obtener los registros duplicados, es decir, aquellos que aparecen en ambas tablas, se puede usar el operador de conjuntos \texttt{\textcolor{blue}{INTERSECT}}.
        En el ejemplo de los nombres de los productos el resultado es una lista con los nombres que aparecían en ambas tablas, los cuales son 69:
        \vskip 8pt
        \begin{center}
        \begin{minipage}{0.92\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={SalesLT.Product,SalesLT.ProductModel},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]AND,OR,NOT,IN}, emphstyle={[2]\color{gray}\bfseries}]
        SELECT Name FROM SalesLT.Product
        INTERSECT
        SELECT Name FROM SalesLT.ProductModel
        ORDER BY Name;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """)
        s95.scale_to_fit_width(0.74*config.frame_width).move_to(ORIGIN).shift(0.10*DOWN)
        self.play(Write(s95, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s95, rt=0.6)

        # ===== SLIDE 96 =====
        self._ensure_logo(); self._ensure_frame()
        p96 = self._first_existing("Tabla8_INNER.png","ImagesSQL_Slides/Tabla8_INNER.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla8_INNER.png","/mnt/data/Tabla8_INNER.png")
        if p96:
            img96 = ImageMobject(p96).set_width(0.20 * config.frame_width).move_to(ORIGIN).shift(0.07*DOWN)
            cap96 = Tex(r"\texttt{Vista parcial}").next_to(img96, DOWN, buff=0.12)
            g96 = Group(img96, cap96)
            self.play(FadeIn(g96, shift=DOWN, run_time=0.9)); self.wait(3.0)
            self._disappear(g96, rt=0.6)

        # ===== SLIDE 97 =====
        self._ensure_logo(); self._ensure_frame()
        p97 = self._first_existing("VENN_INTERSECT.png","ImagesSQL_Slides/VENN_INTERSECT.png","/home/gustavo/SS/ImagesSQL_Slides/VENN_INTERSECT.png","/mnt/data/VENN_INTERSECT.png")
        if p97:
            img97 = ImageMobject(p97).set_width(0.48 * config.frame_width).move_to(ORIGIN).shift(0.06*DOWN)
            self.play(FadeIn(img97, shift=DOWN, run_time=0.9)); self.wait(3.0)
            self._disappear(img97, rt=0.6)

        # ===== SLIDE 98 =====
        self._ensure_logo(); self._ensure_frame()
        self._scroll_code_in_window(r"""
        Retomando el ejemplo de las direcciones, se pueden obtener los nombres de las compañías que tienen tanto dirección de envió como se su oficina principal:
        \vskip 5pt
        \begin{center}
        \begin{minipage}{0.95\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,AND,OR,NOT,IN}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT  C.CompanyName
        FROM    SalesLT.Customer AS C
        JOIN    SalesLT.CustomerAddress AS CA
        ON    C.CustomerID = CA.CustomerID
        JOIN    SalesLT.Address AS A
        ON    CA.AddressID  = A.AddressID
        WHERE   CA.AddressType = 'Main Office'
        INTERSECT
        SELECT  C.CompanyName
        FROM    SalesLT.Customer AS C
        JOIN    SalesLT.CustomerAddress AS CA
        ON    C.CustomerID = CA.CustomerID
        JOIN    SalesLT.Address AS A
        ON    CA.AddressID  = A.AddressID
        WHERE   CA.AddressType = 'Shipping'
        ORDER BY CompanyName;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """,
        window_w=0.92,
        window_h=0.74,
        down=0.10,
        pad=0.22,
        rt_write=WRITE_MEDIUM_RT,
        rt_scroll=22.0,   
        rt_out=0.6,
        show_border=False
        )

        # ===== SLIDE 99 =====
        self._ensure_logo(); self._ensure_frame()
        p99 = self._first_existing("Tabla9_INNER.png","ImagesSQL_Slides/Tabla9_INNER.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla9_INNER.png","/mnt/data/Tabla9_INNER.png")
        if p99:
            img99 = ImageMobject(p99).set_width(0.30 * config.frame_width).move_to(ORIGIN).shift(0.07*DOWN)
            cap99 = Tex(r"\texttt{Vista completa}").next_to(img99, DOWN, buff=0.12)
            g99 = Group(img99, cap99)
            self.play(FadeIn(g99, shift=DOWN, run_time=0.9)); self.wait(3.0)
            self._disappear(g99, rt=0.6)

        # ===== SLIDE 100  =====
        self._ensure_logo(); self._ensure_frame()
        s100 = self._write_block(r"""
        Y finalmente se tiene a \texttt{\textcolor{blue}{EXCEPT}}, el cual regresa los registros distintos que aparecen en la primera tabla, pero no en la segunda. En este caso, el orden de especificación importa.
        """)
        s100.scale_to_fit_width(0.78*config.frame_width).move_to(ORIGIN).shift(0.08*DOWN)
        self.play(Write(s100, run_time=WRITE_MEDIUM_RT)); self.wait(0.8)
        self._disappear(s100, rt=0.6)

        # ===== SLIDE 101  =====
        self._ensure_logo(); self._ensure_frame()
        p101 = self._first_existing("VENN_EXCEPT.png","ImagesSQL_Slides/VENN_EXCEPT.png","/home/gustavo/SS/ImagesSQL_Slides/VENN_EXCEPT.png","/mnt/data/VENN_EXCEPT.png")
        if p101:
            img101 = ImageMobject(p101).set_width(0.48 * config.frame_width).move_to(ORIGIN).shift(0.06*DOWN)
            self.play(FadeIn(img101, shift=DOWN, run_time=0.9)); self.wait(3.0)
            self._disappear(img101, rt=0.6)

        # ===== SLIDE 102 =====
        self._ensure_logo(); self._ensure_frame()
        self._scroll_code_in_window(r"""
        Así, para obtener los nombres de las compañías que tienen dirección de su oficina principal pero no para envío se puede usar lo siguiente:
        \vskip 8pt
        \begin{center}
        \begin{minipage}{0.95\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        breaklines=true, columns=fullflexible,
        emph={SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address},
        emphstyle=\color{magenta}\bfseries,
        emph={[2]JOIN,AND,OR,NOT,IN}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]AS}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT  C.CompanyName
        FROM    SalesLT.Customer AS C
        JOIN    SalesLT.CustomerAddress AS CA
        ON    C.CustomerID = CA.CustomerID
        JOIN    SalesLT.Address AS A
        ON    CA.AddressID  = A.AddressID
        WHERE   CA.AddressType = 'Main Office'
        EXCEPT
        SELECT  C.CompanyName
        FROM    SalesLT.Customer AS C
        JOIN    SalesLT.CustomerAddress AS CA
        ON    C.CustomerID = CA.CustomerID
        JOIN    SalesLT.Address AS A
        ON    CA.AddressID  = A.AddressID
        WHERE   CA.AddressType = 'Shipping'
        ORDER BY CompanyName;
        \end{lstlisting}
        \end{minipage}
        \end{center}
        """,
        window_w=0.92,
        window_h=0.74,
        down=0.10,
        pad=0.22,
        rt_write=WRITE_MEDIUM_RT,
        rt_scroll=22.0,   
        rt_out=0.6,
        show_border=False
        )

        # ===== SLIDE 103  =====
        self._ensure_logo(); self._ensure_frame()
        p103 = self._first_existing("Tabla10_INNER.png","ImagesSQL_Slides/Tabla10_INNER.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla10_INNER.png","/mnt/data/Tabla10_INNER.png")
        if p103:
            img103 = ImageMobject(p103).set_width(0.20 * config.frame_width).move_to(ORIGIN).shift(0.07*DOWN)
            cap103 = Tex(r"\texttt{Vista parcial}").next_to(img103, DOWN, buff=0.12)
            g103 = Group(img103, cap103)
            self.play(FadeIn(g103, shift=DOWN, run_time=0.9)); self.wait(3.0)
            self._disappear(g103, rt=0.6)


# manim -pql ConsultasMultitabla.py ConsultasMultitabla