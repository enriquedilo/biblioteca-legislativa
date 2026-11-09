#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Catálogo del Instituto Estatal Electoral de Nayarit.

Lee las dos páginas de normatividad del IEEN y deja un catálogo estable con
la versión vigente de cada ordenamiento. No descarga los PDF ni convierte:
eso es trabajo del pipeline de conversión, con supervisión.

Las páginas son una aplicación de Vue, pero el arreglo `documentos` viene
embebido en el HTML como literal de JavaScript: claves sin comillas, cadenas
con escapes \\/ y \\uXXXX, y coma sobrante antes del corchete de cierre. Se
extrae con un recorrido que respeta las cadenas y se normaliza a JSON. No
hace falta navegador.

Salida:
  IEEN/catalogo/normatividad.json

Uso:
    python3 bin/catalogo_ieen.py [--verificar] [--salida RUTA]
"""
import argparse, json, os, re, sys, time
import urllib.request, urllib.error, urllib.parse
from datetime import datetime, timezone

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BASE = "https://ieenayarit.org"
FUENTES = (
    ("normatividad", BASE + "/normatividad/IEEN"),
    ("interna",      BASE + "/normatividad/Interna"),
)
UA = ("biblioteca-legislativa/1.0 (catálogo del IEEN; "
      "+github.com/enriquedilo/biblioteca-legislativa)")
TIMEOUT = 30
REINTENTOS = 2
PAUSA = 0.4  # cortesía con el servidor del Instituto

# Los ocho documentos de «Legislación Local» del catálogo del IEEN son leyes
# del Congreso de Nayarit que la biblioteca ya tiene por su fuente oficial.
# No se duplican: se deja constancia de a dónde apuntan. El Compendio
# Electoral es una recopilación de esas mismas leyes en un solo PDF de 207 MB,
# y queda fuera por redundante.
YA_EN_LA_BIBLIOTECA = {
    1: ("Nayarit", 5),    # Constitución Política del Estado Libre y Soberano
    2: ("Nayarit", 55),   # Ley Electoral del Estado de Nayarit
    3: ("Nayarit", 79),   # Ley de Justicia Electoral (LJEN) — confirmar cotejo
    4: ("Nayarit", 86),   # Ley de Participación Ciudadana
    5: ("Nayarit", 122),  # Ley de Transparencia y Acceso a la Información
    7: ("Nayarit", 9),    # Ley de Adquisiciones, Arrendamientos y Servicios
    8: ("Nayarit", 91),   # Ley de Presupuestación, Contabilidad y Gasto
}
EXCLUIDOS = {6: "recopilación de leyes que la biblioteca ya tiene por separado"}

RE_DOCUMENTOS = re.compile(r"\bdocumentos\s*:\s*\[")


def pedir(url, metodo="GET"):
    """Devuelve (cabeceras, cuerpo_o_None). Lanza la última excepción."""
    ultimo = None
    for intento in range(REINTENTOS + 1):
        try:
            pet = urllib.request.Request(escapar(url), method=metodo,
                                         headers={"User-Agent": UA})
            with urllib.request.urlopen(pet, timeout=TIMEOUT) as r:
                cuerpo = r.read() if metodo == "GET" else None
                return dict(r.headers), cuerpo
        except Exception as e:          # noqa: BLE001 - se reintenta y se reporta
            ultimo = e
            time.sleep(PAUSA * (intento + 1))
    raise ultimo


def _recorte(html):
    """Devuelve el literal del arreglo `documentos`, con sus corchetes."""
    m = RE_DOCUMENTOS.search(html)
    if not m:
        raise ValueError("la página no trae el arreglo `documentos`")
    i = html.index("[", m.start())
    hondo, k = 0, i
    while k < len(html):
        c = html[k]
        if c == '"':                     # saltar la cadena completa
            k += 1
            while k < len(html):
                if html[k] == "\\":
                    k += 2
                    continue
                if html[k] == '"':
                    break
                k += 1
        elif c == "[":
            hondo += 1
        elif c == "]":
            hondo -= 1
            if hondo == 0:
                return html[i:k + 1]
        k += 1
    raise ValueError("el arreglo `documentos` no cierra")


def a_json(bruto):
    """Literal de JavaScript -> JSON: entrecomilla las claves y quita la
    coma sobrante. Respeta las cadenas, para no tocar un `algo:` que viva
    dentro del nombre de un ordenamiento."""
    out, k = [], 0
    while k < len(bruto):
        c = bruto[k]
        if c == '"':
            j = k + 1
            trozo = ['"']
            while j < len(bruto):
                if bruto[j] == "\\":
                    trozo.append(bruto[j:j + 2])
                    j += 2
                    continue
                if bruto[j] == '"':
                    trozo.append('"')
                    j += 1
                    break
                trozo.append(bruto[j])
                j += 1
            out.append("".join(trozo))
            k = j
            continue
        if c.isalpha() or c == "_":
            j = k
            while j < len(bruto) and (bruto[j].isalnum() or bruto[j] == "_"):
                j += 1
            ident = bruto[k:j]
            t = j
            while t < len(bruto) and bruto[t].isspace():
                t += 1
            out.append('"%s"' % ident if t < len(bruto) and bruto[t] == ":"
                       else ident)
            k = j
            continue
        if c == ",":
            t = k + 1
            while t < len(bruto) and bruto[t].isspace():
                t += 1
            if t < len(bruto) and bruto[t] in "]}":
                k += 1
                continue
        out.append(c)
        k += 1
    return json.loads("".join(out))


def extraer(html):
    return a_json(_recorte(html))


def fecha_iso(s):
    """«28/01/2016» -> «2016-01-28». «2021» -> «2021». Vacío -> None."""
    s = (s or "").strip()
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", s)
    if m:
        return "%s-%s-%s" % (m.group(3), m.group(2), m.group(1))
    return s if re.fullmatch(r"\d{4}", s) else None


# Caracteres que no se tocan al escapar una URL. El % va dentro a proposito:
# asi volver a escapar una URL ya escapada no la rompe.
SEGUROS = "/%:@&=+$,;~!*'()?#[]"


def escapar(u):
    """Deja la URL en ASCII. El sitio publica rutas con acentos
    -«Manual_integración_funcionamiento_CA.pdf»- y urllib no las acepta:
    revienta con UnicodeEncodeError antes de salir a la red."""
    partes = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((
        partes.scheme, partes.netloc,
        urllib.parse.quote(partes.path, safe=SEGUROS),
        urllib.parse.quote(partes.query, safe=SEGUROS),
        urllib.parse.quote(partes.fragment, safe=SEGUROS)))


def absoluta(u):
    u = (u or "").strip()
    if not u:
        return None
    return escapar(u if u.startswith("http") else BASE + u)


def vigente_de(doc):
    """La versión en vigor: el PDF propio si lo hay; si no, el acuerdo de
    reforma más reciente. El sitio no lista los anexos en orden constante
    -unos van del más viejo al más nuevo y otros al revés-, así que se
    escoge por fecha, nunca por posición."""
    if doc.get("pdf"):
        return {"acuerdo": doc.get("acuerdo") or None,
                "fecha": fecha_iso(doc.get("fecha")),
                "url": absoluta(doc["pdf"]), "origen": "documento"}
    anexos = [a for a in doc.get("anexos") or [] if a.get("pdf")]
    if not anexos:
        return None
    ultimo = max(anexos, key=lambda a: (fecha_iso(a.get("fecha")) or "", a.get("pdf")))
    return {"acuerdo": ultimo.get("acuerdo") or None,
            "fecha": fecha_iso(ultimo.get("fecha")),
            "url": absoluta(ultimo["pdf"]), "origen": "acuerdo de reforma"}


def normalizar(seccion, fuente, docs):
    salida = []
    for d in docs:
        num = d.get("numero")
        clave = "%s-%s" % (seccion, num)
        reg = {
            "clave": clave,
            "seccion": seccion,
            "numero": num,
            "tipo": d.get("tipo"),
            "nombre": (d.get("nombre") or "").strip(),
            "fuente": fuente,
            "vigente": vigente_de(d),
            "reformas": [
                {"acuerdo": a.get("acuerdo") or None,
                 "fecha": fecha_iso(a.get("fecha")),
                 "url": absoluta(a.get("pdf"))}
                for a in d.get("anexos") or []
            ],
        }
        if seccion == "normatividad" and num in YA_EN_LA_BIBLIOTECA:
            ent, idl = YA_EN_LA_BIBLIOTECA[num]
            reg["en_la_biblioteca"] = {"entidad": ent, "id": idl}
        if seccion == "normatividad" and num in EXCLUIDOS:
            reg["excluido"] = EXCLUIDOS[num]
        salida.append(reg)
    return salida


def verificar(registros):
    """Comprueba que la URL vigente responde y anota tamaño y Last-Modified.
    Es la misma lectura barata de cabeceras que usa bin/vigilancia.py."""
    for r in registros:
        v = r.get("vigente")
        if not v or r.get("excluido") or r.get("en_la_biblioteca"):
            continue
        try:
            cab, _ = pedir(v["url"], "HEAD")
            v["verificacion"] = {
                "estado": 200,
                "tipo": cab.get("Content-Type"),
                "bytes": int(cab.get("Content-Length") or 0) or None,
                "last_modified": cab.get("Last-Modified"),
                "etag": cab.get("ETag"),
            }
        except urllib.error.HTTPError as e:
            v["verificacion"] = {"estado": e.code}
        except Exception as e:           # noqa: BLE001
            v["verificacion"] = {"estado": None, "error": str(e)[:120]}
        time.sleep(PAUSA)


def main():
    p = argparse.ArgumentParser(description="Catálogo normativo del IEEN")
    p.add_argument("--verificar", action="store_true",
                   help="pedir cabeceras de cada PDF vigente")
    p.add_argument("--salida", default=os.path.join(RAIZ, "IEEN", "catalogo",
                                                    "normatividad.json"))
    a = p.parse_args()

    registros = []
    for seccion, url in FUENTES:
        html = pedir(url)[1].decode("utf-8", "replace")
        docs = extraer(html)
        print("%s: %d documentos" % (seccion, len(docs)))
        registros += normalizar(seccion, url, docs)

    if a.verificar:
        verificar(registros)

    porconvertir = [r for r in registros
                    if not r.get("excluido") and not r.get("en_la_biblioteca")]
    doc = {
        "entidad": "IEEN",
        "nombre": "Instituto Estatal Electoral de Nayarit",
        "generado": datetime.now(timezone.utc).isoformat(),
        "fuentes": [u for _, u in FUENTES],
        "nota": ("Detección de catálogo. La versión vigente de un reglamento "
                 "suele ser el anexo del acuerdo que lo reformó: se elige por "
                 "fecha, no por posición en la lista."),
        "conteo": {
            "total": len(registros),
            "por_convertir": len(porconvertir),
            "ya_en_la_biblioteca": sum(1 for r in registros if r.get("en_la_biblioteca")),
            "excluidos": sum(1 for r in registros if r.get("excluido")),
            "sin_version_vigente": sum(1 for r in porconvertir if not r["vigente"]),
            "reformas_registradas": sum(len(r["reformas"]) for r in registros),
        },
        "documentos": registros,
    }
    os.makedirs(os.path.dirname(a.salida), exist_ok=True)
    with open(a.salida, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(json.dumps(doc["conteo"], ensure_ascii=False))
    print("escrito en", os.path.relpath(a.salida, RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
