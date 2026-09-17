# Biblioteca Legislativa de Sinaloa

## Empieza aquí

1. Abre [el índice](Sinaloa/INDICE.md).
2. Elige el Markdown de la ley que necesitas.
3. Usa `metadata.json` para publicación, decreto, reformas y abrogaciones impresas; usa `validacion.json` para conocer campos no localizados y limitaciones.
4. La ruta estable de consulta es `Sinaloa/ordenamientos/<id>/actual/`.

## Qué contiene

La biblioteca contiene los 151 ordenamientos de la categoría «Leyes Estatales» descargados del catálogo del Congreso. Cada ordenamiento conserva su PDF y Word originales, la conversión Markdown, la extracción de control, metadata normativa y trazabilidad. La categoría «Leyes de Ingreso» no está incluida.

Fuente: [Leyes Estatales del Congreso](https://www.congresosinaloa.gob.mx/leyes-estatales/), que enlaza al [catálogo de la Gaceta](https://gaceta.congresosinaloa.gob.mx/#/leyes).

## Cómo se organiza

- `Sinaloa/INDICE.md`: entrada principal.
- `Sinaloa/catalogo/`: inventarios del Congreso.
- `Sinaloa/ordenamientos/`: una carpeta por identificador de ley.
- `Sinaloa/ordenamientos/<id>/actual/`: enlace estable a la versión que declara `actual.json`.
- `Sinaloa/ordenamientos/<id>/versiones/`: originales, Markdown, metadata, validación, revisiones y referencias.
- `Sinaloa/reportes/`: documentos de síntesis y avance general.
- `bin/`: herramientas de mantenimiento local.
- `pruebas/PRUEBA_01/`: copias de prueba, separadas del árbol de datos.

Los números de carpeta son identificadores de catálogo, no números de decreto. `actual.json` apunta a la versión seleccionada; no declara vigencia jurídica. Los comentarios `PAGINA_PDF` del Markdown permiten localizar el texto en el PDF.

## Alcance

La extracción de metadata normativa usa únicamente menciones impresas en cada PDF. Si falta un dato, se deja `null` o un arreglo vacío y se registra la incidencia en `validacion.json`. Las tablas de reformas se conservan sólo cuando el documento incluye una lista o tabla explícita; no se reconstruyen desde referencias dispersas.

La descarga y la conversión están completas. La revisión de calidad visual y la certificación de vigencia jurídica no son equivalentes a la descarga y siguen indicadas en los reportes de síntesis. La actualización periódica aún no está configurada.
