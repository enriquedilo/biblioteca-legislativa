# Skill de consulta — para compartir

`biblioteca-legislativa/SKILL.md` contiene las reglas de consulta de este
acervo, listas para usarse en un asistente que soporte skills.

Está escrito para **cualquier persona**: usa únicamente el repositorio público,
no depende de la computadora de nadie y no contiene rutas locales. Quien lo
instale puede consultar la biblioteca desde donde sea.

## Cómo usarlo

Copia el contenido de `biblioteca-legislativa/SKILL.md` y guárdalo como skill en
tu asistente. El nombre y la descripción salen del propio archivo.

## Qué esperar

Funciona para localizar disposiciones, investigar qué ordenamientos regulan una
materia y comparar entre los tres acervos —federal, Sinaloa y Nayarit—, siempre
con cita de acervo, artículo y página.

No incluye los PDF y Word originales: quedaron fuera del repositorio para
mantenerlo ligero. Si una conclusión exige cotejar contra el original, el skill
está instruido para decirlo en vez de responder sin él. Cada `metadata.json`
conserva el SHA-256 y la URL de origen, así que cualquiera puede descargar el
archivo del Congreso y verificar que corresponde.

Seis reglamentos federales antiguos no tienen texto en el acervo: son PDF
escaneados cuya conversión no superó el control de conservación. El skill está
instruido para decirlo en vez de responder por ellos.

El acervo refleja la compilación oficial a la fecha de descarga que registra
cada `metadata.json`, no el estado del día.
