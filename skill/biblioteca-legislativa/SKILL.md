---
name: "biblioteca-legislativa"
description: "Consulta las bibliotecas legislativas del usuario (Sinaloa, Nayarit, Federal y la normatividad del IEEN de Nayarit), en su Mac o desde el repositorio de GitHub cuando la Mac no esté disponible: localiza leyes, reglamentos, lineamientos, artículos, transitorios, aranceles, fórmulas e historial de reformas por artículo, y responde qué ordenamientos regulan una materia, con entidad, fuente, vigencia y fecha."
---

<!--
COPIA PUBLICADA. Generada el 13 de noviembre de 2026 a partir de la skill
instalada en la cuenta de Claude de su autor. No se edita a mano: cualquier
cambio se hace en la skill y se vuelve a publicar aquí.

Diferencias respecto de la skill instalada, y solo estas: se sustituyeron las
rutas absolutas del equipo de su autor por una descripción equivalente. El
resto del texto es idéntico.
-->

# Consultar las bibliotecas legislativas

## Dónde está la biblioteca

Hay dos vías. Usa la primera que esté disponible y **di cuál usaste** al responder.

**1. La Mac del usuario** (acervo completo). Carpeta raíz:

la carpeta `Biblioteca_Legislativa` del equipo del usuario (su ruta absoluta varía según el equipo y la carpeta que se haya autorizado).

La carpeta compartida puede aparecer montada con otra ruta. Identifícala buscando `Sinaloa/INDICE.md`, `Nayarit/INDICE.md`, `Federal/INDICE.md` o `IEEN/INDICE.md` dentro de la carpeta que el usuario haya autorizado. No busques en tareas ajenas. Este skill no concede permisos ni transporta los documentos.

Los originales PDF y Word de **Sinaloa y Nayarit** están en esa misma carpeta. Los originales **federales** no: viven en la carpeta de trabajo de la conversión, una carpeta de trabajo aparte de la conversión federal, en `Federal/ordenamientos/<id>/actual/original.pdf` dentro de ella. Si necesitas cotejar un original federal y esa carpeta no está autorizada, dilo y pídela; no respondas sin él. Los originales del **IEEN** también quedan fuera de Git, pero su PDF es público: `metadata.json` guarda la URL del Instituto y el SHA-256, así que un cotejo se puede hacer descargando de la fuente.

**2. El repositorio en GitHub**, cuando la Mac no esté conectada o la carpeta no esté autorizada:

`https://github.com/enriquedilo/biblioteca-legislativa`

**Clónalo** (`git clone`, rama `main`; unos 250 MB) y trabaja desde el clon: es la forma fiable. Leer archivos sueltos por HTTP funciona, pero exige la regla de resolución de rutas de la sección siguiente. Si la clonación falla por credenciales, díselo al usuario en una línea y no insistas.

El repositorio **no contiene** los originales PDF, Word ni RTF, ni las bases `biblioteca.db`. Para una consulta de texto no hacen falta. Si vas a hacer una consulta transversal, **regenera la base antes**:

    python3 bin/indices.py fts --entidad <Entidad>

Y si la respuesta exige cotejar contra el PDF original —validación dudosa, fórmula, tabla como imagen, texto anulado por sentencia— ese archivo solo existe en la Mac o en la fuente: dilo explícitamente en vez de responder sin él.

## Cómo abrir un ordenamiento — léelo antes de concluir que algo falta

Cada ordenamiento vive en `<Entidad>/ordenamientos/<id>/`, con sus versiones en `versiones/<hash>/` y un **enlace simbólico** `actual/` que apunta a la vigente.

**En un clon o en la Mac**, lee y cita por la ruta estable: `<Entidad>/ordenamientos/<id>/actual/texto.md`.

**Por HTTP el enlace no se resuelve.** `raw.githubusercontent.com/.../ordenamientos/<id>/actual/texto.md` devuelve **404**, y la interfaz de GitHub muestra el enlace, no el archivo. Un 404 ahí **no significa que el ordenamiento falte ni que esté vacío**: significa que pediste el enlace. Resuelve la ruta real por cualquiera de estos dos caminos:

1. `<Entidad>/indices/rutas.json` — trae por ordenamiento el `id`, el `nombre`, la ruta ya resuelta del `texto.md`, el `metadata`, la `validacion` y, cuando está documentado, el `estado_vigencia`. Es el punto de entrada recomendado.
2. `<Entidad>/ordenamientos/<id>/actual.json` — declara el `version` (hash); el texto está en `<Entidad>/ordenamientos/<id>/versiones/<hash>/texto.md`.

**Antes de afirmar que un ordenamiento está vacío, ausente o no consultable, comprueba las tres cosas:** que aparece en `rutas.json`, que el `texto.md` de esa ruta resuelta tiene tamaño, y —si buscabas por texto— que `biblioteca.db` existe, porque no se versiona y hay que regenerarla. Las únicas ausencias reales están listadas más abajo por su ID: seis federales y cuatro del IEEN. Fuera de esas, un «no encuentro el texto» es casi siempre una ruta mal resuelta: dilo así y corrige la ruta, no reportes un vacío del acervo.

Los números de carpeta son identificadores de catálogo propios de cada entidad —el ID 70 de Sinaloa, el de Nayarit y el federal son ordenamientos distintos— y no son números de decreto. No compongas rutas con el hash salvo para resolver el enlace o para consultar una versión histórica concreta.

## Qué contiene

Una biblioteca por entidad, con esquema idéntico:

- `Sinaloa/` — 151 ordenamientos de la categoría «Leyes Estatales» del Congreso de Sinaloa.
- `Nayarit/` — 141 ordenamientos del Congreso de Nayarit (Códigos, Constitución, Leyes, Leyes Orgánicas, Marco Jurídico del Congreso y Marco Jurídico Municipal). El ID 133, Reglamento Interior de la Auditoría Superior, está en el catálogo pero el sitio no publica su archivo. Las leyes de ingresos de los municipios quedan fuera a propósito; la Ley de Ingresos del Estado (ID 141) y el Presupuesto de Egresos del Estado (ID 142) del ejercicio 2026 sí están, ambos con `vigencia_anual`.
- `Federal/` — compilación de leyes federales vigentes de la Cámara de Diputados: **447 ordenamientos de los 453 catalogados**. Constitución, 9 códigos, 302 leyes (ordinarias, generales y orgánicas), 134 reglamentos y una ordenanza.
- `IEEN/` — normatividad del Instituto Estatal Electoral de Nayarit: **60 ordenamientos promovidos de los 64 catalogados**. En los ids **9 a 51** la normatividad electoral —reglamentos y lineamientos— y en los **101 a 121** la normatividad interna —estatuto, manuales, procedimientos, protocolos—. El catálogo completo del Instituto está en `IEEN/catalogo/normatividad.json` y las convenciones en `IEEN/LEEME.md`.

Las herramientas de mantenimiento están en `bin/`. En el equipo local puede haber además `pruebas/PRUEBA_01`: no es la biblioteca.

## Regla de entidad — la más importante

**Fija la entidad antes de consultar y declárala en la respuesta.** Si el usuario no la nombra, dedúcela del contexto de trabajo y dilo explícitamente; si es ambiguo, pregúntalo antes de leer. Federal e IEEN son entidades más para esta regla.

**Toda cita lleva la entidad.** Nunca «artículo 47, página 21», siempre «Ley de Profesiones de Sinaloa, artículo 47, página 21, `Sinaloa/ordenamientos/70/actual/texto.md`». En federal, «Ley de Instituciones de Crédito, artículo 5 Bis 1, página 3, `Federal/ordenamientos/62/actual/texto.md`». Con la entidad en la ruta, un error de atribución es visible de inmediato.

**No mezcles entidades.** Una consulta de una entidad no toca la carpeta ni el índice de otra. Para derecho comparado —incluida la contrastación de una ley estatal con la ley general o federal que la rige— corre la misma pregunta en cada índice por separado y presenta los resultados en bloques rotulados por orden de gobierno, nunca en un párrafo común ni en una tabla que funda las fuentes.

**IEEN no es Nayarit, y el trabajo electoral cruza las dos.** El catálogo del Instituto lista también leyes del Congreso de Nayarit —Constitución, Ley Estatal Electoral, Ley de Justicia Electoral, Participación Ciudadana, Transparencia, Adquisiciones y Presupuestación—, pero esas **no están en `IEEN/`**: viven en `Nayarit/` por su fuente oficial, y por eso los ids 1 a 8 de IEEN están vacíos a propósito. Una pregunta por la Ley Estatal Electoral se responde con `Nayarit/ordenamientos/55/`, no buscándola en IEEN. En `IEEN/` están los reglamentos y lineamientos propios del Instituto. Una consulta electoral completa suele necesitar los tres: la ley en `Nayarit/`, el reglamento en `IEEN/` y la ley general en `Federal/`, cada uno en su bloque rotulado.

Cuando el usuario traiga un ordenamiento suelto de otra entidad para una comparación puntual, **no lo incorpores al acervo**: trátalo como documento externo de la conversación y cítalo como tal —fuente y fecha de consulta—, no como ruta de biblioteca.

## Qué camino tomar

**Si el usuario nombra la ley**, localízala en el `INDICE.md` de su entidad —si el nombre admite varias coincidencias, muestra las opciones relevantes— y ábrela según la sección de rutas. Si no la encuentras por nombre, búscala en `<Entidad>/indices/rutas.json` o en la tabla `leyes` de `biblioteca.db`; los nombres del catálogo empiezan por el tipo («LEY General de…», «CÓDIGO Federal de…»), así que busca por una palabra distintiva de la materia y no por el nombre exacto.

**Si la pregunta es transversal** —qué ordenamientos regulan una materia, dónde aparece un término, qué leyes mencionan a otra— usa los índices antes de leer. Recorrer los archivos uno por uno es el último recurso, no el primero.

## Capa de índices

Cada entidad tiene la suya en `<Entidad>/indices/`, regenerable con `python3 bin/indices.py todo --entidad <Entidad>`:

- `biblioteca.db`: SQLite con FTS5 a nivel de entrada, insensible a acentos. Tabla `articulos(ley_id, ley, articulo, tipo, pagina, linea, texto)` y tabla `leyes` con la metadata normativa. **No se versiona en GitHub: si trabajas desde el repositorio, regenérala.** En la Mac, el montaje de carpetas compartidas no admite el bloqueo de SQLite: copia el archivo a almacenamiento local antes de consultarlo.
- `articulos/<id>.json`: articulado con número (incluidos Bis, Bis-A, Ter, series compuestas como `5 Bis 1`, ordinales latinos hasta Novodecies, ordinales compuestos como `DÉCIMO PRIMERO`, numeración con coma de millar, y ordinales en letra en leyes antiguas), `tipo`, página del PDF, rango de líneas y notas de reforma.
- `remisiones.json`: menciones nominales entre ordenamientos **de la misma entidad**, con el artículo donde ocurren.
- `articulado_resumen.json`: conteos por ordenamiento.
- `rutas.json`: id, nombre, ruta resuelta del `texto.md` vigente y, cuando está documentado, `estado_vigencia`.

**Hay tres tipos de entrada, no dos.** `cuerpo` y `transitorio` son artículos. **`seccion` no lo es**: aparece en documentos que no se numeran por artículos —lineamientos, manuales, protocolos— y su etiqueta es la división propia del documento (`CAPÍTULO II`, `TÍTULO I`) o, si no trae divisiones, `Página N`. **Nunca conviertas una sección en un número de artículo al citar**: se cita «sección CAPÍTULO II, página 4» o «página 7». Hoy 15 ordenamientos del IEEN se indexan así y ninguno de los otros tres acervos.

Ejemplo de consulta transversal:

```sql
SELECT ley, articulo, pagina, snippet(articulos,6,'>>','<<','…',12)
FROM articulos WHERE articulos MATCH '(arancel OR honorarios) AND (perito OR pericial)';
```

En cualquier discrepancia entre un índice y el `texto.md`, manda el texto. Los índices orientan la búsqueda; la cita se toma del documento.

## Los únicos ordenamientos sin texto en la biblioteca

**Seis federales.** Catalogados, con su PDF y su SHA-256 conservados, pero su conversión no superó el control —o el PDF no trae capa de texto— y no se promovió: no tienen `actual/` ni entran en ningún índice. No se les aplicó OCR.

| ID | Ordenamiento |
|----|--------------|
| 372 | Reglamento de la Ley del Servicio Militar (1942) |
| 413 | Reglamento de la LGS en Materia de Control Sanitario de Actividades, Establecimientos, Productos y Servicios (1988) |
| 414 | Reglamento de la LGS en Materia de Control Sanitario de la Disposición de Órganos, Tejidos y Cadáveres (1985) |
| 416 | Reglamento de la LGS en Materia de Investigación para la Salud (1987) |
| 444 | Reglamento de la Ley Federal de Ganadería (1955) |
| 446 | Reglamento del artículo 5º constitucional (1945) |

Su única fuente es el PDF de la Cámara, cuya URL y hash están en `Federal/reportes/pendientes-finales.json`.

**Cuatro del IEEN**, por la misma razón: el 45 (reglas procesales de procedimientos sancionadores 2025) y el 104 (manual de operación de la Oficialía de Partes) son escaneos sin texto en ninguna página; el 48 (criterios de validez o nulidad del voto) y el 106 (manual de contabilidad gubernamental) pierden texto normativo en páginas interiores. Su URL pública está en `IEEN/catalogo/normatividad.json`.

Si la consulta toca uno de estos diez, **dilo y ofrece su PDF**. No cites de memoria lo que dicen. **Las dos listas son exhaustivas**: cualquier otro ordenamiento sí tiene texto.

## Vigencia: la compilación se toma como buena

El usuario trabaja con la compilación consolidada de los congresos, de la Cámara de Diputados y del Instituto como fuente válida. **No añadas advertencias genéricas sobre cotejo con el Periódico Oficial o el Diario Oficial**, ni recuerdes en cada respuesta que la compilación es administrativa: ya lo sabe, y repetirlo estorba. Cita el texto del acervo con normalidad.

Lo que sí se advierte es lo concreto, y solo cuando afecta al texto citado:

- **`estado_vigencia` en `rutas.json`.** Cuando un ordenamiento lo trae, respeta lo que dice. **Nayarit 78, Ley de Justicia Alternativa, está abrogada**: el Congreso la movió a su carpeta de ordenamientos abrogados y la sustituye la **Ley de Mecanismos Alternativos de Solución de Controversias, Nayarit 140**. Si la consulta toca la materia, responde con la 140 y menciona la 78 solo como antecedente, nunca como derecho vigente. Su texto se conserva para trabajo histórico.
- **Texto anulado que no se ve.** El acervo guarda texto plano y **el tachado es formato del PDF que no sobrevive a la conversión**. Cuando una compilación tacha lo que una sentencia dejó sin efectos, en el `texto.md` ese pasaje se lee igual que el vigente y la nota que lo explica suele estar al final, sin decir cuál es. Caso conocido: **IEEN 27**, Lineamientos dirigidos a los partidos políticos, página 14, sentencia del Tribunal Estatal Electoral en el recurso TEE-AP-09/2019. Si el `texto.md` o el `validacion.json` mencionan texto tachado, sin efectos, invalidez o sentencia, **adviertelo antes de citar y manda al PDF**, explicando por qué: no es cautela genérica, es que el texto plano no distingue lo anulado de lo vigente.
- **Ley General del Sistema de Medios de Impugnación en Materia Electoral (ID 223)**: **no está abrogada**. Su `metadata.json` trae `vigencia_recuperada` porque la SCJN invalidó el decreto de 2023 que la abrogaba. Nunca la cites como abrogada.
- **Código Federal de Procedimientos Civiles (ID 5)**: trae `abrogacion_programada` —abrogado por el decreto que expide el Código Nacional de Procedimientos Civiles y Familiares, con vigencia a más tardar al 1 de abril de 2027—. Adviértelo siempre que lo cites.
- **Ley de Ingresos federal (ID 60) y LIGIE (ID 78 federal), y en Nayarit la Ley de Ingresos del Estado (ID 141) y el Presupuesto de Egresos del Estado (ID 142)**: `vigencia_anual`. Comprueba el ejercicio antes de citarlas.
- Un artículo con **declaratoria de invalidez de la SCJN**, o una versión con una incidencia en `validacion.json` que toque el pasaje citado.
- **Reglamento de la LGS en Materia de Sanidad Internacional (ID 419)**: la compilación oficial salta del artículo 22 al 24. El 23 no existe en la fuente; no es una omisión de la biblioteca.

Si el usuario pregunta expresamente por vigencia al día de hoy, dile que el acervo refleja la compilación a la fecha de descarga que registra `metadata.json` y ofrécele consultar la fuente oficial en línea.

## Lectura y verificación

Lee `metadata.json` y `validacion.json` de la versión consultada para conocer fuente, descarga, revisión, correcciones y campos no localizados. `metadata.json` incluye `decreto_numero`, `po_publicacion`, `ultima_reforma`, `reformas`, `abroga`, y en Nayarit y Federal también `orden`, `regimen` y `tipo`. En Federal revisa además `abrogacion_programada`, `vigencia_recuperada` y `vigencia_anual`. En IEEN trae `seccion` —`electoral` o `interna`—, `acuerdo` —el del Consejo o de la Junta que aprobó la versión vigente, como `IEEN-CLE-015/2025`— y `reformas` con la cadena de acuerdos anteriores. Donde haya `estado_vigencia`, `abrogada_por` o `abroga`, respetarlos manda sobre cualquier inferencia.

**Un campo nulo o un arreglo vacío significa que el dato no está impreso, no que no exista.** En Sinaloa solo 10 de 151 documentos traen tabla explícita de reformas y 64 registran abrogación expresa. En Nayarit, 61 de 139 no imprimen la sección de publicación y 39 no imprimen fecha de última reforma. Es la regla de «solo lo impreso» funcionando, no una falla de extracción.

Busca términos y variantes (arancel, honorarios, perito, tarifa, cuota, remuneración). Lee el artículo completo y el contexto aplicable, incluso si cruza páginas. Para afirmar que una ley no contiene algo, busca en el documento completo, incluidos transitorios; distingue una remisión a otra norma de una tarifa o regla expresamente incluida.

Identifica la página con el comentario `<!-- PAGINA_PDF: n -->` inmediatamente anterior al pasaje. Distingue artículos del cuerpo, referencias dentro de párrafos y artículos transitorios de distintos decretos. No confundir 1°, 1º o 1o con 11. Sinaloa rotula el articulado como `Artículo N` y, en la Constitución y los dos primeros códigos, como `Art. Nº`; Nayarit usa `Artículo N.-`, y dos leyes antiguas —las que crean la Comisión de Financiamiento y Comercialización de Productos Agrícolas (ID 31) y la Procuraduría de la Defensa del Menor y la Familia (ID 34)— numeran su cuerpo con ordinales en letra. Federal usa `Artículo N.-` o `Artículo N.`, con series como `5 Bis 1`, `78 Octodecies` o `1,000`; la LGIPE (ID 200), el Reglamento del Senado (ID 315) y la LGSMIME (ID 223) rotulan `Artículo N` sin puntuación y numeran párrafos debajo (`1.`, `2.`): esos números de párrafo no son artículos. Los reglamentos del IEEN rotulan `Artículo N.-`, como Nayarit, y varios ponen un título temático en la línea siguiente al encabezado: ese título es texto del artículo, no parte de su número.

Las compilaciones traen erratas de imprenta que el acervo conserva tal cual: «Artículos 135» en plural (LFDA, ID 169), «Artículo. 88» con punto (Reglamento de la Ley Aduanera, ID 317), «. Artículo 40» con punto suelto (Reglamento de la LF de Cinematografía, ID 377), «P.O. 3 DE SDEPTIEMBRE DE 2026» en la Constitución de Nayarit. No las corrijas en la cita literal; si el usuario las va a reproducir en un documento formal, señálalas.

Consulta `original.pdf` o el Word cuando la validación advierta una omisión o el texto sea dudoso; recuerda que esos archivos solo están en la Mac, salvo los del IEEN, que se pueden volver a descargar de la URL que guarda su `metadata.json`. Las correcciones documentadas del Markdown pueden diferir deliberadamente de la compilación original: revisa sus referencias antes de revertirlas o descartarlas.

## Historial de reformas

Los acervos de los congresos imprimen anotaciones al pie o al final de los párrafos. Sinaloa con la forma `(Ref. Según Dec. No. 257, publicado en el P.O. No. 115, del 23 de septiembre de 2022)`; Nayarit más escueto, `(REFORMADO, P.O. 8 DE NOVIEMBRE DE 2016)`, normalmente sin número de decreto ni de periódico; Federal sin paréntesis y pegado al párrafo, `Párrafo reformado DOF 30-09-2024`. La capa de índices las extrae a `articulos/<id>.json` con lo que haya impreso.

**IEEN funciona distinto.** Sus reglamentos y lineamientos no imprimen la anotación en el artículo: la cadena de reformas vive en `metadata.json`, como lista de acuerdos del Consejo o de la Junta con su fecha y su URL. El texto cargado es el consolidado vigente, y **las versiones anteriores no están convertidas**: si el usuario necesita un texto anterior, dilo y ofrece el acuerdo correspondiente del catálogo, no reconstruyas la versión vieja a partir del texto vigente.

En Federal no se anclan todavía tres tipos de anotación: las notas explicativas `Reforma DOF dd-mm-aaaa: …`, las declaratorias de invalidez de la SCJN y las referencias de la tabla arancelaria de la LIGIE. Búscalas en el texto cuando importen. **Una declaratoria de invalidez no es una reforma**: si un artículo la trae, dilo expresamente.

Las anotaciones sirven para saber cuándo se intervino un artículo, pero **no son una tabla oficial de reformas**: pueden faltar en artículos efectivamente reformados. No presentes ese historial como completo.

Cuando el acervo viva en el repositorio, el historial de Git muestra qué cambió en un `texto.md` entre dos fechas (`git log -p`). Úsalo como evidencia de qué se actualizó en la biblioteca, no como cronología normativa oficial.

## Fórmulas y tablas

Lee las advertencias de la versión consultada. En Sinaloa, Coordinación Fiscal (ID 24) tiene las expresiones recuperadas al inicio de las secciones de página y en `formulas_recuperadas.json`; el cuerpo extraído conserva huecos. Relaciona expresiones y párrafos mediante su página y la imagen de respaldo. No simplifiques ni completes símbolos por intuición. En Pensiones (ID 65), la tabla de página 36 está conservada como imagen y sus valores no están transcritos; para una pregunta numérica, comprueba la celda en el original y declara si no es legible. En Federal, la tabla arancelaria de la LIGIE (ID 78) es una tabla de fracciones, no articulado. En IEEN, varios documentos se promovieron con una página ilegible anotada en `validacion.json` —portada, página en blanco o composición gráfica—: si la pregunta cae en esa página, dilo y manda al PDF.

## Respuesta

Responde en español, directamente a la pregunta, distinguiendo cita literal e interpretación. Cita entidad, ley, artículo o fracción —o sección y página, cuando el documento no se numere por artículos—, página y ruta del archivo efectivamente leído. Cuando trabajes desde el repositorio en vez de la Mac, dilo. Añade limitaciones solo cuando afecten la respuesta concreta —una incidencia de conversión, un ordenamiento sin texto, una abrogación, texto anulado por sentencia—, no como fórmula de cierre.

**Nunca reportes que un ordenamiento está vacío, ausente o inconsultable sin haber agotado la resolución de ruta descrita arriba.** Decirle al usuario que una ley no está cuando sí está lo lleva a reconstruir trabajo ya hecho; si tras comprobar `rutas.json`, la ruta versionada y la base de búsqueda sigue sin aparecer, describe exactamente qué intentaste.

Para preguntas sobre el contenido archivado, usa la biblioteca como fuente y no amplíes por iniciativa propia a una investigación externa. Si el usuario pide vigencia actual o búsqueda externa, consulta fuentes oficiales con las herramientas y permisos disponibles, diferenciando esos resultados del archivo local. Cumple las reglas de fuentes de la aplicación anfitriona.

## Límites de los índices

Las remisiones son detección léxica de nombres: no distinguen la remisión normativa de la cita incidental y no capturan las genéricas. El artículo 47 de la Ley de Profesiones de Sinaloa remite a «los aranceles respectivos» sin nombrar la Ley de Aranceles, y por eso no figura como arista. Trata `remisiones.json` como pista, no como mapa normativo. Tampoco hay remisiones entre entidades: que una ley estatal remita a una ley general no aparece en ningún índice, y eso incluye la relación entre un reglamento del IEEN y la Ley Electoral de Nayarit que lo funda.

El conteo de artículos duplicados dentro de un mismo ordenamiento —unos 400 en el acervo— está sin diagnosticar: parte son ordinales impresos repetidos en listas finales de decretos y parte, errores de segmentación. Si un número de artículo devuelve dos entradas, compara su página y su texto antes de citar.

## Regla de escritura

Las consultas son de lectura: no regeneres conversiones, muevas leyes ni actives actualizaciones periódicas al responder, y **no hagas commit ni push al repositorio** por una consulta. Si el usuario pide modificar una biblioteca, trata ese trabajo como una tarea distinta, conserva originales y trazabilidad, y no escribas en el árbol mientras otra herramienta lo esté procesando. Los índices sí pueden borrarse y regenerarse sin riesgo: son derivados, y la base `biblioteca.db` se regenera cada vez que haga falta.