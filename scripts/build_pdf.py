"""Build the Japanese paper from its Markdown source using ReportLab."""
import html, json, os, re
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'output/pdf';out.mkdir(parents=True,exist_ok=True)
font=os.environ.get('STUDY_PDF_FONT')
if not font:
 choices=['/System/Library/Fonts/Supplemental/Arial Unicode.ttf','/System/Library/Fonts/STHeiti Light.ttc']
 font=next((f for f in choices if Path(f).exists()),None)
if not font:raise RuntimeError('Set STUDY_PDF_FONT to a Japanese TrueType font')
pdfmetrics.registerFont(TTFont('JP',font))
pdfmetrics.registerFontFamily('JP',normal='JP',bold='JP',italic='JP',boldItalic='JP')
blue=colors.HexColor('#243e56');gray=colors.HexColor('#526273')
body=ParagraphStyle('body',fontName='JP',fontSize=9.7,leading=16.1,wordWrap='CJK',spaceAfter=7,allowWidows=0,allowOrphans=0,textColor=colors.HexColor('#17232e'))
styles={'body':body,'title':ParagraphStyle('title',parent=body,fontSize=21,leading=30,spaceAfter=10,textColor=blue),
 'subtitle':ParagraphStyle('subtitle',parent=body,fontSize=12.5,leading=20,spaceAfter=13,textColor=gray),
 'h2':ParagraphStyle('h2',parent=body,fontSize=14,leading=22,spaceBefore=16,spaceAfter=8,keepWithNext=True,textColor=blue),
 'h3':ParagraphStyle('h3',parent=body,fontSize=11.1,leading=18,spaceBefore=10,spaceAfter=5,keepWithNext=True,textColor=blue),
 'cell':ParagraphStyle('cell',parent=body,fontSize=8.3,leading=13,spaceAfter=0),
 'head':ParagraphStyle('head',parent=body,fontSize=8.3,leading=13,spaceAfter=0,textColor=colors.white),
 'caption':ParagraphStyle('caption',parent=body,fontSize=8.3,leading=13,textColor=gray),
 'ref':ParagraphStyle('ref',parent=body,fontSize=8.5,leading=14,spaceAfter=6)}
def markup(s):
 s=s.replace('−','-').replace('—','-').replace('–','-')
 # Escaping happens before adding ReportLab markup.
 s=html.escape(s)
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:'<a href="'+m[2]+'" color="#236488">'+m[1]+'</a>',s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
 s=re.sub(r'`([^`]+)`',r'\1',s)
 return s
P=lambda s,style='body':Paragraph(markup(s),styles[style])
W,H=595.276,841.89;margin=48;width=W-margin*2
story=[];lines=(ROOT/'manuscript/paper.ja.md').read_text().splitlines();i=0;refs=False
while i<len(lines):
 line=lines[i].strip()
 if not line:i+=1;continue
 if line.startswith('# '):story.append(P(line[2:],'title'));i+=1;continue
 if line.startswith('## '):
  txt=line[3:]
  style='subtitle' if txt.startswith('Unflatten Adaptive') else 'h2'
  refs=txt=='参考文献・一次資料' or refs
  story.append(P(txt,style));i+=1;continue
 if line.startswith('### '):story.append(P(line[4:],'h3'));i+=1;continue
 if line.startswith('|'):
  rows=[]
  while i<len(lines) and lines[i].strip().startswith('|'):
   cells=[c.strip() for c in lines[i].strip().strip('|').split('|')];i+=1
   if all(re.fullmatch(r'[:\- ]+',c) for c in cells):continue
   rows.append(cells)
  n=len(rows[0]);table=Table([[P(c,'head' if rid==0 else 'cell') for c in row] for rid,row in enumerate(rows)],colWidths=[width/n]*n,repeatRows=1,hAlign='LEFT')
  table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),blue),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f1f5f8'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#cbd5dd'))]))
  story.extend([Spacer(1,5),KeepTogether([table]),Spacer(1,10)]);continue
 if line.startswith('!['):
  m=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',line);p=(ROOT/'manuscript'/m[2]).resolve()
  from PIL import Image as PILImage
  with PILImage.open(p) as im:iw,ih=im.size
  story.extend([Spacer(1,6),Image(str(p),width=width,height=width*ih/iw),Spacer(1,4)]);i+=1;continue
 parts=[line];i+=1
 while i<len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(('#','|','![','- ')) and not re.match(r'^\d+\. ',lines[i].lstrip()):
  parts.append(lines[i].strip());i+=1
 text=' '.join(parts)
 if text.startswith('- '):text='・'+text[2:]
 story.append(P(text,'ref' if refs else 'caption' if text.startswith('図1は') else 'body'))

def footer(c,doc):
 c.saveState();c.setStrokeColor(colors.HexColor('#d5dfe6'));c.line(margin,40,W-margin,40)
 c.setFont('Helvetica',8);c.setFillColor(gray);c.drawString(margin,27,'ALIGNMENT ASYMMETRY STUDY  /  v1.0  /  2026-09-09')
 c.drawRightString(W-margin,27,str(doc.page))
 if doc.page>1:c.setFont('Helvetica',8);c.drawString(margin,H-28,'Unflatten Adaptive 0.3.2 + Aperture Mesh Protocol')
 c.restoreState()
path=out/'alignment-asymmetry-study.pdf'
doc=SimpleDocTemplate(str(path),pagesize=(W,H),rightMargin=margin,leftMargin=margin,topMargin=44,bottomMargin=54,title='Unflatten Adaptive 0.3.2 and Aperture Mesh: Alignment Asymmetry Study',author='kentaroid-bot; AI assistance: Astra',subject='Exploratory technical report, not peer reviewed')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
r=PdfReader(path);report={'pages':len(r.pages),'source_characters':sum(len(x) for x in lines),'extracted_characters':sum(len(p.extract_text()) for p in r.pages),'page_text_characters':[len(p.extract_text()) for p in r.pages]}
(ROOT/'tmp/pdfs').mkdir(parents=True,exist_ok=True);(ROOT/'tmp/pdfs/text-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
