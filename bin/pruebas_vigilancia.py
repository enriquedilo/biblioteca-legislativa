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
print("\nTodas las pruebas pasaron.")
