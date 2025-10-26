from manim import *
from pathlib import Path
import os, tempfile
import numpy as np

config.background_color = WHITE
config.pixel_width  = 1920
config.pixel_height = 1080
config.frame_rate   = 60
WRITE_MEDIUM_RT = 3   
TITLE_IN_RT     = 1.5   

Tex.set_default(font_size=44, color=BLACK)
MathTex.set_default(font_size=44, color=BLACK)
Text.set_default(font_size=44, color=BLACK)

tex_template = TexTemplate()
tex_template.add_to_preamble(r"""
\usepackage[T1]{fontenc}
\usepackage{amsmath, amssymb, mathtools}
\usepackage{array, booktabs, multirow, tabularx}
\usepackage{xcolor}
\usepackage{siunitx}
\usepackage{graphicx}
\usepackage{upquote}
\usepackage{inconsolata}
\usepackage{listings}

\definecolor{codebg}{HTML}{F8F8F8}
\definecolor{codefg}{HTML}{000000}
\definecolor{kw}{HTML}{005CC5}
\definecolor{kw2}{HTML}{008080}
\definecolor{str}{HTML}{D73A49}
\definecolor{com}{HTML}{6A737D}

\lstdefinelanguage{SQLcustom}{
  sensitive=false,
  morekeywords=[1]{SELECT,FROM,WHERE,ORDER,BY,GROUP,HAVING,JOIN,INNER,LEFT,RIGHT,OUTER,ON,COUNT,AS,AND,OR,NOT,IN,LIKE,TOP,LIMIT,FETCH,FIRST,ROWS,ONLY,DATE,DESC,ASC},
  morekeywords=[2]{DATABASE,TABLE},
  morecomment=[l]{--},
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
% ---------------------------------------------------------------------------
""")

def write_block(tex_str, scale=1.0, pos=ORIGIN):
    m = Tex(tex_str, tex_template=tex_template)
    if scale != 1.0:
        m.scale(scale)
    m.move_to(pos)
    return m

class BaseSlide(Scene):
    def show_title(self, title_tex, animate_from=UP, run_time=None, y_offset=0.5):
        rt = TITLE_IN_RT if run_time is None else run_time
        t = Tex(title_tex, tex_template=tex_template)
        t.to_edge(UP).shift(y_offset*UP)
        self.play(FadeIn(t, shift=0.6*animate_from, run_time=rt))
        self.wait(0.1)
        return t

    def show_body(self, body_tex, below, buff=0.5, align_edge=LEFT, scale=1.0, run_time=None):
        rt = WRITE_MEDIUM_RT if run_time is None else run_time
        b = write_block(body_tex, scale=scale)
        b.next_to(below, DOWN, buff=buff, aligned_edge=align_edge)
        self.play(Write(b, run_time=rt))
        self.wait(0.1)
        return b

    def show_console_latex(self, listing_tex, below, buff=0.5, align_edge=LEFT, scale=0.95, run_time=None):
        rt = WRITE_MEDIUM_RT if run_time is None else run_time
        block = Tex(listing_tex, tex_template=tex_template)
        if scale != 1.0:
            block.scale(scale)
        block.next_to(below, DOWN, buff=buff, aligned_edge=align_edge)
        self.play(Write(block, run_time=rt))
        self.wait(0.1)
        return block

    def appear_from(self, mob, direction=DOWN, run_time=0.8):
        self.play(FadeIn(mob, shift=0.6*direction, run_time=run_time))
        self.wait(0.1)

    def disappear(self, mob, run_time=0.6):
        self.play(FadeOut(mob, run_time=run_time))
        self.wait(0.05)

    def pause(self, t=0.5):
        self.wait(t)

    def fade_out_all(self, *mobs, run_time=0.6):
        targets = list(mobs) if mobs else list(self.mobjects)
        if not targets:
            return
        self.play(*[FadeOut(m) for m in targets], run_time=run_time)
        self.wait(0.05)

def make_code_block(code_text, language="python"):
    ext_map = {"python": ".py", "py": ".py", "cpp": ".cpp", "c++": ".cpp", "c": ".c"}
    ext = ext_map.get(str(language).lower(), ".txt")
    tmp_dir = Path("media") / "_tmp" / "sql_snippets"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_file = tmp_dir / f"snippet_{language}{ext}"
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(code_text)
    try:
        return Code(file_name=str(tmp_file), language=language, background="rectangle", insert_line_no=False, style="default", tab_width=2)
    except TypeError:
        try:
            return Code(file_name=str(tmp_file), language=language, tab_width=2)
        except Exception:
            lang_map = {"python": "Python", "py": "Python", "cpp": "C++", "c++": "C++", "c": "C"}
            lst_lang = lang_map.get(str(language).lower(), "text")
            listing = rf"""
\begin{{lstlisting}}[style=sqlBlue,language={lst_lang}]
{code_text}
\end{{lstlisting}}
"""
            return Tex(listing, tex_template=tex_template)

def fit_text_block(mobj, max_w, max_h, pad=0.0, min_sf=0.45):

    eff_w = max_w * (1.0 - pad)
    eff_h = max_h * (1.0 - pad)

    sw = eff_w / mobj.width  if mobj.width  > eff_w else 1.0
    sh = eff_h / mobj.height if mobj.height > eff_h else 1.0
    sf = min(sw, sh)

    if sf > 1.0:
        sf = 1.0
    sf = min(sf, 1.00)
    if mobj.width > eff_w*0.92 or mobj.height > eff_h*0.92:
        pass
    else:
        sf = min(sf, 1.0)
        sf = max(min_sf, sf)

    if sf < 1.0:
        mobj.scale(sf)
    return sf

TITLE_1 = r"""
{\fontsize{28}{34}\selectfont \textcolor{purple}{Fundamentos de bases de datos para SQL}}
"""

CONTENT_1 = r"""
% Contenido del Slide 1 (LaTeX). Pega el bloque EXACTO aquí.
% Ejemplo NO vinculante (sólo de referencia):
% \begin{itemize}
%   \item ¿Qué es SQL? Lenguaje de consulta estructurado
%   \item Tablas, filas, columnas
%   \item Consultas SELECT básicas
% \end{itemize}
"""

# --- Slide 2
CONTENT_2 = r"""
\textbf{SQL} son las siglas de  Lenguaje de Consulta Estructurada (Structured Query Language), es un tipo de lenguaje declarativo desarrollado por IBM alredededor de 1947 con el propósito de ser usado para administrar y consultar la información almacenada en bases de datos.
\vskip 20pt
\noindent A diferencia de lenguajes populares como los compilados (C, C++, Go, etc.) o los interpretados (Python, JavaScript, etc.), un lenguaje declarativo especifica qué resultado se desea, pero no es de interés como se realiza.
"""

IMG_2_PATH = "/home/gustavo/SS/lenguajes.png" 

S2_TEXT_MAX_W   = 0.92
S2_TEXT_MAX_H   = 0.48
S2_TOP_BUFF     = 0.40

S2_IMG_W_FRAC   = 0.58  
S2_IMG_MAX_H    = 0.38  
S2_GAP_TXT_IMG  = 0.42   
S2_BOTTOM_PAD   = 0.26  

# --- Slide 3 
CONTENT_3 = r"""
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
"""

# --- Slide 4 
CONTENT_4 = r"""
\vskip 10pt
A diferencia de lenguajes como Python, C++, Java, donde existe solo un núcleo en general para cada lenguaje, SQL es un lenguaje que tiene distintas versiones, a estas se les suele llamar \textbf{dialectos}, por ejemplo PL/SQL, MySQL, PostgreSQL, etc., aqui se utilizará el dialecto de SQL implementado en los productos y servicios de Microsoft como SQL Server o Azure,el cual es conocido como Transact-SQL o T-SQL. T-SQL.
"""

IMG_4_PATH = "/home/gustavo/SS/SQL-Server.png"

# --- Slide 5
SUBTITLE_5 = r"\subsection*{Bases de Datos Relacionales}"

# --- Slide 6
CONTENT_6A = r"""
\vskip 5pt
\noindent
Usualmente en una base de datos no tenemos una sola tabla, sino muchas tablas, y cuando estas tablas se relacionan entre sí decimos que son tablas relacionales o que son \textbf{relaciones}
"""

CONTENT_6B = r"""
\vskip 10pt
\noindent
Las tablas almacenadas en una base de datos son representaciones de una entidad. Una \textbf{entidad} puede referirse a cualquier cosa como autos, personas, etc. Y resulta que cada tabla debe o debería ser diseñada para contener información de un tipo particular de cosa, o una entidad.
"""

IMG_6A_PATH = "/home/gustavo/SS/Tablas.png"   
IMG_6B_PATH = "/home/gustavo/SS/Entidad.png"  

IMG_6A_WIDTH_FRAC = 0.8 
IMG_6B_WIDTH_FRAC = 0.8
MAX_IMG_HEIGHT_FRAC = 0.5
MIN_IMG_WIDTH_FRAC = 0.5  

IMG_5A_WIDTH_FRAC = 1.0
IMG_5B_WIDTH_FRAC = 1.0

# --- Slide 7
CONTENT_7 = r"""
Una relación o tabla suele tener dos estructuras básicas que son las columnas y las entradas (o registros). 
A lo que comúnmente le llamamos columnas también recibe el nombre de \textbf{dominio, atributo o campo,} y 
cada dominio lo que hace es contener atributos de la entidad de la tabla.
"""
IMG_7_PATH = "/home/gustavo/SS/entradas.png"   
IMG_7_WIDTH_FRAC = 0.8                    
MAX_IMG7_HEIGHT_FRAC = 0.6             

# --- Slide 8
CONTENT_8A = r"""
Por ejemplo, si nuestra entidad son Personas, la tabla correspondiente podría contener dominios como: ID, Nombre, Edad, entre otros.  Pero no todos los campos son igual de importantes o tienen las mismas características, y el campo más importante en una relación es lo que se conoce como llave primaria (Primary Key). 
\vskip 10pt 
\noindent 
Supón una tabla \texttt{VENTAS}:
\vskip 5pt
"""

TABLE_8 = r"""
\begin{tabular}{@{} l l l r @{}}
\hline
\textbf{Id venta} & \textbf{Fecha} & \textbf{Id producto} & \textbf{Cantidad} \\
\hline
\texttt{V001} & 2025-10-24 & \texttt{A10167} & 5 \\
\texttt{V002} & 2025-10-24 & \texttt{A10168} & 2 \\
\hline
\end{tabular}
"""

CONTENT_8B = r"""
\vskip 10pt
\noindent
Aqui la llave primaria es  \textit{Id venta}, ya que es un campo que identifica de manera única al producto. Cuando tomamos la llave primaria de una tabla en otra tabla, esta recibe el nombre de llave foránea (foreign key), en la tabla esta es \textit{Id Producto}.
"""

TABLE_8_SCALE = 1.00   

# --- Slide 9
CONTENT_9 = r"""
El objetivo de tener una base relacional es que no exista duplicación. Así, tenemos una tabla de productos, una tabla de ventas, y para obtener detalles de cada uno de los productos podemos usar la tabla de productos y no es necesario almacenarlos en las de ventas. De esta forma también optimizamos el almacenamiento de datos. Y nuestro objetivo al aprender SQL deberá ser entender cómo funcionan estas relaciones.
\vskip 10pt
\noindent
Definidos los conceptos de entidad y relaciones y su estructura podemos entrar a los \textbf{gráficos de entidad-relación}, que nos ayuda a representar gráficamente los enlaces en una base de datos relacional. A continuación, tenemos el gráfico de entidad-relación de la base de datos que usaremos de aqui en adelante.\\
"""
# --- Slide 10
IMG_10_PATH = "/home/gustavo/SS/Grafico Entidad Relacion.png"  
IMG_10_FIT_PAD = 0.96   
CAPTION_10 = r"""
Este diagrama contiene las relaciones de cada entidad en la base de datos, el esquema al que pertenecen, los campos que contienen, un icono lateral identifica a las llaves primarias y a las llaves foráneas, y se representan las conexiones que existen entre las relaciones, así como la dirección de estas conexiones, en esta representación también se indica mediante iconos circulares el orden de conexión (si es $1:1$, leído uno a uno, o si es $1:n$, o $n:n$).
"""
CAPTION_10_MAX_WIDTH_FRAC = 0.96  
CAPTION_10_BUFF = 0.5           
WAIT_BEFORE_CAPTION = 3.0         

# --- Slide 11
SUBTITLE_11 = r"""
\vskip 15pt
\subsection*{Esquemas y Objetos}
\vskip 10pt
"""

# ---------- Slide 12
CONTENT_12 = r"""
Una base de datos es un conjunto de objetos, principalmente tablas, que almacenan información. Estas tablas se agrupan dentro de esquemas, los cuales funcionan como contenedores o divisiones lógicas que permiten organizar los objetos según su propósito. Por ejemplo, una misma base de datos puede tener un esquema llamado Exportaciones y otro llamado Importaciones, cada uno con sus propias tablas.\\
"""
IMG_12_PATH = "/home/gustavo/SS/Servidor.png"

S12_TEXT_MAX_W = 0.78   
S12_TEXT_MAX_H = 0.46   
S12_TOP_BUFF   = 0.42   

S12_IMG_W_TGT  = 0.6   
S12_IMG_W_MIN  = 0.2   
S12_IMG_W_MAX  = 0.7   
S12_IMG_H_MAX  = 0.5  
S12_GAP        = 0.5  
S12_BOTTOM_PAD = 0.4  


# --- Slide 13
CONTENT_13A = r"""
Aunque nombrar objetos en SQL puede hacerse de distintas formas, una práctica recomendada es usar la estructura:
"""

CODE_13 = r"""
\begin{center}
\begin{minipage}{0.8\linewidth}
\begin{lstlisting}[basicstyle=\ttfamily\small\color{blue}, frame=none, showstringspaces=false]
[Esquema].[Objeto]
\end{lstlisting}
\end{minipage}
\end{center}
"""

CONTENT_13B = r"""
Especialmente cuando se trabaja con sistemas como SQL Server que gestionan varias bases de datos a la vez. Sin embargo, no siempre es obligatorio incluir el nombre del esquema; en bases de datos pequeñas o con un solo esquema, el nombre del objeto suele bastar.\\
\noindent
Al crear nombres para bases de datos, esquemas, tablas o campos, conviene evitar espacios o caracteres especiales y preferir nombres claros que describan el contenido del objeto.
"""

CODE_13_MAX_W_FRAC = 0.90   
GAP_TEXT_CODE      = 0.45   
GAP_CODE_TEXT      = 0.45   

# --- Slide 14
SUBTITLE_14 = r"""
\vskip 15pt
\subsection*{Clasificación Lingüistica de SQL}
\vskip 10pt
"""
# --- Slide 15
CONTENT_15 = r"""
El lenguaje SQL se divide en varios sublenguajes según su propósito dentro de las bases de datos:

\begin{enumerate}
  \item \textbf{DML (Data Manipulation Language):} Permite consultar y modificar datos. Sus comandos principales son \textcolor{blue}{SELECT}, \textcolor{blue}{INSERT}, \textcolor{blue}{UPDATE} y \textcolor{blue}{DELETE}.

  \item \textbf{DDL (Data Definition Language):} Define y gestiona la estructura de los objetos de la base de datos mediante comandos como \textcolor{blue}{CREATE}, \textcolor{blue}{ALTER} y \textcolor{blue}{DROP}.

  \item \textbf{DCL (Data Control Language):} Administra los permisos y la seguridad con \textcolor{blue}{GRANT}, \textcolor{blue}{REVOKE} y \textcolor{blue}{DENY}.

  \item \textbf{TCL (Transaction Control Language):} Controla las transacciones y garantiza la integridad de los datos con \textcolor{blue}{BEGIN}, \textcolor{blue}{COMMIT}, \textcolor{blue}{ROLLBACK} y \textcolor{blue}{SAVE}.
\end{enumerate}
"""
LIST15_MAX_W_FRAC = 0.95   
LIST15_MAX_H_FRAC = 0.90 

# --- Slide 16
CONTENT_16A = r"""
Algunos autores separan el DML en \textbf{DML} y \textbf{DQL (Data Query Language)}, considerando que \textcolor{blue}{SELECT} pertenece a este último, aunque generalmente se agrupan juntos.
"""

CONTENT_16B = r"""
En la práctica, el \textbf{DML} es el más utilizado, ya que permite interactuar directamente con los datos almacenados. Por su frecuencia y relevancia, los comandos DML, especialmente \textcolor{blue}{SELECT}, son la base del aprendizaje y uso cotidiano del lenguaje SQL.
"""
TEXT16_MAX_W_FRAC = 0.90   
TEXT16_MAX_H_FRAC = 0.85   
GAP_16             = 0.45 

# --- Slide 17
SUBTITLE_17 = r"""
\subsection*{Tipos de Datos}
"""

# --- Slide 18
CONTENT_18A = r"""
Existen dos tipos de datos, los estructurados y no estructurados. Los datos estructurados son todos aquellos tipos de datos que se encuentran definidos de manera clara y concisa, con un formato estandarizado, presentando un patrón u orden entre ellos de tal manera que son fáciles de organizar y de consultar, tanto por humanos como por maquinas (p. ej., nombres, números de teléfono, códigos postales).\\
"""

CONTENT_18B = r"""
Los datos estructurados suelen ser almacenados en bases de datos relacionales, y son accesibles usando SQL.\\
"""


TEXT18_MAX_W_FRAC = 0.90  
TEXT18_MAX_H_FRAC = 0.84  
GAP_18             = 0.45  

# --- Slide 19
CONTENT_19A = r"""
Por otro lado, todo lo que no entra en la definición anterior suele ser considerado como datos no estructurados (p. ej., texto, audio, imagen). Existe una clasificación intermedia llamada datos semiestructurados (p. ej., JSON, XML, HTML)\\
"""

CONTENT_19B = r"""
Tanto los datos no estructurados como los semiestructurados suelen ser almacenados en un tipo de base de datos no relacional, entre estas se encuentras las bases que trabajan con el llamado NoSQL. Las bases NoSQL no realizan una organización separada de datos, y suelen ser usadas cuando los datos no pueden ser encapsulados en tablas estructuradas, y no pueden ser consultados o mostrados de manera simple. En adelante, se trabajará con los datos estructurados.
"""

TEXT19_MAX_W_FRAC = 0.90 
TEXT19_MAX_H_FRAC = 0.86   
GAP_19             = 0.45 


# --- Slide 20
CONTENT_20A = r"""
Los datos estructurados suelen tener muchas clasificaciones, por lo cual es crucial tener bien definidos los tipos de datos con los que se esten trabajando para optimizar procesos, servicios, tiempo y sistemas.\\
El tipo de datos es quizá la restricción o \textit{constraint} más fundamental de nuestros datos y tablas. La siguiente tabla muestra algunos de los tipos de datos que se tienen en T-SQL y su clasificación.
"""

TABLE_20 = r"""
\begin{table}[ht]
\centering
\footnotesize
\begin{tabular}{|c|c|c|c|c|c|}
\hline
\shortstack{\textbf{Numéricos}\\\textbf{Exactos}} &
\shortstack{\textbf{Numéricos}\\\textbf{Aproximados}} &
\textbf{Caracteres} &
\textbf{Tiempo y Fechas} &
\textbf{Binarios} &
\textbf{Otros} \\
\hline
tinyint         & float  & char      & date              & binary     & cursor            \\
smallint        & real   & varchar   & time              & varbinary  & hierarchyid       \\
int             &        & text      & datetime          & image      & sql\_variant      \\
bigint          &        & nchar     & datetime2         &            & table             \\
bit             &        & nvarchar  & smalldatetime     &            & timestamp         \\
decimal/numeric &        & ntext     & datetimeoffset    &            & uniqueidentifier  \\
numeric         &        &           &                   &            & xml               \\
money           &        &           &                   &            & geography         \\
smallmoney      &        &           &                   &            & geometry          \\
\hline
\end{tabular}
\end{table}
"""

CONTENT_20C = r"""
Los datos numéricos permiten distinguir entre valores \textbf{exactos} (enteros y decimales) y \textbf{aproximados} (flotantes). Los tipos exactos incluyen \textcolor{blue}{tinyint}, \textcolor{blue}{smallint}, \textcolor{blue}{int}, \textcolor{blue}{bigint} y \textcolor{blue}{decimal/numeric(p,s)}, usados cuando se conoce la cantidad de decimales con precisión; los monetarios (\textcolor{blue}{money}, \textcolor{blue}{smallmoney}) también son exactos. En cambio, \textcolor{blue}{float} y \textcolor{blue}{real} se emplean cuando los decimales pueden variar o los datos provienen de mediciones.
"""


S20_TEXT_MAX_W = 0.60  
S20_TEXT_MAX_H = 0.36   
S20_TOP_BUFF   = 0.36   

S20_TBL_W_MAX  = 0.90   
S20_TBL_H_MAX  = 0.54   
S20_GAP        = 0.28   
S20_BOTTOM_PAD = 0.20   

S20_WAIT_BEFORE = 3.0   


S20_AFTER_TOP_BUFF   = 0.7  
S20_AFTER_GAP        = 0.48  
S20_AFTER_TBL_H_MAX  = 0.46  
S20_BOTTOM_PAD_AFTER = 0.18  

S20_TEXT2_MAX_W  = 0.75  
S20_TEXT2_MAX_H  = 0.45 
S20_TEXT2_MIN_SF = 0.46  

# --- Slide 21
CONTENT_21 = r"""
El tipo entero varía según el rango y el espacio de almacenamiento necesario: \textcolor{blue}{tinyint} (0--255), \textcolor{blue}{smallint} ($-32,768, 32,767$), \textcolor{blue}{int} ($-2^{31},2^{31}-1$) y \textcolor{blue}{bigint} ($- 2^{63},2^{63}-1$). Los datos de tipo decimal o \textcolor{blue}{numeric} permiten precisión definida mediante \textcolor{blue}{(p,s)}, donde \textcolor{purple}{p} indica la cantidad total de dígitos (máximo 38) e incluye tanto a los números a la derecha como a la izquierda del punto decimal y \textcolor{purple}{s} son los decimales a la derecha del punto decimal; el valor de \textcolor{purple}{s} se le resta a \textcolor{purple}{p} para determinar el número de dígitos máximo que irá a la izquierda del punto decimal, y siempre se cumple que $0 \leq s \leq p $. Cuando se usa su precisión máxima, un numeric puede tomar valores entre $10^{38}$ hasta $10^{38}-1$.
"""

S21_MAX_W_FRAC = 0.90 
S21_MAX_H_FRAC = 0.78  
S21_MIN_SCALE  = 0.60   

# --- Slide 22 
CONTENT_22A = r"""
Los tipos de datos de \textbf{caracteres} (\textcolor{blue}{char}, \textcolor{blue}{varchar}, \textcolor{blue}{nchar}, \textcolor{blue}{nvarchar}) almacenan texto; los prefijos \textcolor{purple}{var} y \textcolor{purple}{n} indican caracteres variables en un rango y el largo del dato en bytes, respectivamente.
"""
CONTENT_22B = r"""
\noindent
En los \textbf{datos de fecha y hora}, SQL ofrece \textcolor{blue}{date}, \textcolor{blue}{time}, \textcolor{blue}{smalldatetime}, \textcolor{blue}{datetime}, \textcolor{blue}{datetime2} (con mayor rango y precisión) y \textcolor{blue}{datetimeoffset} (incluye zona horaria).
"""
TABLE_22 = r"""
\footnotesize
\begin{tabular}{|c|c|}
\hline
\textbf{Data Type} & \textbf{Output} \\
\hline
time & 12:35:29.1234567 \\
\hline
date & 2007-05-08 \\
\hline
smalldatetime & 2007-05-08 12:35:00 \\
\hline
datetime & 2007-05-08 \newline 12:35:29.123 \\
\hline
datetime2 & 2007-05-08 \newline 12:35:29.1234567 \\
\hline
datetimeoffset & 2007-05-08 \newline 12:35:29.1234567 \newline +12:15 \\
\hline
\end{tabular}
"""

CONTENT_22C = r"""
SQL Server también soporta tipos menos comunes como \textcolor{blue}{binarios}, \textcolor{blue}{XML}, \textcolor{blue}{geográficos}. Comprender las diferencias y compatibilidades entre tipos permite saber cuándo usar cada uno, evita errores y mejora el rendimiento optimizando tanto la estructura como la eficiencia de las bases de datos.
"""

S22_TXT_MAX_W   = 0.92
S22_TXT_MAX_H_A = 0.26
S22_TXT_MAX_H_B = 0.22
S22_TBL_W_MAX   = 0.92
S22_TBL_H_MAX   = 0.42
S22_MIN_SF_TXT  = 0.60
S22_MIN_SF_TBL  = 0.55
S22_GAP_AB      = 0.22
S22_GAP_BT      = 0.28
S22_WAIT_AFTER_TABLE = 3.0

# --- Slide 23
CONTENT_23_SUB = r"\subsection*{NULLS}"

S23_MAX_W = 0.90  
S23_MAX_H = 0.18   

# --- Slide 24
CONTENT_24A = r"""
El valor \textbf{NULL} representa un dato desconocido o ausente dentro de una base de datos, distinto de un valor vacío o cero. Indica que el valor existe, pero no se conoce. Por ejemplo, si en una tabla de pacientes uno no tiene edad registrada, no significa que tenga cero años, sino que su edad es \textbf{desconocida}. 
"""

CONTENT_24B = r"""
\noindent
Toda operación que involucra un \textbf{NULL} devuelve otro \textbf{NULL}, porque el resultado también es desconocido. Así, si sumamos un número con un \textbf{NULL}, el resultado es \textbf{NULL}; del mismo modo, concatenar texto con un \textbf{NULL} también produce \textbf{NULL}. Aunque algunos sistemas permiten reemplazar los valores \textbf{NULL} por ceros o cadenas vacías, esto se considera una mala práctica, ya que rompe el estándar y puede generar inconsistencias.
"""

S24_MAX_W_FRAC = 0.90  
S24_MAX_H_A    = 0.46  
S24_MAX_H_B    = 0.42   
S24_GAP        = 0.42   

# --- Slide 25
CONTENT_25A = r"""
Las comparaciones con \textbf{NULL} son especiales: cualquier comparación entre \textbf{NULL} y otro valor devuelve \textbf{FALSE} o \textbf{NULL}, porque no se puede determinar igualdad entre valores desconocidos. Sin embargo, se puede comprobar si un valor es \textbf{NULL} mediante el operador \textbf{IS NULL} (por ejemplo: \texttt{Precio IS NULL}), lo cual devuelve \textbf{TRUE} si el valor efectivamente es nulo.
"""

CONTENT_25B = r"""
\noindent
Un dominio que permite valores \textbf{NULL} se llama \textbf{nullable}, y es importante definir en el diseño de la base de datos qué campos pueden admitirlos. Llaves primarias o campos obligatorios no deberían permitirlos, para garantizar integridad y consistencia.
"""

# --- Slide 26
CONTENT_26 = r"""
En otros lenguajes de programación existen conceptos similares, como \textbf{NA (Not Available)} y \textbf{NaN (Not A Number)}. El primero suele representar datos faltantes, mientras que el segundo se usa para resultados indefinidos en operaciones numéricas (por ejemplo, dividir $0/0$). Aunque pueden parecer equivalentes, su interpretación depende del lenguaje, y en SQL es esencial mantener la semántica formal del \textbf{NULL} como indicador de valor desconocido, no como número o cadena vacía.
"""
S26_MAX_W_FRAC = 0.90   
S26_MAX_H_FRAC = 0.78   
S26_MIN_SCALE  = 0.62   

S25_MAX_W_FRAC = 0.90   
S25_MAX_H_A    = 0.46   
S25_MAX_H_B    = 0.40   
S25_GAP        = 0.42   


class IntroduccionSQL(BaseSlide):
    def construct(self):
        SAFE_X_MARGIN = 1.0
        SAFE_Y_MARGIN = 0.8
        GUTTER = 1.4
        frame_w = config.frame_width
        frame_h = config.frame_height
        allowed_w = frame_w - 2*SAFE_X_MARGIN
        allowed_h = frame_h - 2*SAFE_Y_MARGIN

        def set_width_safe(mob, w):
            try:
                mob.set(width=w)
            except Exception:
                mob.scale_to_fit_width(w)

        def fit_group(group):
            scale_w = allowed_w / group.width if group.width > allowed_w else 1.0
            scale_h = allowed_h / group.height if group.height > allowed_h else 1.0
            scale_factor = min(scale_w, scale_h)
            if scale_factor < 1.0:
                group.scale(scale_factor)
            group.move_to(ORIGIN)

        # ----------------- Slide 1 

        title = write_block(TITLE_1, scale=1.0)
        if title.width > (allowed_w * 0.65):
            set_width_safe(title, allowed_w * 0.65)
        title.move_to(ORIGIN)
        self.play(Write(title, run_time=WRITE_MEDIUM_RT))
        self.pause(0.4)
        self.disappear(title)

        # ----------------- Slide 2 
        p2 = write_block(CONTENT_2)
        try:
            fit_text_block(
                p2,
                max_w=allowed_w * S2_TEXT_MAX_W,
                max_h=allowed_h * S2_TEXT_MAX_H,
                pad=0.04,
                min_sf=0.62
            )
        except NameError:
            cap_w = allowed_w * S2_TEXT_MAX_W
            if p2.width > cap_w:
                p2.scale(cap_w / p2.width)
            cap_h = allowed_h * S2_TEXT_MAX_H
            if p2.height > cap_h:
                p2.scale(cap_h / p2.height)

        p2.to_edge(UP, buff=S2_TOP_BUFF).set_x(0)

        img2 = None
        try:
            pth = Path(IMG_2_PATH)
            if pth.exists():
                img2 = ImageMobject(str(pth))
        except Exception:
            img2 = None

        g_txt = p2.copy()
        g_img = img2.copy() if img2 is not None else None

        if g_img is not None:
            target_w = allowed_w * S2_IMG_W_FRAC
            if g_img.width != 0:
                g_img.scale(target_w / g_img.width)

            hard_h = allowed_h * S2_IMG_MAX_H
            free_h = allowed_h - g_txt.height - S2_GAP_TXT_IMG - S2_BOTTOM_PAD
            free_h = max(free_h, 0.0)
            lim_h  = min(hard_h, free_h) if free_h > 0 else hard_h
            if g_img.height > lim_h and lim_h > 0:
                g_img.scale(lim_h / g_img.height)
            g_img.next_to(g_txt, DOWN, buff=S2_GAP_TXT_IMG).set_x(0)


        ghost = Group(g_txt, *( [g_img] if g_img is not None else [] ))
        sw = allowed_w / ghost.width  if ghost.width  > allowed_w else 1.0
        sh = allowed_h / ghost.height if ghost.height > allowed_h else 1.0
        sf = min(sw, sh, 1.0)
        if sf < 1.0:
            ghost.scale(sf)
        ghost.move_to(ORIGIN)

        p2.move_to(g_txt.get_center())
        if img2 is not None:
            img2.scale(g_img.width / img2.width)
            img2.move_to(g_img.get_center())

        self.play(Write(p2, run_time=WRITE_MEDIUM_RT))
        if img2 is not None:
            self.play(FadeIn(img2, shift=0.4*DOWN), run_time=0.9)
            self.pause(0.3)

        self.fade_out_all(p2, img2 if img2 is not None else None)


        # ----------------- Slide 3 
        body3 = write_block(CONTENT_3, scale=1.0)
        if body3.width > allowed_w:
            set_width_safe(body3, allowed_w)

        tmp3 = VGroup(body3)
        sw = allowed_w / tmp3.width  if tmp3.width  > allowed_w else 1.0
        sh = allowed_h / tmp3.height if tmp3.height > allowed_h else 1.0
        sf = min(sw, sh)
        if sf < 1.0: tmp3.scale(sf)
        tmp3.move_to(ORIGIN)

        self.play(Write(body3, run_time=WRITE_MEDIUM_RT))
        self.pause(0.4)

        self.fade_out_all(body3)

        # ----------------- Slide 4 
        body4 = write_block(CONTENT_4, scale=1.0)
        if body4.width > allowed_w:
            set_width_safe(body4, allowed_w)

        body4.move_to(ORIGIN)
        self.play(Write(body4, run_time=WRITE_MEDIUM_RT))
        self.pause(0.1)

        img4 = None
        try:
            p = Path(IMG_4_PATH)
            if p.exists():
                img4 = ImageMobject(str(p))
                if img4.width > allowed_w:
                    img4.width = allowed_w
        except Exception:
            img4 = None

        if img4 is not None:
            ghost = body4.copy()                   
            ghost.move_to(ORIGIN + 0.6*UP)           
            img4_temp = img4.copy()
            img4_temp.next_to(ghost, DOWN, buff=0.5) 

            final_group = Group(ghost, img4_temp)
            sw = allowed_w / final_group.width  if final_group.width  > allowed_w else 1.0
            sh = allowed_h / final_group.height if final_group.height > allowed_h else 1.0
            sf = min(sw, sh)
            if sf < 1.0:
                final_group.scale(sf)
            final_group.move_to(ORIGIN)

            body4_final_center = ghost.get_center()
            img4_final_center  = img4_temp.get_center()

            img4.move_to(img4_final_center)
            self.play(
                body4.animate.move_to(body4_final_center),
                FadeIn(img4, shift=0.6*DOWN),
                run_time=0.9
            )
            self.pause(0.5)

        self.fade_out_all(body4, img4 if img4 is not None else None)

# ----------------- Slide 5 
        subtitle5 = write_block(SUBTITLE_5)
        subtitle5.move_to(ORIGIN)  
        self.play(Write(subtitle5, run_time=WRITE_MEDIUM_RT))
        self.pause(0.5)
        self.fade_out_all(subtitle5)  

# ----------------- Slide 6 
        para6a = write_block(CONTENT_6A)
        para6b = write_block(CONTENT_6B)

        img6a = img6b = None
        try:
            p = Path(IMG_6A_PATH)
            if p.exists(): img6a = ImageMobject(str(p))
        except Exception: img6a = None
        try:
            p = Path(IMG_6B_PATH)
            if p.exists(): img6b = ImageMobject(str(p))
        except Exception: img6b = None

        def autosize_two_images_stack(img_top, img_bot, w_allowed, h_allowed, p_top, p_bot,
                                    frac_top, frac_bot, max_h_frac, min_w_frac):
            if img_top is not None:
                img_top.width = w_allowed * frac_top
            if img_bot is not None:
                img_bot.width = w_allowed * frac_bot

            def cap_max_height(img):
                if img is None: return
                max_h = h_allowed * max_h_frac
                if img.height > max_h:
                    img.scale(max_h / img.height)
            cap_max_height(img_top); cap_max_height(img_bot)

            def total_height():
                h = 0.0
                h += p_top.height
                if img_top is not None: h += 0.5 + img_top.height
                h += 0.6 + p_bot.height
                if img_bot is not None: h += 0.5 + img_bot.height
                return h

            for _ in range(10):
                if total_height() <= h_allowed: break
                scaled_any = False
                for img, frac in ((img_top, frac_top), (img_bot, frac_bot)):
                    if img is None: continue
                    min_w = w_allowed * min_w_frac
                    if img.width > min_w:
                        img.scale(0.90)  
                        scaled_any = True
                if not scaled_any: break  

        autosize_two_images_stack(img6a, img6b, allowed_w, allowed_h,
                                para6a, para6b,
                                IMG_6A_WIDTH_FRAC, IMG_6B_WIDTH_FRAC,
                                MAX_IMG_HEIGHT_FRAC, MIN_IMG_WIDTH_FRAC)

        g_para6a = para6a.copy()
        g_para6b = para6b.copy()
        g_img6a  = img6a.copy() if img6a is not None else None
        g_img6b  = img6b.copy() if img6b is not None else None

        g_para6a.move_to(ORIGIN + 0.8*UP)
        if g_img6a is not None:
            g_img6a.next_to(g_para6a, DOWN, buff=0.5).set_x(0)
        g_para6b.next_to((g_img6a if g_img6a is not None else g_para6a), DOWN, buff=0.6).set_x(0)
        if g_img6b is not None:
            g_img6b.next_to(g_para6b, DOWN, buff=0.5).set_x(0)

        ghost_elems = [g_para6a, g_para6b]
        if g_img6a is not None: ghost_elems.append(g_img6a)
        if g_img6b is not None: ghost_elems.append(g_img6b)
        ghost_grp = Group(*ghost_elems)

        sw = allowed_w / ghost_grp.width  if ghost_grp.width  > allowed_w else 1.0
        sh = allowed_h / ghost_grp.height if ghost_grp.height > allowed_h else 1.0
        sf = min(sw, sh)
        if sf < 1.0:
            ghost_grp.scale(sf)
        ghost_grp.move_to(ORIGIN)

        para6a_c = g_para6a.get_center()
        para6b_c = g_para6b.get_center()
        img6a_c  = g_img6a.get_center() if g_img6a is not None else None
        img6b_c  = g_img6b.get_center() if g_img6b is not None else None

        if sf < 1.0:
            for m in (para6a, para6b, img6a, img6b):
                if m is not None: m.scale(sf)

        para6a.move_to(para6a_c)
        self.play(Write(para6a, run_time=WRITE_MEDIUM_RT))
        self.pause(0.05)

        if img6a is not None:
            img6a.move_to(img6a_c)
            self.play(FadeIn(img6a, shift=0.6*DOWN), run_time=0.8)
            self.pause(0.05)

        para6b.move_to(para6b_c)
        self.play(Write(para6b, run_time=WRITE_MEDIUM_RT))
        self.pause(0.05)

        if img6b is not None:
            img6b.move_to(img6b_c)
            self.play(FadeIn(img6b, shift=0.6*DOWN), run_time=0.8)
            self.pause(0.4)

        self.fade_out_all(para6a, img6a if img6a else None, para6b, img6b if img6b else None)

        # ----------------- Slide 7 
        p7 = write_block(CONTENT_7)

        img7 = None
        try:
            p = Path(IMG_7_PATH)
            if p.exists():
                img7 = ImageMobject(str(p))
                img7.width = allowed_w * IMG_7_WIDTH_FRAC
                max_h7 = allowed_h * MAX_IMG7_HEIGHT_FRAC
                if img7.height > max_h7:
                    img7.scale(max_h7 / img7.height)
        except Exception:
            img7 = None

        g_p7   = p7.copy()
        g_img7 = img7.copy() if img7 is not None else None

        g_p7.move_to(ORIGIN + 0.6*UP)
        if g_img7 is not None:
            g_img7.next_to(g_p7, DOWN, buff=0.5).set_x(0)

        ghost_elems = [g_p7] + ([g_img7] if g_img7 is not None else [])
        ghost_grp = Group(*ghost_elems)

        sw = allowed_w / ghost_grp.width  if ghost_grp.width  > allowed_w else 1.0
        sh = allowed_h / ghost_grp.height if ghost_grp.height > allowed_h else 1.0
        sf = min(sw, sh)
        if sf < 1.0:
            ghost_grp.scale(sf)
        ghost_grp.move_to(ORIGIN)

        p7_c   = g_p7.get_center()
        img7_c = g_img7.get_center() if g_img7 is not None else None

        if sf < 1.0:
            p7.scale(sf)
            if img7 is not None:
                img7.scale(sf)

        p7.move_to(p7_c)
        self.play(Write(p7, run_time=WRITE_MEDIUM_RT))
        self.pause(0.05)

        if img7 is not None:
            img7.move_to(img7_c)
            self.play(FadeIn(img7, shift=0.6*DOWN), run_time=0.8) 
            self.pause(0.4)

        self.fade_out_all(p7, img7 if img7 is not None else None)

        # ----------------- Slide 8 
        p8a  = write_block(CONTENT_8A)
        tbl8 = Tex(TABLE_8, tex_template=tex_template)
        p8b  = write_block(CONTENT_8B)

        if TABLE_8_SCALE != 1.0:
            tbl8.scale(TABLE_8_SCALE)

        g_p8a  = p8a.copy()
        g_tbl8 = tbl8.copy()
        g_p8b  = p8b.copy()

        g_p8a.move_to(ORIGIN + 0.8*UP)
        g_tbl8.next_to(g_p8a, DOWN, buff=0.45).set_x(0)
        g_p8b.next_to(g_tbl8, DOWN, buff=0.55).set_x(0)

        ghost_grp = Group(g_p8a, g_tbl8, g_p8b)

        sw = allowed_w / ghost_grp.width  if ghost_grp.width  > allowed_w else 1.0
        sh = allowed_h / ghost_grp.height if ghost_grp.height > allowed_h else 1.0
        sf = min(sw, sh)
        if sf < 1.0:
            ghost_grp.scale(sf)
        ghost_grp.move_to(ORIGIN)

        p8a_c  = g_p8a.get_center()
        tbl8_c = g_tbl8.get_center()
        p8b_c  = g_p8b.get_center()

        if sf < 1.0:
            p8a.scale(sf); tbl8.scale(sf); p8b.scale(sf)

        p8a.move_to(p8a_c)
        self.play(Write(p8a, run_time=WRITE_MEDIUM_RT))
        self.pause(0.05)

        tbl8.move_to(tbl8_c)
        self.play(FadeIn(tbl8, shift=0.5*DOWN), run_time=0.8)  
        self.pause(0.05)

        p8b.move_to(p8b_c)
        self.play(Write(p8b, run_time=WRITE_MEDIUM_RT))
        self.pause(0.4)

        self.fade_out_all(p8a, tbl8, p8b)

        # ----------------- Slide 9 
        p9 = write_block(CONTENT_9)
        if p9.width > allowed_w:
            set_width_safe(p9, allowed_w)

        p9.move_to(ORIGIN)  
        self.play(Write(p9, run_time=WRITE_MEDIUM_RT))
        self.pause(0.4)
        self.fade_out_all(p9)

        # ----------------- Slide 10 
        img10 = None
        try:
            p = Path(IMG_10_PATH)
            if p.exists():
                img10 = ImageMobject(str(p))
        except Exception:
            img10 = None

        if img10 is not None:
            target_w = allowed_w * IMG_10_FIT_PAD
            target_h = allowed_h * IMG_10_FIT_PAD
            sf0 = min(target_w / img10.width, target_h / img10.height)
            if sf0 != 1.0:
                img10.scale(sf0)
            img10.move_to(ORIGIN)  

            self.play(FadeIn(img10, shift=0.4*DOWN), run_time=0.9)
            self.pause(WAIT_BEFORE_CAPTION)

            caption10 = write_block(CAPTION_10)
            cap_max_w = allowed_w * CAPTION_10_MAX_WIDTH_FRAC
            if caption10.width > cap_max_w:
                try: caption10.set(width=cap_max_w)
                except Exception: caption10.scale_to_fit_width(cap_max_w)

            g_img  = img10.copy()
            g_cap  = caption10.copy()

            g_cap.next_to(g_img, DOWN, buff=CAPTION_10_BUFF).set_x(0)

            def total_size():
                grp = Group(g_img, g_cap)
                return grp.width, grp.height

            for _ in range(12):
                gw, gh = total_size()
                if gw <= allowed_w and gh <= allowed_h:
                    break
                fx = allowed_w / gw if gw > allowed_w else 1.0
                fy = allowed_h / gh if gh > allowed_h else 1.0
                f  = min(fx, fy, 0.96)  
                if f >= 1.0:
                    f = 0.96
                g_img.scale(f)
                g_cap.next_to(g_img, DOWN, buff=CAPTION_10_BUFF).set_x(0)

            Group(g_img, g_cap).move_to(ORIGIN)

            self.play(
                img10.animate.move_to(g_img.get_center()).scale(g_img.width / img10.width),
                run_time=0.9
            )
            caption10.move_to(g_cap.get_center())
            self.play(Write(caption10, run_time=WRITE_MEDIUM_RT))
            self.pause(0.5)

            self.fade_out_all(img10, caption10)

        # ----------------- Slide 11 
        sub11 = write_block(SUBTITLE_11)
        if sub11.width > allowed_w:
            try: sub11.set(width=allowed_w)
            except Exception: sub11.scale_to_fit_width(allowed_w)

        sub11.move_to(ORIGIN)  
        self.play(Write(sub11, run_time=WRITE_MEDIUM_RT))
        self.pause(0.5)

        self.fade_out_all(sub11)

        # ----------------- Slide 12 
        txt12 = write_block(CONTENT_12)
        g_txt12 = txt12.copy()
        fit_text_block(
            g_txt12,
            max_w=allowed_w * S12_TEXT_MAX_W,
            max_h=allowed_h * S12_TEXT_MAX_H,
            pad=0.04,           
            min_sf=0.60        
        )
        g_txt12.to_edge(UP, buff=S12_TOP_BUFF).set_x(0)
        img12 = None
        try:
            p = Path(IMG_12_PATH)
            if p.exists():
                img12 = ImageMobject(str(p))
        except Exception:
            img12 = None

        g_img12 = img12.copy() if img12 is not None else None
        if g_img12 is not None:
            target_w = allowed_w * S12_IMG_W_TGT
            min_w    = allowed_w * S12_IMG_W_MIN
            max_w    = allowed_w * S12_IMG_W_MAX
            if g_img12.width != 0:
                g_img12.scale(target_w / g_img12.width)

            if g_img12.width > max_w:
                g_img12.scale(max_w / g_img12.width)
            if g_img12.width < min_w:
                g_img12.scale(min_w / g_img12.width)

            hard_h = allowed_h * S12_IMG_H_MAX
            free_h = allowed_h - g_txt12.height - S12_GAP - S12_BOTTOM_PAD
            free_h = max(free_h, 0.0)
            lim_h  = min(hard_h, free_h) if free_h > 0 else hard_h
            if g_img12.height > lim_h and lim_h > 0:
                g_img12.scale(lim_h / g_img12.height)
            g_img12.next_to(g_txt12, DOWN, buff=S12_GAP).set_x(0)

        ghost = Group(g_txt12, *( [g_img12] if g_img12 is not None else [] ))
        for _ in range(6):
            if ghost.width <= allowed_w and ghost.height <= allowed_h:
                break
            if g_img12 is not None and g_img12.width > allowed_w*0.30:
                g_img12.scale(0.94)
                g_img12.next_to(g_txt12, DOWN, buff=S12_GAP).set_x(0)
                ghost = Group(g_txt12, g_img12)
            else:
                g_txt12.scale(0.96)
                g_txt12.to_edge(UP, buff=S12_TOP_BUFF).set_x(0)
                if g_img12 is not None:
                    g_img12.next_to(g_txt12, DOWN, buff=S12_GAP).set_x(0)
                ghost = Group(g_txt12, *( [g_img12] if g_img12 is not None else [] ))

        ghost.move_to(ORIGIN)

        txt12.move_to(g_txt12.get_center()).scale(g_txt12.width / txt12.width)
        self.play(Write(txt12, run_time=WRITE_MEDIUM_RT)); self.pause(0.05)

        if img12 is not None:
            img12.move_to(g_img12.get_center()).scale(g_img12.width / img12.width)
            self.play(FadeIn(img12, shift=0.5*DOWN), run_time=0.8); self.pause(0.4)

        self.fade_out_all(txt12, img12 if img12 is not None else None)

        # ----------------- Slide 13 
        p13a  = write_block(CONTENT_13A)
        code13 = Tex(CODE_13, tex_template=tex_template)
        p13b  = write_block(CONTENT_13B)

        g_p13a  = p13a.copy()
        g_code  = code13.copy()
        g_p13b  = p13b.copy()

        cap_w = allowed_w * CODE_13_MAX_W_FRAC
        if g_code.width > cap_w:
            g_code.scale(cap_w / g_code.width)

        g_p13a.move_to(ORIGIN + 0.6*UP).set_x(0)
        g_code.next_to(g_p13a, DOWN, buff=GAP_TEXT_CODE).set_x(0)
        g_p13b.next_to(g_code, DOWN, buff=GAP_CODE_TEXT).set_x(0)

        ghost = Group(g_p13a, g_code, g_p13b)

        sw = allowed_w / ghost.width  if ghost.width  > allowed_w else 1.0
        sh = allowed_h / ghost.height if ghost.height > allowed_h else 1.0
        sf = min(sw, sh)
        if sf < 1.0:
            ghost.scale(sf)
        ghost.move_to(ORIGIN)

        p13a_c  = g_p13a.get_center()
        code_c  = g_code.get_center()
        p13b_c  = g_p13b.get_center()

        if sf < 1.0:
            p13a.scale(sf)
            code13.scale(sf)
            p13b.scale(sf)
        p13a.move_to(p13a_c)
        self.play(Write(p13a, run_time=WRITE_MEDIUM_RT))
        self.pause(0.05)

        code13.move_to(code_c)
        self.play(FadeIn(code13, shift=0.4*DOWN), run_time=0.8)
        self.pause(0.05)

        p13b.move_to(p13b_c)
        self.play(Write(p13b, run_time=WRITE_MEDIUM_RT))
        self.pause(0.4)
        self.fade_out_all(p13a, code13, p13b)

        # ----------------- Slide 14 
        sub14 = write_block(SUBTITLE_14)
        if sub14.width > allowed_w:
            try: sub14.set(width=allowed_w)
            except Exception: sub14.scale_to_fit_width(allowed_w)

        sub14.move_to(ORIGIN)  
        self.play(Write(sub14, run_time=WRITE_MEDIUM_RT))
        self.pause(0.5)

        self.fade_out_all(sub14)

        # ----------------- Slide 15 
        p15 = write_block(CONTENT_15)

        max_w = allowed_w * LIST15_MAX_W_FRAC
        max_h = allowed_h * LIST15_MAX_H_FRAC
        sf_w  = max_w / p15.width  if p15.width  > max_w else 1.0
        sf_h  = max_h / p15.height if p15.height > max_h else 1.0
        sf    = min(sf_w, sf_h)
        if sf < 1.0:
            p15.scale(sf)

        p15.move_to(ORIGIN) 
        self.play(Write(p15, run_time=WRITE_MEDIUM_RT))
        self.pause(0.4)
        self.fade_out_all(p15)

        # ----------------- Slide 16 
        p16a = write_block(CONTENT_16A)
        p16b = write_block(CONTENT_16B)

        cap_w = allowed_w * 0.88
        fit_text_block(p16a, max_w=cap_w, max_h=allowed_h*0.50, pad=0.04, min_sf=0.65)
        fit_text_block(p16b, max_w=cap_w, max_h=allowed_h*0.50, pad=0.04, min_sf=0.65)

        g16a = p16a.copy()
        g16b = p16b.copy()
        g16a.move_to(ORIGIN + 0.20*UP).set_x(0)
        g16b.next_to(g16a, DOWN, buff=0.40).set_x(0)

        ghost = Group(g16a, g16b)

        sw = allowed_w / ghost.width  if ghost.width  > allowed_w else 1.0
        sh = allowed_h / ghost.height if ghost.height > allowed_h else 1.0
        sf = min(sw, sh, 1.0)
        if sf < 1.0:
            ghost.scale(sf)

        ghost.move_to(ORIGIN)
        p16a.move_to(g16a.get_center()); p16b.move_to(g16b.get_center())

        # Animación
        self.play(Write(p16a, run_time=WRITE_MEDIUM_RT)); self.pause(0.05)
        self.play(Write(p16b, run_time=WRITE_MEDIUM_RT)); self.pause(0.4)
        self.fade_out_all(p16a, p16b)

        # ----------------- Slide 17 
        sub17 = write_block(SUBTITLE_17)

        if sub17.width > allowed_w:
            try: sub17.set(width=allowed_w)
            except Exception: sub17.scale_to_fit_width(allowed_w)

        sub17.move_to(ORIGIN)  
        self.play(Write(sub17, run_time=WRITE_MEDIUM_RT))
        self.pause(0.5)

        self.fade_out_all(sub17)

        # ----------------- Slide 18 
        p18a = write_block(CONTENT_18A)
        p18b = write_block(CONTENT_18B)

        cap_w = allowed_w * TEXT18_MAX_W_FRAC
        fit_text_block(p18a, max_w=cap_w, max_h=allowed_h*0.55, pad=0.04, min_sf=0.65)
        fit_text_block(p18b, max_w=cap_w, max_h=allowed_h*0.45, pad=0.04, min_sf=0.65)

        g18a = p18a.copy()
        g18b = p18b.copy()
        g18a.move_to(ORIGIN + 0.18*UP).set_x(0)
        g18b.next_to(g18a, DOWN, buff=GAP_18).set_x(0)

        ghost = Group(g18a, g18b)

        sw = allowed_w / ghost.width  if ghost.width  > allowed_w else 1.0
        sh = allowed_h / ghost.height if ghost.height > allowed_h else 1.0
        sf = min(sw, sh, 1.0)
        if sf < 1.0:
            ghost.scale(sf)
        ghost.move_to(ORIGIN)

        p18a.move_to(g18a.get_center())
        p18b.move_to(g18b.get_center())

        self.play(Write(p18a, run_time=WRITE_MEDIUM_RT)); self.pause(0.05)
        self.play(Write(p18b, run_time=WRITE_MEDIUM_RT)); self.pause(0.4)

        self.fade_out_all(p18a, p18b)

        # ----------------- Slide 19 
        p19a = write_block(CONTENT_19A)
        p19b = write_block(CONTENT_19B)

        cap_w = allowed_w * TEXT19_MAX_W_FRAC
        fit_text_block(p19a, max_w=cap_w, max_h=allowed_h*0.52, pad=0.04, min_sf=0.65)
        fit_text_block(p19b, max_w=cap_w, max_h=allowed_h*0.52, pad=0.04, min_sf=0.65)

        g19a = p19a.copy()
        g19b = p19b.copy()
        g19a.move_to(ORIGIN + 0.18*UP).set_x(0)
        g19b.next_to(g19a, DOWN, buff=GAP_19).set_x(0)

        ghost = Group(g19a, g19b)

        sw = allowed_w / ghost.width  if ghost.width  > allowed_w else 1.0
        sh = allowed_h / ghost.height if ghost.height > allowed_h else 1.0
        sf = min(sw, sh, 1.0)
        if sf < 1.0:
            ghost.scale(sf)
        ghost.move_to(ORIGIN)

        p19a.move_to(g19a.get_center())
        p19b.move_to(g19b.get_center())

        self.play(Write(p19a, run_time=WRITE_MEDIUM_RT)); self.pause(0.05)
        self.play(Write(p19b, run_time=WRITE_MEDIUM_RT)); self.pause(0.4)
        self.fade_out_all(p19a, p19b)

        # ----------------- Slide 20 
        p20a   = write_block(CONTENT_20A)
        tbl20  = write_block(TABLE_20)

        try:
            fit_text_block(
                p20a,
                max_w=allowed_w * S20_TEXT_MAX_W,
                max_h=allowed_h * S20_TEXT_MAX_H,
                pad=0.04,
                min_sf=0.62
            )
        except NameError:
            cap_w = allowed_w * S20_TEXT_MAX_W
            if p20a.width > cap_w:
                p20a.scale(cap_w / p20a.width)
        p20a.to_edge(UP, buff=S20_TOP_BUFF).set_x(0)

        cap_tbl_w = allowed_w * S20_TBL_W_MAX
        if tbl20.width > cap_tbl_w:
            tbl20.scale(cap_tbl_w / tbl20.width)

        hard_tbl_h = allowed_h * S20_TBL_H_MAX
        free_h     = allowed_h - p20a.height - S20_GAP - S20_BOTTOM_PAD
        free_h     = max(free_h, 0.0)
        lim_h      = min(hard_tbl_h, free_h) if free_h > 0 else hard_tbl_h
        if lim_h > 0 and tbl20.height > lim_h:
            tbl20.scale(lim_h / tbl20.height)

        tbl20.next_to(p20a, DOWN, buff=S20_GAP).set_x(0)

        ghost = Group(p20a, tbl20)
        for _ in range(6):
            if ghost.width <= allowed_w and ghost.height <= allowed_h:
                break
            if tbl20.width > allowed_w * 0.40:
                tbl20.scale(0.94)
                tbl20.next_to(p20a, DOWN, buff=S20_GAP).set_x(0)
            else:
                p20a.scale(0.96)
                p20a.to_edge(UP, buff=S20_TOP_BUFF).set_x(0)
                tbl20.next_to(p20a, DOWN, buff=S20_GAP).set_x(0)
            ghost = Group(p20a, tbl20)

        ghost.move_to(ORIGIN)

        self.play(Write(p20a, run_time=WRITE_MEDIUM_RT))
        self.pause(0.05)
        self.play(FadeIn(tbl20, shift=0.4*DOWN), run_time=0.9)
        self.pause(S20_WAIT_BEFORE)

        self.play(FadeOut(p20a), run_time=0.6)
        self.wait(0.05)

        p20c  = write_block(CONTENT_20C)
        g_tbl = tbl20.copy()
        g_tbl.to_edge(UP, buff=S20_AFTER_TOP_BUFF).set_x(0)

        if g_tbl.height > allowed_h * S20_AFTER_TBL_H_MAX:
            g_tbl.scale((allowed_h * S20_AFTER_TBL_H_MAX) / g_tbl.height)
            g_tbl.to_edge(UP, buff=S20_AFTER_TOP_BUFF).set_x(0)
        if g_tbl.width > allowed_w * 0.96:
            g_tbl.scale((allowed_w * 0.96) / g_tbl.width)
            g_tbl.to_edge(UP, buff=S20_AFTER_TOP_BUFF).set_x(0)

        g_p20c = p20c.copy()
        if g_p20c.width > allowed_w * S20_TEXT2_MAX_W:
            g_p20c.scale((allowed_w * S20_TEXT2_MAX_W) / g_p20c.width)

        free_h = allowed_h - g_tbl.height - S20_AFTER_GAP - S20_BOTTOM_PAD_AFTER
        free_h = max(free_h, 0.0)
        if g_p20c.height > free_h and g_p20c.height > 0:
            g_p20c.scale(min(1.0, free_h / g_p20c.height))

        g_p20c.next_to(g_tbl, DOWN, buff=S20_AFTER_GAP).set_x(0)

        self.play(
            tbl20.animate.move_to(g_tbl.get_center()).scale(g_tbl.width / tbl20.width),
            run_time=0.8
        )
        self.wait(0.05)  

        safe_sf = min(g_p20c.width / p20c.width, g_p20c.height / p20c.height)
        p20c.scale(safe_sf)
        p20c.move_to(g_p20c.get_center())

        self.play(Write(p20c, run_time=WRITE_MEDIUM_RT))
        self.pause(0.4)
        self.fade_out_all(tbl20, p20c)

        # ----------------- Slide 21 
        p21 = write_block(CONTENT_21)

        try:
            fit_text_block(
                p21,
                max_w=allowed_w * S21_MAX_W_FRAC,
                max_h=allowed_h * S21_MAX_H_FRAC,
                pad=0.04,
                min_sf=S21_MIN_SCALE
            )
        except NameError:
            cap_w = allowed_w * S21_MAX_W_FRAC
            if p21.width > cap_w:
                p21.scale(cap_w / p21.width)
            cap_h = allowed_h * S21_MAX_H_FRAC
            if p21.height > cap_h:
                p21.scale(cap_h / p21.height)

        p21.move_to(ORIGIN)

        self.play(Write(p21, run_time=WRITE_MEDIUM_RT))
        self.pause(0.4)
        self.fade_out_all(p21)

        # ----------------- Slide 22 
        p22a = write_block(CONTENT_22A)
        p22b = write_block(CONTENT_22B)
        t22  = write_block(TABLE_22)

        def _fit_txt(mob, max_w_frac, max_h_frac, min_sf=S22_MIN_SF_TXT):
            try:
                fit_text_block(
                    mob,
                    max_w=allowed_w * max_w_frac,
                    max_h=allowed_h * max_h_frac,
                    pad=0.04,
                    min_sf=min_sf
                )
            except NameError:
                cap_w = allowed_w * max_w_frac
                if mob.width > cap_w:
                    mob.scale(cap_w / mob.width)
                cap_h = allowed_h * max_h_frac
                if mob.height > cap_h:
                    mob.scale(cap_h / mob.height)

        _fit_txt(p22a, S22_TXT_MAX_W, S22_TXT_MAX_H_A)
        _fit_txt(p22b, S22_TXT_MAX_W, S22_TXT_MAX_H_B)

        if t22.width > allowed_w * S22_TBL_W_MAX:
            t22.scale((allowed_w * S22_TBL_W_MAX) / t22.width)
        if t22.height > allowed_h * S22_TBL_H_MAX:
            t22.scale((allowed_h * S22_TBL_H_MAX) / t22.height)

        p22a.to_edge(UP, buff=0.35).set_x(0)
        p22b.next_to(p22a, DOWN, buff=S22_GAP_AB).set_x(0)
        t22.next_to(p22b, DOWN, buff=S22_GAP_BT).set_x(0)
        self.play(Write(p22a, run_time=WRITE_MEDIUM_RT))
        self.play(Write(p22b, run_time=WRITE_MEDIUM_RT))
        self.play(FadeIn(t22, shift=0.3*DOWN), run_time=0.9)

        self.pause(S22_WAIT_AFTER_TABLE)

        
        self.play(
            FadeOut(p22a),
            FadeOut(p22b),
            t22.animate.move_to(ORIGIN),   
            run_time=0.9
        )

        p22c = write_block(CONTENT_22C)
        _fit_txt(p22c, S22_TXT_MAX_W, 0.30)

        p22c.next_to(t22, DOWN, buff=0.24).set_x(0)

        grp = Group(t22, p22c)
        for _ in range(10):
            if grp.width <= allowed_w and grp.height <= allowed_h:
                break
            if p22c.height > allowed_h * 0.20 or p22c.width > allowed_w * 0.90:
                p22c.scale(0.95)
            else:
                t22.scale(0.97)
                t22.move_to(ORIGIN)         
            p22c.next_to(t22, DOWN, buff=0.24).set_x(0)   
            grp = Group(t22, p22c)


        self.play(Write(p22c, run_time=WRITE_MEDIUM_RT))
        self.pause(0.4)

        self.fade_out_all(t22, p22c)

        # ----------------- Slide 23 
        sub23 = write_block(CONTENT_23_SUB)

        try:
            fit_text_block(
                sub23,
                max_w=allowed_w * S23_MAX_W,
                max_h=allowed_h * S23_MAX_H,
                pad=0.04,
                min_sf=0.60
            )
        except NameError:
            if sub23.width > allowed_w * S23_MAX_W:
                sub23.scale((allowed_w * S23_MAX_W) / sub23.width)
            if sub23.height > allowed_h * S23_MAX_H:
                sub23.scale((allowed_h * S23_MAX_H) / sub23.height)

        sub23.move_to(ORIGIN) 
        self.play(Write(sub23, run_time=WRITE_MEDIUM_RT))
        self.pause(0.5)
        self.fade_out_all(sub23)

        # ----------------- Slide 24 
        p24a = write_block(CONTENT_24A)
        p24b = write_block(CONTENT_24B)

        def _fit_txt(mob, max_w_frac, max_h_frac, min_sf=0.62):
            try:
                fit_text_block(
                    mob,
                    max_w=allowed_w * max_w_frac,
                    max_h=allowed_h * max_h_frac,
                    pad=0.04,
                    min_sf=min_sf
                )
            except NameError:
                cap_w = allowed_w * max_w_frac
                if mob.width > cap_w:
                    mob.scale(cap_w / mob.width)
                cap_h = allowed_h * max_h_frac
                if mob.height > cap_h:
                    mob.scale(cap_h / mob.height)

        _fit_txt(p24a, S24_MAX_W_FRAC, S24_MAX_H_A, min_sf=0.65)
        _fit_txt(p24b, S24_MAX_W_FRAC, S24_MAX_H_B, min_sf=0.65)

        g24a = p24a.copy()
        g24b = p24b.copy()

        g24a.move_to(ORIGIN + 0.12*UP).set_x(0)
        g24b.next_to(g24a, DOWN, buff=S24_GAP).set_x(0)

        ghost = Group(g24a, g24b)

        sw = allowed_w / ghost.width  if ghost.width  > allowed_w else 1.0
        sh = allowed_h / ghost.height if ghost.height > allowed_h else 1.0
        sf = min(sw, sh, 1.0)
        if sf < 1.0:
            ghost.scale(sf)
        ghost.move_to(ORIGIN)

        p24a.move_to(g24a.get_center())
        p24b.move_to(g24b.get_center())

        self.play(Write(p24a, run_time=WRITE_MEDIUM_RT)); self.pause(0.05)
        self.play(Write(p24b, run_time=WRITE_MEDIUM_RT)); self.pause(0.4)
        self.fade_out_all(p24a, p24b)

        # ----------------- Slide 25 
        p25a = write_block(CONTENT_25A)
        p25b = write_block(CONTENT_25B)

        def _fit_txt_25(mob, max_w_frac, max_h_frac, min_sf=0.62):
            try:
                fit_text_block(
                    mob,
                    max_w=allowed_w * max_w_frac,
                    max_h=allowed_h * max_h_frac,
                    pad=0.04,
                    min_sf=min_sf
                )
            except NameError:
                cap_w = allowed_w * max_w_frac
                if mob.width > cap_w:
                    mob.scale(cap_w / mob.width)
                cap_h = allowed_h * max_h_frac
                if mob.height > cap_h:
                    mob.scale(cap_h / mob.height)

        _fit_txt_25(p25a, S25_MAX_W_FRAC, S25_MAX_H_A, min_sf=0.65)
        _fit_txt_25(p25b, S25_MAX_W_FRAC, S25_MAX_H_B, min_sf=0.65)
        g25a = p25a.copy()
        g25b = p25b.copy()

        g25a.move_to(ORIGIN + 0.12*UP).set_x(0)
        g25b.next_to(g25a, DOWN, buff=S25_GAP).set_x(0)

        ghost = Group(g25a, g25b)

        sw = allowed_w / ghost.width  if ghost.width  > allowed_w else 1.0
        sh = allowed_h / ghost.height if ghost.height > allowed_h else 1.0
        sf = min(sw, sh, 1.0)
        if sf < 1.0:
            ghost.scale(sf)
        ghost.move_to(ORIGIN)

        p25a.move_to(g25a.get_center())
        p25b.move_to(g25b.get_center())

        # Animación
        self.play(Write(p25a, run_time=WRITE_MEDIUM_RT)); self.pause(0.05)
        self.play(Write(p25b, run_time=WRITE_MEDIUM_RT)); self.pause(0.4)
        self.fade_out_all(p25a, p25b)

        # ----------------- Slide 26 
        p26 = write_block(CONTENT_26)

        try:
            fit_text_block(
                p26,
                max_w=allowed_w * S26_MAX_W_FRAC,
                max_h=allowed_h * S26_MAX_H_FRAC,
                pad=0.04,
                min_sf=S26_MIN_SCALE
            )
        except NameError:
            cap_w = allowed_w * S26_MAX_W_FRAC
            if p26.width > cap_w:
                p26.scale(cap_w / p26.width)
            cap_h = allowed_h * S26_MAX_H_FRAC
            if p26.height > cap_h:
                p26.scale(cap_h / p26.height)

        p26.move_to(ORIGIN)  
        self.play(Write(p26, run_time=WRITE_MEDIUM_RT))
        self.pause(0.4)
        self.fade_out_all(p26)

#manim -pqh IntroduccionSQL.py IntroduccionSQL
