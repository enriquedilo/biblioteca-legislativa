#!/usr/bin/env python3
"""Convierte originales IEEN respaldados localmente; no descarga reformas ni ejecuta OCR.
Uso: python3 bin/ieen/convertir.py --originales CARPETA --ids 9 10 ...
Reutiliza la conversión conservadora de Nayarit y verifica el Markdown guardado.
"""
import argparse,collections,datetime,hashlib,json,re,shutil,sys,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'bin/nayarit'))
import revisar_local as conv
from pypdf import PdfReader
# El título temático es texto, no sufijo del número de artículo.
NUM=re.compile(r'^(?:ART[ÍI]CULO\.?|ART\.)\s*\d+(?:[oº°])?(?:\s+(?:Bis|Ter|Qu[áa]ter)(?:\s+[A-Z])?)?\s*[.\-–:]+',re.I)
old_decision=conv.heading_decision
def decision(lines,index):
 line=re.sub(r'[ \t]+',' ',lines[index].strip())
 # Las entradas del índice impreso con puntos guía no son artículos del cuerpo.
 if re.match(r'^(?:ART[ÍI]CULO\.?|ART\.)\s*\d+.*\.{3,}\s*\d+\s*$',line,re.I):return None,None
 m=NUM.match(line)
 if m and line[0].isupper():return m,None
 return old_decision(lines,index)
conv.heading_decision=decision
# No normalizamos las comas o cifras impresas.
conv.normalizar_millares=lambda s:s
compact=lambda s:re.sub(r'\s+','',s)
def save(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def process(row,backup,lote=1):
 assert row['vigente']['fecha']==max(x['fecha'] for x in [row['vigente']]+row['reformas']), 'La versión del catálogo no es la más reciente por fecha'
 ident=row['numero'];src=backup/str(ident);pdf=src/'original.pdf';data=pdf.read_bytes();sha=hashlib.sha256(data).hexdigest();receipt=json.loads((src/'descarga.json').read_text());assert receipt['sha256']==sha
 dest=ROOT/'IEEN/ordenamientos'/str(ident)/'versiones'/sha
 if dest.exists():raise ValueError('Versión ya existente: no se sobrescribe; revisar antes de reanudar')
 dest.mkdir(parents=True);shutil.copy2(pdf,dest/'original.pdf');raw=(src/'extraccion.txt').read_text();(dest/'extraccion.txt').write_text(raw)
 pages=raw.split('\f');pages=pages[:-1] if not pages[-1].strip() else pages
 reader=PdfReader(pdf);assert len(pages)==len(reader.pages)
 stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();blocks=[];checks=[];blocked=[]
 for n,(page,pg) in enumerate(zip(pages,reader.pages),1):
  clean,removed=conv.strip_pagination(page,n);inc=[];md=conv.to_markdown(clean,inc);blocked.extend(dict(x,pagina=n) for x in inc)
  flat=compact(conv.unformat(md));assert flat==compact(clean),(ident,n,'conservacion')
  labels=[x.strip() for x in clean.splitlines() if conv.LIST.match(x.strip())];cursor=0
  for label in labels:
   at=flat.find(compact(label),cursor);assert at>=0,(ident,n,'lista');cursor=at+len(compact(label))
  other=pg.extract_text() or '';digits=lambda x:re.sub(r'\D','',x)
  checks.append({'pagina':n,'caracteres_no_blancos':len(flat),'contenido_y_signos_conservados':True,'cifras_pdf_markdown_conservadas':digits(clean)==digits(conv.unformat(md)),'inicios_lista':len(labels),'inicios_lista_conservados':True,'secuencia_cifras_dos_lectores_pdf':digits(page)==digits(other),'frecuencias_digitos_dos_lectores_pdf':collections.Counter(digits(page))==collections.Counter(digits(other)),'paginacion_retirada':removed})
  blocks.append(f'<!-- PAGINA_PDF: {n} -->\n\n'+md)
 text='# '+row['nombre']+'\n\n> Transcripción del PDF original. Véanse metadata.json y validacion.json; no certifica vigencia jurídica.\n\n'+'\n'.join(blocks)
 (dest/'texto.md').write_text(text)
 saved=re.split(r'<!-- PAGINA_PDF: \d+ -->\s*', (dest/'texto.md').read_text())[1:];assert len(saved)==len(pages)
 for n,(pg,md) in enumerate(zip(pages,saved),1):assert compact(conv.strip_pagination(pg,n)[0])==compact(conv.unformat(md))
 empty=[n for n,p in enumerate(pages,1) if len(p.strip())<20]
 title=' '.join(re.split(r'\n\s*\n',pages[0].strip())[0].split())
 official=title if title.lower().startswith(('reglamento','lineamientos','procedimiento')) else None
 incidents=[{'campo':f,'motivo':'No localizado inequívocamente en la extracción; pendiente de cotejo normativo, no se infiere del catálogo.'} for f in ['decreto_numero','po_publicacion','ultima_reforma']]
 if not official:incidents.append({'campo':'nombre_oficial','motivo':'Pendiente cotejo de portada.'})
 abroga=[]
 for n,p in enumerate(pages,1):
  for para in re.split(r'\n\s*\n',p):
   if re.search(r'\b(?:se abroga[n]?|quedan? abrogad[oa]s?)\b',para,re.I):abroga.append({'nombre':None,'fecha':None,'po_numero':None,'nota':' '.join(para.split()),'pagina_pdf':n})
 if not abroga:incidents.append({'campo':'abroga','motivo':'Sin cláusula inequívoca localizada; arreglo vacío no afirma ausencia normativa.'})
 status='pendiente sin texto extraíble; sin OCR' if empty else 'Conversión conservada; cotejo visual e indexación por revisar'
 meta={'id':ident,'nombre_catalogo':row['nombre'],'nombre_oficial':official,'nombre_catalogo_sitio':row['nombre'],'fuente':row['fuente'],'urls':{'pdf':row['vigente']['url'],'word':None},'url_pdf':row['vigente']['url'],'url_word':None,'fecha_descarga':receipt['fecha_descarga'],'hash_sha256':{'pdf':sha},'version':sha,'validacion':status,'tipo':{'Reglamentos':'reglamento','Lineamientos':'lineamientos'}[row['tipo']],'seccion':'electoral','seccion_sitio':row['seccion'],'secciones_sitio':[row['seccion']],'acuerdo':row['vigente']['acuerdo'],'reformas':row['reformas'],'fecha_catalogo_sin_interpretar':row['vigente']['fecha'],'decreto_numero':None,'po_publicacion':None,'ultima_reforma':None,'abroga':abroga,'slug':re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',row['nombre']).encode('ascii','ignore').decode().lower()).strip('-'),'fecha_revision_conversion':stamp,'conversor':'bin/ieen/convertir.py; Poppler layout y controles conservadores Nayarit','origen_markdown':'PDF original; sin OCR; erratas conservadas','procedencia_metadata':{'acuerdo':'catálogo IEEN, versión vigente','reformas':'cadena íntegra del catálogo IEEN, no convertida','nombre_oficial':'primer bloque de portada, pendiente cotejo visual' if official else None}}
 val={'id':ident,'fecha_revision':stamp,'resultado':status,'originales_sha256_verificados':True,'paginas_pdf':len(pages),'paginas_sin_texto':empty,'texto_conservado':True,'transitorios_y_notas_completos_incluidos':True,'ocr_ejecutado':False,'paginas_cotejadas_visualmente':[],'controles_por_pagina':checks,'promociones_encabezado_evitadas':blocked,'incidencias_metadata':incidents,'comparacion_word_pdf':None,'diferencias_de_fuente':['No hay Word en el catálogo; sin comparación Word/PDF.'],'alcance':'Conservación por página de todos los caracteres no blancos, signos, cifras y comienzos de listas respecto de Poppler; doble lector numérico informativo, discrepancias no reparadas. No equivale a cotejo visual integral. Acuerdo y reformas proceden del catálogo por instrucción expresa.'}
 reviewfile=ROOT/f'IEEN/catalogo/revision_lote{lote}.json'
 if reviewfile.exists():
  reviewed=json.loads(reviewfile.read_text()).get(str(ident))
  if reviewed and reviewed['pdf_sha256']==sha:
   for field in ['nombre_oficial','po_publicacion','ultima_reforma','abroga']:meta[field]=reviewed[field]
   val['evidencia_metadata']=reviewed['evidencia'];val['paginas_cotejadas_visualmente']=reviewed['paginas_cotejadas_visualmente']
 save(dest/'metadata.json',meta);save(dest/'validacion.json',val)
 if not empty:
  folder=dest.parents[1];save(folder/'actual.json',{'version':sha,'nombre':meta['nombre_oficial'] or row['nombre'],'validacion':status,'conversor':'ieen-2'});(folder/'actual').symlink_to('versiones/'+sha,target_is_directory=True)
 return {'id':ident,'version':sha,'paginas':len(pages),'paginas_sin_texto':empty,'paginas_cifras_discrepantes':[x['pagina'] for x in checks if not x['secuencia_cifras_dos_lectores_pdf']],'estado':status}
def main():
 p=argparse.ArgumentParser();p.add_argument('--originales',type=Path,required=True);p.add_argument('--ids',type=int,nargs='+',required=True);p.add_argument('--lote',type=int,default=1);a=p.parse_args();rows=json.loads((ROOT/'IEEN/catalogo/normatividad.json').read_text())['documentos'];out=[]
 for i in a.ids:
  row=next(r for r in rows if r['seccion']=='normatividad' and r['numero']==i);assert row['tipo'] in ('Reglamentos','Lineamientos')
  try:r=process(row,a.originales,a.lote)
  except Exception as e:r={'id':i,'estado':'pendiente','incidencia':str(e)}
  out.append(r);save(ROOT/f'IEEN/reportes/lote-{a.lote}.json',out);print(json.dumps(r,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
