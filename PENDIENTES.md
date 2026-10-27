# Pendientes abiertos

Lista corta de lo que falta en la biblioteca, para no depender de la memoria
de una conversación. Quien cierre un punto lo borra de aquí.

Última revisión: 27 de octubre de 2026.

## Decisión de alcance

**Acervo electoral del IEEN y del INE.** Reconocimiento hecho el 26 de octubre
de 2026. El catálogo del Instituto Estatal Electoral de Nayarit publica 51
ordenamientos en `ieenayarit.org/normatividad/IEEN` —8 de legislación local, 13
reglamentos y 30 lineamientos— y 21 más en `/normatividad/Interna`, con 74 PDF
adicionales de acuerdos de reforma colgados como anexos. El arreglo
`documentos` viene embebido como literal de JavaScript dentro del HTML, de modo
que se extrae con una expresión regular, sin navegador. Los PDF son texto
generado desde Word, de 11 a 24 páginas, y responden `Last-Modified`: la
detección barata por cabecera de `bin/vigilancia.py` sirve igual. Los anexos
«A1/A2» son el texto consolidado completo, no la hoja del acuerdo.

Del INE, el enlace de normatividad del IEEN lleva al Compendio Normativo:
23 documentos servidos desde `sidj.ine.mx/restWS…/app/doc/<id>/20/1`, con
identificador numérico estable. Detrás está NormaINE, repositorio de miles de
acuerdos: eso se consulta, no se espeja.

Recomendación: **dos acervos nuevos en este mismo repositorio**, `IEEN` e `INE`,
con la estructura de Sinaloa, Nayarit y Federal, y una vista electoral en la
capa de índices. No una biblioteca aparte: el trabajo electoral cruza la
Constitución federal, la LGIPE, la LGPP, la Constitución de Nayarit y la Ley
Estatal Electoral, que ya están cargadas. Volumen neto estimado: 82
ordenamientos, unos seis lotes de conversión, más un adaptador de catálogo en
`bin/vigilancia.py`.

Falta el visto bueno para empezar, y decidir si se cargan las 74 versiones
históricas o solo el texto vigente con la cadena de reformas anotada en
`metadata.json`.

## Correcciones de conversión

Dos aperturas de artículo quedaron sin marca de encabezado en el Markdown, así
que el texto está pero el artículo no entra al índice ni a las búsquedas:

- **Nayarit 69**, Ley del Fondo de Ahorro para el Retiro Digno, línea 841:
  `Artículo. 45. Régimen laboral.`
- **Nayarit 79**, Ley de Justicia Electoral para el Estado de Nayarit, línea
  1463: `Artículo. 93.- Con independencia de lo establecido…`

En ambos casos el original imprime «Artículo.» con punto intruso. El índice ya
tolera esa errata cuando la línea viene marcada como encabezado; lo que falta
es la marca.

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
