from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parents[2]
pdf=root/'Tecnicas_de_Control/outputs/PDF/Primer_Parcial_24-11-2022_guia_comentada.pdf'
out=root/'tmp/pdfs/final_exam_render'; out.mkdir(parents=True,exist_ok=True)
doc=pdfium.PdfDocument(pdf); thumbs=[]
for i,page in enumerate(doc):
    im=page.render(scale=1.6).to_pil().convert('RGB'); im.save(out/f'page-{i+1:02d}.png')
    th=im.copy(); th.thumbnail((420,594)); card=Image.new('RGB',(440,630),'white'); card.paste(th,((440-th.width)//2,24)); ImageDraw.Draw(card).text((10,8),f'Página {i+1}',fill='black'); thumbs.append(card)
sheet=Image.new('RGB',(1760,((len(thumbs)+3)//4)*630),'#d8dde2')
for i,th in enumerate(thumbs): sheet.paste(th,((i%4)*440,(i//4)*630))
sheet.save(out/'contact.png'); print('Rendered',len(doc),'pages')
