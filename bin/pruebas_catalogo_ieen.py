#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas de bin/catalogo_ieen.py. No tocan la red: corren contra un HTML de
muestra que reproduce el formato real del sitio del IEEN, con sus rarezas
-claves sin comillas, escapes, coma sobrante, anexos en orden inverso y un
nombre que lleva dos puntos y corchetes dentro de la cadena-.

Uso:
    python3 bin/pruebas_catalogo_ieen.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import catalogo_ieen as C

HTML = r'''
<html><body><script>
var vue = new Vue({ el:'#app', data: () => ({
        sdocumentos: '',
        hdocumentos: [ { text: 'No.', value: 'numero' } ],
        documentos: [
                {
                        id: 0,
                        numero: 1,
                        tipo: "Legislación Local",
                        nombre: "Constitución Estatal.",
                        acuerdo: "",
                        fecha: "03\/09\/2026",
                        pdf: "\/images\/pdf\/consnay-03092026.pdf",
                        anexos: [
                            ]
                    },
                {
                        id: 8,
                        numero: 9,
                        tipo: "Reglamentos",
                        nombre: "Nombre con trampa: dice pdf: \"algo\" y corchetes [ ] adentro",
                        acuerdo: "",
                        fecha: "",
                        pdf: "",
                        anexos: [
                            { acuerdo: "IEEN-CLE-001\/2016", fecha: "28\/01\/2016", pdf: "\/PDF\/a.pdf" },
                            { acuerdo: "IEEN-CLE-015\/2025", fecha: "30\/01\/2025", pdf: "\/PDF\/b.pdf" },
                            ]
                    },
                {
                        id: 32,
                        numero: 33,
                        tipo: "Lineamientos",
                        nombre: "Anexos al revés",
                        acuerdo: "",
                        fecha: "",
                        pdf: "",
                        anexos: [
                            { acuerdo: "IEEN-CLE-128\/2023", fecha: "15\/12\/2023", pdf: "\/PDF\/nuevo.pdf" },
                            { acuerdo: "IEEN-CLE-088\/2021", fecha: "07\/04\/2021", pdf: "\/PDF\/viejo.pdf" },
                            ]
                    },
                                ]
        }), computed: { totalDocumentos(){ return this.documentos.length; } } });
</script></body></html>
'''

d = C.extraer(HTML)
assert len(d) == 3, d
assert d[0]["nombre"] == "Constitución Estatal."
assert d[0]["pdf"] == "/images/pdf/consnay-03092026.pdf"
assert d[1]["nombre"] == 'Nombre con trampa: dice pdf: "algo" y corchetes [ ] adentro'
assert len(d[1]["anexos"]) == 2
print("1. extracción del literal: OK")

assert C.fecha_iso("28/01/2016") == "2016-01-28"
assert C.fecha_iso("2021") == "2021"
assert C.fecha_iso("") is None
print("2. fechas: OK")

v0 = C.vigente_de(d[0]); v1 = C.vigente_de(d[1]); v2 = C.vigente_de(d[2])
assert v0["origen"] == "documento" and v0["fecha"] == "2026-09-03", v0
assert v1["acuerdo"] == "IEEN-CLE-015/2025" and v1["url"].endswith("/PDF/b.pdf"), v1
# el caso que importa: anexos en orden inverso, gana la fecha mayor
assert v2["acuerdo"] == "IEEN-CLE-128/2023" and v2["url"].endswith("/PDF/nuevo.pdf"), v2
print("3. versión vigente elegida por fecha, no por posición: OK")

regs = C.normalizar("normatividad", "http://x", d)
assert regs[0]["en_la_biblioteca"] == {"entidad": "Nayarit", "id": 5}
assert "en_la_biblioteca" not in regs[1]
assert regs[1]["clave"] == "normatividad-9"
print("4. marcado de duplicados: OK")

# sin anexos y sin pdf -> sin versión vigente, no revienta
assert C.vigente_de({"pdf": "", "anexos": []}) is None
print("5. documento sin versión vigente: OK")

# 6. URL con acentos: el sitio publica rutas como
# «Manual_integración_funcionamiento_CA.pdf» y urllib no admite no-ASCII.
u = C.absoluta("/PDF/2020/Manual_integración_funcionamiento_CA.pdf")
assert u == "https://ieenayarit.org/PDF/2020/Manual_integraci%C3%B3n_funcionamiento_CA.pdf", u
assert all(ord(c) < 128 for c in u)
assert C.escapar(u) == u, "escapar debe ser idempotente"
assert C.absoluta("/PDF/2025/Acuerdos/IEEN-CLE-015-2025-A1.pdf").endswith(
    "/PDF/2025/Acuerdos/IEEN-CLE-015-2025-A1.pdf")
print("6. URL con acentos escapadas, sin doble escape: OK")

print("\nTodas las pruebas pasaron.")

