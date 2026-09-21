# Capa de índices — Federal

Índices **derivados** del acervo federal (compilación de la Cámara de Diputados).
No forman parte del acervo: se generan leyendo `Federal/ordenamientos/<id>/actual/`
y no modifican ningún original, Markdown, `metadata.json` ni hash. Si algo aquí se
corrompe o se duda de su contenido, se borra la carpeta y se regenera:

    python3 bin/indices.py todo --entidad Federal

En caso de discrepancia entre un índice y el `texto.md`, **manda el texto**.

## Aislamiento entre entidades

Cada entidad tiene su propia carpeta de índices y su propia base de datos. Una
consulta federal abre un archivo que no contiene un solo artículo estatal. El
derecho comparado se hace corriendo la misma pregunta en cada índice y
presentando los resultados por separado: **nunca se fusionan las tablas**.

## Qué contiene

- `articulos/<id>.json` — articulado de cada ordenamiento: número (incluidos Bis,
  Ter, series compuestas como `5 Bis 1`, ordinales latinos hasta Novodecies y
  numeración con coma de millar), tipo `cuerpo` / `transitorio`, página del PDF,
  rango de líneas y notas de reforma del artículo.
- `articulado_resumen.json` — conteos por ordenamiento.
- `biblioteca.db` — SQLite con FTS5 a nivel de artículo, insensible a acentos,
  más una tabla `leyes`. No se versiona: se regenera.
- `remisiones.json` — menciones nominales entre ordenamientos federales.
- `rutas.json` — id, nombre y ruta resuelta del `texto.md` vigente de cada
  ordenamiento (útil cuando el enlace `actual/` no se resuelve, p. ej. por HTTP).

## Cifras de esta generación (acervo cerrado)

- 447 de 453 ordenamientos catalogados. Seis no tienen versión promovida.
- 58,794 artículos de cuerpo y 15,698 transitorios.
- 35,344 notas de reforma DOF ancladas a su artículo.
- 74,492 artículos en el índice de búsqueda; 6,678 aristas de remisión.

## Nombres de reglamentos

28 reglamentos traen en el catálogo la fecha DOF en lugar del nombre
(«DOF 20/04/2015»). En los índices el nombre se toma del encabezado de página
de la propia compilación («REGLAMENTO DE LA LEY ADUANERA») y se marca
`nombre_derivado_de_portada`. El `metadata.json` del acervo no se modifica.

## Seis ordenamientos sin versión promovida

Están catalogados y sus originales se conservan con su SHA-256, pero no tienen
`actual/` ni entran en los índices, porque su conversión no superó el control de
conservación o el PDF no trae texto. Detalle en
`Federal/reportes/pendientes-finales.json`. No se les aplicó OCR.

| ID | Ordenamiento | Motivo |
|----|--------------|--------|
| 372 | Reglamento de la Ley del Servicio Militar (1942) | conversión altera contenido |
| 413 | Reglamento de la LGS en Materia de Control Sanitario de Actividades, Establecimientos, Productos y Servicios (1988) | conversión altera contenido |
| 414 | Reglamento de la LGS en Materia de Control Sanitario de la Disposición de Órganos, Tejidos y Cadáveres (1985) | conversión altera contenido |
| 416 | Reglamento de la LGS en Materia de Investigación para la Salud (1987) | conversión altera contenido |
| 444 | Reglamento de la Ley Federal de Ganadería (1955) | PDF sin capa de texto |
| 446 | Reglamento del artículo 5º constitucional (1945) | conversión altera contenido |

Si la consulta toca uno de estos, dilo: el texto no está en la biblioteca y el
PDF original es la única fuente.

## Otros límites

- **Reglamento de la LGS en Materia de Sanidad Internacional (ID 419)**: la
  compilación oficial salta del artículo 22 al 24. El 23 no existe en la fuente.
- Notas no ancladas: explicativas `Reforma DOF …:`, declaratorias de invalidez
  de la SCJN y la tabla arancelaria de la LIGIE (ID 78).
- Las notas son anotaciones del compilador, no tabla oficial de reformas. Las
  remisiones son detección léxica. Ningún índice declara vigencia jurídica.
