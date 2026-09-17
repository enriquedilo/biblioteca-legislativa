# Piloto corregido v2

**Sustituye las conclusiones sobre remisiones y clasificación del piloto inicial.** Las tres remisiones de las páginas 128, 133 y 163 de la Constitución permanecen ahora en el cuerpo de sus párrafos. Se revisaron y reprocesaron los cuatro documentos, sin encontrar ese patrón en los otros tres. Se verificaron de nuevo conservación integral, listas y cifras en 793 páginas. Ocho hashes y cuatro versiones sin cambios.

Los 139 nombres de catálogo están reconstruidos; el original del sitio se conserva en `nombre_catalogo_sitio`. Todos tienen `orden: estatal`, `regimen` y `tipo`; se elimina `ambito`. IDs, slugs y procedencias no cambian. Conversiones anteriores en `conversiones_anteriores/v1`.

[Informe estructurado de correcciones](PILOTO_CORREGIDO_V2.json). El cotejo léxico Word/PDF mantiene sus incidencias anteriores.

## Informe inicial (histórico; para clasificación y remisiones rige v2)

# Piloto de la Biblioteca Legislativa de Nayarit

**Piloto cerrado con incidencias documentadas.** Cuatro ordenamientos, 793 páginas con capa de texto y 29 páginas cotejadas visualmente. La conservación PDF → Markdown pasa en todas las páginas. La equivalencia léxica Word/PDF no queda aprobada: se detectaron diferencias y no se repararon. No se ha iniciado ningún lote posterior.

## Resultado por documento

| ID propio | Ordenamiento | Páginas | Inicios de lista conservados | Marcadores numéricos Word / PDF | Sin texto |
|---|---|---:|---:|---:|---:|
| 1 | [Código Civil para el Estado de Nayarit](../ordenamientos/1/actual/texto.md) | 437 | 1009 | 2965 / 2965 | 0 |
| 5 | [Constitución Política del Estado Libre y Soberano de Nayarit](../ordenamientos/5/actual/texto.md) | 181 | 653 | 155 / 158 | 0 |
| 12 | [Ley Arancelaria de los Abogados para el Estado de Nayarit](../ordenamientos/12/actual/texto.md) | 15 | 44 | 39 / 39 | 0 |
| 139 | [Ley Municipal para el Estado de Nayarit](../ordenamientos/139/actual/texto.md) | 160 | 963 | 288 / 288 | 0 |

Los marcadores son resultados del detector heredado, no un cómputo jurídico de artículos. En la Constitución, los tres adicionales son remisiones que quedaron al inicio de renglón: artículo 131 en páginas 128 y 133; artículo 105 en página 163. Se preservan los resultados originales para hacer visible esa limitación.

## Controles y límites

- SHA-256 de los ocho originales comprobado contra las descargas; versión calculada con el mismo procedimiento de Sinaloa.
- 793 marcadores `<!-- PAGINA_PDF: n -->`, uno por página. Se conserva también el índice impreso dentro de cada PDF, sin crear un índice de búsqueda ni archivos de articulado.
- Igualdad de todos los caracteres no blancos, incluidos signos y cifras, entre cada página extraída y su Markdown desprovisto del formato añadido. Solo se retiran números aislados de paginación en los bordes, igual que en Sinaloa, y se registra cada retirada.
- 2,669 inicios de lista conservados en orden, incluidas fracciones con la grafía «I.-». Los encabezados, ordinales y cola completa de transitorios se conservan por el mismo control integral.
- Secuencia de cifras coincidente entre Poppler y pypdf en las 793 páginas, incluida la paginación en ambos lectores. Se mantiene además el resultado del control original de Sinaloa.
- Ley Arancelaria, páginas 10–15: el número de página está superpuesto al encabezado. El control heredado con retirada de paginación falla por retirar el número en un solo lector; la comparación simétrica coincide. La observación está confirmada visualmente. No se repara la superposición ni se altera la extracción.
- La comparación léxica Word/PDF no coincide en los cuatro: el PDF repite encabezados y el lector DOC incluye campos TOC/HYPERLINK/PAGEREF. La lista completa de diferencias léxicas permanece en `validacion.json`; otras diferencias no se dan por resueltas ni se declara equivalencia sustantiva de ambas fuentes.
- No hay páginas sin texto extraíble en el piloto. No se ejecutó OCR.

## Campos incompletos: solo lo impreso

En los cuatro documentos, `po_publicacion.numero` y `po_publicacion.edicion` quedan null. `ultima_reforma` mantiene los campos `numero`, `edicion` y `fecha`: solo la fecha está impresa. Las notas de reformas que no imprimen número de Periódico Oficial o decreto mantienen esos valores null. Las secciones de publicación se guardan literalmente, sin convertirlas en números.

| Documento | Publicación impresa | Última reforma/enmienda impresa | Incidencias particulares |
|---|---|---|---|
| Código Civil | Segunda Sección, 22 de agosto de 1981 | 17 de diciembre de 2025 | Decreto 6433. `abroga[0].fecha` null: el 1 de julio de 1938 es entrada en vigor del ordenamiento abrogado, no fecha de publicación. Una nota imprime «8 DE JUNI0 DE 2011», con cero, en página 78: su fecha normalizada queda null. |
| Constitución | 17, 21, 24 y 28 de febrero y 3, 7, 10 y 14 de marzo de 1918 | 9 de julio de 2026 | `decreto_numero` y `po_publicacion.seccion` null. `po_publicacion.fecha` null porque hay varias fechas impresas y el campo de Sinaloa es escalar; el pasaje completo está en la evidencia. `abroga: []`: no se identificó abrogación expresa de un ordenamiento. Una nota en página 78 imprime «19 E MAYO DE 2022»: fecha normalizada null. |
| Ley Arancelaria | Sección Décima, 4 de septiembre de 2010 | 8 de noviembre de 2016 | `decreto_numero` null: el decreto de expedición no imprime número. Abroga el Arancel de los Abogados, decreto 5991, publicado el 21 de enero de 1978; número de P.O. null. |
| Ley Municipal | Segunda Sección, 4 de agosto de 2001 | 14 de mayo de 2024 | Decreto 8345. Abroga los decretos 7295 y 7281; el segundo no trae título oficial, por lo que `abroga[1].nombre` queda null. Fechas impresas: 15 de septiembre y 28 de marzo de 1990, respectivamente; números de P.O. null. |

`reformas` contiene notas impresas distintas por página, con evidencia y página en `validacion.json`; no es un recuento de decretos únicos ni una cronología reconstruida. Los diez números de decreto impresos junto a encabezados de P.O. de la Constitución se conservan; no se propagan a otras notas por coincidencia de fechas. Las erratas se detectan y se conservan, no se corrigen.

## Estructura, identidad y continuación

La carpeta real es `Biblioteca_Legislativa/Nayarit`, hermana de `Biblioteca_Legislativa/Sinaloa`. Cada ordenamiento tiene `actual.json`, enlace relativo `actual/`, y `versiones/<hash>/` con `original.pdf`, **`original.doc` autorizado por el usuario**, `texto.md`, `extraccion.txt`, `metadata.json` y `validacion.json`. No se fabrica un DOCX ni se renombra un binario DOC.

Se verificaron los mismos campos base y tipos de Sinaloa; solo se añaden los cinco campos solicitados y `po_publicacion.seccion`. Las herramientas propias están en `../bin/nayarit/` respecto de la carpeta Nayarit, sin modificar las herramientas de Sinaloa. El enlace de acceso en los outputs de esta tarea apunta a la carpeta real y no contiene una segunda copia de la biblioteca.

Catálogo congelado: 139 identidades propias, con ID entero persistente y slug derivado del nombre. La numeración de presentación de la página no se usa como identidad. La Ley de Fiscalización aparece en dos secciones y mantiene una identidad, con las dos procedencias registradas en catálogo y ámbito `congreso`. Se excluyen las secciones solicitadas, los dos códigos rotulados abrogados dentro de Códigos y el enlace auxiliar «Reformas Constitucionales». El Reglamento Interior de la Auditoría Superior está en catálogo pero no tiene enlace PDF/Word reconocido en la instantánea: queda pendiente, sin descargarlo en el piloto.

Quedan 135 documentos en 14 lotes (13 de diez y uno de cinco). `AVANCE.md` y `reportes/avance_lotes.json` guardan el estado. Los documentos sin texto o sin original se registran como pendientes y permiten cerrar el lote; no se les aplica OCR. **Detenido antes del lote 1 para presentar este resultado.**

## Evidencia de revisión

- ID 1: páginas [1](muestra_visual/1/pagina-1.png), [78](muestra_visual/1/pagina-78.png), [100](muestra_visual/1/pagina-100.png), [414](muestra_visual/1/pagina-414.png), [424](muestra_visual/1/pagina-424.png), [426](muestra_visual/1/pagina-426.png), [437](muestra_visual/1/pagina-437.png). [Metadata](../ordenamientos/1/actual/metadata.json) · [Validación](../ordenamientos/1/actual/validacion.json).
- ID 5: páginas [1](muestra_visual/5/pagina-1.png), [40](muestra_visual/5/pagina-40.png), [78](muestra_visual/5/pagina-78.png), [118](muestra_visual/5/pagina-118.png), [128](muestra_visual/5/pagina-128.png), [133](muestra_visual/5/pagina-133.png), [163](muestra_visual/5/pagina-163.png), [170](muestra_visual/5/pagina-170.png), [181](muestra_visual/5/pagina-181.png). [Metadata](../ordenamientos/5/actual/metadata.json) · [Validación](../ordenamientos/5/actual/validacion.json).
- ID 12: páginas [1](muestra_visual/12/pagina-1.png), [5](muestra_visual/12/pagina-5.png), [10](muestra_visual/12/pagina-10.png), [11](muestra_visual/12/pagina-11.png), [12](muestra_visual/12/pagina-12.png), [13](muestra_visual/12/pagina-13.png), [14](muestra_visual/12/pagina-14.png), [15](muestra_visual/12/pagina-15.png). [Metadata](../ordenamientos/12/actual/metadata.json) · [Validación](../ordenamientos/12/actual/validacion.json).
- ID 139: páginas [1](muestra_visual/139/pagina-1.png), [60](muestra_visual/139/pagina-60.png), [142](muestra_visual/139/pagina-142.png), [145](muestra_visual/139/pagina-145.png), [160](muestra_visual/139/pagina-160.png). [Metadata](../ordenamientos/139/actual/metadata.json) · [Validación](../ordenamientos/139/actual/validacion.json).

[Verificación de esquema](VERIFICACION_ESQUEMA.json) · [Resultados estructurados](piloto_resultados.json) · [Avance](../AVANCE.md) · [Catálogo](../catalogo/leyes-estatales.json)
