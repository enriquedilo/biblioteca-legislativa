import sys,json,re,subprocess,difflib,collections,unicodedata
from pathlib import Path
sys.path.insert(0,'bin');import indices
oldidx=json.loads(subprocess.check_output(['git','show','e37266b5435f9e02936b4bdf56f19eceeaff2fb3:Nayarit/indices/articulos/5.json']));old=Path('Nayarit/ordenamientos/5/versiones',oldidx['version'],'texto.md').read_text();new=Path('Nayarit/ordenamientos/5/actual/texto.md').read_text()
def clean(s):
 s=unicodedata.normalize('NFC',s);s=re.split(r'(?m)^INDICE\s*$',s)[0];s=re.sub(r'<!-- PAGINA_PDF: \d+ -->','',s);s=re.sub(r'(?m)^\s*(?:CONSTITUCI[ÓO]N POL[ÍI]TICA DEL ESTADO LIBRE Y SOBERANO DE NAYARIT|Poder Legislativo del Estado de Nayarit|Secretaría General|\d+)\s*$','',s);s=re.sub(r'Poder Legislativo del Estado de Nayarit\s+Secretaría General','',s);s=s.replace('\\.','.');return re.sub(r'\s+',' ',s).strip()
def parse(s,arts):
 lines=s.split('\n');out={};count=collections.Counter()
 for a in arts:
  dates=re.findall(r'(?m)^P\s*\.\s*O\s*\.[^\n]+','\n'.join(lines[:a['linea_inicio']]))
  key=(a['tipo'],re.match(r'P\s*\.\s*O\s*\.\s*\d+ DE [A-Z]+ DE \d{4}',dates[-1]).group(0) if dates and re.match(r'P\s*\.\s*O\s*\.\s*\d+ DE [A-Z]+ DE \d{4}',dates[-1]) and a['tipo']=='transitorio' else '',a['articulo']);count[key]+=1;k=' | '.join(key)+f' | {count[key]}'
  raw='\n'.join(lines[a['linea_inicio']-1:a['linea_fin']])
  if a['tipo']=='transitorio':raw=re.split(r'(?m)^P\s*\.\s*O\s*\.',raw)[0]
  out[k]={'pagina':a['pagina_pdf'],'texto':clean(raw)}
 return out
a=parse(old,oldidx['articulos']);b=parse(new,indices.articulos_de(new));diff=[]
for k in dict.fromkeys([*a,*b]):
 x=a.get(k);y=b.get(k)
 if x and y and re.sub(r'\s','',x['texto'])==re.sub(r'\s','',y['texto']):continue
 chunks=[]
 if x and y:
  aa=x['texto'].split();bb=y['texto'].split()
  for tag,l,r,u,v in difflib.SequenceMatcher(None,aa,bb,autojunk=False).get_opcodes():
   if tag!='equal':chunks.append({'antes':' '.join(aa[max(0,l-4):r+4]),'despues':' '.join(bb[max(0,u-4):v+4])})
 d={'clave':k,'estado':'añadido' if not x else 'eliminado' if not y else 'modificado','antes':x,'despues':y,'fragmentos':chunks};diff.append(d);print(k,d['estado'],json.dumps(chunks,ensure_ascii=False)[:2500])
Path('vigilancia/conversiones/2026-11-24/comparacion.json').write_text(json.dumps(diff,ensure_ascii=False,indent=2)+'\n')
print('conteos',len(a),len(b))
