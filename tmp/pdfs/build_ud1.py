from pathlib import Path
import math
import sys
import re
import hashlib
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tmp/pdfs/math_deps'))
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['savefig.transparent'] = True
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties
from PIL import Image
OUT = ROOT / 'Tecnicas_de_Control/outputs/PDF/Resumen_UD1_Estructuras_de_Control_formulas.pdf'
MATH_DIR = ROOT / 'tmp/pdfs/equations'
MATH_DIR.mkdir(parents=True, exist_ok=True)
math_records=[]
OUT.parent.mkdir(parents=True, exist_ok=True)
for name, file in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Arial-Italic','ariali.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / file)))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial-Italic', boldItalic='Arial-Bold')
INK=HexColor('#183449'); TEAL=HexColor('#007C83'); MUTED=HexColor('#526475')
PALE=HexColor('#EAF4F3'); LINE=HexColor('#D5E1E5'); ORANGE=HexColor('#AF5B26')
W,H=595.276,841.89
c=canvas.Canvas(str(OUT),pagesize=(W,H))
c.setTitle('UD1 | Estructuras de control avanzadas - Resumen de estudio')
c.setAuthor('UPVITOR | Material de estudio derivado')
c.setSubject('Seguimiento, perturbaciones, 2DoF, cascada, prealimentación, Padé y Smith')
styles={
 'body':ParagraphStyle('body',fontName='Arial',fontSize=10.6,leading=15,textColor=INK,autoLeading='max'),
 'small':ParagraphStyle('small',fontName='Arial',fontSize=8.6,leading=12,textColor=MUTED,autoLeading='max'),
 'formula':ParagraphStyle('formula',fontName='Arial',fontSize=12,leading=19,textColor=INK),
 'cell':ParagraphStyle('cell',fontName='Arial',fontSize=9.4,leading=13,textColor=INK),
}
y=0
def math_image(tex,size=14):
    tex=tex.replace(r'\frac',r'\dfrac')
    key=hashlib.sha256(('transparent-display'+str(size)+tex).encode()).hexdigest()[:16]
    path=MATH_DIR/(key+'.png')
    if not path.exists():
        math_to_image('$'+tex+'$',str(path),prop=FontProperties(size=size),dpi=450,color='#183449',format='png')
    with Image.open(path) as im:
        width,height=im.size
    math_records.append({'latex':tex,'size_pt':size,'image':str(path.relative_to(ROOT))})
    return path,width*72/450,height*72/450
def inline_math(match):
    path,w,h=math_image(match.group(1),10.6)
    return f'<img src="{path.as_posix()}" width="{w}" height="{h}" valign="middle"/>'
def para(text,kind='body',after=9):
    global y
    text=re.sub(r'\$(.+?)\$',inline_math,text)
    p=Paragraph(text,styles[kind]); _,h=p.wrap(W-88,700)
    p.drawOn(c,44,y-h); y-=h+after
def heading(text):
    global y
    y-=5;c.setFillColor(TEAL);c.setFont('Arial-Bold',13);c.drawString(44,y-14,text);y-=25
def box(text,kind='formula'):
    global y
    p=Paragraph(text,styles[kind]); _,h=p.wrap(W-112,650)
    c.setFillColor(PALE);c.roundRect(44,y-h-20,W-88,h+20,7,fill=1,stroke=0)
    p.drawOn(c,56,y-h-10);y-=h+32
def eq(*rows,size=13):
    global y
    images=[math_image(row,size) for row in rows]
    for _,w,_ in images:
        assert w<=W-116, f'Equation too wide: {w}: {rows}'
    height=sum(h for _,_,h in images)+9*(len(images)-1)+20
    c.setFillColor(PALE);c.roundRect(44,y-height,W-88,height,7,fill=1,stroke=0)
    cursor=y-10
    for path,w,h in images:
        c.drawImage(str(path),56,cursor-h,w,h,mask='auto');cursor-=h+9
    y-=height+11
def table(rows,widths):
    global y
    data=[[Paragraph(x,styles['cell']) for x in row] for row in rows]
    t=Table(data,colWidths=widths)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.4,LINE),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    _,h=t.wrap(W-88,700);t.drawOn(c,44,y-h);y-=h+14
def page(n,title,subtitle,source):
    global y
    c.setFillColor(TEAL);c.rect(0,H-12,W,12,fill=1,stroke=0)
    c.setFillColor(MUTED);c.setFont('Arial-Bold',9);c.drawString(44, H-43,'UPVITOR  /  TÉCNICAS DE CONTROL  /  UD1')
    c.setFillColor(INK);c.setFont('Arial-Bold',24);c.drawString(44,H-83,title)
    c.setFillColor(MUTED);c.setFont('Arial',10);c.drawString(44,H-103,subtitle)
    c.setStrokeColor(LINE);c.line(44,47,W-44,47)
    c.setFont('Arial',7.8);c.drawString(44,32,source);c.drawRightString(W-44,32,f'{n} / 16')
    y=H-126
def end():
    print('PAGE_BOTTOM',c.getPageNumber(),round(y,1))
    assert y>=63, f'Page overflow: {y}'
    c.showPage()
def arrow(x1,y1,x2,y2):
    c.setStrokeColor(INK);c.setLineWidth(1);c.line(x1,y1,x2,y2)
    angle=math.atan2(y2-y1,x2-x1);a=5
    for d in [-.5,.5]:c.line(x2,y2,x2-a*math.cos(angle+d),y2-a*math.sin(angle+d))
def block(x,yy,w,label):
    c.setFillColor(PALE);c.setStrokeColor(TEAL);c.roundRect(x,yy-14,w,28,4,fill=1,stroke=1)
    c.setFillColor(INK);c.setFont('Arial-Bold',10);c.drawCentredString(x+w/2,yy-3,label)
def label(x,yy,text):
    c.setFillColor(INK);c.setFont('Arial',9);c.drawString(x,yy,text)
def feedback_diagram(prefilter=False):
    global y
    yy=y-29
    label(46,yy+5,'r');arrow(57,yy,86,yy)
    if prefilter:block(86,yy,48,'F(s)');arrow(134,yy,167,yy)
    else:arrow(86,yy,167,yy)
    c.circle(174,yy,7);label(170,yy+11,'+');label(180,yy-19,'−')
    arrow(181,yy,211,yy);block(211,yy,69,'C(s)');arrow(280,yy,317,yy);label(290,yy+6,'u')
    c.circle(324,yy,7);label(319,yy+11,'+');arrow(324,yy+39,324,yy+7);label(332,yy+30,'dᵢ')
    arrow(331,yy,366,yy);block(366,yy,73,'G(s)');arrow(439,yy,535,yy);label(520,yy+7,'y')
    c.line(490,yy,490,yy-43);c.line(490,yy-43,174,yy-43);arrow(174,yy-43,174,yy-7)
    y=yy-63

page(1,'Estructuras de control','Guía ampliada para estudiar el tema por primera vez','Fuentes: [A] p. 2; [B] pp. 8-18. Referencias completas en p. 16.')
para('El tema trata de cómo organizar un sistema de control para que <b>siga la consigna</b> y <b>rechace perturbaciones</b>. Un PID es una pieza de ese sistema: la estructura, las señales medidas y el lugar donde entra cada perturbación también determinan el resultado.')
feedback_diagram()
para('<b>Notación:</b> r = referencia; y = salida; u = acción de control; C = regulador; G = planta; d<sub>i</sub> = perturbación sumada a la entrada de G. El esquema usa realimentación negativa unitaria. Las variables describen desviaciones respecto al punto de operación.','small')
eq(r'\frac{Y(s)}{R(s)}=\frac{C(s)G(s)}{1+C(s)G(s)}\qquad \frac{Y(s)}{D_i(s)}=\frac{G(s)}{1+C(s)G(s)}')
para('Para obtener cada función se anulan las otras entradas y se suponen condiciones iniciales nulas. Para una perturbación con camino propio y para otra sumada directamente a la salida, respectivamente:')
eq(r'\frac{Y}{D}=\frac{G_d}{1+CG}\qquad \frac{Y}{D_o}=\frac{1}{1+CG}',size=13)
table([['<b>Objetivo</b>','<b>Qué observar</b>'],['Seguimiento de referencia','Error final, tiempo de establecimiento y sobreoscilación tras cambiar r.'],['Rechazo de perturbaciones','Desviación máxima y tiempo de recuperación, manteniendo r fija.'],['Esfuerzo de control','Acción u, límites del actuador y sensibilidad al ruido.']], [145,W-233])
heading('Qué aporta cada estructura')
para('<b>2DoF:</b> ajusta por separado la respuesta a la referencia. <b>Cascada:</b> corrige antes en una variable auxiliar. <b>Prealimentación:</b> compensa una perturbación medida. <b>Padé:</b> aproxima un retardo. <b>Smith:</b> usa un modelo para predecir la salida sin retardo.')
para('Material derivado y reorganizado; no es un documento oficial. Fuente docente principal: grupos 233-234, curso 2026-2027. No se ha identificado material específico del grupo 236 para este resumen.','small')
end()

page(2,'Antes de empezar','Qué controla un sistema y por qué se cierra el lazo','Fuente: [B] pp. 8-15. Explicación y ejemplo introductorio: elaboración propia.')
heading('Las cuatro señales que debes localizar')
table([['<b>Señal</b>','<b>Pregunta que responde</b>','<b>Ejemplo: horno</b>'],['Referencia r','¿Qué valor deseo?','200 °C.'],['Salida y','¿Qué valor tengo?','Temperatura medida.'],['Error e = r − y','¿Cuánto falta?','Si y = 180 °C, e = 20 °C.'],['Control u','¿Qué orden envío?','Potencia del calentador.'],['Perturbación d','¿Qué altera el proceso?','Abrir la puerta o introducir una pieza fría.']], [105,228,W-421])
para('La planta G transforma la acción u en una salida y. El sensor devuelve una medida al comparador. Con realimentación negativa, el regulador recibe el error y actúa para reducirlo. Si y supera la referencia, el error cambia de signo y la acción correctora disminuye.')
eq(r'E(s)=R(s)-Y(s)',r'U(s)=C(s)E(s)\qquad Y(s)=G(s)U(s)')
heading('¿Por qué no basta con mandar una orden fija?')
para('En bucle abierto no se mide el resultado. Una potencia que hoy mantiene 200 °C puede fallar mañana si cambia la carga o la temperatura ambiente. Al cerrar el lazo, el controlador observa la desviación y corrige. A cambio, un diseño incorrecto puede oscilar o volverse inestable.')
box('<b>Idea clave:</b> la realimentación aporta corrección, pero no garantiza por sí sola estabilidad, rapidez ni buen rechazo de perturbaciones. Esas propiedades se comprueban sobre el lazo completo.','body')
heading('Vocabulario mínimo')
para('<b>Servosistema:</b> busca seguir cambios de r. <b>Regulación:</b> busca mantener y cerca de r cuando aparece d. <b>Régimen transitorio:</b> lo que ocurre durante el cambio. <b>Régimen permanente:</b> el comportamiento cuando el transitorio ha desaparecido.')
end()

page(3,'Cómo leer un diagrama','Un método mecánico para no perder signos ni caminos','Fuente: [B] pp. 8-18. Derivación guiada: elaboración propia.')
feedback_diagram()
heading('Paso 1: escribe una ecuación por cada punto')
para('Para el esquema superior, la perturbación d<sub>i</sub> se suma a la entrada de la planta. Se leen los bloques siguiendo las flechas:')
eq(r'E=R-Y',r'U=CE',r'Y=G(U+D_i)')
heading('Paso 2: sustituye y agrupa la salida')
eq(r'Y=G\left[C(R-Y)+D_i\right]=CGR-CGY+GD_i',r'Y(1+CG)=CGR+GD_i')
heading('Paso 3: aplica superposición')
para('El sistema es lineal: para estudiar la referencia se pone D<sub>i</sub> = 0; para estudiar la perturbación se pone R = 0. Así se obtienen dos funciones distintas:')
eq(r'\left.\frac{Y}{R}\right|_{D_i=0}=\frac{CG}{1+CG}',r'\left.\frac{Y}{D_i}\right|_{R=0}=\frac{G}{1+CG}')
para('El denominador 1 + CG es común porque representa la dinámica del mismo lazo cerrado. El numerador cambia porque cada entrada recorre un camino diferente hasta y.')
heading('Tres errores muy frecuentes')
para('<b>1.</b> Usar la misma transferencia para referencia y perturbación.<br/><b>2.</b> Olvidar el sensor cuando la realimentación no es unitaria.<br/><b>3.</b> Cambiar el signo de una perturbación sin mirar el sumador. Empieza siempre escribiendo las ecuaciones del diagrama.')
end()

page(4,'Diseñar para regular','Polos, ceros y perturbaciones: tres comprobaciones distintas','Fuente: [B] pp. 9-25. Ejemplo y aclaraciones: elaboración propia.')
heading('1. El lugar de las raíces fija polos')
para('La ecuación característica es <b>1 + C(s)G(s) = 0</b>. Los polos determinan la estabilidad y condicionan la rapidez; los ceros también modifican la forma de la respuesta. Dos transferencias con los mismos polos pueden presentar sobreoscilaciones diferentes.')
eq(r't_{e,2\%}\approx\frac{4}{\zeta\omega_n}=\frac{4}{\sigma}',r'M_p=\exp\!\left(-\frac{\pi\zeta}{\sqrt{1-\zeta^2}}\right),\qquad 0<\zeta<1')
para('Recordatorio de diseño: aproximaciones para un segundo orden dominante, sin ceros relevantes. ζ es el amortiguamiento y ω<sub>n</sub>, la frecuencia natural en rad/s. σ = ζω<sub>n</sub> es la distancia horizontal de los polos al eje imaginario; M<sub>p</sub> es una fracción (multiplica por 100 para %). No garantizan por sí solas la respuesta real.','small')
heading('2. La acción integral corrige el error persistente')
para('La integral acumula r − y. En un lazo estable y sin saturación sostenida, permite seguir una consigna constante y rechazar una perturbación constante en los modelos habituales del tema. Hay que comprobarlo con la función de transferencia correspondiente y el teorema del valor final; no basta con ver una I en el regulador.')
heading('3. Cancelar un polo puede ocultar un problema')
para(r'<b>Ejemplo propio:</b> $G(s)=\frac{1}{(s+1)(s+5)}$ y $C(s)=K(s+1)$, con K &gt; 0. La cancelación parece eliminar el polo lento −1 al mirar únicamente la referencia:')
eq(r'\frac{Y}{R}=\frac{K}{s+5+K}',r'\frac{Y}{D_i}=\frac{1}{(s+1)(s+5+K)}')
para('Para <b>K = 5</b>, el seguimiento tiene un polo en −10, pero la respuesta a la perturbación conserva el polo lento −1. El sistema puede seguir rápido la consigna y recuperarse despacio de una perturbación. La D ideal de este ejemplo es una simplificación académica.')
box('<b>Regla de resolución:</b> comprueba Y/R y cada Y/D, conserva a la vista los modos cancelados y evita cancelaciones inestables. Un buen seguimiento no demuestra buen rechazo de perturbaciones.','body')
end()

page(5,'Seguimiento y regulación','El mismo lazo afronta dos problemas diferentes','Fuente: [B] pp. 8-25. Desarrollo didáctico: elaboración propia.')
heading('Dos experimentos que conviene separar')
table([['<b>Experimento</b>','<b>Qué cambia</b>','<b>Qué se observa</b>'],['Seguimiento','Cambia r; se fija d = 0.','Rapidez, sobreoscilación y error entre y y r.'],['Regulación','Se mantiene r; aparece d.','Desviación de y y tiempo de recuperación.']], [128,205,W-333])
para('Un controlador puede seguir muy bien una consigna y rechazar lentamente una carga. No es una contradicción: referencia y perturbación recorren caminos distintos hasta la salida.')
heading('Qué aporta la acción integral')
eq(r'e(t)=r(t)-y(t)',r'u_I(t)=K_i\int_0^t e(\tau)\,d\tau')
para('Si queda un error constante, la integral sigue creciendo y obliga al actuador a corregirlo. Suele eliminar el error permanente ante entradas constantes, siempre que el lazo sea estable y el actuador no permanezca saturado.')
heading('Estable no significa bien ajustado')
table([['<b>Magnitud</b>','<b>Pregunta que responde</b>'],['Tiempo de establecimiento','¿Cuándo queda la salida cerca del valor final?'],['Sobreoscilación','¿Cuánto supera la salida el valor deseado?'],['Error permanente','¿Qué diferencia queda al terminar el transitorio?'],['Esfuerzo de control','¿La orden u es físicamente alcanzable?']], [155,W-260])
box('<b>Idea clave:</b> primero demuestra estabilidad. Después evalúa por separado seguimiento, regulación y esfuerzo de control. Una sola gráfica no responde a todo.','body')
end()

page(6,'Dos grados de libertad','Ajustar el seguimiento después de diseñar el rechazo','Fuente: [B] pp. 20-36. Ejemplo basado en los casos de p. 20.')
feedback_diagram(prefilter=True)
eq(r'\frac{Y}{R}=\frac{FCG}{1+CG}\qquad \frac{Y}{D_i}=\frac{G}{1+CG}')
para('<b>Orden de trabajo:</b> primero diseña C para la estabilidad y el rechazo de perturbaciones. Después ajusta el prefiltro F para suavizar el seguimiento. F no cambia la ecuación característica del lazo original, aunque sus propios polos sí aparecen en el camino desde la referencia.')
heading('Ejemplo: mismos polos, menos sobreoscilación')
para(r'Con $G(s)=\frac{1}{s+1}$ y $C(s)=\frac{6(s+2)}{s}$, resulta:')
eq(r'\frac{Y}{R}=\frac{6(s+2)}{(s+3)(s+4)}\qquad \frac{Y}{D_i}=\frac{s}{(s+3)(s+4)}',r'F(s)=\frac{2}{s+2}\quad\Longrightarrow\quad \frac{Y}{R}=\frac{12}{(s+3)(s+4)}')
para(r'El prefiltro tiene ganancia estática 1 y elimina el cero −2 del seguimiento. La respuesta al escalón es $y(t)=1-4e^{-3t}+3e^{-4t}$: crece de forma monótona hacia 1. El camino de la perturbación no cambia.')
heading('PID industrial con ponderación de referencia')
eq(r'u(t)=K_c\left[b\,r(t)-y(t)+\frac{1}{T_i}\int_0^t\!\left(r(\tau)-y(\tau)\right)\,d\tau\right.',r'\left.\qquad\qquad +\,T_d\left(c\,\frac{dr(t)}{dt}-\frac{dy(t)}{dt}\right)\right]',size=13)
para('Expresión académica con estado integral inicial nulo.','small',after=5)
para('<b>b</b> pondera la referencia en la acción proporcional; <b>c</b>, en la derivativa. La integral sigue actuando sobre r − y. Con c = 0 se evita derivar los saltos de consigna; la derivada sobre la medida requiere filtrado en una implementación real.')
para('<b>Límite:</b> un prefiltro debe ser estable y realizable. No se puede invertir libremente un cero inestable ni un retardo. La ponderación b,c modifica los ceros introducidos por el PID, pero no elimina arbitrariamente los de la planta.','small')
end()

page(7,'2DoF paso a paso','Qué cambia el prefiltro y qué permanece igual','Fuente: [B] pp. 26-36. Desarrollo del ejemplo: elaboración propia.')
heading('1. El controlador C cierra el lazo')
para('Con G = 1/(s+1) y C = 6(s+2)/s, el integrador ayuda a eliminar el error permanente. Al cerrar el lazo aparecen los polos −3 y −4, ambos estables. El cero −2 solo aparece en el camino de referencia.')
eq(r'1+C(s)G(s)=\frac{(s+3)(s+4)}{s(s+1)}',r'\frac{Y}{R}=\frac{6(s+2)}{(s+3)(s+4)}')
heading('2. El prefiltro modifica la orden')
para('Se elige F = 2/(s+2). Su ganancia en s = 0 es uno, así que no cambia el valor final de una consigna constante. Su polo −2 cancela el cero −2 únicamente en el camino de referencia.')
eq(r'F(0)=1',r'\frac{Y}{R}=\frac{12}{(s+3)(s+4)}\quad\mathrm{con}\;F(s)=\frac{2}{s+2}')
heading('3. Comprueba qué no ha cambiado')
para('El denominador del lazo, la estabilidad y la transferencia Y/D siguen iguales. Si llega una perturbación, el prefiltro ni siquiera la ve. Por eso C se diseña primero y F después.')
table([['<b>Pregunta</b>','<b>Respuesta</b>'],['¿F estabiliza un lazo inestable?','No; no modifica la ecuación característica original.'],['¿F reduce una perturbación de carga?','No en esta estructura; solo procesa r.'],['¿Se puede cancelar cualquier cero?','No; F debe ser estable, causal y realizable.']], [202,W-307])
box('<b>Mini comprobación:</b> si mejora la respuesta al cambiar r, pero la respuesta ante d queda igual, el prefiltro hace exactamente lo esperado.','body')
end()

page(8,'Control en cascada','Medir una variable intermedia para corregir antes','Fuente: [B] pp. 43-58; ejemplo docente pp. 52-55, recálculo propio.')
para('El regulador externo controla y y entrega la consigna del regulador interno. Este controla una variable auxiliar x sobre la que actúa u. Una perturbación debe afectar a x antes de propagarse a y para que la estructura resulte útil.')
box('r → [regulador externo] → r<sub>x</sub> → [lazo interno] → x → G<sub>2</sub> → y<br/>El lazo interno realimenta x; el externo realimenta y.','body')
para('<b>Ejemplo físico:</b> el lazo externo regula la temperatura de un intercambiador; el interno, el caudal de fluido caliente. Si cambia la presión de suministro, el caudal lo detecta antes de que la temperatura se desvíe demasiado.')
heading('Se diseña de dentro hacia fuera')
para('<b>1.</b> Selecciona x y comprueba las relaciones u → x, d → x y x → y.<br/><b>2.</b> Diseña C<sub>i</sub> (habitualmente P o PI) y verifica estabilidad, rapidez y atenuación.<br/><b>3.</b> Sustituye el lazo interno por su equivalente y diseña el externo.')
eq(r'G_{bi}(s)=\frac{C_i(s)G_1(s)}{1+C_i(s)G_1(s)H_x(s)}',r'G_{\mathrm{externa}}(s)=G_{bi}(s)G_2(s)')
para('El criterio de las diapositivas pide un lazo interno <b>al menos 5 veces más rápido</b> que la dinámica deseada para y. Para un P se plantea una atenuación del 90 % en régimen permanente; con PI, rechazo total de una perturbación constante si se cumplen las condiciones de estabilidad. Son criterios del diseño del tema, no resultados automáticos de elegir P o PI.')
heading('Ejemplo del material: Cᵢ = 8,1')
para(r'Con $G_1(s)=\frac{10}{s+9}$ y $H_x=1$, la relación entre el efecto estático con y sin lazo interno es:')
eq(r'\frac{1}{1+C_iG_1(0)}=\frac{9}{9+10C_i}=0{,}1',r'C_i=8{,}1\qquad G_{bi}(s)=\frac{81}{s+90}')
para('El polo pasa de −9 a −90. A baja frecuencia puede aproximarse G<sub>bi</sub> ≈ 0,9; no lo sustituyas por 1. Si el polo externo objetivo es −4,5, la separación es 90/4,5 = 20: satisface el criterio de rapidez.','small')
end()

page(9,'Cascada paso a paso','Cuándo merece la pena añadir un segundo lazo','Fuente: [B] pp. 43-58. Interpretación didáctica: elaboración propia.')
heading('Ejemplo mental: temperatura y caudal')
para('Queremos mantener una temperatura y. La válvula modifica un caudal x, y ese caudal modifica después la temperatura. Una variación de presión altera primero x. Si medimos el caudal, el lazo interno corrige antes de que el efecto completo llegue a y.')
heading('Orden correcto de diseño')
para('<b>1.</b> Cierra el lazo de caudal y comprueba estabilidad.<br/><b>2.</b> Hazlo claramente más rápido que la temperatura.<br/><b>3.</b> Trata el lazo interno cerrado como parte de la nueva planta.<br/><b>4.</b> Diseña el controlador externo.')
eq(r'G_{bi}(s)=\frac{C_iG_1}{1+C_iG_1H_x}',r'G_{eq}(s)=G_{bi}(s)G_2(s)')
heading('Cómo leer “cinco veces más rápido”')
para('Si el polo externo deseado está cerca de −4,5 rad/s y el interno queda en −90 rad/s, el interno es veinte veces más rápido. La variable x se asienta mucho antes de que y termine su evolución.')
table([['<b>Buena candidata</b>','<b>Mala candidata</b>'],['x se mide con rapidez y poco ruido.','El sensor de x es lento o ruidoso.'],['La perturbación afecta a x antes que a y.','La perturbación entra después del lazo interno.'],['El lazo interno puede ser mucho más rápido.','Ambos lazos tienen velocidades parecidas.']], [251,W-306])
box('<b>Error típico:</b> diseñar primero el lazo externo. Al cerrar después el interno cambia la planta que veía el controlador exterior.','body')
end()

page(10,'Control por prealimentación','Medir la perturbación y compensar su efecto','Fuente: [B] pp. 60-74. Modelo genérico y ejemplo: elaboración propia.')
para('La prealimentación (feedforward) calcula una acción correctora a partir de una <b>perturbación medible</b>. Se mantiene la realimentación para corregir errores del modelo y perturbaciones que no se miden.')
eq(r'Y=G_uU+G_dD\qquad D_m=H_dD',r'U=C(R-Y)+F_{\!ff}D_m')
para('G<sub>u</sub> es el camino completo desde la acción correctora hasta y; G<sub>d</sub>, desde la perturbación hasta y; H<sub>d</sub>, el sensor de la perturbación. El signo del compensador depende de estos caminos y del sumador mostrado en las ecuaciones.')
eq(r'\frac{Y}{D}=\frac{G_d+G_uF_{\!ff}H_d}{1+CG_u}',r'F_{\!ff}=-\frac{G_d}{G_uH_d}\qquad\text{(cancelación ideal)}')
heading('Ejemplo propio, paso a paso')
para(r'Supón $G_u=\frac{2}{5s+1}$, $G_d=\frac{1}{2s+1}$ y $H_d=1$. Variables normalizadas y tiempo en segundos.')
eq(r'F_{\!ff}(s)=-\frac{5s+1}{2(2s+1)}',r'G_uF_{\!ff}=-\frac{1}{2s+1}=-G_d')
para('Las contribuciones se anulan en el modelo ideal. Para una perturbación constante de +1, la compensación final es −0,5: el efecto 2·(−0,5) + 1 es cero. El compensador es propio y tiene su polo en −0,5: es realizable y estable.')
heading('Qué comprobar antes de darlo por válido')
para('La perturbación debe medirse a tiempo y con una escala conocida. La inversión no puede requerir polos inestables, derivación ideal ilimitada ni conocer el futuro. Si el camino de control tarda más que el de la perturbación, la cancelación exacta puede necesitar un adelanto temporal imposible.')
para('<b>Cascada frente a prealimentación:</b> la primera mide una variable afectada por la perturbación y la realimenta; la segunda mide la perturbación y calcula una compensación. Para los ejercicios del tema, asigna a cada perturbación el camino de compensación indicado; pueden aparecer ambas estructuras para perturbaciones distintas.','small')
end()

page(11,'Prealimentación paso a paso','Anticiparse sin abandonar la realimentación','Fuente: [B] pp. 60-74. Desarrollo didáctico: elaboración propia.')
heading('Ejemplo físico')
para('En un depósito calentado, la temperatura de entrada es una perturbación medible. La prealimentación modifica la potencia antes de que la salida se desvíe. La realimentación corrige después errores de modelo, pérdidas no medidas y cambios del proceso.')
heading('De dónde sale el signo negativo')
para('La salida recibe G_dD por la perturbación y G_uF_ffD por la acción anticipada. Para cancelarlas en el modelo se exige que su suma sea cero:')
eq(r'G_dD+G_uF_{ff}D=0',r'F_{ff}=-\frac{G_d}{G_u}')
para('El signo no se memoriza a ciegas: depende de los sumadores y de los signos físicos de G_u y G_d.')
heading('Qué ocurre con un 10 % de error')
para('Si la compensación prevista es −1 pero el camino real de control solo produce −0,9, queda un efecto residual de +0,1. La cancelación ya no es perfecta, pero la realimentación puede reducir ese residuo.')
table([['<b>Prealimentación</b>','<b>Realimentación</b>'],['Actúa al medir d, antes de observar error en y.','Actúa cuando aparece el error r − y.'],['Necesita un modelo de los caminos de d y u.','Puede corregir perturbaciones no medidas.'],['Es sensible a escala, retardo y modelo.','Aporta robustez, pero actúa después del efecto.']], [238,W-293])
box('<b>Conclusión:</b> normalmente se combinan. Feedforward anticipa lo previsible; feedback corrige lo que el modelo no acertó.','body')
end()

page(12,'Retardos y aproximación de Padé','El proceso responde tarde aunque el regulador actúe ahora','Fuente: [B] pp. 75-81 (numeración impresa 76-82).')
para('Un retardo puro L retrasa una señal sin cambiar su forma: y(t) = u(t − L). Aparece por transporte, adquisición de datos, cálculo o actuación. En Laplace se representa por <b>e<super>−Ls</super></b>, con L en la misma unidad de tiempo que el modelo.')
eq(r'G_p(s)=G_0(s)e^{-Ls}',r'\left|e^{-j\omega L}\right|=1\qquad \angle e^{-j\omega L}=-\omega L\;\mathrm{rad}')
para('El retardo añade desfase y puede reducir la estabilidad del lazo aunque no atenúe su magnitud. No equivale exactamente a un polo: durante el tiempo muerto la salida todavía no ha empezado a responder.')
heading('Padé de primer orden')
eq(r'e^{-Ls}\approx\frac{2-Ls}{2+Ls}')
para('Permite trabajar con una función racional y aplicar herramientas de polos y ceros. Introduce un polo en <b>−2/L</b> y un cero en <b>+2/L</b>. Ese cero en el semiplano derecho es una característica de la aproximación; no se debe cancelar con un regulador inestable.')
heading('Ejemplo propio: L = 2 s')
eq(r'G_p(s)=\frac{e^{-2s}}{5s+1}\approx\frac{1-s}{(1+s)(5s+1)}')
para('El retardo exacto empieza a afectar a la salida tras 2 s; la aproximación racional puede producir un transitorio inicial inverso. Sirve para aproximar el diseño, pero la respuesta final debe comprobarse también con el retardo real.')
table([['<b>Pregunta</b>','<b>Consecuencia</b>'],['¿L es pequeño frente a las escalas de tiempo relevantes?','Un orden bajo puede ser suficiente; evalúa el error en la banda de interés.'],['¿Se pretende una respuesta extremadamente rápida?','El desfase del retardo cobra más importancia; verifica estabilidad y márgenes.'],['¿El retardo es grande y está bien identificado?','Puede interesar un predictor de Smith, comprobando sus limitaciones.']], [236,W-324])
para('Aclaración propia: no hay un límite universal de segundos para llamar “pequeño” a un retardo. Importa su relación con la dinámica y las frecuencias a las que trabajará el lazo.','small')
end()

page(13,'Entender el retardo','Por qué unos segundos pueden limitar todo el control','Fuente: [B] pp. 75-81. Cálculos e interpretación: elaboración propia.')
heading('Una imagen mental')
para('Imagina una cinta transportadora: aunque el actuador cambie ahora, el material tarda L segundos en llegar al sensor. Mientras tanto el controlador aún no ve el efecto y puede seguir corrigiendo de más.')
heading('El desfase crece con la frecuencia')
eq(r'\phi(\omega)=-\omega L\;\mathrm{rad}',r'\phi(^\circ)=-\omega L\frac{180}{\pi}')
para('Para L = 2 s, el módulo sigue siendo uno, pero el desfase cambia con ω:')
table([['<b>ω (rad/s)</b>','<b>Desfase</b>','<b>Lectura</b>'],['0,1','−11,5°','Efecto moderado.'],['0,5','−57,3°','Consume bastante margen de fase.'],['1,0','−114,6°','Puede volver peligroso un lazo rápido.']], [125,150,W-275])
heading('Qué representa Padé')
para('Padé sustituye el exponencial por polos y ceros para usar técnicas racionales. En primer orden aproxima bajas frecuencias, pero introduce un cero en el semiplano derecho y no reproduce exactamente el intervalo inicial sin respuesta.')
eq(r'e^{-Ls}\approx\frac{1-Ls/2}{1+Ls/2}')
box('<b>Consecuencia:</b> acelerar el lazo aumenta la frecuencia de cruce y el desfase del retardo. Diseña con Padé si ayuda, pero valida con el retardo exacto.','body')
end()

page(14,'Predictor de Smith','Controlar con una predicción y corregirla con la medida','Fuente: [B] pp. 82-87 (numeración impresa 83-88). Ejemplo propio.')
para('El predictor utiliza un modelo de la planta y del retardo para estimar la salida que se tendría sin esperar al tiempo muerto. La salida medida sigue siendo necesaria para corregir diferencias entre modelo y proceso.')
eq(r'G_p(s)=G_0(s)e^{-Ls}',r'Y_{\mathrm{pred}}=G_mU+\left[Y-G_me^{-L_ms}U\right]',r'U=C\left(R-Y_{\mathrm{pred}}\right)')
para('El primer término estima la salida sin retardo. El corchete compara la medida con la salida retardada que predice el modelo. G<sub>m</sub> y L<sub>m</sub> representan el modelo sin retardo y el tiempo muerto estimado; en el caso perfecto coinciden con G<sub>0</sub> y L.')
heading('Con un modelo perfecto')
eq(r'\frac{Y(s)}{R(s)}=\frac{C(s)G_0(s)}{1+C(s)G_0(s)}\,e^{-Ls}')
para('El controlador puede diseñarse sobre G<sub>0</sub> sin el retardo en la ecuación característica nominal. Sin embargo, <b>la salida real sigue retrasada L</b>. El predictor no elimina el tiempo físico de transporte.')
heading('Ejemplo propio: respuesta nominal')
para(r'Sea $G_0=\frac{1}{5s+1}$, L = 2 s y $C=\frac{5s+1}{\tau_cs}$, con τ<sub>c</sub> = 1 s. Entonces:')
eq(r'\frac{Y(s)}{R(s)}=\frac{e^{-2s}}{s+1}',r'y(t)=0\quad(t<2),\qquad y(t)=1-e^{-(t-2)}\quad(t\geq2)')
para(r'Ante un escalón unitario, el tiempo para entrar en la banda del 2 % es $t_e=2+\ln(50)\approx5{,}91\;\mathrm{s}$. La regla aproximada L + 4τ<sub>c</sub> daría 6 s. La cancelación usada es nominal y afecta a un polo estable; un error de modelo cambia el resultado.')
box('<b>Límites del Smith clásico del tema:</b> necesita un buen modelo y un retardo conocido. No aplicar directamente a plantas inestables. El buen seguimiento nominal no garantiza buen rechazo de perturbaciones ni robustez ante errores de identificación.','body')
end()

page(15,'Smith paso a paso','Qué predice, qué mide y qué puede fallar','Fuente: [B] pp. 82-87. Desarrollo didáctico: elaboración propia.')
heading('Secuencia conceptual')
para('<b>1.</b> El controlador calcula u usando una salida predicha.<br/><b>2.</b> El modelo retardado calcula qué debería medir el sensor.<br/><b>3.</b> Se compara esa predicción con la medida real.<br/><b>4.</b> La diferencia corrige el predictor si planta y modelo no coinciden.')
eq(r'Y_{pred}=G_mU+\left(Y-G_me^{-L_ms}U\right)')
heading('En el caso ideal')
para('Si G_m = G_0 y L_m = L, el controlador se diseña nominalmente sobre G_0. Aun así, la salida física empieza a cambiar después de L: el predictor anticipa información mediante el modelo, pero no elimina el transporte real.')
heading('Si el modelo no coincide')
table([['<b>Error</b>','<b>Consecuencia probable</b>'],['L_m menor que L','El predictor espera la respuesta demasiado pronto y puede corregir en exceso.'],['Ganancia incorrecta','La amplitud predicha no coincide y queda un error residual.'],['Dinámica no modelada','La respuesta puede ser más lenta, oscilatoria o menos robusta.']], [178,W-288])
heading('Decisión rápida')
para('Smith es atractivo si el retardo es grande, casi constante y bien identificado, y G_0 es estable y modelable. Si el retardo varía mucho o la planta es inestable, el esquema clásico no se aplica directamente.')
box('<b>Pregunta:</b> ¿por qué Smith no viola la física? Porque predice con un modelo, pero no hace que materia, energía o información lleguen antes al sensor.','body')
end()

page(16,'Repaso y fuentes','Una ruta de resolución y cuatro comprobaciones rápidas','Resumen elaborado el 22/09/2026. Páginas citadas: posición física en el archivo.')
heading('Antes de resolver un ejercicio')
para('<b>1.</b> Dibuja r, y, u, sensores y cada perturbación.<br/><b>2.</b> Decide qué se mide: y, una variable auxiliar x o la propia perturbación.<br/><b>3.</b> Obtén Y/R y cada Y/D, incluyendo sensores y signos.<br/><b>4.</b> Diseña primero el lazo interno o el compensador auxiliar; después, el externo y el prefiltro si procede.<br/><b>5.</b> Comprueba polos, ceros, error final, rapidez, esfuerzo de control y realizabilidad.')
heading('Preguntas de práctica con respuesta')
table([['<b>Pregunta</b>','<b>Respuesta razonada</b>'],['¿Un prefiltro mejora el rechazo de perturbaciones?','No en la estructura de la p. 6: solo modifica el camino desde r.'],['¿Basta con dos sensores para justificar cascada?','No: x debe ser controlable, reflejar la perturbación y permitir un lazo interno suficientemente rápido.'],['¿La prealimentación ideal siempre se puede implementar?','No: comprueba el sensor, causalidad, estabilidad y grado del compensador.'],['¿Smith hace desaparecer el retardo?','No: el retardo permanece en la respuesta física; simplifica el diseño nominal mediante predicción.']], [219,W-307])
heading('Fuentes y alcance')
para('<b>[A] Guía docente de Técnicas de Control, 2026-2027.</b> Página 2: alcance oficial de la UD1. Archivo: <font size="8">sources/official/GuiaDocente_TC.pdf</font>.','small')
para('<b>[B] UD1 - Estructuras de control avanzadas.</b> Eduardo Quiles; grupos 233 y 234; curso 2026-2027. Secciones utilizadas: pp. 8-25 (seguimiento, regulación y ceros), 26-36 (2DoF), 43-58 (cascada), 60-74 (prealimentación), 75-81 (retardos y Padé), 82-87 (Smith).','small')
para('Archivo [B], relativo a Tecnicas_de_Control:<br/><font size="8">sources/teaching_material/groups_233-234/UD1/<br/>UD1-_Estructuras_de_control_avanzadas.pptx</font><br/>Su contenido real es PDF pese a la extensión. A partir de la página física 75, la numeración impresa va una unidad por delante.','small')
para('<b>Criterio de elaboración:</b> síntesis del material docente, con redacción, esquemas y explicaciones propias. Los ejemplos se identifican como propios o recalculados del material. Se han explicitado estabilidad, causalidad y realizabilidad para evitar aplicar fórmulas fuera de sus hipótesis. Las preguntas son de práctica, no oficiales.','small')
end()
c.save()
r=PdfReader(OUT)
assert len(r.pages)==16
print(OUT)
print('Pages:',len(r.pages),'Bytes:',OUT.stat().st_size)
(MATH_DIR/'manifest.json').write_text(json.dumps(math_records,ensure_ascii=False,indent=2),encoding='utf-8')
