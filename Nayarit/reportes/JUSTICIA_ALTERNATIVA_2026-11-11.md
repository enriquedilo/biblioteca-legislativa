# Nayarit: cotejo del catálogo y sustitución de Justicia Alternativa

Fecha de cotejo: **11 de noviembre de 2026**. Fuente: [catálogo del Congreso](https://congresonayarit.gob.mx/legislacion-estatal/). Se conserva la captura completa y el inventario de URL en [cotejo reproducible](catalogo-2026-11-11-cotejo.json).

## Alcance del hueco, antes de esta carga

Se verificaron **163 URL únicas de PDF vigentes** (secciones 1–7, excluidos los rótulos abrogados) contra **138 URL archivadas**. El Word es otro formato del mismo ordenamiento y no se cuenta dos veces. **135 coincidencias exactas y 28 URL no coincidentes**:

| Clasificación | PDF | Resultado |
|---|---:|---|
| Leyes de ingresos municipales 2026 | 20 | Excluidas desde la carga inicial |
| Fe de erratas de ingresos municipales | 3 | Fuera por pertenecer a la misma sección excluida |
| Ley de Ingresos del Estado 2026 | 1 | Excluida desde la carga inicial |
| Presupuesto de Egresos 2026 | 1 | Excluido desde la carga inicial |
| Ley de Igualdad entre Mujeres y Hombres | 1 | Ya cargada, ID 75; nueva URL y PDF diferente |
| Ley Municipal | 1 | Ya cargada, ID 139; nueva URL, PDF idéntico por SHA-256 |
| Ley de Mecanismos Alternativos de Solución de Controversias | 1 | Único ordenamiento nuevo faltante fuera de las exclusiones fiscales; cargado como ID 140 |

Las exclusiones originales constan en `Nayarit/catalogo/exclusiones.json`: se excluyó la sección 4 completa, no solo los ingresos municipales. Las tres fe de erratas son las de **Compostela, San Pedro Lagunillas y Santiago Ixcuintla**. No se presentan como tres leyes independientes. La relación completa de los 25 PDF excluidos aparece abajo.

Los tres archivos archivados que no coinciden con el catálogo vigente corresponden a 75, 139 y 78. El 78 se trasladó a Ordenamientos Abrogados y no representa otra ley vigente faltante.

El **ID 133**, Reglamento Interior de la Auditoría Superior, sigue como pendiente conocido: el catálogo muestra el título, pero no ofrece PDF ni Word. No forma parte de los 163 enlaces PDF y no se oculta al declarar un único nuevo faltante con enlace.

## Otro desfase detectado: ID 75

El archivo `igualdad_entre_mujeres_y_hombres_ley_de-.pdf` es distinto por contenido al archivado. Su encabezado declara **última enmienda de 18 de septiembre de 2026**, frente a **29 de abril de 2024** en la versión del acervo. Queda registrado en `PENDIENTES.md` para descarga de ambos formatos, conversión y versionado en una tarea posterior. No se modificó el ID 75.

El PDF de la Ley Municipal `municipal_para_el_estado_de_nayarit_ley-1.pdf` coincide exactamente por SHA-256 con el del ID 139. No se modificó ese ordenamiento.

## ID 78: texto histórico conservado

Se verificó que tanto el PDF como el Word de la carpeta de abrogados son **idénticos por SHA-256** a los archivados. Por tanto, se conserva la misma versión, originales, fecha de descarga y `texto.md`. Solo se corrigen procedencia y estado documentado:

- `urls.pdf`, `urls.word`, `url_pdf` y `url_word` apuntan a la carpeta `ordenamientos_abrogados`, leída del catálogo. Las URL anteriores quedan en `procedencia_urls`.
- `estado_vigencia: "abrogada"`, `abrogada: true`, `estatus` explicativo y `abrogada_por` apuntan a Nayarit/140 con nombre, versión y evidencia.
- `abrogacion` conserva la regla de entrada en vigor y el régimen transitorio. No se inventa un número de decreto ni una fecha calendario que no esté impresa: esos campos quedan null con incidencia.
- La vigilancia lee las nuevas URL desde metadata; se verificaron las descargas correctas de ambos originales. El 78 conserva `actual` y sus artículos en los índices para consulta histórica.

## ID 140: nueva ley

**Ley de Mecanismos Alternativos de Solución de Controversias del Estado de Nayarit.** Se asigna el siguiente ID local libre, 140, sin renumerar los anteriores ni confundirlo con el ordinal 76 del catálogo web. PDF y DOCX descargados individualmente desde los enlaces del catálogo y archivados por contenido.

La página 1 imprime publicación en la **Sección Décima Tercera del Periódico Oficial, 22 de octubre de 2026**. No imprime número de decreto ni última reforma identificable: null con incidencia.

La página PDF 85 contiene:

- Primero transitorio: entra en vigor al día siguiente de su publicación.
- Segundo transitorio: abroga la Ley de Justicia Alternativa para el Estado de Nayarit, publicada el 23 de abril de 2011.
- Tercero transitorio: los procedimientos iniciados anteriormente en el Centro Estatal de Justicia Alternativa continúan con las disposiciones vigentes al momento de su inicio, hasta su conclusión.

`abroga` relaciona expresamente el nuevo ID 140 con el histórico 78, conserva la fecha de publicación de la ley abrogada y la evidencia literal. Esta relación no convierte el texto histórico en una norma aplicable indiscriminadamente: debe revisarse el tercero transitorio para los procedimientos previos.

## Conversión e índices

**89 páginas con texto extraíble, 153 artículos de cuerpo (1–153 sin huecos), 12 transitorios y cero secciones.** Se comprobó la conservación de caracteres no blancos, signos, cifras y listas contra Poppler en todas las páginas, y la correspondencia de los rótulos originales con el índice. Cotejo visual de páginas 1, 85 y 86 para título, publicación, abrogación y régimen transitorio. El Word también contiene los 153 artículos propios; los cuatro rótulos adicionales del contador bruto PDF son remisiones partidas por salto de línea (páginas 34, 38, 39 y 43), conservadas como cuerpo. No se aplicó OCR ni se corrigieron discrepancias Word/PDF o del doble lector; los originales y sus incidencias están conservados. El cotejo visual es una muestra, no una revisión integral de las 89 páginas.

Los índices se regeneraron solo para Nayarit. `rutas.json` muestra el estado de vigencia documentado y las relaciones 78↔140, además de enlazar sus metadata. La presencia de `actual` selecciona versión, no afirma vigencia jurídica.

| Conteo | Antes | Después | Incremento |
|---|---:|---:|---:|
| Ordenamientos con versión | 138 | 139 | 1 |
| Artículos de cuerpo | 16,803 | 16,956 | 153 |
| Transitorios | 2,492 | 2,504 | 12 |
| Entradas | 19,295 | 19,460 | 165 |

Las **19,295 entradas de los 138 ordenamientos previos permanecen idénticas**, incluido el histórico ID 78. [Evidencia de regresión](justicia-alternativa-regresion.json). Las relaciones y el estado se agregan a rutas sin alterar el texto ni los rangos del articulado anterior.

Originales y extracciones conservados localmente y en el respaldo de conversión, conforme a la exclusión de binarios del repositorio. Markdown, metadata, validación, catálogo, índices y reportes se publican en `nayarit-justicia-alternativa`, con PR en borrador y sin merge.

## Los 25 PDF fiscales excluidos

- [Ley de Ingresos del Estado Libre y Soberano de  Nayarit](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_de_ingresos_del_estado_libre_y_soberano_de_nayarit_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Acaponeta](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_acaponeta_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Ahuacatlán](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_ahuacatlan_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Amatlán de Cañas](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_amatlan_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Bahía de Banderas](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_bahia_de_banderas_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Compostela](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_compostela_2026.pdf)
- [Fe de erratas — Ley de Ingresos para la Municipalidad de Compostela](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/fe_erratas_ley_ingresos_compostela.pdf)
- [Ley de Ingresos para la Municipalidad del Nayar](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_del_nayar_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Huajicori](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_Ingresos_huajicori_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Ixtlán del Río](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_ixtlan_del_rio_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Jala](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_jala_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Rosamorada](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_rosamorada_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Ruíz](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_ruiz_2026.pdf)
- [Ley de Ingresos para la Municipalidad de San Blas](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_san_blas_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Santa María del Oro](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_santa_maria_del_oro_2026.pdf)
- [Ley de Ingresos para la Municipalidad de San Pedro Lagunillas](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingreos_san_pedro_lagunillas_2026.pdf)
- [Fe de erratas — Ley de Ingresos para la Municipalidad de San Pedro Lagunillas](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/fe_erratas_ley_ingresos_san_pedro_lagunillas.pdf)
- [Ley de Ingresos para la Municipalidad de Santiago Ixcuintla](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_santiago_ixcuintla_2026.pdf)
- [Fe de erratas — Ley de Ingresos para la Municipalidad de Santiago Ixcuintla](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/fe_erratas_ley_ingresos_santiago_ixcuintla.pdf)
- [Ley de Ingresos para la Municipalidad de Tecuala](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_tecuala_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Tepic](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_tepic_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Tuxpan](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_tuxpan_2026.pdf)
- [Ley de Ingresos para la Municipalidad de Xalisco](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_xalisco_2026.pdf)
- [Ley de Ingresos para la Municipalidad de la Yesca](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_ingresos_la_yesca_2026.pdf)
- [Presupuesto de Egresos 2026](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/presupuesto_egresos_2026.pdf)

## URL de los ordenamientos relacionados

- ID 78: [PDF](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/ordenamientos_abrogados/justicia_alternativa_para_el_estado_de_nayarit_ley_de.pdf) · [Word](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/ordenamientos_abrogados/justicia_alternativa_para_el_estado_de_nayarit_ley_de.doc).
- ID 140: [PDF](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes/mecanismos_alternativos_de_solucion_de_controversias_del_estado_de_nayarit_ley_de.pdf) · [Word](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes/mecanismos_alternativos_de_solucion_de_controversias_del_estado_de_nayarit_ley_de.docx).
