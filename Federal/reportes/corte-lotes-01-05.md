# Corte tras lote 5

Detenido por instrucción expresa del usuario antes del lote 6.

- Alcance confirmado: 453 ordenamientos (316 principales y 137 reglamentos).
- Piloto aprobado: 4 documentos. Lotes 1–5: 50 documentos adicionales.
- Total procesado: 54. Restantes sin iniciar: 399.
- Páginas verificadas: 4706. Originales con URL individual y SHA-256 comprobado: 108.
- Pendientes por falta de PDF o capa de texto: 0. Incidencias de descarga/formato Word: 0.
- Cada lote tiene commit y push en federal; referencias en avance_lotes.json.

Controles completos de integridad de originales, enlace actual, metadatos de versión, secuencia de marcadores y conservación de contenido/signos/listas aprobados. Las diferencias Word/PDF y campos no impresos continúan documentados en cada validacion.json. El control pypdf es informativo conforme al diagnóstico del usuario; no modifica el texto generado con Poppler ni bloquea el proceso. No se realizó cotejo visual exhaustivo de los lotes.

Cambios de main incorporados: parser de notas DOF y reconocimiento de Federal por el generador de índices. No se ejecutó ese generador: sin índices de búsqueda ni articulado, y sin OCR. No se modificaron textos para compensar fragmentación de cifras de pypdf.

Originales y extraccion.txt conservados localmente y excluidos de Git según la política existente. GitHub conserva texto, metadatos, validaciones y estado; el inventario originales-corte-05.json registra URL, SHA-256 y ruta local de cada original.

Se reconcilió el historial tras incorporar main durante el lote 2; se comprobaron todos los resultados ya publicados antes de resolver los tres archivos de progreso. No hubo push forzado ni eliminación de versiones.

No se abre PR final porque el acervo sigue incompleto. El siguiente trabajo, cuando lo indique el usuario, comienza por lote 6. El estado permite retomar tras una interrupción por documento o por publicación.

El rebase representó 24 enlaces actual como archivos debido a core.symlinks=false en la configuración del clon. Se comprobó su contenido contra actual.json y se restauraron como enlaces simbólicos al mismo destino; no se cambiaron originales, versiones ni textos.
