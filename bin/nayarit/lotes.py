#!/usr/bin/env python3
"""Un lote de hasta diez por ejecución; progreso persistente tras cada intento."""
import argparse,fcntl,hashlib,json
from pathlib import Path
import biblioteca as b
ROOT=b.ROOT
TERMINALES={'procesado','procesado_con_incidencias','piloto_revisado','pendiente_sin_texto','pendiente_original','error_reportado'}
def persist(state):
 state['actualizado']=b.now();b.savejson(ROOT/'reportes/avance_lotes.json',state)
 items=state['items'];done=sum(x['estado'] in {'procesado','procesado_con_incidencias','piloto_revisado'} for x in items)
 lines=['# Avance de la Biblioteca Legislativa de Nayarit','',f"Actualizado: {state['actualizado']}",'',f'**Procesados: {done} de {len(items)}.**','',state['ultimo_evento'],'','El piloto se reporta antes de iniciar los lotes. No se ha autorizado ni aplicado OCR. Los campos incompletos y discrepancias permanecen señalados.','','[Informe del piloto](reportes/REVISION_PILOTO.md) · [Índice](INDICE.md)','','| Lote | Procesados | Estado |','|---|---:|---|']
 for batch in sorted({x['lote'] for x in items}):
  group=[x for x in items if x['lote']==batch];n=sum(x['estado'] in TERMINALES for x in group)
  lines.append(f"| {'Piloto' if batch==0 else batch} | {n}/{len(group)} | {'Intentos cerrados; revisar incidencias' if n==len(group) else 'Pendiente'} |")
 lines+=['','## Detalle por ordenamiento','','| Lote | ID | Ordenamiento | Estado | Revisión / incidencia |','|---|---|---|---|---|']
 for x in items:
  detail=x.get('detalle') or {};v=detail.get('resultado') or detail.get('error') or '—'
  lines.append(f"| {x['lote']} | {x['id']} | {x['nombre']} | {x['estado']} | {str(v).replace('|','/')} |")
 (ROOT/'AVANCE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 index=['# Biblioteca Legislativa de Nayarit','',f'Catálogo local: {len(items)} identidades propias. Piloto: cuatro ordenamientos.','','Versiones descargadas del Congreso; no certifican vigencia jurídica. Los números son IDs locales estables, no números de decreto.','','[Avance](AVANCE.md) · [Informe del piloto](reportes/REVISION_PILOTO.md) · [Esquema](reportes/ESQUEMA.md)','','| ID | Ordenamiento | Texto | Original | Revisión |','|---|---|---|---|---|']
 for x in items:
  p=ROOT/'ordenamientos'/str(x['id'])/'actual.json'
  if p.exists():
   c=json.loads(p.read_text());rel=f"ordenamientos/{x['id']}/actual"
   word=next(iter((ROOT/rel).glob('original.doc*')),None);wordlink=f' · [Word]({rel}/{word.name})' if word else ' · Word pendiente'
   index.append(f"| {x['id']} | {x['nombre']} | [Markdown]({rel}/texto.md) | [PDF]({rel}/original.pdf){wordlink} | {c['validacion']} |")
  else:index.append(f"| {x['id']} | {x['nombre']} | — | — | Pendiente, lote {x['lote']} |")
 (ROOT/'INDICE.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
def initialize():
 p=ROOT/'reportes/avance_lotes.json'
 if p.exists():return json.loads(p.read_text())
 src=ROOT/'catalogo/leyes-estatales.json';rows=json.loads(src.read_text());pilots={r['id'] for r in json.loads((ROOT/'reportes/seleccion_piloto.json').read_text())};results={r['id']:r for r in json.loads((ROOT/'reportes/piloto_resultados.json').read_text())};items=[];pending=0
 for r in rows:
  pilot=r['id'] in pilots;batch=0 if pilot else 1+pending//10
  if not pilot:pending+=1
  items.append({'id':r['id'],'nombre':r['ley'],'lote':batch,'estado':'piloto_revisado' if pilot else 'pendiente','detalle':results.get(r['id']),'catalogo':r})
 state={'creado':b.now(),'actualizado':b.now(),'tamano_lote':10,'catalogo_origen':'catalogo/leyes-estatales.json','catalogo_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'nota':'IDs propios persistidos; URLs no identifican ordenamientos. El catálogo queda congelado durante estos lotes.','items':items,'ultimo_evento':'Piloto de cuatro documentos cerrado con incidencias documentadas. Detenido antes del lote 1.'};persist(state);return state

def execute_one(state):
 if not (ROOT/'reportes/PILOTO_REPORTADO.json').exists():raise RuntimeError('Primero debe reportarse el piloto al usuario; no se inicia lote.')
 pending=[x for x in state['items'] if x['estado'] not in TERMINALES]
 if not pending:return
 batch=pending[0]['lote'];report=ROOT/'reportes'/f'lote-{batch:02d}.json';results=json.loads(report.read_text()) if report.exists() else []
 for item in [x for x in pending if x['lote']==batch]:
  item['estado']='en_curso';state['ultimo_evento']=f"Lote {batch}: iniciando ID {item['id']}";persist(state);print(state['ultimo_evento'],flush=True)
  try:
   result=b.process(item['catalogo']);print(f"ID {item['id']}: {result['paginas']} páginas; {len(result['paginas_sin_texto'])} sin texto; {len(result.get('paginas_cifras_discrepantes',[]))} con discrepancia de cifras",flush=True);status='pendiente_sin_texto' if result['paginas_sin_texto'] else 'procesado_con_incidencias'
  except Exception as e:result={'id':item['id'],'error':str(e)};status='pendiente_original' if not item['catalogo']['url_pdf'] else 'error_reportado'
  item.update(estado=status,detalle=result);results=[x for x in results if x['id']!=result['id']];results.append(result);b.savejson(ROOT/'reportes'/f'lote-{batch:02d}.json',results);state['ultimo_evento']=f"Lote {batch}: ID {item['id']} registrado. Incidencias no reparadas.";persist(state)
 state['ultimo_evento']=f'Lote {batch} cerrado; siguiente lote solo tras este cierre; avisar al usuario cada tres lotes.';persist(state)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--continuar',action='store_true');args=p.parse_args()
 with (ROOT/'.lotes.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);state=initialize()
  if args.continuar:execute_one(state)
  else:persist(state)
  print(state['ultimo_evento'])
