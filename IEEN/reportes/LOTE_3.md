# IEEN — lote 3: cierre de la sección normatividad

Criterio vigente de `IEEN/LEEME.md` (0b0a218): portada en imagen sin texto normativo admite promoción con cotejo visual vinculado al SHA-256 y título transcrito en metadata. Una página interior sin texto bloquea la promoción. Nunca OCR.

Quince documentos 37–51 procesados: **13 promovidos, 2 pendientes**. Los promovidos suman 196 páginas, **283 artículos de cuerpo, 14 transitorios y 39 secciones**: 11 documentos con articulado y 2 por secciones (47 y 50).

| ID | Nombre de portada | Páginas | Cuerpo | Transitorios | Secciones | Estado |
|---|---|---:|---:|---:|---:|---|
| 37 | Lineamientos para garantizar el cumplimiento del principio de paridad de género y no discriminación en la postulación de candidaturas, así como en la integración del Congreso del Estado y Ayuntamientos en el proceso electoral local ordinario 2024. | 16 | 20 | 2 | 0 | Promovido |
| 38 | LINEAMIENTOS PARA QUE LOS PARTIDOS POLÍTICOS NACIONALES Y, EN SU CASO, LOS PARTIDOS POLÍTICOS LOCALES, PREVENGAN, ATIENDAN, SANCIONEN, REPAREN Y ERRADIQUEN LA VIOLENCIA POLÍTICA CONTRA LAS MUJERES EN RAZÓN DE GÉNERO | 24 | 32 | 5 | 0 | Promovido |
| 39 | LINEAMIENTOS DEL INSTITUTO ESTATAL ELECTORAL DE NAYARIT, PARA QUE LOS PARTIDOS POLÍTICOS LOCALES PREVENGAN, ATIENDAN, SANCIONEN, REPAREN Y ERRADIQUEN LA VIOLENCIA POLÍTICA CONTRA LAS MUJERES EN RAZÓN DE GÉNERO. | 25 | 32 | 4 | 0 | Promovido |
| 40 | LINEAMIENTOS PARA LA RECOPILACIÓN DE FIRMAS Y ACTIVIDADES RELACIONADAS CON EL PROCESO DE SOLICITUD DE REVOCACIÓN DE MANDATO | 14 | 31 | 0 | 0 | Promovido |
| 41 | LINEAMIENTOS QUE ESTABLECEN LAS REGLAS Y CRITERIOS QUE LAS PERSONAS FÍSICAS O MORALES DEBERÁN ADOPTAR PARA REALIZAR ENCUESTAS O SONDEOS DE OPINIÓN EN EL MARCO DEL PROCESO ELECTORAL EXTRAORDINARIO 2025. | 12 | 26 | 0 | 0 | Promovido |
| 42 | LINEAMIENTOS PARA EL FUNCIONAMIENTO Y LA INTEGRACIÓN DE LAS JUNTAS AUXILIARES OPERATIVAS DEL INSTITUTO ESTATAL ELECTORAL DE NAYARIT PARA EL PROCESO ELECTORAL EXTRAORDINARIO 2025 | 10 | 13 | 0 | 0 | Promovido |
| 43 | LINEAMIENTOS DEL SISTEMA CONÓCELES PARA LA ELECCIÓN DE INTEGRANTES DEL PODER JUDICIAL DEL ESTADO DE NAYARIT. | 10 | 14 | 0 | 0 | Promovido |
| 44 | Lineamientos para garantizar el principio constitucional de paridad de género en el Proceso Electoral Extraordinario 2025. | 9 | 10 | 2 | 0 | Promovido |
| 45 | Lineamientos que establecen las reglas procesales en el trámite de procedimientos sancionadores a cargo de la Dirección Jurídica del Instituto Estatal Electoral de Nayarit, así como el Catálogo de Infracciones para el proceso electoral extraordinario del Poder Judicial del estado de Nayarit 2025. | 5 | — | — | — | Pendiente |
| 46 | LINEAMIENTO PARA EL DESARROLLO DE LOS FOROS DE DEBATE | 8 | 31 | 1 | 0 | Promovido |
| 47 | LINEAMIENTOS PARA EL DESARROLLO DE LOS CÓMPUTOS PARCIALES Y ESTATAL DEL INSTITUTO ESTATAL ELECTORAL DE NAYARIT. PROCESO ELECTORAL EXTRAORDINARIO DEL PODER JUDICIAL LOCAL 2025 | 29 | 0 | 0 | 29 | Promovido |
| 48 | CRITERIOS ORIENTADORES PARA DETERMINAR LA VALIDEZ O NULIDAD DEL VOTO. | 27 | — | — | — | Pendiente |
| 49 | Lineamientos que regulan la propaganda electoral, para garantizar la imparcialidad y equidad en el Proceso Electoral Extraordinario 2025. | 8 | 13 | 0 | 0 | Promovido |
| 50 | LINEAMIENTOS PARA LA DESTRUCCIÓN DE LA DOCUMENTACIÓN ELECTORAL UTILIZADA EN EL PROCESO ELECTORAL EXTRAORDINARIO 2025 DEL PODER JUDICIAL DEL ESTADO DE NAYARIT | 10 | 0 | 0 | 10 | Promovido |
| 51 | LINEAMIENTOS PARA EL REGISTRO DE LA CIUDADANÍA QUE ASPIRA A CONTENDER A TRAVÉS DE UNA CANDIDATURA INDEPENDIENTE A LOS DISTINTOS CARGOS DE ELECCIÓN POPULAR PARA EL PROCESO ELECTORAL LOCAL 2027 | 21 | 61 | 0 | 0 | Promovido |

## Portadas cotejadas y pendientes

Se revisó visualmente la página 1 de **40, 42 y 47**: solo contiene membrete, logotipos y título; ninguna arranca el articulado ni contiene texto normativo. Se promueven conservando el hash, originales y extracción existentes. `validacion.json` conserva `paginas_sin_texto: [1]` y registra `cotejo_portada`, `control_capa_texto.excepcion_portada: true` y la incidencia admitida. `metadata.json` conserva el título transcrito por cotejo visual y su procedencia explícita. No se agrega texto supuesto ni OCR a la portada en Markdown.

Aportes: **40: 31 artículos, 0 transitorios, 0 secciones; 42: 13 artículos, 0 transitorios, 0 secciones; 47: 0 artículos, 0 transitorios, 29 secciones por página**. El ID 47 usa apartados y numerales, no artículos. La entrada de portada por página procede del fallback del generador; no se presenta como artículo normativo.

Permanecen sin `actual`, fuera de rutas y búsqueda:

- **45:** ninguna de sus cinco páginas tiene texto extraíble; páginas interiores 2–5 ilegibles para el conversor. No aplica la excepción de portada.
- **48:** capa parcial; además de la portada, faltan las páginas interiores **7, 18 y 20**. Contiene ejemplos de boletas en imágenes. No aplica la excepción.

El ID 50 sí tiene texto incorporado por la fuente en sus diez páginas, aunque es escaneado. Se conserva esa capa, incluidas sus grafías anómalas, sin ejecutar OCR ni corregirla. Tablas, firmas y diseño requieren cotejo del original.

## Control general de promoción

`bin/ieen/convertir.py` usa `evaluar_capa_texto`: ninguna página faltante permite promoción ordinaria; cualquier interior faltante bloquea; solo página 1 permite excepción si el registro de cotejo coincide con el SHA-256, contiene título oficial transcrito y certifica página 1 revisada visualmente sin texto normativo. Un cotejo ausente, de otro PDF, o portada con articulado bloquea la excepción. No hay lista de IDs autorizados en el control.

La conversión normal aplica este criterio al terminar sus controles. Para versiones ya convertidas se dispone de `--revisar-promocion --lote 3 --ids 40 42 47`; utiliza los registros de `IEEN/catalogo/revision_lote3.json`. No reconvierte ni sobrescribe originales. Pruebas de regresión cubren portada admitida, revisión ausente o hash distinto, portada normativa, falta de título e interiores faltantes.

## Índices y regresión

Se regeneró con `python3 bin/indices.py --entidad IEEN`, sin modificar el parser de main 1c12ac6. Los **38 documentos ya promovidos mantienen exactamente sus 1,588 entradas anteriores**, incluidos todos los campos de cada entrada (artículos, transitorios y secciones). Evidencia contra 0b0a218 en `regresion-portadas-lote-3.json`. Solo se agregan las entradas de 40, 42 y 47; las fechas de generación se actualizan fuera del arreglo de entradas.

Se mantiene la comprobación anterior contra 1c12ac6: los 25 articulados de lotes 1–2 conservaron sus 1,309 entradas; 28, 29 y 34 tienen 4, 5 y 7 secciones. Ese reporte previo es histórico; la regresión de portadas es el control de este ajuste.

Acumulado IEEN: **41 documentos, 691 páginas promovidas, 1,548 artículos de cuerpo, 58 transitorios y 55 secciones**; 1,661 entradas en FTS. Rutas, enlaces, rangos y hashes verificados. 45 y 48 permanecen excluidos. No cambian índices de otras entidades.

El ID 41 conserva la corrección de los 26 rótulos del índice impreso de páginas 2–3: texto intacto sin promoverlos como artículos; cuerpo real 1–26 desde página 4. Ningún documento ya promovido se reconvirtió en este ajuste.

## Selección por fecha y metadata

- **37:** cadena de cuatro reformas, versión más reciente IEEN-CLE-043/2024, **2024-02-08**, promovida.
- **47:** cadena de dos reformas, versión más reciente IEEN-CLE-PEEPJN-051/2025, **2025-05-29**, URL A1_1, ahora promovida por excepción de portada.

Se comparan fechas de vigente y cadena, nunca posiciones. Recibos y SHA-256 vinculan cada original con su URL individual; antecedentes no convertidos. Fechas y acuerdos del catálogo no se presentan como necesariamente impresos. ID 37 conserva la nota particular del artículo 14 (29 de noviembre de 2023), sin inferir última reforma global.

ID 38 sigue como IEEN/38 con `emisor: INE`, `deduplicacion.clave_origen: INE/CG517/2020:A1`, `evitar_duplicado: true`, referencia IEEN/38 e `id_destino: null`. La clave procede del nombre del archivo; `acuerdo` sigue null como en catálogo. Al cargar INE se cotejarán clave, título y hash antes de duplicar. ID 39 deja sin efectos la adopción local mediante IEEN-CLE-201/2020, no abroga el instrumento nacional; evidencia en página 25.

## Conservación

Quince originales y recibos en `../respaldo-conversiones/IEEN/lote-3/<id>/` respecto del repositorio y copias en cada versión local, excluidos de Git conforme a las convenciones. Versiones por SHA-256; originales intactos. No hay Word en catálogo.

Conservación de caracteres no blancos, signos, cifras y listas entre extracción Poppler y Markdown por página; doble lector informativo sin reparaciones. En los dos pendientes la extracción diagnóstica no acredita integridad normativa. Cotejo visual previo de primera y última página de cada PDF y nueva revisión explícita de las tres portadas. No es cotejo visual integral. Campos normativos no localizados inequívocamente permanecen null con incidencia.

Validaciones: `bin/ieen/pruebas_portadas.py`, `bin/ieen/verificar.py --lote 3`, igualdad exacta de entradas anteriores y comprobación FTS. Misma rama y PR en borrador, sin merge.
