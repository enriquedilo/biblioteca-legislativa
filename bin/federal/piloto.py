#!/usr/bin/env python3
"""Piloto federal. Reutiliza controles conservadores existentes sin crear índices."""
import sys,json,re,datetime,hashlib,os
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin
ROOT=Path(__file__).resolve().parents[2]; FED=ROOT/'Federal'
sys.path.insert(0,str(ROOT/'bin/nayarit'))
import biblioteca as base
base.ROOT=FED;base.BASE='https://www.diputados.gob.mx/LeyesBiblio/'
os.environ['BIBLIOTECA_CACHE_NAYARIT']=str(FED/'preparacion')
class Table(HTMLParser):
 def __init__(self):super().__init__();self.rows=[];self.row=None;self.cell=None;self.href=None
 def handle_starttag(self,t,a):
  if t=='tr':self.row=[]
  if t=='td' and self.row is not None:self.cell={'text':'','links':[]};self.row.append(self.cell)
  if t=='a' and self.cell is not None:
   self.href=dict(a).get('href','');self.cell['links'].append({'href':self.href,'text':''})
 def handle_endtag(self,t):
  if t=='a':self.href=None
  if t=='td':self.cell=None
  if t=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
 def handle_data(self,d):
  if self.cell is not None:
   self.cell['text']+=d+' '
   if self.href and self.cell['links']:self.cell['links'][-1]['text']+=d

def catalog():
 old=FED/'catalogo/catalogo.json';prior=json.loads(old.read_text()) if old.exists() else [];ids={r['url_pdf']:r['id'] for r in prior};nextid=max(ids.values(),default=0)+1;rows=[]
 for section,pattern in [('index.htm',r'^pdf/[^/]+\.pdf$'),('regla.htm',r'^regley/Reg_[^/]+\.pdf$')]:
  p=Table();p.feed((FED/'catalogo'/section).read_bytes().decode('cp1252'))
  for cells in p.rows:
   links=[l for c in cells for l in c['links']];pdf=next((l['href'] for l in links if re.match(pattern,l['href'],re.I)),None)
   if not pdf:continue
   # Only numbered entries in the vigente table, excluding navigation and compilations.
   if not cells or not re.fullmatch(r'\s*\d+\s*',cells[0]['text']):continue
   sigla=Path(pdf).stem;url=urljoin(base.BASE,pdf)
   if any(r['url_pdf']==url for r in rows):continue
   titlelinks=[l for l in cells[1]['links'] if l['text'].strip()]
   name=' '.join((titlelinks[0]['text'] if titlelinks else cells[1]['text'].split('DOF')[0]).split())
   word=next((l['href'] for l in links if Path(l['href']).stem.lower()==sigla.lower() and l['href'].lower().endswith('.doc')),None)
   low=name.casefold();tipo='reglamento' if section=='regla.htm' else ('constitucion' if low.startswith('constitución') else 'codigo' if low.startswith('código') else 'ley_general' if low.startswith('ley general') else 'ley_organica' if low.startswith('ley orgánica') else 'ley')
   ident=ids.get(url)
   if ident is None:ident=nextid;nextid+=1
   rows.append({'id':ident,'sigla':sigla,'slug':sigla.lower(),'nombre_catalogo':name,'nombre_catalogo_sitio':name,'ley':name,'url_pdf':url,'url_word':urljoin(base.BASE,word) if word else None,'nb_extword':'doc','seccion_sitio':section,'secciones_sitio':[section],'orden':'federal','regimen':'general','tipo':tipo,'vigencia_anual':(low.startswith('ley de ingresos de la federación') and 'ejercicio fiscal' in low) or 'tarifa de la ley de los impuestos generales de importación y exportación' in low})
 base.savejson(old,rows);return rows

def iso(s):
 m=re.search(r'\b(\d{2})[-/](\d{2})[-/](\d{4})\b',s)
 if m:
  try:return datetime.date(int(m[3]),int(m[2]),int(m[1])).isoformat()
  except ValueError:return None
 return base.date(s)

def normative(raw):
 head=' '.join(raw.split('\f')[0].split());inc=[]
 pub=re.search(r'(?:Constitución|Código|Ley|Reglamento)(?:\s+\w+){0,20}?\s+publicad[ao].*?\d{4}',head,re.I)
 reform=re.search(r'(?:Última(?:s)?\s+reforma(?:s)?(?:\s+publicada(?:s)?)?|Nueva Ley|Nuevo Reglamento)\s+DOF\s+\d{2}[-/]\d{2}[-/]\d{4}',head,re.I)
 notes=[];ev=[]
 for n,page in enumerate(raw.split('\f'),1):
  lines=page.splitlines();i=0
  while i<len(lines):
   line=lines[i].strip()
   if 'DOF' in line and re.search(r'reformad|adicionad|derogad',line,re.I):
    note=line;j=i+1
    while j<len(lines) and re.match(r'^\s*(?:\d{2}[-/]\d{2}[-/]\d{4}|,)',lines[j]):note+=' '+lines[j].strip();j+=1
    dates=[iso(m[0]) for m in re.finditer(r'\d{2}[-/]\d{2}[-/]\d{4}',note)]
    notes.append({'fecha':dates[0] if len(dates)==1 else None,'po_numero':None,'decreto':None,'nota':note,'fechas':dates});ev.append({'indice':len(notes)-1,'pagina':n,'texto':note});i=j
   else:i+=1
 po={'numero':None,'edicion':None,'fecha':iso(pub[0]) if pub else None,'seccion':None,'diario':'DOF'}
 last={'numero':None,'edicion':None,'fecha':iso(reform[0])} if reform and re.match(r'Última',reform[0],re.I) else None
 for field,value in [('decreto_numero',None)]+[('po_publicacion.'+k,v) for k,v in po.items()]+[('ultima_reforma',last),('abroga',None)]:
  if value is None:inc.append({'campo':field,'motivo':'Dato no localizado de forma inequívoca en lo impreso; no se infiere.','pagina':1})
 inc.append({'campo':'reformas','motivo':'Notas literales conservadas con todas las fechas; fecha escalar null si hay varias. Números de diario/decreto no impresos quedan null. Captura automática pendiente de revisión.'})
 return {'decreto_numero':None,'po_publicacion':po,'ultima_reforma':last,'reformas':notes,'abroga':[]},inc,{'publicacion':pub[0] if pub else None,'ultima_reforma':reform[0] if last else None,'reformas':ev}
base.metadata_normativa=normative

def state(rows,results):
 payload={'fase':'piloto detenido antes de lotes','tamano_lote':10,'catalogados':len(rows),'procesados':len(results),'resultados':results,'actualizado':base.now(),'lotes':[]}
 base.savejson(FED/'reportes/avance_lotes.json',payload)
 (FED/'AVANCE.md').write_text('# Avance Federal\n\nPiloto: '+str(len(results))+'/4. Lotes no iniciados; requieren revisión del usuario.\n\nCatálogo: '+str(len(rows))+' identidades.\n\n'+''.join(f"- {r['sigla']} (ID {r['id']}): {r['resultado']}\n" for r in results))
 (FED/'INDICE.md').write_text('# Biblioteca Federal\n\nFuente: Cámara de Diputados. Captura de índices vigentes; no certifica vigencia jurídica.\n\nPiloto; sin índices de búsqueda ni articulado. Originales y extracción conservados localmente, excluidos de Git conforme a la política del repositorio.\n\n| ID | Sigla | Ordenamiento | Estado |\n|---|---|---|---|\n'+''.join(f"| {r['id']} | {r['sigla']} | {r['nombre_catalogo']} | {'piloto procesado' if any(x['id']==r['id'] and x.get('version') for x in results) else 'pendiente'} |\n" for r in rows))
if __name__=='__main__':
 rows=catalog();selected=[next(r for r in rows if r['sigla']==s) for s in ['CPEUM','CFF','LGDNNA','Reg_CFF']];base.savejson(FED/'reportes/seleccion_piloto.json',selected)
 path=FED/'reportes/piloto_resultados.json';results=json.loads(path.read_text()) if path.exists() else []
 for row in selected:
  if any(r['id']==row['id'] and not any(x.get('url') is None for x in r.get('incidencias_descarga',[])) for r in results):continue
  results=[r for r in results if r['id']!=row['id']]
  try:
   result=base.process(row);dest=FED/'ordenamientos'/str(row['id'])/'versiones'/result['version'];meta=json.loads((dest/'metadata.json').read_text());meta.update(sigla=row['sigla'],vigencia_anual=row['vigencia_anual'],fuente=base.BASE,estatus='Incluido en índice federal vigente; vigencia jurídica no certificada',conversor='Controles conservadores existentes / adaptación federal piloto');base.savejson(dest/'metadata.json',meta)
  except Exception as e:result={'id':row['id'],'resultado':'pendiente','incidencia':str(e)}
  result['sigla']=row['sigla'];results.append(result);base.savejson(path,results);state(rows,results);print(json.dumps(result,ensure_ascii=False),flush=True)
