# Informe del piloto federal

## Resultado

Cuatro PDF y cuatro originales .doc descargados individualmente; sin LEYFED, OCR, índices de búsqueda ni articulado. 928 páginas. Integridad SHA-256 y correspondencia de actual.json/enlace actual verificadas. Todos los controles de conservación de contenido, signos e inicios de listas del PDF extraído al Markdown pasan. Marcadores de página completos.

Captura oficial: 316 entradas principales y 137 reglamentos (453), frente a la estimación de 317/127. Se capturaron únicamente filas numeradas con enlace al documento vigente en index.htm y regla.htm; no se siguieron índices de abrogados. El alcance se debe revisar antes de lotes.

## Límites e incidencias

Hay diferencias de extracción entre Word y PDF en los cuatro documentos; en CPEUM y CFF difiere la secuencia de encabezados reconocidos, aunque el conjunto de identificadores coincide en los cuatro documentos. La secuencia de cifras entre Poppler y pypdf difiere en muchas páginas. Aun sin exigir orden, difieren las ocurrencias numéricas en 28 páginas: CPEUM 14, CFF 12, LGDNNA 1 y Reg_CFF 1. No se han reparado ni certificado equivalentes. Ver verificacion_piloto.json y validacion.json de cada versión para páginas y controles.

Cotejo visual por muestra: primera página, inicio de transitorios y última página de cada PDF (12 páginas); no exhaustivo. Las notas de reforma conservan texto literal y todas las fechas reconocidas en fechas; fecha escalar null cuando son varias. Reglamento sin notas de reforma identificadas; ultima_reforma null. Campos no impresos quedan null con incidencias. Abrogaciones expresas se capturan automáticamente como evidencia pendiente de cotejo, sin completar datos ausentes.

Las primeras conversiones preparatorias de CPEUM, CFF y LGDNNA omitieron Word por un defecto de selección de enlace. Se corrigió la selección y se crearon versiones nuevas con ambos originales; se conservan las versiones preparatorias sin sobrescribirlas. Las versiones actuales son las del reporte de verificación.

Originales y extraccion.txt permanecen en la Mac y están excluidos de Git según la política existente. SHA-256 y URL de cada original constan en metadata.json. La publicación en la rama federal conserva textos, metadatos, controles y avance, pero los binarios locales requieren respaldo independiente.

## Continuación

Piloto detenido. No se iniciaron lotes. Antes de escalar deben revisarse alcance y diferencias de extracción. El estado se guarda tras cada documento en AVANCE.md y reportes/avance_lotes.json. El controlador de lotes de diez y sus pushes se implementará al autorizar la continuación; el piloto no ejecuta lotes. No se modifican vigilancia, automatizaciones, skills ni las entidades estatales. PR final al concluir el acervo; merge reservado al usuario.
