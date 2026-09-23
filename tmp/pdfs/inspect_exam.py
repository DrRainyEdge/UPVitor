from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[2]
source = root / 'Tecnicas_de_Control/sources/exams/unsolved/1erP_24_11_2022.pdf'
out = root / 'tmp/pdfs/exam_source_render'
out.mkdir(parents=True, exist_ok=True)
doc = pdfium.PdfDocument(source)
thumbs = []
for i, page in enumerate(doc):
    image = page.render(scale=2.4).to_pil().convert('RGB')
    image.save(out / f'page-{i+1:02d}.png')
    thumb = image.copy()
    thumb.thumbnail((620, 877))
    card = Image.new('RGB', (640, 920), 'white')
    card.paste(thumb, ((640-thumb.width)//2, 30))
    ImageDraw.Draw(card).text((12, 8), f'Página {i+1}', fill='black')
    thumbs.append(card)
sheet = Image.new('RGB', (1280, 1840), '#d8dde2')
for i, thumb in enumerate(thumbs):
    sheet.paste(thumb, ((i % 2)*640, (i//2)*920))
sheet.save(out / 'contact.png')
print(f'Rendered {len(doc)} pages')
