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

## Cifras de esta generación (corte de lotes 1–35)

- 354 de 453 ordenamientos: leyes y códigos completos; 38 de 137 reglamentos.
- 47,517 artículos de cuerpo y 14,807 transitorios.
- 33,281 notas de reforma DOF ancladas a su artículo, en 269 ordenamientos.
- 62,324 artículos en el índice de búsqueda; 5,923 aristas de remisión.

## Nombres de reglamentos

28 reglamentos traen en el catálogo la fecha DOF en lugar del nombre
(«DOF 20/04/2015»). En los índices el nombre se toma del encabezado de página
de la propia compilación («REGLAMENTO DE LA LEY ADUANERA») y se marca
`nombre_derivado_de_portada`. El `metadata.json` del acervo no se modifica.

## Límites conocidos de este corte

- **Reglamento del Senado (ID 315)**: su articulado no está marcado en la
  conversión; el índice solo tiene 7 entradas espurias. Consultar el `texto.md`
  directamente.
- **Ordenanza General de la Armada (ID 312)**: los artículos 1,000 a 1,289 no
  están marcados; consultar el `texto.md`.
- **LGSMIME (ID 223)**: 118 aperturas de artículo sin marcar (formato de
  párrafos numerados). Además tiene `vigencia_recuperada`: la SCJN invalidó el
  decreto que la abrogaba.
- **Reglamento de la Ley Aduanera (ID 317)**: falta el artículo 88 en el
  articulado; pendiente de cotejo con el PDF.
- Notas no ancladas: explicativas `Reforma DOF …:`, declaratorias de invalidez
  de la SCJN y la tabla arancelaria de la LIGIE (ID 78).
- Las notas son anotaciones del compilador, no tabla oficial de reformas. Las
  remisiones son detección léxica. Ningún índice declara vigencia jurídica.
