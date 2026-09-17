#!/usr/bin/env python3
"""Biblioteca de Nayarit: descarga original, conversión conservadora y controles de Sinaloa."""
import os
import argparse,collections,datetime,hashlib,io,json,os,re,subprocess,tempfile,zipfile,unicodedata
from pathlib import Path
from xml.etree import ElementTree as ET
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]/'Nayarit'
BASE='https://congresonayarit.gob.mx/legislacion-estatal/'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def savejson(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(dir=path.parent,prefix=path.name+'.',suffix='.tmp')
 with os.fdopen(fd,'w',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
def extract_word(data,ext):
 if ext=='docx':
  with zipfile.ZipFile(io.BytesIO(data)) as z:root=ET.fromstring(z.read('word/document.xml'))
  ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
  return '\n\n'.join(''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in root.findall('.//w:p',ns))
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp)/'original.doc';p.write_bytes(data)
  return subprocess.check_output(['/usr/bin/textutil','-convert','txt','-stdout',str(p)]).decode('utf-8')
def get(url):
 if not url:raise ValueError('El catálogo no ofrece enlace al original')
 return subprocess.check_output(['curl','-L','--fail','--silent','--show-error','--max-time','60','--retry','2',url])
MONTHS={s:i+1 for i,s in enumerate('enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split())}
DATE=re.compile(r'(\d{1,2})(?:º|o|°)?\.?\s+(?:de\s+)?(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s*(?:de|del)\s+(\d{4})',re.I)
def date(s):
 m=DATE.search(s)
 if not m:return None
 try:return datetime.date(int(m[3]),MONTHS[m[2].lower()],int(m[1])).isoformat()
 except ValueError:return None
TRANS=re.compile(r'^(?:ART[ÍI]CULOS?\s+)?T\s*R\s*A\s*N\s*S\s*I\s*T\s*O\s*R\s*I\s*O\s*S?\s*:?$',re.I)
LIST_ALL=re.compile(r'^(?:[IVXLCDM]+|[A-Za-z]|\d+)[.)](?:-)?\s*')
def metadata_normativa(raw):
 head=' '.join(raw.split('\f')[0].split());inc=[]
 dm=re.search(r'DECRETO\s+N[ÚU]MERO\s+(\d+)',head,re.I)
 pub=re.search(r'(?:Constitución|Código|Ley|Reglamento)\s+publicad[ao]\s+en\s+.*?(?:\d{4})\.',head,re.I)
 publication=pub[0] if pub else None
 ordinal=r'(?:Primera|Segunda|Tercera|Cuarta|Quinta|Sexta|Séptima|Octava|Novena|Décima)(?:\s+(?:Primera|Segunda|Tercera))?'
 sec=re.search(r'(?:Sección\s+'+ordinal+'|'+ordinal+r'\s+Sección)',publication or '',re.I)
 reform=re.search(r'[ÚU]LTIMA\s+(?:REFORMA|ENMIENDA)\s+PUBLICADA[^:]*:\s*(.*?\d{4})',head,re.I)
 po={'numero':None,'edicion':None,'fecha':date(publication or ''),'seccion':sec[0] if sec else None}
 # Do not collapse several printed publication dates into an invented single date.
 if publication and re.search(r'los días|\d+,\s*\d+',publication):po['fecha']=None;inc.append({'campo':'po_publicacion.fecha','motivo':'Publicación en varias fechas; el campo escalar queda null. Se conserva el pasaje completo.','evidencia':publication,'pagina':1})
 last={'numero':None,'edicion':None,'fecha':date(reform[1])} if reform else None
 reforms=[];evidence=[];seen=set()
 for n,page in enumerate(raw.split('\f'),1):
  candidates=[]
  for m in re.finditer(r'\([^()]*P\s*\.\s*O\s*\.[^()]*\)',page,re.I):
   if re.search(r'REFORM|ADICION|DEROG|ENMIEND',m[0],re.I):candidates.append(m[0])
  for m in re.finditer(r'(?m)^\s*P\s*\.\s*O\s*\.[^\n]+',page):
   note=m[0]
   following=page[m.end():].lstrip().splitlines()
   if following and re.match(r'DECRETO\s+(?:N[ÚU]MERO\s+)?\d+',following[0],re.I):note+=' '+following[0].strip()
   candidates.append(note)
  for note in candidates:
   note=' '.join(note.split());key=(n,note)
   if key in seen:continue
   seen.add(key);tail=re.split(r'P\s*\.\s*O\s*\.',note,maxsplit=1,flags=re.I)[-1]
   d=re.search(r'DECRETO\s+(?:N[ÚU]MERO\s+|NO\.?\s*)?(\d+)',note,re.I)
   num=re.search(r'^\s*(?:No\.?|N[úu]m(?:ero)?\.?)\s*(\d+)',tail,re.I)
   reforms.append({'fecha':date(tail),'po_numero':num[1] if num else None,'decreto':d[1] if d else None,'nota':note})
   evidence.append({'indice':len(reforms)-1,'pagina':n,'texto':note})
 for k,v in [('decreto_numero',dm[1] if dm else None)]+[('po_publicacion.'+k,v) for k,v in po.items()]+[('ultima_reforma.'+k,v) for k,v in (last or {'fecha':None,'numero':None,'edicion':None}).items()]:
  if v is None and not any(x['campo']==k for x in inc):inc.append({'campo':k,'motivo':'Dato no impreso de forma identificable; no se infiere.','pagina':1})
 if reforms:
  for field in ['fecha','po_numero','decreto']:
   indices=[i for i,r in enumerate(reforms) if r[field] is None]
   if indices:inc.append({'campo':'reformas[].'+field,'motivo':'Dato ausente o no normalizable sin corregir la nota impresa; queda null y se conserva evidencia literal.','indices':indices})
 else:inc.append({'campo':'reformas','motivo':'Sin notas reconocidas; arreglo vacío, revisar si existen notas con otra presentación.'})
 return {'decreto_numero':dm[1] if dm else None,'po_publicacion':po,'ultima_reforma':last,'reformas':reforms,'abroga':[]},inc,{'publicacion':publication,'ultima_reforma':reform[0] if reform else None,'reformas':evidence}

def attach_normative_validation(val,raw):
 evidence=val.pop('evidencia_metadata');inc=val.pop('incidencias_metadata')
 ev={'abroga':evidence.get('abroga',[])}
 for source,target in [('publicacion','po_publicacion'),('ultima_reforma','ultima_reforma')]:
  if evidence.get(source):ev[target]={'pagina':1,'texto':evidence[source]}
 dm=re.search(r'DECRETO\s+N[ÚU]MERO\s+\d+',raw.split('\f')[0],re.I)
 if dm:ev['decreto_numero']={'pagina':1,'texto':' '.join(dm[0].split())}
 if evidence['reformas']:
  ev['reformas']={'pagina_inicio':evidence['reformas'][0]['pagina'],'encabezado':None,'filas':[{'fila':x['indice'],'texto':x['texto'],'pagina':x['pagina']} for x in evidence['reformas']]}
 val['metadatos_normativos']={'fecha_extraccion':val['fecha_revision'],'estado':'parcial: campos no localizados o estructura impresa no representable en el objeto solicitado','incidencias':inc,'evidencia':ev}
 return val

def process(row,local=None):
 from revisar_local import strip_pagination,to_markdown,compact,unformat,article_ids,lexical_tokens,ORD
 stamp=now();files={};download_issues=[];ext=row.get('nb_extword') or 'docx'
 for kind,suffix,url in [('pdf','pdf',row['url_pdf']),('word',ext,row['url_word'])]:
  if url:
   if local:files[kind]=(local/('original.'+suffix)).read_bytes()
   else:
    cache=Path(os.environ.get('BIBLIOTECA_CACHE_NAYARIT','work/descargas_nayarit')).expanduser()/str(row['id'])
    cache.mkdir(parents=True,exist_ok=True);cached=cache/('original.'+suffix)
    try:
     files[kind]=cached.read_bytes() if cached.exists() else get(url)
     if not cached.exists():cached.write_bytes(files[kind])
    except Exception as e:
     download_issues.append({'archivo':kind,'url':url,'motivo':str(e)})
  else:download_issues.append({'archivo':kind,'url':None,'motivo':'Enlace ausente en el catálogo capturado'})
 if not files.get('pdf',b'').startswith(b'%PDF'):raise ValueError('PDF ausente o inválido; no se promueve versión')
 if 'word' in files:
  if files['word'].startswith(b'PK'):ext='docx'
  elif files['word'].startswith(bytes.fromhex('d0cf11e0a1b11ae1')):ext='doc'
  else:
   download_issues.append({'archivo':'word','motivo':'Formato Word no reconocido; descarga conservada en preparación, pendiente de cotejo.'});del files['word']
 hashes={k:hashlib.sha256(v).hexdigest() for k,v in files.items()};version=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
 folder=ROOT/'ordenamientos'/str(row['id']);dest=folder/'versiones'/version
 dest.mkdir(parents=True,exist_ok=True)
 for kind,data in files.items():
  p=dest/('original.'+('pdf' if kind=='pdf' else ext))
  if p.exists() and p.read_bytes()!=data:raise ValueError('Original existente distinto; no se sobrescribe')
  if not p.exists():p.write_bytes(data)
 raw=subprocess.check_output(['pdftotext','-layout',str(dest/'original.pdf'),'-']).decode('utf-8');pages=raw.split('\f')
 if not pages[-1].strip():pages.pop()
 reader=PdfReader(dest/'original.pdf')
 if len(pages)!=len(reader.pages):raise ValueError('Número de páginas no coincide entre lectores')
 try:word=extract_word(files['word'],ext) if 'word' in files else ''
 except Exception as e:
  word='';download_issues.append({'archivo':'word','motivo':'No se pudo extraer el Word: '+str(e)})
 blocks=[];checks=[];all_preserved=True;heading_corrections=[]
 for n,(page,independent) in enumerate(zip(pages,reader.pages),1):
  clean,removed=strip_pagination(page,n);blocked=[];md=to_markdown(clean,blocked);heading_corrections.extend(dict(x,pagina=n) for x in blocked);preserved=compact(clean)==compact(unformat(md));all_preserved &= preserved
  other=independent.extract_text() or ''
  # Main comparison includes original pagination in both readers, avoiding asymmetric removal.
  numerical=re.sub(r'\D','',page)==re.sub(r'\D','',other)
  old_other=re.sub(r'(?m)^\s*'+str(n)+r'\s*$','',other)
  original_check=re.sub(r'\D','',clean)==re.sub(r'\D','',old_other)
  flat=compact(unformat(md));cursor=0;labels=[l.strip() for l in clean.splitlines() if LIST_ALL.match(l.strip())];lists=True
  for label in labels:
   at=flat.find(compact(label),cursor)
   if at<0:lists=False;break
   cursor=at+len(compact(label))
  blocks.append(f'<!-- PAGINA_PDF: {n} -->\n\n'+md)
  checks.append({'pagina':n,'caracteres_no_blancos':len(compact(clean)),'contenido_y_signos_conservados':preserved,'secuencia_cifras_dos_lectores_pdf':numerical,'inicios_lista':len(labels),'paginacion_retirada':removed,'inicios_lista_conservados':lists,'control_sinaloa_paginacion_retirada':original_check})
 wa,pa=article_ids(word),article_ids(raw);wt,pt=lexical_tokens(word),lexical_tokens(raw)
 trans=[{'pagina':n,'encabezado':l.strip()} for n,p in enumerate(pages,1) for l in p.splitlines() if TRANS.match(l.strip())]
 first=next((j for j,l in enumerate(raw.splitlines()) if TRANS.match(l.strip())),None)
 tail='\n'.join(raw.splitlines()[first:]) if first is not None else ''
 normative,inc,evidence=metadata_normativa(raw)
 # Reviewed abrogation records are tied to the exact PDF hash, never merely to an ID.
 manual=ROOT/'catalogo/metadata_piloto.json';overrides=json.loads(manual.read_text()) if manual.exists() else {}
 review=overrides.get(str(row['id']))
 if review and review['pdf_sha256']==hashes['pdf']:
  normative['abroga']=review['abroga'];inc+=review.get('incidencias',[]);evidence['abroga']=review['evidencia_abroga']
 else:
  evidence['abroga']=[]
  for n,page in enumerate(pages,1):
   for para in re.split(r'\n\s*\n',page):
    flat=' '.join(para.split())
    if not re.search(r'\b(?:se abroga|queda abrogad[ao])\b',flat,re.I):continue
    evidence['abroga'].append({'pagina':n,'texto':flat})
    title=re.search(r'(?:se abroga|queda abrogad[ao])\s+(?:la\s+|el\s+)?((?:Ley|Código|Reglamento|Arancel)\b.*?)(?=,|\s+publicad[ao]|\s+expedid[ao]|\s+que\s|\.$)',flat,re.I)
    decree=re.search(r'decreto\s+(?:n[úu]mero\s+|no\.?\s*)?(\d+)',flat,re.I)
    # Only a date in a clause explicitly tying publication to the repealed ordering is eligible.
    pubdate=re.search(r'publicad[ao]\s+.*',flat,re.I)
    normative['abroga'].append({'nombre':title[1].strip() if title else None,'po_numero':None,'fecha':date(pubdate[0]) if pubdate else None,'decreto':decree[1] if decree else None})
  inc.append({'campo':'abroga','motivo':'Cláusulas expresas capturadas para cotejo; no se infieren nombres ni fechas faltantes. Revisar evidencia impresa.' if evidence['abroga'] else 'No se localizaron cláusulas con la forma expresa se abroga/queda abrogado; arreglo vacío pendiente de cotejo.'})
 if not normative['abroga'] and review:inc.append({'campo':'abroga','motivo':'No se identificó abrogación expresa de un ordenamiento en el PDF completo; arreglo vacío.'})
 for k in ['nombre','po_numero','fecha','decreto']:
  ids=[j for j,r in enumerate(normative['abroga']) if r[k] is None]
  if ids:inc.append({'campo':'abroga[].'+k,'motivo':'Dato no impreso; queda null.','indices':ids})
 if not review:
  literal=' '.join(pages[0].split()) if pages else ''
  words=[re.escape(x) for x in row['nombre_catalogo'].split()]
  name_match=re.search(r'\s+'.join(words),literal,re.I)
  if name_match:review={'nombre_oficial':name_match[0]}
  else:inc.append({'campo':'nombre_oficial','motivo':'Nombre de catálogo no cotejado literalmente en la primera página; nombre oficial queda null.'})
 empty=[n for n,p in enumerate(pages,1) if len(p.strip())<20]
 discrepancies=[]
 if wa!=pa:discrepancies.append('La secuencia de encabezados numéricos difiere Word/PDF; consultar contadores y evidencia. No se corrige.')
 if wt!=pt:discrepancies.append('La comparación léxica Word/PDF no coincide: encabezados repetidos, campos Word y otras diferencias pendientes de cotejo. No equivale a pérdida del Markdown.')
 if any(not x['control_sinaloa_paginacion_retirada'] for x in checks):discrepancies.append('El control original con retirada de paginación difiere. Se conserva el resultado y se añade comparación simétrica de cifras sin retirar paginación.')
 status='pendiente sin texto extraíble; sin OCR' if empty else ('Conversión conservada; cotejo Word/PDF con incidencias' if discrepancies else 'Conversión conservada; pendiente de cotejo visual')
 val={'id':row['id'],'fecha_revision':stamp,'resultado':status,'originales_sha256_verificados':True,'paginas_pdf':len(pages),'paginas_sin_texto':empty,'pagina_blanca_confirmada_visualmente':False,'texto_conservado':all_preserved,
 'comparacion_word_pdf':{'palabras_comparadas':len(wt),'palabras_pdf':len(pt),'frecuencias_coinciden':collections.Counter(wt)==collections.Counter(pt),'orden_coincide_separando_nota_al_pie':wt==pt,'nota_al_pie_reubicada_por_lector_word':None,'normalizaciones_solo_comparacion':['Misma función lexical_tokens de Sinaloa; no modifica los originales ni el Markdown.'],'limite':'Campos Word y encabezados permanecen en el control; las diferencias se reportan sin reparación.','solo_word':dict(collections.Counter(wt)-collections.Counter(pt)),'solo_pdf':dict(collections.Counter(pt)-collections.Counter(wt))},
 'articulos_word':wa,'articulos_pdf':pa,'identificadores_articulos_coinciden':set(wa)==set(pa),'encabezados_transitorios':trans,'encabezados_ordinales_en_seccion_transitoria':[l.strip() for l in tail.splitlines() if ORD.match(l.strip())],'articulos_numericos_en_seccion_transitoria':article_ids(tail),'transitorios_y_notas_completos_incluidos':all_preserved and bool(trans),'paginas_cotejadas_visualmente':[],'controles_por_pagina':checks,'alcance':'Controles de conservación en todas las páginas; comparación de cifras con Poppler y pypdf. El cotejo visual se registra por separado. No certifica vigencia jurídica.','incidencias_resueltas':[],'diferencias_de_fuente':discrepancies,'incidencias_metadata':inc,'evidencia_metadata':evidence,'formato_word_original':ext,'ocr_ejecutado':False,'incidencias_descarga':download_issues}
 if any(not x['secuencia_cifras_dos_lectores_pdf'] for x in checks):
  val['diferencias_de_fuente'].append('Hay discrepancias en la secuencia de cifras entre los dos lectores PDF; requieren cotejo, no se reparan.')
 if ext=='doc':val['diferencias_de_fuente'].append('Word original .doc conservado por autorización expresa del usuario; no se fabrica original.docx.')
 meta={'id':row['id'],'nombre_catalogo':row['nombre_catalogo'],'nombre_oficial':review['nombre_oficial'] if review else None,'nombre_oficial_pendiente_de_cotejo':not bool(review),'fuente':BASE,'urls':{'pdf':row['url_pdf'],'word':row['url_word']},'fecha_descarga':datetime.datetime.fromtimestamp((local/'original.pdf').stat().st_mtime,datetime.timezone.utc).isoformat() if local else stamp,'fecha_catalogo_sin_interpretar':None,'ultima_reforma':normative['ultima_reforma'],'evidencia_encabezado':[x for x in [evidence['publicacion'],evidence['ultima_reforma']] if x],'hash_sha256':hashes,'version':version,'origen_markdown':'PDF original; conserva texto, numeración impresa, fracciones, transitorios y notas','estatus':'Incluido en catálogo de Nayarit; vigencia jurídica no verificada','validacion':status,'fecha_revision_conversion':stamp,'conversor':'Poppler pdftotext -layout / controles de Sinaloa adaptados a Nayarit v2','decreto_numero':normative['decreto_numero'],'po_publicacion':normative['po_publicacion'],'reformas':normative['reformas'],'abroga':normative['abroga'],'slug':row['slug'],'url_pdf':row['url_pdf'],'url_word':row['url_word'],'seccion_sitio':row['seccion_sitio'],'secciones_sitio':row['secciones_sitio'],'nombre_catalogo_sitio':row['nombre_catalogo_sitio'],'orden':row['orden'],'regimen':row['regimen'],'tipo':row['tipo']}
 (dest/'extraccion.txt').write_text(raw,encoding='utf-8');(dest/'texto.md').write_text('# '+(meta['nombre_oficial'] or row['ley'])+'\n\n> Transcripción del PDF descargado. Consulta metadata.json y validacion.json para límites e incidencias.\n\n'+'\n'.join(blocks),encoding='utf-8')
 val['promociones_encabezado_evitadas']=heading_corrections
 attach_normative_validation(val,raw)
 savejson(dest/'metadata.json',meta);savejson(dest/'validacion.json',val)
 if not all_preserved:raise ValueError('Conversión altera contenido; versión no promovida')
 savejson(folder/'actual.json',{'version':version,'nombre':meta['nombre_oficial'] or row['ley'],'validacion':status,'conversor':4})
 link=folder/'actual';temp=folder/'actual.tmp'
 if temp.is_symlink():temp.unlink()
 temp.symlink_to('versiones/'+version,target_is_directory=True);os.replace(temp,link)
 return {'id':row['id'],'resultado':status,'paginas':len(pages),'version':version,'campos_incompletos':sorted(set(x['campo'] for x in inc)),'paginas_sin_texto':empty,'incidencias_descarga':download_issues,'paginas_cifras_discrepantes':[x['pagina'] for x in checks if not x['secuencia_cifras_dos_lectores_pdf']],'remisiones_en_cuerpo':len(heading_corrections)}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--piloto-local',type=Path);args=p.parse_args()
 if not args.piloto_local:p.error('Use lotes.py para continuar; esta entrada solo procesa el piloto local.')
 rows=json.loads((ROOT/'reportes/seleccion_piloto.json').read_text());results=[]
 for row in rows:
  results.append(process(row,args.piloto_local/str(row['carpeta_preparacion'])));savejson(ROOT/'reportes/piloto_resultados.json',results);print(json.dumps(results[-1],ensure_ascii=False),flush=True)
