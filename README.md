# Biblioteca Legislativa

Acervo consultable de la legislación estatal de **Sinaloa** y **Nayarit**,
descargada de los sitios oficiales de cada Congreso, convertida a Markdown con
trazabilidad de página, validada e indexada.

| Entidad | Ordenamientos | Artículos de cuerpo | Notas de reforma |
|---|---:|---:|---:|
| Sinaloa | 151 | 18,910 | 4,733 |
| Nayarit | 138 | 16,768 | 5,355 |

Nayarit tiene un ordenamiento pendiente (ID 133, Reglamento Interior de la
Auditoría Superior): está en el catálogo del Congreso pero el sitio no publica
su archivo.

## Cómo está organizado

    <Entidad>/
      INDICE.md                    entrada principal
      catalogo/                    inventario del Congreso e identidades propias
      ordenamientos/<id>/
        actual.json                declara la versión seleccionada
        actual/ -> versiones/<hash>/
        versiones/<hash>/
          texto.md                 texto de consulta, con <!-- PAGINA_PDF: n -->
          metadata.json            publicación, decreto, reformas, abrogaciones
          validacion.json          controles, incidencias y campos no impresos
      indices/                     capa derivada (ver su README)
      reportes/                    síntesis de validación por lote

La ruta estable de consulta es `<Entidad>/ordenamientos/<id>/actual/texto.md`.
Los identificadores son de catálogo, propios de cada entidad, y no son números
de decreto: el ID 70 de Sinaloa y el 70 de Nayarit son leyes distintas.

## Qué NO está en este repositorio

Los **originales PDF y Word** y las **bases de búsqueda SQLite** están excluidos
deliberadamente (ver `.gitignore`):

- Los originales son el respaldo de cotejo, 214 MB de binarios que Git
  versionaría completos en cada actualización. Se conservan fuera del
  repositorio. `metadata.json` guarda su SHA-256 y su URL de origen, así que
  cualquier copia puede verificarse contra lo declarado aquí.
- Las bases `biblioteca.db` se regeneran en segundos:

      python3 bin/indices.py todo --entidad Sinaloa
      python3 bin/indices.py todo --entidad Nayarit

## Regla de entidad

Cada entidad es un acervo independiente, con su propio índice. Una consulta a
una entidad no toca la otra. Para derecho comparado, se corre la misma pregunta
en cada índice por separado y se presentan los resultados rotulados por estado:
las tablas no se fusionan.

## Vigencia

Los textos provienen de la compilación consolidada que publica cada Congreso,
que es una compilación administrativa. **Ningún archivo de este repositorio
certifica vigencia jurídica.** `actual.json` identifica la versión seleccionada
de la biblioteca, no acredita que sea el texto vigente. El respaldo de una cita
formal es el decreto publicado en el Periódico Oficial.

Las notas de reforma al pie de los artículos son anotaciones impresas por el
compilador del Congreso: sirven para saber cuándo se intervino un artículo, pero
no son una tabla oficial y pueden faltar en artículos efectivamente reformados.

## Fuentes

- Sinaloa: [Leyes Estatales del Congreso](https://www.congresosinaloa.gob.mx/leyes-estatales/) · [Gaceta](https://gaceta.congresosinaloa.gob.mx/#/leyes)
- Nayarit: [Legislación Estatal del Congreso](https://congresonayarit.gob.mx/legislacion-estatal/)
