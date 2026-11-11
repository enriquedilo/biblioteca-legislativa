# Acervo IEEN

Normatividad del Instituto Estatal Electoral de Nayarit. Es el cuarto acervo
de la biblioteca y sigue la misma estructura que Sinaloa, Nayarit y Federal:
`ordenamientos/<id>/versiones/<hash>/` con el enlace `actual` apuntando a la
versión vigente, e `indices/` como capa derivada regenerable.

## De dónde sale

`bin/catalogo_ieen.py` lee las dos páginas de normatividad del Instituto y
escribe `IEEN/catalogo/normatividad.json`. Ese archivo es la fuente del
acervo: dice qué documentos hay, cuál es la versión vigente de cada uno y
qué acuerdos lo han reformado.

La versión vigente de un reglamento suele ser el anexo del acuerdo que lo
reformó, no un PDF propio. **El sitio no lista los anexos en orden
constante**: unos van del más viejo al más nuevo y otros al revés. La versión
vigente se elige por fecha, nunca por posición en la lista.

## Numeración

El identificador es estable y viene del catálogo, no del orden de carga:

- `normatividad-N` → id **N** (1 a 51)
- `interna-N` → id **100 + N** (101 a 121)

Hay huecos a propósito. Siete documentos de «Legislación Local» del catálogo
del IEEN son leyes del Congreso de Nayarit que la biblioteca ya tiene por su
fuente oficial, y no se duplican: los ids 1, 2, 3, 4, 5, 7 y 8 quedan vacíos,
y `metadata` del catálogo dice a qué ordenamiento de Nayarit corresponde cada
uno. El id 6, el Compendio Electoral 2021, queda fuera por ser una
recopilación de esas mismas leyes en un PDF de 207 MB.

Volver a correr el extractor siempre devuelve el mismo id para el mismo
documento. Si el Instituto da de alta uno nuevo, toma el número que le asigne
el catálogo y los demás no se mueven.

## Secciones

Un solo acervo, con el campo `seccion` en `metadata.json`:

- `electoral` — los 43 reglamentos y lineamientos de `/normatividad/IEEN`.
- `interna` — los 21 estatutos, manuales, procedimientos y lineamientos
  administrativos de `/normatividad/Interna`.

No se parten en dos acervos: una sola capa de índices y una sola entrada en
la vigilancia. Cuando una consulta sea estrictamente electoral, se filtra por
sección.

## Metadata

Además de los campos que ya usan los otros acervos —`id`, `nombre_catalogo`,
`nombre_oficial`, `fuente`, `urls`, `fecha_descarga`, `hash_sha256`,
`version`, `validacion`, `tipo`—, este acervo guarda:

- `seccion`: `electoral` o `interna`.
- `acuerdo`: el acuerdo del Consejo o de la Junta que aprobó la versión
  vigente, por ejemplo `IEEN-CLE-015/2025`.
- `reformas`: la cadena de acuerdos que han reformado el ordenamiento, cada
  uno con su fecha y su URL. **No se convierten**: quedan anotados para poder
  promover una versión anterior el día que haga falta, sin rehacer nada.

## Páginas sin capa de texto: portada e interior no pesan igual

Varios documentos del Instituto traen la **portada como imagen** —membrete,
escudo y título— aunque el cuerpo esté perfectamente extraíble. Frenar la
carga por eso dejaba fuera normatividad vigente y completa, así que el
control distingue:

- **Si lo único sin texto extraíble es la portada**, el documento **se
  promueve**. La incidencia se registra en `validacion.json` y el título se
  transcribe por cotejo visual a `metadata.json`, marcado como tal. Debe
  comprobarse en el cotejo visual de esa página que no lleva texto normativo:
  si la portada arranca el articulado, no aplica esta excepción.
- **Si falta texto en cualquier página interior**, el documento **no se
  promueve**: ahí sí se pierde contenido normativo. Queda con su PDF, su
  extracción diagnóstica y su metadata, sin enlace `actual`, fuera de los
  índices y de la búsqueda.
- **Nunca se aplica OCR.** La biblioteca no mezcla texto de la fuente con
  texto generado por máquina. Un documento que no se puede leer se declara
  ilegible y se cita su PDF.

Casos del lote 3: los ids 40, 42 y 47 entran por la primera regla; el 45
—escaneo sin texto en ninguna de sus cinco páginas— y el 48 —sin texto en las
páginas 7, 18 y 20, que sí llevan contenido— quedan fuera por la segunda.

## Lo que no está aquí

Los acuerdos del Consejo Local Electoral. Son cientos por año y son materia
de consulta puntual, no de acervo.

## Documentos de otro emisor

El ID 38 pertenece al INE y se carga por el catálogo IEEN. Su metadata conserva
`emisor: "INE"` y `deduplicacion` con clave de procedencia `INE/CG517/2020:A1`,
`evitar_duplicado: true` y referencia existente IEEN/38. Al incorporar el acervo
INE, cotejar nombre, clave y hash y reutilizar/enlazar esa versión si coincide;
una versión diferente se conserva por contenido. `id_destino` queda null hasta
comprobar la correspondencia. La clave de archivo no sustituye un acuerdo no
impreso ni la fuente de descarga.
