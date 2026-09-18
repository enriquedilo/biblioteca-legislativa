"""Registra el cotejo del piloto y comprueba integridad local antes de publicar."""
import json,re,hashlib,collections
from pathlib import Path
import piloto
from pypdf import PdfReader
F=piloto.FED;rows=piloto.catalog();results=json.loads((F/'reportes/piloto_resultados.json').read_text());reviews=json.loads((piloto.ROOT/'work/resumen.json').read_text());summary=[]
for r in results:
 d=F/'ordenamientos'/str(r['id'])/'actual';m=json.loads((d/'metadata.json').read_text());v=json.loads((d/'validacion.json').read_text());raw=(d/'extraccion.txt').read_text();md=(d/'texto.md').read_text();review=next(x for x in reviews if x['sigla']==r['sigla'])
 for kind,suffix in [('pdf','pdf'),('word','doc')]:assert hashlib.sha256((d/('original.'+suffix)).read_bytes()).hexdigest()==m['hash_sha256'][kind]
 assert m['version']==json.loads((d.parent/'actual.json').read_text())['version']
 assert len(re.findall(r'<!-- PAGINA_PDF: \d+ -->',md))==v['paginas_pdf']
 assert v['texto_conservado'] and all(x['inicios_lista_conservados'] for x in v['controles_por_pagina'])
 assert m['orden']=='federal' and m['po_publicacion']['diario']=='DOF'
 multi=[x for x in m['reformas'] if len(x['fechas'])>1];assert all(x['fecha'] is None for x in multi)
 v['paginas_cotejadas_visualmente']=review['samples'];v['cotejo_visual']={'alcance':'Muestra de primera página, inicio de transitorios y última página; encabezados, fracciones y transitorios contrastados con extracción. No es cotejo visual exhaustivo.','paginas':review['samples'],'fecha':piloto.base.now()}
 v['comparacion_cifras_multiconjunto']={'paginas_coinciden':review['paginas_cifras_mismo_multiconjunto'],'paginas_difieren':review['paginas_cifras_diferentes'],'limite':'Compara ocurrencias de cadenas numéricas sin exigir orden; diferencias no reparadas. No sustituye control de secuencia.'}
 piloto.base.savejson(d/'validacion.json',v)
 summary.append({'sigla':r['sigla'],'id':r['id'],'version':r['version'],'paginas':r['paginas'],'notas_reforma':len(m['reformas']),'notas_con_varias_fechas':len(multi),'paginas_cifras_difieren':review['paginas_cifras_diferentes'],'paginas_visuales':review['samples'],'word_pdf_articulos_coinciden':v['identificadores_articulos_coinciden']})
piloto.base.savejson(F/'reportes/verificacion_piloto.json',{'fecha':piloto.base.now(),'documentos':summary,'controles_integridad_y_conservacion':'aprobados','cotejo_dos_lectores':'con incidencias pendientes; no habilita escalamiento automático','catalogo':dict(collections.Counter(x['seccion_sitio'] for x in rows))})
piloto.state(rows,results)
report='''# Informe del piloto federal

## Resultado

Cuatro PDF y cuatro originales .doc descargados individualmente; sin LEYFED, OCR, índices de búsqueda ni articulado. 928 páginas. Integridad SHA-256 y correspondencia de actual.json/enlace actual verificadas. Todos los controles de conservación de contenido, signos e inicios de listas del PDF extraído al Markdown pasan. Marcadores de página completos.

Captura oficial: 316 entradas principales y 137 reglamentos (453), frente a la estimación de 317/127. Se capturaron únicamente filas numeradas con enlace al documento vigente en index.htm y regla.htm; no se siguieron índices de abrogados. El alcance se debe revisar antes de lotes.

## Límites e incidencias

Hay diferencias de extracción entre Word y PDF en los cuatro documentos; en CPEUM y CFF difiere la secuencia de encabezados reconocidos, aunque el conjunto de identificadores coincide en los cuatro documentos. La secuencia de cifras entre Poppler y pypdf difiere en muchas páginas. Aun sin exigir orden, difieren las ocurrencias numéricas en 28 páginas: CPEUM 14, CFF 12, LGDNNA 1 y Reg_CFF 1. No se han reparado ni certificado equivalentes. Ver verificacion_piloto.json y validacion.json de cada versión para páginas y controles.

Cotejo visual por muestra: primera página, inicio de transitorios y última página de cada PDF (12 páginas); no exhaustivo. Las notas de reforma conservan texto literal y todas las fechas reconocidas en fechas; fecha escalar null cuando son varias. Reglamento sin notas de reforma identificadas; ultima_reforma null. Campos no impresos quedan null con incidencias. Abrogaciones expresas se capturan automáticamente como evidencia pendiente de cotejo, sin completar datos ausentes.

Las primeras conversiones preparatorias de CPEUM, CFF y LGDNNA omitieron Word por un defecto de selección de enlace. Se corrigió la selección y se crearon versiones nuevas con ambos originales; se conservan las versiones preparatorias sin sobrescribirlas. Las versiones actuales son las del reporte de verificación.

Originales y extraccion.txt permanecen en la Mac y están excluidos de Git según la política existente. SHA-256 y URL de cada original constan en metadata.json. La publicación en la rama federal conserva textos, metadatos, controles y avance, pero los binarios locales requieren respaldo independiente.

## Continuación

Piloto detenido. No se iniciaron lotes. Antes de escalar deben revisarse alcance y diferencias de extracción. El estado se guarda tras cada documento en AVANCE.md y reportes/avance_lotes.json. El controlador de lotes de diez y sus pushes se implementará al autorizar la continuación; el piloto no ejecuta lotes. No se modifican vigilancia, automatizaciones, skills ni las entidades estatales. PR final al concluir el acervo; merge reservado al usuario.
'''
(F/'reportes/piloto.md').write_text(report)
print(json.dumps(summary,ensure_ascii=False))
