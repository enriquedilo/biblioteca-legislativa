# Corte de lotes 11–15

- Cinco lotes de diez completados y publicados individualmente en federal.
- Total acumulado: 154/453 ordenamientos; 50 nuevos. Restan 299, comenzando por lote 16.
- Páginas: 11307 acumuladas; 3460 nuevas.
- Originales actuales con SHA-256 y URL individual comprobados: 308.
- Pendientes por falta de PDF/texto: 0. Incidencias de descarga/formato Word: 0.

## Ajuste exclusivo de metadatos anteriores

Se descartaron 41 entradas de abroga con todos los campos null en 29 documentos, incluido ID 5 (CFPC). Se preservan entradas que contienen algún dato y la evidencia literal de las cláusulas; los índices de incidencias se ajustan al arreglo filtrado. Las 154 versiones actuales carecen de entradas completamente nulas.

Se crearon versiones nuevas solo para esos 29 documentos; los otros 75 del corte anterior permanecen sin modificar. Versiones anteriores intactas, originales/texto/extracción idénticos byte a byte, y restantes campos de metadata sin cambios (excepto version). No se volvió a convertir ningún documento anterior. Detalle e IDs en ajuste-metadata-abrogacion.json.

## Abrogación programada

Campo abrogacion_programada añadido a los 50 nuevos documentos y a las 29 versiones de metadatos ajustadas, conforme al alcance indicado. Es objeto con decreto_dof, fecha_dof, fecha_fin_vigencia y evidencia cuando la portada declara abrogación o término cierto de vigencia; null en caso contrario. No se completan datos ausentes ni se extrae esta declaración de disposiciones del cuerpo que abrogan otras leyes.

CFPC: decreto_dof = Decreto por el que se expide el Código Nacional de Procedimientos Civiles y Familiares; fecha_dof = 2023-06-07; fecha_fin_vigencia = 2027-04-01. Portada PDF página 1 cotejada visualmente. Evidencia: Código Abrogado, en un plazo que no exceda del 1o. de abril de 2027, por Decreto DOF 07-06-2023. Se registra como límite máximo condicionado a entrada gradual y declaratorias; no se afirma una fecha única de entrada en vigor. Los restantes casos ajustados y nuevos contienen null, sin inferencias.

## Controles y continuidad

Verificados integridad de originales, enlaces actual, identidad de versión, marcadores correlativos y conservación del contenido/signos/listas en todas las páginas. Slugs numéricos del nombre oficial y archivo_origen comprobados. Diferencias Word/PDF y metadatos ausentes permanecen registrados; pypdf informativo y no bloqueante. No se afirma cotejo visual exhaustivo de los lotes.

Avance persistido por documento y push por lote, sincronizando main sin publicación forzada. Originales y extraccion.txt locales excluidos de Git; inventario en originales-corte-15.json. Sin OCR, LEYFED, índices de búsqueda ni articulado; sin cambios de vigilancia, automatizaciones o skills. Los reportes anteriores permanecen como cortes históricos. PR final al concluir el acervo; merge reservado al usuario.
