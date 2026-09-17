# Capa de índices — Sinaloa

Índices **derivados** de la biblioteca de Sinaloa. No forman parte del acervo: se
generan leyendo `Sinaloa/ordenamientos/<id>/actual/` y no modifican ningún
original, Markdown, `metadata.json` ni hash. Si algo aquí se corrompe o se duda
de su contenido, se borra la carpeta y se regenera:

    python3 bin/indices.py todo --entidad Sinaloa

En caso de discrepancia entre un índice y el `texto.md`, **manda el texto**.

## Aislamiento entre entidades

Cada entidad tiene su propia carpeta de índices y su propia base de datos. Una
consulta a Sinaloa abre un archivo que no contiene un solo artículo de otra
entidad. El derecho comparado se hace corriendo la misma pregunta en cada índice
y presentando los resultados por separado: **nunca se fusionan las tablas**.

## Qué contiene

- `articulos/<id>.json` — articulado de cada ordenamiento: número (incluidos Bis,
  Bis-A, Ter, y ordinales en letra en leyes antiguas), tipo `cuerpo` /
  `transitorio`, página del PDF, rango de líneas y notas de reforma del artículo.
- `articulado_resumen.json` — conteos por ordenamiento.
- `biblioteca.db` — SQLite con búsqueda de texto completo (FTS5) a nivel de
  artículo, insensible a acentos, más una tabla `leyes` con la metadata
  normativa.
- `remisiones.json` — menciones nominales entre ordenamientos de esta entidad,
  con el artículo donde ocurre cada una.

## Cifras de esta generación

- 151 ordenamientos, 18,910 artículos de cuerpo y 3,036 transitorios.
- 4,733 notas de reforma ancladas a su artículo, en 97 ordenamientos.
- 21,946 artículos en el índice de búsqueda; 774 aristas de remisión.

## Consulta

El montaje de carpetas compartidas no admite el bloqueo de SQLite: copia
`biblioteca.db` a almacenamiento local antes de consultarla. El generador ya lo
hace al construirla.

    sqlite3 /ruta/local/biblioteca.db \
      "SELECT ley, articulo, pagina FROM articulos
       WHERE articulos MATCH 'perito AND arancel' LIMIT 20;"

## Límites

- Las **notas de reforma** son anotaciones impresas por el compilador del
  Congreso. No son una tabla oficial y pueden faltar en artículos efectivamente
  reformados.
- Las **remisiones** son detección léxica de nombres: no distinguen la remisión
  normativa de la cita incidental y no capturan las genéricas.
- Ningún índice declara vigencia jurídica.
