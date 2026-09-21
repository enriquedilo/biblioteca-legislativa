# Piloto Federal

Desde la raíz del repositorio, con Python que disponga de pypdf y Pillow, y Poppler instalado:

1. `python3 bin/federal/piloto.py`: captura catálogo desde las capturas HTML existentes y procesa únicamente los cuatro documentos seleccionados, guardando estado tras cada uno. Descarga cada URL individual; reutiliza descargas locales de preparación. Reutiliza controles de `bin/nayarit` sin modificar esa entidad.
2. `python3 bin/federal/revision.py`: compara ocurrencias de cifras de ambos lectores y genera muestras visuales locales en `work/piloto_visual/` y resumen en `work/resumen.json`.
3. Revisar visualmente las muestras y sus extracciones antes del cierre. `cerrar_piloto.py` registra el cotejo efectuado en esta corrida; no debe ejecutarse sin esa revisión. Comprueba hashes, marcadores, enlaces y conservación.

Resultados y límites del piloto: `Federal/reportes/piloto.md`. La continuación autorizada usa lotes.py, descrito abajo. No construyen índices ni articulado.

## Lotes y corte vigente

El piloto y el corte de cinco lotes fueron aprobados. Los lotes 1–45 están publicados. `lotes.py` persiste cada intento, recupera publicaciones interrumpidas y sincroniza federal antes del push, incorporando main sin reescribir commits publicados. El control pypdf es informativo.

Captura concluida: 453 intentados, 447 incorporados y seis pendientes sin promover (372, 413, 414, 416, 444 y 446). No quedan registros sin intentar. El 444 no tiene texto extraíble; los otros cinco fallaron conservación. No reparar ni aplicar OCR; 372 expresamente ratificado por el usuario. Para avanzar cinco lotes: `python3 bin/federal/lotes.py --lotes 5`. Si el usuario ordena detenerse, registrar la barrera reanudar_requiere_instruccion_usuario y usar --reanudar únicamente tras una instrucción posterior de continuación.

Slugs: cuando la sigla de origen sea numérica, incluidos sufijos numéricos de fecha, derivar del nombre oficial mediante slug_nombre; conservar sigla y archivo_origen. Si nombre_oficial no está cotejado, slug null con incidencia. Los siete casos señalados por el usuario y los dos casos anteriores con sufijo de fecha se ajustaron creando nuevas versiones de metadatos; originales y texto permanecen idénticos. Reporte: ajuste-slugs-numericos.json.

Informe e inventario: `Federal/reportes/corte-lotes-41-45.md` y `originales-corte-45.json`. Los enlaces locales actual deben ser enlaces simbólicos; el clon principal tiene core.symlinks=false y un rebase puede representarlos como archivos. Verificar/restaurar al destino exacto de actual.json sin tocar originales ni textos.

## Abrogación: metadatos

`metadatos.ajustar` elimina entradas de abroga totalmente null, remapea los índices de incidencias y conserva evidencia impresa. Extrae abrogacion_programada de la portada, antes del cuerpo/preambulo histórico; objeto con decreto_dof, fecha_dof, fecha_fin_vigencia y evidencia, o null sin declaración. No infiere término anual a partir de ejercicio fiscal ni confunde abroga (otras normas) con la abrogación del propio ordenamiento. Fecha límite impresa se registra con su condición literal en validacion.json.

`python3 bin/federal/metadatos.py --corregir-existentes` corrigió solo ID 5 y los documentos con entradas de abroga vacías: 29 documentos, 41 entradas. Se crearon versiones nuevas de metadatos y se comprobaron originales/texto/extracción idénticos. Los otros 75 del corte anterior permanecen sin modificar; el nuevo campo se añade también a cada documento de los lotes 11 en adelante. Estado y reporte por documento permiten retomar la corrección tras una interrupción. Detalle: ajuste-metadata-abrogacion.json.

## Encabezados compuestos

`bin/encabezados.py` comparte el reconocimiento conservador de sufijos ordinales y serie numérica, plural Artículos de un solo número y abreviaturas ordinales impresas. Los conversores de Nayarit/Federal y Sinaloa lo usan conservando el rótulo literal, salvo la normalización de comas de millar expresamente autorizada en Federal. La corrección histórica se conserva en versiones nuevas, con evidencia de página en validacion.json y resumen en correccion-encabezados-compuestos.json de cada entidad. LFDA ID 169: errata impresa Artículos 135.- preservada. Índices/articulado no regenerados; sus rutas históricas se conservan hasta esa fase separada.

La detección usa una palabra de sufijo abierta (incluye acentos), con serie opcional y delimitador. Admite rangos plurales impresos como Artículos 60 al 68.- sin expandirlos. Ver correccion-sufijos-abiertos.json y cotejo-id223.json. La portada del ID 223 declara invalidez de la abrogación y recuperación de vigencia; no se infiere una fecha de fin.

Corrección del criterio: una abrogación cuyo decreto se declaró inválido no es abrogación vigente. ID 223: abrogacion_programada null; vigencia_recuperada con fecha_publicacion_sentencia 2023-11-24, decreto_invalidado y evidencia. Revisión de 304 portadas registrada en revision-vigencia-recuperada-304.json; notas de artículos/títulos no se interpretan como recuperación de la ley completa. IDs 203 y 281 declaran invalidez del decreto de expedición; quedan señalados para revisión del alcance, sin eliminar documentos.

Antes del lote 36 se revisaron los 354 publicados: 1,297 aperturas corregidas y nuevas versiones para 33 documentos, incluidos títulos y tipos. Se acepta Artículo N en línea completa sin puntuación y Artículo. N con punto impreso tras la palabra. En Federal se normaliza la coma de millar del número de encabezado, con literal y página de evidencia. ID 317 artículo 88 cotejado visualmente en página 34. Reporte: correccion-formatos-354.json.

Cierre 41–45: ID 377 conserva «. Artículo 40.» como encabezado y errata, con nueva versión. Auditoría de 403 documentos sin otros casos de puntuación suelta; ver correccion-puntuacion-403.json. Los seis pendientes se documentan con URL y SHA-256 en pendientes-finales.json, sin promoción. Los 447 incorporados incluyen 23,824 páginas y 894 originales verificados; seis originales de pendientes conservados aparte. La captura está cerrada y la integración se propone por pull request, sin merge automático.
