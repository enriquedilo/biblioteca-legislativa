# Actualización del 16 de noviembre de 2026

Origen: corrida de vigilancia del 16 de noviembre, 23:39 UTC, 739 ordenamientos
revisados. Cuatro ordenamientos señalados; los cuatro atendidos.

Las URL de Nayarit se leyeron del catálogo vigente el 16 de noviembre, no se
construyeron por sufijo. Esa precaución fue decisiva: **los dos punteros
congelados se movieron en direcciones opuestas**. La Constitución perdió el
sufijo `-1` y la Ley Municipal lo ganó. Adivinar habría fallado en ambos, cada
uno por el lado contrario.

## Nayarit 5 — Constitución Política del Estado

Versión nueva. Reforma publicada en el **P.O. del 6 de noviembre de 2026**, que
el acervo no tenía: la última registrada era del 3 de septiembre.

| Artículo | Qué | Página |
|---|---|---:|
| 69 | Fracción XXXII reformada, sobre la designación de la persona titular de la Autoridad Estatal | 54 |
| 69 | Fracción XXXIII adicionada | 55 |
| 134 | Tres párrafos reformados | 110 |
| 134 | Fracción VII adicionada, sujeción de los sectores social y privado | 111 |

185 páginas, 155 artículos, sin cambio en el número de artículos.

**URL repuntada.** El catálogo dejó de enlazar el archivo archivado, que
terminaba en `-1`, y pasó a enlazar el mismo nombre sin sufijo.

**El Congreso publicó dos PDF casi idénticos con diez segundos de diferencia**
el 13 de noviembre: el que enlaza el catálogo y el que conserva el sufijo `-1`,
que es el que la vigilancia venía observando. Difieren en cuatro bytes, con toda
probabilidad metadatos del archivo. Se archivó el que enlaza el catálogo, por
ser el que la fuente declara vigente.

## Nayarit 36 — Ley de Cultura Física y Deporte

Versión nueva. Misma reforma del **6 de noviembre de 2026**. El articulado pasa
de 131 a 136 artículos: se adicionaron **94 Quinquies, 94 Sexies, 94 Septies,
94 Octies y 94 Nonies**.

**El Word del sitio no se actualizó.** El archivo Word que publica hoy el
Congreso es byte por byte el que ya teníamos archivado, mientras que el PDF sí
trae la reforma. Quien coteje contra el Word leerá el texto anterior. El cotejo
Word/PDF de la conversión se ejecutó y no reportó artículos presentes en uno y
ausentes en el otro, de modo que la diferencia está en el contenido de los
artículos, no en su inventario.

## Nayarit 139 — Ley Municipal

**Sin versión nueva.** El PDF y el Word que publica el catálogo son byte por
byte los archivados: el Congreso solo renombró el archivo, que ganó el sufijo
`-1`. Se repuntaron las URL en la metadata de la versión vigente y nada más.
Es el caso para el que sirve versionar por contenido: un cambio de nombre en la
fuente no produce una versión del acervo.

## Sinaloa 66 — Ley de Pesca y Acuacultura Sustentables

Versión nueva, pero **no hubo reforma**. El articulado es idéntico: 95 artículos
en PDF y en Word, sin discrepancias. Lo que cambió es otra cosa, y es lo más
importante de esta actualización.

La compilación ahora imprime, al pie de los artículos **67 Bis y 67 Bis A**,
páginas 42 y 43:

> Artículo declarado inválido por el Tribunal del Pleno de la Suprema Corte de
> Justicia de la Nación por la Controversia de Constitucional 215/2025, en su
> respectiva sesión ordinaria con fecha 10 de marzo de 2026.

Ambos artículos fueron adicionados por el Decreto No. 148, publicado en el
Periódico Oficial «El Estado de Sinaloa» No. 086, de 16 de julio de 2025.

**La versión anterior del acervo, descargada el 7 de septiembre de 2026, no
traía esa leyenda**, pese a que la resolución de la Suprema Corte es del 10 de
marzo. El Congreso la incorporó a su compilación después. Consecuencia práctica:
cualquier cita de esos dos artículos tomada del acervo entre septiembre y el 16
de noviembre no llevaba la advertencia de invalidez.

Queda registrado en `incidencias_de_vigencia` dentro del `validacion.json` de la
versión nueva, con la referencia a la versión anterior que no la traía.

## Dos incidencias de proceso

**El conversor de Sinaloa no actualiza el enlace `actual`.** `bin/biblioteca.py`
escribe `actual.json` y la carpeta de la versión, pero no toca el enlace
simbólico. Tras la conversión, el 66 quedó con `actual.json` apuntando a la
versión nueva y el enlace a la de septiembre: quien leyera por la ruta estable
habría obtenido el texto viejo. Se corrigió a mano. Era el único incoherente de
los 799 ordenamientos porque es el primero de Sinaloa que se reconvierte desde
que existen los enlaces. **Falta corregirlo en el conversor**; queda anotado en
`PENDIENTES.md`.

**La conversión de Nayarit exige macOS.** La extracción de los `.doc` usa
`/usr/bin/textutil`. En Linux falla y el cotejo Word/PDF no se ejecuta, pero la
versión se escribe igual, con la misma etiqueta de validación que las buenas y
el fallo relegado a `incidencias_descarga`. Un primer intento en Linux se
revirtió por eso. **La etiqueta de validación debería reflejar que el cotejo no
corrió**; queda anotado en `PENDIENTES.md`.

## Índices

Regenerados en los dos acervos tocados:

| Acervo | Ordenamientos | Artículos de cuerpo | Notas de reforma | FTS |
|---|---:|---:|---:|---:|
| Nayarit | 141 | 17,130 | 5,467 | 19,655 |
| Sinaloa | 151 | 18,912 | 4,752 | 22,180 |

Nayarit suma cinco artículos de cuerpo y nueve notas de reforma, que son los
cinco artículos nuevos de la 36 y las anotaciones de las dos reformas.

## Lo que queda de ese reporte de vigilancia

Pendiente, por decisión de alcance ya tomada: incorporar la **Ley de Ingresos de
la Federación para 2027**, que el sitio ya publica, conservando la de 2026 como
vigente hasta enero y distinguiendo ambas por ejercicio; y dar de alta las dos
leyes federales nuevas que aparecieron en el catálogo, la **Ley General para el
Fortalecimiento y Armonización Catastral y Registral** y la **Ley de Economía
Digital para Pagos Digitales y Electrónicos**.
