"""Reconocimiento de rótulos impresos; no normaliza el texto del encabezado."""
import re
SUFIJO=r'(?:bis|ter|qu[áa]ter|quinquies|sexies|sexties|septies|octies|nonies|decies|quintus|sextus|septimus|octavus|nonus|decimus)'
NUMERO=r'\d+(?:ro|do|to|o|º|°)?'
ROTULO=r'(?:ART[ÍI]CULOS?|ART\.)\s*'+NUMERO+r'(?:\s*'+SUFIJO+r'(?:[ -]*(?:\d+|[A-Z])(?=[.\s:-]|$))?|\s+[A-Z](?=[.\s:-]|$))?'
CANDIDATO=re.compile(r'^'+ROTULO+r'(?:\.-|[.:-])?',re.I)
EXPLICITO=re.compile(r'^'+ROTULO+r'\s*(?:\.-|[.:-])',re.I)
def encabezado(line):
    m=EXPLICITO.match(line)
    if not m:return None
    # Wrapped references in lowercase are not new article headings.
    if not line[0].isupper():return None
    tail=line[m.end():].lstrip()
    if re.match(r'^ART[ÍI]CULOS\b',line,re.I) and re.match(r'^(?:[,;]|\d|[yYeE]\s+\d)',tail):return None
    return m
