# Biblioteca Legislativa

Acervo consultable de legislación mexicana —**federal**, de **Sinaloa** y de
**Nayarit**— descargada de los sitios oficiales, convertida a Markdown con
trazabilidad de página, validada e indexada a nivel de artículo.

| Acervo | Ordenamientos | Artículos de cuerpo | Transitorios | Notas de reforma |
|---|---:|---:|---:|---:|
| Federal | 447 | 58,794 | 15,698 | 35,344 |
| Sinaloa | 151 | 18,911 | 3,036 | 4,733 |
| Nayarit | 138 | 16,793 | 2,334 | 5,360 |
| **Total** | **736** | **94,498** | **21,068** | **45,437** |

- **Federal**: compilación de leyes federales vigentes de la Cámara de
  Diputados. 447 de los 453 ordenamientos catalogados: la Constitución, 9
  códigos, 302 leyes —ordinarias, generales y orgánicas—, 134 reglamentos y una
  ordenanza.
- **Sinaloa**: los 151 ordenamientos de la categoría «Leyes Estatales» del
  Congreso del Estado. La categoría «Leyes de Ingreso» no está incluida.
- **Nayarit**: 138 ordenamientos del Congreso del Estado (Códigos,
  Constitución, Leyes, Leyes Orgánicas, Marco Jurídico del Congreso y Marco
  Jurídico Municipal).

## Lo que no está, y por qué

**Nayarit, 1 ordenamiento.** El ID 133, Reglamento Interior de la Auditoría
Superior, está en el catálogo del Congreso pero el sitio no publica su archivo.

**Federal, 6 ordenamientos.** Son reglamentos antiguos publicados como imagen
escaneada. Su conversión no superó el control de conservación de contenido —o el
PDF no trae capa de texto—, así que **no se promovió ninguna versión**: no
tienen `actual/` ni aparecen en los índices. No se les aplicó OCR. Sus PDF
originales se conservan con su SHA-256 y su URL en
`Federal/reportes/pendientes-finales.json`.

| ID | Ordenamiento |
|---|---|
| 372 | Reglamento de la Ley del Servicio Militar (1942) |
| 413 | Reglamento de la LGS en Materia de Control Sanitario de Actividades, Establecimientos, Productos y Servicios (1988) |
| 414 | Reglamento de la LGS en Materia de Control Sanitario de la Disposición de Órganos, Tejidos y Cadáveres (1985) |
| 416 | Reglamento de la LGS en Materia de Investigación para la Salud (1987) |
| 444 | Reglamento de la Ley Federal de Ganadería (1955) |
| 446 | Reglamento del artículo 5º constitucional (1945) |

Un ordenamiento ausente es un hueco visible; uno con el texto alterado es una
cita falsa esperando a que alguien la use. Por eso se prefirió dejarlos fuera.

## Cómo está organizado

    <Acervo>/
      INDICE.md                    entrada principal
      catalogo/                    inventario oficial e identidades propias
      ordenamientos/<id>/
        actual.json                declara la versión seleccionada
        actual/ -> versiones/<hash>/
        versiones/<hash>/
          texto.md                 texto de consulta, con <!-- PAGINA_PDF: n -->
          metadata.json            publicación, decreto, reformas, abrogaciones
          validacion.json          controles, incidencias y campos no impresos
      indices/                     capa derivada (ver su README)
      reportes/                    síntesis de validación por lote

La ruta estable de consulta es `<Acervo>/ordenamientos/<id>/actual/texto.md`.
El `<hash>` de cada versión es el SHA-256 del original del que se convirtió: el
versionado es por contenido, no por fecha.

Los identificadores son de catálogo, propios de cada acervo, y no son números de
decreto: el ID 70 de Sinaloa, el de Nayarit y el federal son ordenamientos
distintos.

## Búsqueda

Cada acervo tiene su capa de índices en `<Acervo>/indices/`, con el articulado
en JSON, las remisiones nominales internas, las rutas resueltas y una base
SQLite con búsqueda de texto completo insensible a acentos:

```sql
SELECT ley, articulo, pagina, snippet(articulos,6,'>>','<<','…',12)
FROM articulos WHERE articulos MATCH '(arancel OR honorarios) AND (perito OR pericial)';
```

El articulado reconoce las numeraciones que usan las compilaciones oficiales:
`12 Bis`, `3 Bis-A`, series compuestas `5 Bis 1`, ordinales latinos hasta
Novodecies, numeración con coma de millar (`1,000`) y ordinales en letra en
leyes antiguas. En cualquier discrepancia entre un índice y el `texto.md`, manda
el texto.

## Qué NO está en este repositorio

Los **originales PDF y Word** y las **bases de búsqueda SQLite** están excluidos
deliberadamente (ver `.gitignore`):

- Los originales son el respaldo de cotejo: cientos de MB de binarios que Git
  versionaría completos en cada actualización. Se conservan fuera del
  repositorio. `metadata.json` guarda su SHA-256 y su URL de origen, así que
  cualquier copia puede verificarse contra lo declarado aquí.
- Las bases `biblioteca.db` se regeneran en segundos:

      python3 bin/indices.py todo --entidad Federal
      python3 bin/indices.py todo --entidad Sinaloa
      python3 bin/indices.py todo --entidad Nayarit

## Regla de acervo

Cada acervo es independiente, con su propio índice y su propia base. Una
consulta a uno no toca los otros. Para derecho comparado —incluida la
contrastación de una ley estatal con la ley general o federal que la rige— se
corre la misma pregunta en cada índice por separado y los resultados se
presentan rotulados por orden de gobierno: **las tablas no se fusionan**.

## Vigencia

Los textos provienen de la compilación consolidada que publica cada Congreso,
que es una compilación administrativa. **Ningún archivo de este repositorio
certifica vigencia jurídica.** `actual.json` identifica la versión seleccionada
de la biblioteca, no acredita que sea el texto vigente. El respaldo de una cita
formal es el decreto publicado en el Periódico Oficial del Estado o en el Diario
Oficial de la Federación.

Las notas de reforma al pie de los artículos son anotaciones impresas por el
compilador: sirven para saber cuándo se intervino un artículo, pero no son una
tabla oficial y pueden faltar en artículos efectivamente reformados. Una
declaratoria de invalidez de la SCJN no es una reforma.

Tres ordenamientos federales exigen advertencia expresa al citarlos:

- **Ley General del Sistema de Medios de Impugnación en Materia Electoral**
  (ID 223): **no está abrogada**. La SCJN invalidó el decreto de 2023 que la
  abrogaba y el texto recuperó vigencia (`vigencia_recuperada`).
- **Código Federal de Procedimientos Civiles** (ID 5): abrogado por el decreto
  que expide el Código Nacional de Procedimientos Civiles y Familiares, con
  vigencia a más tardar al 1 de abril de 2027 (`abrogacion_programada`).
- **Ley de Ingresos** (ID 60) y **LIGIE** (ID 78): `vigencia_anual`. Hay que
  comprobar el ejercicio antes de citarlas.

## Vigilancia de reformas

`bin/vigilancia.py` revisa semanalmente los catálogos oficiales y compara contra
el SHA-256 archivado de cada ordenamiento; el flujo de GitHub Actions
(`.github/workflows/vigilancia.yml`) abre un issue cuando detecta cambios.
Actualmente cubre Sinaloa y Nayarit.

## Fuentes

- Federal: [Leyes Federales Vigentes, Cámara de Diputados](https://www.diputados.gob.mx/LeyesBiblio/index.htm)
- Sinaloa: [Leyes Estatales del Congreso](https://www.congresosinaloa.gob.mx/leyes-estatales/) · [Gaceta](https://gaceta.congresosinaloa.gob.mx/#/leyes)
- Nayarit: [Legislación Estatal del Congreso](https://congresonayarit.gob.mx/legislacion-estatal/)
