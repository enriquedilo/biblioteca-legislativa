"""Reconocimiento de rótulos impresos; normalización explícita de millares en rótulos."""
import re
SUFIJO=r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+'
NUMERO=r'(?:\d{1,3}(?:,\d{3})+|\d+)(?:ro|do|to|o|º|°)?'
PUNTUACION=r'(?:[.;:,–—-]+\s+)?'
ROTULO=PUNTUACION+r'(?:ART[ÍI]CULOS?\.?|ART\.)\s*'+NUMERO+r'(?:\s*'+SUFIJO+r'(?:[ -]*(?:\d+|[A-Z])(?=[.\s:-]|$))?|\s+[A-Z](?=[.\s:-]|$))?'
CANDIDATO=re.compile(r'^'+ROTULO+r'(?:\.-|[.:-])?',re.I)
RANGO=re.compile(r'^'+PUNTUACION+r'(?:ART[ÍI]CULOS)\s+(\d+)\s+al\s+(\d+)\s*(?:\.-|[.-])',re.I)
EXPLICITO=re.compile(r'^'+ROTULO+r'\s*(?:\.-|[.:-])',re.I)
SOLO=re.compile(r'^'+PUNTUACION+r'(?:ART[ÍI]CULOS?\.?|ART\.)\s*'+NUMERO+r'(?:\s+(?:Bis|Ter|Qu[áa]ter|[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]*(?:ies|íes|imus|enus))(?:\s+\d+)?)?\s*$',re.I)
MILLARES=re.compile(r'((?:ART[ÍI]CULOS?\.?|ART\.)\s*)(\d{1,3}(?:,\d{3})+)',re.I)
def normalizar_millares(text):
    return MILLARES.sub(lambda m:m[1]+m[2].replace(',',''),text)
def encabezado(line):
    m=RANGO.match(line) or EXPLICITO.match(line) or SOLO.match(line)
    if not m:return None
    # Wrapped references in lowercase are not new article headings.
    literal=re.sub(r'^[.;:,–—-]+\s+','',line)
    if not literal[0].isupper():return None
    tail=line[m.end():].lstrip()
    if re.match(r'^ART[ÍI]CULOS\b',literal,re.I) and re.match(r'^(?:[,;]|\d|[yYeE]\s+\d)',tail):return None
    return m
