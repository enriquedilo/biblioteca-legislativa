# Conversión semanal — 13 de octubre de 2026

Estado: borrador pendiente de cotejo. No incorporar a main todavía.

Fuente: vigilancia/reporte.md del commit ffb0858, reporte de 12 de octubre de 2026. SHA-256: b6c44a04d1b232d78b92a1441a182dbfe183f501b3c6e581ee690a1cbf42865c

Se conservaron las versiones anteriores y seis originales en respaldo local permanente. Ningún original ni SQLite se publica. Sin OCR. Las 322 páginas conservan los caracteres no blancos de la extracción. Esta comprobación no sustituye cotejo visual del PDF.

## Sinaloa — 7 Código Penal

188 páginas. Añadidos: ['172 BIS H', '172 BIS I', '274 BIS F']; eliminados: []; diferencias por rango de artículo: ['172 BIS', '172 BIS D', '240', '241', '273', '274 BIS E'].

La comparación omite espacios, marcadores de página y encabezados repetidos reconocidos. Los rangos pueden incluir títulos o notas contiguas: la lista señala diferencias textuales, no certifica que todos esos artículos hayan sido reformados. El diff completo conserva el contexto de los transitorios y decretos; su correspondencia definitiva está pendiente, sin emparejar ordinales repetidos a ciegas.

Campos/incidencias: abroga, po_publicacion.edicion, reformas, ultima_reforma.edicion.

## Sinaloa — 55 Ley de los Derechos de Niñas, Niños y Adolescentes

92 páginas. Añadidos: ['13 BIS', '27 BIS 1', '27 BIS 10', '27 BIS 11', '27 BIS 12', '27 BIS 13', '27 BIS 2', '27 BIS 3', '27 BIS 4', '27 BIS 5', '27 BIS 6', '27 BIS 7', '27 BIS 8', '27 BIS 9', '67 BIS 1', '67 BIS 2', '67 BIS 3', '81 BIS 1']; eliminados: []; diferencias por rango de artículo: ['11 BIS', '13', '27 BIS', '53', '67 BIS', '81 BIS', '83', '99'].

La comparación omite espacios, marcadores de página y encabezados repetidos reconocidos. Los rangos pueden incluir títulos o notas contiguas: la lista señala diferencias textuales, no certifica que todos esos artículos hayan sido reformados. El diff completo conserva el contexto de los transitorios y decretos; su correspondencia definitiva está pendiente, sin emparejar ordinales repetidos a ciegas.

Campos/incidencias: po_publicacion.edicion, reformas, ultima_reforma.edicion.

## Nayarit — 73 Ley de Gobierno Digital para el Estado de Nayarit

42 páginas. Añadidos: []; eliminados: []; diferencias por rango de artículo: ['1', '2', '5', '6', '8', '9', '10', '11', '12', '13', '14', '15', '16', '18', '20', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '36', '38', '39', '40', '41', '43', '46', '47', '49', '50', '53', '54', '55'].

La comparación omite espacios, marcadores de página y encabezados repetidos reconocidos. Los rangos pueden incluir títulos o notas contiguas: la lista señala diferencias textuales, no certifica que todos esos artículos hayan sido reformados. El diff completo conserva el contexto de los transitorios y decretos; su correspondencia definitiva está pendiente, sin emparejar ordinales repetidos a ciegas.

Campos/incidencias: abroga, decreto_numero, po_publicacion.edicion, po_publicacion.numero, reformas[].decreto, reformas[].po_numero, ultima_reforma.edicion, ultima_reforma.numero.

## Pendientes y controles

- Nayarit 73: discrepancias en secuencia de cifras entre lectores PDF y diferencias Word/PDF, documentadas en validacion.json; no se reparó el texto.
- Sinaloa 7 y 55: encabezados de reformas requieren lectura manual; reformas permanece vacío, sin inferir una cronología. Cotejo visual pendiente.
- Se corrigió la lectura literal de publicación de Nayarit 73: Sección Décima Tercera, 13 de junio de 2022, página 1.
- Se corrigió el generador para no interpretar el día de una fecha después de P.O. como número de edición. Esto corrige también notas derivadas de otros índices de las dos entidades regeneradas; no cambia sus textos ni versiones.
- Regenerados articulado, FTS, remisiones y rutas de Sinaloa y Nayarit.
- Federal 1, 396 y 441: fuera del alcance original de la automatización; convertidos el 14 de octubre por ampliación expresa del usuario. Véase el informe del 14 de octubre.
- No se declara cotejo visual ni vigencia jurídica. El PR permanece en borrador hasta resolver los controles pendientes.

Actualización 14 de octubre: 172 Bis D queda identificado como encabezado propio, conservando «Derogado» sin agregar punto. La ausencia anterior era del índice, no del original. Los federales 1, 396 y 441 ya se convirtieron por instrucción expresa posterior: véase ../2026-10-14/reporte.md.
