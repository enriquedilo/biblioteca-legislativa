import sys,json,re,subprocess,hashlib,shutil
from pathlib import Path
sys.path.insert(0,'bin/nayarit');from revisar_local import strip_pagination,unformat
from pypdf import PdfReader
root=Path('Nayarit/ordenamientos/5/actual');v=json.loads((root/'validacion.json').read_text());m=json.loads((root/'metadata.json').read_text());t=(root/'texto.md').read_text()
parts=re.split(r'<!-- PAGINA_PDF: (\d+) -->',t);reader=PdfReader(root/'original.pdf');assert len(reader.pages)==188
for n,md in zip(parts[1::2],parts[2::2]):
 raw,_=strip_pagination((root/'extraccion.txt').read_text().split('\f')[int(n)-1],int(n));assert re.sub(r'\s','',raw)==re.sub(r'\s','',unformat(md)),n
assert all(x['contenido_y_signos_conservados'] and x['inicios_lista_conservados'] and x['secuencia_cifras_dos_lectores_pdf'] for x in v['controles_por_pagina'])
for typ,ext in [('pdf','pdf'),('word','doc')]:assert hashlib.sha256((root/('original.'+ext)).read_bytes()).hexdigest()==m['hash_sha256'][typ]
i=json.load(open('Nayarit/indices/articulos/5.json'));assert i['version']==m['version'];lines=t.split('\n')
for a in i['articulos']:
 assert 1<=a['linea_inicio']<=a['linea_fin']<=len(lines)
 marks=re.findall(r'<!-- PAGINA_PDF: (\d+) -->','\n'.join(lines[:a['linea_inicio']]))
 assert int(marks[-1])==a['pagina_pdf']
r=json.load(open('Nayarit/indices/rutas.json'));entry=next(x for x in r['ordenamientos'] if x['id']==5)
for k in ['texto','metadata','validacion','articulado']:assert '/actual/' not in entry[k] and Path(entry[k]).exists()
print('Conservación de 188 páginas, hashes, cifras, rangos y rutas: OK')
