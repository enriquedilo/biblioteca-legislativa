# Conversión semanal — 10 de noviembre de 2026

Fuente: `vigilancia/reporte.md`, corrida 9 de noviembre, 23:43 UTC; copia en `reporte-fuente.md`. Base main `294d96d62df47bb0765483a973da6593e0077909`. Se procesan exclusivamente Nayarit 48 y 98. No se ejecutó detección. Sin merge a main.

## Cambios por artículo

### Nayarit 48 — Ley de Desarrollo Forestal Sustentable

- **154:** sustituye la formulación general de vigilancia por prevención y vigilancia según competencias de los tres órdenes de gobierno. Delimita la revisión de áreas y establecimientos en competencia estatal; explicita acciones de la Comisión Forestal y facultades de inspección, vigilancia y sanción de la Procuraduría Estatal de Protección al Ambiente y Ordenamiento Territorial; prevé coordinación y participación de personas propietarias y poseedoras.
- **153:** sin cambio de contenido. Su rango en el índice incorpora la nota impresa que anuncia la reforma del 154; se clasifica como nota contigua.
- **Transitorio Único, P.O. 26 de octubre de 2026:** añadido; vigencia al día siguiente de publicación. No se mezcla con Primero/Segundo del 2 de septiembre de 2026 ni con los transitorios originales. El antiguo rango del Segundo incluía el índice temático final: se excluye esa tabla únicamente para comparar, no del Markdown conservado.
- Sin artículos de cuerpo añadidos o eliminados. Índice: 160 de cuerpo, 11 transitorios (antes 10).

**Particularidad de fuente:** el PR #12 ya incorporó una versión del 2 de septiembre desde URLs con `-1`. El reporte semanal detectó cambios en las URLs anteriores, sin `-1`, cuyos cuatro prefijos de hash permiten identificar la fuente observada. Los originales descargados coinciden exactamente con los hashes del reporte y la nueva portada imprime enmienda de 26 de octubre de 2026. Se compara contra la versión más reciente de main, no contra la versión más antigua que usó la Action. Se conserva íntegra la versión de septiembre. Metadata de la versión nueva registra las URLs efectivamente descargadas. No se reescribe el catálogo capturado ni se ejecuta detección para cambiar sus enlaces.

### Nayarit 98 — Ley de Protección a la Fauna

- **2:** fracción I amplía el objeto a especies silvestres, domésticas y exóticas; incorpora un párrafo sobre confinamiento seguro y trato digno para ejemplares y poblaciones exóticos. Fracción III modifica concurrencia y coordinación conforme a la distribución de competencias de la legislación general.
- **3:** incluye ejemplares o poblaciones exóticos y añade un párrafo sobre ejercicio de atribuciones estatales y municipales conforme a legislación general y convenios con la Federación.
- **4, fracción VIII:** sustituye la definición de especies/poblaciones exóticas por ejemplares/poblaciones exóticos fuera de su distribución natural, incluidos híbridos y modificados.
- **12:** delimita las atribuciones de la Comisión Estatal al ámbito de su competencia. Cambia las fracciones I (protección y coordinación), II (asesoría sobre fauna en general) y V (capacitación del personal que maneja o tiene contacto con fauna silvestre, doméstica y exótica).
- **31:** modifica la prohibición de maltrato, sacrificio, destrucción, daño o perturbación para incluir afectación directa o indirecta y fauna exótica; conserva la remisión de excepción al último párrafo del artículo 34.
- **11 y 30 Bis:** sin modificación sustantiva; sus rangos incorporan notas de reforma de los artículos siguientes. El rango 2 también contiene la nota que anuncia la reforma del 3, además de sus cambios propios.
- **Transitorio Único, P.O. 26 de octubre de 2026:** añadido; entrada en vigor al día siguiente de publicación. Identificado por su bloque de P.O., distinto de los Únicos de reformas anteriores.
- Sin artículos de cuerpo añadidos o eliminados. Índice: 83 de cuerpo, 16 transitorios (antes 15).

Los JSON `Nayarit-48-comparacion.json` y `Nayarit-98-comparacion.json` conservan antes/después, páginas y fragmentos. La comparación elimina solo para análisis membretes, marcadores de página, espacios, escapes Markdown e índice temático final. Los textos publicados conservan esos contenidos. No se atribuyen desplazamientos de líneas o páginas a reformas.

## Controles

- Cuatro originales respaldados permanentemente en la Mac bajo `respaldo-conversiones/2026-11-10/Nayarit/<id>/`, con recibos y hashes. Los cuatro SHA-256 coinciden con `vigilancia/estado.json`. PDF, Word, extracción y SQLite excluidos de Git.
- 112 páginas (80 + 32), sin páginas carentes de texto. Sin OCR ni erratas reparadas. Conservación de todos los caracteres no blancos y signos, cifras e inicios de listas/fracciones frente al Markdown guardado; incluye articulado, transitorios y notas completos.
- Frecuencias de dígitos iguales entre Poppler y pypdf en las 112 páginas; discrepancias de orden entre lectores permanecen informativas. Las diferencias Word/PDF se registran, no se reparan ni se presentan como igualdad de originales.
- Cotejo visual por muestra: Forestal 1, 72, 73, 76; Fauna 1, 2, 3, 7, 8, 13, 30 (11 páginas). No cotejo visual integral ni cotejo del decreto original del Periódico Oficial.
- Publicación de Forestal recuperada literalmente: 1 de junio de 2023, Sección Octava; el parser no reconocía «Ley publicada el día». Fauna: 16 de diciembre de 2006, Sección Décima Tercera. Última enmienda impresa de ambas: 26 de octubre de 2026. Números de decreto, de periódico, ediciones y campos de notas no impresos o no desglosados permanecen null con incidencia. Detalle por campo en `resultados.json` y `validacion.json`.
- Índices regenerados con `python3 bin/indices.py todo --entidad Nayarit`. Verificados SHA-256, punteros, enlaces, rutas.json y rangos/páginas de artículos. Se descartaron cambios de mera fecha de generación en los otros índices de Nayarit. Ningún archivo de versiones históricas modificado.

## Pendientes del reporte

- **Nayarit 78, Justicia Alternativa:** reporte registra 404 en PDF y Word. No se dispone de fuente sustituta identificada por el reporte. No se descarga otra ley ni se inventa URL; se conserva la versión existente y se deja pendiente la revisión de la fuente.
- **Catálogos de Nayarit y Federal:** alertas sin altas/bajas individualizadas. No se ejecuta detección ni se incorporan documentos por inferencia. Federal está fuera del alcance de esta conversión semanal.
- Revisión humana del diff y de las incidencias de fuente/metadata antes del merge. PR en borrador.
