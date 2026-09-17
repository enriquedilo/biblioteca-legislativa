#!/usr/bin/env python3
"""Biblioteca local: originales inmutables y conversiones auditables."""
import argparse, datetime, hashlib, io, json, re, subprocess, tempfile, urllib.request, zipfile, os
from pathlib import Path
from xml.etree import ElementTree as ET
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent / 'Sinaloa'
BASE = 'https://gaceta.congresosinaloa.gob.mx'
def get(url, payload=None):
    command=['/usr/bin/curl','-L','--fail','--silent','--show-error','--max-time','60','--retry','2',url]
    if payload is not None: command += ['-H','Content-Type: application/json','--data',json.dumps(payload)]
    return subprocess.check_output(command)
def savejson(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd,tmp=tempfile.mkstemp(dir=path.parent, prefix=path.name+'.',suffix='.tmp')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(value,f,ensure_ascii=False,indent=2); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
def norm(s):
    return re.sub(r'\s+', '', s).casefold()
def extract_word(data, ext):
    if ext == 'docx':
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            root = ET.fromstring(z.read('word/document.xml'))
        ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        return '\n\n'.join(''.join(t.text or '' for t in p.findall('.//w:t', ns)) for p in root.findall('.//w:p', ns))
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)/'original.doc'; p.write_bytes(data)
        return subprocess.check_output(['/usr/bin/textutil','-convert','txt','-stdout',str(p)]).decode('utf-8')
def markers(text):
    found=re.findall(r'(?m)^\s*(?:Artículo|ARTÍCULO|ARTICULO|Articulo|Art\.|ART\.)\s+(\d+(?:[oº°.]?\s*(?i:bis|ter|qu[áa]ter)(?:\s+[A-Z]\b)?)?)', text)
    return [re.sub(r'\s+',' ',x.replace('.','').replace('º','').replace('°','')).strip().casefold() for x in found]
def convert(text):
    lines=[]
    for block in re.split(r'\n\s*\n',text.strip()):
        block=re.sub(r'[ \t]+',' ', block.strip())
        block=re.sub(r'\n(?!\s*(?:[IVX]+\.|[a-z]\)|\d+\.))',' ',block)
        if re.match(r'(?i)^(art[íi]culo\s+\d+|transitorios?\s*$|t[íi]tulo\s|cap[íi]tulo\s)',block):
            # Only isolate the article label; keep substantive wording untouched.
            m=re.match(r'(?i)^(art[íi]culo\s+\d+(?:\s*(?:bis|ter))?\s*[.º°-]?)\s*(.*)',block)
            block=('### '+m[1]+'\n\n'+m[2]) if m else '## '+block
        lines.append(block)
    return '\n\n'.join(lines)+'\n'
def run(ids, catalog=None):
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    fresh=catalog is None
    if fresh: catalog=json.loads(get(BASE+'/api/obtenerLeyes',{'id_tipoley':1}))
    if not isinstance(catalog,list) or not catalog: raise ValueError('Catálogo vacío o inesperado; no se modifica la biblioteca')
    if fresh: savejson(ROOT/'catalogo'/('catalogo-'+now[:10]+'.json'),catalog)
    results=[]
    for row in catalog:
        if ids and row['id'] not in ids: continue
        try:
            files={}; urls={}
            for kind,available,filename in [('pdf',row.get('pdf'),f"Ley_{row['id']}.pdf"),('word',row.get('word'),f"Leyword_{row['id']}.{row.get('nb_extword','docx')}")]:
                if available:
                    urls[kind]=BASE+':3001/pdfs/leyes/'+filename
                    files[kind]=get(urls[kind])
            if 'pdf' not in files or not files['pdf'].startswith(b'%PDF'): raise ValueError('PDF ausente o inválido')
            hashes={k:hashlib.sha256(v).hexdigest() for k,v in files.items()}
            version=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
            folder=ROOT/'ordenamientos'/str(row['id']); dest=folder/'versiones'/version
            current=folder/'actual.json'
            if current.exists() and json.loads(current.read_text())['version']==version and json.loads(current.read_text()).get('conversor',0)>=2:
                results.append({'id':row['id'],'resultado':'sin cambios'}); continue
            dest.mkdir(parents=True,exist_ok=True)
            for kind,data in files.items():
                ext='pdf' if kind=='pdf' else row['nb_extword']
                (dest/('original.'+ext)).write_bytes(data)
            reader=PdfReader(io.BytesIO(files['pdf']))
            pages=subprocess.check_output(['pdftotext','-layout',str(dest/'original.pdf'),'-']).decode('utf-8').split('\f')
            if not pages[-1].strip(): pages.pop()
            if len(pages)!=len(reader.pages): raise ValueError('Número de páginas no coincide')
            pdftext='\n\n'.join(pages)
            wordtext=extract_word(files['word'],row['nb_extword']) if 'word' in files else ''
            # PDF preserves printed list numbering that basic Word readers can lose.
            text=pdftext
            if len(text)<200: raise ValueError('Texto insuficiente; requiere OCR/revisión')
            (dest/'extraccion.txt').write_text(text,encoding='utf-8')
            from revisar_local import to_markdown, strip_pagination, unformat, compact
            converted=[]; preserved=True
            for page_number,page in enumerate(pages,1):
                page_clean,_=strip_pagination(page,page_number)
                page_md=to_markdown(page_clean)
                preserved=preserved and compact(page_clean)==compact(unformat(page_md))
                converted.append(f'<!-- PAGINA_PDF: {page_number} -->\n\n'+page_md)
            md='\n'.join(converted)
            a,b=markers(wordtext),markers(pdftext)
            missing=sorted(set(b)-set(a)); extra=sorted(set(a)-set(b))
            validation={'texto_conservado':preserved,'paginas_pdf':len(pages),'paginas_sin_texto':[i+1 for i,p in enumerate(pages) if len(p.strip())<20], 'articulos_word':a,'articulos_pdf':b,'solo_pdf':missing,'solo_word':extra,'transitorios_word':len(re.findall(r'(?i)transitorios?',wordtext)), 'transitorios_pdf':len(re.findall(r'(?i)transitorios?',pdftext)), 'alcance':'Control mecánico; requiere cotejo visual y no certifica vigencia jurídica.'}
            status='pendiente de cotejo visual' if preserved and not missing and not extra else 'requiere revisión'
            evidence=[line.strip() for line in text[:12000].splitlines() if re.search(r'(?i)(última reforma|últimas reformas|texto vigente|publicado en)',line)]
            reform=re.search(r'(?i)última reforma[^\n]*(?:\n[^\n]+)?',text[:2000])
            meta={'id':row['id'],'nombre_catalogo':row['ley'],'nombre_oficial':None,'nombre_oficial_pendiente_de_cotejo':True,'fuente':BASE+'/#/leyes','urls':urls,'fecha_descarga':now,'fecha_catalogo_sin_interpretar':row.get('fecha'),'ultima_reforma':reform[0].strip() if reform else None,'evidencia_encabezado':evidence,'hash_sha256':hashes,'version':version,'origen_markdown':'PDF; conserva numeración impresa, notas y páginas','estatus':'Incluido en catálogo de Leyes Estatales; vigencia jurídica no verificada','validacion':status}
            (dest/'texto.md').write_text('# '+row['ley']+'\n\n> Transcripción del original del Congreso. Consulta metadata.json y validacion.json.\n\n'+md,encoding='utf-8')
            savejson(dest/'metadata.json',meta); savejson(dest/'validacion.json',validation)
            if not preserved: raise ValueError('La conversión alteró texto; versión no promovida')
            savejson(current,{'version':version,'nombre':row['ley'],'validacion':status,'conversor':2})
            results.append({'id':row['id'],'resultado':status,'paginas':len(pages),'articulos_word':len(a),'articulos_pdf':len(b),'solo_pdf':missing,'solo_word':extra})
        except Exception as e:
            results.append({'id':row['id'],'resultado':'ERROR','detalle':str(e)})
        print(json.dumps(results[-1],ensure_ascii=False),flush=True)
    savejson(ROOT/'reportes'/('revision-'+now.replace(':','-')+'.json'),results)
    index=['# Biblioteca Legislativa de Sinaloa','',f'Última ejecución: {now}','',f'Catálogo consultado: {len(catalog)} ordenamientos. Categoría: Leyes Estatales. No incluye Leyes de Ingreso.','','Las fechas del catálogo no se interpretan automáticamente como últimas reformas. Las versiones son copias descargadas; la vigencia requiere cotejo.','','| Ordenamiento | Texto | Original | Revisión |','|---|---|---|---|']
    for p in sorted((ROOT/'ordenamientos').glob('*/actual.json')):
        c=json.loads(p.read_text()); rel=f"ordenamientos/{p.parent.name}/versiones/{c['version']}"
        index.append(f"| {c['nombre']} | [Markdown]({rel}/texto.md) | [PDF]({rel}/original.pdf) | {c['validacion']} |")
    (ROOT/'INDICE.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
    return results
if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--todos',action='store_true'); args=parser.parse_args()
    if args.todos and not (ROOT/'reportes'/'PILOTO_VALIDADO.json').exists():
        parser.error('Primero debe cerrarse el cotejo del piloto y registrarse PILOTO_VALIDADO.json; consulte LEEME.md.')
    run(None if args.todos else {1,9,42,70})
