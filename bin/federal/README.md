# Piloto Federal

Desde la raíz del repositorio, con Python que disponga de pypdf y Pillow, y Poppler instalado:

1. `python3 bin/federal/piloto.py`: captura catálogo desde las capturas HTML existentes y procesa únicamente los cuatro documentos seleccionados, guardando estado tras cada uno. Descarga cada URL individual; reutiliza descargas locales de preparación. Reutiliza controles de `bin/nayarit` sin modificar esa entidad.
2. `python3 bin/federal/revision.py`: compara ocurrencias de cifras de ambos lectores y genera muestras visuales locales en `work/piloto_visual/` y resumen en `work/resumen.json`.
3. Revisar visualmente las muestras y sus extracciones antes del cierre. `cerrar_piloto.py` registra el cotejo efectuado en esta corrida; no debe ejecutarse sin esa revisión. Comprueba hashes, marcadores, enlaces y conservación.

No existe entrada que inicie lotes. Resultados y límites: `Federal/reportes/piloto.md`. Los scripts son piloto; requieren extensión y revisión antes de escalar. No construyen índices ni articulado.
