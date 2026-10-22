# Conversión semanal del 20 de octubre de 2026

Cierre documentado el 21 de octubre. Estado: PR borrador para cotejo del usuario, sin incorporación a main.

Fuente: vigilancia/reporte.md, corrida 2026-10-19 20:10 UTC, commit 17c6db4. Se procesaron exclusivamente Sinaloa 9 y Nayarit 16, 55 y 139, los ocho originales reportados. No hubo detección adicional ni fuentes externas. El PR #6 anterior ya estaba incorporado en main; no había PR abiertos al iniciar.

## Resultado y alcance

| Entidad / ID | Ordenamiento | Páginas | Resultado |
|---|---|---:|---|
| Sinaloa 9 | Constitución Política del Estado | 196 | Conversión conservada; cambios en transitorios de reforma judicial |
| Nayarit 16 | Ley de Atención y Protección a Migrantes y sus Familias | 35 | Cambios en artículos 6 y 76 y nuevo bloque de transitorios |
| Nayarit 55 | Ley Electoral | 175 | Cambios en 11 artículos de contenido; notas y entradas de índice distinguidas |
| Nayarit 139 | Ley Municipal | 162 | Cambios de contenido en 12 artículos; varios bloques transitorios incorporados |

Todos tienen texto extraíble. Sin OCR. Versiones anteriores intactas; ocho originales nuevos respaldados permanentemente en la Mac y excluidos de GitHub. Los hashes coinciden con los prefijos publicados por la vigilancia. Los JSON de comparación conservan texto anterior/nuevo y páginas; resumen.json distingue resultados automáticos de su clasificación revisada.

## Sinaloa 9

No se identificaron cambios sustantivos en los artículos permanentes. La diferencia del rango del artículo 4 es la posición de la nota al pie respecto del título I Bis; la del 140 es el escape Markdown del punto de «138.». No se presentan como reformas de esos artículos.

Sí cambian los transitorios del **Decreto 86, publicado el 6 de junio de 2025**, reformados por **Decreto 509, P.O. 121 del 9 de octubre de 2026**:

- Segundo: elección judicial de 2027 pasa a 2028 y se elimina «ordinaria» en esa referencia.
- Cuarto: inicio del Tribunal de Disciplina Judicial/Órgano de Administración y extinción del Consejo ligados al proceso de 2028; incorpora Magistradas.
- Quinto: elección de 2028, con escalonamiento de magistraturas por 2, 5 y 8 años, en lugar de 3, 6 y 9.
- Sexto: continuidad de Salas de Circuito hasta toma de protesta derivada de elección de 2028; incorpora Magistradas.
- Séptimo: adecuaciones legislativas con anticipación al proceso de 2028.
- Octavo: referencia al haber de retiro para quienes concluyan por no postularse/no ser electos cambia de 2027 a 2028.

El propio Decreto 509 agrega dos transitorios: Primero, entrada en vigor al día siguiente de la publicación; Segundo, derogación de disposiciones opuestas. Se incorpora su entrada a la lista final de reformas. No se emparejan ordinales de distintos decretos por el solo número.

Incidencias de metadatos: la publicación original es seriada (números 78–84, varias fechas de julio de 1922); el objeto singular queda null y conserva evidencia de página 1. El extractor seleccionaba una mención interna de «reformas» como encabezado: se recuperó la lista desde el encabezado exacto. Contiene 199 entradas aunque llega al ordinal 192, por números repetidos 3 y 116–121; se conserva ese dato impreso sin renumerar. Campos no identificados inequívocamente siguen null.

## Nayarit 16

- Artículo 6: los Ayuntamientos contarán preferentemente con una oficina de atención a personas migrantes.
- Artículo 76: ajusta fracción V; nueva fracción VI sobre oficina de atención; la anterior VI se recorre a VII.

Nuevo bloque P.O. 2 de octubre de 2026: Primero, entrada en vigor al día siguiente; Segundo, mecanismos municipales de atención/asesoría sin presupuesto adicional; Tercero, comunicación a los veinte Ayuntamientos. No hay artículos completos añadidos o eliminados.

Publicación original recuperada literalmente: Sección Cuarta, 21 de diciembre de 2018. El extractor omitía la frase por no terminar en punto. No se alteró el original.

## Nayarit 55

Cambios de contenido por artículo, respecto de la versión archivada:

| Artículo | Diferencia observada |
|---|---|
| 23 | Cinco pasa a cuatro en la regla de integración correspondiente; incorpora igualdad sustantiva y perspectiva de género. |
| 66 | Plazo de convenio de candidatura común vinculado al inicio de precampaña; modificación hasta un día antes del registro. |
| 67 | Detalla cargos de candidaturas comunes, representación proporcional y redacción incluyente. |
| 86 | Suprime obligatoriedad de circulares/proyectos señalados y añade renovación de integrantes/presidencias de comisiones. |
| 87 | Titularidad de presidencia y procedimiento de propuestas/nombramientos de secretaría, direcciones y áreas ejecutivas. |
| 89 | Cambia formulación de secretaría y elimina referencia a antigüedad mínima de cinco años. |
| 89 Bis | Límites de remuneración y prohibiciones de prestaciones/seguros financiados con recursos públicos. |
| 90 | Integración y atribuciones de Junta Estatal Ejecutiva, designación de personal y excepciones. |
| 92 | Requisitos de titulares de direcciones: edad de 25 a 30, licenciatura, experiencia y demás condiciones impresas. |
| 227 | Incorpora Comisión de Quejas y Denuncias entre órganos competentes y ajustes de redacción. |
| 239 | Trámite del proyecto ante Comisión de Quejas y Denuncias, devolución y nueva propuesta, antes de votación del consejo. |

88, 91 y 238 muestran notas de reforma/elementos contiguos sin cambio sustantivo de su cuerpo en la comparación. **107 y 209 no son artículos nuevos:** sus textos completos ya estaban absorbidos en rangos 106 y 208; se comprobó que el texto de cada entrada nueva está íntegro en el rango anterior. Se recuperan como encabezados/entradas propias con el conversor vigente, sin alterar las versiones históricas. No se reporta eliminación de artículos.

Nuevo bloque P.O. 28 de septiembre de 2026: Primero, vigencia al día siguiente; Segundo, armonización de reglamentos/acuerdos/lineamientos por el Instituto dentro de 30 días naturales; Tercero, derogación de disposiciones opuestas.

## Nayarit 139

Cambios de contenido por artículo respecto de la versión archivada; no se atribuyen todos al último decreto, pues la fuente incorpora también notas de fechas anteriores:

| Artículo | Diferencia observada |
|---|---|
| 2 | Presidenta/Presidente, sindicatura y hasta quince regidurías; paridad vertical/horizontal e igualdad sustantiva. |
| 30 | Integración del Ayuntamiento bajo las reglas anteriores. |
| 50 | Acceso público a sesiones, transmisión por medios electrónicos y atención de imposibilidad técnica antes de siguiente sesión. |
| 57 | Apartados del orden del día de sesiones de Cabildo. |
| 61 | Bases reglamentarias municipales para atención y asesoría a migrantes. |
| 108 | Designaciones con paridad, igualdad sustantiva y perspectiva de género; redacción incluyente. |
| 111 | Requisitos/impedimentos y tratamiento del expediente de personas servidoras públicas. |
| 119 | Vigilancia de publicitación/transmisión de Cabildo y recorrido de fracciones. |
| 172 | Actualiza denominación de la ley de adquisiciones/arrendamientos/prestación de servicios aplicable. |
| 196 | Actualiza referencia a esa misma legislación. |
| 258 | Ajustes de redacción y puntuación del procedimiento; no se infiere un nuevo alcance jurídico. |
| 267 | Redacción sobre titularidad de cargo y Presidenta/Presidente. |

29, 56, 107, 118, 171 y 195 tienen diferencias de notas/elementos contiguos sin modificación sustantiva detectada en el cuerpo. Sin artículos completos nuevos o eliminados.

Bloques transitorios añadidos, identificados por fecha y contexto:

- **21 de agosto de 2026:** Único, entrada en vigor al día siguiente de publicación.
- **2 de octubre de 2026 — migrantes:** Primero, entrada en vigor; Segundo, mecanismos de atención sin recursos adicionales; Tercero, comunicación a veinte Ayuntamientos. La ausencia de punto tras «Tercero» se conserva.
- **2 de octubre de 2026 — integración municipal:** Primero, entrada en vigor; Segundo, hasta quince regidurías a partir del siguiente periodo constitucional, respetando integración actual; Tercero, derogación de disposiciones opuestas; Cuarto, armonización municipal dentro de 120 días naturales; Quinto, comunicación a Ayuntamientos.

No se mezclan los dos bloques del 2 de octubre ni se fabrican números de decreto ausentes.

## Controles, incidencias y pendientes

568 páginas verificadas contra el Markdown efectivamente guardado: conservación de caracteres no blancos y secuencias de cifras por página. Conservación íntegra incluye fracciones y transitorios; el pipeline de Nayarit añade verificación de inicios de listas. Regenerados índices, FTS, remisiones y rutas de ambas entidades, con comprobación de destinos, rangos y páginas.

Cotejo visual limitado a Sinaloa 9 p.169; Nayarit 16 p.33, 55 p.169 y 139 p.158. Los pasajes coinciden con la extracción. No se declara cotejo visual integral ni apertura de los decretos originales del Periódico Oficial. Las compilaciones administrativas no sustituyen esa publicación para uso formal.

Persisten diferencias Word/PDF y del orden de cifras entre lectores, registradas sin reparar. Sinaloa: 183 marcadores Word y 185 PDF, mismos identificadores pero ocurrencias distintas. Nayarit Electoral presenta muchas discrepancias del control entre lectores. No equivalen a pérdidas del Markdown, cuya conservación contra Poppler pasó, pero deben considerarse en el cotejo. Los datos ausentes y abrogaciones no identificables quedan null/arreglos con evidencia e incidencias. El PR queda en borrador para esa revisión, sin modificar main.

### Campos incompletos registrados

- Sinaloa 9: abroga, decreto_numero, po_publicacion, po_publicacion.edicion, po_publicacion.fecha, po_publicacion.numero, reformas.numeracion_impresa, reformas[].fecha, reformas[].po_numero, ultima_reforma.edicion.
- Nayarit 16: abroga, decreto_numero, po_publicacion.edicion, po_publicacion.numero, reformas[].decreto, reformas[].po_numero, ultima_reforma.edicion, ultima_reforma.numero.
- Nayarit 55: abroga, abroga[].nombre, abroga[].po_numero, decreto_numero, po_publicacion.edicion, po_publicacion.numero, reformas[].decreto, reformas[].fecha, reformas[].po_numero, ultima_reforma.edicion, ultima_reforma.numero.
- Nayarit 139: abroga, abroga[].nombre, abroga[].po_numero, po_publicacion.edicion, po_publicacion.numero, reformas[].decreto, reformas[].po_numero, ultima_reforma.edicion, ultima_reforma.numero.

SHA-256 del reporte de vigilancia: 044281193a0f52a18c241f8625a3ad38f29629fd93991827d9d5eac7163ec53a
