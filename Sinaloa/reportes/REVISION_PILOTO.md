# Revisión terminada — biblioteca piloto de Sinaloa

**Resultado: los cuatro Markdown quedaron verificados como conversiones de los originales descargados.** Se corrigió la extracción, se conservaron originales y conversiones anteriores y se actualizaron el índice y la metadata.

| Ordenamiento | Páginas del PDF | Páginas cotejadas visualmente | Resultado |
|---|---:|---|---|
| Código Civil | 248 | 1, 6, 64, 83, 237, 240, 248 | Conversión verificada |
| Constitución | 167 | 1, 2, 109, 134, 167 | Conversión verificada |
| Gobierno Municipal | 70 | 1, 38, 61, 62, 70 | Conversión verificada |
| Profesiones | 57 | 1, 50, 55, 57 | Conversión verificada |
| **Total** | **542** | **21 páginas seleccionadas** | **Cuatro documentos** |

## Qué se comprobó

- Las huellas SHA-256 de los ocho originales coinciden con las registradas. Los originales no fueron modificados.
- Se procesaron las 542 páginas. La página 6 del Código Civil está en blanco también en el PDF, confirmado visualmente; no falta texto por esa causa.
- Los identificadores de artículos detectados en los cuatro Word coinciden con los de los PDF, incluidos los sufijos bis y sus variantes. Los recuentos de apariciones pueden diferir por referencias y reproducciones dentro de reformas; no se confundieron con artículos faltantes.
- El cotejo léxico de Word y PDF coincide en contenido y orden después de separar dos notas al pie y normalizar las diferencias de presentación documentadas. No quedaron diferencias léxicas sin explicar en ese control.
- Dos lectores independientes de PDF coinciden en la secuencia de cifras de cada página, descontando la paginación. Esto resuelve números que la primera extracción había separado, por ejemplo el artículo 1135 del Código Civil.
- El Markdown conserva, página por página, todos los caracteres no blancos del texto PDF extraído, incluidos signos y cifras. Sólo se añade formato Markdown y se retira la paginación aislada en los bordes, registrada en el control.
- Se verificó la conservación y el orden de 1,898 inicios de listas detectados en los PDF. El control de texto completo cubre también las continuaciones de esas fracciones e incisos.
- Se incluyeron completos los bloques de transitorios, transitorios de reformas, notas, firmas y anexos presentes en cada original. Hay dos encabezados de secciones transitorias en Civil, Constitución y Gobierno Municipal, y uno en Profesiones; ésta conserva sus seis transitorios originales.
- Se repitió la conversión: los cuatro Markdown resultaron idénticos y los ocho originales conservaron sus huellas.

## Problemas corregidos o explicados

**Numeración automática de Word.** Su lector omitía fracciones y apartados o los sustituía por viñetas. Se genera el Markdown desde el PDF, conservando las etiquetas impresas.

**Saltos de línea y cifras partidas.** Se sustituyó la extracción inicial por una que respeta la disposición de página. Se separaron los encabezados de artículos y se recompusieron los párrafos sin alterar palabras, cifras ni signos.

**Falsos artículos faltantes.** Por ejemplo, el artículo 156 mencionado en Profesiones es una referencia a la Ley de Educación, no un artículo propio que se hubiera perdido. También se reconocen las abreviaturas «ART.» y «Art.».

**Notas al pie.** El lector de Word coloca al final la nota histórica de la primera página de la Constitución y la nota de publicación de Gobierno Municipal. El Markdown conserva la ubicación por página del PDF.

**Encabezados espaciados.** «CONSIDERANDO» está presente en ambos formatos; en la extracción Word aparece con espacios entre letras. No falta ese encabezado.

**Defectos del original.** Algunas menciones del Periódico Oficial en el Código Civil aparecen como «AEl … @» en el PDF. Se conservan, sin corrección editorial silenciosa. Para el cotejo con Word únicamente se equiparó esa representación de comillas. Del mismo modo se normalizaron «IVLos/IV Los», «BisA/Bis A» y los campos de paginación de Word sólo para comparar; estas normalizaciones no sustituyen palabras del Markdown.

## Alcance y límites

Esta revisión acredita el resultado de los controles de **integridad de conversión de estas copias**. Incluye controles automáticos sobre todas las páginas y cotejo visual de una muestra dirigida; no es una lectura jurídica ni un cotejo visual exhaustivo de las 542 páginas. La comparación léxica Word/PDF excluye etiquetas de listas que el lector Word no conserva; esas etiquetas se verifican por separado entre PDF y Markdown.

No se volvió a consultar el portal durante esta revisión local, ni se comprobó si existe una reforma posterior en el Periódico Oficial. Las fechas registradas siguen siendo las declaradas en los originales descargados: Civil, 11 de marzo de 2022; Constitución, 26 de agosto de 2026; Gobierno Municipal, 17 de agosto de 2026. Profesiones declara publicación de 27 de septiembre de 2019; no se le atribuye una última reforma inexistente en su encabezado.

La verificación del piloto no se hereda automáticamente a leyes nuevas o futuras versiones. Cada nueva conversión debe pasar sus controles.

## Dónde consultar

Abre el [índice actualizado](../INDICE.md). Cada carpeta de versión incluye `texto.md`, sus originales, `metadata.json` y `validacion.json` con el detalle por página. Las conversiones previas están en `conversiones_anteriores/v2`.

La revisión del piloto está cerrada. La siguiente etapa es ampliar la biblioteca al catálogo y revisar sus incidencias; la actualización periódica aún no está activada.
