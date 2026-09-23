from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Tecnicas_de_Control/outputs/PDF/Primer_Parcial_24-11-2022_guia_comentada.pdf'
SOURCE_IMG = ROOT / 'tmp/pdfs/exam_source_render/page-01.png'
OUT.parent.mkdir(parents=True, exist_ok=True)

try:
    pdfmetrics.registerFont(TTFont('Aptos', r'C:\Windows\Fonts\arial.ttf'))
    FONT='Aptos'
except Exception:
    FONT='Helvetica'

teal = colors.HexColor('#007f86')
navy = colors.HexColor('#17374d')
soft = colors.HexColor('#eaf3f4')
gold = colors.HexColor('#fff4d6')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleES', parent=styles['Title'], fontName=FONT, fontSize=24, leading=29, textColor=navy, spaceAfter=10))
styles.add(ParagraphStyle(name='H1ES', parent=styles['Heading1'], fontName=FONT, fontSize=17, leading=21, textColor=teal, spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name='H2ES', parent=styles['Heading2'], fontName=FONT, fontSize=12.5, leading=16, textColor=navy, spaceBefore=6, spaceAfter=4))
styles.add(ParagraphStyle(name='BodyES', parent=styles['BodyText'], fontName=FONT, fontSize=9.7, leading=13.2, textColor=navy, spaceAfter=6))
styles.add(ParagraphStyle(name='SmallES', parent=styles['BodyText'], fontName=FONT, fontSize=8, leading=10.5, textColor=colors.HexColor('#526a78'), spaceAfter=4))
styles.add(ParagraphStyle(name='Callout', parent=styles['BodyText'], fontName=FONT, fontSize=9.5, leading=13, textColor=navy, backColor=soft, borderColor=colors.HexColor('#c4dfe1'), borderWidth=.5, borderPadding=8, spaceBefore=5, spaceAfter=8))
styles.add(ParagraphStyle(name='Warning', parent=styles['BodyText'], fontName=FONT, fontSize=9.5, leading=13, textColor=navy, backColor=gold, borderColor=colors.HexColor('#e7c76a'), borderWidth=.5, borderPadding=8, spaceBefore=5, spaceAfter=8))
styles.add(ParagraphStyle(name='CenterSmall', parent=styles['SmallES'], alignment=TA_CENTER))

def P(text, style='BodyES'):
    return Paragraph(text, styles[style])

def header_footer(canvas, doc):
    canvas.saveState()
    w,h=A4
    canvas.setFillColor(teal); canvas.rect(0,h-7*mm,w,7*mm,fill=1,stroke=0)
    canvas.setStrokeColor(colors.HexColor('#d5e0e4')); canvas.line(18*mm,14*mm,w-18*mm,14*mm)
    canvas.setFont(FONT,7.5); canvas.setFillColor(colors.HexColor('#526a78'))
    canvas.drawString(18*mm,8*mm,'UPVITOR / TÉCNICAS DE CONTROL / PRIMER PARCIAL')
    canvas.drawRightString(w-18*mm,8*mm,f'{doc.page}')
    canvas.restoreState()

def section(title, subtitle=None):
    out=[P(title,'H1ES')]
    if subtitle: out.append(P(subtitle,'SmallES'))
    return out

def bullet(text): return P('• '+text,'BodyES')

story=[]
story += [P('Primer parcial de Técnicas de Control','TitleES'), P('Guía comentada para tu primer examen de la asignatura','H2ES'), P('Examen original: 24/11/2022 · Duración indicada: 1 h 30 min · 2 ejercicios de 5 puntos', 'SmallES')]
story += [P('<b>Cómo usar este documento</b>','H1ES'), P('Primero intenta leer y resolver el enunciado original sin mirar las ayudas. Después utiliza los comentarios para entender qué está pidiendo cada apartado, qué teoría necesitas recuperar y en qué orden conviene trabajar. Las ayudas son orientación didáctica, no una solución oficial.', 'BodyES')]
story += [P('<b>Regla para este primer intento:</b> no empieces operando. Empieza clasificando el problema: ¿es continuo o discreto?, ¿hay una perturbación?, ¿qué variable se mide?, ¿qué especificación temporal se pide?', 'Callout')]
story += section('Mapa rápido del examen')
data=[['Ejercicio','Bloque principal','Qué se entrena'],['1','Discretización e implementación','ZOH, estabilidad en z, respuesta a una entrada y ecuación en diferencias del PI.'],['2','Estructuras de control','Prealimentación, cascada, rapidez relativa de lazos, error estacionario y diagrama de bloques.']]
t=Table(data,colWidths=[25*mm,48*mm,105*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),teal),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,-1),FONT),('FONTSIZE',(0,0),(-1,-1),8.5),('LEADING',(0,0),(-1,-1),11),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#c8d7dc')),('BACKGROUND',(0,1),(-1,-1),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)])); story.append(t)
story += [Spacer(1,7), P('<b>Fuente:</b> PDF escaneado <i>1erP_24_11_2022.pdf</i>, conservado en sources/exams/unsolved/. La página original se reproduce en la página siguiente. Las explicaciones y aplicaciones de este documento son elaboración didáctica propia.', 'SmallES'), PageBreak()]

story += [P('Enunciado original','TitleES'), P('Esta página reproduce el enunciado del examen para conservar su redacción, datos, puntuación y diagrama. Si trabajas en papel, puedes imprimirla y resolver aquí.', 'SmallES')]
im=Image(str(SOURCE_IMG)); im._restrictSize(180*mm,245*mm); story.append(im); story += [PageBreak()]

story += section('Ejercicio 1 · cómo empezar sin perderse','Este ejercicio mezcla una planta continua, muestreo, discretización y un regulador PI. No son tres ejercicios independientes: cada apartado usa el resultado o la idea del anterior.')
story += [P('<b>Antes de calcular, traduce el enunciado:</b> G(s) es el proceso; PI(s) es el controlador diseñado en continuo; T es el periodo de muestreo. Cuando pasas a z, debes indicar qué bloque estás discretizando y qué método utilizas.', 'Callout')]
story += [P('Apartado a · ZOH y estabilidad', 'H2ES'), bullet('<b>Qué te piden:</b> obtener una representación discreta del proceso G(s) suponiendo que la entrada se mantiene constante entre muestras (Zero-Order Hold).'), bullet('<b>Por qué aparece ZOH:</b> un computador no entrega una señal continua ideal; mantiene cada valor calculado hasta la siguiente muestra.'), bullet('<b>Qué recordar:</b> el periodo T = 0,01 s fija el instante kT. La estabilidad discreta se comprueba mirando los polos en el plano z: para estabilidad asintótica deben quedar dentro del círculo unidad, |z_i| < 1.'), bullet('<b>Orden recomendado:</b> 1) identifica el polo continuo; 2) aplica el método ZOH; 3) simplifica la función en z; 4) localiza sus polos; 5) responde claramente sí/no y justifica.')]
story += [P('Apartado b · respuesta a la entrada', 'H2ES'), bullet('<b>Qué significa la secuencia:</b> {u_k} = {0,0,1,1,1,...} es un escalón discreto que empieza después de dos muestras. No confundas el índice k con el tiempo continuo t.'), bullet('<b>Qué necesitas:</b> la función de transferencia discreta del apartado a y la relación entre entrada y salida. Puedes trabajar con la transformada Z y fracciones parciales o reconocer la respuesta de primer orden desplazada.'), bullet('<b>Comprobación física:</b> la salida no puede responder antes del instante en que aparece la entrada; el retardo de dos muestras equivale a 2T segundos.')]
story += [P('Apartado c · PI por Tustin y ecuación en diferencias', 'H2ES'), bullet('<b>Qué significa:</b> ahora sí discretizas el controlador PI, no el proceso. Tustin sustituye el operador continuo s por una expresión racional en z que usa la muestra actual y la anterior.'), bullet('<b>Ruta:</b> 1) escribe PI(s) separando acción proporcional e integral; 2) aplica la sustitución de Tustin con T = 0,01 s; 3) agrupa en potencias de z⁻¹; 4) despeja la salida del controlador u[k].'), bullet('<b>La ecuación final debe ser implementable:</b> debe expresar u[k] usando errores actuales y pasados, y valores anteriores de u si aparecen. Comprueba que los coeficientes tengan sentido dimensional y que no hayas cambiado el signo del error.')]
story += [P('<b>Recordatorio de la primera parte:</b> una función de transferencia describe una relación entrada-salida bajo condiciones iniciales nulas. Una ecuación en diferencias es la misma relación preparada para ejecutarse muestra a muestra.', 'Warning'), PageBreak()]

story += section('Ejercicio 2 · elegir la arquitectura','Aquí no basta con calcular una ganancia. Primero debes decidir qué estructura responde mejor a la perturbación P y a las medidas disponibles.')
story += [P('<b>Lee el diagrama de izquierda a derecha:</b> G₁ transforma U en C; la perturbación P pasa por G<sub>d</sub>; ambas contribuciones se suman para formar X; G₂ transforma X en Y. Por tanto, X es una variable intermedia y Y es la salida final.', 'Callout')]
story += [P('Apartado a · se pueden medir Y, X y P', 'H2ES'), bullet('<b>Qué pregunta realmente:</b> qué combinación de estructuras permite corregir rápido y anticiparse a la perturbación.'), bullet('<b>Idea 1, cascada:</b> X puede medirse y está antes de Y. Un lazo interno sobre X puede corregir cambios que afecten a X antes de que lleguen completamente a Y. Se diseña de dentro hacia fuera.'), bullet('<b>Idea 2, prealimentación:</b> P puede medirse. Un compensador puede actuar cuando aparece P, antes de esperar a que Y se desvíe. Necesita conocer los caminos G₁ y G<sub>d</sub> y debe ser realizable.'), bullet('<b>Idea 3, realimentación externa:</b> Y también se mide. El lazo externo corrige el error final y hace robusta la solución frente a errores de modelo.'), bullet('<b>Qué dibujar:</b> no basta con escribir “cascada + feedforward”. Representa sensores, sumadores, controladores y señales; marca qué lazo es interno y cuál externo.')]
story += [P('Apartado b · solo se pueden medir Y y X', 'H2ES'), bullet('<b>Qué cambia:</b> ya no puedes medir P directamente, así que la prealimentación basada en P no puede utilizarse tal cual.'), bullet('<b>Pregunta de decisión:</b> ¿la cascada sigue siendo viable? Comprueba que X sea medible, controlable y suficientemente rápida respecto al lazo de Y.'), bullet('<b>Cómo razonar:</b> la estructura anterior era válida gracias a tres medidas. Al perder P, elimina o sustituye únicamente la parte que dependía de ella; conserva la realimentación de Y y X si sigue siendo coherente.'), bullet('<b>Especificaciones:</b> tiempo de establecimiento menor de 1 s implica rapidez; sobreoscilación menor del 4,32 % se relaciona con el amortiguamiento; error de posición cero ante escalón exige suficiente tipo/acción integral en el camino correspondiente.')]
story += [P('<b>Qué no debes hacer:</b> elegir PID, PI o una ganancia al azar antes de decidir la arquitectura. Primero explica qué mide cada sensor y por qué la perturbación es rechazada por ese camino.', 'Warning'), PageBreak()]

story += section('Qué significa en la industria','Los nombres del examen no son solamente técnicas académicas. Aparecen en sistemas industriales porque cada estructura resuelve una limitación distinta.')
data=[['Estructura','Ejemplo industrial','Por qué se usa'],['Cascada','Temperatura de un intercambiador con lazo interno de caudal.','El caudal cambia antes que la temperatura; el lazo interno corrige antes.'],['Prealimentación','Compensación de potencia ante cambios medidos de caudal de entrada.','Se actúa antes de observar el error de temperatura.'],['Realimentación','Velocidad de un motor o posición de un eje.','Corrige errores, cargas y variaciones no modeladas.'],['Discreto + PI','PLC o controlador digital que regula presión, nivel o velocidad.','El algoritmo se ejecuta cada T segundos con señales muestreadas.'],['ZOH y retardos','Válvula, transporte de material o comunicación industrial.','La orden se mantiene entre muestras y la planta puede responder con retraso.']]
t=Table(data,colWidths=[30*mm,62*mm,61*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),teal),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,-1),FONT),('FONTSIZE',(0,0),(-1,-1),8.2),('LEADING',(0,0),(-1,-1),10.5),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#c8d7dc')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)])); story.append(t)
story += [Spacer(1,8), P('<b>Aplicación a un sistema real:</b> en una línea de proceso, un sensor puede medir la variable final Y, otro una variable intermedia X y un tercero una perturbación P. La decisión no se toma por “tener más bloques”, sino por causalidad, velocidad de respuesta, calidad de medida, ruido, saturación y seguridad.', 'Callout'), P('<b>Importante:</b> un esquema correcto en el examen es un diseño académico. Para maquinaria o proceso real todavía harían falta identificación, límites de actuadores, alarmas, anti-windup, pruebas y validación de seguridad.', 'SmallES'), PageBreak()]

story += section('Hoja de estrategia para resolverlo','Úsala mientras haces el examen y escribe las decisiones, no solo las operaciones.')
checks=[['Paso','Pregunta que debes contestar'],['1. Clasificar','¿Continuo o discreto? ¿Proceso, controlador o estructura?'],['2. Definir señales','¿Qué son r/u/y/e, X, Y y P? ¿Dónde entra cada una?'],['3. Elegir método','¿ZOH, Tustin, cascada, prealimentación o realimentación?'],['4. Calcular','Escribe la fórmula antes de sustituir números. Conserva unidades.'],['5. Comprobar','Polos, estabilidad, signo, error final, rapidez y sobreoscilación.'],['6. Dibujar','El diagrama debe mostrar sensores, sumadores, lazos y sentido de señales.'],['7. Explicar','Añade una frase de por qué la solución cumple lo pedido.']]
t=Table(checks,colWidths=[33*mm,120*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),teal),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,-1),FONT),('FONTSIZE',(0,0),(-1,-1),9),('LEADING',(0,0),(-1,-1),12),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#c8d7dc')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)])); story.append(t)
story += [Spacer(1,12), P('<b>Autoevaluación antes de mirar una solución:</b>', 'H2ES'), bullet('¿Puedo explicar con mis palabras qué hace ZOH?'), bullet('¿Sé por qué la estabilidad discreta se mira dentro del círculo unidad?'), bullet('¿Sé distinguir cascada de prealimentación?'), bullet('¿Puedo justificar qué sensor necesito y qué ocurre si no puedo medir P?'), bullet('¿He comprobado que mi respuesta cumple rapidez, sobreoscilación y error estacionario?'), Spacer(1,10), P('No se ha incorporado aquí una solución completa. Cuando termines tu intento, podemos corregirlo paso a paso empezando por el primer error, conservando lo que esté bien.', 'Callout'), P('<b>Alcance y fuentes:</b> enunciado escaneado del examen 1erP_24_11_2022.pdf; guía docente de Técnicas de Control; material UD1 y UD2 de grupos 233-234 como apoyo explicativo. Las aplicaciones industriales y comentarios están marcados como explicación propia.', 'SmallES')]

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=18*mm,title='Primer parcial de Técnicas de Control - guía comentada',author='UPVITOR')
doc.build(story,onFirstPage=header_footer,onLaterPages=header_footer)
print(OUT)
