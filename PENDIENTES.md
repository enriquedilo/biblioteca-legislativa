# Pendientes abiertos

Lista corta de lo que falta en la biblioteca, para no depender de la memoria
de una conversación. Quien cierre un punto lo borra de aquí.

Última revisión: 9 de noviembre de 2026.

## Acervo electoral: en construcción

**Decidido el 9 de noviembre de 2026.** Se cargan en este mismo repositorio,
no en una biblioteca aparte: el trabajo electoral cruza la Constitución
federal, la LGIPE, la LGPP, la Constitución de Nayarit y la Ley Estatal
Electoral, que ya están aquí. Alcance acordado:

- **IEEN completo**: los 51 documentos de `ieenayarit.org/normatividad/IEEN`
  y los 21 de `/normatividad/Interna`. De los 51, siete son leyes del Congreso
  de Nayarit que la biblioteca ya tiene por su fuente oficial y no se
  duplican, y el Compendio Electoral 2021 queda fuera por ser una
  recopilación de esas mismas leyes en un PDF de 207 MB. **Neto: 64.**
- **Compendio normativo del INE**: 23 documentos servidos desde
  `sidj.ine.mx/restWS…/app/doc/<id>/20/1`, con identificador numérico estable.
  NormaINE, el repositorio de miles de acuerdos que está detrás, se consulta,
  no se espeja.
- **Solo texto vigente.** Los 75 acuerdos de reforma quedan anotados con su
  fecha y su URL, sin convertir. Si después hace falta un texto anterior, se
  promueve esa versión sin rehacer nada.
- **Los acuerdos del Consejo quedan fuera por ahora.** Son cientos por año y
  son materia de consulta puntual, no de acervo. Se evalúa después.

### Ruta

1. **Catálogo.** `bin/catalogo_ieen.py` lee las dos páginas del IEEN y escribe
   `IEEN/catalogo/normatividad.json` con la versión vigente de cada documento.
   Hecho y probado; falta correrlo y publicar su salida.
2. **Acervo IEEN.** Estructura igual a la de los otros tres acervos y carga en
   lotes de unos doce ordenamientos, con cotejo por lote.
3. **Vigilancia.** Adaptador del catálogo del IEEN en `bin/vigilancia.py`. El
   sitio responde `Last-Modified` y `Content-Length` en los 72 documentos, así
   que sirve la misma detección barata por cabecera.
4. **INE.** Los 23 del compendio, con su propio adaptador de catálogo.
5. **Vista electoral** en la capa de índices, que es regenerable.

### Notas técnicas comprobadas

- El arreglo `documentos` viene embebido en el HTML como literal de
  JavaScript: claves sin comillas, escapes `\/` y `\uXXXX`, coma sobrante
  antes del corchete. Se extrae sin navegador.
- **Los anexos no vienen en orden constante**: unos van del más viejo al más
  nuevo y otros al revés. La versión vigente se elige por fecha, nunca por
  posición en la lista.
- Los PDF son texto generado desde Word, no escaneos, de 11 a 24 páginas. Los
  anexos «A1/A2» son el texto consolidado completo, no la hoja del acuerdo.
- Dos ordenamientos del IEEN apuntan a PDF alojados en el sitio del Congreso
  de Nayarit, y uno pesa 207 MB: los tres quedan resueltos por las reglas de
  arriba.
- Pendiente de confirmar en el primer lote: que «Ley de Justicia del Estado de
  Nayarit» del catálogo del IEEN (`LJEN-07102020.pdf`) sea la Ley de Justicia
  Electoral, que la biblioteca tiene como Nayarit 79.
- Las URL del INE no pudieron verificarse desde el entorno de trabajo porque
  el proxy bloquea `sidj.ine.mx`. Se verifican al llegar al paso 4.

## Vigilancia del catálogo de Sinaloa

Sinaloa sigue sin protección frente al cambio de enlaces: su catálogo se arma con JavaScript desde otro host y su lista no es observable desde el HTML servido. La corrección de enlaces congelados de Nayarit queda documentada en `Nayarit/reportes/actualizacion-enlaces-2026-11-09.md`.

## Auditoría integral — pendiente mayor

**La biblioteca se ha venido corrigiendo a parches, cada uno a raíz del error
que lo destapó.** Han funcionado, pero ninguno nació de una revisión
sistemática: el índice que se detenía en DUODÉCIMO llevaba meses perdiendo
2,651 transitorios, las remisiones salían distintas en cada corrida sin que
nadie lo notara, y cuatro ordenamientos de Nayarit quedaron congelados dos
meses mientras la alerta semanal decía «algo cambió» sin decir qué. Los tres
se descubrieron de casualidad, no por buscarlos.

Hace falta una pasada completa y de una sola vez, antes de que el acervo
crezca más. Lo que debe cubrir, con lo que hoy sabemos:

**Integridad de los punteros.** Cada URL archivada contra el catálogo vigente,
en los cuatro acervos. Incluye resolver la observabilidad del catálogo de
Sinaloa, hoy el único sin protección contra el enlace congelado.

**Vigencia real.** Fecha de última reforma archivada contra la que publica
cada fuente, ordenamiento por ordenamiento. No solo los que cambiaron de
enlace: también los que la fuente actualizó sin que lo notáramos.

**Altas que nunca entraron.** Ordenamientos publicados por los congresos
después de la carga inicial y que no están en el acervo. Hoy no hay ningún
control que los busque.

**Consistencia estructural.** Que `version` sea el SHA-256 del original, que
`actual` resuelva a un directorio existente, que no queden versiones huérfanas
ni `metadata.json` apuntando a un texto que no es el suyo.

**Calidad del articulado.** Los 398 números de artículo duplicados dentro de
un mismo ordenamiento; aperturas de artículo sin marcar; transitorios que
absorben el resto del documento —el último de Nayarit 139 carga 18,665
caracteres—; las notas del DOF, las declaratorias de invalidez de la SCJN y la
tabla de la LIGIE, todas sin anclar.

**Reproducibilidad.** Que regenerar los índices dos veces produzca exactamente
lo mismo. Se corrigió en `remisiones.json`; falta comprobar el resto de la
capa.

**El proceso, no solo el dato.** Por qué una alerta se cerró dos veces como
ruido. Una alerta que no se puede accionar enseña a ignorar la alarma, y ese
es el fallo más caro de todos.

## Skill

El acervo del IEEN obliga a actualizar la skill `biblioteca-legislativa` en
dos momentos:

1. **Al fusionar el primer lote**: la descripción, que hoy dice «Sinaloa,
   Nayarit y Federal». Es lo que decide si la skill se activa; sin ese cambio
   una pregunta por un reglamento del IEEN puede no invocarla.
2. **Al terminar los 64**: conteos reales, la numeración con huecos, que
   siete números del catálogo del IEEN corresponden a ordenamientos de
   Nayarit y no a IEEN, las dos secciones, el rotulado de artículos de los
   reglamentos —que se conoce con el lote 1— y la receta de consulta
   electoral cruzando Nayarit, Federal e IEEN en bloques rotulados.

La skill instalada se actualiza con una tarjeta de revisión, no editando
archivos. La copia de `skill/biblioteca-legislativa/SKILL.md` está
desincronizada: hoy tiene una estructura vieja, de tres entidades, sin la
regla de los enlaces `actual/` ni la de no advertir sobre cotejo. **Decidido:
el repositorio queda público y se publica todo**, así que esa copia se deja
idéntica a la instalada, con una nota de que es copia publicada y no la
fuente.

## Calidad del índice

- **398 números de artículo duplicados** dentro de un mismo ordenamiento
  (Sinaloa 171, Nayarit 7, Federal 220). Sin diagnosticar. Parte serán
  ordinales impresos repetidos en listas finales de decretos, parte errores de
  segmentación.
- **Federal**: las notas explicativas `Reforma DOF …`, las declaratorias de
  invalidez de la SCJN y la tabla arancelaria de la LIGIE siguen sin anclarse a
  artículo.

## Infraestructura

- **Enero de 2027**: el token de acceso personal de GitHub vence a mediados de
  enero. Quedó acordado no regenerar otro, sino pasar la autenticación al
  GitHub CLI (`gh auth login`), que guarda una credencial que se renueva sola
  en el llavero del Mac, y revocar el token viejo.
- El cron de la vigilancia está puesto los lunes a las 14:17 UTC, pero las
  corridas caen entre cinco y ocho horas después. Es la cola de GitHub para
  tareas programadas, no una falla del flujo.
