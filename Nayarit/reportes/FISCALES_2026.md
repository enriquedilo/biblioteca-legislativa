# Normas fiscales anuales estatales — ejercicio 2026

Revisión del 11 de noviembre de 2026. Rama `nayarit-fiscales-2026`. Sin merge y sin incorporación de documentos de Sinaloa.

## Nayarit: fuentes y alcance

Enlaces leídos del catálogo vigente, no construidos:

- [Ley de Ingresos 2026](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/ley_de_ingresos_del_estado_libre_y_soberano_de_nayarit_2026.pdf), ID 141.
- [Presupuesto de Egresos 2026](https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes_ingresos_presupuesto/2026/presupuesto_egresos_2026.pdf), ID 142.

El catálogo solo ofrece PDF para ambos; URL Word nula e incidencia registrada, sin fabricar originales. Captura y enlaces en `fiscales-2026/`. Ambos llevan `vigencia_anual: true` y `ejercicio_fiscal: 2026` en metadata. Publicación impresa del 29 de diciembre de 2025: Ingresos, Sección Cuarta, número 117; Presupuesto, Sección Quinta en tres partes. No se infieren números de decreto ni últimas reformas ausentes.

Se retiran de `exclusiones.json` la ley estatal, el presupuesto y el contenedor de sección «Leyes de Ingresos 2026». Permanecen las veinte leyes municipales, ahora con motivo explícito de decisión de alcance. Los restantes motivos de exclusión no cambian. Renovación anual en diciembre/enero anotada en `PENDIENTES.md`.

El usuario autorizó promover el Presupuesto con limitación explícita para las tablas actuariales y la cifra en imagen; remisión al PDF en metadata y validación. Ambos documentos están promovidos.

## Controles de conversión

El PDF de Ingresos contiene 921 bytes de HTML antes de la cabecera PDF y HTML después del cierre. Se preserva íntegro el archivo descargado y su SHA-256; no se recorta ni repara. Se ajusta la comprobación de formato para admitir una cabecera dentro de los primeros 1,024 bytes solo si el lector confirma páginas válidas. Los archivos HTML sin PDF siguen rechazándose.

Ingresos: 75 páginas, 70 artículos de cuerpo y cinco transitorios. Presupuesto: 1,376 páginas, 99 artículos de cuerpo y siete transitorios. Ninguna página totalmente carente de texto. El control verifica caracteres, signos y listas de la capa extraíble por página; las diferencias de cifras entre lectores se conservan como incidencias, no se reparan. Las tablas extensas conservan su extracción, sin reconstrucción de celdas.

El presupuesto contiene imágenes que el Markdown no representa: esquema y cifra en página 437; dos tablas del estudio actuarial en 786; diagramas en 823 y 826, y gráfico ODS en 832. Las páginas 852 y 1134, de escaso texto, son separadores con rótulo y se cotejaron visualmente. Los membretes gráficos de las matrices del Poder Legislativo no se confunden con tablas escaneadas: sus celdas sí son extraíbles. Los límites se registran en `validacion.json`.

El índice existente segmenta por artículos; los anexos posteriores quedan dentro del tramo final del séptimo transitorio, no como artículos añadidos. Se conserva el documento completo con marcadores de página, pero no se presenta el conteo de artículos como un conteo de anexos. No se modifica ese comportamiento del generador en esta tarea.

## Sinaloa: fuente encontrada, sin carga

**Es un solo ordenamiento:** Ley de Ingresos y Presupuesto de Egresos del Estado de Sinaloa para el Ejercicio Fiscal del año 2026 y Anexos. La portada del Periódico Oficial cotejada dice decreto **294**, número **154**, **22 de diciembre de 2025**, **Segunda Sección**, ocho partes. El Congreso [informó su aprobación el 9 de diciembre de 2025](https://www.congresosinaloa.gob.mx/comunicados/aprueba-congreso-ley-de-ingresos-y-presupuesto-de-egresos/).

La publicación oficial completa está en el [portal de Transparencia del Gobierno de Sinaloa](https://transparencia.sinaloa.gob.mx/p/ley-de-ingresos-y-presupuesto-de-egresos-del-estado-de-sinaloa-para-el-ejercicio-fiscal-2026), no en el catálogo de Leyes Estatales del Congreso. Esa página enlaza ocho PDF individuales; no ofrece Word.

La [parte uno enlazada actualmente](https://media.transparencia.sinaloa.gob.mx/uploads/files/11874/POE-22-diciembre-2025-154-I-OCR.pdf) tiene un nombre que dice `154-I-OCR`, pero su portada dice Segunda Sección, Parte Uno: no se infiere la sección del nombre del archivo. La denominación OCR viene del servidor; no se ha aplicado OCR ni convertido este documento al acervo.

Todos los enlaces respondieron HTTP 200, `Content-Type: application/pdf`, con `ETag`, `Last-Modified` y tamaño. Evidencia exacta en [cabeceras](fiscales-2026/sinaloa-cabeceras.json) y [lista de ocho URL](fiscales-2026/sinaloa-enlaces.json).

**Valoración de estabilidad:** son enlaces públicos directos, sin sesión ni firma temporal visible, aptos para vigilar cambios de bytes por URL y SHA-256. No se puede garantizar su permanencia. Son publicaciones del ejercicio 2026, no una URL que prometa sustituirse por la ley anual vigente: vigilar solo esos PDF no detectaría el ejercicio 2027. Para renovar el acervo se debe comprobar además la página de publicaciones y el nuevo Periódico Oficial en diciembre/enero. La integración queda pendiente de que el usuario revise estas fuentes.

## Índices y verificación final

Índices regenerados: Nayarit pasa de 16,956 a 17,125 artículos de cuerpo y de 2,506 a 2,518 transitorios. Las 139 entradas de ordenamientos anteriores se verificaron idénticas (sin contar el sello de generación, que se conservó). Los IDs 141 y 142 tienen secuencias completas, sin huecos, y sus rutas resuelven al mismo hash que `actual`. [Controles por documento](fiscales-2026/verificacion.json).

Control de formato probado con los dos PDF oficiales válidos y con HTML de error y un falso encabezado PDF: ambos inválidos se rechazan sin promoción.

Incidencia del índice: las notas pasan de 5,457 a 5,458, pero la adicional es un **falso positivo** del parser existente («Derechos Humanos» marcado como derogación sin fecha dentro de los anexos del ID 142). No representa una reforma del presupuesto. Se documenta junto con la segmentación pendiente de anexos; metadata mantiene `reformas: []`.
