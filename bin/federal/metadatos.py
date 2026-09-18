#!/usr/bin/env python3
"""Ajustes federales de abrogación basados únicamente en la portada impresa."""
import argparse,hashlib,json,os,re,shutil
from pathlib import Path
import piloto as p
b=p.base;F=p.FED
FECHA=r'(?:\d{1,2}(?:o|º|°)?\.?\s+(?:de\s+)?(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+(?:de|del)\s+\d{4}|\d{2}[-/]\d{2}[-/]\d{4})'
SELF=re.compile(r'\b(?:Código|Ley|Reglamento|Estatuto|Constitución)\s+abrogad[ao]\b|\b(?:este|esta|su)\s+(?:ordenamiento|Código|Ley|Reglamento|vigencia).{0,80}?(?:abrogad[ao]|termina|concluye|finaliza|cesa)|\b(?:fin\s+de\s+vigencia|(?:vigencia|vigente)\s+(?:hasta|termina|concluye|finaliza|cesa|concluirá|terminará))\b',re.I)
FIN=re.compile(r'(?:no\s+exceda|no\s+(?:podrá|pueda)\s+exceder|a\s+partir|(?:vigencia|vigente).{0,80}?(?:termina|concluye|hasta|finaliza|cesa|concluirá|terminará)|fin\s+de\s+vigencia)\s*(?:del?|el|día|:)?\s*('+FECHA+r')',re.I)
def abrogacion_programada(raw):
 first=raw.split('\f')[0]
 # The portada ends before the historical promulgation preamble or article 1.
 first=re.split(r'(?mi)^\s*Al margen\b|^\s*(?:ART[ÍI]CULO|ART\.)\s*1[oº°]?[.:-]',first,maxsplit=1)[0]
 paragraphs=[' '.join(x.split()) for x in re.split(r'\n\s*\n',first) if x.strip()]
 declarations=[x for x in paragraphs if SELF.search(x)]
 if not declarations:return None
 # Supplemental portada note can name the decree; it is retained as literal evidence.
 notes=[x for x in paragraphs if re.search(r'Nota sobre la vigencia y abrogación de (?:este|esta)',x,re.I)]
 source=' '.join(dict.fromkeys(declarations+notes))
 dm=re.search(r'\bDecreto por (?:el|la) que\b.*?(?=,\s*publicad[ao]|\s+publicad[ao]\s+en|,\s*DOF|\.$)',source,re.I)
 if not dm:dm=re.search(r'\bDecreto\s+DOF\s+\d{2}[-/]\d{2}[-/]\d{4}',source,re.I)
 dof=re.search(r'\bDOF\s+(\d{2}[-/]\d{2}[-/]\d{4})',source,re.I)
 limit=FIN.search(source)
 return {'decreto_dof':dm[0] if dm else None,'fecha_dof':p.iso(dof[1]) if dof else None,'fecha_fin_vigencia':p.iso(limit[1]) if limit else None,'evidencia':{'pagina_pdf':1,'texto':source}}
def ajustar(m,v,raw):
 rows=m.get('abroga') or [];removed=[i for i,row in enumerate(rows) if all(value is None for value in row.values())];mapping={i:j for j,i in enumerate(i for i in range(len(rows)) if i not in removed)}
 m['abroga']=[row for i,row in enumerate(rows) if i not in removed]
 nv=v['metadatos_normativos'];inc=[]
 for x in nv['incidencias']:
  if x.get('campo','').startswith('abroga[].') and 'indices' in x:
   x=dict(x);x['indices']=[mapping[i] for i in x['indices'] if i in mapping]
   if not x['indices']:continue
  inc.append(x)
 nv['incidencias']=inc
 if removed:
  nv['incidencias'].append({'campo':'abroga','motivo':'Entradas con todos los campos null descartadas; se conserva evidencia literal de las cláusulas sin inferir datos.','indices_anteriores_descartados':removed})
  v['abroga_entradas_sin_datos_descartadas']={'cantidad':len(removed),'indices_anteriores':removed}
 m['abrogacion_programada']=abrogacion_programada(raw)
 if m['abrogacion_programada']:
  a=m['abrogacion_programada'];nv['evidencia']['abrogacion_programada']=a['evidencia']
  for field in ['decreto_dof','fecha_dof','fecha_fin_vigencia']:
   if a[field] is None:nv['incidencias'].append({'campo':'abrogacion_programada.'+field,'motivo':'Declaración impresa identificada, pero este dato no se localizó inequívocamente; null sin inferir.'})
  if re.search(r'no\s+exceda|no\s+(?:pueda|podrá)\s+exceder',a['evidencia']['texto'],re.I):nv['incidencias'].append({'campo':'abrogacion_programada.fecha_fin_vigencia','motivo':'La portada imprime una fecha límite máxima, sujeta a entrada gradual/declaratorias; no es una fecha única inferida de entrada en vigor. Se conserva la condición literal.'})
 else:nv['incidencias'].append({'campo':'abrogacion_programada','motivo':'Portada/encabezado sin declaración identificada de abrogación o término de vigencia en fecha cierta; null.'})
 return removed
def corregir_existentes():
 import sys
 sys.path.insert(0,str(Path(__file__).resolve().parent))
 import lotes as l
 path=F/'reportes/avance_lotes.json';s=json.loads(path.read_text());report=F/'reportes/ajuste-metadata-abrogacion.json';changes=json.loads(report.read_text())['cambios'] if report.exists() else [];done={x['id'] for x in changes}
 for item in s['items']:
  if item['estado'] not in l.OK or item['id'] in done:continue
  folder=F/'ordenamientos'/str(item['id']);a=json.loads((folder/'actual.json').read_text());old=folder/'versiones'/a['version'];m=json.loads((old/'metadata.json').read_text());v=json.loads((old/'validacion.json').read_text());empty=[x for x in m['abroga'] if all(value is None for value in x.values())]
  if item['id']!=5 and not empty:continue
  raw=(old/'extraccion.txt').read_text();removed=ajustar(m,v,raw)
  correction={'abroga':m['abroga'],'abrogacion_programada':m['abrogacion_programada']};version=hashlib.sha256(json.dumps({'version_anterior':a['version'],'correccion_metadata':correction},sort_keys=True,ensure_ascii=False).encode()).hexdigest();new=folder/'versiones'/version
  if not new.exists():shutil.copytree(old,new)
  m['version']=version;v['correccion_metadata_abrogacion']={'fecha':b.now(),'version_anterior':a['version'],'alcance':'Solo metadatos: elimina entradas de abroga sin datos y extrae declaración de portada. Originales, extracción y Markdown sin cambios.'};b.savejson(new/'metadata.json',m);b.savejson(new/'validacion.json',v)
  for fn in ['texto.md','extraccion.txt']+['original.pdf' if k=='pdf' else 'original.'+v['formato_word_original'] for k in m['hash_sha256']]:assert (old/fn).read_bytes()==(new/fn).read_bytes()
  change={'id':item['id'],'sigla':item['sigla'],'entradas_descartadas':len(removed),'version_anterior':a['version'],'version_nueva':version,'abrogacion_programada':m['abrogacion_programada']};changes.append(change)
  a['version']=version;b.savejson(folder/'actual.json',a);temp=folder/'actual.metadata.tmp'
  if temp.exists() or temp.is_symlink():temp.unlink()
  temp.symlink_to('versiones/'+version,target_is_directory=True);os.replace(temp,folder/'actual');item['detalle']['version']=version;s['ultimo_evento']=f"Ajuste de metadata registrado: ID {item['id']}.";l.persist(s)
  b.savejson(report,{'fecha':b.now(),'alcance':'Solo ID 5 y documentos con entradas de abroga totalmente null. Sin reconversión ni cambios de textos u originales; versiones anteriores intactas.','cambios':changes})
 print(json.dumps({'documentos':len(changes),'entradas_descartadas':sum(x['entradas_descartadas'] for x in changes),'ids':[x['id'] for x in changes],'CFPC':next(x['abrogacion_programada'] for x in changes if x['id']==5)},ensure_ascii=False))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--corregir-existentes',action='store_true');a=ap.parse_args()
 if a.corregir_existentes:corregir_existentes()
