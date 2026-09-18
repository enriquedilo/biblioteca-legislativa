# Piloto Federal

Desde la raíz del repositorio, con Python que disponga de pypdf y Pillow, y Poppler instalado:

1. `python3 bin/federal/piloto.py`: captura catálogo desde las capturas HTML existentes y procesa únicamente los cuatro documentos seleccionados, guardando estado tras cada uno. Descarga cada URL individual; reutiliza descargas locales de preparación. Reutiliza controles de `bin/nayarit` sin modificar esa entidad.
2. `python3 bin/federal/revision.py`: compara ocurrencias de cifras de ambos lectores y genera muestras visuales locales en `work/piloto_visual/` y resumen en `work/resumen.json`.
3. Revisar visualmente las muestras y sus extracciones antes del cierre. `cerrar_piloto.py` registra el cotejo efectuado en esta corrida; no debe ejecutarse sin esa revisión. Comprueba hashes, marcadores, enlaces y conservación.

No existe entrada que inicie lotes. Resultados y límites: `Federal/reportes/piloto.md`. Los scripts son piloto; requieren extensión y revisión antes de escalar. No construyen índices ni articulado.

## Lotes y corte vigente

El piloto fue aprobado y los lotes 1–5 están publicados. `lotes.py` persiste cada intento, recupera publicaciones interrumpidas y sincroniza federal antes del push, incorporando main sin reescribir commits publicados. El control pypdf es informativo.

El usuario ordenó detenerse después del lote 5. El estado contiene una barrera explícita: no ejecutar el lote 6 sin nueva instrucción. Tras esa autorización, `python3 bin/federal/lotes.py --reanudar --lotes 5` retoma desde el lote pendiente. Sin `--reanudar`, el controlador se detiene mientras esa barrera esté activa.

Informe e inventario: `Federal/reportes/corte-lotes-01-05.md` y `originales-corte-05.json`. Los enlaces locales `actual` deben ser enlaces simbólicos; el clon principal tiene core.symlinks=false y un rebase puede representarlos como archivos. El corte verificó y restauró los enlaces federales al destino exacto de actual.json, sin tocar originales ni textos.
