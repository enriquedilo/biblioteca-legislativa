# Biblioteca Legislativa — empieza aquí

Tres acervos independientes, con la misma estructura:

| Acervo | Índice | Ordenamientos |
|---|---|---:|
| Federal | [Federal/INDICE.md](Federal/INDICE.md) | 447 |
| Sinaloa | [Sinaloa/INDICE.md](Sinaloa/INDICE.md) | 151 |
| Nayarit | [Nayarit/INDICE.md](Nayarit/INDICE.md) | 138 |

## Cómo consultar

1. Abre el índice del acervo que te interesa y localiza el ordenamiento.
2. Lee `<Acervo>/ordenamientos/<id>/actual/texto.md`. Es la ruta estable.
3. Consulta `metadata.json` para publicación, decreto, reformas y abrogaciones
   impresas, y `validacion.json` para las limitaciones y los campos no
   localizados de esa conversión.
4. Para búsquedas por materia o por término, usa la capa de índices:
   `<Acervo>/indices/` —articulado en JSON, remisiones, rutas resueltas y base
   SQLite con búsqueda de texto completo—. Se regenera con
   `python3 bin/indices.py todo --entidad <Acervo>`.

Los comentarios `<!-- PAGINA_PDF: n -->` del Markdown permiten localizar
cualquier pasaje en el PDF original. Los números de carpeta son identificadores
de catálogo, no números de decreto, y son propios de cada acervo.

## Reglas que conviene no saltarse

**Un acervo no toca al otro.** Cada uno tiene su índice y su base. El derecho
comparado se hace corriendo la misma pregunta en cada uno y presentando los
resultados por separado.

**Solo lo impreso.** La metadata se extrae únicamente de lo que el documento
imprime. Si falta un dato se deja `null` y se registra la incidencia; las tablas
de reformas se conservan solo cuando el documento trae una lista explícita, no
se reconstruyen desde referencias dispersas.

**Lo que el acervo fija es la versión, no la vigencia.** `actual.json`
identifica la versión seleccionada y `metadata.json` su fecha de descarga: el
texto es el que la compilación oficial publicaba ese día.

El alcance, lo que falta y por qué, y la organización completa están en
[README.md](README.md). Para compartir las reglas de consulta con otra persona,
[skill/](skill/) trae una versión que no depende de ninguna computadora.
