# Revisión de los 13 documentos señalados

Estado inicial de la revisión dirigida (véase actualización del 10 de septiembre al final): se aclararon las incidencias puntuales de 10 documentos. Tres requieren trabajo adicional: dos presentan diferencias de numeración entre originales y uno contiene fórmulas gráficas ausentes del Markdown. Esto no constituye validación integral de los 151 documentos.

## Páginas sin contenido normativo

Se confirmó visualmente que las páginas siguientes están vacías salvo la paginación, cuando aparece:

| ID | Ordenamiento | Página del PDF |
|---|---|---:|
| 24 | Coordinación Fiscal | 30 |
| 48 | Justicia Administrativa | 64 |
| 56 | Trabajadores al Servicio de los Municipios | 30 |
| 59 | Movilidad Sustentable y Seguridad Vial | 195 |
| 163 | Fomento y Protección del Maíz Nativo | 12 |
| 165 | Orgánica del Centro de Conciliación Laboral | 24 |
| 167 | Protección de Personas Defensoras de Derechos Humanos y Periodistas | 53 |
| 173 | Revocación de Mandato | 28 |

No se requiere OCR para estas páginas. Coordinación Fiscal tiene, además, una incidencia distinta de fórmulas descrita más abajo.

## Referencias confundidas con artículos

Se cotejaron los pasajes impresos y se retiró el formato de encabezado añadido por error a estas referencias en el Markdown, sin eliminar sus palabras:

- Hacienda, ID 43, página 60: referencia al artículo 2899 del Código Civil, dentro del artículo 52, inciso d).
- Regularización de Predios Rurales, ID 74, página 4: referencia al artículo 194 de la Ley del Notariado, dentro del artículo 16.
- Reglamentaria del Artículo 154, ID 133, página 2: referencia al artículo 154 de la Constitución, dentro del artículo 5o.
- Coordinación Fiscal, ID 24, página 36: referencia al artículo 3º Bis A, dentro del transitorio décimo séptimo. La detección inicial no trataba de la misma forma «3o» y «3º».

## Tres documentos con trabajo pendiente

**Instituto de Evaluación Educativa, ID 85, y Fondo para equipo de cómputo escolar, ID 121.** Los PDF muestran en sus primeras páginas «11, 21, 31…» donde los Word contienen «1, 2, 3…». Se confirmó la impresión del PDF mediante imagen, de modo que la diferencia no es sólo un error del extractor. Se conservó la numeración del PDF y se añadió una advertencia al inicio de cada Markdown. No se infirió una renumeración. Antes de cerrar estas discrepancias debe cotejarse la publicación oficial correspondiente.

**Coordinación Fiscal, ID 24.** La fórmula del artículo 3o Bis A, página 3, está visible en el PDF y ausente del texto extraído. El Markdown tiene ahora una advertencia expresa y la validación registra que el documento completo no está íntegramente convertido. Debe recuperarse esa fórmula y revisarse el resto de fórmulas y elementos gráficos de la ley. Para cálculos, utilizar el PDF original.

## Consecuencia para los controles de la biblioteca

Los controles anteriores comprobaron la conservación del texto extraíble. No prueban por sí solos que se hayan conservado ecuaciones, imágenes o tablas. Antes de declarar verificada la biblioteca completa, debe incluirse un control de esos elementos, además del cotejo visual y de artículos, fracciones y transitorios. Los demás documentos siguen con su revisión general pendiente.

## Archivos y trazabilidad

Se conservaron los originales y las conversiones previas en `conversiones_anteriores/antes_revision_incidencias`. Se actualizaron las fichas de validación, metadata, el índice y el avance. El detalle estructurado está en [revision_13_incidencias.json](revision_13_incidencias.json).

La descarga sigue completa: 151 documentos. No se consultó nuevamente el catálogo ni se activó una actualización periódica durante esta revisión local.

[Volver al índice](../INDICE.md) · [Consultar avance](../AVANCE.md)

## Actualización del 10 de septiembre de 2026 — Fondo, ID 121

Se cotejaron y corrigieron únicamente los nueve primeros encabezados con el [PDF oficial del IIP](https://iip.congresosinaloa.gob.mx/docs/le/097.pdf). La secuencia del Markdown es ahora 1°–9°, 10–23. Se conservaron originales, conversión previa, PDF de referencia y registro de correcciones con hash. El resto del cuerpo y los transitorios no cambió. La referencia interna «artículo 51» está en ambos PDF y se conservó expresamente. La incidencia de los nueve encabezados queda aclarada; el cotejo general sigue pendiente.

## Cierre dirigido del 10 de septiembre de 2026 — Instituto y Coordinación Fiscal

**ID 85:** nueve encabezados y la referencia al artículo 3° constitucional del artículo 6(I) cotejados con páginas 5–10 del Periódico Oficial No. 120 de 5 de octubre de 2007. Diez correcciones, originales y conversión previa conservados.

**ID 24:** los 46 elementos de imagen detectados están contenidos en 11 páginas (3–8 y 10–14). Se preservaron esas páginas completas como imágenes vinculadas en sus secciones del Markdown. La recuperación es visual; no se declara conversión de las fórmulas a texto matemático. El Word contiene ecuaciones, pero el conversor disponible las omite. Al entregar el Markdown a una IA debe adjuntarse también el PDF original. El cotejo general de la biblioteca sigue pendiente.

## Preparación de pruebas

Coordinación Fiscal: las 46 apariciones de fórmulas y símbolos se restituyeron como LaTeX, en suplementos al inicio de cada página afectada. Se conservaron las imágenes como respaldo. Los huecos del cuerpo extraído deben leerse junto con esos suplementos.

La inspección adicional de imágenes de los 151 PDF detectó una tabla en Pensiones (ID 65, página 36): preservada como imagen y señalada como no transcrita a datos. No se incluyen cálculos con esa tabla en las pruebas.

Se preparó PRUEBA_01 con cinco archivos y preguntas de control. Las comprobaciones son locales; aún falta ejecutar las consultas en ChatGPT o Claude. La revisión visual integral de los 151 documentos no está certificada.
