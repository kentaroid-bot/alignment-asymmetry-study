"""Render the saved pilot data as a vector scientific plot and PNG."""
import json, shutil, subprocess, os, sys
from pathlib import Path
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics import renderPDF
from reportlab.lib import colors
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'figures';out.mkdir(exist_ok=True)
rows=json.loads((ROOT/'data/pilot-002/results-summary.json').read_text())['rows']
d=Drawing(680,260);palette=[colors.HexColor('#24618a'),colors.HexColor('#bc652c')]
for j,w in enumerate(['A','B']):
 x=45+j*340
 plot=LinePlot();plot.x=x;plot.y=48;plot.width=280;plot.height=156
 plot.data=[[(i,next(r['H'] for r in rows if r['world']==w and r['state']==s and r['pair']==p)) for i,p in enumerate(['BB','UB','BU','UU'])] for s in [0,1]]
 plot.xValueAxis.valueMin=0;plot.xValueAxis.valueMax=3;plot.xValueAxis.valueSteps=[0,1,2,3]
 plot.xValueAxis.labelTextFormat=lambda v:['NN','UN','NU','UU'][int(v)]
 plot.yValueAxis.valueMin=0;plot.yValueAxis.valueMax=1;plot.yValueAxis.valueSteps=[0,.25,.5,.75,1]
 plot.yValueAxis.labelTextFormat='%.2f';plot.yValueAxis.visibleGrid=1;plot.yValueAxis.gridStrokeColor=colors.HexColor('#e0e5ea')
 plot.xValueAxis.labels.fontName='Helvetica';plot.xValueAxis.labels.fontSize=10;plot.yValueAxis.labels.fontSize=9
 for i in [0,1]:
  plot.lines[i].strokeColor=palette[i];plot.lines[i].strokeWidth=2;plot.lines[i].symbol=makeMarker('FilledCircle' if i==0 else 'FilledSquare');plot.lines[i].symbol.size=6;plot.lines[i].symbol.fillColor=palette[i]
 d.add(plot)
 d.add(String(x,230,'A: unilateral execution' if w=='A' else 'B: default allocation',fontName='Helvetica-Bold',fontSize=12,fillColor=colors.HexColor('#23354a')))
 d.add(String(x-22,211,'H',fontName='Helvetica-Bold',fontSize=10))
 for i in [0,1]:d.add(String(x+90*i,214,f'State {i}',fontName='Helvetica',fontSize=10,fillColor=palette[i]))
 d.add(String(x+65,14,'Protocol use: P / Q',fontName='Helvetica',fontSize=10))
renderPDF.drawToFile(d,str(out/'pilot-harm.pdf'))
exe=shutil.which('pdftoppm')
if not exe:raise RuntimeError('Poppler pdftoppm is required')
env=os.environ.copy()
if sys.platform=='darwin' and 'FONTCONFIG_FILE' not in env:
 cache=ROOT/'tmp/pdfs/font-cache';cache.mkdir(parents=True,exist_ok=True)
 config=ROOT/'tmp/pdfs/fonts.conf'
 config.write_text('<?xml version="1.0"?><fontconfig><dir>/System/Library/Fonts/Supplemental</dir><cachedir>'+str(cache)+'</cachedir></fontconfig>')
 env['FONTCONFIG_FILE']=str(config)
subprocess.run([exe,'-r','200','-png','-singlefile',str(out/'pilot-harm.pdf'),str(out/'pilot-harm')],check=True,env=env,timeout=60,capture_output=True)
print('figures/pilot-harm.pdf and .png')
