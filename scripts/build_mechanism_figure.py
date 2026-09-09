"""Plot assumption-conditioned participation bounds, not model performance."""
import json, os, shutil, subprocess
from pathlib import Path
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from reportlab.lib import colors
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'experiments/open-world-v1/mechanism-results.json').read_text())
d=Drawing(640,310)
d.add(String(20,286,'Conditional dependency-rent bound',fontName='Helvetica-Bold',fontSize=16,fillColor=colors.HexColor('#243e56')))
d.add(String(20,265,'Gross supply 12; need 6; one-time exit cost 12. No Unflatten effect is assumed.',fontName='Helvetica',fontSize=10))
bs=[0,6,12,24]; alternatives=[4,6,8,10,12]
palette={0:'#b8ddcf',2:'#d4e8db',4:'#e7eadc',6:'#ecd7c5'}
for i,b in enumerate(bs):
    y=60+(3-i)*40
    d.add(String(63,y+15,str(b),fontName='Helvetica',fontSize=11,textAnchor='end'))
    for j,a in enumerate(alternatives):
        r=next(r for r in data['rows'] if r['reserve']==b and r['exit_cost']==12 and r['alternative']==a)
        x=80+j*82; val=r['dependency_rent_bound']
        d.add(Rect(x,y,79,37,fillColor=colors.HexColor(palette[val]),strokeColor=colors.white))
        d.add(String(x+39.5,y+16,str(val)+(' *' if not r['exit_feasible'] else ''),fontName='Helvetica-Bold',fontSize=13,textAnchor='middle'))
for j,a in enumerate(alternatives):d.add(String(119.5+j*82,226,str(a),fontName='Helvetica',fontSize=11,textAnchor='middle'))
d.add(String(80,244,'Alternative supply after exit',fontName='Helvetica',fontSize=10))
d.add(String(20,204,'Reserve',fontName='Helvetica',fontSize=9))
d.add(String(80,38,'* Exit not feasible under the stated resource conditions.',fontName='Helvetica',fontSize=10))
d.add(String(80,20,'Zero means no positive dependency rent in this local model, not absence of all power.',fontName='Helvetica',fontSize=9))
out=ROOT/'figures';renderPDF.drawToFile(d,str(out/'exit-conditions.pdf'))
cache=ROOT/'tmp/pdfs/font-cache';cache.mkdir(parents=True,exist_ok=True)
config=ROOT/'tmp/pdfs/fonts.conf';config.write_text('<?xml version="1.0"?><fontconfig><dir>/System/Library/Fonts/Supplemental</dir><cachedir>'+str(cache)+'</cachedir></fontconfig>')
env=os.environ.copy();env.setdefault('FONTCONFIG_FILE',str(config))
subprocess.run([shutil.which('pdftoppm'),'-r','180','-png','-singlefile',str(out/'exit-conditions.pdf'),str(out/'exit-conditions')],env=env,check=True,capture_output=True,timeout=60)
print('figures/exit-conditions.pdf and .png')
