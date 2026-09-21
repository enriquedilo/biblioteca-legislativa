#!/usr/bin/env python3
"""Lotes federales reanudables: persistencia por documento y publicación por lote."""
import argparse,collections,fcntl,hashlib,json,os,subprocess,tempfile
from pathlib import Path
import piloto as p
import metadatos
b=p.base;F=p.FED;ROOT=p.ROOT
TERMINALES={'piloto_aprobado','procesado_con_incidencias','procesado','pendiente_original','pendiente_sin_texto','error_reportado'}
OK={'piloto_aprobado','procesado_con_incidencias','procesado'}
DIAGNOSTICO={'fuente':'Usuario; piloto aprobado en la conversación','descripcion':'pypdf fragmenta números con espacios; verificado por el usuario contra originales en 11 páginas señaladas del CFF y tres de CPEUM. Markdown generado con Poppler.','decision':'Control informativo, no bloquea lotes y no modifica textos. No se atribuye cotejo visual adicional a Codex.'}
def atomic_text(path,text):
 fd,tmp=tempfile.mkstemp(dir=path.parent,prefix=path.name+'.',suffix='.tmp')
 with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(text);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
def persist(s):
 s['actualizado']=b.now();items=s['items'];s['procesados']=sum(x['estado'] in OK for x in items);s['intentados']=sum(x['estado'] in TERMINALES for x in items);s['pendientes_reportados']=sum(x['estado'] in TERMINALES-OK for x in items)
 b.savejson(F/'reportes/avance_lotes.json',s)
 lines=['# Avance Federal','',f"Actualizado: {s['actualizado']}",'',f"Procesados: **{s['procesados']}/453**. Intentados: {s['intentados']}/453. Pendientes reportados: {s['pendientes_reportados']}.",'',s['ultimo_evento'],'','Piloto aprobado. Alcance confirmado: 316 principales y 137 reglamentos. Sin OCR, búsqueda ni articulado. Control pypdf informativo; diagnóstico del usuario en reportes/aprobacion_piloto.json. Originales y extracción conservados localmente; Git excluye binarios.','','| Lote | Intentados | Estado |','|---|---:|---|']
 for n in sorted({x['lote'] for x in items}):
  group=[x for x in items if x['lote']==n];done=sum(x['estado'] in TERMINALES for x in group);published=s.get('publicados',{}).get(str(n));label='Piloto' if n==0 else str(n)
  lines.append(f"| {label} | {done}/{len(group)} | {'Publicado' if published else 'Cerrado localmente' if done==len(group) else 'Pendiente'} |")
 lines+=['','| Lote | ID | Sigla | Estado | Detalle |','|---|---|---|---|---|']
 for x in items:lines.append(f"| {x['lote']} | {x['id']} | {x['sigla']} | {x['estado']} | {str((x.get('detalle') or {}).get('resultado') or (x.get('detalle') or {}).get('error') or '—').replace('|','/').replace(chr(10),' ')} |")
 atomic_text(F/'AVANCE.md','\n'.join(lines)+'\n')
 lines=['# Biblioteca Federal','','Cámara de Diputados: índices vigentes capturados individualmente. 453 identidades; la compilación no certifica vigencia jurídica.','','[Avance](AVANCE.md) · [Piloto](reportes/piloto.md)','','Sin índices de búsqueda ni articulado. URLs individuales y SHA-256 en metadata.json. Originales y extracción local excluidos de Git.','','| ID | Sigla | Ordenamiento | Texto / Estado |','|---|---|---|---|']
 for x in items:
  a=F/'ordenamientos'/str(x['id'])/'actual.json'
  text=x['estado']
  if a.exists():
   version=json.loads(a.read_text())['version'];text=f"[Markdown](ordenamientos/{x['id']}/versiones/{version}/texto.md) · {x['estado']}"
  lines.append(f"| {x['id']} | {x['sigla']} | {x['catalogo']['nombre_catalogo']} | {text} |")
 atomic_text(F/'INDICE.md','\n'.join(lines)+'\n')
def initialize():
 path=F/'reportes/avance_lotes.json';old=json.loads(path.read_text())
 if 'items' in old:return old
 rows=json.loads((F/'catalogo/catalogo.json').read_text());assert len(rows)==453
 pilots={r['id']:r for r in old['resultados']};items=[];pending=0
 for row in rows:
  # The tariff contained in LIGIE is marked as requested; no printed dates inferred.
  if row['sigla'].startswith('LIGIE'):row['vigencia_anual']=True
  pilot=row['id'] in pilots;batch=0 if pilot else 1+pending//10
  if not pilot:pending+=1
  items.append({'id':row['id'],'sigla':row['sigla'],'lote':batch,'estado':'piloto_aprobado' if pilot else 'pendiente','detalle':pilots.get(row['id']),'catalogo':row})
 b.savejson(F/'catalogo/catalogo.json',rows)
 b.savejson(F/'reportes/aprobacion_piloto.json',{'fecha_registro':b.now(),'aprobado_por':'Usuario en conversación','alcance_confirmado':453,'diagnostico_cifras':DIAGNOSTICO})
 s={'creado':b.now(),'fase':'lotes autorizados','tamano_lote':10,'catalogados':453,'catalogo_sha256':hashlib.sha256((F/'catalogo/catalogo.json').read_bytes()).hexdigest(),'items':items,'publicados':{'0':'62c86e6'},'ultimo_evento':'Piloto aprobado; iniciando lotes de diez.','control_pypdf':'informativo, no bloqueante'};persist(s);return s
class PendienteOriginal(Exception):pass
class PendienteTexto(Exception):pass
def prepare(row):
 cache=F/'preparacion'/str(row['id']);cache.mkdir(parents=True,exist_ok=True)
 for kind,suffix,url in [('pdf','pdf',row['url_pdf']),('word','doc',row['url_word'])]:
  if not url:continue
  dest=cache/('original.'+suffix)
  if not dest.exists():
   try:data=b.get(url)
   except Exception as e:
    if kind=='pdf':raise PendienteOriginal(str(e))
    continue
   if kind=='pdf' and not data.startswith(b'%PDF'):raise PendienteOriginal('Respuesta no es PDF: '+url)
   dest.write_bytes(data)
 pdf=cache/'original.pdf'
 if not pdf.exists():raise PendienteOriginal('Original PDF no disponible')
 raw=subprocess.check_output(['pdftotext','-layout',str(pdf),'-']).decode('utf-8')
 if not raw.strip():raise PendienteTexto('PDF sin capa de texto extraíble; sin OCR. Original conservado en preparación.')
def finalize(row,result):
 d=F/'ordenamientos'/str(row['id'])/'versiones'/result['version'];m=json.loads((d/'metadata.json').read_text());v=json.loads((d/'validacion.json').read_text())
 m.update(sigla=row['sigla'],vigencia_anual=row['vigencia_anual'],fuente=b.BASE,estatus='Incluido en índice federal vigente; vigencia jurídica no certificada',conversor='Poppler / controles conservadores existentes / adaptación federal')
 m['archivo_origen']=Path(row['url_pdf']).name
 if p.numeric_sigla(row['sigla']):
  m['slug']=p.slug_nombre(m['nombre_oficial']) if m['nombre_oficial'] else None
  if m['slug'] is None:v['metadatos_normativos']['incidencias'].append({'campo':'slug','motivo':'Sigla numérica y nombre oficial pendiente de cotejo; slug null, no se atribuye al catálogo el valor de nombre oficial.'})
  else:row['slug']=m['slug']
 metadatos.ajustar(m,v,(d/'extraccion.txt').read_text())
 from encabezados import encabezado,normalizar_millares
 normalization=[]
 for pn,page in enumerate((d/'extraccion.txt').read_text().split('\f'),1):
  for ln,line in enumerate(page.splitlines(),1):
   match=encabezado(' '.join(line.split()))
   if match and normalizar_millares(match[0])!=match[0]:normalization.append({'pagina_pdf':pn,'linea_extraccion':ln,'encabezado_literal':match[0],'encabezado_markdown':normalizar_millares(match[0]),'motivo':'Normalización de coma de millar autorizada por el usuario; original intacto.'})
 v['normalizacion_millares_encabezados']=normalization
 import re
 v['puntuacion_previa_encabezados']=[{'pagina_pdf':pn,'encabezado_literal':match[0],'criterio':'Puntuación impresa conservada, solo separación de encabezado; pendiente de cotejo de errata.'} for pn,page in enumerate((d/'extraccion.txt').read_text().split('\f'),1) for line in page.splitlines() if re.match(r'^[.;:,–—-]+\s+Art',line.strip(),re.I) and (match:=encabezado(' '.join(line.split())))]
 v['control_pypdf_informativo']=DIAGNOSTICO
 if row['sigla'].startswith('LIGIE'):v['metadatos_normativos']['incidencias'].append({'campo':'vigencia_anual','motivo':'Bandera administrativa solicitada por el usuario para la tarifa contenida en LIGIE; no se infiere vigencia jurídica anual del texto.'})
 for kind,sha in m['hash_sha256'].items():
  path=d/('original.pdf' if kind=='pdf' else 'original.'+v['formato_word_original']);assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
 assert v['texto_conservado'];assert all(x['inicios_lista_conservados'] for x in v['controles_por_pagina'])
 assert len(__import__('re').findall(r'<!-- PAGINA_PDF: \d+ -->',(d/'texto.md').read_text()))==v['paginas_pdf']
 b.savejson(d/'metadata.json',m);b.savejson(d/'validacion.json',v)
 return result
def process(row):
 a=F/'ordenamientos'/str(row['id'])/'actual.json'
 # Recover a completed conversion if interruption occurred before state persistence.
 if a.exists():
  d=a.parent/'versiones'/json.loads(a.read_text())['version'];v=json.loads((d/'validacion.json').read_text())
  result={'id':row['id'],'resultado':v['resultado'],'version':d.name,'paginas':v['paginas_pdf'],'paginas_sin_texto':v['paginas_sin_texto'],'incidencias_descarga':v['incidencias_descarga'],'recuperado_tras_interrupcion':True}
  return finalize(row,result)
 prepare(row);return finalize(row,b.process(row))
def execute_one(s):
 pending=[x for x in s['items'] if x['estado'] not in TERMINALES]
 if not pending:return None
 batch=pending[0]['lote'];report=F/'reportes'/f'lote-{batch:02d}.json';results=json.loads(report.read_text()) if report.exists() else []
 for item in [x for x in pending if x['lote']==batch]:
  item['estado']='en_curso';s['ultimo_evento']=f"Lote {batch}: iniciando {item['sigla']} (ID {item['id']}).";persist(s);print(s['ultimo_evento'],flush=True)
  try:
   result=process(item['catalogo']);status='pendiente_sin_texto' if result['paginas_sin_texto'] else 'procesado_con_incidencias'
  except PendienteOriginal as e:result={'id':item['id'],'error':str(e),'url_pdf':item['catalogo']['url_pdf']};status='pendiente_original'
  except PendienteTexto as e:result={'id':item['id'],'error':str(e),'url_pdf':item['catalogo']['url_pdf']};status='pendiente_sin_texto'
  except Exception as e:result={'id':item['id'],'error':str(e),'url_pdf':item['catalogo']['url_pdf']};status='error_reportado'
  result['sigla']=item['sigla'];item.update(estado=status,detalle=result);results=[r for r in results if r['id']!=item['id']]+[result];b.savejson(report,results);s['ultimo_evento']=f"Lote {batch}: {item['sigla']} registrado: {status}.";persist(s);print(s['ultimo_evento']+f" Páginas: {result.get('paginas','—')}",flush=True)
 s['ultimo_evento']=f'Lote {batch} cerrado localmente; pendiente de push.';persist(s);return batch
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,stderr=subprocess.STDOUT,text=True)
def publish(s,batch):
 # The ledger records publication intent in its commit; the local state confirms success afterwards.
 s['ultimo_evento']=f'Lote {batch} cerrado; publicación por commit del lote.';persist(s)
 git('add','Federal','bin/federal');git('commit','-m',f'Federal: cierra lote {batch:02d} de diez con avance e incidencias')
 print(git('pull','--rebase','origin','federal'),flush=True)
 print(git('fetch','origin','main'),flush=True)
 print(git('merge','--no-edit','origin/main'),flush=True)
 print(git('push','origin','federal'),flush=True)
 commit=git('rev-parse','HEAD').strip();s['publicados'][str(batch)]=commit;s['ultimo_evento']=f'Lote {batch} publicado en federal: {commit}.';persist(s)
 print(s['ultimo_evento'],flush=True)
def run(count,reanudar=False):
 with (F/'.lotes.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);s=initialize()
  if s.get('reanudar_requiere_instruccion_usuario'):
   if not reanudar:raise RuntimeError('Detenido en el corte por instrucción del usuario. Use --reanudar solo tras una nueva instrucción de continuación.')
   s['reanudar_requiere_instruccion_usuario']=False;s['fase']='lotes autorizados';persist(s)
  # Retry an interrupted publication before moving to another batch.
  closed=sorted({x['lote'] for x in s['items'] if x['lote'] and all(y['estado'] in TERMINALES for y in s['items'] if y['lote']==x['lote'])})
  for batch in closed:
   if str(batch) not in s['publicados']:
    status=git('status','--porcelain','--','Federal','bin/federal')
    if status.strip():publish(s,batch)
    else:
     print(git('pull','--rebase','origin','federal'),flush=True);print(git('fetch','origin','main'),flush=True);print(git('merge','--no-edit','origin/main'),flush=True);print(git('push','origin','federal'),flush=True);s['publicados'][str(batch)]=git('rev-parse','HEAD').strip();persist(s)
  for _ in range(count):
   batch=execute_one(s)
   if batch is None:break
   publish(s,batch)
  print(json.dumps({'procesados':s['procesados'],'intentados':s['intentados'],'pendientes':s['pendientes_reportados'],'lotes_publicados':len(s['publicados'])-1},ensure_ascii=False),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--lotes',type=int,default=1);ap.add_argument('--reanudar',action='store_true');a=ap.parse_args();run(a.lotes,a.reanudar)
