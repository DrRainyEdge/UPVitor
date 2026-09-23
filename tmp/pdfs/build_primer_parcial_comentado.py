from pathlib import Path
from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, HRFlowable, Image
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Tecnicas_de_Control/sources/exams/solved/_erParcial2025.pdf"
OUTDIR = ROOT / "Tecnicas_de_Control/outputs/PDF"
OUTDIR.mkdir(parents=True, exist_ok=True)
GUIDE = ROOT / "tmp/pdfs/Primer_Parcial_2025_comentado_guia.pdf"
FINAL = OUTDIR / "Primer_Parcial_2025_comentado.pdf"

font_dir = Path(r"C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("Aptos", str(font_dir / "arial.ttf")))
pdfmetrics.registerFont(TTFont("AptosB", str(font_dir / "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("AptosI", str(font_dir / "ariali.ttf")))

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2D6A9F")
PALE = colors.HexColor("#EAF3F8")
MINT = colors.HexColor("#E8F5EF")
AMBER = colors.HexColor("#FFF2CC")
ROSE = colors.HexColor("#FBE9E7")
INK = colors.HexColor("#18232D")
GREY = colors.HexColor("#61717E")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleX", fontName="AptosB", fontSize=24, leading=28, textColor=NAVY, spaceAfter=10))
styles.add(ParagraphStyle(name="SubTitle", fontName="Aptos", fontSize=11.5, leading=16, textColor=GREY, spaceAfter=16))
styles.add(ParagraphStyle(name="H1X", fontName="AptosB", fontSize=17, leading=21, textColor=NAVY, spaceBefore=8, spaceAfter=8))
styles.add(ParagraphStyle(name="H2X", fontName="AptosB", fontSize=12.5, leading=16, textColor=BLUE, spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyX", fontName="Aptos", fontSize=9.4, leading=13.2, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="SmallX", fontName="Aptos", fontSize=8, leading=10.5, textColor=GREY, spaceAfter=3))
styles.add(ParagraphStyle(name="Eq", fontName="Aptos", fontSize=10, leading=14, leftIndent=10, rightIndent=10, textColor=NAVY, spaceBefore=4, spaceAfter=6, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="Exam", fontName="Aptos", fontSize=9, leading=12.5, textColor=INK, leftIndent=6, rightIndent=6, spaceAfter=4))

def P(text, style="BodyX"):
    return Paragraph(text, styles[style])

def equation(tex, width=158*mm, fontsize=15):
    """Render a display equation with real stacked fractions and math layout."""
    fig = plt.figure(figsize=(8, 0.55), dpi=220)
    fig.patch.set_alpha(0)
    fig.text(0.5, 0.5, f"${tex}$", ha="center", va="center", fontsize=fontsize, color="#17324D")
    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    buf.seek(0)
    img = Image(buf)
    ratio = img.imageHeight / img.imageWidth
    img.drawWidth = min(width, img.imageWidth * 0.30)
    img.drawHeight = img.drawWidth * ratio
    img.hAlign = "CENTER"
    return img

def box(title, body, color=PALE):
    data = [[P(f"<b>{title}</b>", "BodyX")], [P(body, "BodyX")]]
    t = Table(data, colWidths=[170*mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("BOX", (0,0), (-1,-1), 0.6, BLUE),
        ("LINEBELOW", (0,0), (-1,0), 0.4, BLUE),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    return t

def bullet(text):
    return P(f"• {text}")

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD6DE")); canvas.line(20*mm, 14*mm, 190*mm, 14*mm)
    canvas.setFont("Aptos", 7.5); canvas.setFillColor(GREY)
    canvas.drawString(20*mm, 9*mm, "Técnicas de Control · Primer parcial 2025 comentado")
    canvas.drawRightString(190*mm, 9*mm, f"Guía comentada · {doc.page}")
    canvas.restoreState()

story = []
story += [Spacer(1, 22*mm), P("Primer parcial 2025", "TitleX"), P("Técnicas de Control · Examen comentado para una primera toma de contacto", "SubTitle")]
story += [box("Objetivo del documento", "Conservar el examen y su resolución, pero explicar qué se está haciendo, por qué se hace, qué significa cada elemento y cómo se conecta con un sistema industrial real. La guía comentada es material derivado; el examen original completo se incluye al final como anexo.", MINT), Spacer(1, 7*mm)]
story += [P("Cómo usarlo", "H1X")]
for x in [
    "Lee primero el enunciado sin mirar el resultado y marca: planta, entradas, salidas, perturbaciones, sensores y especificaciones.",
    "En cada paso, intenta responder: ¿qué condición del enunciado obliga a hacer esto?",
    "No memorices números aislados. Aprende la secuencia: traducir especificaciones → elegir estructura → diseñar lazos → comprobar → discretizar → implementar.",
    "Las cajas azules son explicación propia; las amarillas señalan errores frecuentes; el anexo reproduce la fuente original.",
]: story.append(bullet(x))
story += [Spacer(1,5*mm), P("Fuente y alcance", "H2X"), P("Fuente principal: <i>_erParcial2025.pdf</i>, 11 páginas, examen de 27-11-2025. Alcance: ejercicios 1 y 2 completos. La notación y los resultados originales se conservan; cuando se aclara o interpreta algo se indica como comentario didáctico."), PageBreak()]

story += [P("Mapa rápido del parcial", "H1X")]
data = [
    [P("Ejercicio", "BodyX"), P("Qué evalúa", "BodyX"), P("Idea central", "BodyX")],
    [P("1 · PID-2DoF", "BodyX"), P("Diseño en continuo, ponderación de referencia, Tustin y ecuación en diferencias", "BodyX"), P("Separar seguimiento y rechazo sin cambiar los polos del denominador", "BodyX")],
    [P("2 · Cascada", "BodyX"), P("Elección de estructura, retardos, discretización y predictor de Smith", "BodyX"), P("Usar la medida intermedia X2 para rechazar P1 antes de que afecte a Y", "BodyX")],
]
t=Table(data,colWidths=[32*mm,73*mm,65*mm],repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#B7C6D1")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)])); story += [t, Spacer(1,6*mm)]
story += [box("Antes de calcular", "En control, el diagrama de bloques es parte de la solución. Una señal que entra antes o después de la planta produce una función de transferencia distinta. Define siempre desde qué entrada hasta qué salida estás calculando.", AMBER)]
story += [P("Recordatorio mínimo", "H2X")]
for x in [
    "Referencia r: valor deseado. Salida y: variable controlada. Error e=r-y: diferencia que el controlador intenta reducir.",
    "Perturbación d o P: influencia externa no ordenada (carga, presión, par resistente, caudal, temperatura exterior...).",
    "Polos: determinan estabilidad y rapidez. Ceros: moldean la forma de la respuesta y pueden aumentar la sobreoscilación.",
    "Acción integral: acumula error y permite error estacionario nulo ante escalones si el lazo es estable.",
    "Tustin: transforma un regulador continuo a discreto mediante s=(2/T)(z-1)/(z+1).",
]: story.append(bullet(x))
story.append(PageBreak())

story += [P("Ejercicio 1 · PID con dos grados de libertad", "H1X"), P("Enunciado reproducido", "H2X")]
story += [P("Diseñar un PID-2DoF para la planta indicada, ante escalones en referencia r y perturbación d, con <b>t<sub>e</sub>≤2 s</b>, <b>e<sub>∞</sub>=0</b> y, ante referencia, <b>δ≤4,3 %</b>. Dibujar el esquema, verificar polos, discretizar ambos bloques con T=0,1 s y obtener la ecuación en diferencias.", "Exam")]
story += [equation(r"G(s)=\frac{Y(s)}{U(s)}=\frac{1}{s(s+5)}")]
story += [box("Qué te están pidiendo realmente", "Un controlador que sea rápido y sin error permanente frente a dos causas distintas: una orden de consigna y una perturbación. El 2DoF permite que el bloque de referencia tenga un numerador distinto del bloque de realimentación; así se mejora el seguimiento sin estropear el rechazo de perturbaciones.")]
story += [P("1. Traducir las especificaciones a una zona de polos", "H2X")]
story += [P("Con el criterio de establecimiento usado en la solución, t<sub>e</sub>≈4/σ. Por tanto, t<sub>e</sub>≤2 s exige σ≥2: los polos dominantes deben quedar a la izquierda de Re(s)=-2. Una sobreoscilación del 4,3 % corresponde aproximadamente a ζ≈0,707. La elección habitual de diseño es:")]
story += [equation(r"s_d=-2\pm2j")]
story += [box("Por qué esos polos", "Su parte real -2 fija la rapidez aproximada; la relación entre parte real e imaginaria da ζ≈0,707, que produce alrededor del 4,3 % de sobreoscilación en un segundo orden sin ceros dominantes.", MINT)]
story += [P("2. Por qué hace falta integral y por qué se prueba un PID", "H2X")]
story += [P("La exigencia e<sub>∞</sub>=0 ante escalones obliga a incluir un integrador. La fuente indica que un PI no permite situar todos los polos dentro de la zona dinámica requerida, por lo que se aumenta un grado de libertad añadiendo la acción derivativa: se pasa a un PID con dos ceros ajustables.")]
story += [box("Idea que conviene recordar", "No se elige PID porque sea 'mejor' de forma universal. Se elige porque el PI no proporciona suficientes parámetros para colocar la dinámica donde exigen las especificaciones.", AMBER)]
story.append(PageBreak())

story += [P("Ejercicio 1 · Diseño del PID (solución principal)", "H1X"), P("3. Colocar los ceros con lugar de las raíces", "H2X")]
story += [P("Se propone un PID en forma factorizada:")]
story += [equation(r"PID(s)=k_r\,\frac{(s+z_1)(s+z_2)}{s}")]
story += [P("En el punto deseado s=-2+2j debe cumplirse el criterio del argumento. La solución original obtiene un déficit angular de 123,7°. Si ambos ceros aportan la misma fase, se colocan coincidentes:")]
story += [equation(r"z_1=z_2=2+\frac{2}{\tan\!\left(\frac{123{,}7^\circ}{2}\right)}=3{,}07")]
story += [P("Después se aplica el criterio del módulo |L(s<sub>d</sub>)|=1 para encontrar la ganancia:")]
story += [equation(r"k_r=5{,}6\qquad\Longrightarrow\qquad PID(s)=5{,}6\,\frac{(s+3{,}07)^2}{s}")]
story += [box("Qué hacen los dos criterios", "El criterio del argumento decide dónde colocar ceros o polos para que el lugar de las raíces pase por el punto deseado. El criterio del módulo calcula qué ganancia sitúa realmente el polo cerrado en ese punto.")]
story += [P("4. Pasar a parámetros ISA", "H2X")]
story += [P("La forma ISA paralela usada es:")]
story += [equation(r"PID(s)=k_c\left(1+\frac{1}{T_i s}+T_d s\right)")]
story += [P("Al igualar sus coeficientes con los del PID obtenido:")]
story += [equation(r"T_d\approx0{,}16\ \mathrm{s},\qquad T_i\approx0{,}65\ \mathrm{s},\qquad k_c=\frac{k_r}{T_d}\approx35")]
story += [P("Estos parámetros no son un segundo diseño: son otra forma de escribir el mismo regulador, útil porque muchos PLC y controladores industriales piden k<sub>c</sub>, T<sub>i</sub> y T<sub>d</sub>.")]
story += [P("5. Ponderar la referencia", "H2X")]
story += [P("Se toman b=c=0 para que la referencia solo entre por la parte integral. El bloque de referencia queda:")]
story += [equation(r"PID_F(s)=\frac{52{,}84}{s}")]
story += [box("Por qué se pondera", "Los ceros del PID completo son útiles para colocar polos, pero si también aparecen en la transferencia r→y pueden provocar una respuesta de referencia más brusca y con mayor sobreoscilación. La ponderación permite conservar el denominador (los polos) y modificar el numerador del seguimiento.", MINT)]
story.append(PageBreak())

story += [P("Ejercicio 1 · Verificación y alternativa", "H1X"), P("6. Comprobar las dos entradas", "H2X")]
story += [P("Con PID en realimentación y PID<sub>F</sub> en el camino de referencia:")]
story += [equation(r"Y(s)=\frac{PID_F(s)G(s)}{1+PID(s)G(s)}\,R(s)+\frac{G(s)}{1+PID(s)G(s)}\,D(s)", fontsize=13)]
story += [P("La fuente obtiene un denominador equivalente con polos en -2±2j y un tercer polo suficientemente rápido. La transferencia de referencia no contiene los ceros del PID completo, por lo que la sobreoscilación queda gobernada principalmente por los polos elegidos. Para perturbación, el integrador asegura rechazo estacionario del escalón si el lazo permanece estable.")]
story += [box("Comprobación de examen", "No basta con escribir los polos. Debes enlazarlos con cada condición: Re(p)≤-2 → rapidez; ζ≈0,707 → sobreoscilación; integrador + estabilidad → error estacionario nulo.", AMBER)]
story += [P("Solución alternativa de la fuente", "H2X")]
story += [P("También se cancela el polo de la planta en -5 con un cero del PID y se coloca el otro cero en -2. Aplicando argumento y módulo:")]
story += [equation(r"PID(s)=4\,\frac{(s+5)(s+2)}{s}")]
story += [P("En forma ISA se obtiene T<sub>d</sub>≈0,1429 s, T<sub>i</sub>≈0,7 s y k<sub>c</sub>≈28. Para conservar la cancelación en el seguimiento puede usarse c=0 y b≈0,2857:")]
story += [equation(r"PID_F(s)=8\,\frac{s+5}{s}")]
story += [P("La propia fuente también admite b=c=0 porque el polo -5 ya está dentro de la zona aceptable:")]
story += [equation(r"PID_F(s)=\frac{40}{s}")]
story += [box("Precaución industrial", "Las cancelaciones exactas polo-cero son frágiles: si el modelo real cambia, la cancelación deja de ser exacta. En una planta real se revisan robustez, saturación, ruido y límites del actuador antes de aceptar este diseño.", ROSE)]
story.append(PageBreak())

story += [P("Ejercicio 1 · Discretización por Tustin", "H1X"), P("7. Qué significa discretizar", "H2X")]
story += [P("El controlador se diseñó en s (tiempo continuo), pero un PLC ejecuta cálculos cada T segundos. Tustin sustituye:")]
story += [equation(r"s\;\longrightarrow\;\frac{2}{T}\,\frac{z-1}{z+1}\qquad\qquad \frac{1}{s}\;\longrightarrow\;\frac{T}{2}\,\frac{z+1}{z-1}")]
story += [P("Para T=0,1 s y la solución principal, la fuente obtiene:")]
story += [equation(r"PID(z)=\frac{U_1(z)}{Y(z)}=\frac{149{,}2z^2-218{,}9z+80{,}33}{z^2-1}")]
story += [equation(r"PID_F(z)=\frac{U_2(z)}{R(z)}=2{,}64\,\frac{z+1}{z-1}")]
story += [box("Lectura física", "U1 es la contribución asociada a la medida y U2 la asociada a la referencia. En el sumador final, u=u2-u1: la referencia empuja la acción de control y la medida la corrige por realimentación negativa.")]
story += [P("8. Pasar de función en z a ecuación en diferencias", "H2X")]
story += [P("Primero se divide numerador y denominador por la mayor potencia de z para escribir todo con retardos z<super>-1</super>. Después se usa z<super>-1</super>X(z) ↔ x(k-1). La resolución original expresa:")]
story += [equation(r"u_2(k)=u_2(k-1)+2{,}64\,r(k)+2{,}64\,r(k-1)", fontsize=13)]
story += [equation(r"u_1(k)=u_1(k-1)+149{,}2\,y(k)-218{,}9\,y(k-1)+80{,}33\,y(k-2)", fontsize=12)]
story += [P("y finalmente:")]
story += [equation(r"u(k)=u(k-1)+2{,}64\,r(k)+2{,}64\,r(k-1)", fontsize=12)]
story += [equation(r"\phantom{u(k)=u(k-1)}-149{,}2\,y(k)+218{,}9\,y(k-1)-80{,}33\,y(k-2)", fontsize=12)]
story += [box("Observación de trazabilidad", "La solución original menciona una aproximación entre estados anteriores al combinar componentes. Conviene conservar por separado u1 y u2 en una implementación real si se quiere evitar ambigüedad y facilitar pruebas, saturación y anti-windup.", AMBER)]
story.append(PageBreak())

story += [P("Ejercicio 1 · Uso laboral e industrial", "H1X")]
for title, body in [
    ("Control de velocidad de motores", "La referencia es la velocidad deseada; una variación de carga actúa como perturbación. El 2DoF permite una consigna suave y, a la vez, rechazo rápido del par resistente."),
    ("Temperatura de hornos", "La apertura de puerta o el cambio de producto perturban la temperatura. La integral elimina el error sostenido; la ponderación evita picos de potencia ante cambios de consigna."),
    ("Presión y caudal", "En bombas y compresores, el regulador digital se ejecuta en PLC/DCS. La ecuación en diferencias es la forma que acaba programándose."),
    ("Puesta en marcha", "Además de polos y respuesta ideal, se verifican saturación, límites de velocidad, ruido de medida, filtro derivativo, anti-windup, periodo real de tarea y comportamiento seguro ante fallo de sensor."),
]: story += [P(title,"H2X"), P(body)]
story += [box("Qué demuestra este ejercicio en una entrevista", "Que sabes traducir requisitos de proceso a dinámica, elegir una estructura, justificarla, llevarla a software y comprobar que la implementación conserva la intención del diseño.", MINT)]
story += [P("Errores frecuentes", "H2X")]
for x in ["Confundir el bloque de referencia con el PID de realimentación.", "Comprobar solo r→y y olvidar d→y.", "Usar t_e≈4/σ sin declarar el criterio de establecimiento.", "Perder el signo negativo de la medida al formar u=u2-u1.", "Redondear demasiado pronto durante Tustin."]: story.append(bullet(x))
story.append(PageBreak())

story += [P("Ejercicio 2 · Control en cascada", "H1X"), P("Enunciado reproducido", "H2X")]
story += [P("El proceso contiene dos bloques principales, un retardo y dos caminos de perturbación:", "Exam")]
story += [equation(r"G_1(s)=\frac{2}{s+5},\quad G_{d1}(s)=\frac{2}{s+4},\quad G_{d2}(s)=\frac{1}{s+10},\quad G_2(s)=\frac{4}{s+1}", fontsize=13)]
story += [P("El retardo es e<sup>-sT</sup>, con T=0,01 s, y se miden X2 e Y. Se pide elegir una estructura que logre error nulo ante referencia, P1 y P2, t<sub>e</sub>=2 s y δ≤4,3 %; analizar la discretización del lazo interno; y razonar qué hacer si T=2 s.", "Exam")]
story += [box("Primera decisión", "Como X2 es medible y P1 entra antes de X2, puede cerrarse un lazo interno sobre X2. Ese lazo detecta y corrige P1 antes de que su efecto atraviese G2. El lazo externo usa Y para seguir la referencia y rechazar P2.")]
story += [P("1. Estructura propuesta", "H2X")]
story += [P("Control en cascada: controlador interno C<sub>i</sub> sobre X2 y controlador externo C<sub>o</sub> sobre Y. El lazo interno incluye G1 y el retardo; el externo ve el lazo interno ya cerrado más G2.")]
story += [box("Regla de cascada", "El lazo interno debe ser claramente más rápido que el externo. Si ambos tienen velocidades parecidas, se acoplan y el diseño por etapas deja de ser válido.", AMBER)]
story += [P("2. Aproximación del retardo pequeño", "H2X")]
story += [P("Como T=0,01 s es pequeño frente a la dinámica dominante, la resolución aproxima:")]
story += [equation(r"e^{-0{,}01s}\approx\frac{1}{1+0{,}01s}=\frac{100}{s+100}")]
story += [P("Esta es una aproximación racional de primer orden que introduce un polo rápido en -100. Sirve para diseñar con técnicas de lugar de raíces sin manejar directamente el exponencial.")]
story.append(PageBreak())

story += [P("Ejercicio 2 · Diseño del lazo interno", "H1X"), P("3. Ganancia proporcional para X2", "H2X")]
story += [P("La solución usa inicialmente C<sub>i</sub>(s)=k. El rechazo de P1 se evalúa con la sensibilidad del lazo interno:")]
story += [equation(r"\frac{X_2(s)}{P_1(s)}=\frac{G_{d1}(s)}{1+k\,G_1(s)\,\dfrac{100}{s+100}}", fontsize=13)]
story += [P("Se fija como objetivo didáctico reducir aproximadamente un 90 % el efecto estacionario de P1. A frecuencia cero:")]
story += [equation(r"\frac{1}{1+k\left(\dfrac{2}{5}\right)}=0{,}1\qquad\Longrightarrow\qquad k=22{,}5")]
story += [P("Con esa ganancia, el lazo interno de referencia a X2 queda:")]
story += [equation(r"\frac{X_2(s)}{R_2(s)}=\frac{4500}{s^2+105s+5000}")]
story += [P("Sus polos son aproximadamente -52,5±47,36j; por tanto, su parte real está muy a la izquierda de -2 y el lazo interno es mucho más rápido que el externo solicitado.")]
story += [box("Importante", "El 90 % de rechazo no aparece literalmente como especificación del examen: es una elección de diseño de la resolución manuscrita para hacer fuerte el lazo interno. Debe presentarse como supuesto de diseño, no como dato del enunciado.", AMBER)]
story += [P("4. Modelo que ve el lazo externo", "H2X")]
story += [P("Como el lazo interno es muy rápido, se aproxima por su ganancia estática:")]
story += [equation(r"\frac{X_2(0)}{R_2(0)}=\frac{4500}{5000}=0{,}9")]
story += [P("Así, para diseñar el lazo externo se usa el proceso equivalente aproximado:")]
story += [equation(r"G_{eq}(s)\approx0{,}9\,\frac{4}{s+1}")]
story += [P("Esta simplificación reduce el orden del problema y es válida porque hay separación clara de velocidades.")]
story.append(PageBreak())

story += [P("Ejercicio 2 · Diseño del lazo externo", "H1X"), P("5. Por qué el controlador externo lleva integral", "H2X")]
story += [P("P2 entra después de X2, de modo que el lazo interno no puede verla ni corregirla. El lazo externo, que mide Y, debe rechazarla. Para error nulo ante escalones de referencia y P2 se introduce un integrador:")]
story += [equation(r"C_o(s)=k\,\frac{s+a}{s}")]
story += [P("Se eligen de nuevo polos dominantes -2±2j. Aplicando el criterio del argumento al proceso equivalente anterior, la resolución obtiene a≈2,66. Con el criterio del módulo:")]
story += [equation(r"k_L\approx3\qquad\Longrightarrow\qquad k=\frac{3}{0{,}9\cdot4}\approx0{,}83")]
story += [P("Resultado de la solución manuscrita:")]
story += [equation(r"C_o(s)=0{,}83\,\frac{s+2{,}66}{s}")]
story += [box("Por qué funciona", "El integrador asegura el tipo necesario para eliminar error estacionario. El cero en -2,66 aporta la fase que falta para que el lugar de las raíces pase por -2±2j. La ganancia coloca los polos exactamente en ese punto.", MINT)]
story += [box("Qué debes dibujar", "Dos realimentaciones anidadas: la interna desde X2 hasta el sumador anterior a Ci; la externa desde Y al sumador anterior a Co. P1 entra antes de X2 y P2 después de X2. Dibujar bien estos puntos explica por sí solo qué perturbación rechaza cada lazo.", AMBER)]
story.append(PageBreak())

story += [P("Ejercicio 2 · Discretización y retardo", "H1X"), P("6. Caso T=0,01 s", "H2X")]
story += [P("El enunciado da el proceso discretizado con ZOH:")]
story += [equation(r"\frac{X_2(z)}{U(z)}=\frac{0{,}01951}{z-0{,}9512}\,z^{-1}")]
story += [P("El factor z<super>-1</super> es un retardo exacto de una muestra. En tiempo continuo, el retardo añade fase; en discreto, ese efecto aparece explícitamente como una muestra de demora. La resolución advierte que los polos se desplazan en el plano z y disminuye el margen disponible para aumentar ganancia.")]
story += [box("Respuesta razonada al apartado b", "La discretización no es neutra: el retardo de cálculo/muestreo reduce el margen de fase y puede empeorar amortiguamiento o estabilidad. Con T=0,01 s, mucho menor que las constantes de tiempo del proceso, el efecto es limitado, pero debe comprobarse sobre el modelo discreto y no asumir que el diseño continuo se conserva exactamente.")]
story += [P("7. Caso T=2 s", "H2X")]
story += [P("Si el retardo pasa a 2 s y la especificación sigue siendo t<sub>e</sub>≤2 s, no puede construirse un lazo interno claramente más rápido: la propia información tarda tanto como todo el tiempo permitido. La medida X2 deja de aportar la ventaja práctica de cascada para esa especificación.")]
story += [P("La resolución propone abandonar la cascada y usar un lazo único, relajando especificaciones, con un predictor de Smith para compensar el retardo conocido.")]
story += [box("Qué hace un predictor de Smith", "Usa un modelo del proceso y del retardo para que el controlador actúe sobre una predicción sin retardo, mientras la diferencia entre planta real y modelo corrige la predicción. Mejora el control cuando el retardo es grande y está bien modelado; su calidad cae si el modelo o el retardo varían.", MINT)]
story.append(PageBreak())

story += [P("Ejercicio 2 · Uso laboral e industrial", "H1X")]
for title, body in [
    ("Reactores y hornos", "Un lazo interno de caudal o presión corrige perturbaciones rápidas; el lazo externo regula temperatura o composición, que evolucionan más despacio."),
    ("Accionamientos", "El lazo de corriente es interno y rápido; velocidad y posición son lazos externos progresivamente más lentos."),
    ("Calderas y vapor", "Caudal de combustible/aire puede cerrarse internamente y presión o temperatura externamente."),
    ("Procesos con transporte", "Cintas, tuberías y analizadores introducen tiempo muerto. Cuando domina la dinámica, se usan predictores, feedforward o rediseño de instrumentación."),
]: story += [P(title,"H2X"), P(body)]
story += [P("Errores frecuentes", "H2X")]
for x in [
    "Diseñar primero el lazo externo: en cascada se cierra y valida primero el interno.",
    "Pretender que el lazo interno rechace P2 aunque P2 entra después de X2.",
    "Aproximar un retardo grande con un polo rápido: esa aproximación solo es razonable cuando T es pequeño frente a la dinámica relevante.",
    "Usar la ganancia estática 0,9 sin demostrar antes que el lazo interno es mucho más rápido.",
    "Confundir z<super>-1</super> con un polo cualquiera: representa exactamente una muestra de retardo.",
]: story.append(bullet(x))
story.append(PageBreak())

story += [P("Guion para resolver un examen parecido", "H1X")]
steps = [
    ("1", "Dibuja y etiqueta", "Referencia, salida, señales intermedias, perturbaciones, sensores y puntos de suma."),
    ("2", "Traduce especificaciones", "t_e a parte real; sobreoscilación a amortiguamiento; error nulo a necesidad de integral."),
    ("3", "Elige estructura", "PID/2DoF si necesitas separar seguimiento y rechazo; cascada si existe una medida intermedia útil y rápida."),
    ("4", "Diseña", "Argumento para geometría; módulo para ganancia; declara aproximaciones y supuestos."),
    ("5", "Verifica todas las entradas", "Referencia y cada perturbación; polos, ceros, error permanente y coherencia física."),
    ("6", "Discretiza", "Elige T, método, normaliza en z<super>-1</super> y deriva la ecuación en diferencias con signos correctos."),
    ("7", "Piensa como ingeniero", "Saturación, ruido, retardo, incertidumbre, sensores, fallos y límites del actuador."),
]
for n,tit,body in steps:
    tb=Table([[P(n,"H2X"),P(f"<b>{tit}</b><br/>{body}","BodyX")]],colWidths=[12*mm,158*mm])
    tb.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),NAVY),("TEXTCOLOR",(0,0),(0,0),colors.white),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("BOX",(0,0),(-1,-1),0.4,colors.HexColor("#CAD5DD")),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)])); story += [tb,Spacer(1,3*mm)]
story += [Spacer(1,4*mm), box("Autoevaluación breve", "Antes de mirar el anexo, intenta explicar con tus palabras: (1) por qué b=c=0 elimina ceros del seguimiento, (2) por qué X2 permite rechazar P1 pero no P2, y (3) por qué un retardo de 2 s invalida la separación rápida de la cascada.", MINT)]
story.append(PageBreak())

story += [P("Ficha final de fórmulas", "H1X")]
rows=[
    ("Especificaciones", equation(r"t_e\approx\frac{4}{\sigma}\qquad M_p=e^{-\frac{\pi\zeta}{\sqrt{1-\zeta^2}}}", 112*mm, 11)),
    ("Polos elegidos", equation(r"s_d=-2\pm2j\qquad \zeta\approx0{,}707\qquad \omega_n\approx2{,}828\ \mathrm{rad/s}", 112*mm, 11)),
    ("PID solución 1", equation(r"PID(s)=5{,}6\,\frac{(s+3{,}07)^2}{s}", 112*mm, 11)),
    ("Referencia 2DoF", equation(r"PID_F(s)=\frac{52{,}84}{s}\qquad (b=c=0)", 112*mm, 11)),
    ("Tustin", equation(r"s=\frac{2}{T}\,\frac{z-1}{z+1}\qquad \frac{1}{s}=\frac{T}{2}\,\frac{z+1}{z-1}", 112*mm, 11)),
    ("Cascada interna", equation(r"k=22{,}5\qquad \frac{X_2(s)}{R_2(s)}=\frac{4500}{s^2+105s+5000}", 112*mm, 11)),
    ("Cascada externa", equation(r"C_o(s)=0{,}83\,\frac{s+2{,}66}{s}", 112*mm, 11)),
    ("Retardo discreto", equation(r"z^{-1}=\text{una muestra de retraso}", 112*mm, 11)),
]
tb=Table([[P("Concepto","BodyX"),P("Resultado / relación","BodyX")]]+[[P(a),b] for a,b in rows],colWidths=[47*mm,123*mm],repeatRows=1)
tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#B7C6D1")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)])); story += [tb,Spacer(1,6*mm)]
story += [box("Límite del material", "Este documento explica una solución histórica y añade comentarios propios. No convierte el examen en predicción del próximo parcial ni valida por sí solo una implementación industrial. Las decisiones reales requieren modelo validado, análisis de robustez, simulación y pruebas seguras.", ROSE)]
story += [Spacer(1,8*mm), P("A continuación: anexo con las 11 páginas del examen original, sin modificar.", "H2X")]

doc=SimpleDocTemplate(str(GUIDE), pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=19*mm, title="Primer Parcial 2025 comentado", author="UPVITOR")
doc.build(story, onFirstPage=footer, onLaterPages=footer)

writer=PdfWriter()
for page in PdfReader(str(GUIDE)).pages: writer.add_page(page)
for page in PdfReader(str(SOURCE)).pages: writer.add_page(page)
writer.add_metadata({"/Title":"Primer Parcial 2025 comentado - Técnicas de Control","/Subject":"Guía comentada y anexo original","/Author":"UPVITOR"})
with FINAL.open("wb") as f: writer.write(f)
print(FINAL)
