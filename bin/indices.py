#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Capa de indices derivados de la Biblioteca Legislativa.

No modifica el acervo: solo lee ordenamientos/<id>/actual/ y escribe en
Sinaloa/indices/. Todo lo que produce es regenerable y desechable.

Uso:  python3 bin/indices.py [articulos|remisiones|fts|todo]
"""
import json, os, re, sys, sqlite3, unicodedata
from datetime import datetime, timezone

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ENTIDADES_CONOCIDAS = ("Sinaloa", "Nayarit", "Federal")
ENTIDAD = "Sinaloa"
SIN = os.path.join(RAIZ, ENTIDAD)
ORD = os.path.join(SIN, "ordenamientos")
IDX = os.path.join(SIN, "indices")


def usar_entidad(nombre):
    """Apunta el generador a la biblioteca de una entidad."""
    global ENTIDAD, SIN, ORD, IDX
    ENTIDAD = nombre
    SIN = os.path.join(RAIZ, nombre)
    ORD = os.path.join(SIN, "ordenamientos")
    IDX = os.path.join(SIN, "indices")
    if not os.path.isdir(ORD):
        raise SystemExit(f"No existe {ORD}")


def entidades_disponibles():
    return [e for e in ENTIDADES_CONOCIDAS
            if os.path.isdir(os.path.join(RAIZ, e, "ordenamientos"))]

MESES = {m: i + 1 for i, m in enumerate(
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
     "agosto", "septiembre", "octubre", "noviembre", "diciembre"])}
MESES["setiembre"] = 9

RE_PAGINA = re.compile(r"<!--\s*PAGINA_PDF:\s*(\d+)\s*-->")
# Encabezados de articulo: "### Artículo 47." / "### ARTÍCULO 1o." / "### Artículo 12 Bis."
RE_ART = re.compile(
    r"^#{1,4}\s*[.,;:]?\s*(?:ART[IÍ]CULOS?\.?|ART[O]?\.)\s*([0-9][0-9,]*)\s*(?:(?:o|º|°)(?![A-ZÁÉÍÓÚa-záéíóú]))?\s*[.\-–]*\s*"
    r"((?:[-–A-ZÁÉÍÓÚa-záéíóú][-–A-ZÁÉÍÓÚa-záéíóú.\s0-9]{0,25})?)$",
    re.IGNORECASE)
# Encabezado cortado por salto de pagina: "### ARTÍCULO 29-" y el sufijo abajo.
RE_SUFIJO_SIG = re.compile(r"^\**\s*((?:BIS|TER|QUATER|QUINQUIES|SEXIES)?[-\s]*[A-Z])\s*\.", re.IGNORECASE)
ORDINAL_SUELTO = re.compile(r"^(?:o|º|°|bis|ter)?$", re.IGNORECASE)


def norm_sufijo(s):
    if not s:
        return ""
    s = " ".join(s.replace(".", " ").split()).upper().strip(" -")
    if not s or not re.fullmatch(r"[-–A-ZÁÉÍÓÚ][-–A-ZÁÉÍÓÚ0-9\s]*", s):
        return ""
    return re.sub(r"\s*-\s*", "-", s)


RE_TRANS_TIT = re.compile(r"^#{1,4}\s*(ART[IÍ]CULOS?\s+)?TRANSITORIOS?\s*:?\s*$", re.IGNORECASE)
ORDINALES = ("ÚNICO UNICO PRIMERO SEGUNDO TERCERO CUARTO QUINTO SEXTO SÉPTIMO SEPTIMO "
             "OCTAVO NOVENO DÉCIMO DECIMO UNDÉCIMO UNDECIMO DUODÉCIMO DUODECIMO").split()
RE_TRANS_ART = re.compile(r"^\**\s*(?:ART[IÍ]CULO\s+)?(" + "|".join(ORDINALES) + r")\s*(BIS)?\s*[\.\-—]", re.IGNORECASE)
# Leyes antiguas que numeran el CUERPO con ordinales en letra (p. ej. Nayarit 31 y 34).
RE_ART_ORDINAL = re.compile(r"^\**\s*ART[IÍ]CULO\s+(" + "|".join(ORDINALES) + r")\s*(BIS)?\s*[\.\-—]", re.IGNORECASE)
# Nota de reforma al pie de articulo o inline
RE_NOTA = re.compile(
    r"\((?:\s*)((?:Ref|Adic|Der|Reformad|Adicionad|Derogad|Fe\s+de\s+erratas)[^)]{0,300}?)\)",
    re.IGNORECASE | re.DOTALL)
# Formato federal (Camara de Diputados): la nota va sin parentesis y pegada al
# final del parrafo, con una o varias fechas DOF.
#   "Parrafo reformado DOF 30-09-2024"
#   "Articulo reformado DOF 20-12-1991, 18-12-1992, 28-12-1994"
RE_NOTA_DOF = re.compile(
    r"((?:Art[ií]culo|P[áa]rrafo|Fracci[óo]n|Inciso|Apartado|Denominaci[óo]n|"
    r"Cap[ií]tulo|Secci[óo]n|T[ií]tulo|Libro|Ep[ií]grafe|Ap[ée]ndice)"
    r"[^.]{0,90}?"
    r"(?:reformad[oa]|adicionad[oa]|derogad[oa]|recorrid[oa]|reubicad[oa]|"
    r"renumerad[oa]|fe\s+de\s+erratas)"
    r"[^.]{0,60}?"
    r"DOF\s+((?:\d{2}-\d{2}-\d{4}(?:\s*,\s*)?)+))",
    re.IGNORECASE)
RE_FECHA_DOF = re.compile(r"(\d{2})-(\d{2})-(\d{4})")

RE_DEC = re.compile(r"Dec(?:reto)?\.?\s*(?:No\.?|N[uú]m\.?)?\s*([0-9]{1,4})", re.IGNORECASE)
RE_PO = re.compile(r"P\.?\s*O\.?\s*(?:No\.?|N[uú]m\.?)?\s*([0-9]{1,4})", re.IGNORECASE)
RE_FECHA = re.compile(r"([0-9]{1,2})\s*de\s*([A-Za-zÁÉÍÓÚáéíóúü]+)\s*(?:de[l]?\s*)?([0-9]{4})", re.IGNORECASE)


def sin_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()


def fecha_iso(txt):
    m = RE_FECHA.search(txt)
    if not m:
        return None
    d, mes, a = m.group(1), sin_acentos(m.group(2)), m.group(3)
    if mes not in MESES:
        return None
    try:
        return datetime(int(a), MESES[mes], int(d)).strftime("%Y-%m-%d")
    except ValueError:
        return None


def tipo_nota(txt):
    t = sin_acentos(txt)
    if t.startswith("fe de erratas"):
        return "fe_de_erratas"
    if t.startswith(("ref", "reformad")):
        return "reforma"
    if t.startswith(("adic", "adicionad")):
        return "adicion"
    if t.startswith(("der", "derogad")):
        return "derogacion"
    return "otra"


def parse_notas_dof(bloque):
    """Notas al estilo federal: sin parentesis, con una o varias fechas DOF."""
    out, vistos = [], set()
    for m in RE_NOTA_DOF.finditer(bloque):
        crudo = " ".join(m.group(1).split())
        fechas = []
        for d, mes, a in RE_FECHA_DOF.findall(m.group(2)):
            try:
                fechas.append(datetime(int(a), int(mes), int(d)).strftime("%Y-%m-%d"))
            except ValueError:
                pass
        if not fechas:
            continue
        t = sin_acentos(crudo)
        tipo = ("fe_de_erratas" if "fe de erratas" in t else
                "adicion" if "adicionad" in t else
                "derogacion" if "derogad" in t else
                "reforma" if "reformad" in t else "otra")
        ambito = sin_acentos(crudo.split()[0])
        for f in fechas:
            clave = (tipo, ambito, f)
            if clave in vistos:
                continue
            vistos.add(clave)
            out.append({"tipo": tipo, "ambito": ambito, "decreto": None,
                        "po_numero": None, "fecha": f, "diario": "DOF",
                        "nota": crudo[:300]})
    return out


def parse_notas(bloque):
    out, vistos = [], set()
    for m in RE_NOTA.finditer(bloque):
        crudo = " ".join(m.group(1).split())
        dec = RE_DEC.search(crudo)
        po = RE_PO.search(crudo)
        reg = {
            "tipo": tipo_nota(crudo),
            "decreto": dec.group(1) if dec else None,
            "po_numero": po.group(1) if po else None,
            "fecha": fecha_iso(crudo),
            "nota": crudo[:300],
        }
        clave = (reg["tipo"], reg["decreto"], reg["po_numero"], reg["fecha"])
        if clave in vistos:
            continue
        vistos.add(clave)
        out.append(reg)
    if not out:
        out = parse_notas_dof(bloque)
    return out


RE_PORTADA_CD = re.compile(
    r"^\s*(.{8,200}?)\s+C[ÁA]MARA DE DIPUTADOS DEL H\. CONGRESO DE LA UNI[ÓO]N",
    re.MULTILINE)


def nombre_utilizable(meta, txt):
    """Nombre para los indices. Algunos catalogos (reglamentos federales)
    traen la fecha DOF en lugar del nombre: se toma entonces el nombre oficial
    o, si falta, el que imprime el encabezado de pagina de la compilacion."""
    nc = (meta.get("nombre_catalogo") or "").strip()
    if nc and not re.match(r"^DOF\s", nc):
        return nc, False
    no = (meta.get("nombre_oficial") or "").strip()
    if no:
        return no, True
    m = RE_PORTADA_CD.search(txt[:6000])
    if m:
        return " ".join(m.group(1).split()), True
    return nc or meta.get("sigla") or "", True


def leer(idl):
    base = os.path.join(ORD, idl, "actual")
    meta = json.load(open(os.path.join(base, "metadata.json"), encoding="utf-8"))
    txt = open(os.path.join(base, "texto.md"), encoding="utf-8", errors="replace").read()
    nombre, derivado = nombre_utilizable(meta, txt)
    if derivado:
        meta["nombre_catalogo_original"] = meta.get("nombre_catalogo")
        meta["nombre_catalogo"] = nombre
        meta["nombre_derivado_de_portada"] = True
    return meta, txt


def articulos_de(texto):
    """Devuelve lista de articulos con sus limites, pagina y texto."""
    lineas = texto.split("\n")
    pagina, en_trans = None, False
    marcas = []  # (indice_linea, numero, tipo, pagina)
    for i, ln in enumerate(lineas):
        mp = RE_PAGINA.search(ln)
        if mp:
            pagina = int(mp.group(1))
            continue
        if RE_TRANS_TIT.match(ln.strip()):
            en_trans = True
            continue
        ma = RE_ART.match(ln.strip())
        if ma:
            suf = norm_sufijo(ma.group(2))
            if not suf and ln.strip().rstrip().endswith("-"):
                for j in range(i + 1, min(i + 4, len(lineas))):
                    sig = lineas[j].strip()
                    if not sig or RE_PAGINA.search(sig):
                        continue
                    ms = RE_SUFIJO_SIG.match(sig)
                    if ms:
                        suf = norm_sufijo(ms.group(1))
                    break
            num = ma.group(1).replace(",", "") + (" " + suf if suf else "")
            marcas.append((i, num, "transitorio" if en_trans else "cuerpo", pagina))
            continue
        mt = RE_TRANS_ART.match(ln.strip())
        if mt and en_trans:
            num = mt.group(1).upper() + (" BIS" if mt.group(2) else "")
            marcas.append((i, num, "transitorio", pagina))
    if not any(t == "cuerpo" for _, _, t, _ in marcas):
        en_trans = False
        pagina = None
        extra = []
        for i, ln in enumerate(lineas):
            mp = RE_PAGINA.search(ln)
            if mp:
                pagina = int(mp.group(1))
                continue
            if RE_TRANS_TIT.match(ln.strip()):
                en_trans = True
                continue
            if en_trans:
                continue
            mo = RE_ART_ORDINAL.match(ln.strip())
            if mo:
                extra.append((i, mo.group(1).upper() + (" BIS" if mo.group(2) else ""),
                              "cuerpo", pagina))
        if extra:
            marcas = sorted(marcas + extra, key=lambda x: x[0])

    arts = []
    for k, (i, num, tipo, pag) in enumerate(marcas):
        fin = marcas[k + 1][0] if k + 1 < len(marcas) else len(lineas)
        cuerpo = "\n".join(lineas[i:fin])
        limpio = RE_PAGINA.sub("", cuerpo).strip()
        arts.append({
            "articulo": num, "tipo": tipo, "pagina_pdf": pag,
            "linea_inicio": i + 1, "linea_fin": fin,
            "caracteres": len(limpio),
            "reformas": parse_notas(cuerpo),
            "_texto": limpio,
        })
    return arts


def ids():
    return sorted([d for d in os.listdir(ORD) if d.isdigit()], key=int)


# ---------------------------------------------------------------- articulado
def gen_articulos():
    dest = os.path.join(IDX, "articulos")
    os.makedirs(dest, exist_ok=True)
    resumen = []
    for idl in ids():
        meta, txt = leer(idl)
        arts = articulos_de(txt)
        cuerpo = [a for a in arts if a["tipo"] == "cuerpo"]
        trans = [a for a in arts if a["tipo"] == "transitorio"]
        notas = sum(len(a["reformas"]) for a in arts)
        doc = {
            "id": int(idl),
            "nombre": meta.get("nombre_catalogo"),
            "nombre_oficial": meta.get("nombre_oficial"),
            "version": meta.get("version"),
            "ruta_texto": f"{ENTIDAD}/ordenamientos/{idl}/actual/texto.md",
            "generado": datetime.now(timezone.utc).isoformat(),
            "conteo": {"cuerpo": len(cuerpo), "transitorios": len(trans),
                       "notas_de_reforma": notas},
            "articulos": [{k: v for k, v in a.items() if k != "_texto"} for a in arts],
        }
        with open(os.path.join(dest, f"{idl}.json"), "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        resumen.append({"id": int(idl), "nombre": doc["nombre"],
                        **doc["conteo"]})
    with open(os.path.join(IDX, "articulado_resumen.json"), "w", encoding="utf-8") as f:
        json.dump({"generado": datetime.now(timezone.utc).isoformat(),
                   "ordenamientos": len(resumen), "detalle": resumen},
                  f, ensure_ascii=False, indent=1)
    return resumen


# -------------------------------------------------------------------- fts
DDL = """
DROP TABLE IF EXISTS leyes;
CREATE TABLE leyes (
  id INTEGER PRIMARY KEY, nombre TEXT, nombre_oficial TEXT,
  decreto TEXT, po_numero TEXT, po_fecha TEXT,
  ultima_reforma_fecha TEXT, ultima_reforma_po TEXT,
  reformas_tabla INTEGER, abroga INTEGER,
  fecha_descarga TEXT, validacion TEXT, ruta TEXT
);
DROP TABLE IF EXISTS articulos;
CREATE VIRTUAL TABLE articulos USING fts5(
  ley_id UNINDEXED, ley, articulo UNINDEXED, tipo UNINDEXED,
  pagina UNINDEXED, linea UNINDEXED, texto,
  tokenize="unicode61 remove_diacritics 2"
);
"""


def _campo(d, *ruta):
    for r in ruta:
        if not isinstance(d, dict):
            return None
        d = d.get(r)
    return d if not isinstance(d, (dict, list)) else None


def gen_fts():
    os.makedirs(IDX, exist_ok=True)
    ruta = os.path.join(IDX, "biblioteca.db")
    # El montaje de carpetas compartidas no soporta el bloqueo de SQLite:
    # se construye en almacenamiento local y se copia al final.
    tmp = os.path.join(os.environ.get("TMPDIR", "/tmp"), "biblioteca_fts.db")
    for f in (tmp, tmp + "-journal", tmp + "-wal"):
        if os.path.exists(f):
            os.remove(f)
    con = sqlite3.connect(tmp)
    con.executescript(DDL)
    nart = 0
    for idl in ids():
        meta, txt = leer(idl)
        con.execute(
            "INSERT INTO leyes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (int(idl), meta.get("nombre_catalogo"), meta.get("nombre_oficial"),
             meta.get("decreto_numero"),
             _campo(meta, "po_publicacion", "numero"),
             _campo(meta, "po_publicacion", "fecha"),
             _campo(meta, "ultima_reforma", "fecha"),
             _campo(meta, "ultima_reforma", "po_numero"),
             len(meta.get("reformas") or []), len(meta.get("abroga") or []),
             meta.get("fecha_descarga"), meta.get("validacion"),
             f"{ENTIDAD}/ordenamientos/{idl}/actual/texto.md"))
        for a in articulos_de(txt):
            con.execute("INSERT INTO articulos VALUES (?,?,?,?,?,?,?)",
                        (int(idl), meta.get("nombre_catalogo"), a["articulo"],
                         a["tipo"], a["pagina_pdf"], a["linea_inicio"], a["_texto"]))
            nart += 1
    con.commit()
    con.execute("INSERT INTO articulos(articulos) VALUES('optimize')")
    con.commit()
    con.close()
    import shutil
    shutil.copyfile(tmp, ruta)
    os.remove(tmp)
    return nart


# ------------------------------------------------------------- remisiones
GENERICOS = {"ley", "codigo", "constitucion", "esta ley", "la ley"}


def _nombres():
    """Nombres buscables por ordenamiento, del mas largo al mas corto."""
    reg = []
    for idl in ids():
        meta, _ = leer(idl)
        for n in {meta.get("nombre_oficial"), meta.get("nombre_catalogo")}:
            if not n or len(n) < 12:
                continue
            reg.append((sin_acentos(n), int(idl), n))
    reg.sort(key=lambda r: -len(r[0]))
    return reg


def gen_remisiones():
    os.makedirs(IDX, exist_ok=True)
    nombres = _nombres()
    aristas = {}
    for idl in ids():
        meta, txt = leer(idl)
        arts = articulos_de(txt)
        plano = sin_acentos(RE_PAGINA.sub("", txt))
        # posiciones ocupadas: evita que "Ley de Cultura" case dentro de
        # "Ley de Cultura Fisica y Deporte"
        ocupado = []
        for clave, destino, canon in nombres:
            if destino == int(idl):
                continue
            ini = 0
            while True:
                p = plano.find(clave, ini)
                if p < 0:
                    break
                ini = p + 1
                if any(a <= p < b for a, b in ocupado):
                    continue
                ocupado.append((p, p + len(clave)))
                # ubicar el articulo por offset de linea
                linea = plano.count("\n", 0, p) + 1
                art = None
                for a in arts:
                    if a["linea_inicio"] <= linea <= a["linea_fin"]:
                        art = a
                        break
                k = (int(idl), destino)
                e = aristas.setdefault(k, {
                    "origen": int(idl), "origen_nombre": meta.get("nombre_catalogo"),
                    "destino": destino, "destino_nombre": canon,
                    "menciones": 0, "articulos": []})
                e["menciones"] += 1
                if art and art["articulo"] not in [x["articulo"] for x in e["articulos"]]:
                    e["articulos"].append({"articulo": art["articulo"],
                                           "tipo": art["tipo"],
                                           "pagina_pdf": art["pagina_pdf"]})
    salida = sorted(aristas.values(), key=lambda e: (-e["menciones"], e["origen"]))
    for e in salida:
        e["articulos"] = e["articulos"][:25]
    doc = {"generado": datetime.now(timezone.utc).isoformat(),
           "aristas": len(salida),
           "nota": ("Mencion nominal de un ordenamiento de la biblioteca dentro del "
                    "texto de otro. Es deteccion lexica: no distingue remision "
                    "normativa de cita incidental."),
           "remisiones": salida}
    with open(os.path.join(IDX, "remisiones.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    return len(salida)


# ------------------------------------------------------------------ rutas web
def gen_rutas():
    """Mapa id -> rutas con el hash ya resuelto.

    El enlace `actual/` es un symlink: sirve en disco, pero no por HTTP.
    Este archivo permite a un cliente web (ChatGPT, un navegador, cualquier
    lector del repositorio) llegar al texto en un solo salto.
    """
    os.makedirs(IDX, exist_ok=True)
    reg = []
    for idl in ids():
        meta, _ = leer(idl)
        v = json.load(open(os.path.join(ORD, idl, "actual.json"),
                           encoding="utf-8"))["version"]
        base = f"{ENTIDAD}/ordenamientos/{idl}/versiones/{v}"
        reg.append({
            "id": int(idl),
            "nombre": meta.get("nombre_catalogo"),
            "nombre_oficial": meta.get("nombre_oficial"),
            "tipo": meta.get("tipo"),
            "texto": f"{base}/texto.md",
            "metadata": f"{base}/metadata.json",
            "validacion": f"{base}/validacion.json",
            "articulado": f"{ENTIDAD}/indices/articulos/{idl}.json",
        })
    doc = {
        "entidad": ENTIDAD,
        "generado": datetime.now(timezone.utc).isoformat(),
        "base_raw": ("https://raw.githubusercontent.com/enriquedilo/"
                     "biblioteca-legislativa/main/"),
        "nota": ("Rutas relativas a la raiz del repositorio, con la version "
                 "vigente ya resuelta. Antepon base_raw para leer por HTTP. "
                 "No uses el enlace actual/ por HTTP: es un symlink."),
        "ordenamientos": reg,
    }
    with open(os.path.join(IDX, "rutas.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    return len(reg)


def main():
    args = [a for a in sys.argv[1:]]
    ents = None
    if "--entidad" in args:
        j = args.index("--entidad")
        ents = [args[j + 1]]
        del args[j:j + 2]
    if ents is None or ents == ["todas"]:
        ents = entidades_disponibles()
    que = args[0] if args else "todo"
    for e in ents:
        usar_entidad(e)
        print(f"== {e} ==")
        _generar(que)


def _generar(que):
    os.makedirs(IDX, exist_ok=True)
    if que in ("articulos", "todo"):
        r = gen_articulos()
        print("articulado:", len(r), "ordenamientos,",
              sum(x["cuerpo"] for x in r), "articulos de cuerpo,",
              sum(x["notas_de_reforma"] for x in r), "notas de reforma")
    if que in ("fts", "todo"):
        print("fts:", gen_fts(), "articulos indexados")
    if que in ("remisiones", "todo"):
        print("remisiones:", gen_remisiones(), "aristas")
    if que in ("rutas", "todo"):
        print("rutas web:", gen_rutas(), "ordenamientos")


if __name__ == "__main__":
    main()
