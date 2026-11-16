# Pendientes abiertos

Lo que falta en la biblioteca, para no depender de la memoria de una
conversación. Quien cierre un punto lo mueve a «Cerrado» con su fecha.

**Última revisión: 16 de noviembre de 2026.** Esta revisión consolida tres
fuentes: los pendientes anteriores, las dos auditorías externas independientes
del 12 de noviembre —una en Claude sobre el repositorio público, otra en Codex
sobre el clon local con los originales— y el reporte de mantenimiento derivado
de las auditorías de Salud Mental (Sinaloa) y Ley de Bienes (Nayarit).

Cada punto dice de dónde sale. `[Codex Hn]` y `[Claude Cn/An/Mn/Bn]` remiten a
los hallazgos numerados de cada auditoría; `[Mant.]` al reporte de
mantenimiento; `[Previo]` a lo que ya estaba registrado aquí.

---

## 1. Identidad del artículo citado — lo más grave

Hasta noviembre de 2026 la premisa de trabajo era que los índices orientan y el
texto manda. **Eso dejó de ser suficiente**: hay rótulos equivocados en el
propio `texto.md`, no solo en el índice. Mientras esto no se corrija, una cita
puede llevar página correcta y número falso, que es el error más difícil de
detectar y el único que llega a un documento formal sin avisar.

### 1.1 Rótulos inexistentes en el texto convertido `[Codex H1]`

El conversor partió la palabra «Terminado» y se llevó «Ter» al encabezado:

| Documento | Página | Rótulo archivado | Rótulo real |
|---|---:|---|---|
| Sinaloa 1, Código Civil | 53 | `ART. 1046. Ter` | 1046 |
| Sinaloa 1, Código Civil | 154 | `ART. 2340. Ter` | 2340 |
| Sinaloa 4, Código Familiar | 29 | `Artículo 114. Ter` | 114 |

El control de conservación los aprueba porque no se pierde ni sobra una letra.
**Exige versión nueva del `texto.md` con el PDF delante**, no basta regenerar
índices. Añadir regresión que compruebe el rótulo como unidad léxica,
incluyendo la primera palabra del párrafo.

### 1.2 Artículo de otra ley rotulado como propio `[Claude C4]`

El Código Civil Federal (Federal 2) tiene cinco entradas «54». Solo la de la
página 8 es suya; las otras cuatro —páginas 173, 197, 221 y 224— son el
artículo 54 de la Ley del Notariado de 1946 transcrito en notas del compilador.
El artículo 1777 queda además truncado antes de su nota.

### 1.3 Encabezados espurios dentro del texto `[Claude C3]`

El conversor promovió a rótulo una remisión que venía a media frase, de modo
que el tramo queda atribuido a un artículo que no lo contiene. Verificados a
mano: Nayarit 52 y 116; Sinaloa 5, 16, 19, 88, 102 y 108. El recuento de
candidatos —rótulo seguido de línea que abre en minúscula o coma— da Federal
27, Sinaloa 52, Nayarit 3, IEEN 5; no todos son espurios.

### 1.4 Los ~400 duplicados, ya diagnosticados

`[Previo]` registraba 398 duplicados «sin diagnosticar» (Sinaloa 171, Nayarit
7, Federal 220). Las dos auditorías los desarmaron en cinco causas
reproducibles. Las tres primeras se corrigen en `bin/indices.py`:

- **Sufijo compuesto partido** `[Claude C1] [Codex H2]`. Con el rótulo cortado
  en dos líneas —`### Artículo 17-` y debajo `H Bis.`— el índice guarda `17`.
  `RE_SUFIJO_SIG` solo acepta una letra seguida de punto o guion, y la línea 274
  solo busca el sufijo siguiente cuando el reconocido está vacío, así que
  `485 Bis-1` y `485 Bis-2` colapsan en `485 BIS`. Alcance estimado: ~130
  entradas federales en 21 ordenamientos, ~73 de Sinaloa en 13, una de Nayarit.
- **La letra «O» de serie leída como ordinal** `[Claude C2]`. `RE_ART` acepta
  `(?:o|º|°)` con `IGNORECASE`, así que «145 O.-» se indexa como «145».
  Confirmado en Nayarit 58 y 67.
- **Transitorios tipificados como cuerpo** `[Claude C5] [Codex H3]`.
  `RE_TRANS_TIT` exige que «TRANSITORIOS» sea encabezado Markdown y palabra
  sola. Con el título en texto plano todo lo que sigue entra como `cuerpo`:
  Federal 241 (quince transitorios de 1931 como artículos 1 a 15), Federal 307
  (una fe de erratas como 27 artículos), Federal 271.

Las otras dos son 1.2 y 1.3. **Orden obligado: corregir textos, luego el
parser con sus regresiones, y solo entonces regenerar índices.**

### 1.5 La columna `pagina` de la base no es la del pasaje `[Claude A3]`

La FTS guarda una fila por artículo con la página de su rótulo y elimina los
marcadores del texto. Entre un cuarto y un tercio de las entradas cruzan un
salto de página. El ejemplo del README invita a citar esa columna junto al
snippet. **Ya advertido en la skill**; falta corregir el ejemplo del README y
evaluar guardar el desplazamiento de cada salto.

### 1.6 El control de conversión no certifica estructura `[Claude A5]`

«Conversión conservada» descansa en comparación léxica de frecuencias y orden
de palabras. Los defectos 1.1 a 1.3 la superan porque no alteran el inventario
de palabras. Falta un control de articulado: secuencia de numeración, rótulos
seguidos de minúscula, rótulos que repiten número.

---

## 2. Vigilancia

Cuatro defectos reproducibles, con pruebas que fallan contra el código actual
en el apéndice A de la auditoría de Codex. **Cerrarlos antes de ampliar la
cobertura a IEEN e INE**, no después.

### 2.1 La primera corrida descarta diferencias SHA confirmadas `[Codex H7]`

`main` conserva solo `no_encontrado` e `inaccesible`; descarta `modificado`. El
primer reporte puede decir «sin cambios» habiendo detectado contenido distinto
del archivado.

### 2.2 `--entidad` borra el estado de los demás acervos `[Codex H8]`

`main` inicializa el estado nuevo vacío, procesa solo la entidad pedida y
reemplaza el archivo global. Revisar Sinaloa elimina las observaciones
federales y de Nayarit.

### 2.3 La alerta por prefijo no persiste `[Codex H5] [Claude M1]`

La comparación es contra el prefijo observado en la corrida anterior, no contra
la línea base archivada. A la semana siguiente coincide y el hallazgo
desaparece aunque el acervo no se haya actualizado. La persistencia de
pendientes solo usa `sha256` completo. Hoy afecta a la LIGIE (Federal 78, PDF
de 18 MB y Word de 25 MB), que además es de vigencia anual.

### 2.4 Un alta nueva entra sin cotejo inicial `[Codex H6] [Claude M1]`

Con estado global previo y sin observación anterior del archivo, `revisar`
recibe `previo=None` y `forzar=False`; con cabeceras disponibles no descarga ni
compara contra el SHA archivado, y la cabecera pasa a ser línea base sin
verificar. Afecta a Nayarit 140, 141 y 142, que no están en `estado.json`.
Corrección mínima: cotejo completo obligatorio en la primera observación de
cada archivo, no solo en la primera corrida global.

### 2.5 El IEEN no se vigila `[Previo] [Codex H9] [Claude M2]`

`ENTIDADES = ("Sinaloa", "Nayarit", "Federal")` en `bin/vigilancia.py:30`, y
`CATALOGOS` tampoco incluye al Instituto. Los 60 promovidos llevan desde su
carga sin ninguna detección de cambio. Falta el adaptador de catálogo; el sitio
responde `Last-Modified` y `Content-Length`, así que sirve la detección barata.

### 2.6 El catálogo de Sinaloa no es observable `[Previo] [Codex H9]`

Se arma con JavaScript desde otro host y su lista no se ve en el HTML servido,
así que la función de catálogo retorna `lista_no_observable` y no hay segunda
consulta que detecte altas o sustituciones de enlace. El reporte debería
distinguir «sin cambios observados» de «catálogo no evaluable», y publicarse
una matriz explícita de cobertura por acervo.

### 2.7 El workflow puede perder su propia constancia `[Claude M3]`

`.github/workflows/vigilancia.yml` hace `git push` sin `pull --rebase`. Si se
fusiona un PR durante la corrida —unos 18 minutos— el push falla por no ser
fast-forward y se pierde el registro de esa semana.

### 2.8 Nombre temporal fijo en la generación FTS `[Codex H13] [Claude M7]`

`bin/indices.py` usa `biblioteca_fts.db` dentro de `TMPDIR` y borra cualquier
archivo previo con ese nombre. Dos procesos que regeneren entidades distintas
se pisan. Usar ruta exclusiva por proceso y publicación atómica.

### 2.9 El cron se retrasa `[Previo]`

Puesto los lunes a las 14:17 UTC, las corridas caen entre cinco y ocho horas
después. Es la cola de GitHub para tareas programadas, no una falla del flujo.
No requiere acción.

---

## 3. Vigencia y advertencias que no llegan a la consulta

### 3.1 La base de búsqueda no sabe nada de vigencia `[Claude A4]`

La tabla `leyes` de `biblioteca.db` no tiene columna de estado, y `rutas.json`
solo expone `estado_vigencia`, que en Federal no existe. Un resultado de FTS de
la Nayarit 78 abrogada se ve igual que el de una ley vigente, y
`abrogacion_programada`, `vigencia_recuperada` y `vigencia_anual` quedan fuera.
**Ya advertido en la skill**; falta exponerlo en el índice.

### 3.2 Federal 203 y 281 `[Codex H4]`

Sus portadas imprimen la invalidez del decreto que expidió cada ley, pero el
preámbulo queda fuera de la fila indexada del primer artículo y el hecho no
aparece en `rutas.json`. Agrava la semejanza de nombre entre Federal 203 y 223.

### 3.3 Texto anulado que no se ve `[Previo]`

El acervo guarda texto plano y el tachado es formato del PDF que no sobrevive a
la conversión. Caso conocido: IEEN 27, página 14, sentencia TEE-AP-09/2019.
**Regla ya incorporada a la skill.** Queda abierto si conviene marcarlo en
`validacion.json` de forma que el índice pueda exponerlo.

---

## 4. Integridad y especificación

### 4.1 Cinco federales rechazados tienen texto legible `[Claude A1]`

Los ids 372, 413, 414, 416 y 446 **sí tienen `texto.md` versionado y legible**,
pese a no estar promovidos. No tienen `actual.json` y llevan
`texto_conservado: false`, pero abren con la misma línea genérica que cualquier
conversión buena, y un `grep` o una lectura por HTTP puede encontrarlos y
citarlos. El acervo IEEN resuelve esto bien: sus cuatro no promovidos abren con
«EXTRACCIÓN DIAGNÓSTICA INCOMPLETA». **Federal debe adoptar ese rótulo o
retirar esos textos.** Advertido en la skill mientras tanto.

### 4.2 El id 444 está mal identificado y no tiene carpeta `[Claude A2]`

README e índices lo llaman «Reglamento de la Ley Federal de Ganadería», que no
existe en el catálogo. Es el Reglamento de la Ley que Crea el Fondo de Garantía
y Fomento para la Agricultura, Ganadería y Avicultura. El 446 también estaba
descrito de forma imprecisa. **Corregido en la skill**; falta en README y en
`Federal/indices/README.md`.

### 4.3 `version` no es el SHA-256 del original `[Codex H10] [Claude B8]`

README, brief y un razonamiento de este archivo lo daban por invariante. Solo
se cumple en los 60 documentos del IEEN. En Federal, Sinaloa y Nayarit el
identificador se deriva del SHA del mapa de hashes (`bin/biblioteca.py:65`,
`bin/nayarit/biblioteca.py:115`) o de una corrección de metadata
(`bin/federal/metadatos.py:74`). No es corrupción: es una especificación mal
escrita. **Corregido en la skill.** Falta definir por separado, y documentar, el
hash de cada original y el identificador de versión de la representación.

### 4.4 Enlaces de entrada desincronizados `[Codex H12] [Claude B6] [Claude B7]`

`Sinaloa/INDICE.md:30` enlaza el ID 23 a la versión `2ffab4bc…` cuando
`actual.json` y `rutas.json` seleccionan `4dc4c10d…`. Además los INDICE de
Sinaloa (151 enlaces) y Nayarit (279) apuntan a `original.pdf` y `original.doc`,
excluidos por `.gitignore`: en GitHub son enlaces rotos. Generar los enlaces
desde `actual.json`/`rutas.json` y comprobarlos al publicar.

### 4.5 Versiones sustituidas sin marca `[Claude, decisión cuestionada]`

Hay 151 versiones no seleccionadas; en Sinaloa y Nayarit cerca de la mitad no
trae señal de haber sido sustituida —Sinaloa 23 tiene ambas versiones con la
misma `fecha_descarga` y metadata idéntica—. Conservarlas es correcto; dejarlas
indistinguibles para quien llega por HTTP, `grep` o un enlace viejo, no.

### 4.6 `actual/` no resuelve en todos los clones `[Claude B13]`

Con `core.symlinks=false`, que es el valor por defecto en Windows, `actual` es
un archivo de texto con una ruta dentro. La skill ya manda resolver por
`rutas.json`; conviene que el README lo diga en vez de afirmar que «en un clon
se resuelve».

---

## 5. Metadata y trazabilidad

### 5.1 Nombres oficiales sin cotejar `[Mant. 1]`

Sinaloa 145 de 151 y Nayarit 24 de 141 tienen `nombre_oficial` vacío con
`nombre_oficial_pendiente_de_cotejo` en true. Federal e IEEN están completos.
Verificado. Hoy no impide identificar ninguna ley porque el nombre se toma del
encabezado del `texto.md`, que trae el nombre corto del catálogo y no la
denominación oficial. Conviene llenar el campo y evaluar una lista de alias por
ordenamiento.

### 5.2 «Sin reformas» frente a «no impreso» `[Mant. 2]`

Federal 139 de 447 y Nayarit 40 de 141 no traen `ultima_reforma`; Sinaloa está
completo. Verificado. Con el campo vacío no se puede afirmar que una ley no ha
sido reformada: la Ley de Bienes de Nayarit (ord. 20) obligó a comprobarlo en
el sitio del Congreso.

**IEEN es distinto y no debe «arreglarse»:** 59 de 60 no traen
`ultima_reforma` porque el Instituto no imprime la anotación en el artículo; su
cadena de reformas vive en `metadata.json` como lista de acuerdos. Lo que sí
amerita revisión es que **solo 18 de 60 tienen esa cadena poblada**.

Sobre la propuesta de un campo `sin_reformas: true`: afirma una ausencia dentro
de un archivo cuya regla entera es «solo lo impreso». Si entra, debe entrar con
procedencia —qué catálogo se consultó y en qué fecha—, no como booleano suelto.

### 5.3 El campo `validacion` no discrimina `[Mant. 3]`

Federal: los 447 traen exactamente la misma cadena. Nayarit: 133 de 141.
Sinaloa: 134 de 151 en «pendiente de cotejo visual». Verificado. No es que haya
muchos pendientes: es que el campo es constante y por tanto no informa.

Se descarta la propuesta de un `apto_para_cita: sí/no`: colapsa el matiz que el
acervo existe para conservar y hoy saldría «no» en 714 de 799 documentos. La
forma útil es la **lista de incidencias por artículo**, que sí permitiría al
índice advertir solo cuando el pasaje citado está afectado. Priorizar el cotejo
de las leyes que más se intervienen: salud mental, víctimas, desplazamiento,
desaparición, bienes.

### 5.4 Fecha del último cotejo contra el catálogo `[Mant. 4]`

La observación del reporte era que los ordenamientos de Nayarit se descargaron
el 14 de septiembre; en realidad hay al menos seis fechas de descarga, del 14 de
septiembre al 10 de noviembre. **La propuesta de fondo sigue siendo buena y es
más barata de lo que parece:** `vigilancia/estado.json` ya guarda, por
ordenamiento, la última observación contra el catálogo oficial con su fecha y la
firma del archivo. El dato existe; falta exponerlo en `rutas.json` para que una
respuesta pueda decir «vigente al …» y avisar cuando tenga antigüedad.

---

## 6. Alcance del acervo

### 6.1 Acervo del INE `[Previo]`

23 documentos del compendio, servidos desde `sidj.ine.mx/restWS…/app/doc/<id>/20/1`
con identificador numérico estable, con su propio adaptador de catálogo.
NormaINE se consulta, no se espeja. Las URL no pudieron verificarse desde el
entorno de trabajo porque el proxy bloquea el host. Al incorporarlo, cotejar
IEEN/38 antes de duplicar: su metadata trae `deduplicacion` con clave
`INE/CG517/2020:A1`.

### 6.2 IEEN: cuatro no promovidos `[Previo]`

45 (reglas procesales de procedimientos sancionadores 2025) y 104 (manual de
operación de la Oficialía de Partes) son escaneos sin texto; 48 (criterios de
validez o nulidad del voto) y 106 (manual de contabilidad gubernamental)
pierden texto normativo en páginas interiores. Sin `actual`, fuera de índices,
sin OCR. Véanse los reportes de los lotes 3 y 4.

Queda abierto que el 47 podría reconocer numerales en lugar de la segmentación
por página que se le aplicó.

### 6.3 Sinaloa: materia fiscal `[Previo]`

Decidido el 12 de noviembre no cargarla por ahora. La fuente es una sola ley
conjunta de ingresos y egresos en ocho PDF del Periódico Oficial, en el portal
de Transparencia, sin Word y fuera del catálogo de «Leyes Estatales».
Cargarla obligaría a romper la regla de un texto por ordenamiento. **La skill
debe advertirlo cuando la consulta sea fiscal de Sinaloa**; sigue pendiente de
incorporar.

### 6.4 Normas fiscales anuales `[Previo]`

Nayarit 141 y 142, ejercicio 2026, marcados `vigencia_anual`. **Revisar y
refrescar cada diciembre o enero** desde los enlaces del catálogo: conservar
versiones anteriores, actualizar URL y hashes, comprobar el ejercicio antes de
citar. Una URL anual que siga respondiendo no acredita que sea el ejercicio
vigente. Las veinte leyes de ingresos municipales siguen excluidas por alcance.

### 6.5 Nayarit 133 `[Previo]`

Reglamento Interior de la Auditoría Superior: está en el catálogo del Congreso
pero el sitio no publica ni PDF ni Word. Sin cambios.

### 6.6 Leyes de otras entidades `[Mant. 5]`

Las auditorías de iniciativas citan leyes de otros estados verificadas en web
—Ciudad de México, Zacatecas, Jalisco, Aguascalientes, Morelos, Chiapas,
Guerrero, Oaxaca, Nuevo León—. Si las comparativas se vuelven frecuentes,
**la forma no puede ser una colección temática**: rompería el invariante de un
acervo por catálogo oficial y la regla de no mezclar entidades. Serían acervos
nuevos, uno por congreso, aunque se cargue solo un subconjunto.

### 6.7 Vista electoral en la capa de índices `[Previo]`

Prevista como paso 5 del acervo electoral; no existe. Evaluar si sigue siendo
necesaria ahora que la consulta electoral se resuelve cruzando `Nayarit/`,
`IEEN/` y `Federal/` en bloques rotulados.

---

## 7. Proceso, pruebas y documentación

### 7.1 Sin pruebas del parser de articulado y sin CI `[Claude M6]`

`bin/ieen/pruebas_indices.py` tiene tres pruebas, ninguna sobre sufijos
compuestos, la «O» de serie ni títulos de transitorios. Ninguna suite corre en
integración continua: el único workflow es la vigilancia. Los casos de 1.4 son
regresiones naturales.

### 7.2 Índices publicados desfasados del código `[Claude M5]`

`1c12ac6` agregó el conteo `secciones` y el tipo `seccion`, pero
`Federal/indices/` y `Sinaloa/indices/` no se regeneraron. Al regenerar cambian
811 archivos y el diff semántico solo agrega `secciones: 0`, así que el
contenido es reproducible. Falta un paso que impida publicar índices
desfasados.

### 7.3 Modos inválidos aceptados en silencio `[Claude M7]`

`python3 bin/indices.py tdo --entidad IEEN` imprime el encabezado y sale con
código 0 sin generar nada. Quien teclee mal el modo cree haber regenerado.

### 7.4 Cambios de contenido en `main` sin PR `[Claude M4]`

`git log --first-parent --no-merges main` muestra 38 commits directos, entre
ellos uno que actualiza la Constitución de Sinaloa y otro que cambia el parser
de índices. El flujo declarado es rama y pull request. Decidir si la regla
aplica siempre o se documenta la excepción. La vigilancia escribe directo en
`main` por diseño, y eso causa 2.7.

### 7.5 Documentación que no describe el repositorio `[Codex H11] [Claude B1–B5, B10–B14]`

`README.md` y `LEEME.md` siguen describiendo **tres acervos y 737
ordenamientos**; la suma de sus propias cifras da 739 y el total real con IEEN
es 799. Las cifras de artículos y transitorios no corresponden a los índices
actuales. `Federal/INDICE.md:7` dice «sin índices de búsqueda ni articulado»,
que existen desde `8527e2d`. `Federal/indices/README.md` conserva cifras
anteriores. `IEEN/AVANCE.md` dice «PR en borrador, sin merge», fusionado en
`c4ab46a`. `IEEN/INDICE.md` tiene dos filas fuera de la tabla por una línea en
blanco. `.gitignore` repite `original.rtf` y `original.txt`.

**Generar los conteos desde los índices en vez de escribirlos a mano**, y
separar la información vigente de los reportes históricos.

### 7.6 Auditoría integral `[Previo]`

El pendiente mayor registrado el 12 de noviembre queda **cumplido en su mayor
parte** por las dos auditorías externas. Lo que ninguna cubrió y sigue abierto:

- **Altas que nunca entraron**: ordenamientos publicados por los congresos
  después de la carga inicial y ausentes del acervo. No hay control que los
  busque.
- **Vigencia real** ordenamiento por ordenamiento contra lo que publica cada
  fuente hoy. Ambas auditorías fueron estáticas: ninguna alcanzó los sitios
  oficiales.
- **Cotejo de originales faltantes**: Codex verificó 646 originales presentes
  contra su SHA declarado, sin una sola discrepancia, y comparó 15,680 páginas
  de 323 PDF. Quedaron sin cotejar los 447 federales —la carpeta de originales
  no estaba autorizada—, 13 PDF del IEEN (ids 9 a 21) y 16 estatales ausentes
  del montaje.
- **El proceso, no solo el dato.** Por qué una alerta se cerró dos veces como
  ruido. Una alerta que no se puede accionar enseña a ignorar la alarma.

### 7.7 Infraestructura `[Previo]`

**Enero de 2027**: el token de acceso personal de GitHub vence a mediados de
enero. Quedó acordado no regenerar otro, sino pasar la autenticación al GitHub
CLI (`gh auth login`) y revocar el token viejo. Hay tarea programada.

---

## Cerrado desde la revisión del 10 de noviembre

- **Acervo del IEEN**: los 64 candidatos procesados, 60 promovidos (ids 9–51
  electoral, 101–121 interna). Catálogo, carga por lotes y cotejo, hechos.
- **Skill actualizada** en sus dos momentos: descripción con los cuatro
  acervos, conteos reales, numeración con huecos, las siete leyes del catálogo
  del IEEN que viven en `Nayarit/`, las dos secciones, el rotulado de artículos
  de los reglamentos y la receta de consulta electoral cruzada.
- **Regla del texto anulado**, incorporada a la skill con el caso IEEN 27.
- **Copia publicada de la skill sincronizada** (PR #22, 16 de noviembre). La
  afirmación de que le faltaban la regla de los enlaces `actual/` y la de no
  advertir sobre cotejo era incorrecta: ambas estaban. Lo que le faltaba era el
  IEEN y la nota de copia publicada, ya resuelto. Las tres copias —instalada en
  Claude, instalada en Codex y publicada— tienen hoy cuerpo idéntico.
- **Control de enlaces huérfanos de Nayarit**: `_clave` y `_huerfanos` están
  implementados y `enlace_fuera_del_catalogo` figura en las categorías del
  reporte. Verificado en el código; sus pruebas pasan. Este archivo lo seguía
  pidiendo.
- **Nayarit 75** actualizado el 11 de noviembre a la enmienda del 18 de
  septiembre de 2026, versión anterior conservada e índices regenerados.
- **Nayarit 78** marcada abrogada con evidencia textual y página, cruzada en
  ambas direcciones con la **140** que la sustituye.
- **Normas fiscales de Nayarit**: ids 141 y 142 incorporados.
- **Reproducibilidad de `remisiones.json`**: corregida. Regenerar los cuatro
  acervos reproduce el contenido versionado salvo el campo `generado` y la
  clave `secciones`.
- **Identidad de la LJEN del catálogo del IEEN**: `YA_EN_LA_BIBLIOTECA` la
  mapea a Nayarit 79, cuyo nombre de catálogo es «Ley de Justicia Electoral
  para el Estado de Nayarit». Identidad confirmada; queda el cotejo de versión
  contra el archivo `LJEN-07102020.pdf`.

## Lo que las auditorías verificaron y está bien

Conviene no perderlo de vista al leer la lista de arriba:

- Los **646 originales presentes coinciden con su SHA-256 declarado**, sin una
  sola discrepancia, incluidos los históricos.
- En los **799 ordenamientos** con `actual.json`, el enlace resuelve al
  directorio declarado. Cero enlaces rotos.
- Los marcadores `PAGINA_PDF` van de 1 a N sin huecos en todos los textos
  vigentes, y N coincide con `paginas_pdf` de `validacion.json`. En Federal y
  Sinaloa los 24,935 pies «N de M» impresos coinciden con el marcador; solo
  IEEN 117 desfasa uno por portada.
- Las **121,182 entradas de índice** tienen `pagina_pdf` igual al último
  marcador anterior a su `linea_inicio`.
- Las 304 portadas federales con «Última Reforma DOF» coinciden con
  `ultima_reforma.fecha`.
- Las cuatro suites de pruebas existentes pasan.
- El tratamiento de los no promovidos del **IEEN** —rótulo explícito en el
  texto, `validacion` coherente, exclusión de índices— es el modelo que Federal
  debería copiar.
