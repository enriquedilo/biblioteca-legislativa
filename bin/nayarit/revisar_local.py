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
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from encabezados import CANDIDATO, EXPLICITO, encabezado, normalizar_millares

ROOT = Path(__file__).resolve().parents[2] / 'Nayarit'
ART = CANDIDATO
TRANS = re.compile(r'^(?:ART[ÍI]CULOS?\s+)?TRANSITORIOS?(?:\s+DE\s+LAS\s+REFORMAS)?\s*:?$', re.I)
ORD = re.compile(r'^(?:(?:ART[ÍI]CULO|Artículo|Articulo)\s+)?(?:PRIMERO|SEGUNDO|TERCERO|CUARTO|QUINTO|SEXTO|SÉPTIMO|SEPTIMO|OCTAVO|NOVENO|DÉCIMO|DECIMO|ÚNICO|UNICO|Primero|Segundo|Tercero|Cuarto|Quinto|Sexto|Único)(?:[.\s-]|$)')
LIST = re.compile(r'^(?:[IVXLCDM]+|[A-Za-z]|\d+)[.)]\s+')
ROMAN = re.compile(r'M{0,3}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})')

def compact(s):
    return re.sub(r'\s+', '', normalizar_millares(s))

def strip_pagination(page, number):
    lines=page.splitlines(); removed=[]
    nonempty=[i for i,l in enumerate(lines) if l.strip()]
    for i in set(nonempty[:1]+nonempty[-1:]):
        if lines[i].strip()==str(number):
            removed.append({'linea':i+1,'texto':lines[i].strip()});lines[i]=''
    return '\n'.join(lines),removed

EXPLICIT_ART = EXPLICITO

def heading_decision(lines,index):
    line=re.sub(r'[ \t]+',' ',lines[index].strip());candidate=ART.match(line)
    if not candidate:return None,None
    explicit=encabezado(line)
    if explicit:return explicit,None
    previous=lines[index-1].strip() if index else ''
    following=lines[index+1].strip() if index+1<len(lines) else ''
    reasons=[]
    if previous and not previous.endswith('.'):reasons.append('renglón anterior sin punto final')
    if following and following[0].islower():reasons.append('renglón siguiente empieza en minúscula')
    # A bare reference is never promoted solely because wrapping put it at line start.
    if not reasons:reasons.append('sin delimitador impreso de inicio de artículo; se conserva en cuerpo')
    return None,{'linea':index+1,'texto':line,'anterior':previous,'siguiente':following,'motivo':'; '.join(reasons)}

def to_markdown(page, incidencias=None):
    out=[]; paragraph=[];lines=page.splitlines()
    def flush():
        if paragraph:
            line=re.sub(r'^(\d+)\.',r'\1\\.',' '.join(paragraph))
            out.append(line);paragraph.clear()
    for index,raw in enumerate(lines):
        line=re.sub(r'[ \t]+',' ',raw.strip())
        if not line:flush();continue
        article,blocked=heading_decision(lines,index)
        if blocked and incidencias is not None:incidencias.append(blocked)
        section=TRANS.match(line) or re.match(r'^(?:T[ÍI]TULO|CAP[ÍI]TULO|SECCI[ÓO]N|LIBRO)\b',line)
        if article:
            flush();out.append('### '+normalizar_millares(article[0].strip()))
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
