from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[2]
pdf_path = root / 'Tecnicas_de_Control/outputs/PDF/Resumen_UD1_Estructuras_de_Control_formulas.pdf'
out = root / 'tmp/pdfs/rendered_expanded'
out.mkdir(parents=True, exist_ok=True)
doc = pdfium.PdfDocument(pdf_path)
thumbs = []
for i, page in enumerate(doc):
    image = page.render(scale=1.7).to_pil().convert('RGB')
    path = out / f'page-{i+1:02d}.png'
    image.save(path)
    thumb = image.copy()
    thumb.thumbnail((420, 594))
    canvas = Image.new('RGB', (440, 630), 'white')
    canvas.paste(thumb, ((440-thumb.width)//2, 22))
    ImageDraw.Draw(canvas).text((12, 8), f'Página {i+1}', fill='black')
    thumbs.append(canvas)

for group in range(2):
    sheet = Image.new('RGB', (1760, 1260), '#d8dde2')
    for pos, thumb in enumerate(thumbs[group*8:(group+1)*8]):
        sheet.paste(thumb, ((pos % 4)*440, (pos // 4)*630))
    sheet.save(out / f'contact-{group+1}.png')
print(f'Rendered {len(doc)} pages to {out}')
