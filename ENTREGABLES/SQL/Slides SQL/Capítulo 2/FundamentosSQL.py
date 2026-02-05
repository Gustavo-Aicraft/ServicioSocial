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

TITLE_MAIN = r"\section*{\textcolor{myPurple}{Fundamentos de Consultas \texttt{SQL}}}"

class FundamentosSQL(Scene):
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
        s2 = self._write_block(r"\subsection*{\textcolor{myPurple}{El comando \texttt{SELECT}}}")
        self.play(Write(s2, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s2)

        # ===== SLIDE 3 =====
        self._ensure_logo(); self._ensure_frame()
        s3 = self._write_block(r"""El comando más importante en \texttt{SQL} es \texttt{\textbf{\textcolor{blue}{SELECT}}}, cuya función es recuperar datos de una o varias tablas mediante una consulta o \textit{\textbf{query}}. Su estructura general es la siguiente:
        \vskip 5pt
        \begin{center}
        \begin{minipage}{0.8\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none]
        SELECT <lista de selección>
        FROM <tabla fuente>
        WHERE <condición de búsqueda>
        GROUP BY <lista de agrupación>
        HAVING <condición de búsqueda>
        ORDER BY <lista de ordenamiento>
        \end{lstlisting}
        \end{minipage}
        \end{center}""")
        self._fit_group_center(s3)
        self.play(Write(s3, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s3, rt=0.6)

        # ===== SLIDE 4 =====
        self._ensure_logo(); self._ensure_frame()
        s4 = self._write_block(r"""Cada cláusula cumple una función específica en la selección de datos, y el orden mostrado es fijo; modificarlo genera errores. Las cláusulas más importantes son \texttt{\textbf{\textcolor{blue}{SELECT}}} y \texttt{\textbf{\textcolor{blue}{FROM}}}.
        \vskip 15pt
        \paragraph{\textcolor{purple}{Cláusula}} \texttt{\textbf{\textcolor{blue}{SELECT.}}} 
        Define qué columnas o expresiones queremos visualizar en el resultado. Usualmente son columnas de una tabla, aunque pueden ser columnas provenientes de distintas tablas o expresiones calculadas. El resultado de un \texttt{\textbf{\textcolor{blue}{SELECT}}} es una tabla virtual, es decir, una representación de los datos sin alterar las tablas originales. """)
        self._fit_group_center(s4)
        self.play(Write(s4, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s4, rt=0.6)

        # ===== SLIDE 5 =====
        self._ensure_logo(); self._ensure_frame()
        s5 = self._write_block(r"""
        \noindent\begin{minipage}{0.96\linewidth}
        \paragraph{\textcolor{purple}{Cláusula}} \texttt{\textbf{\textcolor{blue}{FROM.}}}
        Indica de qué tabla o tablas se obtendrán los datos. Una vez seleccionadas las columnas, se especifica la fuente mediante \texttt{\textbf{\textcolor{blue}{FROM}}}.\par\vskip 10pt
        \vskip 5pt
        Las dos formas de comentar en \texttt{T-SQL} son las siguientes:
        \end{minipage}
        \vskip 10pt
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        commentstyle=\color{green!50!black},
        stringstyle=\color{red},
        frame=none]
        --Forma 1: Mi primer SELECT
        /* Forma 2:
        Mi Primer SELECT
        */
        SELECT * FROM SalesLT.Product;
        \end{lstlisting}
        \end{minipage}
        \end{center}""")
        self._fit_group_center(s5)
        self.play(Write(s5, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s5, rt=0.6)

        # ===== SLIDE 6 =====
        self._ensure_logo(); self._ensure_frame()
        s6 = self._write_block(r"""El símbolo $*$ es conocido como punto inicial o punto flotante. Este tipo de \textit{query} es útil cuando se quiere una vista rápida al contenido de una tabla o cuando sabemos que la tabla no se modificará. """)
        self._fit_group_center(s6)
        self.play(Write(s6, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s6, rt=0.6)

        # ===== SLIDE 7 =====
        self._ensure_logo(); self._ensure_frame()
        s7 = self._write_block(r"""Aplicar el comando anterior puede ejecutarse lento dependiendo del tamaño de la tabla, ya que se obtiene toda la información de esta y puede tener más datos de los necesarios. Asi que es mejor hacer \textit{queries} que sean mas específicos, como el siguiente: """)
        self._fit_group_center(s7)
        self.play(Write(s7, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s7, rt=0.6)

        # ===== SLIDE 8 =====
        self._ensure_logo(); self._ensure_frame()
        s8 = self._write_block(r"""\begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none,
        aboveskip=0pt, belowskip=0pt
        ]
        SELECT Name AS Product, ListPrice
        FROM SalesLT.Product;
        \end{lstlisting}
        \end{minipage}
        \end{center}""")
        self._fit_group_center(s8)
        self.play(Write(s8, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s8, rt=0.6)

        # ===== SLIDE 9 =====
        self._ensure_logo(); self._ensure_frame()
        p9 = self._first_existing("Tabla2SQL.png","ImagesSQL_Slides/Tabla2SQL.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla2SQL.png","/mnt/data/Tabla2SQL.png")
        if p9:
            img9 = ImageMobject(p9).set_height(0.62 * config.frame_height)
            cap9 = Tex(r"\texttt{Vista parcial}").next_to(img9, DOWN, buff=0.12)
            g9 = Group(img9, cap9)
            self._fit_group_center(g9)
            g9.shift(0.07*DOWN)
            self.play(FadeIn(img9, shift=DOWN, run_time=0.9))
            self.play(Write(cap9, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g9, rt=0.6)

        # ===== SLIDE 10 =====
        self._ensure_logo(); self._ensure_frame()
        s10 = self._write_block(r"""El \textit{query} usa \texttt{\textcolor{blue}{\textbf{AS}}} para asignar alias, permitiendo renombrar columnas en el resultado. Esto es útil para mostrar nombres más claros, traducir encabezados o nombrar columnas resultantes de operaciones que no tienen nombre por defecto.
        \vskip 20pt
        Si quisiéramos aplicar un descuento al precio de lista del producto de $25\%$ y quisiéramos que el resultado apareciera en español podríamos hacerlo de la siguiente forma:  """)
        self._fit_group_center(s10)
        self.play(Write(s10, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s10, rt=0.6)

        # ===== SLIDE 11 =====
        self._ensure_logo(); self._ensure_frame()
        s11 = self._write_block(r"""\begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none,
        aboveskip=0pt, belowskip=0pt]
        SELECT Name AS Producto, 
            ListPrice*0.75 AS Precio_con_Descuento
        FROM SalesLT.Product;
        \end{lstlisting}
        \end{minipage}
        \end{center}""")
        self._fit_group_center(s11)
        self.play(Write(s11, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s11, rt=0.6)

        # ===== SLIDE 12 =====
        self._ensure_logo(); self._ensure_frame()
        p12 = self._first_existing("Tabla4SQL.png","ImagesSQL_Slides/Tabla4SQL.png","/home/gustavo/SS/ImagesSQL_Slides/Tabla4SQL.png","/mnt/data/Tabla4SQL.png")
        if p12:
            img12 = ImageMobject(p12).set_height(0.62 * config.frame_height)
            cap12 = Tex(r"\texttt{Vista parcial}").next_to(img12, DOWN, buff=0.12)
            g12 = Group(img12, cap12)
            self._fit_group_center(g12)
            g12.shift(0.07*DOWN)
            self.play(FadeIn(img12, shift=DOWN, run_time=0.9))
            self.play(Write(cap12, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g12, rt=0.6)

        # ===== SLIDE 13 =====
        self._ensure_logo(); self._ensure_frame()
        s13 = self._write_block(r"\subsection*{\textcolor{myPurple}{Eliminar Duplicados}}")
        self.play(Write(s13, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s13)

        # ===== SLIDE 14 =====
        self._ensure_logo(); self._ensure_frame()
        s14 = self._write_block(r"""Todo \textcolor{blue}{\texttt{\textbf{SELECT}}} por defecto regresa todos los registros sin hacer alguna consideración especial. De hecho, la forma “completa” de \textcolor{blue}{\texttt{\textbf{SELECT}}} es \textcolor{blue}{\texttt{\textbf{SELECT}}} \textcolor{gray}{\texttt{\textbf{ALL}}}, pero solemos omitir la palabra \textcolor{gray}{\texttt{\textbf{ALL}}}. Sin embargo, hay ocasiones en las que necesitamos solamente obtener los valores únicos de una columna o una lista de columnas, en este caso sustituiríamos la palabra \textcolor{gray}{\texttt{\textbf{ALL}}} por \textcolor{blue}{\texttt{\textbf{DISTINCT}}}.
        \begin{center}
        \vskip 15pt
        \noindent
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,   % SELECT, DISTINCT, FROM
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries]
        SELECT DISTINCT Color
        FROM SalesLT.Product;
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s14)
        self.play(Write(s14, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s14, rt=0.6)

        # ===== SLIDE 15 =====
        self._ensure_logo(); self._ensure_frame()
        p15 = self._first_existing("Draft_SQL_2.png","ImagesSQL_Slides/Draft_SQL_2.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_2.png","/mnt/data/Draft_SQL_2.png")
        if p15:
            img15 = ImageMobject(p15).set_height(0.62 * config.frame_height)
            cap15 = Tex(r"\texttt{Vista parcial}").next_to(img15, DOWN, buff=0.12)
            g15 = Group(img15, cap15)
            self._fit_group_center(g15)
            g15.shift(0.07*DOWN)
            self.play(FadeIn(img15, shift=DOWN, run_time=0.9))
            self.play(Write(cap15, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g15, rt=0.6)

        # ===== SLIDE 16 =====
        self._ensure_logo(); self._ensure_frame()
        s16 = self._write_block(r"""Al usar \textcolor{blue}{\texttt{\textbf{DISTINCT}}} quitamos los duplicados de una columna o de las combinaciones de valores de varias columnas. Esto quiere decir que \textcolor{blue}{\texttt{\textbf{DISTINCT}}} actúa a un nivel de registro, no de columna. Si tenemos dos columnas, \textcolor{blue}{\texttt{\textbf{DISTINCT}}} va a comparar la combinación de los valores de las columnas por cada registro con todos los demás registros para encontrar los duplicados.
        \begin{center}
        \vskip 15pt
        \noindent

        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,   % SELECT, DISTINCT, FROM
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries]
        SELECT DISTINCT Color, Size
        FROM SalesLT.Product;
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s16)
        self.play(Write(s16, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s16, rt=0.6)

        # ===== SLIDE 17 =====
        self._ensure_logo(); self._ensure_frame()
        p17 = self._first_existing("Draft_SQL_3.png","ImagesSQL_Slides/Draft_SQL_3.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_3.png","/mnt/data/Draft_SQL_3.png")
        if p17:
            img17 = ImageMobject(p17).set_height(0.62 * config.frame_height)
            cap17 = Tex(r"\texttt{Vista parcial}").next_to(img17, DOWN, buff=0.12)
            g17 = Group(img17, cap17)
            self._fit_group_center(g17)
            g17.shift(0.07*DOWN)
            self.play(FadeIn(img17, shift=DOWN, run_time=0.9))
            self.play(Write(cap17, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g17, rt=0.6)

        # ===== SLIDE 18 =====
        self._ensure_logo(); self._ensure_frame()
        s18 = self._write_block(r"\subsection*{\textcolor{myPurple}{\texttt{TOP}}}")
        self.play(Write(s18, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s18)

        # ===== SLIDE 19 =====
        self._ensure_logo(); self._ensure_frame()
        s19 = self._write_block(r"""\textcolor{blue}{\texttt{\textbf{TOP}}} nos permite limitar el número o porcentaje de registros que regresa un \textit{query}. Para usar \textcolor{blue}{\texttt{\textbf{TOP}}} debemos incluirla en la cláusula \textcolor{blue}{\texttt{\textbf{SELECT}}}, especificando el numero o porcentaje de registros deseados, y la podemos usar en conjunto con \textcolor{blue}{\texttt{\textbf{ORDER BY}}} para crear limites ordenados.
        \begin{center}
        \vskip 10pt
        \noindent
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        morekeywords={TOP,WITH,TIES},      % <-- aquí
        emph={Product}, emphstyle=\color{magenta}\bfseries]
        SELECT TOP 10 ProductID, ListPrice as Price
        FROM SalesLT.Product
        ORDER BY Price, StandardCost DESC;
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s19)
        self.play(Write(s19, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s19, rt=0.6)

        # ===== SLIDE 20 =====
        self._ensure_logo(); self._ensure_frame()
        p20 = self._first_existing("Draft_SQL_4.png","ImagesSQL_Slides/Draft_SQL_4.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_4.png","/mnt/data/Draft_SQL_4.png")
        if p20:
            img20 = ImageMobject(p20).set_height(0.62 * config.frame_height)
            cap20 = Tex(r"\texttt{Vista parcial}").next_to(img20, DOWN, buff=0.12)
            g20 = Group(img20, cap20)
            self._fit_group_center(g20)
            g20.shift(0.07*DOWN)
            self.play(FadeIn(img20, shift=DOWN, run_time=0.9))
            self.play(Write(cap20, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g20, rt=0.6)

        # ===== SLIDE 21 =====
        self._ensure_logo(); self._ensure_frame()
        s21 = self._write_block(r"""Otro uso común de \textcolor{blue}{\texttt{\textbf{TOP}}} se da cuando queremos inspeccionar de manera rápida una tabla o un conjunto de columnas de una tabla, pero quizá tenemos muchos registros y no queremos obtener la tabla completa porque tomaría tiempo, así que usamos \textcolor{blue}{\texttt{\textbf{TOP}}} para ayudarnos a dar un vistazo rápido. En este caso, al no usar \textcolor{blue}{\texttt{\textbf{ORDER BY}}}, solo nos arroja los primeros $n$ registros del resultado de un \textit{query} sin un orden especifico.
        \vskip 10PT
        \begin{center}
        \begin{minipage}{0.8\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        morekeywords={TOP,WITH,TIES},      % <-- aquí
        emph={Product}, emphstyle=\color{magenta}\bfseries]
        SELECT TOP 10 *
        FROM SalesLT.Product;
        \end{lstlisting}
        \end{minipage}
        \end{center}""")
        self._fit_group_center(s21)
        self.play(Write(s21, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s21, rt=0.6)

        # ===== SLIDE 22 =====
        self._ensure_logo(); self._ensure_frame()
        s22 = self._write_block(r"""Si al ordenar hay empates (p. ej., mismo precio), \textcolor{blue}{\texttt{\textbf{TOP}}} puede dejar fuera algunas filas empatadas. Se usa \textcolor{blue}{\texttt{\textbf{TOP WITH TIES}}} para incluirlas, en este caso el uso de \textcolor{blue}{\texttt{\textbf{ORDER BY}}} es obligatorio y suele ejecutar un poco más lento.
        \begin{center}
        \vskip 15pt
        \noindent
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        morekeywords={TOP,WITH,TIES},      % <-- aquí
        emph={Product}, emphstyle=\color{magenta}\bfseries]
        SELECT TOP 10 WITH TIES ProductID, ListPrice 
        AS Price
        FROM SalesLT.Product
        ORDER BY Price DESC;
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s22)
        self.play(Write(s22, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s22, rt=0.6)

        # ===== SLIDE 23 =====
        self._ensure_logo(); self._ensure_frame()
        p23 = self._first_existing("Draft_SQL_5.png","ImagesSQL_Slides/Draft_SQL_5.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_5.png","/mnt/data/Draft_SQL_5.png")
        if p23:
            img23 = ImageMobject(p23).set_height(0.62 * config.frame_height)
            cap23 = Tex(r"\texttt{Vista parcial}").next_to(img23, DOWN, buff=0.12)
            g23 = Group(img23, cap23)
            self._fit_group_center(g23)
            g23.shift(0.07*DOWN)
            self.play(FadeIn(img23, shift=DOWN, run_time=0.9))
            self.play(Write(cap23, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g23, rt=0.6)

        # ===== SLIDE 24 =====
        self._ensure_logo(); self._ensure_frame()
        s24 = self._write_block(r"\subsection*{\textcolor{myPurple}{\texttt{ORDER BY} y \texttt{WHERE}}}")
        self.play(Write(s24, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s24)

        # ===== SLIDE 25 =====
        self._ensure_logo(); self._ensure_frame()
        s25 = self._write_block(r"""
        \noindent\begin{minipage}{0.96\linewidth}
        \paragraph{\textcolor{purple}{Cláusula} \textcolor{blue}{\textbf{\texttt{WHERE}}}.}
        Permite filtrar registros según condiciones lógicas. Por ejemplo, si deseamos obtener los modelos de vehículos fabricados en 2025:
        \end{minipage}
        \vskip 10 pt
        \begin{center}
        \begin{minipage}{0.8\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none]
        WHERE Año = 2025
        \end{lstlisting}
        \end{minipage}
        \end{center}

        Los registros que cumplan la condición serán los devueltos por el \textit{\textbf{query}}.""")
        self._fit_group_center(s25)
        self.play(Write(s25, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s25, rt=0.6)

        # ===== SLIDE 26 =====
        self._ensure_logo(); self._ensure_frame()
        s26 = self._write_block(r"""
        \noindent\begin{minipage}{0.96\linewidth}
        \paragraph{\textcolor{purple}{Cláusula} \textcolor{blue}{\texttt{\textbf{ORDER BY}}}.}  
        Ordena el resultado según una o más columnas, de forma ascendente (\textcolor{blue}{\texttt{\textbf{ASC}}}) o descendente (\textcolor{blue}{\texttt{\textbf{DESC}}}). Por defecto \texttt{SQL} no aplica orden, por lo que esta cláusula es necesaria si se requiere una presentación específica.
        \vskip 5PT
        Estas dos cláusulas se pueden visualizar en el siguiente ejemplo:
        \end{minipage}
        \begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,   % SELECT, FROM, WHERE, ORDER BY
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries]
        SELECT ProductID, Name, ListPrice
        FROM SalesLT.Product
        WHERE ListPrice < 1000
        ORDER BY ListPrice DESC;
        \end{lstlisting}
        \end{minipage}
        \end{center}""")
        self._fit_group_center(s26)
        self.play(Write(s26, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s26, rt=0.6)

        # ===== SLIDE 27 =====
        self._ensure_logo(); self._ensure_frame()
        p27 = self._first_existing("Draft_SQL_1.png","ImagesSQL_Slides/Draft_SQL_1.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_1.png","/mnt/data/Draft_SQL_1.png")
        if p27:
            img27 = ImageMobject(p27).set_height(0.62 * config.frame_height)
            cap27 = Tex(r"\texttt{Vista parcial}").next_to(img27, DOWN, buff=0.12)
            g27 = Group(img27, cap27)
            self._fit_group_center(g27)
            g27.shift(0.07*DOWN)
            self.play(FadeIn(img27, shift=DOWN, run_time=0.9))
            self.play(Write(cap27, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g27, rt=0.6)

        # ===== SLIDE 28 =====
        self._ensure_logo(); self._ensure_frame()
        s28 = self._write_block(r"""Esta consulta toma la tabla \texttt{SalesLT.}\texttt{\textcolor{magenta}{\textbf{Product}}}, filtra con \texttt{\textcolor{blue}{\textbf{WHERE}}} \texttt{ListPrice} $< 1000$, selecciona \texttt{\textcolor{blue}{\textbf{SELECT}}} \texttt{ProductID}, \texttt{Name} y \texttt{ListPrice}, y ordena por \texttt{\textcolor{blue}{\textbf{ORDER BY}}} \texttt{ListPrice} \texttt{\textcolor{blue}{\textbf{DESC}}}. El orden lógico es \texttt{\textcolor{blue}{\textbf{FROM}}} $\rightarrow$ \texttt{\textcolor{blue}{\textbf{WHERE}}} $\rightarrow$ \texttt{\textcolor{blue}{\textbf{SELECT}}} $\rightarrow$ \texttt{\textcolor{blue}{\textbf{ORDER BY}}}. """)
        self._fit_group_center(s28)
        self.play(Write(s28, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s28, rt=0.6)

        # ===== SLIDE 29 =====
        self._ensure_logo(); self._ensure_frame()
        s29 = self._write_block(r"\subsection*{\textcolor{myPurple}{Operadores lógicos}}")
        self.play(Write(s29, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s29)

        # ===== SLIDE 30 =====
        self._ensure_logo(); self._ensure_frame()
        s30 = self._write_block(r"""Se puede pensar en \textcolor{blue}{\texttt{\textbf{WHERE}}} como un filtro fila por fila, \textcolor{gray}{\texttt{\textbf{AND}}} pide que todas las condiciones se cumplan. Podemos extraer de la tabla \texttt{SalesLT.Product} las columnas \texttt{ProductID, Name} y \texttt{ListPrice}, pero \textbf{solo} aquellos cuyo precio de lista este entre 500 y 1500:   """)
        self._fit_group_center(s30)
        self.play(Write(s30, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s30, rt=0.6)

        # ===== SLIDE 31 =====
        self._ensure_logo(); self._ensure_frame()
        s31 = self._write_block(r"""\begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,        % SELECT, FROM, WHERE...
        stringstyle=\color{red},
        commentstyle=\color{green!50!black},         % comentario en verde
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,  % tablas en magenta
        emph={[2]AND,OR,NOT}, emphstyle={[2]\color{gray}\bfseries} % operadores lógicos en gris
        ]
        -- Ejemplo usando: AND
        SELECT ProductID, Name, ListPrice
        FROM SalesLT.Product
        WHERE ListPrice >= 500 AND ListPrice <= 1500;
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s31)
        self.play(Write(s31, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s31, rt=0.6)

        # ===== SLIDE 32 =====
        self._ensure_logo(); self._ensure_frame()
        p32 = self._first_existing("Draft_SQL_8.png","ImagesSQL_Slides/Draft_SQL_8.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_8.png","/mnt/data/Draft_SQL_8.png")
        if p32:
            img32 = ImageMobject(p32).set_height(0.62 * config.frame_height)
            cap32 = Tex(r"\texttt{Vista parcial}").next_to(img32, DOWN, buff=0.12)
            g32 = Group(img32, cap32)
            self._fit_group_center(g32)
            g32.shift(0.07*DOWN)
            self.play(FadeIn(img32, shift=DOWN, run_time=0.9))
            self.play(Write(cap32, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g32, rt=0.6)

        # ===== SLIDE 33 =====
        self._ensure_logo(); self._ensure_frame()
        s33 = self._write_block(r"""Por otra parte, \textcolor{gray}{\texttt{\textbf{OR}}} pide que se cumpla al menos una; de la misma tabla, podemos tomar las columnas \texttt{ProductID} y \texttt{Name}, pero únicamente los productos cuyo color sea \texttt{Black} o bien puede ser \texttt{Red}.
        \begin{center}
        \vskip 15pt
        \noindent
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          % SELECT, FROM, WHERE...
        stringstyle=\color{red},                     % 'Black', 'Red'
        commentstyle=\color{green!50!black},         % comentario en verde
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,       % tabla
        emph={[2]AND,OR,NOT}, emphstyle={[2]\color{gray}\bfseries}% operadores lógicos en gris
        ]
        -- Ejemplo usando: OR
        SELECT ProductID, Name
        FROM SalesLT.Product
        WHERE Color = 'Black' OR Color = 'Red';
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s33)
        self.play(Write(s33, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s33, rt=0.6)

        # ===== SLIDE 34 =====
        self._ensure_logo(); self._ensure_frame()
        p34 = self._first_existing("Draft_SQL_9.png","ImagesSQL_Slides/Draft_SQL_9.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_9.png","/mnt/data/Draft_SQL_9.png")
        if p34:
            img34 = ImageMobject(p34).set_height(0.62 * config.frame_height)
            cap34 = Tex(r"\texttt{Vista parcial}").next_to(img34, DOWN, buff=0.12)
            g34 = Group(img34, cap34)
            self._fit_group_center(g34)
            g34.shift(0.07*DOWN)
            self.play(FadeIn(img34, shift=DOWN, run_time=0.9))
            self.play(Write(cap34, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g34, rt=0.6)

        # ===== SLIDE 35 =====
        self._ensure_logo(); self._ensure_frame()
        s35 = self._write_block(r"""Y finalmente, \textcolor{gray}{\texttt{\textbf{NOT}}} niega una condición; usando las mismas columnas del ejemplo anterior, podemos filtrar los productos cuyos colores \textbf{no} sean \texttt{Black} \textbf{o} \texttt{Red}, que es equivalente a filtrar los productos cuyos colores \textbf{no} sean \texttt{Black} \textbf{y} que \textbf{no} sean \texttt{Red}. """)
        self._fit_group_center(s35)
        self.play(Write(s35, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s35, rt=0.6)

        # ===== SLIDE 36 =====
        self._ensure_logo(); self._ensure_frame()
        s36 = self._write_block(r"""\begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          % SELECT, FROM, WHERE...
        stringstyle=\color{red},                     % 'Black', 'Red'
        commentstyle=\color{green!50!black},         % comentario en verde
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,        % tabla
        emph={[2]AND,OR,NOT}, emphstyle={[2]\color{gray}\bfseries} % operadores lógicos en gris
        ]
        -- Ejemplo usando: NOT
        SELECT ProductID, Name
        FROM SalesLT.Product
        WHERE NOT (Color = 'Black' OR Color = 'Red');
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s36)
        self.play(Write(s36, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s36, rt=0.6)

        # ===== SLIDE 37 =====
        self._ensure_logo(); self._ensure_frame()
        p37 = self._first_existing("Draft_SQL_10.png","ImagesSQL_Slides/Draft_SQL_10.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_10.png","/mnt/data/Draft_SQL_10.png")
        if p37:
            img37 = ImageMobject(p37).set_height(0.62 * config.frame_height)
            cap37 = Tex(r"\texttt{Vista parcial}").next_to(img37, DOWN, buff=0.12)
            g37 = Group(img37, cap37)
            self._fit_group_center(g37)
            g37.shift(0.07*DOWN)
            self.play(FadeIn(img37, shift=DOWN, run_time=0.9))
            self.play(Write(cap37, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g37, rt=0.6)

        # ===== SLIDE 38 =====
        self._ensure_logo(); self._ensure_frame()
        s38 = self._write_block(r"""Como se hizo ver en este último caso, estos operadores siguen las leyes de De Morgan:
        \[
        \textcolor{gray}{\texttt{\textbf{NOT}}}\,(A\,\textcolor{gray}{\texttt{\textbf{AND}}}\,B)\ \equiv\ (\textcolor{gray}{\texttt{\textbf{NOT}}}\,A)\,\textcolor{gray}{\texttt{\textbf{OR}}}\,(\textcolor{gray}{\texttt{\textbf{NOT}}}\,B)
        \quad\text{y}\quad
        \textcolor{gray}{\texttt{\textbf{NOT}}}\,(A\,\textcolor{gray}{\texttt{\textbf{OR}}}\,B)\ \equiv\ (\textcolor{gray}{\texttt{\textbf{NOT}}}\,A)\,\textcolor{gray}{\texttt{\textbf{AND}}}\,(\textcolor{gray}{\texttt{\textbf{NOT}}}\,B).
        \]""")
        self._fit_group_center(s38)
        self.play(Write(s38, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s38, rt=0.6)

        # ===== SLIDE 39 =====
        self._ensure_logo(); self._ensure_frame()
        s39 = self._write_block(r"\subsection*{\textcolor{myPurple}{Operadores de comparación}}")
        self.play(Write(s39, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s39)

        # ===== SLIDE 40 =====
        self._ensure_logo(); self._ensure_frame()
        s40 = self._write_block(r"""Los operadores de comparación \texttt{=}, \texttt{<>}, \texttt{<}, \texttt{>}, \texttt{<=}, \texttt{>=}, comparan dos expresiones y producen un valor lógico. Es importante recordar que no podemos realizar comparaciones con un \texttt{\textcolor{gray}{\textbf{NULL}}}.
        \vskip 5pt
        La siguiente tabla ilustra cada descripción de estos operadores: """)
        self._fit_group_center(s40)
        self.play(Write(s40, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s40, rt=0.6)

        # ===== SLIDE 41 =====
        self._ensure_logo(); self._ensure_frame()
        p41 = self._first_existing("TablaOperadores.png","ImagesSQL_Slides/TablaOperadores.png","/home/gustavo/SS/ImagesSQL_Slides/TablaOperadores.png","/mnt/data/TablaOperadores.png")
        if p41:
            img41 = ImageMobject(p41).set_width(0.70 * config.frame_width)
            self._fit_group_center(img41)
            img41.shift(0.07*DOWN)
            self.play(FadeIn(img41, shift=DOWN, run_time=0.9))
            self.wait(3.0)
            self._disappear(img41, rt=0.6)

        # ===== SLIDE 42 =====
        self._ensure_logo(); self._ensure_frame()
        s42 = self._write_block(r"\subsection*{\textcolor{myPurple}{Operadores especiales: \texttt{BETWEEN, IN, LIKE}}}")
        self.play(Write(s42, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s42)

        # ===== SLIDE 43 =====
        self._ensure_logo(); self._ensure_frame()
        s43 = self._write_block(r"""\noindent En \texttt{T-SQL}, \textcolor{gray}{\texttt{\textbf{BETWEEN}}} expresa un rango \emph{inclusivo}: \texttt{x \textcolor{gray}{\texttt{\textbf{BETWEEN}}} a \textcolor{gray}{\texttt{\textbf{AND}}} b} equivale a \texttt{x >= a \textcolor{gray}{\texttt{\textbf{AND}}} x <= b}; funciona con números y fechas, su negación \textcolor{gray}{\texttt{\textbf{NOT BETWEEN}}} selecciona valores fuera del rango, y si interviene \textcolor{gray}{\texttt{\textbf{NULL}}} en la expresión o en los límites el resultado es \textcolor{gray}{\texttt{\textbf{NULL}}} y la fila no pasa el \textcolor{blue}{\texttt{\textbf{WHERE}}}; para un buen rendimiento se aplica directamente sobre la columna y, en fechas, por ser inclusivo, suele preferirse un rango semiabierto con \texttt{>=} y \texttt{<} para no perder registros al final del periodo.  """)
        self._fit_group_center(s43)
        self.play(Write(s43, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s43, rt=0.6)

        # ===== SLIDE 44 =====
        self._ensure_logo(); self._ensure_frame()
        s44 = self._write_block(r"""\begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          % SELECT, FROM, WHERE, ORDER BY...
        stringstyle=\color{red},
        commentstyle=\color{green!50!black},         % comentario en verde
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,             % tabla
        emph={[2]AND,OR,NOT,BETWEEN}, emphstyle={[2]\color{gray}\bfseries} % operadores lógicos / BETWEEN en gris
        ]
        SELECT ProductID, Name, ListPrice
        FROM SalesLT.Product
        WHERE ListPrice BETWEEN 500 AND 1500
        ORDER BY ListPrice;
        \end{lstlisting}
        \end{minipage}
        \end{center}""")
        self._fit_group_center(s44)
        self.play(Write(s44, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s44, rt=0.6)

        # ===== SLIDE 45 =====
        self._ensure_logo(); self._ensure_frame()
        p45 = self._first_existing("Draft_SQL_11.png","ImagesSQL_Slides/Draft_SQL_11.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_11.png","/mnt/data/Draft_SQL_11.png")
        if p45:
            img45 = ImageMobject(p45).set_height(0.62 * config.frame_height)
            cap45 = Tex(r"\texttt{Vista parcial}").next_to(img45, DOWN, buff=0.12)
            g45 = Group(img45, cap45)
            self._fit_group_center(g45)
            g45.shift(0.07*DOWN)
            self.play(FadeIn(img45, shift=DOWN, run_time=0.9))
            self.play(Write(cap45, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g45, rt=0.6)

        # ===== SLIDE 46 =====
        self._ensure_logo(); self._ensure_frame()
        s46 = self._write_block(r"""El operador \textcolor{gray}{\texttt{\textbf{BETWEEN}}} permite filtrar usando un rango de valores, pero \textcolor{gray}{\texttt{\textbf{IN}}} permite filtrar por un conjunto explícito de valores:  \texttt{expr \textcolor{gray}{\texttt{\textbf{IN}}} (v1, v2, v3)} es equivalente a \texttt{expr = v1 \textcolor{gray}{\texttt{\textbf{OR}}} expr = v2 \textcolor{gray}{\texttt{\textbf{OR}}} expr = v3}; el orden y los repetidos en la lista no importan, \textcolor{gray}{\texttt{\textbf{NOT IN}}} selecciona lo que queda fuera y, por la lógica de tres valores, si interviene \textcolor{gray}{\texttt{\textbf{NULL}}} en la expresión o en la lista el resultado puede ser \textcolor{gray}{\texttt{\textbf{NULL}}}. """)
        self._fit_group_center(s46)
        self.play(Write(s46, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s46, rt=0.6)

        # ===== SLIDE 47 =====
        self._ensure_logo(); self._ensure_frame()
        s47 = self._write_block(r"""\begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          % SELECT, FROM, WHERE, ORDER BY...
        stringstyle=\color{red},                     % 'Black', 'Red', 'Silver'
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,              % tabla
        emph={[2]AND,OR,NOT,BETWEEN,IN}, emphstyle={[2]\color{gray}\bfseries} % operadores lógicos, BETWEEN, IN en gris
        ]
        SELECT ProductID, Name, Color, ListPrice
        FROM SalesLT.Product
        WHERE Color IN ('Black', 'Red', 'Silver')
        ORDER BY Color, Name;
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s47)
        self.play(Write(s47, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s47, rt=0.6)

        # ===== SLIDE 48 =====
        self._ensure_logo(); self._ensure_frame()
        p48 = self._first_existing("Draft_SQL_12.png","ImagesSQL_Slides/Draft_SQL_12.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_12.png","/mnt/data/Draft_SQL_12.png")
        if p48:
            img48 = ImageMobject(p48).set_height(0.62 * config.frame_height)
            cap48 = Tex(r"\texttt{Vista parcial}").next_to(img48, DOWN, buff=0.12)
            g48 = Group(img48, cap48)
            self._fit_group_center(g48)
            g48.shift(0.07*DOWN)
            self.play(FadeIn(img48, shift=DOWN, run_time=0.9))
            self.play(Write(cap48, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g48, rt=0.6)

        # ===== SLIDE 49 =====
        self._ensure_logo(); self._ensure_frame()
        s49 = self._write_block(r"""\noindent El operador \textcolor{gray}{\texttt{\textbf{LIKE}}} permite verificar si una cadena coincide con un patrón específico y, aunque cada carácter cuenta, se pueden usar comodines para flexibilizar la búsqueda: el guion bajo \verb|_| representa exactamente un carácter, los corchetes \verb|[...]| definen un conjunto o rango de caracteres válidos y con \verb|[^...]| se niega ese rango, y el signo \verb|%| representa cualquier secuencia de caracteres (incluso vacía) que puede ubicarse antes, después o entre lo que especifiquemos. """)
        self._fit_group_center(s49)
        self.play(Write(s49, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s49, rt=0.6)

        # ===== SLIDE 50 =====
        self._ensure_logo(); self._ensure_frame()
        s50 = self._write_block(r"""\begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          % SELECT, FROM, WHERE...
        stringstyle=\color{red},                     % 'B___'
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,              % tabla
        emph={[2]AND,OR,NOT,BETWEEN,IN,LIKE}, emphstyle={[2]\color{gray}\bfseries} % operadores en gris
        ]
        SELECT ProductID, Color
        FROM SalesLT.Product
        WHERE Color LIKE 'B___';
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s50)
        self.play(Write(s50, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s50, rt=0.6)

        # ===== SLIDE 51 =====
        self._ensure_logo(); self._ensure_frame()
        p51 = self._first_existing("Draft_SQL_13.png","ImagesSQL_Slides/Draft_SQL_13.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_13.png","/mnt/data/Draft_SQL_13.png")
        if p51:
            img51 = ImageMobject(p51).set_height(0.62 * config.frame_height)
            cap51 = Tex(r"\texttt{Vista parcial}").next_to(img51, DOWN, buff=0.12)
            g51 = Group(img51, cap51)
            self._fit_group_center(g51)
            g51.shift(0.07*DOWN)
            self.play(FadeIn(img51, shift=DOWN, run_time=0.9))
            self.play(Write(cap51, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g51, rt=0.6)

        # ===== SLIDE 52 =====
        self._ensure_logo(); self._ensure_frame()
        s52 = self._write_block(r"""\noindent El siguiente \textit{query} utiliza \textcolor{gray}{\texttt{\textbf{LIKE}}} \verb|'[WXYZ]%'| para obtener productos cuyo color comienza con \texttt{W}, \texttt{X}, \texttt{Y} o \texttt{Z}; en la tabla solo coinciden \texttt{White} y \texttt{Yellow}, los únicos colores que cumplen ese rango inicial.
        \vskip 10pt
        \begin{center}
        \begin{minipage}{0.7\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          % SELECT, FROM, WHERE...
        stringstyle=\color{red},                     % '[WXYZ]%'
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,              % tabla
        emph={[2]AND,OR,NOT,BETWEEN,IN,LIKE}, emphstyle={[2]\color{gray}\bfseries} % operadores en gris
        ]
        SELECT ProductID, Color
        FROM SalesLT.Product
        WHERE Color LIKE '[WXYZ]%';
        \end{lstlisting}
        \end{minipage}
        \end{center}""")
        self._fit_group_center(s52)
        self.play(Write(s52, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s52, rt=0.6)

        # ===== SLIDE 53 =====
        self._ensure_logo(); self._ensure_frame()
        s53 = self._write_block(r"""Como en este caso el rango de letras es continuo, en el sentido de que van una detrás de la otra, podemos especificar lo mismo de la siguiente forma: 
        \begin{center}
        \vskip 10pt
        \noindent
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          % SELECT, FROM, WHERE...
        stringstyle=\color{red},                     % '[W-Z]%'
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,              % tabla
        emph={[2]AND,OR,NOT,BETWEEN,IN,LIKE}, emphstyle={[2]\color{gray}\bfseries} % operadores en gris
        ]
        SELECT ProductID, Color
        FROM SalesLT.Product
        WHERE Color LIKE '[W-Z]%';
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s53)
        self.play(Write(s53, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s53, rt=0.6)

        # ===== SLIDE 54 =====
        self._ensure_logo(); self._ensure_frame()
        p54 = self._first_existing("Draft_SQL_14.png","ImagesSQL_Slides/Draft_SQL_14.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_14.png","/mnt/data/Draft_SQL_14.png")
        if p54:
            img54 = ImageMobject(p54).set_height(0.62 * config.frame_height)
            cap54 = Tex(r"\texttt{Vista parcial}").next_to(img54, DOWN, buff=0.12)
            g54 = Group(img54, cap54)
            self._fit_group_center(g54)
            g54.shift(0.07*DOWN)
            self.play(FadeIn(img54, shift=DOWN, run_time=0.9))
            self.play(Write(cap54, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g54, rt=0.6)

        # ===== SLIDE 55 =====
        self._ensure_logo(); self._ensure_frame()
        s55 = self._write_block(r"""\noindent Es importante entender que la especificación del rango actúa por caracteres individuales (por ejemplo, \verb|[a-cdf]| equivale a \{\texttt{a}, \texttt{b}, \texttt{c}, \texttt{d}, \texttt{f}\}) y pueden negarse con \verb|[^...]| para excluirlos; aplicado al ejemplo de colores, \verb|Color| \textcolor{blue}{\texttt{\textbf{LIKE}}} \verb|'[^W-Z]%'| recupera todos los que \emph{no} comienzan con letras del rango W--Z, por lo que desaparecen justo los dos colores mostrados en las consultas anteriores. """)
        self._fit_group_center(s55)
        self.play(Write(s55, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s55, rt=0.6)

        # ===== SLIDE 56 =====
        self._ensure_logo(); self._ensure_frame()
        s56 = self._write_block(r"""\begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          % SELECT, FROM, WHERE...
        stringstyle=\color{red},                     % '[^W-Z]%'
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,              % tabla
        emph={[2]AND,OR,NOT,BETWEEN,IN,LIKE}, emphstyle={[2]\color{gray}\bfseries} % operadores en gris
        ]
        SELECT ProductID, Color
        FROM SalesLT.Product
        WHERE Color LIKE '[^W-Z]%';
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s56)
        self.play(Write(s56, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s56, rt=0.6)

        # ===== SLIDE 57 =====
        self._ensure_logo(); self._ensure_frame()
        p57 = self._first_existing("Draft_SQL_15.png","ImagesSQL_Slides/Draft_SQL_15.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_15.png","/mnt/data/Draft_SQL_15.png")
        if p57:
            img57 = ImageMobject(p57).set_height(0.62 * config.frame_height)
            cap57 = Tex(r"\texttt{Vista parcial}").next_to(img57, DOWN, buff=0.12)
            g57 = Group(img57, cap57)
            self._fit_group_center(g57)
            g57.shift(0.07*DOWN)
            self.play(FadeIn(img57, shift=DOWN, run_time=0.9))
            self.play(Write(cap57, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g57, rt=0.6)

        # ===== SLIDE 58 =====
        self._ensure_logo(); self._ensure_frame()
        s58 = self._write_block(r"""\noindent Si una cadena contiene símbolos que \textcolor{blue}{\texttt{\textbf{LIKE}}} usa como comodines, búsquelos literalmente escapándolos: enciérrelos entre corchetes (\verb|[%]|, \verb|[_]|) o use la cláusula \textcolor{blue}{\texttt{\textbf{ESCAPE}}} para definir un carácter de escape (p. ej., \verb|\|), de modo que \verb|%| y \verb|_| no actúen como comodines; por ejemplo, si tuviéramos una columna llamada \texttt{Disc\_Desc} que describiera descuentos aplicables en los productos de una forma similar a “Descuento de $30\%$ aplicable”, y quisiéramos filtrar los productos con un $15\%$ de descuento, cualquiera de las siguientes dos opciones nos ayudaría a usar el wildcard de signo porcentual en el filtro: """)
        self._fit_group_center(s58)
        self.play(Write(s58, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s58, rt=0.6)

        # ===== SLIDE 59 =====
        self._ensure_logo(); self._ensure_frame()
        s59 = self._write_block(r"""\begin{center}
        \begin{minipage}{0.8\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,
        emph={[2]AND,OR,NOT,BETWEEN,IN,LIKE}, emphstyle={[2]\color{gray}\bfseries},
        emph={[3]ESCAPE}, emphstyle={[3]\color{blue}\bfseries}
        ]
        SELECT SalesOrderID, Disc_Desc
        FROM SalesLT.Product
        WHERE Disc_Desc LIKE '%15[%]%';

        SELECT SalesOrderID, Disc_Desc
        FROM SalesLT.Product
        WHERE Disc_Desc LIKE '%15!%%' ESCAPE '!';
        \end{lstlisting}
        \end{minipage}
        \end{center}""")
        self._fit_group_center(s59)
        self.play(Write(s59, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s59, rt=0.6)

        # ===== SLIDE 60 =====
        self._ensure_logo(); self._ensure_frame()
        s60 = self._write_block(r"""Dentro de un mismo patrón a filtrar con \textcolor{blue}{\texttt{\textbf{LIKE}}} podemos usar varios \text{wildcards}. En el siguiente \text{query} regresamos los productos cuyo número de producto comienza con \verb|“FR-“| seguido de cualquier carácter y luego de cualquier número entre 0 y 5, seguido de cualquier número entre 0 y 2, finalizando con lo que sea que esté delante de este último número. 
        \begin{center}
        \vskip 15pt
        \noindent
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,          % SELECT, FROM, WHERE...
        stringstyle=\color{red},                     % 'FR-_[0-5][0-2]%'
        frame=none, aboveskip=0pt, belowskip=0pt,
        emph={Product}, emphstyle=\color{magenta}\bfseries,               % tabla
        emph={[2]AND,OR,NOT,BETWEEN,IN,LIKE}, emphstyle={[2]\color{gray}\bfseries} % operadores en gris
        ]
        SELECT ProductID, ProductNumber
        FROM SalesLT.Product
        WHERE ProductNumber LIKE 'FR-_[0-5][0-2]%';
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s60)
        self.play(Write(s60, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s60, rt=0.6)

        # ===== SLIDE 61 =====
        self._ensure_logo(); self._ensure_frame()
        p61 = self._first_existing("Draft_SQL_16.png","ImagesSQL_Slides/Draft_SQL_16.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_16.png","/mnt/data/Draft_SQL_16.png")
        if p61:
            img61 = ImageMobject(p61).set_height(0.62 * config.frame_height)
            cap61 = Tex(r"\texttt{Vista parcial}").next_to(img61, DOWN, buff=0.12)
            g61 = Group(img61, cap61)
            self._fit_group_center(g61)
            g61.shift(0.07*DOWN)
            self.play(FadeIn(img61, shift=DOWN, run_time=0.9))
            self.play(Write(cap61, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g61, rt=0.6)

        # ===== SLIDE 62 =====
        self._ensure_logo(); self._ensure_frame()
        s62 = self._write_block(r"\subsection*{\textcolor{myPurple}{Saltando resultados con \texttt{OFFSET-FETCH}}}")
        self.play(Write(s62, run_time=WRITE_MEDIUM_RT)); self.wait(0.2)
        self._disappear(s62)

        # ===== SLIDE 63 =====
        self._ensure_logo(); self._ensure_frame()
        s63 = self._write_block(r"""\textcolor{blue}{\texttt{\textbf{OFFSET-FETCH}}} es una extensión de \textcolor{blue}{\texttt{\textbf{ORDER BY}}} para tomar rangos del resultado ya ordenado. Sirve para cuando no se quieren “los primeros $n$”, sino saltar los primeros $n$ y traer los $m    $ siguientes (p. ej., los productos 11–15 más costosos). """)
        self._fit_group_center(s63)
        self.play(Write(s63, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s63, rt=0.6)

        # ===== SLIDE 64 =====
        self._ensure_logo(); self._ensure_frame()
        s64 = self._write_block(r"""Con \textcolor{blue}{\texttt{\textbf{OFFSET ROWS}}} indicamos el número de registros a omitir, y con \textcolor{blue}{\texttt{
        \textbf{FETCH ROWS}}} el número de registros a obtener. Juntos nos permiten filtrar un rango de registros de acuerdo con nuestras necesidades. Un aspecto interesante es que la palabra \textcolor{blue}{\texttt{\textbf{ROWS}}} puede ir en plural o singular y no afecta nada. """)
        self._fit_group_center(s64)
        self.play(Write(s64, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s64, rt=0.6)

        # ===== SLIDE 65 =====
        self._ensure_logo(); self._ensure_frame()
        s65 = self._write_block(r"""Aún más, \textcolor{blue}{\texttt{\textbf{FETCH}}} va acompañado de \textcolor{blue}{\texttt{\textbf{FIRST}}} o \textcolor{blue}{\texttt{\textbf{NEXT}}}, y sucede lo mismo que con \textcolor{blue}{\texttt{\textbf{ROWS}}}, es decir, es indiferente cuál de los dos usemos, el comportamiento es el mismo. Este detalle con \textcolor{blue}{\texttt{\textbf{ROWS/ROW}}} y \textcolor{blue}{\texttt{\textbf{FIRST/NEXT}}} es para tener compatibilidad con los estándares de la \textit{ANSI}. También, debido a esta compatibilidad, todo \textcolor{blue}{\texttt{\textbf{OFFSET-FETCH}}} debe terminar con la palabra \textcolor{blue}{\texttt{\textbf{ONLY}}}.  """)
        self._fit_group_center(s65)
        self.play(Write(s65, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s65, rt=0.6)

        # ===== SLIDE 66 =====
        self._ensure_logo(); self._ensure_frame()
        s66 = self._write_block(r"""\begin{center}
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,   % SELECT, FROM, ORDER BY...
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        morekeywords={OFFSET,ROWS,FETCH,NEXT,ONLY}, % que también salgan en azul
        emph={Product}, emphstyle=\color{magenta}\bfseries]
        SELECT ProductID, ListPrice AS Price
        FROM SalesLT.Product
        ORDER BY Price, StandardCost DESC
        OFFSET 10 ROWS
        FETCH NEXT 5 ROWS ONLY;
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s66)
        self.play(Write(s66, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s66, rt=0.6)

        # ===== SLIDE 67 =====
        self._ensure_logo(); self._ensure_frame()
        p67 = self._first_existing("Draft_SQL_6.png","ImagesSQL_Slides/Draft_SQL_6.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_6.png","/mnt/data/Draft_SQL_6.png")
        if p67:
            img67 = ImageMobject(p67).set_height(0.62 * config.frame_height)
            cap67 = Tex(r"\texttt{Vista completa}").next_to(img67, DOWN, buff=0.12)
            g67 = Group(img67, cap67)
            self._fit_group_center(g67)
            g67.shift(0.07*DOWN)
            self.play(FadeIn(img67, shift=DOWN, run_time=0.9))
            self.play(Write(cap67, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g67, rt=0.6)

        # ===== SLIDE 68 =====
        self._ensure_logo(); self._ensure_frame()
        s68 = self._write_block(r"""También puede emplearse \textcolor{blue}{\texttt{\textbf{OFFSET}}} sin \textcolor{blue}{\texttt{\textbf{FETCH}}} a fin de recuperar la totalidad de los registros subsiguientes una vez excluidos los $n$ iniciales.
        \vskip 10pt
        \begin{center}
        \noindent
        \begin{minipage}{0.98\linewidth}
        \begin{lstlisting}[language=SQL,
        backgroundcolor=\color{white},
        basicstyle=\fontfamily{pcr}\selectfont\small,
        keywordstyle=\color{blue}\bfseries,   % SELECT, FROM, ORDER BY, DESC
        stringstyle=\color{red},
        frame=none, aboveskip=0pt, belowskip=0pt,
        morekeywords={OFFSET,ROWS},           % para que también salgan en azul
        emph={Product}, emphstyle=\color{magenta}\bfseries]
        SELECT ProductID, ListPrice AS Price
        FROM SalesLT.Product
        ORDER BY Price, StandardCost DESC
        OFFSET 10 ROWS;
        \end{lstlisting}
        \end{minipage}%
        \end{center}""")
        self._fit_group_center(s68)
        self.play(Write(s68, run_time=WRITE_MEDIUM_RT)); self.wait(3.0)
        self._disappear(s68, rt=0.6)

        # ===== SLIDE 69 =====
        self._ensure_logo(); self._ensure_frame()
        p69 = self._first_existing("Draft_SQL_7.png","ImagesSQL_Slides/Draft_SQL_7.png","/home/gustavo/SS/ImagesSQL_Slides/Draft_SQL_7.png","/mnt/data/Draft_SQL_7.png")
        if p69:
            img69 = ImageMobject(p69).set_height(0.62 * config.frame_height)
            cap69 = Tex(r"\texttt{Vista parcial}").next_to(img69, DOWN, buff=0.12)
            g69 = Group(img69, cap69)
            self._fit_group_center(g69)
            g69.shift(0.07*DOWN)
            self.play(FadeIn(img69, shift=DOWN, run_time=0.9))
            self.play(Write(cap69, run_time=WRITE_MEDIUM_RT))
            self.wait(3.0)
            self._disappear(g69, rt=0.6)


# manim -pqh FundamentosSQL.py FundamentosSQL
