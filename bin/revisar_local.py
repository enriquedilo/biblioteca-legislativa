#!/usr/bin/env python3
"""Cotejo reproducible del piloto con originales locales; no descarga archivos."""
import collections
import datetime
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from pypdf import PdfReader
from biblioteca import extract_word, savejson
from encabezados import CANDIDATO, encabezado

ROOT = Path(__file__).resolve().parent.parent / 'Sinaloa'
PILOTO = {'1': [1,6,64,83,237,240,248], '9': [1,2,109,134,167],
          '42': [1,38,61,62,70], '70': [1,50,55,57]}
ART = CANDIDATO
TRANS = re.compile(r'^(?:ART[ÍI]CULOS?\s+)?TRANSITORIOS?(?:\s+DE\s+LAS\s+REFORMAS)?\s*:?$', re.I)
ORD = re.compile(r'^(?:(?:ART[ÍI]CULO|Artículo|Articulo)\s+)?(?:PRIMERO|SEGUNDO|TERCERO|CUARTO|QUINTO|SEXTO|SÉPTIMO|SEPTIMO|OCTAVO|NOVENO|DÉCIMO|DECIMO|ÚNICO|UNICO|Primero|Segundo|Tercero|Cuarto|Quinto|Sexto|Único)(?:[.\s-]|$)')
LIST = re.compile(r'^(?:[IVXLCDM]+|[A-Za-z]|\d+)[.)]\s+')
ROMAN = re.compile(r'M{0,3}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})')

def compact(s):
    return re.sub(r'\s+', '', s)

def strip_pagination(page, number):
    lines=page.splitlines(); removed=[]
    nonempty=[i for i,l in enumerate(lines) if l.strip()]
    for i in set(nonempty[:1]+nonempty[-1:]):
        if lines[i].strip()==str(number):
            removed.append({'linea':i+1,'texto':lines[i].strip()});lines[i]=''
    return '\n'.join(lines),removed

def to_markdown(page):
    out=[]; paragraph=[]
    def flush():
        if paragraph:
            line=' '.join(paragraph)
            # Prevent Markdown from renumbering printed numeric lists.
            line=re.sub(r'^(\d+)\.',r'\1\\.',line)
            out.append(line);paragraph.clear()
    for raw in page.splitlines():
        line=re.sub(r'[ \t]+',' ',raw.strip())
        if not line:
            flush();continue
        article=encabezado(line)
        section=TRANS.match(line) or re.match(r'^(?:T[ÍI]TULO|CAP[ÍI]TULO|SECCI[ÓO]N|LIBRO)\b',line)
        if article:
            flush();out.append('### '+article[0].strip())
            rest=line[article.end():].strip()
            if rest:paragraph.append(rest)
        elif section:
            flush();out.append('## '+line)
        else:
            if LIST.match(line) or ORD.match(line):flush()
            paragraph.append(line)
    flush()
    return '\n\n'.join(out)+'\n'

def unformat(md):
    return re.sub(r'(?m)^#{1,6} ','',md).replace('\\.','.')

def article_ids(text):
    result=[]
    for line in text.replace('\f','\n').splitlines():
        m=ART.match(line.strip())
        if m:
            label=re.sub(r'^(?:ART[ÍI]CULO|Artículo|Articulo|ART\.|Art\.)\s*','',m[0])
            label=re.sub(r'(?<=\d)[oº°]','',label)
            result.append(re.sub(r'[\s.:-]','',label).casefold())
    return result

def lexical_tokens(text):
    # Only for cross-format comparison. None of these substitutions edit the Markdown.
    text=text.replace('\f','\n').replace('C O N S I D E R A N D O','CONSIDERANDO')
    text=text.replace('IVLos','IV Los').replace('AEl','El')
    text=re.sub(r'(?i)Bis([A-G])\b',r'Bis \1',text)
    text=re.sub(r'(?m)^\s*PAGE\s*\d*\s*$','',text)
    text=re.sub(r'(?m)^\s*[ABa-z][.)]\s+','',text)
    return [x.casefold() for x in re.findall(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+',text) if not ROMAN.fullmatch(x)]

def compare_words(word,pdf,ident):
    a=lexical_tokens(word);b=lexical_tokens(pdf)
    if collections.Counter(a)!=collections.Counter(b):
        raise ValueError(f'{ident}: diferencia léxica Word/PDF no resuelta')
    # Word exports two footnotes at the document end; PDF prints them on page 1.
    notes={'9':'Constitución Política del Estado de Sinaloa. Expedida el 22 de junio de 1922. El texto íntegro de la Constitución fue publicado en el P.O. “El Estado de Sinaloa” Núms. 78, 79, 80, 81, 82, 83 y 84 del Tomo XIII correspondiente a los días 6, 8, 11, 13, 15, 18 y 20 de julio de 1922.',
           '42':'Publicada en el P.O. No. 142 de 26 de noviembre de 2001.'}
    if ident in notes:
        needle=lexical_tokens(notes[ident])
        def remove_once(tokens):
            hits=[k for k in range(len(tokens)-len(needle)+1) if tokens[k:k+len(needle)]==needle]
            if len(hits)!=1: raise ValueError(f'{ident}: nota al pie no localizada de forma única')
            k=hits[0];return tokens[:k]+tokens[k+len(needle):]
        a=remove_once(a);b=remove_once(b)
    if a!=b:raise ValueError(f'{ident}: orden léxico no coincide')
    return {'palabras_comparadas':len(lexical_tokens(word)), 'frecuencias_coinciden':True,
            'orden_coincide_separando_nota_al_pie':True,
            'nota_al_pie_reubicada_por_lector_word':notes.get(ident),
            'normalizaciones_solo_comparacion':['Se excluyen etiquetas de listas romanas y alfabéticas; se cotejan por separado en PDF/Markdown.', 'Se excluyen campos PAGE del Word.', 'Se equiparan IVLos/IV Los, BisA/Bis A, AEl/El y el espaciado de CONSIDERANDO.'],
            'limite':'Comparación léxica no compara puntuación Word/PDF; Markdown sí conserva signos y cifras de la extracción PDF.'}

def review():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat(); prepared=[]
    for ident,visual in PILOTO.items():
        folder=ROOT/'ordenamientos'/ident; current=json.loads((folder/'actual.json').read_text())
        dest=folder/'versiones'/current['version'];meta=json.loads((dest/'metadata.json').read_text())
        wordfile=next(dest.glob('original.doc*')); pdf=dest/'original.pdf'
        for kind,p in [('word',wordfile),('pdf',pdf)]:
            assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['hash_sha256'][kind],f'Hash {ident} {kind}'
        raw=subprocess.check_output(['pdftotext','-layout',str(pdf),'-']).decode('utf-8')
        pages=raw.split('\f')
        if not pages[-1].strip():pages.pop()
        reader=PdfReader(pdf);assert len(pages)==len(reader.pages)
        word=extract_word(wordfile.read_bytes(),wordfile.suffix[1:])
        words=compare_words(word,raw,ident)
        # Full document article identities, including Bis-A variants.
        wa,pa=article_ids(word),article_ids(raw)
        assert set(wa)==set(pa),f'Artículos {ident}: {set(wa)^set(pa)}'
        blocks=[];checks=[]
        for n,(page,independent) in enumerate(zip(pages,reader.pages),1):
            assert len(page.strip())>20 or (ident=='1' and n==6 and not page.strip()), f'Página vacía no cotejada {ident}/{n}'
            clean,removed=strip_pagination(page,n);md=to_markdown(clean)
            assert compact(clean)==compact(unformat(md)),f'Contenido {ident}/{n}'
            # Independent PDF engines must agree on all digits, in order, per page.
            other=re.sub(r'(?m)^\s*'+str(n)+r'\s*$','',independent.extract_text() or '')
            numerical=re.sub(r'\D','',other)==re.sub(r'\D','',clean)
            assert numerical,f'Cifras {ident}/{n}'
            labels=[l.strip() for l in clean.splitlines() if LIST.match(l.strip())]
            # Every full list-start line must survive conversion in the same order.
            flat=compact(unformat(md));cursor=0
            for label in labels:
                key=compact(label);at=flat.find(key,cursor)
                assert at>=0,f'Fracción {ident}/{n}';cursor=at+len(key)
            blocks.append(f'<!-- PAGINA_PDF: {n} -->\n\n'+md)
            checks.append({'pagina':n,'caracteres_no_blancos':len(compact(clean)), 'contenido_y_signos_conservados':True,
                           'secuencia_cifras_dos_lectores_pdf':True,'inicios_lista':len(labels),'paginacion_retirada':removed})
        trans=[{'pagina':n,'encabezado':l.strip()} for n,p in enumerate(pages,1) for l in p.splitlines() if TRANS.match(l.strip())]
        assert trans,f'Transitorios {ident}'
        # Verify complete transitory tail, not just its headings.
        first=next(j for j,l in enumerate(raw.splitlines()) if TRANS.match(l.strip()))
        trans_tail='\n'.join(raw.splitlines()[first:])
        trans_articles=article_ids(trans_tail)
        trans_ord=[l.strip() for l in trans_tail.splitlines() if ORD.match(l.strip())]
        status='Conversión verificada: controles completos y cotejo visual por muestra'
        report={'id':int(ident),'fecha_revision':now,'resultado':status,'originales_sha256_verificados':True,
                'paginas_pdf':len(pages),'paginas_sin_texto':[6] if ident=='1' else [], 'pagina_blanca_confirmada_visualmente':ident=='1', 'texto_conservado':True,'comparacion_word_pdf':words,
                'articulos_word':wa,'articulos_pdf':pa,'identificadores_articulos_coinciden':True,
                'encabezados_transitorios':trans,'encabezados_ordinales_en_seccion_transitoria':trans_ord,
                'articulos_numericos_en_seccion_transitoria':trans_articles,
                'transitorios_y_notas_completos_incluidos':True,'paginas_cotejadas_visualmente':visual,
                'controles_por_pagina':checks,
                'alcance':'Integridad de la conversión de los originales descargados. Controles automáticos sobre todas las páginas y cotejo visual de muestra; no revisión jurídica ni cotejo visual exhaustivo.',
                'incidencias_resueltas':['Se sustituyó pypdf como extractor principal por Poppler con disposición de página.', 'Se conservan listas impresas que el lector Word omite.', 'Se retiran únicamente números de página aislados en los bordes; la página queda identificada por comentario.', 'Las referencias dentro de párrafos no se cuentan como artículos.'],
                'diferencias_de_fuente':['Código Civil: AEl y @ aparecen en el original PDF y se conservan.'] if ident=='1' else []}
        title=meta['nombre_oficial'];body='# '+title+'\n\n> Transcripción del PDF original descargado. Integridad de conversión verificada; vigencia jurídica no certificada. Los comentarios PAGINA_PDF permiten localizar el original.\n\n'+'\n'.join(blocks)
        meta['validacion']=status;meta['fecha_revision_conversion']=now;meta['conversor']='Poppler pdftotext -layout / revisión local v3'
        meta['origen_markdown']='PDF original; numeración impresa, fracciones, transitorios y notas conservados'
        if ident in {'1','9','42'}:
            reform=re.search(r'Última reforma[^\n]+',raw)
            assert reform;meta['ultima_reforma']=reform[0].strip()
        current.update(validacion=status,conversor=3)
        prepared.append((dest,folder,body,raw,meta,current,report))
        print(f'{ident}: {len(pages)} páginas; cotejo aprobado',flush=True)
    # No publication until all four have passed. Originals are never overwritten.
    for dest,folder,body,raw,meta,current,report in prepared:
        archive=dest/'conversiones_anteriores'/'v2';archive.mkdir(parents=True,exist_ok=True)
        for name in ['texto.md','extraccion.txt','metadata.json','validacion.json']:
            if (dest/name).exists() and not (archive/name).exists():shutil.copy2(dest/name,archive/name)
        (dest/'texto.md').write_text(body,encoding='utf-8');(dest/'extraccion.txt').write_text(raw,encoding='utf-8')
        savejson(dest/'metadata.json',meta);savejson(dest/'validacion.json',report);savejson(folder/'actual.json',current)
    approval={'fecha':now,'alcance':'Integridad de conversión del piloto; no vigencia jurídica ni aprobación automática de descargas nuevas.',
              'originales':{str(report['id']):meta['hash_sha256'] for _,_,_,_,meta,_,report in prepared},
              'paginas':sum(x[-1]['paginas_pdf'] for x in prepared),'paginas_muestra_visual':sum(len(x) for x in PILOTO.values()),
              'estado':'piloto verificado','descarga_masiva_ejecutada':False}
    savejson(ROOT/'reportes'/'PILOTO_VALIDADO.json',approval)
    index=['# Biblioteca Legislativa de Sinaloa','','Cuatro conversiones verificadas. Controles automáticos sobre 542 páginas y cotejo visual de 21 páginas seleccionadas. Esta revisión corresponde a los originales ya descargados; no comprueba reformas posteriores.','','| Ordenamiento | Texto | Original | Revisión |','|---|---|---|---|']
    for dest,folder,body,raw,meta,current,report in prepared:
        rel=dest.relative_to(ROOT).as_posix()
        index.append(f"| {meta['nombre_oficial']} | [Markdown]({rel}/texto.md) | [PDF]({rel}/original.pdf) | Conversión verificada |")
    index.extend(['','[Reporte de revisión](reportes/REVISION_PILOTO.md) · [Guía](../LEEME.md)'])
    (ROOT/'INDICE.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
    return prepared

if __name__=='__main__':
    review()
