from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tmp/pdfs/math_deps'))
import sympy as sp
import pdfplumber
from PIL import Image

s,t=sp.symbols('s t',positive=True)
G,C,Gd,Gu,Hd,F,Y,R,D,U=sp.symbols('G C Gd Gu Hd F Y R D U')
checks=[]
def same(name,a,b):
    result=sp.simplify(a-b)==0
    checks.append({'check':name,'pass':bool(result)})
    assert result,(name,sp.simplify(a-b))

closed=sp.solve(sp.Eq(Y,G*(C*(R-Y)+D)),Y)[0]
same('reference transfer',sp.diff(closed,R),C*G/(1+C*G))
same('input disturbance',sp.diff(closed,D),G/(1+C*G))
general=sp.solve(sp.Eq(Y,G*C*(R-Y)+Gd*D),Y)[0]
same('general disturbance',sp.diff(general,D),Gd/(1+C*G))
same('output disturbance',sp.diff(general,D).subs(Gd,1),1/(1+C*G))
K=sp.symbols('K',positive=True)
g=1/((s+1)*(s+5)); controller=K*(s+1)
same('cancellation reference',controller*g/(1+controller*g),K/(s+5+K))
same('cancellation disturbance',g/(1+controller*g),1/((s+1)*(s+5+K)))
g=1/(s+1); controller=6*(s+2)/s
same('2DoF before filter',controller*g/(1+controller*g),6*(s+2)/((s+3)*(s+4)))
same('2DoF disturbance',g/(1+controller*g),s/((s+3)*(s+4)))
filtered=(2/(s+2))*controller*g/(1+controller*g)
same('2DoF after filter',filtered,12/((s+3)*(s+4)))
response=1-4*sp.exp(-3*t)+3*sp.exp(-4*t)
same('2DoF step response',sp.laplace_transform(response,t,s,noconds=True),filtered/s)
same('2DoF derivative',sp.diff(response,t),12*(sp.exp(-3*t)-sp.exp(-4*t)))
ci=sp.Rational(81,10);g1=10/(s+9)
same('cascade attenuation',1/(1+ci*g1.subs(s,0)),sp.Rational(1,10))
same('cascade inner loop',ci*g1/(1+ci*g1),81/(s+90))
ffsolution=sp.solve(sp.Eq(Y,Gu*(C*(R-Y)+F*Hd*D)+Gd*D),Y)[0]
same('feedforward disturbance',sp.diff(ffsolution,D),(Gd+Gu*F*Hd)/(1+C*Gu))
same('feedforward cancellation',(Gd+Gu*F*Hd).subs(F,-Gd/(Gu*Hd)),0)
gu=2/(5*s+1);gd=1/(2*s+1);ff=-(5*s+1)/(2*(2*s+1))
same('feedforward numeric example',gu*ff+gd,0)
L=sp.symbols('L',positive=True)
pade=(2-L*s)/(2+L*s)
same('Pade equivalent form',pade,(1-L*s/2)/(1+L*s/2))
same('Pade Taylor to order two',sp.series(pade,s,0,3).removeO(),sp.series(sp.exp(-L*s),s,0,3).removeO())
same('Pade numeric example',pade.subs(L,2)/(5*s+1),(1-s)/((1+s)*(5*s+1)))
same('delay phase omega 0.1 L2',-sp.Rational(1,10)*2*180/sp.pi,-36/sp.pi)
same('delay phase omega 0.5 L2',-sp.Rational(1,2)*2*180/sp.pi,-180/sp.pi)
same('delay phase omega 1 L2',-1*2*180/sp.pi,-360/sp.pi)
Gp,Gm,E=sp.symbols('Gp Gm E')
pred=Gm*U+(Y-Gm*E*U)
solution=sp.solve([sp.Eq(Y,Gp*U),sp.Eq(U,C*(R-pred))],[Y,U])
same('Smith perfect model',sp.diff(solution[Y],R).subs(Gp,Gm*E),C*Gm*E/(1+C*Gm))
g0=1/(5*s+1);controller=(5*s+1)/s
same('Smith numeric example',controller*g0/(1+controller*g0)*sp.exp(-2*s),sp.exp(-2*s)/(s+1))
same('Smith settling residual',sp.exp(-(2+sp.log(50)-2)),sp.Rational(1,50))
manifest=json.loads((ROOT/'tmp/pdfs/equations/manifest.json').read_text(encoding='utf-8'))
pdf=ROOT/'Tecnicas_de_Control/outputs/PDF/Resumen_UD1_Estructuras_de_Control_formulas.pdf'
with pdfplumber.open(pdf) as doc:
    assert len(doc.pages)==16
    image_count=0
    for page in doc.pages:
        for im in page.images:
            assert im['x0']>=43 and im['x1']<=page.width-43
            assert im['top']>=100 and im['bottom']<=page.height-58
            image_count+=1
    assert image_count==len(manifest),(image_count,len(manifest))
for rec in manifest:
    with Image.open(ROOT/rec['image']) as im:
        assert im.mode=='RGBA'
        assert im.getchannel('A').getextrema()==(0,255)
report={'symbolic_checks':checks,'equation_images':len(manifest),'pdf_images':image_count,'pages':16,'all_passed':True}
(ROOT/'tmp/pdfs/equations/verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PASS:',len(checks),'algebraic checks;',image_count,'equation images; 16 pages; image bounds and transparency checked.')
