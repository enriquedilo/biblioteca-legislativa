# Esquema Nayarit v2

Se mantienen los campos base de Sinaloa y la estructura de archivos. Las extensiones autorizadas son `slug`, `url_pdf`, `url_word`, `seccion_sitio`, `secciones_sitio`, `nombre_catalogo_sitio`, `orden`, `regimen`, `tipo` y `po_publicacion.seccion`. Se elimina `ambito` por instrucción del usuario.

`nombre_catalogo` reconstruye el nombre quitando el ordinal de presentación, reubicando el tipo y su preposición al inicio, y quitando el punto final. `nombre_catalogo_sitio` conserva el nombre crudo. `orden` es `estatal` en los 139. `regimen` es `municipal` en 138 y 139, `legislativo` en los seis con procedencia Marco Jurídico del Congreso, y `general` en los demás. `tipo` usa constitucion, codigo, ley, ley_organica o reglamento según el nombre; el cotejo con el nombre impreso se marca pendiente cuando aún no se ha realizado. Las procedencias del sitio no expresan jerarquía ni competencia normativa.

Los IDs y slugs nunca se recalculan al cambiar un nombre o URL. `actual.json` selecciona `versiones/<hash>` y `actual/` es un enlace relativo. El hash de versión depende de los originales, no de la conversión. Los DOC auténticos se conservan como original.doc por autorización del usuario.

La conversión v2 evita promover remisiones en continuación de párrafo: el contexto anterior sin punto o el siguiente en minúscula se registra, y las referencias sin delimitador impreso permanecen en cuerpo. Las etiquetas explícitas completas (`Artículo 24 C.-`, por ejemplo) siguen siendo encabezados. Se verifica conservación sin espacios y con signos y cifras. Las correcciones de formato se archivan y registran; no se corrigen erratas del original ni se aplica OCR.

[Verificación v2](PILOTO_CORREGIDO_V2.json). La verificación inicial se conserva como antecedente, no como definición vigente.
