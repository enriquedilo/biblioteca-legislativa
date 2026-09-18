# Piloto Federal

Desde la raíz del repositorio, con Python que disponga de pypdf y Pillow, y Poppler instalado:

1. `python3 bin/federal/piloto.py`: captura catálogo desde las capturas HTML existentes y procesa únicamente los cuatro documentos seleccionados, guardando estado tras cada uno. Descarga cada URL individual; reutiliza descargas locales de preparación. Reutiliza controles de `bin/nayarit` sin modificar esa entidad.
2. `python3 bin/federal/revision.py`: compara ocurrencias de cifras de ambos lectores y genera muestras visuales locales en `work/piloto_visual/` y resumen en `work/resumen.json`.
3. Revisar visualmente las muestras y sus extracciones antes del cierre. `cerrar_piloto.py` registra el cotejo efectuado en esta corrida; no debe ejecutarse sin esa revisión. Comprueba hashes, marcadores, enlaces y conservación.

No existe entrada que inicie lotes. Resultados y límites: `Federal/reportes/piloto.md`. Los scripts son piloto; requieren extensión y revisión antes de escalar. No construyen índices ni articulado.

## Lotes y corte vigente

El piloto y el corte de cinco lotes fueron aprobados. Los lotes 1–25 están publicados. `lotes.py` persiste cada intento, recupera publicaciones interrumpidas y sincroniza federal antes del push, incorporando main sin reescribir commits publicados. El control pypdf es informativo.

El usuario solicitó corregir los encabezados compuestos de las tres entidades y continuar los lotes 21–25. Corte actual: 254 procesados y 199 restantes; próximo lote 26. Para avanzar cinco lotes: `python3 bin/federal/lotes.py --lotes 5`. Si el usuario ordena detenerse, registrar la barrera reanudar_requiere_instruccion_usuario y usar --reanudar únicamente tras una instrucción posterior de continuación.

Slugs: cuando la sigla de origen sea numérica, incluidos sufijos numéricos de fecha, derivar del nombre oficial mediante slug_nombre; conservar sigla y archivo_origen. Si nombre_oficial no está cotejado, slug null con incidencia. Los siete casos señalados por el usuario y los dos casos anteriores con sufijo de fecha se ajustaron creando nuevas versiones de metadatos; originales y texto permanecen idénticos. Reporte: ajuste-slugs-numericos.json.

Informe e inventario: `Federal/reportes/corte-lotes-21-25.md` y `originales-corte-25.json`. Los enlaces locales actual deben ser enlaces simbólicos; el clon principal tiene core.symlinks=false y un rebase puede representarlos como archivos. Verificar/restaurar al destino exacto de actual.json sin tocar originales ni textos.

## Abrogación: metadatos

`metadatos.ajustar` elimina entradas de abroga totalmente null, remapea los índices de incidencias y conserva evidencia impresa. Extrae abrogacion_programada de la portada, antes del cuerpo/preambulo histórico; objeto con decreto_dof, fecha_dof, fecha_fin_vigencia y evidencia, o null sin declaración. No infiere término anual a partir de ejercicio fiscal ni confunde abroga (otras normas) con la abrogación del propio ordenamiento. Fecha límite impresa se registra con su condición literal en validacion.json.

`python3 bin/federal/metadatos.py --corregir-existentes` corrigió solo ID 5 y los documentos con entradas de abroga vacías: 29 documentos, 41 entradas. Se crearon versiones nuevas de metadatos y se comprobaron originales/texto/extracción idénticos. Los otros 75 del corte anterior permanecen sin modificar; el nuevo campo se añade también a cada documento de los lotes 11 en adelante. Estado y reporte por documento permiten retomar la corrección tras una interrupción. Detalle: ajuste-metadata-abrogacion.json.

## Encabezados compuestos

`bin/encabezados.py` comparte el reconocimiento conservador de sufijos ordinales y serie numérica, plural Artículos de un solo número y abreviaturas ordinales impresas. Los conversores de Nayarit/Federal y Sinaloa lo usan sin normalizar el rótulo literal. La corrección histórica se conserva en versiones nuevas, con evidencia de página en validacion.json y resumen en correccion-encabezados-compuestos.json de cada entidad. LFDA ID 169: errata impresa Artículos 135.- preservada. Índices/articulado no regenerados; sus rutas históricas se conservan hasta esa fase separada.
