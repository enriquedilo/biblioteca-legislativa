# IEEN — lote 3: cierre de la sección normatividad

Fuente: `IEEN/catalogo/normatividad.json`, sección `normatividad`, tipo `Lineamientos`, números e IDs 37–51. Metadata con `seccion: electoral`. Quince PDF descargados individualmente: 228 páginas examinadas; 10 documentos promovidos (143 páginas), 5 pendientes sin promover. Sin OCR.

**9 documentos con articulado y 1 por secciones.** El lote incorporado suma 239 artículos de cuerpo, 14 transitorios y 10 secciones. Los cinco pendientes no se cuentan como documentos indexados.

| ID | Nombre oficial de portada | Páginas | Cuerpo | Transitorios | Secciones | Estado |
|---|---|---:|---:|---:|---:|---|
| 37 | Lineamientos para garantizar el cumplimiento del principio de paridad de género y no discriminación en la postulación de candidaturas, así como en la integración del Congreso del Estado y Ayuntamientos en el proceso electoral local ordinario 2024. | 16 | 20 | 2 | 0 | Promovido |
| 38 | LINEAMIENTOS PARA QUE LOS PARTIDOS POLÍTICOS NACIONALES Y, EN SU CASO, LOS PARTIDOS POLÍTICOS LOCALES, PREVENGAN, ATIENDAN, SANCIONEN, REPAREN Y ERRADIQUEN LA VIOLENCIA POLÍTICA CONTRA LAS MUJERES EN RAZÓN DE GÉNERO | 24 | 32 | 5 | 0 | Promovido |
| 39 | LINEAMIENTOS DEL INSTITUTO ESTATAL ELECTORAL DE NAYARIT, PARA QUE LOS PARTIDOS POLÍTICOS LOCALES PREVENGAN, ATIENDAN, SANCIONEN, REPAREN Y ERRADIQUEN LA VIOLENCIA POLÍTICA CONTRA LAS MUJERES EN RAZÓN DE GÉNERO. | 25 | 32 | 4 | 0 | Promovido |
| 40 | LINEAMIENTOS PARA LA RECOPILACIÓN DE FIRMAS Y ACTIVIDADES RELACIONADAS CON EL PROCESO DE SOLICITUD DE REVOCACIÓN DE MANDATO | 14 | — | — | — | Pendiente |
| 41 | LINEAMIENTOS QUE ESTABLECEN LAS REGLAS Y CRITERIOS QUE LAS PERSONAS FÍSICAS O MORALES DEBERÁN ADOPTAR PARA REALIZAR ENCUESTAS O SONDEOS DE OPINIÓN EN EL MARCO DEL PROCESO ELECTORAL EXTRAORDINARIO 2025. | 12 | 26 | 0 | 0 | Promovido |
| 42 | LINEAMIENTOS PARA EL FUNCIONAMIENTO Y LA INTEGRACIÓN DE LAS JUNTAS AUXILIARES OPERATIVAS DEL INSTITUTO ESTATAL ELECTORAL DE NAYARIT PARA EL PROCESO ELECTORAL EXTRAORDINARIO 2025 | 10 | — | — | — | Pendiente |
| 43 | LINEAMIENTOS DEL SISTEMA CONÓCELES PARA LA ELECCIÓN DE INTEGRANTES DEL PODER JUDICIAL DEL ESTADO DE NAYARIT. | 10 | 14 | 0 | 0 | Promovido |
| 44 | Lineamientos para garantizar el principio constitucional de paridad de género en el Proceso Electoral Extraordinario 2025. | 9 | 10 | 2 | 0 | Promovido |
| 45 | Lineamientos que establecen las reglas procesales en el trámite de procedimientos sancionadores a cargo de la Dirección Jurídica del Instituto Estatal Electoral de Nayarit, así como el Catálogo de Infracciones para el proceso electoral extraordinario del Poder Judicial del estado de Nayarit 2025. | 5 | — | — | — | Pendiente |
| 46 | LINEAMIENTO PARA EL DESARROLLO DE LOS FOROS DE DEBATE | 8 | 31 | 1 | 0 | Promovido |
| 47 | LINEAMIENTOS PARA EL DESARROLLO DE LOS CÓMPUTOS PARCIALES Y ESTATAL DEL INSTITUTO ESTATAL ELECTORAL DE NAYARIT. PROCESO ELECTORAL EXTRAORDINARIO DEL PODER JUDICIAL LOCAL 2025 | 29 | — | — | — | Pendiente |
| 48 | CRITERIOS ORIENTADORES PARA DETERMINAR LA VALIDEZ O NULIDAD DEL VOTO. | 27 | — | — | — | Pendiente |
| 49 | Lineamientos que regulan la propaganda electoral, para garantizar la imparcialidad y equidad en el Proceso Electoral Extraordinario 2025. | 8 | 13 | 0 | 0 | Promovido |
| 50 | LINEAMIENTOS PARA LA DESTRUCCIÓN DE LA DOCUMENTACIÓN ELECTORAL UTILIZADA EN EL PROCESO ELECTORAL EXTRAORDINARIO 2025 DEL PODER JUDICIAL DEL ESTADO DE NAYARIT | 10 | 0 | 0 | 10 | Promovido |
| 51 | LINEAMIENTOS PARA EL REGISTRO DE LA CIUDADANÍA QUE ASPIRA A CONTENDER A TRAVÉS DE UNA CANDIDATURA INDEPENDIENTE A LOS DISTINTOS CARGOS DE ELECCIÓN POPULAR PARA EL PROCESO ELECTORAL LOCAL 2027 | 21 | 61 | 0 | 0 | Promovido |

## Capa de texto y pendientes

- **45:** ninguna de las cinco páginas tiene texto extraíble; es un documento escaneado. No promovido.
- **48:** capa parcial; páginas 1, 7, 18 y 20 sin texto extraíble. Contiene ejemplos de boletas como imágenes que el Markdown no reproduce. No promovido.
- **50:** sí tiene capa de texto en sus diez páginas, aunque el PDF es un escaneo con texto incorporado previamente por la fuente. No se ejecutó OCR. Se conserva la extracción, incluidas sus grafías anómalas (por ejemplo, membrete de portada), sin correcciones interpretativas. Queda promovido con diez secciones por página; las tablas y firmas deben cotejarse en el PDF.
- **40, 42 y 47:** tienen texto en el cuerpo, pero la portada (página 1) contiene texto visible en imagen que no se extrae —solo paginación en 42 y 47—. Se mantienen sin promover conforme al control de páginas sin texto. No se los describe como PDF totalmente sin capa de texto.

Las cinco versiones pendientes conservan PDF, extracción diagnóstica, Markdown marcado como incompleto, metadata y validación; carecen de `actual.json` y enlace `actual`, y no aparecen en rutas ni FTS. Los nombres de sus portadas se transcribieron mediante cotejo visual únicamente en metadata; no se completó el texto ni se aplicó OCR. La etapa de procesamiento de los 43 candidatos electorales está recorrida, pero el acervo promovido no está completo: quedan estos cinco pendientes y los 21 documentos de la sección interna aún no abordados.

## Índices y protección de los lotes anteriores

Se partió de `main` con `1c12ac6` y se ejecutó `python3 bin/indices.py --entidad IEEN`, sin modificar `bin/indices.py`.

| ID del lote 2 | Entradas antes | Entradas después | Tipo |
|---|---:|---:|---|
| 28 | 0 | 4 | seccion |
| 29 | 0 | 5 | seccion |
| 34 | 0 | 7 | seccion |

Los **25 documentos con articulado de los lotes 1 y 2 conservan idénticas sus 1,309 entradas**: 1,265 de cuerpo y 44 transitorias. Se comparó el arreglo completo de entradas, no solo conteos; no cambia una sola entrada, sus rangos, notas ni hashes. El nuevo contador `secciones: 0` y la fecha de generación están fuera del arreglo. Evidencia reproducible en `regresion-indices-lote-3.json`, con base y hashes de las entradas.

Acumulado IEEN promovido: **38 documentos, 1,504 artículos de cuerpo, 58 transitorios y 26 secciones**, equivalentes a 1,588 entradas de búsqueda. Los cuatro documentos sin articulado (28, 29, 34 y 50) tienen entradas y quedan incluidos en FTS. Solo se regeneran índices IEEN; los acervos anteriores permanecen intactos.

En el ID 41 se corrigió una falsa promoción de 26 rótulos del índice impreso en páginas 2–3: las líneas de puntos guía se conservan íntegramente, pero sin marca de encabezado de artículo. El cuerpo tiene artículos 1–26 desde la página 4. No hubo necesidad de cambiar el parser de índices ni de reconvertir documentos anteriores. Auditoría de rótulos propios por número y página: cero omitidos entre los promovidos; sin huecos ni duplicados en sus secuencias.

## Selección de versiones por fecha

| ID | Cadena de reformas | Acuerdo seleccionado | Fecha mayor | Resultado |
|---|---:|---|---|---|
| 37 | 4 | IEEN-CLE-043/2024 | 2024-02-08 | Descargado, convertido y promovido desde su URL A1. |
| 47 | 2 | IEEN-CLE-PEEPJN-051/2025 | 2025-05-29 | Descargado y convertido como diagnóstico desde su URL A1_1; sin promover por portada sin texto extraíble. |

Se compararon las fechas de `vigente` y toda la cadena; no se eligió por posición. Los recibos y hashes acreditan la descarga de la URL exacta seleccionada; no se descargaron los antecedentes. Acuerdo y fecha provienen del catálogo, no se presentan como datos necesariamente impresos en el anexo. El ID 37 conserva la nota particular «Reformado, 29 de noviembre de 2023» del artículo 14, página 9, sin sustituir con ella la fecha de versión del catálogo ni inferir una declaración de última reforma global.

## ID 38: origen INE y deduplicación futura

Se incorpora como **IEEN/38**, con `fuente` y `urls` del catálogo IEEN. En metadata se agregan:

- `emisor: "INE"`.
- `deduplicacion.entidad_origen: "INE"`.
- `deduplicacion.clave_origen: "INE/CG517/2020:A1"`.
- `deduplicacion.evitar_duplicado: true`.
- `deduplicacion.referencia_existente: {entidad: "IEEN", id: 38}`.
- `deduplicacion.id_destino: null`, porque aún no existe una correspondencia comprobada en el acervo INE.

La clave procede del nombre del archivo en la URL oficial de catálogo, documentado expresamente. `acuerdo` se mantiene null como en el catálogo; no se inventa un acuerdo impreso. Al cargar INE se deberá cotejar clave, nombre oficial y hash para reutilizar o enlazar el texto existente; si la versión difiere, deberá mantenerse trazabilidad por contenido. Esta marca es una instrucción persistente para la futura carga, no una afirmación de que ya exista deduplicación automática.

El ID 39, tercero transitorio (página 25), deja sin efectos la adopción local de los lineamientos INE realizada mediante IEEN-CLE-201/2020. Se conserva y documenta como tal; no se confunde con abrogación del instrumento nacional del ID 38.

## Conservación y alcance de la validación

Originales y recibos permanentes en `../respaldo-conversiones/IEEN/lote-3/<id>/` respecto del repositorio; copias locales en cada versión. Cada versión utiliza directamente el SHA-256 del PDF. Originales y extracciones están excluidos de Git según las convenciones; metadata, texto y validación se publican. No hay Word en el catálogo.

Se verificaron hashes de los 15 originales y conservación por página entre la extracción Poppler y Markdown: caracteres no blancos, signos, cifras y comienzos de listas. En los pendientes este control verifica solo la extracción disponible, no la integridad del PDF visible. Marcadores de página, rangos y rutas se verificaron; comparación con pypdf informativa, sin reparaciones por diferencias entre lectores.

Cotejo visual por muestra: primera y última página de los quince PDF (30 páginas), sin cotejo visual integral. Número de decreto, publicación y última reforma quedan null cuando no hay declaración inequívoca; incidencias registradas por campo. Los datos de catálogo no sustituyen los impresos.

Validación: `bin/ieen/verificar.py --lote 3` con Python provisto de pypdf; comprobación de regresión de índices contra `1c12ac6`. PR en borrador, sin merge.
