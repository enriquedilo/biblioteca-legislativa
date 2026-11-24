# Conversión semanal — 24 de noviembre de 2026

Fuente: vigilancia/reporte.md, corrida 2026-11-24 03:22 UTC, conservada como reporte_fuente.md. Base main e37266b5435f9e02936b4bdf56f19eceeaff2fb3. Sin PR abierto al iniciar.

## Nayarit 5 — Constitución Política del Estado Libre y Soberano de Nayarit

El PDF cambió de hash y pasó de 185 a 188 páginas. No se detectaron cambios de contenido en los 144 artículos de cuerpo y 436 transitorios: cero añadidos, cero eliminados, cero modificados. Se mantienen 344 notas de reforma. La fecha impresa de última enmienda sigue siendo 6 de noviembre de 2026. Se versiona el documento cambiado, sin declarar nueva reforma.

Comparación entrada por entrada reproducible en comparar.py y comparacion.json (arreglo vacío). Se identificaron los transitorios por fecha de P.O., ordinal y ocurrencia. Solo para comparar se ignoraron espacios, encabezados repetidos, equivalencias Unicode NFC y la tabla editorial final; no se alteraron estos elementos en el texto conservado. Las primeras diferencias aparentes en transitorios de 1994 y 2007 eran saltos en el rótulo de contexto; las de 2025, representación de acentos. La tabla editorial final y los rangos de páginas se desplazaron. El cotejo no sustituye una revisión visual integral.

Nueva versión: 38ac1f8905a52277510141015506bd49329cbdce6073e0a8b7aa0049289e6d7b.
PDF SHA-256: f5b3ddff327d4ba4489392e0ef4fae4e50c9e8b2f033acfd30d315cc1bdd33c7.
Word SHA-256, sin cambio: 29ea7ddf9b68c7cc2e4bbc570ec8721fa0db6f33ad8a938e88782a8bb4c76892.

## Controles e incidencias

Conservación estricta de todos los caracteres no blancos entre extracción y Markdown en 188 páginas; conservación de listas/fracciones y cifras contrastadas con segundo lector PDF; 188 páginas con texto, sin OCR. Páginas 1 y 186 abiertas visualmente: portada, publicación seriada de 1918 y cinco transitorios de 6 de noviembre de 2026. No se cotejó visualmente todo el PDF.

El Word no coincide literalmente con el PDF: campos internos/tabla de contenido, encabezados y acentos; la incidencia queda registrada y no se reparó. La publicación original enumera ocho fechas de febrero/marzo de 1918, por lo que no se inventó una fecha escalar. Permanecen datos incompletos de decreto, número/edición/sección de publicación y referencias de reformas/abrogación; detalle en resultados.json y validacion.json. No confundir estos límites de metadata con fallos de conservación.

Índices regenerados para Nayarit; versión, rutas web, rangos y páginas comprobados. Se descartaron solo cambios de fecha de generación en 141 índices sin diferencia de contenido. Versiones anteriores intactas. Los originales y la extracción quedan respaldados permanentemente en la Mac bajo Documents/Codex/2026-09-14/construye-una-biblioteca-separada-de-la/respaldo-conversiones/2026-11-24/Nayarit/5. PDF, Word y SQLite excluidos de Git.

## Pendientes del reporte

- Sinaloa: errores de acceso de la vigilancia en IDs 28 (Word), 29–31 (PDF/Word), 32 (PDF), 34 (Word), 45 y 48 (PDF), 53 (Word), 75 (PDF), 85, 102 y 132 (Word). No prueban modificaciones; no convertidos.
- Nayarit 4 y 36: altas/bajas de enlaces en el catálogo, sin cambio de contenido confirmado; pendientes de revisión de fuente. No se ejecutó detección adicional ni se sustituyeron URLs por inferencia.
- Federal 13, 64, 155 y 219: archivos modificados, fuera del alcance Sinaloa/Nayarit de esta automatización. Federal 60: reemplazo de LIF pendiente. No procesados.

Publicación para cotejo en actualizacion/2026-11-24, PR borrador; sin merge ni actualización del acervo del clon principal.
