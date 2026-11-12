#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas del filtro de enlaces de catálogo de bin/vigilancia.py. No tocan la
red: usan el inventario que ya está en el repositorio.

El caso que motivó el filtro: el HTML servido de la página de leyes de
Sinaloa trae un solo PDF, y no es un ordenamiento sino el enlace del menú a
la «Estadística Parlamentaria», que cambia de número cada mes. La lista de
leyes la arma JavaScript desde otro host y nunca está en el HTML.

Uso:
    python3 bin/pruebas_vigilancia.py
"""
import os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "bin"))
os.chdir(RAIZ)
import vigilancia as V
ETIQ = V.ETIQUETAS["enlace_fuera_del_catalogo"]

# inventario real de cada entidad, leido del acervo
for ent in ("Sinaloa", "Nayarit", "Federal"):
    inv = V.inventario(ent)
    pref = V.prefijos_de(inv)
    print(f"{ent}: {len(inv)} ordenamientos | prefijos {sorted(pref)}")

# Sinaloa: el unico PDF del HTML es el del menu -> debe quedar fuera
pref_sin = V.prefijos_de(V.inventario("Sinaloa"))
cat = "https://www.congresosinaloa.gob.mx/leyes-estatales/"
menu = ["https://iip.congresosinaloa.gob.mx/docs/est_par/est/2026/008.pdf"]
assert V.del_catalogo(menu, cat, pref_sin) == [], "el enlace del menu no debe contar"
doc = ["https://gaceta.congresosinaloa.gob.mx:3001/pdfs/leyes/Ley_3.pdf"]
assert V.del_catalogo(doc, cat, pref_sin) == doc, "un PDF de la Gaceta si debe contar"
print("Sinaloa: menu descartado, documento conservado  OK")

# Nayarit y Federal: enlaces relativos y absolutos del catalogo, conservados
pref_nay = V.prefijos_de(V.inventario("Nayarit"))
nay = ["/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes/electoral_del_estado_de_nayarit_ley.pdf"]
assert V.del_catalogo(nay, "https://congresonayarit.gob.mx/legislacion-estatal/", pref_nay) == nay
pref_fed = V.prefijos_de(V.inventario("Federal"))
fed = ["pdf/LGT.pdf", "/LeyesBiblio/doc/LGT.doc"]
assert V.del_catalogo(fed, "https://www.diputados.gob.mx/LeyesBiblio/index.htm", pref_fed) == fed
print("Nayarit y Federal: enlaces del catalogo conservados  OK")

# sin prefijos conocidos no se filtra nada (acervo nuevo, sin metadata aun)
assert V.del_catalogo(menu, cat, set()) == menu
print("sin inventario no se filtra  OK")

# --- enlace congelado: el caso de la Constitucion de Nayarit ---------------
P = "https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/"
VIEJA = P + "constitucion/Constitucion_Politica_del_Estado_Libre_y_Soberano_de_Nayarit.pdf"
NUEVA = P + "constitucion/Constitucion_Politica_del_Estado_Libre_y_Soberano_de_Nayarit-1.pdf"
OTRA  = P + "leyes/electoral_del_estado_de_nayarit_ley.pdf"

# Un acervo realista: 19 leyes bien enlazadas y la Constitucion congelada.
resto = [{"id": 100 + i, "nombre": "Ley %d" % i, "url_pdf": P + "leyes/l%d.pdf" % i}
         for i in range(19)]
inv = [{"id": 5, "nombre": "Constitucion", "url_pdf": VIEJA}] + resto
catalogo = {NUEVA, OTRA} | {it["url_pdf"] for it in resto}

h = V._huerfanos("Nayarit", inv, catalogo, {})
assert len(h) == 1 and h[0]["id"] == 5, h
assert h[0]["tipo"] == "enlace_fuera_del_catalogo"
print("huerfano detectado cuando el catalogo cambia de archivo  OK")

# si el catalogo sigue enlazando lo archivado, no se reporta nada
assert V._huerfanos("Nayarit", inv, catalogo | {VIEJA}, {}) == []
print("sin huerfanos cuando todo sigue enlazado  OK")

# cobertura baja: no se evalua, para no inventar falsos positivos
obs = {}
muchos = [{"id": i, "nombre": "x", "url_pdf": P + "r/%d.pdf" % i} for i in range(20)]
assert V._huerfanos("Federal", muchos, {P + "r/1.pdf"}, obs) == []
assert obs.get("huerfanos_no_evaluables") is True and obs["cobertura"] < 0.9
print("cobertura baja: se abstiene en vez de inventar  OK")

# el detalle nombra los archivos, que es lo que faltaba
d = V._detalle_diferencia([NUEVA], [VIEJA])
assert "Constitucion_Politica_del_Estado_Libre_y_Soberano_de_Nayarit-1.pdf" in d
assert "alta (1)" in d and "baja (1)" in d
print("el aviso nombra el archivo que entro y el que salio  OK")

# --- la caja de la URL: el fallo que dejo el control muerto ----------------
# Las rutas del Congreso traen tramos en mayusculas y el HTML no siempre
# conserva la caja. La prueba anterior usaba la misma caja de los dos lados y
# por eso pasaba con el control roto: la cobertura salia 0% y _huerfanos se
# abstenia en silencio, sin reportar nada, en todas las corridas.
MAYUS = (P + "constitucion/Constitucion_Politica_del_Estado_Libre_y_Soberano_"
         "de_Nayarit.pdf")
inv_real = [{"id": 5, "nombre": "Constitucion", "url_pdf": MAYUS}] + resto
catalogo_min = {u.lower() for u in ({NUEVA} | {it["url_pdf"] for it in resto})}

obs = {}
h = V._huerfanos("Nayarit", inv_real, catalogo_min, obs)
assert obs.get("huerfanos_no_evaluables") is not True, "se abstuvo por la caja"
assert obs["cobertura"] > 0.9, obs
assert len(h) == 1 and h[0]["id"] == 5, h
print("huerfano detectado aunque el catalogo venga en minusculas  OK")

# y al reves: lo archivado en minusculas contra un catalogo en mayusculas
inv_min = [{"id": 5, "nombre": "Constitucion", "url_pdf": MAYUS.lower()}] + resto
assert V._huerfanos("Nayarit", inv_min, {MAYUS} | {it["url_pdf"] for it in resto}, {}) == []
print("sin falsos huerfanos por diferencia de caja  OK")

# --- el reporte no puede omitir una categoria ------------------------------
import tempfile, os as _os
V.VIG = tempfile.mkdtemp()
V.escribir_reporte([{"tipo": "enlace_fuera_del_catalogo", "entidad": "Nayarit",
                     "id": 5, "nombre": "Constitucion", "url": MAYUS,
                     "detalle": "el catalogo ya no enlaza este archivo"}],
                   736, 10, [])
txt = open(_os.path.join(V.VIG, "reporte.md"), encoding="utf-8").read()
assert "Constitucion" in txt and ETIQ in txt, txt[:400]
print("el reporte imprime la categoria de enlace huerfano  OK")

# una categoria imprevista tampoco desaparece
V.escribir_reporte([{"tipo": "categoria_que_no_existia", "entidad": "Nayarit",
                     "id": 1, "nombre": "X", "detalle": "y"}], 1, 1, [])
assert "categoria_que_no_existia" in open(_os.path.join(V.VIG, "reporte.md"),
                                          encoding="utf-8").read()
print("una categoria nueva no se pierde por no estar en la lista  OK")

# --- ejercicio siguiente: lo que no se reforma, se sustituye ---------------
# Una ley de ingresos no cambia: la del ano que viene es otro archivo con otro
# nombre. Vigilar el archivo vigente nunca lo detecta.
c = V.urls_del_siguiente_ejercicio(
    "https://x.gob.mx/leyes/ley_de_ingresos_del_estado_2026.pdf")
assert c[0].endswith("ley_de_ingresos_del_estado_2027.pdf"), c

# ano en la carpeta y en el archivo: se sustituyen los dos, y se prueba
# tambien solo el ultimo por si el sitio versiona nada mas uno
c = V.urls_del_siguiente_ejercicio("https://x.gob.mx/presupuesto/2026/pe_2026.pdf")
assert "https://x.gob.mx/presupuesto/2027/pe_2027.pdf" in c, c
assert "https://x.gob.mx/presupuesto/2026/pe_2027.pdf" in c, c

# una URL sin ano no genera candidatas, y nunca se devuelve la misma
assert V.urls_del_siguiente_ejercicio("https://x.gob.mx/leyes/codigo_civil.pdf") == []
assert all(u != "https://x.gob.mx/a_2026.pdf"
           for u in V.urls_del_siguiente_ejercicio("https://x.gob.mx/a_2026.pdf"))
print("candidatas del ejercicio siguiente  OK")

# un ordenamiento sin vigencia_anual no se prueba, aunque traiga ano
assert V.revisar_ejercicio_anual(
    {"entidad": "Federal", "id": 1, "nombre": "X", "url_pdf":
     "https://x.gob.mx/a_2026.pdf", "vigencia_anual": False}) == []
print("solo se prueban los marcados vigencia_anual  OK")

print("\nTodas las pruebas pasaron.")


