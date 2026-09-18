# Corte de lotes 21–25 y corrección de encabezados

- Cinco lotes de diez completados y publicados individualmente en federal.
- Total acumulado: 254/453 ordenamientos; 50 nuevos. Restan 199, comenzando por lote 26.
- Páginas: 17054 acumuladas; 2973 nuevas.
- Originales federales actuales verificados mediante SHA-256 y URL individual: 508.
- Incidencias de descarga/formato Word: 0. Pendientes por falta de PDF o texto: 0.

## Encabezados corregidos

El detector reconoce Bis, Ter, Quáter, Quinquies, Sexies/Sexties, Septies, Octies, Nonies y Decies, con serie numérica opcional, así como Artículos seguido de un solo número. También conserva las abreviaturas ordinales impresas 1ro., 2do., 3ro. de Nayarit. Exige delimitador de apertura y rechaza plurales con enumeración y remisiones en minúscula; no infiere encabezados por simples menciones dentro de párrafos.

El cotejo por página encontró 618 aperturas en 31 documentos federales, 25 en los seis IDs indicados de Nayarit y una en Sinaloa ID 23 (644 en total, 38 documentos). El conteo supera la estimación inicial de 530/20/1: incluye variantes en mayúsculas, encabezados pegados a notas y dos encabezados truncados antes del dígito de serie. Se registran los IDs, versiones y cantidades en correccion-encabezados-compuestos.json, y cada apertura literal y página en validacion.json de la nueva versión.

Se crearon versiones nuevas sin alterar originales ni extracción. Se comprobó igualdad de todos los caracteres no blancos del Markdown por página, retirando exclusivamente marcas de encabezado y escapes de Markdown. No se alteraron cifras, notas, erratas ni palabras. Versiones anteriores intactas. LFDA ID 169 conserva literalmente «Artículos 135.-» y registra la errata de la compilación oficial en página 30. Sinaloa ID 23 cotejado contra pdftotext de la página 25 del original; su extracción histórica usa otra segmentación de páginas.

Los nuevos lotes usan el detector corregido. Los controles positivos y negativos cubren numeración compuesta, plural de un número, ordinales impresos y remisiones que no deben ser encabezados. No se generaron archivos de articulado ni índices de búsqueda; los índices previos de las entidades estatales siguen apuntando a sus versiones históricas hasta la actualización de esa capa por separado.

## Conservación y continuidad

Verificados integridad de originales, enlaces actual, identidad de versión, marcadores correlativos y conservación de contenido/signos/listas en las 254 versiones federales actuales. Conservados slugs de nombre oficial para siglas numéricas, archivo_origen, descarte de abroga totalmente null y abrogacion_programada conforme al alcance vigente. Controles pypdf informativos, sin reparación por diferencias de lectores. No se afirma cotejo visual exhaustivo ni vigencia jurídica certificada.

Avance persistido por documento y push por lote, sincronizando main sin publicación forzada. Originales y extraccion.txt locales excluidos de Git; inventario en originales-corte-25.json. Sin OCR ni LEYFED; sin cambios de vigilancia, automatizaciones o skills. Reportes previos conservados. PR final al concluir el acervo; merge reservado al usuario.
