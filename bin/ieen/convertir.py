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
def evaluar_capa_texto(paginas_sin_texto, revision, sha):
 """Una portada vacía requiere cotejo visual vinculado al mismo PDF; interior bloquea."""
 interiores=[n for n in paginas_sin_texto if n != 1]
 portada=(revision or {}).get('portada',{})
 cotejada=bool(revision and revision.get('pdf_sha256')==sha
               and revision.get('nombre_oficial') and portada.get('pagina_pdf')==1
               and portada.get('cotejo_visual') is True
               and portada.get('contiene_texto_normativo') is False)
 excepcion=paginas_sin_texto==[1] and cotejada
 return {'promover':not paginas_sin_texto or excepcion,
         'paginas_interiores_sin_texto':interiores,
         'excepcion_portada':excepcion,
         'motivo':('Falta texto en páginas interiores' if interiores else
                   'Portada sin contenido normativo cotejada visualmente' if excepcion else
                   'Falta cotejo visual de portada sin contenido normativo' if paginas_sin_texto else
                   'Todas las páginas tienen texto extraíble')}

def aplicar_criterio_portada(dest, revision):
 meta=json.loads((dest/'metadata.json').read_text())
 val=json.loads((dest/'validacion.json').read_text())
 assert hashlib.sha256((dest/'original.pdf').read_bytes()).hexdigest()==meta['hash_sha256']['pdf']==meta['version']
 assert val['texto_conservado'] and all(x['contenido_y_signos_conservados'] and x['cifras_pdf_markdown_conservadas'] and x['inicios_lista_conservados'] for x in val['controles_por_pagina'])
 decision=evaluar_capa_texto(val['paginas_sin_texto'],revision,meta['hash_sha256']['pdf'])
 val['control_capa_texto']=decision
 val['promovido']=decision['promover']
 if decision['excepcion_portada']:
  meta['nombre_oficial']=revision['nombre_oficial']
  meta['procedencia_metadata']['nombre_oficial']='Transcripción por cotejo visual de portada (página 1), sin texto normativo; sin OCR.'
  val['cotejo_portada']=revision['portada']
  val['incidencia_capa_texto']={'paginas':[1],'descripcion':'Portada con membrete y título en imagen, sin texto normativo; cuerpo extraíble completo.', 'accion':'Promoción por excepción de portada, título visual en metadata, sin OCR.'}
  val['integridad_cuerpo_verificada']=True
  val['transitorios_y_notas_completos_incluidos']=True
  val['alcance']='Conservación por página de la extracción Poppler; portada sin texto normativo cotejada visualmente y título transcrito solo en metadata. Se admite la portada por IEEN/LEEME.md. Sin OCR; no es cotejo visual integral.'
  status='Promovido: cuerpo conservado; portada sin texto normativo cotejada visualmente; sin OCR'
  text=(dest/'texto.md').read_text()
  text=text.replace('> EXTRACCIÓN DIAGNÓSTICA INCOMPLETA. Versión no promovida: hay contenido visible del PDF sin capa de texto. Sin OCR. Véanse metadata.json y validacion.json.', '> Transcripción del cuerpo del PDF. Portada en imagen sin texto normativo; título cotejado visualmente en metadata.json. Sin OCR. Véase validacion.json.')
  (dest/'texto.md').write_text(text)
 elif not decision['promover']:
  status='Pendiente: '+decision['motivo']+'; sin OCR; no promovido'
 else:
  status=meta['validacion']
 meta['validacion']=status;val['resultado']=status
 save(dest/'metadata.json',meta);save(dest/'validacion.json',val)
 if decision['promover']:
  folder=dest.parents[1];link=folder/'actual'
  if link.exists() or link.is_symlink():
   assert link.resolve()==dest.resolve(), 'No se sustituye una versión distinta al revisar la promoción'
  else:link.symlink_to('versiones/'+meta['version'],target_is_directory=True)
  save(folder/'actual.json',{'version':meta['version'],'nombre':meta['nombre_oficial'] or meta['nombre_catalogo'],'validacion':status,'conversor':'ieen-4'})
 return decision

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
 reviewed=None
 reviewfile=ROOT/f'IEEN/catalogo/revision_lote{lote}.json'
 if reviewfile.exists():
  reviewed=json.loads(reviewfile.read_text()).get(str(ident))
  if reviewed and reviewed['pdf_sha256']==sha:
   for field in ['nombre_oficial','po_publicacion','ultima_reforma','abroga']:meta[field]=reviewed[field]
   val['evidencia_metadata']=reviewed['evidencia'];val['paginas_cotejadas_visualmente']=reviewed['paginas_cotejadas_visualmente']
 save(dest/'metadata.json',meta);save(dest/'validacion.json',val)
 decision=aplicar_criterio_portada(dest,reviewed)
 status=json.loads((dest/'metadata.json').read_text())['validacion']
 return {'id':ident,'version':sha,'paginas':len(pages),'paginas_sin_texto':empty,'paginas_cifras_discrepantes':[x['pagina'] for x in checks if not x['secuencia_cifras_dos_lectores_pdf']],'estado':status}
def main():
 p=argparse.ArgumentParser();p.add_argument('--originales',type=Path);p.add_argument('--ids',type=int,nargs='+',required=True);p.add_argument('--lote',type=int,default=1);p.add_argument('--revisar-promocion',action='store_true');a=p.parse_args();rows=json.loads((ROOT/'IEEN/catalogo/normatividad.json').read_text())['documentos'];out=[]
 for i in a.ids:
  row=next(r for r in rows if r['seccion']=='normatividad' and r['numero']==i);assert row['tipo'] in ('Reglamentos','Lineamientos')
  try:
   if a.revisar_promocion:
    reviews=json.loads((ROOT/f'IEEN/catalogo/revision_lote{a.lote}.json').read_text());review=reviews[str(i)]
    dest=ROOT/f'IEEN/ordenamientos/{i}/versiones'/review['pdf_sha256']
    r={'id':i,**aplicar_criterio_portada(dest,review)}
   else:
    if a.originales is None:p.error('--originales es obligatorio al convertir')
    r=process(row,a.originales,a.lote)
  except Exception as e:r={'id':i,'estado':'pendiente','incidencia':str(e)}
  out.append(r)
  if not a.revisar_promocion:save(ROOT/f'IEEN/reportes/lote-{a.lote}.json',out)
  print(json.dumps(r,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
