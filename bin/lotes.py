#!/usr/bin/env python3
"""Un lote por ejecución, con progreso persistente después de cada ordenamiento."""
import argparse, datetime, fcntl, hashlib, json
from pathlib import Path
import biblioteca as b

ROOT=b.ROOT
DONE={'piloto_verificado','procesado'}
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def local_result(ident):
    folder=ROOT/'ordenamientos'/str(ident);pointer=folder/'actual.json'
    if not pointer.exists():return None
    c=json.loads(pointer.read_text());dest=folder/'versiones'/c['version']
    for name in ['metadata.json','validacion.json','texto.md']:
        if not (dest/name).is_file():return None
    meta=json.loads((dest/'metadata.json').read_text());v=json.loads((dest/'validacion.json').read_text())
    if not v.get('texto_conservado'):return None
    for kind,digest in meta['hash_sha256'].items():
        word_originals=[p for p in dest.glob('original.*') if p.suffix.lower() in {'.doc','.docx','.rtf'}]
        p=dest/'original.pdf' if kind=='pdf' else (word_originals[0] if len(word_originals)==1 else None)
        if p is None or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:return None
    return {'version':c['version'],'revision':c['validacion'],'markdown_sha256':hashlib.sha256((dest/'texto.md').read_bytes()).hexdigest()}

def initialize():
    target=ROOT/'reportes'/'avance_lotes.json'
    if target.exists():return json.loads(target.read_text())
    source=ROOT/'catalogo'/'leyes-estatales.json'
    rows=json.loads(source.read_text());rows=sorted(rows,key=lambda r:r['id'])
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('Identificadores duplicados')
    items=[];pending=0
    for row in rows:
        result=local_result(row['id'])
        if result:
            status='piloto_verificado' if row['id'] in {1,9,42,70} else 'procesado';batch=0
        else:
            batch=1+pending//10;pending+=1;status='pendiente'
        items.append({'id':row['id'],'nombre':row['ley'],'lote':batch,'estado':status,'detalle':result,'catalogo':row})
    state={'creado':now(),'actualizado':now(),'tamano_lote':10,'catalogo_origen':str(source.relative_to(ROOT)),
           'catalogo_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
           'nota':'Plan basado en inventario guardado; no implica nueva consulta al Congreso. Nuevos registros se agregarán después sin renumerar lotes.',
           'items':items,'ultimo_evento':'Preparado; esperando acceso de red para el lote 1.'}
    persist(state);return state

def persist(state):
    state['actualizado']=now();b.savejson(ROOT/'reportes'/'avance_lotes.json',state)
    items=state['items'];done=sum(x['estado'] in DONE for x in items)
    next_item=next((x for x in items if x['estado'] not in DONE),None)
    lines=['# Avance de la Biblioteca Legislativa de Sinaloa','',f"Actualizado: {state['actualizado']}",'',
           f"**Guardados y procesados: {done} de {len(items)}. Pendientes de procesar: {len(items)-done}.**",'',
           'Procesado significa que existen los originales, el Markdown y el control de conversión. La revisión adicional se indica por separado; no equivale a vigencia jurídica.','',
           f"Último evento: {state['ultimo_evento']}",'',
           f"Siguiente: lote {next_item['lote']:02d}, {next_item['nombre']} (ID {next_item['id']})." if next_item else 'Todos los lotes están procesados.','',
           'Lotes de hasta 10 leyes. Se guarda el avance después de cada ley. Si se interrumpe una ley, se reintenta; los resultados ya confirmados se conservan.','',
           'Para continuar en esta tarea, escribe: **Retoma la biblioteca desde AVANCE.md, un lote a la vez.**','',
           '| Lote | Procesadas | Estado |','|---|---:|---|']
    for batch in sorted({x['lote'] for x in items}):
        group=[x for x in items if x['lote']==batch];count=sum(x['estado'] in DONE for x in group)
        label='Piloto' if batch==0 else f'{batch:02d}'
        status='Procesado' if count==len(group) else 'Pendiente o interrumpido'
        lines.append(f'| {label} | {count}/{len(group)} | {status} |')
    lines+=['','## Detalle por ley','','| Lote | ID | Ordenamiento | Estado | Revisión / incidencia |','|---|---|---|---|---|']
    for x in items:
        detail=x.get('detalle') or {};rev=detail.get('revision') or detail.get('error') or '—'
        lines.append(f"| {x['lote']:02d} | {x['id']} | {x['nombre']} | {x['estado']} | {str(rev).replace('|','/').replace(chr(10),' ')} |")
    path=ROOT/'AVANCE.md';tmp=path.with_suffix('.md.tmp');tmp.write_text('\n'.join(lines)+'\n');tmp.replace(path)

def execute_one(state):
    # Recover a process that wrote its artifact before its progress checkpoint.
    for item in state['items']:
        if item['estado']=='en_curso':
            recovered=local_result(item['id'])
            item.update(estado='procesado' if recovered else 'pendiente',detalle=recovered)
    pending=[x for x in state['items'] if x['estado'] not in DONE]
    if not pending: persist(state);return
    batch=pending[0]['lote'];catalog=[x['catalogo'] for x in state['items']]
    for item in [x for x in pending if x['lote']==batch]:
        item.update(estado='en_curso',detalle=None);state['ultimo_evento']=f"Lote {batch:02d}: iniciando {item['nombre']} (ID {item['id']}).";persist(state)
        try:
            result=b.run({item['id']},catalog=catalog)
            if not result or result[0]['resultado']=='ERROR':raise RuntimeError(str(result))
            detail=local_result(item['id'])
            if not detail:raise RuntimeError('No se confirmó integridad de los archivos locales')
            item.update(estado='procesado',detalle=detail)
        except Exception as error:
            item.update(estado='error',detalle={'error':str(error)})
            state['ultimo_evento']=f"Lote {batch:02d} pausado en ID {item['id']}: {error}";persist(state)
            return
        state['ultimo_evento']=f"Lote {batch:02d}: guardado {item['nombre']} (ID {item['id']}).";persist(state)
    state['ultimo_evento']=f'Lote {batch:02d} procesado; detenido antes del siguiente lote.';persist(state)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--continuar',action='store_true');args=parser.parse_args()
    (ROOT/'reportes').mkdir(parents=True,exist_ok=True)
    with (ROOT/'.lotes.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        state=initialize()
        if args.continuar:execute_one(state)
        else:persist(state)
        print(state['ultimo_evento'])
