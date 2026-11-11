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

## Páginas sin capa de texto: cuatro casos, uno solo impide cargar

«Página sin texto extraíble» significa cosas muy distintas, y tratarlas igual
dejaba fuera documentos completos. El control las clasifica:

| Caso | Qué es | Qué se hace |
|---|---|---|
| **Portada** | Membrete, escudo y título como imagen | Se promueve. El título se transcribe por cotejo visual a `metadata.json`, marcado como tal |
| **Página en blanco** | No hay nada que extraer | Se promueve. No hay contenido que perder |
| **Página gráfica** | El contenido *es* la imagen: un logotipo, una composición de diseño | Se promueve. El gráfico se pierde en cualquier conversión a texto; retener el documento entero no lo rescata y además pierde el texto de las demás páginas |
| **Texto normativo como imagen** | Articulado, tablas o instrucciones legibles a la vista pero no extraíbles | **No se promueve.** Aquí sí se pierde contenido |

Las tres primeras se registran como incidencia en `validacion.json`, con el
número de página y el motivo. El documento entra al acervo y a la búsqueda.

La cuarta deja el documento con su PDF, su extracción diagnóstica y su
metadata, **sin enlace `actual`**, fuera de los índices y de la búsqueda. Si
una consulta lo toca, se dice que su texto no está en la biblioteca y se cita
su PDF.

La clasificación exige cotejo visual de la página que disparó el control: no
se deduce del conteo de caracteres. En la duda entre «gráfica» y «texto
normativo como imagen», manda la segunda.

**Nunca se aplica OCR.** La biblioteca no mezcla texto de la fuente con texto
generado por máquina. Un documento que no se puede leer se declara ilegible.

Casos resueltos con esta regla: entran los ids 40, 42 y 47 (portada), 105
(página final en blanco) y 103 (página de diseño en un manual de identidad
gráfica). Quedan fuera el 45 y el 104, escaneos sin texto en ninguna página,
y el 48 y el 106, que pierden texto normativo en páginas interiores.

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
