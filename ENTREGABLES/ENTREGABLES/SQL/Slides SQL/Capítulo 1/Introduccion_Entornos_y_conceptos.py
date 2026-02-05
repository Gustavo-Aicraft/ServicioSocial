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
\usepackage{multicol}
\usepackage{pifont}
\newcommand{\fileicon}{\ding{114}}

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

TITLE_MAIN = r"\section*{\textcolor{myPurple}{Introducción: Entornos y conceptos}}"

class Introduccion(Scene):
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

        p_footer = self._first_existing(
            "/home/gustavo/SS/ImagesSQL_Slides/(Pie)_Portada_Aicraft.png"
        )
        p_aj = self._first_existing(
            "/home/gustavo/SS/ImagesSQL_Slides/(Ajolote)_Portada_Aicraft.png"
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

        # ===== SLIDE 2  =====
        self._ensure_logo()
        self._ensure_frame()
        s2 = self._write_block(r"\subsection*{\textcolor{myPurple}{Fundamentos de Bases de Datos}}")
        self._appear(s2, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s2)

        # ===== SLIDE 3  =====
        self._ensure_logo()
        self._ensure_frame()

        s3 = self._write_block(r"""
        Una base de datos es un contenedor lógico diseñado para organizar y preservar información de forma estructurada.
        La idea clave es separar \emph{la información} del \emph{lugar físico} donde se guarda: en vez de trabajar con
        archivos sueltos, concentramos los datos bajo un \emph{sistema gestor de bases de datos} (\texttt{DBMS}), que
        proporciona un entorno controlado para almacenarlos y administrarlos.
        """, scale=0.95)
        s3 = _fit(self, s3, w=0.90, h=0.72, down=0.05)

        self._appear(s3, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s3)

        # ===== SLIDE 4  =====
        self._ensure_logo()
        self._ensure_frame()

        s4 = self._write_block(r"""
        En \texttt{SQL Server} (el motor que introduciremos más adelante), ese \texttt{DBMS} incluye componentes que
        mantienen un catálogo de objetos y coordinan el acceso de múltiples usuarios, de modo que la base se comporta
        como un sistema coherente y no como un conjunto de archivos aislados.
        """, scale=0.95)
        s4 = _fit(self, s4, w=0.90, h=0.72, down=0.05)

        self._appear(s4, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s4)

        # ===== SLIDE 5 =====
        self._ensure_logo()
        self._ensure_frame()

        s5 = self._write_block(r"""
        Para representar el mundo real, organizamos la información en tablas: una tabla describe una entidad (por
        ejemplo, Clientes, Productos o Ventas), cada fila representa una ocurrencia concreta y cada columna describe
        un atributo. Este enfoque permite describir la información de manera clara y consultable, y además facilita que
        el modelo crezca sin perder orden cuando el proyecto aumenta en tamaño.
        """, scale=0.95)
        s5 = _fit(self, s5, w=0.90, h=0.72, down=0.05)

        self._appear(s5, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s5)

        # ===== SLIDE 6 =====
        self._ensure_logo()
        self._ensure_frame()

        s6 = self._write_block(r"""
En bases relacionales es normal distribuir la información en varias tablas y conectarlas mediante relaciones. Cuando repetimos los mismos datos muchas veces, se vuelve difícil mantenerlos actualizados y aparecen inconsistencias; en cambio, si organizamos la información en tablas relacionadas, un dato importante se almacena una sola vez y se reutiliza cuando lo necesitamos. Esta idea está detrás del diseño relacional y explica por qué, en sistemas reales, la información se reparte y se integra a nivel lógico.
""")
        s6 = _fit(self, s6, w=0.90, h=0.72, down=0.05)

        self._appear(s6, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s6)

        # ===== SLIDE 7 =====
        self._ensure_logo()
        self._ensure_frame()

        s7 = self._write_block(r"""
Además de datos, una base de datos contiene \emph{objetos} que el \texttt{DBMS} administra para dar orden y funcionalidad. De manera inicial, los más comunes son:
""")
        s7 = _fit(self, s7, w=0.90, h=0.72, down=0.05)

        self._appear(s7, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s7)

        # ===== SLIDE 8 =====
        self._ensure_logo()
        self._ensure_frame()

        s8 = self._write_block(r"""
\begin{itemize}
  \item \textbf{Tablas:} almacenan los datos.
  \item \textbf{Vistas:} guardan una consulta \texttt{SQL} con nombre, para reutilizarla como si fuera una tabla lógica.
  \item \textbf{Procedimientos almacenados:} guardan lógica ejecutable del lado del servidor para realizar tareas recurrentes.
  \item \textbf{Funciones:} encapsulan cálculos o transformaciones reutilizables que pueden integrarse en consultas.
\end{itemize}
""")
        s8 = _fit(self, s8, w=0.90, h=0.72, down=0.05)

        self._appear(s8, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s8)

        # ===== SLIDE 9 =====
        self._ensure_logo()
        self._ensure_frame()

        s9 = self._write_block(r"""
Lo esencial aquí es que estos objetos existen dentro de la base de datos, tienen nombre, se administran y se pueden reutilizar como componentes del sistema.

\medskip
\noindent
Para mantener orden, agrupamos objetos en \emph{esquemas}. Un esquema funciona como un espacio de nombres: ayuda a clasificar y ubicar objetos, y facilita la administración cuando el proyecto ya contiene muchas tablas y definiciones.
""")
        s9 = _fit(self, s9, w=0.90, h=0.72, down=0.05)

        self._appear(s9, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s9)

        # ===== SLIDE 10 =====
        self._ensure_logo()
        self._ensure_frame()

        s10 = self._write_block(r"""
\texttt{SQL} es el lenguaje estándar para comunicarnos con el \texttt{DBMS}: con él definimos estructuras, consultamos información y ejecutamos operaciones. En \texttt{SQL Server} usaremos \texttt{T-SQL} como dialecto principal, pero en esta etapa conviene quedarnos con la idea general: \texttt{SQL} es la interfaz que permite expresar lo que queremos hacer con los datos y delegar al sistema gestor la ejecución de esas acciones.
""")
        s10 = _fit(self, s10, w=0.90, h=0.72, down=0.05)

        self._appear(s10, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s10)

        # ===== SLIDE 11 =====
        self._ensure_logo()
        self._ensure_frame()

        s11 = self._write_block(r"""
En síntesis, una base de datos es un entorno organizado y administrado por un \texttt{DBMS}, donde modelamos información en tablas relacionadas y reutilizamos objetos para trabajar con los datos de manera consistente y ordenada; esto se puede visualizar con el siguiente diagrama.
""")
        s11 = _fit(self, s11, w=0.90, h=0.72, down=0.05)

        self._appear(s11, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s11)

        # ===== SLIDE 12 (Diagrama) =====
        self._ensure_logo()
        self._ensure_frame()

        p_fund1 = self._first_existing(
            "Fundamentos_1.png", "images/Fundamentos_1.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Fundamentos_1.png"
        )

        img12 = ImageMobject(p_fund1) if p_fund1 else None

        if img12:
            img12.scale_to_fit_width(0.90 * config.frame_width)
            g12 = Group(img12)
            g12 = self._fit_group_center(g12, pad_x=1.0, pad_y=1.0)
            g12.shift(0.06 * DOWN)

            self._appear(g12, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g12)
        else:
            s12_fallback = self._write_block(r"\texttt{Fundamentos\_1.png}")
            self._appear(s12_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s12_fallback)


        # ===== SLIDE 13  =====
        self._ensure_logo()
        self._ensure_frame()

        s13 = self._write_block(r"""\subsection*{\textcolor{myPurple}{Fundamentos de SQL}}""")
        self._appear(s13, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s13)

        # ===== SLIDE 14 =====
        self._ensure_logo()
        self._ensure_frame()

        s14 = self._write_block(r"""
\textbf{SQL} son las siglas de  Lenguaje de Consulta Estructurada (\textit{Structured Query Language}), es un tipo de \textbf{\textit{lenguaje declarativo}}  desarrollado por \texttt{IBM} alrededor de 1947 con el propósito de ser usado para administrar y consultar la información almacenada en bases de datos.
""")
        s14 = _fit(self, s14, w=0.90, h=0.72, down=0.05)

        self._appear(s14, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s14)

        # ===== SLIDE 15 =====
        self._ensure_logo()
        self._ensure_frame()

        s15 = self._write_block(r"""
Un lenguaje es \textit{Turing completo} si, en principio, puede expresar cualquier algoritmo computable, siempre que disponga de mecanismos equivalentes a \textbf{decisión} y \textbf{repetición/recursión} (o, de forma equivalente, la capacidad de simular una máquina de \textit{Turing}).
""")
        s15 = _fit(self, s15, w=0.90, h=0.72, down=0.05)

        self._appear(s15, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s15)

        # ===== SLIDE 16 =====
        self._ensure_logo()
        self._ensure_frame()

        s16 = self._write_block(r"""
En este sentido, \texttt{T-SQL} en \texttt{SQL Server} sí puede considerarse \textit{Turing completo} porque, además de las consultas declarativas, incorpora control de flujo (condicionales y bucles), variables y procedimientos, y permite estructurar cómputos iterativos o recursivos dentro del motor; por ello \textit{SQL Server} no solo describe qué resultado se desea, sino que también puede ejecutar lógica algorítmica para automatizar procesos y transformaciones de datos.
""")
        s16 = _fit(self, s16, w=0.90, h=0.72, down=0.05)

        self._appear(s16, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s16)

        # ===== SLIDE 17 =====
        self._ensure_logo()
        self._ensure_frame()

        s17 = self._write_block(r"""
A diferencia de lenguajes populares como los compilados (\texttt{C, C++, Go}, etc.) o los interpretados (\texttt{Python, JavaScript}, etc.), un lenguaje declarativo especifica qué resultado se desea, pero no es de interés como se realiza.
""")
        s17 = _fit(self, s17, w=0.90, h=0.72, down=0.05)

        self._appear(s17, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s17)

        # ===== SLIDE 18 =====
        self._ensure_logo()
        self._ensure_frame()

        s18 = self._write_block(r"""
Supongamos que queremos declarar el resultado deseado, no el procedimiento:
“Ve a la base de datos \textit{Biblioteca}, toma la tabla \textit{Libros} y dame los títulos y autores
de todos los libros de \textit{Matemáticas}.
Esto en SQL se expresa así:
\begin{center}
\begin{minipage}{0.8\linewidth}
\begin{lstlisting}[language=SQL, backgroundcolor=\color{white},
  basicstyle=\fontfamily{pcr}\selectfont\small,
  keywordstyle=\color{blue}\bfseries,
  stringstyle=\color{red},
  frame=none]
SELECT  TITULO, AUTOR
FROM    BIBLIOTECA.LIBROS
WHERE   CATEGORIA='MATEMATICAS'
\end{lstlisting}
\end{minipage}
\end{center}
""")
        s18 = _fit(self, s18, w=0.92, h=0.78, down=0.05)

        self._appear(s18, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s18)

        # ===== SLIDE 19 =====
        self._ensure_logo()
        self._ensure_frame()

        s19 = self._write_block(r"""
A diferencia de lenguajes como \texttt{Python, C++, Java}, donde existe solo un núcleo en general para cada lenguaje, \texttt{SQL} es un lenguaje que tiene distintas versiones, a estas se les suele llamar \textbf{dialectos}, por ejemplo \texttt{PL/SQL, MySQL, PostgreSQL}, etc., aquí se utilizará el dialecto de \texttt{SQL} implementado en los productos y servicios de Microsoft como \texttt{SQL Server} o Azure, el cual es conocido como \texttt{Transact-SQL} o \texttt{T-SQL}.
""")
        s19 = _fit(self, s19, w=0.90, h=0.72, down=0.05)

        self._appear(s19, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s19)

        # ===== SLIDE 20 =====
        self._ensure_logo()
        self._ensure_frame()

        s20 = self._write_block(r"""
En términos generales, \texttt{T-SQL} comparte el núcleo del \texttt{SQL} con otros motores, por lo que muchas ideas y consultas básicas se ven parecidas, pero se diferencia porque incorpora extensiones propias del ecosistema \texttt{SQL Server/Azure}, ciertos objetos temporales, constructos propios del lenguaje y porque muchas rutinas quedan naturalmente atadas a ese motor, de modo que cuando una solución depende de esas extensiones la portabilidad hacia \texttt{PostgreSQL, MySQL} u \texttt{Oracle} deja de ser directa.
""")
        s20 = _fit(self, s20, w=0.90, h=0.72, down=0.05)

        self._appear(s20, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s20)

        # ===== SLIDE 21 =====
        self._ensure_logo()
        self._ensure_frame()

        s21 = self._write_block(r"""
Esa diferencia de plataforma también suele reflejarse en el modo de uso: en \texttt{SQL Server/Azure} es común que la base de datos funcione como una pieza central del sistema, donde se concentra parte importante de la lógica y de operaciones repetibles bajo herramientas y prácticas de Microsoft; 
""")
        s21 = _fit(self, s21, w=0.90, h=0.72, down=0.05)

        self._appear(s21, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s21)

        # ===== SLIDE 22 =====
        self._ensure_logo()
        self._ensure_frame()

        s22 = self._write_block(r"""
en \texttt{MySQL}, por su presencia histórica en aplicaciones web, es frecuente un enfoque más orientado a usar la base como almacén de datos y mover más lógica a la aplicación; en \texttt{PostgreSQL} suele verse un punto intermedio con \textit{tooling} más diverso y arquitecturas más repartidas; y en \texttt{Oracle} es típico un enfoque \textit{enterprise} tradicional donde también se concentra mucha lógica dentro del motor, pero con un ecosistema y prácticas distintas.
""")
        s22 = _fit(self, s22, w=0.90, h=0.72, down=0.05)

        self._appear(s22, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s22)

        # ===== SLIDE 23 =====
        self._ensure_logo()
        self._ensure_frame()

        s23_txt = self._write_block(r"""
Usualmente en una base de datos no tenemos una sola tabla, sino muchas tablas, y cuando estas tablas se relacionan entre sí decimos que son tablas relacionales o que son \textbf{relaciones}.
""")

        p_tablas = self._first_existing(
            "Tablas.png", "images/Tablas.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tablas.png"
        )
        img23 = ImageMobject(p_tablas) if p_tablas else None

        if img23:
            img23.scale_to_fit_width(0.40 * config.frame_width)
            img23.next_to(s23_txt, DOWN, buff=0.25)

            g23 = Group(s23_txt, img23)
            g23 = self._fit_group_center(g23, pad_x=1.0, pad_y=1.0)
            g23.shift(0.06 * DOWN)

            self._appear(g23, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g23)
        else:
            s23 = _fit(self, s23_txt, w=0.90, h=0.72, down=0.05)
            self._appear(s23, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s23)


        # ===== SLIDE 24 =====
        self._ensure_logo()
        self._ensure_frame()

        s24_txt = self._write_block(r"""
Las tablas almacenadas en una base de datos son representaciones de una entidad. Una \textbf{entidad} puede referirse a cualquier cosa como autos, personas, etc. Y resulta que cada tabla debe o debería ser diseñada para contener información de un tipo particular de cosa, o una entidad.
""")

        p_ent = self._first_existing(
            "Entidad.png", "images/Entidad.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Entidad.png"
        )
        img24 = ImageMobject(p_ent) if p_ent else None

        if img24:
            img24.scale_to_fit_width(0.40 * config.frame_width)
            img24.next_to(s24_txt, DOWN, buff=0.25)

            g24 = Group(s24_txt, img24)
            g24 = self._fit_group_center(g24, pad_x=1.0, pad_y=1.0)
            g24.shift(0.06 * DOWN)

            self._appear(g24, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g24)
        else:
            s24 = _fit(self, s24_txt, w=0.90, h=0.72, down=0.05)
            self._appear(s24, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s24)

        # ===== SLIDE 25 =====
        self._ensure_logo()
        self._ensure_frame()

        s25_txt = self._write_block(r"""
Una relación o tabla suele tener dos estructuras básicas que son las columnas y las entradas (o registros). A lo que comúnmente le llamamos columnas también recibe el nombre de \textbf{dominio, atributo o campo,} y cada dominio lo que hace es contener atributos de la entidad de la tabla.
""")

        p_ent25 = self._first_existing(
            "entradas.png", "images/entradas.png",
            "/home/gustavo/SS/ImagesSQL_Slides/entradas.png"
        )
        img25 = ImageMobject(p_ent25) if p_ent25 else None

        if img25:
            img25.scale_to_fit_width(0.30 * config.frame_width)
            img25.next_to(s25_txt, DOWN, buff=0.25)

            g25 = Group(s25_txt, img25)
            g25 = self._fit_group_center(g25, pad_x=1.0, pad_y=1.0)
            g25.shift(0.06 * DOWN)

            self._appear(g25, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g25)
        else:
            s25 = _fit(self, s25_txt, w=0.90, h=0.72, down=0.05)
            self._appear(s25, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s25)

        # ===== SLIDE 26 =====
        self._ensure_logo()
        self._ensure_frame()

        s26 = self._write_block(r"""
Por ejemplo, si nuestra entidad son Personas, la tabla correspondiente podría contener dominios como: ID, Nombre, Edad, entre otros.  Pero no todos los campos son igual de importantes o tienen las mismas características, y el campo más importante en una relación es lo que se conoce como llave primaria (Primary Key).
""")
        s26 = _fit(self, s26, w=0.90, h=0.72, down=0.05)

        self._appear(s26, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s26)

        # ===== SLIDE 27 =====
        self._ensure_logo()
        self._ensure_frame()

        s27 = self._write_block(r"""
Supongamos una tabla llamada \texttt{VENTAS}:
\vskip 5pt
\begin{center}
\begin{tabular}{@{} l l l r @{}}
\hline
\textbf{Id venta} & \textbf{Fecha} & \textbf{Id producto} & \textbf{Cantidad} \\
\hline
\texttt{V001} & 2025-10-24 & \texttt{A10167} & 5 \\
\texttt{V002} & 2025-10-24 & \texttt{A10168} & 2 \\
\hline
\end{tabular}    
\end{center}
\vskip 10pt
\noindent
Aqui la llave primaria es  \textit{Id venta}, ya que es un campo que identifica de manera única al producto. Cuando tomamos la llave primaria de una tabla en otra tabla, esta recibe el nombre de llave foránea (foreign key), en la tabla esta es \textit{Id Producto}.
""")
        s27 = _fit(self, s27, w=0.92, h=0.78, down=0.05)

        self._appear(s27, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s27)

        # ===== SLIDE 28 =====
        self._ensure_logo()
        self._ensure_frame()

        s28 = self._write_block(r"""
El objetivo de tener una base relacional es que no exista duplicación. Así, tenemos una tabla de productos, una tabla de ventas, y para obtener detalles de cada uno de los productos podemos usar la tabla de productos y no es necesario almacenarlos en las de ventas. De esta forma también optimizamos el almacenamiento de datos. Y nuestro objetivo al aprender SQL deberá ser entender cómo funcionan estas relaciones.
""")
        s28 = _fit(self, s28, w=0.90, h=0.72, down=0.05)

        self._appear(s28, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s28)

        # ===== SLIDE 29 =====
        self._ensure_logo()
        self._ensure_frame()

        s29 = self._write_block(r"""
Definidos los conceptos de entidad y relaciones y su estructura podemos entrar a los \textbf{gráficos de entidad-relación}, que nos ayuda a representar gráficamente los enlaces en una base de datos relacional. A continuación, tenemos el gráfico de entidad-relación de la base de datos que usaremos de aquí en adelante.
""")
        s29 = _fit(self, s29, w=0.90, h=0.72, down=0.05)

        self._appear(s29, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s29)

        # ===== SLIDE 30 =====
        self._ensure_logo()
        self._ensure_frame()

        p_evrel = self._first_existing(
            "Entidad_vs_Relacion.png", "images/Entidad_vs_Relacion.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Entidad_vs_Relacion.png"
        )
        img30 = ImageMobject(p_evrel) if p_evrel else None

        if img30:
            img30.scale_to_fit_width(0.70 * config.frame_width)

            g30 = Group(img30)
            g30 = self._fit_group_center(g30, pad_x=1.0, pad_y=1.0)
            g30.shift(0.06 * DOWN)

            self._appear(g30, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g30)
        else:
            s30_fallback = self._write_block(r"\texttt{Entidad\_vs\_Relacion.png}")
            self._appear(s30_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s30_fallback)

        # ===== SLIDE 31 =====
        self._ensure_logo()
        self._ensure_frame()

        s31 = self._write_block(r"""
Este diagrama contiene las relaciones de cada entidad en la base de datos, el esquema al que pertenecen, los campos que contienen, un icono lateral identifica a las llaves primarias y a las llaves foráneas, y se representan las conexiones que existen entre las relaciones, así como la dirección de estas conexiones, en esta representación también se indica mediante iconos circulares el orden de conexión (si es $1:1$, leído uno a uno, o si es $1:n$, o $n:n$).
""")
        s31 = _fit(self, s31, w=0.90, h=0.72, down=0.05)

        self._appear(s31, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s31)

        # ===== SLIDE 32 =====
        self._ensure_logo()
        self._ensure_frame()

        s32 = self._write_block(
            r"""\subsection*{\textcolor{myPurple}{Bases de datos On-premise vs Cloud}}"""
        )
        self._appear(s32, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s32)

        # ===== SLIDE 33 =====
        self._ensure_logo()
        self._ensure_frame()

        s33 = self._write_block(r"""
Cuando comparamos \textit{On-Premise} vs \textit{Cloud}, la diferencia central no está en el lenguaje \textit{SQL} (las consultas siguen siendo esencialmente las mismas), sino en \textit{dónde corre el motor} y \textit{quién administra} la infraestructura. En un esquema \textit{On-Premise} instalamos y operamos SQL Server dentro de nuestra propia infraestructura (PC de desarrollo, servidor local o un clúster interno): definimos la capacidad de \texttt{CPU}/\texttt{RAM}/almacenamiento, aplicamos parches, configuramos respaldos, monitoreamos rendimiento y resolvemos fallas; el control es máximo, pero también la responsabilidad operativa.
""")
        s33 = _fit(self, s33, w=0.90, h=0.72, down=0.05)

        self._appear(s33, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s33)

        # ===== SLIDE 34 =====
        self._ensure_logo()
        self._ensure_frame()

        s34 = self._write_block(r"""
En \textit{Cloud} desplegamos la base de datos en un proveedor de nube (por ejemplo Azure): el motor puede correr como servicio administrado (p.\ ej., Azure SQL Database o Managed Instance) o sobre una máquina virtual; en ambos casos, consumimos infraestructura en centros de datos del proveedor, con la ventaja de aprovisionar recursos más rápido, escalar con mayor flexibilidad y apoyarnos en componentes administrados para alta disponibilidad, respaldos y monitoreo.
""")
        s34 = _fit(self, s34, w=0.90, h=0.72, down=0.05)

        self._appear(s34, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s34)

        # ===== SLIDE 35 =====
        self._ensure_logo()
        self._ensure_frame()

        s35 = self._write_block(r"""
En términos prácticos, \textit{On-Premise} se elige cuando necesitamos control total, restricciones regulatorias o integración local estricta; \textit{Cloud} se prefiere cuando buscamos elasticidad, despliegue ágil y menor carga operativa, pagando por la capacidad y el servicio conforme al uso.
""")
        s35 = _fit(self, s35, w=0.90, h=0.72, down=0.05)

        self._appear(s35, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s35)

        # ===== SLIDE 36  =====
        self._ensure_logo()
        self._ensure_frame()

        s36 = self._write_block(
            r"""\subsection*{\textcolor{myPurple}{Introducción a SQL Server y a Azure}}"""
        )
        self._appear(s36, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s36)

        # ===== SLIDE 37 =====
        self._ensure_logo()
        self._ensure_frame()

        s37 = self._write_block(r"""
SQL Server es un sistema gestor de bases de datos relacionales (\texttt{RDBMS}) de Microsoft diseñado para almacenar, organizar y consultar información de forma segura y eficiente; en la práctica, se puede pensar como un ``motor'' que mantiene datos en tablas (filas y columnas) y nos permite manipularlos con SQL, usando en particular \texttt{T-SQL} (la variante de Microsoft) para operaciones básicas como consultar (\texttt{SELECT}), filtrar (\texttt{WHERE}), ordenar (\texttt{ORDER BY}), agrupar (\texttt{GROUP BY}) y combinar tablas (\texttt{JOIN}), además de definir estructuras (\texttt{CREATE}/\texttt{ALTER}/\texttt{DROP}) y automatizar lógica del lado del servidor (vistas, procedimientos almacenados, funciones). 
""")
        s37 = _fit(self, s37, w=0.90, h=0.72, down=0.05)

        self._appear(s37, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s37)

        # ===== SLIDE 38 =====
        self._ensure_logo()
        self._ensure_frame()

        s38 = self._write_block(r"""
En cuanto a dónde se ejecuta, \texttt{SQL Server} corre como un servicio en un sistema operativo (típicamente Windows Server o Linux) y puede estar instalado en nuestra propia computadora (desarrollo), en un servidor local (\textit{on-premise}) dentro de una organización, o en una máquina virtual; es decir, nosotros controlamos la infraestructura donde vive el motor y, por tanto, también gran parte de su administración (parches, respaldos, capacidad, disponibilidad). 
""")
        s38 = _fit(self, s38, w=0.90, h=0.72, down=0.05)

        self._appear(s38, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s38)

        # ===== SLIDE 39 =====
        self._ensure_logo()
        self._ensure_frame()

        s39 = self._write_block(r"""
Azure, por su parte, es la plataforma de nube de Microsoft y define el entorno donde se ejecutan recursos administrados: en vez de comprar y mantener servidores, se despliegan servicios en centros de datos de Microsoft. 
""")
        s39 = _fit(self, s39, w=0.90, h=0.72, down=0.05)

        self._appear(s39, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s39)

        # ===== SLIDE 40 =====
        self._ensure_logo()
        self._ensure_frame()

        s40 = self._write_block(r"""
En particular, se pueden ejecutar bases de datos con \textit{Azure SQL Database} (la base como servicio) o \textit{Azure SQL Managed Instance} (una instancia administrada con alta compatibilidad), donde el motor corre en infraestructura de Azure y Microsoft se encarga de muchas tareas operativas; alternativamente, si necesitamos control total, podemos ejecutar \textit{SQL Server en una máquina virtual de Azure}, que conceptualmente se parece a \textit{on-premise} pero hospedado en la nube.
""")
        s40 = _fit(self, s40, w=0.90, h=0.72, down=0.05)

        self._appear(s40, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s40)

        # ===== SLIDE 41 =====
        self._ensure_logo()
        self._ensure_frame()

        s41 = self._write_block(r"""
Lo que se debe de entender es que \texttt{SQL Server} es el motor que ejecuta las consultas y mantiene los datos, mientras que Azure es el entorno (nube) donde ese motor puede correr como servicio administrado o como servidor virtual, cambiando principalmente el ``quién administra'' la infraestructura, el escalado y la disponibilidad, el siguiente diagrama ilustra todo lo anterior:
""")
        s41 = _fit(self, s41, w=0.90, h=0.72, down=0.05)

        self._appear(s41, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s41)

        # ===== SLIDE 42 =====
        self._ensure_logo()
        self._ensure_frame()

        p_avs = self._first_existing(
            "AzurevsServer.png", "images/AzurevsServer.png",
            "/home/gustavo/SS/ImagesSQL_Slides/AzurevsServer.png"
        )
        img42 = ImageMobject(p_avs) if p_avs else None

        if img42:
            img42.scale_to_fit_width(0.90 * config.frame_width)

            g42 = Group(img42)
            g42 = self._fit_group_center(g42, pad_x=1.0, pad_y=1.0)
            g42.shift(0.06 * DOWN)

            self._appear(g42, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g42)
        else:
            s42_fallback = self._write_block(r"\texttt{AzurevsServer.png}")
            self._appear(s42_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s42_fallback)

        # ===== SLIDE 43 =====
        self._ensure_logo()
        self._ensure_frame()

        s43 = self._write_block(r"""
Para exponer una base de datos (local o en la nube) de forma controlada, introducimos el concepto de \textit{firewall}: es un conjunto de reglas que decide qué tráfico de red puede entrar o salir, con base en criterios como IP de origen, puerto y protocolo. 
\vskip 5pt
En \texttt{SQL Server}, típicamente trabajamos con el puerto \texttt{1433} (\texttt{TCP}) y el \textit{firewall} actúa como ``la puerta'' que permite o bloquea conexiones; ejemplo, si instalamos \texttt{SQL Server} en un servidor local, configuramos el \textit{firewall} del sistema (y, si aplica, el del perímetro de la red) para permitir \texttt{TCP/1433} solo desde las redes o equipos autorizados. 
""")
        s43 = _fit(self, s43, w=0.90, h=0.72, down=0.05)

        self._appear(s43, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s43)

        # ===== SLIDE 44 =====
        self._ensure_logo()
        self._ensure_frame()

        s44 = self._write_block(r"""
La conexión, en términos simples, ocurre cuando un cliente (p.\ ej., SSMS, Azure Data Studio o una aplicación) abre un canal \texttt{TCP} hacia \texttt{host:puerto}; después de establecerse el canal, se negocia autenticación (credenciales) y, si todo es válido, el motor acepta la sesión y comenzamos a ejecutar consultas. En Azure el concepto es el mismo, pero las reglas suelen gestionarse a nivel del servicio: definimos qué direcciones IP pueden entrar, y el servicio aplica esas restricciones antes de que el motor procese el intento de inicio de sesión; además, es habitual exigir cifrado (\texttt{TLS}) para que las credenciales y los datos viajen protegidos.
""")
        s44 = _fit(self, s44, w=0.90, h=0.72, down=0.05)

        self._appear(s44, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s44)

        # ===== SLIDE 45 =====
        self._ensure_logo()
        self._ensure_frame()

        s45 = self._write_block(r"""
Finalmente, aunque aquí usamos Azure como referencia, el patrón se repite en nubes alternas (\texttt{AWS}, Google Cloud u otras): en todas, desplegamos un servicio de base de datos o una máquina virtual, configuramos reglas de red (firewalls, \textit{security groups}, listas de control), y habilitamos únicamente los puertos y orígenes necesarios; el objetivo operativo es el mismo: permitir conectividad para el trabajo legítimo, minimizando la superficie de ataque.
""")
        s45 = _fit(self, s45, w=0.90, h=0.72, down=0.05)

        self._appear(s45, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s45)

        # ===== SLIDE 46  =====
        self._ensure_logo()
        self._ensure_frame()

        s46 = self._write_block(
            r"""\subsection*{\textcolor{myPurple}{Tipos de Datos en T-SQL}}"""
        )
        self._appear(s46, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s46)

        # ===== SLIDE 47 =====
        self._ensure_logo()
        self._ensure_frame()

        s47 = self._write_block(r"""
Existen dos tipos de datos, los estructurados y no estructurados. Los datos estructurados son todos aquellos tipos de datos que se encuentran definidos de manera clara y concisa, con un formato estandarizado, presentando un patrón u orden entre ellos de tal manera que son fáciles de organizar y de consultar, tanto por humanos como por maquinas (p. ej., nombres, números de teléfono, códigos postales).
""")
        s47 = _fit(self, s47, w=0.90, h=0.72, down=0.05)

        self._appear(s47, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s47)

        # ===== SLIDE 48 =====
        self._ensure_logo()
        self._ensure_frame()

        s48 = self._write_block(r"""
Los datos estructurados suelen ser almacenados en bases de datos relacionales, y son accesibles usando SQL.\\
Por otro lado, todo lo que no entra en la definición anterior suele ser considerado como datos no estructurados (p. ej., texto, audio, imagen). Existe una clasificación intermedia llamada datos semiestructurados (p. ej., \texttt{JSON, XML, HTML})
""")
        s48 = _fit(self, s48, w=0.90, h=0.72, down=0.05)

        self._appear(s48, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s48)

        # ===== SLIDE 49 =====
        self._ensure_logo()
        self._ensure_frame()

        s49 = self._write_block(r"""
Tanto los datos no estructurados como los semiestructurados suelen ser almacenados en un tipo de base de datos no relacional, entre estas se encuentras las bases que trabajan con el llamado \texttt{NoSQL}. Las bases \texttt{NoSQL} no realizan una organización separada de datos, y suelen ser usadas cuando los datos no pueden ser encapsulados en tablas estructuradas, y no pueden ser consultados o mostrados de manera simple. En adelante, se trabajará con los datos estructurados.
""")
        s49 = _fit(self, s49, w=0.90, h=0.72, down=0.05)

        self._appear(s49, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s49)

        # ===== SLIDE 50 =====
        self._ensure_logo()
        self._ensure_frame()

        s50 = self._write_block(r"""
Los datos estructurados suelen tener muchas clasificaciones, por lo cual es crucial tener bien definidos los tipos de datos con los que se esten trabajando para optimizar procesos, servicios, tiempo y sistemas.\\
El tipo de datos es quizá la restricción o \textit{constraint} más fundamental de nuestros datos y tablas. La siguiente tabla muestra algunos de los tipos de datos que se tienen en T-SQL y su clasificación:
""")
        s50 = _fit(self, s50, w=0.90, h=0.72, down=0.05)

        self._appear(s50, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s50)

        # ===== SLIDE 51  =====
        self._ensure_logo()
        self._ensure_frame()

        p_ttd = self._first_existing(
            "TablaTiposDeDatos.png", "images/TablaTiposDeDatos.png",
            "/home/gustavo/SS/ImagesSQL_Slides/TablaTiposDeDatos.png"
        )
        img51 = ImageMobject(p_ttd) if p_ttd else None

        if img51:
            img51.scale_to_fit_width(0.90 * config.frame_width)

            g51 = Group(img51)
            g51 = self._fit_group_center(g51, pad_x=1.0, pad_y=1.0)
            g51.shift(0.06 * DOWN)

            self._appear(g51, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g51)
        else:
            s51_fallback = self._write_block(r"\texttt{TablaTiposDeDatos.png}")
            self._appear(s51_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s51_fallback)

        # ===== SLIDE 52 =====
        self._ensure_logo()
        self._ensure_frame()

        s52 = self._write_block(r"""
Los datos numéricos permiten distinguir entre valores \textbf{exactos} (enteros y decimales) y \textbf{aproximados} (flotantes). Los tipos exactos incluyen \textcolor{blue}{tinyint}, \textcolor{blue}{smallint}, \textcolor{blue}{int}, \textcolor{blue}{bigint} y \textcolor{blue}{decimal/numeric(p,s)}, usados cuando se conoce la cantidad de decimales con precisión; los monetarios (\textcolor{blue}{money}, \textcolor{blue}{smallmoney}) también son exactos. En cambio, \textcolor{blue}{float} y \textcolor{blue}{real} se emplean cuando los decimales pueden variar o los datos provienen de mediciones.
""")
        s52 = _fit(self, s52, w=0.90, h=0.72, down=0.05)

        self._appear(s52, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s52)

        # ===== SLIDE 53 =====
        self._ensure_logo()
        self._ensure_frame()

        s53 = self._write_block(r"""
El tipo entero varía según el rango y el espacio de almacenamiento necesario: \textcolor{blue}{tinyint} (0--255), \textcolor{blue}{smallint} ($-32,768, 32,767$), \textcolor{blue}{int} ($-2^{31},2^{31}-1$) y \textcolor{blue}{bigint} ($- 2^{63},2^{63}-1$). Los datos de tipo decimal o \textcolor{blue}{numeric} permiten precisión definida mediante \textcolor{blue}{(p,s)}, donde \textcolor{purple}{p} indica la cantidad total de dígitos (máximo 38) e incluye tanto a los números a la derecha como a la izquierda del punto decimal 
""")
        s53 = _fit(self, s53, w=0.90, h=0.72, down=0.05)

        self._appear(s53, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s53)

        # ===== SLIDE 54 =====
        self._ensure_logo()
        self._ensure_frame()

        s54 = self._write_block(r"""
y \textcolor{purple}{s} son los decimales a la derecha del punto decimal; el valor de \textcolor{purple}{s} se le resta a \textcolor{purple}{p} para determinar el número de dígitos máximo que irá a la izquierda del punto decimal, y siempre se cumple que $0 \leq s \leq p $. Cuando se usa su precisión máxima, un numeric puede tomar valores entre $10^{38}$ hasta $10^{38}-1$.
""")
        s54 = _fit(self, s54, w=0.90, h=0.72, down=0.05)

        self._appear(s54, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s54)

        # ===== SLIDE 55 =====
        self._ensure_logo()
        self._ensure_frame()

        s55 = self._write_block(r"""
Los tipos de datos de \textbf{caracteres} (\textcolor{blue}{char}, \textcolor{blue}{varchar}, \textcolor{blue}{nchar}, \textcolor{blue}{nvarchar}) almacenan texto; los prefijos \textcolor{purple}{var} y \textcolor{purple}{n} indican caracteres variables en un rango y el largo del dato en bytes, respectivamente.

\noindent
En los \textbf{datos de fecha y hora}, SQL ofrece \textcolor{blue}{date}, \textcolor{blue}{time}, \textcolor{blue}{smalldatetime}, \textcolor{blue}{datetime}, \textcolor{blue}{datetime2} (con mayor rango y precisión) y \textcolor{blue}{datetimeoffset} (incluye zona horaria).
""")
        s55 = _fit(self, s55, w=0.90, h=0.76, down=0.05)

        self._appear(s55, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s55)

        # ===== SLIDE 56 =====
        self._ensure_logo()
        self._ensure_frame()

        p_tipos = self._first_existing(
            "Tipos de Datos.png", "images/Tipos de Datos.png",
            "/home/gustavo/SS/ImagesSQL_Slides/Tipos de Datos.png"
        )
        img56 = ImageMobject(p_tipos) if p_tipos else None

        if img56:
            img56.scale_to_fit_width(0.70 * config.frame_width)

            g56 = Group(img56)
            g56 = self._fit_group_center(g56, pad_x=1.0, pad_y=1.0)
            g56.shift(0.06 * DOWN)

            self._appear(g56, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g56)
        else:
            s56_fallback = self._write_block(r"\texttt{Tipos de Datos.png}")
            self._appear(s56_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s56_fallback)

        # ===== SLIDE 57 =====
        self._ensure_logo()
        self._ensure_frame()

        s57 = self._write_block(r"""
SQL Server también soporta tipos menos comunes como \textcolor{blue}{binarios}, \textcolor{blue}{XML}, \textcolor{blue}{geográficos}. Comprender las diferencias y compatibilidades entre tipos permite saber cuándo usar cada uno, evita errores y mejora el rendimiento optimizando tanto la estructura como la eficiencia de las bases de datos.
""")
        s57 = _fit(self, s57, w=0.90, h=0.72, down=0.05)

        self._appear(s57, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s57)

        # ===== SLIDE 58 =====
        self._ensure_logo()
        self._ensure_frame()

        s58 = self._write_block(
            r"""\subsection*{\textcolor{myPurple}{Instalación de \texttt{SQL Server} y Carga de Base de Datos}}"""
        )
        self._appear(s58, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s58)

        # ===== SLIDE 59 =====
        self._ensure_logo()
        self._ensure_frame()

        s59 = self._write_block(r"""
Para poder visualizar la teoría, ejecutar ejemplos y realizar ejercicios de los siguientes capítulos será necesario tener instalado un motor de base de datos,  y un ambiente que nos permita interactuar con este motor usando códigos de \texttt{SQL}.
""")
        s59 = _fit(self, s59, w=0.90, h=0.72, down=0.05)

        self._appear(s59, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s59)

        # ===== SLIDE 60 =====
        self._ensure_logo()
        self._ensure_frame()

        s60 = self._write_block(r"""
Para el motor de bases de datos, usaremos \texttt{SQL Server} (el sistema de administración de bases de datos relacionales de Microsoft) y para ello instalaremos una versión de este motor en nuestra computadora, pero otra opción sería usar \texttt{Azure SQL Database}. Por otro lado, la interfaz o ambiente que se usará es \texttt{SQL Server Management Studio}.
""")
        s60 = _fit(self, s60, w=0.90, h=0.72, down=0.05)

        self._appear(s60, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s60)

        # ===== SLIDE 61 =====
        self._ensure_logo()
        self._ensure_frame()

        s61 = self._write_block(r"""
Si no se esta usando una computadora con Windows, para poder realizar estas instalaciones se deberá usar una instancia virtual de Windows con softwares como \texttt{Parallels}, u optar por una interfaz de usuario gráfica de terceros para \texttt{SQL Server}, por ejemplo, \texttt{Talend Open Studio for Data Integration}.
\vskip 5pt
\texttt{SQL Server} puede ser descargado en una versión gratuita, para ello simplemente se puede buscar \textit{"Descargar SQL Server"}, lo cual nos llevará a la página inicial de esta instancia de Microsoft:
""")
        s61 = _fit(self, s61, w=0.90, h=0.76, down=0.05)

        self._appear(s61, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s61)

        # ===== SLIDE 62  =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins1 = self._first_existing(
            "InstalacionSQLserver_1.png", "images/InstalacionSQLserver_1.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_1.png"
        )
        img62 = ImageMobject(p_ins1) if p_ins1 else None

        if img62:
            img62.scale_to_fit_width(0.60 * config.frame_width)

            g62 = Group(img62)
            g62 = self._fit_group_center(g62, pad_x=1.0, pad_y=1.0)
            g62.shift(0.06 * DOWN)

            self._appear(g62, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g62)
        else:
            s62_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_1.png}")
            self._appear(s62_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s62_fallback)

        # ===== SLIDE 63 =====
        self._ensure_logo()
        self._ensure_frame()

        s63 = self._write_block(r"""
Es importante mencionar que al momento de elaboración de este curso, la versión mas actualizada de \texttt{SQL Server} es la \texttt{2025}, la cual puede variar cuando se consulte este curso, pero la dinámica sigue siendo la misma para la instalación del motor de Microsoft.
""")
        s63 = _fit(self, s63, w=0.90, h=0.72, down=0.05)

        self._appear(s63, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s63)

        # ===== SLIDE 64 =====
        self._ensure_logo()
        self._ensure_frame()

        s64 = self._write_block(r"""
Se nos presentaran varias opciones opciones, las primeras dos (de izquierda a derecha) son versiones industriales que podemos descargar y tener un periodo de evaluación gratuita. Pero también, tenemos versiones totalmente gratuitas, una dedicada a desarrolladores y una versión llamada \texttt{SQL Server Express} que es más general, esta última versión es la que suelen usar los principiantes, y es la que descargaremos.
""")
        s64 = _fit(self, s64, w=0.90, h=0.72, down=0.05)

        self._appear(s64, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s64)

        # ===== SLIDE 65 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins2 = self._first_existing(
            "InstalacionSQLserver_2.png", "images/InstalacionSQLserver_2.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_2.png"
        )
        img65 = ImageMobject(p_ins2) if p_ins2 else None

        if img65:
            img65.scale_to_fit_width(0.70 * config.frame_width)

            g65 = Group(img65)
            g65 = self._fit_group_center(g65, pad_x=1.0, pad_y=1.0)
            g65.shift(0.06 * DOWN)

            self._appear(g65, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g65)
        else:
            s65_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_2.png}")
            self._appear(s65_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s65_fallback)

        # ===== SLIDE 66 =====
        self._ensure_logo()
        self._ensure_frame()

        s66 = self._write_block(r"""
Aunque igualmente podríamos decidir instalar la versión de desarrollador sin problema, lo único diferente será que esta versión tendrá algunas características y aplicaciones extra.
\vskip 5pt
Al descargar esta versión, abriremos el archivo \texttt{.exe} y a continuación elegiremos la instalación personalizada.
""")
        s66 = _fit(self, s66, w=0.90, h=0.76, down=0.05)

        self._appear(s66, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s66)

        # ===== SLIDE 67  =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins3 = self._first_existing(
            "InstalacionSQLserver_3.png", "images/InstalacionSQLserver_3.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_3.png"
        )
        img67 = ImageMobject(p_ins3) if p_ins3 else None

        if img67:
            img67.scale_to_fit_width(0.50 * config.frame_width)

            g67 = Group(img67)
            g67 = self._fit_group_center(g67, pad_x=1.0, pad_y=1.0)
            g67.shift(0.06 * DOWN)

            self._appear(g67, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g67)
        else:
            s67_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_3.png}")
            self._appear(s67_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s67_fallback)

        # ===== SLIDE 68 =====
        self._ensure_logo()
        self._ensure_frame()

        s68 = self._write_block(r"""
Una vez instalada, iremos a la carpeta donde se instalaron nuestros archivos y abriremos \texttt{SQL Server Installation Center}, o también lo podemos abrir usando el buscador de Windows. Iremos a la sección de Instalación, y seleccionaremos la primera opción (\texttt{New SQL Server standalone installation or add features to an existing installation}) para comenzar una nueva instalación de \texttt{SQL Server}.
""")
        s68 = _fit(self, s68, w=0.90, h=0.76, down=0.05)

        self._appear(s68, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s68)

        # ===== SLIDE 69 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins4 = self._first_existing(
            "InstalacionSQLserver_4.png", "images/InstalacionSQLserver_4.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_4.png"
        )
        img69 = ImageMobject(p_ins4) if p_ins4 else None

        if img69:
            img69.scale_to_fit_width(0.60 * config.frame_width)

            g69 = Group(img69)
            g69 = self._fit_group_center(g69, pad_x=1.0, pad_y=1.0)
            g69.shift(0.06 * DOWN)

            self._appear(g69, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g69)
        else:
            s69_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_4.png}")
            self._appear(s69_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s69_fallback)

        # ===== SLIDE 70 =====
        self._ensure_logo()
        self._ensure_frame()

        s70 = self._write_block(r"""
Aceptaremos la licencia, y a continuación se hará una corroboración y descarga de archivos, y una revisión de reglas, en esta parte suele saltar una alerta del \textit{firewall} de Windows, pero no hay de que preocuparse.
""")
        s70 = _fit(self, s70, w=0.90, h=0.72, down=0.05)

        self._appear(s70, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s70)

        # ===== SLIDE 71 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins5 = self._first_existing(
            "InstalacionSQLserver_5.png", "images/InstalacionSQLserver_5.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_5.png"
        )
        img71 = ImageMobject(p_ins5) if p_ins5 else None

        if img71:
            img71.scale_to_fit_width(0.60 * config.frame_width)

            g71 = Group(img71)
            g71 = self._fit_group_center(g71, pad_x=1.0, pad_y=1.0)
            g71.shift(0.06 * DOWN)

            self._appear(g71, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g71)
        else:
            s71_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_5.png}")
            self._appear(s71_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s71_fallback)

        # ===== SLIDE 72 =====
        self._ensure_logo()
        self._ensure_frame()

        s72 = self._write_block(r"""
Al continuar, nos aparecerá la siguiente pantalla, en donde nos pide una cuenta de Azure, aquí tendremos que crear una de manera gratuita:
""")
        s72 = _fit(self, s72, w=0.90, h=0.72, down=0.05)

        self._appear(s72, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s72)

        # ===== SLIDE 72 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins6 = self._first_existing(
            "InstalacionSQLserver_6.png", "images/InstalacionSQLserver_6.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_6.png"
        )
        img72 = ImageMobject(p_ins6) if p_ins6 else None

        if img72:
            img72.scale_to_fit_width(0.50 * config.frame_width)

            g72 = Group(img72)
            g72 = self._fit_group_center(g72, pad_x=1.0, pad_y=1.0)
            g72.shift(0.06 * DOWN)

            self._appear(g72, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g72)
        else:
            s72_fallback2 = self._write_block(r"\texttt{InstalacionSQLserver\_6.png}")
            self._appear(s72_fallback2, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s72_fallback2)

        # ===== SLIDE 73 =====
        self._ensure_logo()
        self._ensure_frame()

        s73 = self._write_block(r"""
A continuación, tendremos 3 pasos para crear una cuenta, el primero es agregar datos personales, una cuenta de Microsoft (e.g. Outlook) que no haya tenido previamente una suscripción de Azure y el segundo aceptar los términos y condiciones de Azure, en el tercero tendremos que ingresar los datos de una tarjeta de crédito o débito, esto es \textbf{únicamente} para verificar la identidad del usuario, es decir no generará cargos a menos que hagamos una acción para cambiar a una cuenta de pago por uso (\textit{pay-as-you-go}), lo cual no hará falta para los propósitos del curso.
""")
        s73 = _fit(self, s73, w=0.90, h=0.76, down=0.05)

        self._appear(s73, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s73)

        # ===== SLIDE 74 =====
        self._ensure_logo()
        self._ensure_frame()

        s74 = self._write_block(r"""
Esta oferta nos otorgará \$ 200 de créditos Azure para poder usados durante 30 días, y nos permitirá usar servicios seleccionados durante 12 meses.
""")
        s74 = _fit(self, s74, w=0.90, h=0.72, down=0.05)

        self._appear(s74, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s74)

        # ===== SLIDE 75 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins7 = self._first_existing(
            "InstalacionSQLserver_7.png", "images/InstalacionSQLserver_7.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_7.png"
        )
        img75 = ImageMobject(p_ins7) if p_ins7 else None

        if img75:
            img75.scale_to_fit_width(0.60 * config.frame_width)

            g75 = Group(img75)
            g75 = self._fit_group_center(g75, pad_x=1.0, pad_y=1.0)
            g75.shift(0.06 * DOWN)

            self._appear(g75, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g75)
        else:
            s75_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_7.png}")
            self._appear(s75_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s75_fallback)

        # ===== SLIDE 76 =====
        self._ensure_logo()
        self._ensure_frame()

        s76 = self._write_block(r"""
Sin embargo existe otra opción si se tiene un estatus de estudiante universitario a tiempo completo o de secundaria/bachillerato y con este un correo institucional, en este caso para crear una cuenta de Azure no se requiere tarjeta de crédito o débito.
\vskip 5pt
En este caso debemos crear la cuenta de Azure por fuera del proceso de instalación de \texttt{SQL Server}, simplemente debemos buscar \textit{"Azure for Students"} en el navegador y vamos a llegar a la siguiente página:
""")
        s76 = _fit(self, s76, w=0.90, h=0.78, down=0.05)

        self._appear(s76, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s76)

        # ===== SLIDE 77 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins8 = self._first_existing(
            "InstalacionSQLserver_8.png", "images/InstalacionSQLserver_8.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_8.png"
        )
        img77 = ImageMobject(p_ins8) if p_ins8 else None

        if img77:
            img77.scale_to_fit_width(0.70 * config.frame_width)

            g77 = Group(img77)
            g77 = self._fit_group_center(g77, pad_x=1.0, pad_y=1.0)
            g77.shift(0.06 * DOWN)

            self._appear(g77, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g77)
        else:
            s77_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_8.png}")
            self._appear(s77_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s77_fallback)

        # ===== SLIDE 78 =====
        self._ensure_logo()
        self._ensure_frame()

        s78 = self._write_block(r"""
Los beneficios que se tienen se muestran abajo de esta misma página, es importante señalar que en ambos casos se validará el estatus de estudiante mediante un formulario:
""")
        s78 = _fit(self, s78, w=0.90, h=0.72, down=0.05)

        self._appear(s78, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s78)

        # ===== SLIDE 79  =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins9 = self._first_existing(
            "InstalacionSQLserver_9.png", "images/InstalacionSQLserver_9.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_9.png"
        )
        img79 = ImageMobject(p_ins9) if p_ins9 else None

        if img79:
            img79.scale_to_fit_width(1.00 * config.frame_width)

            g79 = Group(img79)
            g79 = self._fit_group_center(g79, pad_x=1.0, pad_y=1.0)
            g79.shift(0.06 * DOWN)

            self._appear(g79, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g79)
        else:
            s79_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_9.png}")
            self._appear(s79_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s79_fallback)

        # ===== SLIDE 80 =====
        self._ensure_logo()
        self._ensure_frame()

        s80 = self._write_block(r"""
Hay otras ofertas disponibles para usar Azure, sea como prueba o con una suscripción pagada, por ejemplo, hay una prueba disponible para aquellos que sean parte del Gobierno de los Estados Unidos, o cuentas donde solo pagas lo que consumes. Pero los casos más comunes de pruebas gratuitas son los dos que mencionamos, en cualquier caso, para los propósitos de este curso será suficiente con alguna de estas dos cuentas, pues usaremos servicios que otorgan de forma gratuita durante el periodo total de la prueba correspondiente.
""")
        s80 = _fit(self, s80, w=0.90, h=0.78, down=0.05)

        self._appear(s80, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s80)

        # ===== SLIDE 81 =====
        self._ensure_logo()
        self._ensure_frame()

        s81 = self._write_block(r"""
Una vez creada una cuenta gratuita usando cualquiera de las dos opciones anteriores, regresamos al proceso de instalación, en el cual debemos ingresar la cuenta de Azure que tengamos registrada en el campo de \texttt{Use Azure Login}, después aparecerá una pestaña para ingresar los datos de la cuenta:
""")
        s81 = _fit(self, s81, w=0.90, h=0.74, down=0.05)

        self._appear(s81, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s81)

        # ===== SLIDE 82 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins10 = self._first_existing(
            "InstalacionSQLserver_10.png", "images/InstalacionSQLserver_10.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_10.png"
        )
        img82 = ImageMobject(p_ins10) if p_ins10 else None

        if img82:
            img82.scale_to_fit_width(0.60 * config.frame_width)

            g82 = Group(img82)
            g82 = self._fit_group_center(g82, pad_x=1.0, pad_y=1.0)
            g82.shift(0.06 * DOWN)

            self._appear(g82, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g82)
        else:
            s82_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_10.png}")
            self._appear(s82_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s82_fallback)

        # ===== SLIDE 83 =====
        self._ensure_logo()
        self._ensure_frame()

        s83 = self._write_block(r"""
Continuaremos hasta la ventana \texttt{Feature Selection}, habrá algunas características compartidas ya seleccionadas, esas las dejaremos de acuerdo con la selección por defecto, pero en nuestro caso lo más importante es instalar \texttt{Database Engine Services}, así que seleccionaremos esta opción, y otras dos más:
""")
        s83 = _fit(self, s83, w=0.90, h=0.74, down=0.05)

        self._appear(s83, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s83)

        # ===== SLIDE 84 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins11 = self._first_existing(
            "InstalacionSQLserver_11.png", "images/InstalacionSQLserver_11.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_11.png"
        )
        img84 = ImageMobject(p_ins11) if p_ins11 else None

        if img84:
            img84.scale_to_fit_width(0.60 * config.frame_width)

            g84 = Group(img84)
            g84 = self._fit_group_center(g84, pad_x=1.0, pad_y=1.0)
            g84.shift(0.06 * DOWN)

            self._appear(g84, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g84)
        else:
            s84_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_11.png}")
            self._appear(s84_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s84_fallback)

        # ===== SLIDE 85 =====
        self._ensure_logo()
        self._ensure_frame()

        s85 = self._write_block(r"""
La siguiente ventana nos permitirá configurar nuestra instancia de \texttt{SQL Server}, elegiremos la configuración por defecto.
""")
        s85 = _fit(self, s85, w=0.90, h=0.72, down=0.05)

        self._appear(s85, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s85)

        # ===== SLIDE 86 =====
        self._ensure_logo()
        self._ensure_frame()

        s86 = self._write_block(r"""
La siguiente ventana será \texttt{Server Configuration}, aquí dejaremos la configuración por defecto y daremos en continuar.
\vskip 5pt
Continuaremos hasta la ventana \texttt{Database Engine Configuration}, aquí configuraremos nuestro método para acceder al motor de base de datos, para esto seleccionaremos \texttt{Windows authentication mode} y \texttt{Add Current User}, y con esto podremos acceder usando nuestro usuario de Windows. Una vez agregado nuestro usuario de Windows podemos continuar. Si quisiéramos establecer una contraseña propia, podríamos usarlo seleccionando la opción \texttt{Mixed Mode}.
""")
        s86 = _fit(self, s86, w=0.90, h=0.80, down=0.05)

        self._appear(s86, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s86)

        # ===== SLIDE 87  =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins13 = self._first_existing(
            "InstalacionSQLserver_13.png", "images/InstalacionSQLserver_13.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_13.png"
        )
        img87 = ImageMobject(p_ins13) if p_ins13 else None

        if img87:
            img87.scale_to_fit_width(0.60 * config.frame_width)

            g87 = Group(img87)
            g87 = self._fit_group_center(g87, pad_x=1.0, pad_y=1.0)
            g87.shift(0.06 * DOWN)

            self._appear(g87, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g87)
        else:
            s87_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_13.png}")
            self._appear(s87_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s87_fallback)

        # ===== SLIDE 88 =====
        self._ensure_logo()
        self._ensure_frame()

        s88 = self._write_block(r"""
Esperamos a que finalice la instalación y con esto ya tendremos el motor de bases de datos instalado. Lo que haremos ahora será instalar una interfaz gráfica para poder interactuar con este motor de base de datos. Para esto hay ciertos productos que podríamos usar, por ejemplo, \texttt{Visual Studio}, pero en nuestro caso usaremos \texttt{SQL Server Management Studio (SSMS)}, que es un producto de Microsoft capaz de trabajar tanto con \texttt{SQL Server} o como \texttt{Azure SQL Database}, que son las dos principales formas de trabajar con bases de datos en lo que respecta a los productos y servicios de Microsoft.
""")
        s88 = _fit(self, s88, w=0.90, h=0.80, down=0.05)

        self._appear(s88, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s88)

        # ===== SLIDE 89 =====
        self._ensure_logo()
        self._ensure_frame()

        s89 = self._write_block(r"""
Iremos a la pantalla inicial, y seleccionaremos \texttt{Install SQL Server Management Tools}, y se nos abrirá la página para descargar \texttt{SSMS}.
""")
        s89 = _fit(self, s89, w=0.90, h=0.72, down=0.05)

        self._appear(s89, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s89)

        # ===== SLIDE 90  =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins14 = self._first_existing(
            "InstalacionSQLserver_14.png", "images/InstalacionSQLserver_14.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_14.png"
        )
        img90 = ImageMobject(p_ins14) if p_ins14 else None

        if img90:
            img90.scale_to_fit_width(0.60 * config.frame_width)

            g90 = Group(img90)
            g90 = self._fit_group_center(g90, pad_x=1.0, pad_y=1.0)
            g90.shift(0.06 * DOWN)

            self._appear(g90, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g90)
        else:
            s90_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_14.png}")
            self._appear(s90_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s90_fallback)

        # ===== SLIDE 91 =====
        self._ensure_logo()
        self._ensure_frame()

        s91 = self._write_block(r"""
En este caso está disponible la versión \texttt{SSMS 21}, pero esto puede variar dependiendo de en que momento del futuro se consulte el curso, pero no es de importancia, solo se tiene que descargar la versión más reciente (que suele ser la que le recomienda la página),
""")
        s91 = _fit(self, s91, w=0.90, h=0.74, down=0.05)

        self._appear(s91, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s91)

        # ===== SLIDE 92  =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins15 = self._first_existing(
            "InstalacionSQLserver_15.png", "images/InstalacionSQLserver_15.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_15.png"
        )
        img92 = ImageMobject(p_ins15) if p_ins15 else None

        if img92:
            img92.scale_to_fit_width(0.80 * config.frame_width)

            g92 = Group(img92)
            g92 = self._fit_group_center(g92, pad_x=1.0, pad_y=1.0)
            g92.shift(0.06 * DOWN)

            self._appear(g92, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g92)
        else:
            s92_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_15.png}")
            self._appear(s92_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s92_fallback)

        # ===== SLIDE 93 =====
        self._ensure_logo()
        self._ensure_frame()

        s93 = self._write_block(r"""
Así que, una vez descargado el archivo \texttt{.exe}, procederemos a elegir la ruta de instalación e instalar. Al terminar la instalación se nos pedirá reiniciar nuestra computadora. 
\vskip 5PT
Una vez reiniciada nuestra computadora, abriremos \texttt{SSMS} y podremos acceder usando el método de autenticación que hayamos elegido en los pasos anteriores. Con esto ya tendremos nuestras herramientas de trabajo instaladas.
""")
        s93 = _fit(self, s93, w=0.90, h=0.80, down=0.05)

        self._appear(s93, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s93)

        # ===== SLIDE 94 =====
        self._ensure_logo()
        self._ensure_frame()

        s94 = self._write_block(r"""
En este curso se trabajará con una base de datos muestra llamada \texttt{AdventureWorks}, para descargarla basta con buscarla en el navegador y dirigirnos a la página correspondiente de Microsoft, donde encontraremos varias versiones de la base de datos, los ejemplos y ejercicios de este curso se desarrollaron con la versión 2022, pero en realidad esta base de datos no ha tenido cambios significativos desde la versión 2012.
""")
        s94 = _fit(self, s94, w=0.90, h=0.78, down=0.05)

        self._appear(s94, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s94)

        # ===== SLIDE 95 =====
        self._ensure_logo()
        self._ensure_frame()

        s95 = self._write_block(r"""
Así que procederemos a descargar el archivo \texttt{.bak} correspondiente a nuestra versión de \texttt{SQL Server}, o de manera alternativa podemos descargar la versión 2012. Los ejemplos y ejercicios de este libro usan la versión \texttt{\textbf{LT}}, pero también se puede descargar la versión \texttt{OLPT}, en este caso todo el código sigue siendo válido, solo se deberá cambiar el nombre de la base de datos y de algunos objetos en los códigos.
""")
        s95 = _fit(self, s95, w=0.90, h=0.80, down=0.05)

        self._appear(s95, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s95)

        # ===== SLIDE 96  =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins16 = self._first_existing(
            "InstalacionSQLserver_16.png", "images/InstalacionSQLserver_16.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_16.png"
        )
        img96 = ImageMobject(p_ins16) if p_ins16 else None

        if img96:
            img96.scale_to_fit_width(0.90 * config.frame_width)

            g96 = Group(img96)
            g96 = self._fit_group_center(g96, pad_x=1.0, pad_y=1.0)
            g96.shift(0.06 * DOWN)

            self._appear(g96, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g96)
        else:
            s96_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_16.png}")
            self._appear(s96_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s96_fallback)

        # ===== SLIDE 97 =====
        self._ensure_logo()
        self._ensure_frame()

        s97 = self._write_block(r"""
Una vez descargado el archivo \texttt{.bak}, lo copiaremos y pegaremos en la carpeta \texttt{Backup} que se encuentra en la carpeta donde están los archivos de \texttt{SQL Server} en los archivos de programa, su ubicación varía dependiendo de dónde hayamos instalado \texttt{SQL Server}, pero será similar a:
\begin{center}
\begin{verbatim}
C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\Backup
\end{verbatim}    
\end{center}
\vskip 5pt
Ahora, abriremos \texttt{SSMS}, en el panel izquierdo, daremos \textit{click} derecho en \texttt{Bases de datos} y elegiremos \texttt{Restaurar base de datos}.
""")
        s97 = _fit(self, s97, w=0.92, h=0.80, down=0.05)

        self._appear(s97, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s97)

        # ===== SLIDE 98  =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins17 = self._first_existing(
            "InstalacionSQLserver_17.png", "images/InstalacionSQLserver_17.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_17.png"
        )
        img98 = ImageMobject(p_ins17) if p_ins17 else None

        if img98:
            img98.scale_to_fit_width(0.50 * config.frame_width)

            g98 = Group(img98)
            g98 = self._fit_group_center(g98, pad_x=1.0, pad_y=1.0)
            g98.shift(0.06 * DOWN)

            self._appear(g98, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g98)
        else:
            s98_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_17.png}")
            self._appear(s98_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s98_fallback)

        # ===== SLIDE 99 =====
        self._ensure_logo()
        self._ensure_frame()

        s99 = self._write_block(r"""
En la ventana que se abrirá elegiremos \texttt{Dispositivo}, y luego \texttt{(…),}, se abrirá una ventana donde elegiremos la opción \texttt{Agregar}, y seleccionaremos nuestro archivo \texttt{.bak}.
""")
        s99 = _fit(self, s99, w=0.90, h=0.72, down=0.05)

        self._appear(s99, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s99)

        # ===== SLIDE 100 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins18 = self._first_existing(
            "InstalacionSQLserver_18.png", "images/InstalacionSQLserver_18.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_18.png"
        )
        img100 = ImageMobject(p_ins18) if p_ins18 else None

        if img100:
            img100.scale_to_fit_width(0.50 * config.frame_width)

            g100 = Group(img100)
            g100 = self._fit_group_center(g100, pad_x=1.0, pad_y=1.0)
            g100.shift(0.06 * DOWN)

            self._appear(g100, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g100)
        else:
            s100_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_18.png}")
            self._appear(s100_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s100_fallback)

        # ===== SLIDE 101 =====
        self._ensure_logo()
        self._ensure_frame()

        s101 = self._write_block(r"""
Una vez seleccionado el archivo \texttt{.bak}, daremos \texttt{Aceptar}, y de nuevo \texttt{Aceptar} para restaurar la base de datos. Si se obtiene un error, lo más probable es que el \texttt{.bak} que se descargo corresponda a una versión de la base de datos superior a la de \texttt{SQL Server}, por lo cual se deberá descargar una versión adecuada. Una vez terminado el proceso, y dependiendo de si se eligió la versión \texttt{OLTP} o \texttt{LT}, tendremos uno de los siguientes dos resultados.
""")
        s101 = _fit(self, s101, w=0.90, h=0.80, down=0.05)

        self._appear(s101, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s101)

        # ===== SLIDE 102 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins19 = self._first_existing(
            "InstalacionSQLserver_19.png", "images/InstalacionSQLserver_19.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_19.png"
        )
        img102 = ImageMobject(p_ins19) if p_ins19 else None

        if img102:
            img102.scale_to_fit_width(0.50 * config.frame_width)

            g102 = Group(img102)
            g102 = self._fit_group_center(g102, pad_x=1.0, pad_y=1.0)
            g102.shift(0.06 * DOWN)

            self._appear(g102, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g102)
        else:
            s102_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_19.png}")
            self._appear(s102_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s102_fallback)

        # ===== SLIDE 103 =====
        self._ensure_logo()
        self._ensure_frame()

        s103 = self._write_block(r"""
En la práctica, una base de datos puede llegarnos en distintos formatos según el origen y el objetivo de la transferencia: respaldos nativos para restauración (\texttt{.bak}), paquetes portables para mover estructura y/o datos (\texttt{.bacpac}/\texttt{.dacpac}), archivos físicos para adjuntar (\texttt{.mdf}/\texttt{.ldf}), scripts de creación (\texttt{.sql}) o incluso archivos planos para cargar datos (\texttt{.csv}/\texttt{.txt}).
""")
        s103 = _fit(self, s103, w=0.90, h=0.78, down=0.05)

        self._appear(s103, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s103)

        # ===== SLIDE 104 =====
        self._ensure_logo()
        self._ensure_frame()

        s104 = self._write_block(r"""
Por ello, antes de intentar instalar o importar cualquier archivo, conviene verificar que el formato corresponde al flujo correcto en \texttt{SSMS} y, sobre todo, cuidar la compatibilidad con nuestra versión de \texttt{SQL Server} (por ejemplo, un respaldo generado en una versión más nueva no puede restaurarse en una versión más antigua, y ciertos paquetes pueden requerir herramientas/componentes específicos). Con esa idea en mente, el siguiente listado resume, de forma directa, el procedimiento típico en \texttt{SSMS} para cada formato.
""")
        s104 = _fit(self, s104, w=0.90, h=0.80, down=0.05)

        self._appear(s104, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s104)

        # ===== SLIDE 105 =====
        self._ensure_logo()
        self._ensure_frame()

        s105 = self._write_block(r"""
\fileicon \texttt{\textbf{.bak} (respaldo nativo) $\to$ Restaurar base de datos.}
En el Explorador de objetos: clic derecho en \texttt{Bases de datos} $\to$ \texttt{Restaurar base de datos\ldots} $\to$ en \texttt{Origen} selecciona \texttt{Dispositivo} $\to$ clic en \texttt{\ldots} $\to$ \texttt{Agregar} $\to$ elige el archivo \texttt{.bak} $\to$ \texttt{Aceptar} $\to$ en \texttt{Destino} verifica el \texttt{Nombre de la base de datos} $\to$ (opcional) pestaña \texttt{Archivos} para confirmar rutas/ajustar ubicaciones $\to$ \texttt{Aceptar}.
""")
        s105 = _fit(self, s105, w=0.92, h=0.82, down=0.05)

        self._appear(s105, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s105)

        # ===== SLIDE 106 =====
        self._ensure_logo()
        self._ensure_frame()

        s106 = self._write_block(r"""
\fileicon \texttt{\textbf{.bacpac} (esquema + datos) $\to$ Importar aplicación de capa de datos.}
Clic derecho en \texttt{Bases de datos} $\to$ \texttt{Importar aplicación de capa de datos\ldots} $\to$ \texttt{Siguiente} $\to$ en \texttt{Importar desde} selecciona \texttt{Archivo local} $\to$ \texttt{Examinar} y elige el \texttt{.bacpac} $\to$ \texttt{Siguiente} $\to$ define \texttt{Nombre de la nueva base de datos} (y, si se solicita, rutas de datos/log) $\to$ \texttt{Siguiente} $\to$ revisa el resumen $\to$ \texttt{Finalizar}.
""")
        s106 = _fit(self, s106, w=0.92, h=0.82, down=0.05)

        self._appear(s106, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s106)

        # ===== SLIDE 107 =====
        self._ensure_logo()
        self._ensure_frame()

        s107 = self._write_block(r"""
\fileicon \texttt{\textbf{.dacpac} (solo esquema) $\to$ Implementar aplicación de capa de datos.}
Clic derecho en \texttt{Bases de datos} $\to$ \texttt{Implementar aplicación de capa de datos\ldots} $\to$ \texttt{Siguiente} $\to$ \texttt{Examinar} y elige el \texttt{.dacpac} $\to$ \texttt{Siguiente} $\to$ define \texttt{Nombre de la base de datos} (nueva o existente, según el asistente) $\to$ \texttt{Siguiente} $\to$ revisa opciones (si aparecen) $\to$ \texttt{Finalizar}.
""")
        s107 = _fit(self, s107, w=0.92, h=0.82, down=0.05)

        self._appear(s107, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s107)

        # ===== SLIDE 108 =====
        self._ensure_logo()
        self._ensure_frame()

        s108 = self._write_block(r"""
\fileicon \texttt{\textbf{.mdf/.ldf} (archivos físicos) $\to$ Adjuntar base de datos.}
Clic derecho en \texttt{Bases de datos} $\to$ \texttt{Adjuntar\ldots} $\to$ \texttt{Agregar} $\to$ selecciona el \texttt{.mdf} $\to$ SSMS intentará localizar el \texttt{.ldf} automáticamente $\to$ si falta, revisa la lista de archivos y corrige la ruta del log $\to$ \texttt{Aceptar}.
""")
        s108 = _fit(self, s108, w=0.92, h=0.82, down=0.05)

        self._appear(s108, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s108)

        # ===== SLIDE 109 =====
        self._ensure_logo()
        self._ensure_frame()

        s109 = self._write_block(r"""
\fileicon \texttt{Script .\textbf{sql} (instalación por código) $\to$ Ejecutar en SSMS.}
\texttt{Archivo} $\to$ \texttt{Abrir} $\to$ \texttt{Archivo\ldots} $\to$ selecciona el \texttt{.sql} $\to$ verifica el contexto (idealmente el script incluye \texttt{CREATE DATABASE} y/o \texttt{USE}) $\to$ \texttt{Ejecutar} $\to$ confirma que la base y sus objetos aparecen en el Explorador de objetos.
""")
        s109 = _fit(self, s109, w=0.92, h=0.82, down=0.05)

        self._appear(s109, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s109)

        # ===== SLIDE 110 =====
        self._ensure_logo()
        self._ensure_frame()

        s110 = self._write_block(r"""
\fileicon \texttt{\textbf{.csv/.txt} (datos tabulares) $\to$ Importar datos.}
Primero crea o elige una base de datos destino $\to$ clic derecho sobre esa base $\to$ \texttt{Tareas} $\to$ \texttt{Importar datos\ldots} $\to$ \texttt{Siguiente} $\to$ en \texttt{Origen de datos} elige \texttt{Archivo plano} $\to$ selecciona el \texttt{.csv} $\to$ configura separador (coma \texttt{,} o punto y coma \texttt{;}) y comillas \texttt{"} si aplica $\to$ activa ``primera fila con nombres de columna'' si hay encabezados $\to$ \texttt{Siguiente} $\to$ en \texttt{Destino} elige el controlador de SQL Server y selecciona \texttt{Servidor} y \texttt{Base de datos} $\to$ \texttt{Siguiente} $\to$ \texttt{Copiar datos de una o varias tablas o vistas} $\to$ \texttt{Siguiente} $\to$ asigna el \texttt{Nombre de tabla destino}
""")
        s110 = _fit(self, s110, w=0.92, h=0.84, down=0.05)

        self._appear(s110, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s110)

        # ===== SLIDE 111 =====
        self._ensure_logo()
        self._ensure_frame()

        s111 = self._write_block(r"""
(p.\,ej. \texttt{dbo.MiTablaCSV}) $\to$ \texttt{Editar asignaciones\ldots} para ajustar tipos (\texttt{int}, \texttt{decimal}, \texttt{datetime}, longitudes \texttt{varchar}) $\to$ \texttt{Aceptar} $\to$ \texttt{Siguiente} $\to$ \texttt{Finalizar}. Si no aparece \texttt{Importar datos\ldots}, alternativa: clic derecho en la base $\to$ \texttt{Tareas} $\to$ \texttt{Importar archivo plano\ldots} y seguir el asistente.
""")
        s111 = _fit(self, s111, w=0.92, h=0.80, down=0.05)

        self._appear(s111, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s111)

        # ===== SLIDE 112 =====
        self._ensure_logo()
        self._ensure_frame()

        s112 = self._write_block(r"""
Como siguiente paso, ya que tenemos nuestra cuenta de Microsoft con una suscripción activada de Azure, solo iremos a \texttt{\textcolor{blue}{portal.azure.com}}  para entrar a nuestra cuenta y acceder al Portal Azure, para poder crear nuestra instancia de \textit{Azure SQL Database}, para esto ya sea en el menú lateral o en la pantalla inicial elegiremos \texttt{SQL databases}, y luego \texttt{Create}.
""")
        s112 = _fit(self, s112, w=0.90, h=0.78, down=0.05)

        self._appear(s112, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s112)

        # ===== SLIDE 113 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins20 = self._first_existing(
            "InstalacionSQLserver_20.png", "images/InstalacionSQLserver_20.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_20.png"
        )
        img113 = ImageMobject(p_ins20) if p_ins20 else None

        if img113:
            img113.scale_to_fit_width(0.40 * config.frame_width)

            g113 = Group(img113)
            g113 = self._fit_group_center(g113, pad_x=1.0, pad_y=1.0)
            g113.shift(0.06 * DOWN)

            self._appear(g113, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g113)
        else:
            s113_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_20.png}")
            self._appear(s113_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s113_fallback)

        # ===== SLIDE 114 =====
        self._ensure_logo()
        self._ensure_frame()

        s114 = self._write_block(r"""
La pantalla para crear la base de datos y el servidor puede cambiar a través del tiempo, pero los detalles generales de creación son los mismos. Configuraremos primero lo correspondiente a la pestaña \texttt{Basics}. En esta pestaña, seleccionaremos nuestra suscripción, elegiremos crear un nuevo grupo, al que llamaremos \texttt{sqlgroup}, daremos un nombre a nuestra base (\texttt{AdventureWorksLT}), y elegiremos crear un nuevo servidor.
""")
        s114 = _fit(self, s114, w=0.90, h=0.80, down=0.05)

        self._appear(s114, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s114)

        # ===== SLIDE 115 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins23 = self._first_existing(
            "InstalacionSQLserver_23.png", "images/InstalacionSQLserver_23.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_23.png"
        )
        img115 = ImageMobject(p_ins23) if p_ins23 else None

        if img115:
            img115.scale_to_fit_width(0.80 * config.frame_width)

            g115 = Group(img115)
            g115 = self._fit_group_center(g115, pad_x=1.0, pad_y=1.0)
            g115.shift(0.06 * DOWN)

            self._appear(g115, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g115)
        else:
            s115_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_23.png}")
            self._appear(s115_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s115_fallback)

        # ===== SLIDE 116 =====
        self._ensure_logo()
        self._ensure_frame()

        s116 = self._write_block(r"""
En la pantalla de creación de servidor deberemos dar un nombre de servidor (uno que se pueda recordar), elegir una ubicación geográfica (es importante elegir la zona de EU más cercana a nuestra ubicación), escribir un nombre de acceso para el administrador, y una contraseña. Daremos \texttt{Ok}, y ya podremos elegir nuestro servidor en la pestaña de \texttt{Basics}.
""")
        s116 = _fit(self, s116, w=0.90, h=0.80, down=0.05)

        self._appear(s116, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s116)

        # ===== SLIDE 117 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins21 = self._first_existing(
            "InstalacionSQLserver_21.png", "images/InstalacionSQLserver_21.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_21.png"
        )
        img117 = ImageMobject(p_ins21) if p_ins21 else None

        if img117:
            img117.scale_to_fit_width(0.80 * config.frame_width)

            g117 = Group(img117)
            g117 = self._fit_group_center(g117, pad_x=1.0, pad_y=1.0)
            g117.shift(0.06 * DOWN)

            self._appear(g117, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g117)
        else:
            s117_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_21.png}")
            self._appear(s117_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s117_fallback)

        # ===== SLIDE 118 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins22 = self._first_existing(
            "InstalacionSQLserver_22.png", "images/InstalacionSQLserver_22.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_22.png"
        )
        img118 = ImageMobject(p_ins22) if p_ins22 else None

        if img118:
            img118.scale_to_fit_width(0.80 * config.frame_width)

            g118 = Group(img118)
            g118 = self._fit_group_center(g118, pad_x=1.0, pad_y=1.0)
            g118.shift(0.06 * DOWN)

            self._appear(g118, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g118)
        else:
            s118_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_22.png}")
            self._appear(s118_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s118_fallback)

        # ===== SLIDE 119 =====
        self._ensure_logo()
        self._ensure_frame()

        s119 = self._write_block(r"""
Iremos a la pestaña \texttt{Additional Settings} y en \texttt{Data Source} elegiremos \texttt{Sample}. En automático se elegirá la base muestra \texttt{AdventureWorksLT}. antiguamente se debía seleccionar la base, si este fuera el caso seleccionamos \texttt{AdventureWorksLT}.
""")
        s119 = _fit(self, s119, w=0.90, h=0.80, down=0.05)

        self._appear(s119, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s119)

        # ===== SLIDE 120 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins24 = self._first_existing(
            "InstalacionSQLserver_24.png", "images/InstalacionSQLserver_24.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_24.png"
        )
        img120 = ImageMobject(p_ins24) if p_ins24 else None

        if img120:
            img120.scale_to_fit_width(0.80 * config.frame_width)

            g120 = Group(img120)
            g120 = self._fit_group_center(g120, pad_x=1.0, pad_y=1.0)
            g120.shift(0.06 * DOWN)

            self._appear(g120, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g120)
        else:
            s120_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_24.png}")
            self._appear(s120_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s120_fallback)

        # ===== SLIDE 121 =====
        self._ensure_logo()
        self._ensure_frame()

        s121 = self._write_block(r"""
En la pestaña \texttt{Networking}  elegiremos la opción \texttt{Public endpoint}, la cual nos despliega más opciones, seleccionaremos Yes en \texttt{Add current client IP adress}. Esto lo que hace es agregar nuestra dirección \texttt{IP} actual a la lista de \texttt{IPs} que pueden conectarse al servidor y a la base de datos.
""")
        s121 = _fit(self, s121, w=0.90, h=0.80, down=0.05)

        self._appear(s121, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s121)

        # ===== SLIDE 122 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins25 = self._first_existing(
            "InstalacionSQLserver_25.png", "images/InstalacionSQLserver_25.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_25.png"
        )
        img122 = ImageMobject(p_ins25) if p_ins25 else None

        if img122:
            img122.scale_to_fit_width(0.80 * config.frame_width)

            g122 = Group(img122)
            g122 = self._fit_group_center(g122, pad_x=1.0, pad_y=1.0)
            g122.shift(0.06 * DOWN)

            self._appear(g122, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g122)
        else:
            s122_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_25.png}")
            self._appear(s122_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s122_fallback)

        # ===== SLIDE 123 =====
        self._ensure_logo()
        self._ensure_frame()

        s123 = self._write_block(r"""
Una vez que ya hayamos configurado lo anterior, iremos a \texttt{Review + create}, y crearemos nuestra base de datos \texttt{SQL}. También, en esta pantalla aparecerá el costo mensual de la base de datos \texttt{SQL}, el cual debería ser cero.
""")
        s123 = _fit(self, s123, w=0.90, h=0.80, down=0.05)

        self._appear(s123, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s123)

        # ===== SLIDE 124 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins26 = self._first_existing(
            "InstalacionSQLserver_26.png", "images/InstalacionSQLserver_26.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_26.png"
        )
        img124 = ImageMobject(p_ins26) if p_ins26 else None

        if img124:
            img124.scale_to_fit_width(0.80 * config.frame_width)

            g124 = Group(img124)
            g124 = self._fit_group_center(g124, pad_x=1.0, pad_y=1.0)
            g124.shift(0.06 * DOWN)

            self._appear(g124, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g124)
        else:
            s124_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_26.png}")
            self._appear(s124_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s124_fallback)

        # ===== SLIDE 125 =====
        self._ensure_logo()
        self._ensure_frame()

        s125 = self._write_block(r"""
Para usar la base de datos que acabamos de crear deberemos conectarnos al servidor mediante \texttt{SSMS}. Si se conectó con la misma dirección \texttt{IP} que usamos al seguir los pasos anteriores no tendremos problemas para conectarnos, pero si tratamos de conectarnos desde otra \texttt{IP}, deberemos configurar el \textit{}firewall para poder conectarnos. Para esto iremos a la pantalla inicial de \texttt{SQL databases} a la que accedimos al inicio del proceso de creación, y elegiremos nuestra base de datos.
""")
        s125 = _fit(self, s125, w=0.90, h=0.82, down=0.05)

        self._appear(s125, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s125)

        # ===== SLIDE 126 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins27 = self._first_existing(
            "InstalacionSQLserver_27.png", "images/InstalacionSQLserver_27.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_27.png"
        )
        img126 = ImageMobject(p_ins27) if p_ins27 else None

        if img126:
            img126.scale_to_fit_width(0.80 * config.frame_width)

            g126 = Group(img126)
            g126 = self._fit_group_center(g126, pad_x=1.0, pad_y=1.0)
            g126.shift(0.06 * DOWN)

            self._appear(g126, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g126)
        else:
            s126_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_27.png}")
            self._appear(s126_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s126_fallback)

        # ===== SLIDE 127 =====
        self._ensure_logo()
        self._ensure_frame()

        s127 = self._write_block(r"""
Esto nos llevara a los detalles de nuestra base de datos, donde podremos configurar y administrar sus características. En esta pantalla elegiremos el nombre de nuestro servidor, y luego \texttt{Show networking settings}.
""")
        s127 = _fit(self, s127, w=0.90, h=0.80, down=0.05)

        self._appear(s127, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s127)

        # ===== SLIDE 128 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins28 = self._first_existing(
            "InstalacionSQLserver_28.png", "images/InstalacionSQLserver_28.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_28.png"
        )
        img128 = ImageMobject(p_ins28) if p_ins28 else None

        if img128:
            img128.scale_to_fit_width(0.80 * config.frame_width)

            g128 = Group(img128)
            g128 = self._fit_group_center(g128, pad_x=1.0, pad_y=1.0)
            g128.shift(0.06 * DOWN)

            self._appear(g128, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g128)
        else:
            s128_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_28.png}")
            self._appear(s128_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s128_fallback)

        # ===== SLIDE 129 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins29 = self._first_existing(
            "InstalacionSQLserver_29.png", "images/InstalacionSQLserver_29.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_29.png"
        )
        img129 = ImageMobject(p_ins29) if p_ins29 else None

        if img129:
            img129.scale_to_fit_width(0.80 * config.frame_width)

            g129 = Group(img129)
            g129 = self._fit_group_center(g129, pad_x=1.0, pad_y=1.0)
            g129.shift(0.06 * DOWN)

            self._appear(g129, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g129)
        else:
            s129_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_29.png}")
            self._appear(s129_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s129_fallback)

        # ===== SLIDE 130 =====
        self._ensure_logo()
        self._ensure_frame()

        s130 = self._write_block(r"""
En la pantalla que aparecerá podremos elegir las redes a las cuales queremos dar acceso, y en esta sección daremos \textit{click} en \texttt{Add your client IPv4 address}, se agregará nuestra dirección \texttt{IP} y daremos \texttt{Save}.
""")
        s130 = _fit(self, s130, w=0.90, h=0.80, down=0.05)

        self._appear(s130, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s130)

        # ===== SLIDE 131 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins30 = self._first_existing(
            "InstalacionSQLserver_30.png", "images/InstalacionSQLserver_30.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_30.png"
        )
        img131 = ImageMobject(p_ins30) if p_ins30 else None

        if img131:
            img131.scale_to_fit_width(0.80 * config.frame_width)

            g131 = Group(img131)
            g131 = self._fit_group_center(g131, pad_x=1.0, pad_y=1.0)
            g131.shift(0.06 * DOWN)

            self._appear(g131, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g131)
        else:
            s131_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_30.png}")
            self._appear(s131_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s131_fallback)

        # ===== SLIDE 132 =====
        self._ensure_logo()
        self._ensure_frame()

        s132 = self._write_block(r"""
Una vez realizado esto podremos usar \texttt{SSMS} para conectarnos a nuestro servidor y usar la base de datos, para esto solo deberemos poner la dirección de nuestro servidor y las credenciales que establecimos al crear la base de datos.
""")
        s132 = _fit(self, s132, w=0.90, h=0.80, down=0.05)

        self._appear(s132, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s132)

        # ===== SLIDE 133 =====
        self._ensure_logo()
        self._ensure_frame()

        p_ins31 = self._first_existing(
            "InstalacionSQLserver_31.png", "images/InstalacionSQLserver_31.png",
            "/home/gustavo/SS/ImagesSQL_Slides/InstalacionSQLserver_31.png"
        )
        img133 = ImageMobject(p_ins31) if p_ins31 else None

        if img133:
            img133.scale_to_fit_width(0.50 * config.frame_width)

            g133 = Group(img133)
            g133 = self._fit_group_center(g133, pad_x=1.0, pad_y=1.0)
            g133.shift(0.06 * DOWN)

            self._appear(g133, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g133)
        else:
            s133_fallback = self._write_block(r"\texttt{InstalacionSQLserver\_31.png}")
            self._appear(s133_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s133_fallback)

        # ===== SLIDE 134 =====
        self._ensure_logo()
        self._ensure_frame()

        s134 = self._write_block(
            r"""\subsection*{\textcolor{myPurple}{Ejecución de \textit{queries} y comandos básicos en \texttt{SSMS}}}"""
        )

        self._appear(s134, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s134)

        # ===== SLIDE 135 =====
        self._ensure_logo()
        self._ensure_frame()

        s135 = self._write_block(r"""
En \texttt{SSMS} podremos entre otras cosas escribir nuestros códigos de \texttt{SQL}, que en este caso serán conocidos como \textit{queries} (consultas). Para esto, seleccionaremos \texttt{Nueva consulta} o usaremos \texttt{Ctr+N}.
""")
        s135 = _fit(self, s135, w=0.90, h=0.80, down=0.05)

        self._appear(s135, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s135)

        # ===== SLIDE 136 =====
        self._ensure_logo()
        self._ensure_frame()

        p_cb1 = self._first_existing(
            "ComandosBasicos_1.png", "images/ComandosBasicos_1.png",
            "/home/gustavo/SS/ImagesSQL_Slides/ComandosBasicos_1.png"
        )
        img136 = ImageMobject(p_cb1) if p_cb1 else None

        if img136:
            img136.scale_to_fit_width(0.50 * config.frame_width)

            g136 = Group(img136)
            g136 = self._fit_group_center(g136, pad_x=1.0, pad_y=1.0)
            g136.shift(0.06 * DOWN)

            self._appear(g136, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g136)
        else:
            s136_fallback = self._write_block(r"\texttt{ComandosBasicos\_1.png}")
            self._appear(s136_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s136_fallback)

        # ===== SLIDE 137 =====
        self._ensure_logo()
        self._ensure_frame()

        s137 = self._write_block(r"""
Los \textit{queries} se ejecutan sobre las bases de datos, por defecto al no tener seleccionada una base de datos específicamente y crear un nuevo \textit{query} se selecciona la base de datos \textbf{master}. Lo que haremos será seleccionar nuestra base de datos (\texttt{AdventureWorksLT2022}) manualmente antes de ejecutar el \textit{query}.
""")
        s137 = _fit(self, s137, w=0.90, h=0.80, down=0.05)

        self._appear(s137, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s137)

        # ===== SLIDE 138 =====
        self._ensure_logo()
        self._ensure_frame()

        p_cb2 = self._first_existing(
            "ComandosBasicos_2.png", "images/ComandosBasicos_2.png",
            "/home/gustavo/SS/ImagesSQL_Slides/ComandosBasicos_2.png"
        )
        img138 = ImageMobject(p_cb2) if p_cb2 else None

        if img138:
            img138.scale_to_fit_width(0.35 * config.frame_width)

            g138 = Group(img138)
            g138 = self._fit_group_center(g138, pad_x=1.0, pad_y=1.0)
            g138.shift(0.06 * DOWN)

            self._appear(g138, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g138)
        else:
            s138_fallback = self._write_block(r"\texttt{ComandosBasicos\_2.png}")
            self._appear(s138_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s138_fallback)

        # ===== SLIDE 139 =====
        self._ensure_logo()
        self._ensure_frame()

        s139 = self._write_block(r"""
Una vez hecho esto podremos ejecutar nuestros \textit{queries} usando \texttt{Ejecutar} o \texttt{F5}. El resultado de los \textit{queries} aparecerá en una tabla en una ventana en la parte baja de la pantalla, como en el siguiente ejemplo:
""")
        s139 = _fit(self, s139, w=0.90, h=0.80, down=0.05)

        self._appear(s139, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s139)

        # ===== SLIDE 140 =====
        self._ensure_logo()
        self._ensure_frame()

        p_cb3 = self._first_existing(
            "ComandosBasicos_3.png", "images/ComandosBasicos_3.png",
            "/home/gustavo/SS/ImagesSQL_Slides/ComandosBasicos_3.png"
        )
        img140 = ImageMobject(p_cb3) if p_cb3 else None

        if img140:
            img140.scale_to_fit_width(0.95 * config.frame_width)

            g140 = Group(img140)
            g140 = self._fit_group_center(g140, pad_x=1.0, pad_y=1.0)
            g140.shift(0.06 * DOWN)

            self._appear(g140, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g140)
        else:
            s140_fallback = self._write_block(r"\texttt{ComandosBasicos\_3.png}")
            self._appear(s140_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s140_fallback)

        # ===== SLIDE 141 =====
        self._ensure_logo()
        self._ensure_frame()

        s141 = self._write_block(r"""
Lo anterior aplica para más de un comando, por ejemplo:
""")
        s141 = _fit(self, s141, w=0.90, h=0.80, down=0.05)

        self._appear(s141, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s141)

        # ===== SLIDE 142 =====
        self._ensure_logo()
        self._ensure_frame()

        p_cb4 = self._first_existing(
            "ComandosBasicos_4.png", "images/ComandosBasicos_4.png",
            "/home/gustavo/SS/ImagesSQL_Slides/ComandosBasicos_4.png"
        )
        img142 = ImageMobject(p_cb4) if p_cb4 else None

        if img142:
            img142.scale_to_fit_width(0.95 * config.frame_width)

            g142 = Group(img142)
            g142 = self._fit_group_center(g142, pad_x=1.0, pad_y=1.0)
            g142.shift(0.06 * DOWN)

            self._appear(g142, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g142)
        else:
            s142_fallback = self._write_block(r"\texttt{ComandosBasicos\_4.png}")
            self._appear(s142_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s142_fallback)

        # ===== SLIDE 143 =====
        self._ensure_logo()
        self._ensure_frame()

        s143 = self._write_block(r"""
En la parte baja de la pantalla podremos ver las estadísticas de la ejecución, y también es posible cambiar la forma en que se presentan los resultados, por ejemplo, podemos indicar que queremos que se guarden en un archivo, entre otras opciones.
""")
        s143 = _fit(self, s143, w=0.90, h=0.80, down=0.05)

        self._appear(s143, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s143)

        # ===== SLIDE 144 =====
        self._ensure_logo()
        self._ensure_frame()

        s144 = self._write_block(r"""
Hasta este momento podemos notar el uso del carácter \texttt{;}, este es el terminador de instrucción: marca dónde termina un \textit{statement} (declaración) y empieza el siguiente, especialmente cuando ejecutamos varios en el mismo \textit{script}, como en el ejemplo anterior.
""")
        s144 = _fit(self, s144, w=0.90, h=0.80, down=0.05)

        self._appear(s144, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s144)

        # ===== SLIDE 145 =====
        self._ensure_logo()
        self._ensure_frame()

        s145 = self._write_block(r"""
Podemos pensar en \texttt{;} como un “punto final” para que el motor sepa exactamente hasta dónde llega cada instrucción; por eso es buena costumbre escribirlo siempre al final de nuestras consultas, aunque algunas funcionen sin él, pero usarlo evita ambigüedades cuando ponemos varias instrucciones seguidas.
\vskip 5PT
En caso de que no seleccionar la base de datos manualmente, lo podemos hacer con código de la siguiente forma:
""")
        s145 = _fit(self, s145, w=0.90, h=0.80, down=0.05)

        self._appear(s145, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s145)

        # ===== SLIDE 146 =====
        self._ensure_logo()
        self._ensure_frame()

        p_cb5 = self._first_existing(
            "ComandosBasicos_5.png", "images/ComandosBasicos_5.png",
            "/home/gustavo/SS/ImagesSQL_Slides/ComandosBasicos_5.png"
        )
        img146 = ImageMobject(p_cb5) if p_cb5 else None

        if img146:
            img146.scale_to_fit_width(0.95 * config.frame_width)

            g146 = Group(img146)
            g146 = self._fit_group_center(g146, pad_x=1.0, pad_y=1.0)
            g146.shift(0.06 * DOWN)

            self._appear(g146, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(g146)
        else:
            s146_fallback = self._write_block(r"\texttt{ComandosBasicos\_5.png}")
            self._appear(s146_fallback, direction=DOWN, rt=WRITE_MEDIUM_RT)
            self.wait(0.3)
            self._disappear(s146_fallback)

        # ===== SLIDE 147 =====
        self._ensure_logo()
        self._ensure_frame()

        s147 = self._write_block(r"""
Con las herramientas de trabajo que ya tenemos instaladas y la base de datos adjuntada así como la introducción a los comandos básicos de ejecución de un \textit{query}, podremos seguir en los siguiente capítulos con la teoría y práctica de \texttt{T-SQL}.
""")
        s147 = _fit(self, s147, w=0.90, h=0.80, down=0.05)

        self._appear(s147, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s147)

        # ===== SLIDE 148 =====
        self._ensure_logo()
        self._ensure_frame()

        s148 = self._write_block(r"""
A lo largo de los siguientes capítulos encontraremos las partes donde se den ejemplos de código, estos aparecerán de la siguiente forma:
\vskip 5pt
\begin{center} 
\begin{minipage}{0.98\linewidth}
\begin{lstlisting}[language=SQL,
backgroundcolor=\color{white},
basicstyle=\fontfamily{pcr}\selectfont\small,
keywordstyle=\color{blue}\bfseries,
stringstyle=\color{red},
commentstyle=\color{green!60!black}\bfseries,
frame=none, breaklines=true, columns=fullflexible,
deletekeywords={TABLE,COLUMN},
% --- AZUL: control de flujo / batch ---
emph={[2]CREATE,INDEX,ON,UNIQUE,DESC,ASC,CLUSTERED},
emphstyle={[2]\color{blue}\bfseries},
% --- MAGENTA (negritas): funciones de error ---
emph={[3]COUNT,CONVERT,SUM,Product,UPDATE},
emphstyle={[3]\color{magenta}\bfseries},
emph={[1]NOT,EXISTS,OR,ALL},
emphstyle={[1]\color{gray}\bfseries}
]
SELECT CONVERT(varchar(5),CustomerID) + ': ' +  

CompanyName AS Company 

FROM SalesLT.Customer; 
\end{lstlisting}
\end{minipage}
\end{center}
""")
        s148 = _fit(self, s148, w=0.92, h=0.82, down=0.05)

        self._appear(s148, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s148)

        # ===== SLIDE 149 =====
        self._ensure_logo()
        self._ensure_frame()

        s149 = self._write_block(r"""
La códigos son ejecutables en nuestro \texttt{SQL Server}, siempre y cuando haya instalado \texttt{SQL Server} y adjuntado la base de datos con la que se trabaja en este curso. Y para ayudar con la identificación de las partes de código se ha decidido seguir un código de color similar al que usa \texttt{SQL Server}, así que se encontrarán  palabras como \texttt{\textcolor{blue}{\textbf{SELECT}}} o \texttt{\textcolor{magenta}{\textbf{GETDATE}}} de esta forma para indicar que son comandos, funciones, o palabras reservadas que tienen una función dentro del lenguaje.
""")
        s149 = _fit(self, s149, w=0.90, h=0.80, down=0.05)

        self._appear(s149, direction=DOWN, rt=WRITE_MEDIUM_RT)
        self.wait(0.3)
        self._disappear(s149)



# manim -pqh Introduccion_Entornos_y_conceptos.py Introduccion