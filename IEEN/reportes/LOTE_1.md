# IEEN — lote 1: reglamentos electorales

13 documentos, 266 páginas, 788 artículos de cuerpo y 34 transitorios. Cero documentos o páginas sin texto extraíble; sin OCR.

| ID | Reglamento (nombre de catálogo) | Páginas | Cuerpo | Transitorios |
|---|---|---:|---:|---:|
| 9 | Reglamento de Sesiones del Consejo Local Electoral. | 20 | 48 | 2 |
| 10 | Reglamento de Sesiones de la Junta Estatal Ejecutiva del Instituto Estatal Electoral del Estado de Nayarit. | 11 | 29 | 1 |
| 11 | Reglamento de Comisiones del Consejo Local Electoral. | 20 | 26 | 1 |
| 12 | Reglamento de Sesiones de los Consejos Municipales Electorales. | 19 | 47 | 0 |
| 13 | Reglamento para el funcionamiento de la Oficialía Electoral del Instituto Electoral Electoral de Nayarit. | 17 | 46 | 5 |
| 14 | Reglamento de Quejas y Denuncias. | 24 | 73 | 4 |
| 15 | Reglamento del Sistema de Quejas y Denuncias. | 8 | 35 | 4 |
| 16 | Reglamento de la Ley de Participación Ciudadana. | 12 | 59 | 1 |
| 17 | Reglamento para la constitución y registro de partidos políticos locales del Instituto Estatal Electoral de Nayarit. | 40 | 105 | 6 |
| 18 | Reglamento que establece el procedimiento sobre la Pérdida de Registro y Liquidación de los Partidos Políticos Locales. | 13 | 45 | 2 |
| 19 | Reglamento de Fiscalización del Instituto Estatal Electoral de Nayarit para las Organizaciones de Ciudadanos y Ciudadanas que desean constituirse como Partido Político Local. | 31 | 103 | 5 |
| 20 | Reglamento del Centro de Capacitación del Instituto Estatal Electoral. | 20 | 81 | 2 |
| 21 | Reglamento de Quejas y Denuncias en Materia de Violencia Política contra las Mujeres en Razón de Género del Instituto Estatal Electoral de Nayarit | 31 | 91 | 1 |

## Controles y alcance

- Los trece originales se respaldaron permanentemente en la Mac bajo `respaldo-conversiones/IEEN/lote-1/<id>/`, con recibo de URL, fecha y SHA-256. La versión usa directamente ese SHA-256, no el hash de un manifiesto. No se convierten antecedentes.
- PDF y extracción están excluidos de Git. Versiones, actual.json, enlaces actual y metadata conservan la misma identidad.
- Conservación de todos los caracteres no blancos y signos por página entre Poppler y el Markdown guardado, secuencias de cifras, inicios de listas/fracciones, articulado y colas transitorias. Se conservan erratas y números impresos; solo se retira paginación aislada documentada.
- Las frecuencias de dígitos de Poppler y pypdf coinciden en las 266 páginas. Su orden difiere en varias páginas; las discrepancias quedan registradas, sin reparaciones. El Markdown conserva la secuencia de Poppler. No se declara igualdad textual entre lectores.
- Cotejo visual por muestra: primera y última página de cada PDF, y página 2 del ID 16. No es cotejo integral del original ni certificación de vigencia jurídica.
- Auditoría independiente de rótulos numéricos impresos por identificador y página frente al índice: sin rótulos de artículo omitidos. Remisiones minúsculas preservadas en cuerpo y registradas, no promovidas. El artículo 220 citado en ID 21 es una remisión a la Ley Electoral, no un artículo propio.
- ID 9 incluye 15 bis y 16 bis; ID 11 incluye 6 bis. ID 10 conserva «Artículo 29-». ID 16 usa «ARTÍCULO TRANSITORIO» singular; IDs 17 y 18 usan «Artículo Primero…». No fue necesario cambiar las reglas de reconocimiento del índice.
- ID 12 termina en artículo 47, sin sección transitoria en el archivo: cero transitorios, no una pérdida de conversión.

## Metadata y pendientes

`seccion` es `electoral`. Acuerdo, fecha del catálogo y cadena completa de reformas se copian de `normatividad.json` con procedencia explícita, sin inferir que el PDF imprima esos datos. Los antecedentes quedan sin descargar ni convertir. Se conserva «-» si así figura el acuerdo del catálogo.

El ID 16 incluye publicación oficial: Sección Segunda, tomo CXCIII, número 077, 25 de octubre de 2013. El ID 17 imprime última modificación de 17 de agosto de 2018. En los demás, publicación/última reforma no identificadas inequívocamente quedan null; el número de decreto queda null en todos. No se sustituye última reforma por la fecha del catálogo. Cláusulas de abrogación en IDs 13, 14 y 20 se conservan con texto y página; campos no desglosados quedan pendientes. Las incidencias por campo constan en cada validacion.json. Los nombres oficiales se cotejaron en la muestra, diferenciándolos del nombre del catálogo.

## Índices

Se ejecuta `python3 bin/indices.py`. En el commit base ed1eb50, pese al título del commit, ENTIDADES_CONOCIDAS todavía omitía IEEN; se agrega exclusivamente esa entrada. Se conservan intactas las reglas de reconocimiento. Se verifican destinos de rutas.json, versiones y rangos de artículos. Se descartan diferencias de mera fecha de generación en los otros acervos. SQLite se genera localmente y no se publica.

PR en borrador para cotejo. Sin merge a main; no se modifica la automatización semanal.
