# IEEN — lote 2: lineamientos electorales

15 documentos (IDs 22–36), 229 páginas, 477 artículos de cuerpo y 10 transitorios. Sección `electoral`. Fuente: `IEEN/catalogo/normatividad.json`; se descargó cada URL vigente individualmente, sin convertir antecedentes.

| ID | Nombre oficial impreso | Páginas | Cuerpo | Transitorios |
|---|---|---:|---:|---:|
| 22 | LINEAMIENTOS PARA LA INTEGRACIÓN, FUNCIONAMIENTO, ACTUALIZACIÓN Y CONSERVACIÓN DEL REGISTRO ESTATAL DE PERSONAS SANCIONADAS EN MATERIA DE VIOLENCIA POLÍTICA CONTRA LAS MUJERES EN RAZÓN DE GÉNERO. | 11 | 18 | 4 |
| 23 | LINEAMIENTOS DE SEGURIDAD SANITARIA EN LAS ETAPAS DE APOYO CIUDADANO, PRECAMPAÑAS Y CAMPAÑAS ELECTORALES EN EL MARCO DEL PROCESO ELECTORAL LOCAL ORDINARIO 2021, ANTE LA PANDEMIA PROVOCADA POR EL VIRUS SARS-COV2 (COVID-19). | 7 | 16 | 0 |
| 24 | LINEAMIENTOS PARA EL REGISTRO DE CANDIDATURAS COMUNES DEL INSTITUTO ESTATAL ELECTORAL DE NAYARIT | 5 | 15 | 0 |
| 25 | LINEAMIENTOS PARA EL REGISTRO DE PLATAFORMAS Y CANDIDATURAS A LOS DISTINTOS CARGOS DE ELECCIÓN POPULAR, QUE REALICEN LOS PARTIDOS POLÍTICOS, COALICIONES Y CANDIDATURAS COMUNES ANTE EL INSTITUTO ESTATAL ELECTORAL DE NAYARIT, PARA EL PROCESO ELECTORAL LOCAL 2024. | 35 | 86 | 0 |
| 26 | LINEAMIENTOS PARA LA LIQUIDACIÓN DE LAS ASOCIACIONES CIVILES CONSTITUIDAS PARA OBTENCIÓN DE LAS CANDIDATURAS INDEPENDIENTES CORRESPONDIENTES A LOS PROCESOS ELECTORALES LOCALES ORDINARIOS Y EXTRAORDINARIOS EN EL ESTADO DE NAYARIT. | 22 | 45 | 0 |
| 27 | LINEAMIENTOS DIRIGIDOS A LOS PARTIDOS POLÍTICOS LOCALES, Y EN SU CASO, A LOS PARTIDOS POLÍTICOS NACIONALES, SOBRE LAS MODIFICACIONES A SUS DOCUMENTOS BÁSICOS; REGISTRO DE INTEGRANTES DE LOS ÓRGANOS DIRECTIVOS; REGISTRO DE SUS REGLAMENTOS INTERNOS; CAMBIO DE DOMICILIO, Y ACREDITACIÓN DE SUS REPRESENTANTES ANTE EL CONSEJO LOCAL O CONSEJOS MUNICIPALES ELECTORALES DEL INSTITUTO ESTATAL ELECTORAL DE NAYARIT. | 14 | 67 | 0 |
| 28 | LINEAMIENTOS PARA LA DELIMITACIÓN TERRITORIAL DE LAS DEMARCACIONES ELECTORALES MUNICIPALES DEL ESTADO DE NAYARIT | 10 | 0 | 0 |
| 29 | LINEAMIENTOS PARA EL REGISTRO DE LA CIUDADANÍA ASPIRANTES A CANDIDATURAS INDEPENDIENTES. | 31 | 0 | 0 |
| 30 | Lineamientos en materia de adquisiciones de bienes inmuebles del Instituto Estatal Electoral de Nayarit | 9 | 22 | 2 |
| 31 | LINEAMIENTOS PARA EL REGISTRO DE LA CIUDADANÍA QUE ASPIRA A CONTENDER A TRAVÉS DE UNA CANDIDATURA INDEPENDIENTE A LOS DISTINTOS CARGOS DE ELECCION POPULAR PARA EL PROCESO ELECTORAL LOCAL 2024 | 18 | 62 | 0 |
| 32 | PROCEDIMIENTO PARA LA OBTENCIÓN DEL APOYO DE LA CIUDADANÍA. | 14 | 58 | 0 |
| 33 | LINEAMIENTOS QUE REGULAN LA PROPAGANDA ELECTORAL DURANTE LA ETAPA DE OBTENCIÓN DE APOYO DE LA CIUDADANÍA, PRECAMPAÑAS Y CAMPAÑAS ELECTORALES EN LOS PROCESOS ELECTORALES LOCALES. | 12 | 16 | 2 |
| 34 | LINEAMIENTOS GENERALES SOBRE RECOMENDACIONES A LOS MEDIOS DE COMUNICACIÓN RESPECTO DE LA INFORMACIÓN Y DIFUSIÓN DE LAS ACTIVIDADES DE PRECAMPAÑA Y CAMPAÑA QUE REALICEN LOS PARTIDOS POLÍTICOS, COALICIONES ASÍ COMO LAS Y LOS CANDIDATOS INDEPENDIENTES, DURANTE EL PROCESO ELECTORAL LOCAL 2021. | 7 | 0 | 0 |
| 35 | LINEAMIENTOS PARA EL REGISTRO DE PLATAFORMAS Y CANDIDATURAS A LOS DISTINTOS CARGOS DE ELECCIÓN POPULAR, QUE REALICEN LOS PARTIDOS POLÍTICOS Y COALICIONES ANTE EL INSTITUTO ESTATAL ELECTORAL DE NAYARIT, PARA EL PROCESO ELECTORAL LOCAL 2021 | 11 | 40 | 0 |
| 36 | LINEAMIENTOS EN MATERIA DE PARIDAD DE GÉNERO, VIOLENCIA POLÍTICA POR RAZÓN DE GÉNERO E INTEGRACIÓN PARITARIA DEL CONGRESO DEL ESTADO Y AYUNTAMIENTOS, QUE DEBERÁN OBSERVAR ANTE EL INSTITUTO ESTATAL ELECTORAL DE NAYARIT LOS PARTIDOS POLÍTICOS, COALICIONES Y CANDIDATURAS COMUNES EN EL REGISTRO DE CANDIDATAS Y CANDIDATOS A LOS DISTINTOS CARGOS DE ELECCIÓN POPULAR DEL PROCESO ELECTORAL LOCAL ORDINARIO 2021. | 23 | 32 | 2 |

## Conservación, texto e índices

- Los 15 originales tienen capa de texto y las 229 páginas tienen texto extraíble. Ninguno queda sin promover; no se aplicó OCR.
- Originales y recibos permanentes: `../respaldo-conversiones/IEEN/lote-2/<id>/` respecto del repositorio. Cada recibo guarda URL, fecha y SHA-256; la versión es el hash del PDF. PDF y extracción se conservan también en cada versión local, excluidos de Git conforme a las convenciones del acervo. No hay Word en el catálogo.
- Conservación por página de todos los caracteres no blancos, signos, secuencia de cifras y comienzos de listas entre Poppler y el Markdown guardado. Marcadores de las 229 páginas verificados. Discrepancias entre lectores son informativas, sin reparación del texto.
- Cotejo visual de primera y última página de cada PDF (30 páginas). No es cotejo visual integral. Portadas cotejadas para el nombre oficial, distinto del nombre de catálogo cuando corresponde.
- 477 rótulos propios reconocidos por número y página, sin huecos ni duplicados en sus secuencias. Cero rótulos propios omitidos. Las remisiones al inicio de línea se registran en `validacion.json` y no se promueven. El ID 27 imprime `Articulo 4.-` sin tilde y se reconoce. El ID 36, página 2, cita «Artículo 3 párrafo 4, 25 numeral 1 inciso r).» en una nota del marco legal: no es artículo propio.
- Los transitorios son 4 en ID 22, 2 en ID 30, 2 en ID 33 y 2 en ID 36. Los demás documentos no traen sección transitoria en el PDF cargado.
- Se ejecutó `python3 bin/indices.py --entidad IEEN`. Acumulado IEEN: 28 documentos, 1,265 artículos de cuerpo y 44 transitorios. Versiones, enlaces `actual`, destinos de `rutas.json` y rangos de artículos verificados. SQLite regenerado localmente, no publicado. No se cambian índices de otras entidades ni reglas del parser.

## Estructuras no articuladas

No se fuerza el reconocimiento de numerales como artículos:

- **ID 28:** numerales principales 1–35, con listas subordinadas.
- **ID 29:** numerales principales 1–144.
- **ID 34:** doce apartados I–XII, con numerales que reinician en cada apartado.

Los tres tienen texto completo, metadata, versión y ruta; sus conteos de artículos y transitorios son cero. **El índice de articulado y la búsqueda FTS por artículos no cubren estos tres textos**: se consultan completos desde la ruta del documento. Esta limitación queda registrada en su validación; no se modifica el contrato de índices para inventar artículos.

## Acuerdos y cadenas de reformas

La selección se verificó comparando fechas ISO de `vigente` y de toda la cadena, no tomando la última entrada de la lista. El recibo y el hash vinculan cada PDF cargado a esa URL exacta. Acuerdo y fecha de catálogo tienen procedencia explícita; no se afirma que estén impresos en el anexo.

| ID | Acuerdo más reciente | Fecha | Resultado |
|---|---|---|---|
| 26 | IEEN-CLE-130/2020 | 2020-10-30 | Cargado; posterior al antecedente IEEN-CLE-034/2018 de 2018-04-23. |
| 33 | IEEN-CLE-128/2023 | 2023-12-15 | Cargado; la última entrada de reformas es la antigua IEEN-CLE-088/2021 de 2021-04-07. |
| 36 | IEEN-CLE-220/2020 | 2020-12-31 | Cargado; la última entrada de reformas es IEEN-CLE-158/2020 de 2020-11-27. |
| 37 | IEEN-CLE-043/2024 | 2024-02-08 | Comprobado en catálogo; fuera del lote 22–36, no descargado ni promovido. |

La solicitud menciona cinco documentos pero enumera cuatro. En el rango 22–36, el catálogo registra cadena no vacía únicamente en 26, 33 y 36. No se inventó un quinto ni se amplió el lote.

## Metadata e incidencias

Mismos campos del lote 1; `tipo: lineamientos` según categoría del catálogo y `seccion: electoral`. ID 32 conserva como nombre oficial «PROCEDIMIENTO PARA LA OBTENCIÓN DEL APOYO DE LA CIUDADANÍA.» aunque pertenece a la categoría Lineamientos. `reformas` conserva íntegra la lista de origen.

Número de decreto, publicación y última reforma quedan null cuando no se identifican inequívocamente en el texto; las fechas de catálogo no los sustituyen. Las incidencias quedan por campo. El ID 33, página 12, abroga los lineamientos de propaganda de 2021: se conserva íntegro el segundo transitorio; su fecha de efectos queda null porque depende de publicación sin fecha impresa. El 07-04-2021 corresponde a la aprobación del antecedente, no a la abrogación.

El ID 27, página 14, imprime la nota sobre texto tachado dejado sin efectos por sentencia TEE-AP-09/2019, notificada el 25-05-2020. Se conserva texto y nota; la extracción no garantiza reproducir el tachado gráfico y debe consultarse el PDF para ese alcance. No se transforma esa fecha en última reforma o publicación. Los IDs 34 y 36 conservan los fragmentos extraídos de la marca de agua «Copia de Internet», sin limpieza interpretativa.

PR en borrador para revisión. Sin merge a main.
