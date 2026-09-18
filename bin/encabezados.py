"""Reconocimiento de rótulos impresos; no normaliza el texto del encabezado."""
import re
SUFIJO=r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+'
NUMERO=r'\d+(?:ro|do|to|o|º|°)?'
ROTULO=r'(?:ART[ÍI]CULOS?|ART\.)\s*'+NUMERO+r'(?:\s*'+SUFIJO+r'(?:[ -]*(?:\d+|[A-Z])(?=[.\s:-]|$))?|\s+[A-Z](?=[.\s:-]|$))?'
CANDIDATO=re.compile(r'^'+ROTULO+r'(?:\.-|[.:-])?',re.I)
RANGO=re.compile(r'^(?:ART[ÍI]CULOS)\s+(\d+)\s+al\s+(\d+)\s*(?:\.-|[.-])',re.I)
EXPLICITO=re.compile(r'^'+ROTULO+r'\s*(?:\.-|[.:-])',re.I)
def encabezado(line):
    m=RANGO.match(line) or EXPLICITO.match(line)
    if not m:return None
    # Wrapped references in lowercase are not new article headings.
    if not line[0].isupper():return None
    tail=line[m.end():].lstrip()
    if re.match(r'^ART[ÍI]CULOS\b',line,re.I) and re.match(r'^(?:[,;]|\d|[yYeE]\s+\d)',tail):return None
    return m
