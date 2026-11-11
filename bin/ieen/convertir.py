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
 # Las entradas del índice impreso con puntos o guiones guía no son artículos del cuerpo.
 if re.match(r'^(?:ART[ÍI]CULO\.?|ART\.)\s*\d+.*[.\-–—]{3,}\s*\d+\s*$',line,re.I):return None,None
 m=NUM.match(line)
 if m and line[0].isupper():return m,None
 return old_decision(lines,index)
conv.heading_decision=decision
# No normalizamos las comas o cifras impresas.
conv.normalizar_millares=lambda s:s
compact=lambda s:re.sub(r'\s+','',s)
def save(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def sin_texto_sustantivo(pagina):
 # Algunas digitalizaciones solo permiten extraer la marca de agua.
 # Se ignora únicamente para el control: la extracción archivada no se altera.
 letras=re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD',pagina).encode('ascii','ignore').decode().lower())
 return len(pagina.strip())<20 or letras == 'copiadeinternet'

def detectar_blancas(pdf, paginas):
 """Solo blanco uniforme en el render es concluyente; ruido o imagen exige revisión.
 No se ejecuta OCR ni se deduce ausencia de contenido del texto extraído.
 """
 import subprocess,tempfile
 from PIL import Image
 resultado={}
 with tempfile.TemporaryDirectory(prefix='ieen-blancas-') as tmp:
  for n in paginas:
   destino=Path(tmp)/str(n)
   subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-r','150','-singlefile','-gray','-png',str(pdf),str(destino)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
   with Image.open(str(destino)+'.png') as im:
    minimo,maximo=im.convert('L').getextrema()
   resultado[str(n)]={'pagina_pdf':n,'caso':'blanca' if minimo==maximo==255 else 'revision_pendiente',
    'metodo':'Render Poppler 150 dpi, gris; solo blanco uniforme (255) se acepta automáticamente.',
    'extremos_gris':[minimo,maximo]}
 return resultado

def evaluar_capa_texto(paginas_sin_texto, revision, sha, automaticas=None):
 """Cuatro casos: solo texto normativo en imagen impide promover definitivamente.
 Una clasificación desconocida queda pendiente de revisión; nunca se supone gráfica.
 """
 revision=revision or {}; vinculada=revision.get('pdf_sha256')==sha
 clasificaciones=[]
 for n in paginas_sin_texto:
  r=revision.get('paginas_sin_texto',{}).get(str(n),{}) if vinculada else {}
  caso='revision_pendiente';evidencia='Requiere cotejo visual; no se infiere gráfica de la ausencia de texto.'
  if r.get('cotejo_visual') is True and r.get('pagina_pdf')==n and r.get('caso') in ('portada','blanca','grafica','texto_normativo_imagen'):
   caso=r['caso'];evidencia=r.get('evidencia')
   if caso=='portada' and (n!=1 or not revision.get('nombre_oficial') or r.get('contiene_texto_normativo') is not False):caso='revision_pendiente'
  elif vinculada and n==1:
   portada=revision.get('portada',{})
   if revision.get('nombre_oficial') and portada.get('pagina_pdf')==1 and portada.get('cotejo_visual') is True and portada.get('contiene_texto_normativo') is False:
    caso='portada';evidencia=portada.get('evidencia','Portada cotejada, sin texto normativo.')
  auto=(automaticas or {}).get(str(n),{})
  if caso=='revision_pendiente' and auto.get('caso')=='blanca':caso='blanca';evidencia=auto['metodo']
  clasificaciones.append({'pagina_pdf':n,'caso':caso,'evidencia':evidencia})
 bloqueadas=[r['pagina_pdf'] for r in clasificaciones if r['caso']=='texto_normativo_imagen']
 pendientes=[r['pagina_pdf'] for r in clasificaciones if r['caso']=='revision_pendiente']
 return {'criterio_version':2,'promover':not bloqueadas and not pendientes,
         'paginas_interiores_sin_texto':[n for n in paginas_sin_texto if n!=1],
         'excepcion_portada':any(r['caso']=='portada' for r in clasificaciones),
         'clasificacion_paginas':clasificaciones,'paginas_texto_normativo_imagen':bloqueadas,'paginas_por_revisar':pendientes,
         'motivo':('Texto normativo como imagen' if bloqueadas else 'Clasificación visual pendiente' if pendientes else
                   'Páginas sin texto clasificadas: portada, blanca o gráfica; no bloquean promoción' if clasificaciones else
                   'Todas las páginas tienen texto extraíble')}

def aplicar_criterio_portada(dest, revision):
 # Nombre conservado para compatibilidad con las corridas de lotes anteriores.
 meta=json.loads((dest/'metadata.json').read_text());val=json.loads((dest/'validacion.json').read_text())
 assert hashlib.sha256((dest/'original.pdf').read_bytes()).hexdigest()==meta['hash_sha256']['pdf']==meta['version']
 assert val['texto_conservado'] and all(x['contenido_y_signos_conservados'] and x['cifras_pdf_markdown_conservadas'] and x['inicios_lista_conservados'] for x in val['controles_por_pagina'])
 automaticas=detectar_blancas(dest/'original.pdf',val['paginas_sin_texto'])
 decision=evaluar_capa_texto(val['paginas_sin_texto'],revision,meta['version'],automaticas)
 val['deteccion_paginas_blancas']=automaticas;val['control_capa_texto']=decision;val['promovido']=decision['promover']
 if decision['excepcion_portada']:
  meta['nombre_oficial']=revision['nombre_oficial']
  meta['procedencia_metadata']['nombre_oficial']='Transcripción por cotejo visual de portada (página 1), sin texto normativo; sin OCR.'
 if val['paginas_sin_texto']:
  val['incidencia_capa_texto']={'paginas':val['paginas_sin_texto'],'clasificaciones':decision['clasificacion_paginas'],
   'descripcion':decision['motivo'],'accion':'Promover con incidencia; sin OCR.' if decision['promover'] else 'Conservar extracción diagnóstica; sin actual ni índices; sin OCR.'}
  graficas=[r['pagina_pdf'] for r in decision['clasificacion_paginas'] if r['caso']=='grafica']
  val['reglas_graficas_no_representadas_en_texto']={'paginas':graficas,'descripcion':'Las composiciones, logotipos y reglas gráficas de estas páginas no están en texto.md; consultar el PDF original.'} if graficas else None
  val['integridad_cuerpo_verificada']=decision['promover'];val['transitorios_y_notas_completos_incluidos']=decision['promover']
  val['alcance']='Conservación de la extracción Poppler por página, sin OCR. Clasificación de páginas sin texto según IEEN/LEEME.md. Las páginas gráficas no se reproducen en texto y requieren consulta del PDF; no se afirma cotejo visual integral.'
  status=('Promovido: ' if decision['promover'] else 'Pendiente: ')+decision['motivo']+'; sin OCR'
  if decision['promover']:
   text=(dest/'texto.md').read_text()
   text=re.sub(r'^> EXTRACCIÓN DIAGNÓSTICA INCOMPLETA.*$', '> Transcripción del texto extraíble del PDF. Páginas sin texto clasificadas en validacion.json; los gráficos solo están en el original. Sin OCR.',text,flags=re.M)
   (dest/'texto.md').write_text(text)
 else:status=meta['validacion']
 meta['validacion']=status;val['resultado']=status
 save(dest/'metadata.json',meta);save(dest/'validacion.json',val)
 folder=dest.parents[1];link=folder/'actual'
 if decision['promover']:
  if link.exists() or link.is_symlink():assert link.resolve()==dest.resolve(), 'No se sustituye una versión distinta al revisar la promoción'
  else:link.symlink_to('versiones/'+meta['version'],target_is_directory=True)
  save(folder/'actual.json',{'version':meta['version'],'nombre':meta['nombre_oficial'] or meta['nombre_catalogo'],'validacion':status,'conversor':'ieen-5'})
 else:
  # Una revisión negativa solo retira el puntero a esta misma versión.
  if link.is_symlink() and link.resolve()==dest.resolve():
   link.unlink();(folder/'actual.json').unlink(missing_ok=True)
 return decision

TIPOS={'Reglamentos':'reglamento','Reglamento':'reglamento','Lineamientos':'lineamientos','Lineamiento':'lineamientos','Estatuto':'estatuto','Manual':'manual','Política':'politica','Procedimientos':'procedimiento','Protocolo':'protocolo','Guía':'guia'}
def id_catalogo(row):
 return row['numero']+(100 if row['seccion']=='interna' else 0)

def process(row,backup,lote=1):
 assert row['vigente']['fecha']==max(x['fecha'] for x in [row['vigente']]+row['reformas']), 'La versión del catálogo no es la más reciente por fecha'
 ident=id_catalogo(row);src=backup/str(ident);pdf=src/'original.pdf';data=pdf.read_bytes();sha=hashlib.sha256(data).hexdigest();receipt=json.loads((src/'descarga.json').read_text());assert receipt['sha256']==sha
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
 empty=[n for n,p in enumerate(pages,1) if sin_texto_sustantivo(p)]
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
 meta={'id':ident,'nombre_catalogo':row['nombre'],'nombre_oficial':official,'nombre_catalogo_sitio':row['nombre'],'fuente':row['fuente'],'urls':{'pdf':row['vigente']['url'],'word':None},'url_pdf':row['vigente']['url'],'url_word':None,'fecha_descarga':receipt['fecha_descarga'],'hash_sha256':{'pdf':sha},'version':sha,'validacion':status,'tipo':TIPOS[row['tipo']],'seccion':'interna' if row['seccion']=='interna' else 'electoral','seccion_sitio':row['seccion'],'secciones_sitio':[row['seccion']],'acuerdo':row['vigente']['acuerdo'],'reformas':row['reformas'],'fecha_catalogo_sin_interpretar':row['vigente']['fecha'],'decreto_numero':None,'po_publicacion':None,'ultima_reforma':None,'abroga':abroga,'slug':re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',row['nombre']).encode('ascii','ignore').decode().lower()).strip('-'),'fecha_revision_conversion':stamp,'conversor':'bin/ieen/convertir.py; Poppler layout y controles conservadores Nayarit','origen_markdown':'PDF original; sin OCR; erratas conservadas','procedencia_metadata':{'acuerdo':'catálogo IEEN, versión vigente','reformas':'cadena íntegra del catálogo IEEN, no convertida','nombre_oficial':'primer bloque de portada, pendiente cotejo visual' if official else None}}
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
  row=next(r for r in rows if id_catalogo(r)==i);assert row['tipo'] in TIPOS
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
