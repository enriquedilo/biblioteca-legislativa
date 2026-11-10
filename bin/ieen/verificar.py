#!/usr/bin/env python3
"""Verifica el lote IEEN guardado y sus índices, sin red ni cambios al acervo."""
import argparse,collections,hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'bin/ieen'));import convertir as c
sys.path.insert(0,str(ROOT/'bin'));import indices
catalog=json.loads((ROOT/'IEEN/catalogo/normatividad.json').read_text())['documentos']
parser=argparse.ArgumentParser();parser.add_argument('--lote',type=int,default=1);args=parser.parse_args()
rows=json.loads((ROOT/f'IEEN/reportes/lote-{args.lote}.json').read_text())
routes=json.loads((ROOT/'IEEN/indices/rutas.json').read_text())['ordenamientos']
for r in rows:
 i=r['id'];folder=ROOT/f'IEEN/ordenamientos/{i}';ptr=json.loads((folder/'actual.json').read_text());version=ptr['version'];p=folder/'versiones'/version
 assert (folder/'actual').resolve()==p.resolve()
 m=json.loads((p/'metadata.json').read_text());v=json.loads((p/'validacion.json').read_text())
 assert version==m['version']==m['hash_sha256']['pdf']==hashlib.sha256((p/'original.pdf').read_bytes()).hexdigest()
 row=next(x for x in catalog if x['seccion']=='normatividad' and x['numero']==i)
 assert m['reformas']==row['reformas'] and m['acuerdo']==row['vigente']['acuerdo'] and m['seccion']=='electoral'
 s=(p/'texto.md').read_text();parts=re.split(r'<!-- PAGINA_PDF: (\d+) -->\s*',s);raw=(p/'extraccion.txt').read_text().split('\f')[:-1]
 assert len(raw)==v['paginas_pdf']==len(parts[1::2])
 for n,(page,md) in enumerate(zip(raw,parts[2::2]),1):
  clean,_=c.conv.strip_pagination(page,n);assert c.compact(clean)==c.compact(c.conv.unformat(md));assert re.sub(r'\D','',clean)==re.sub(r'\D','',c.conv.unformat(md))
 idx=json.loads((ROOT/f'IEEN/indices/articulos/{i}.json').read_text());assert idx['version']==version
 assert idx['conteo']['cuerpo']==r['cuerpo'] and idx['conteo']['transitorios']==r['transitorios']
 expected=indices.articulos_de(s)
 assert [(a['articulo'],a['tipo'],a['linea_inicio'],a['linea_fin'],a['pagina_pdf']) for a in idx['articulos']]==[(a['articulo'],a['tipo'],a['linea_inicio'],a['linea_fin'],a['pagina_pdf']) for a in expected]
 for a in idx['articulos']:assert 1<=a['linea_inicio']<=a['linea_fin']<=len(s.split('\n')) and 1<=a['pagina_pdf']<=len(raw)
 route=next(x for x in routes if str(x['id'])==str(i))
 for k in ['texto','metadata','validacion','articulado']:
  assert '/actual/' not in route[k] and (ROOT/route[k]).exists()
 assert version in route['texto']
 assert not v['auditoria_encabezados']['rotulos_no_reconocidos']
 if 'rotulos_por_pagina' in v['auditoria_encabezados']:
  labels=v['auditoria_encabezados']['rotulos_por_pagina']
  assert collections.Counter((a['articulo'],a['pagina_pdf']) for a in labels)==collections.Counter((a['articulo'].lower().replace(' ',''),a['pagina_pdf']) for a in idx['articulos'] if a['tipo']=='cuerpo')
  for label in labels:assert label['texto'] in raw[label['pagina_pdf']-1]
 assert row['vigente']['fecha']==max(x['fecha'] for x in [row['vigente']]+row['reformas'])
print(f"{len(rows)} versiones y originales SHA-256; {sum(r['paginas'] for r in rows)} páginas conservadas; metadata de catálogo; rangos y rutas: OK")
