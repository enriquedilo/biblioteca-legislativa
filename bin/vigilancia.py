#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vigilancia de reformas de la Biblioteca Legislativa.

DETECTA, no convierte. Recorre las URLs de origen de cada ordenamiento y
reporta cuáles cambiaron respecto de lo que la biblioteca tiene registrado.
La conversión y validación se hacen aparte, bajo supervisión.

Estrategia en dos niveles:
  1. HEAD: pide solo cabeceras (Last-Modified, ETag, Content-Length). Barato.
  2. Si las cabeceras no son concluyentes, descarga y compara SHA-256 contra
     el hash declarado en metadata.json.

Salidas:
  vigilancia/estado.json   estado observado, para comparar la próxima vez
  vigilancia/reporte.md    reporte legible de la corrida

Uso:
    python3 bin/vigilancia.py [--entidad Sinaloa] [--forzar-descarga]
"""
import argparse, hashlib, json, os, sys, time
import urllib.request, urllib.error
from datetime import datetime, timezone

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
VIG = os.path.join(RAIZ, "vigilancia")
ENTIDADES = ("Sinaloa", "Nayarit")
UA = ("biblioteca-legislativa/1.0 (vigilancia de reformas; "
      "+github.com/enriquedilo/biblioteca-legislativa)")
TIMEOUT = 30
REINTENTOS = 2
PAUSA = 0.4  # cortesía con los servidores del Congreso

CATALOGOS = {
    "Sinaloa": "https://gaceta.congresosinaloa.gob.mx/#/leyes",
    "Nayarit": "https://congresonayarit.gob.mx/legislacion-estatal/",
}


def pedir(url, metodo="HEAD"):
    """Devuelve (cabeceras, cuerpo_o_None, error_o_None)."""
    for intento in range(REINTENTOS + 1):
        try:
            req = urllib.request.Request(url, method=metodo,
                                         headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                h = {k.lower(): v for k, v in r.headers.items()}
                cuerpo = r.read() if metodo == "GET" else None
                return h, cuerpo, None
        except urllib.error.HTTPError as e:
            if e.code in (403, 405) and metodo == "HEAD":
                return None, None, "head_no_permitido"
            if intento == REINTENTOS:
                return None, None, "http_%d" % e.code
        except Exception as e:
            if intento == REINTENTOS:
                return None, None, type(e).__name__
        time.sleep(1 + intento)
    return None, None, "desconocido"


def firma(h):
    """Firma comparable a partir de cabeceras, si el servidor coopera."""
    if not h:
        return None
    etag = (h.get("etag") or "").strip('"')
    lm = h.get("last-modified") or ""
    ln = h.get("content-length") or ""
    if not (etag or lm or ln):
        return None
    return {"etag": etag or None, "last_modified": lm or None,
            "content_length": int(ln) if ln.isdigit() else None}


def inventario(entidad):
    """Lee de la biblioteca: id, nombre, urls y hashes declarados."""
    base = os.path.join(RAIZ, entidad, "ordenamientos")
    reg = []
    if not os.path.isdir(base):
        return reg
    for idl in sorted((d for d in os.listdir(base) if d.isdigit()), key=int):
        m = os.path.join(base, idl, "actual", "metadata.json")
        if not os.path.exists(m):
            continue
        d = json.load(open(m, encoding="utf-8"))
        urls = d.get("urls") or {}
        hs = d.get("hash_sha256") or {}
        reg.append({
            "entidad": entidad, "id": int(idl),
            "nombre": d.get("nombre_catalogo") or d.get("nombre_oficial"),
            "url_pdf": urls.get("pdf") or d.get("url_pdf"),
            "url_word": urls.get("word") or d.get("url_word"),
            "sha_pdf": hs.get("pdf"),
            "sha_word": hs.get("word") or hs.get("doc") or hs.get("docx"),
        })
    return reg


def revisar(item, previo, forzar):
    """Revisa un ordenamiento. Devuelve (registro_estado, lista_hallazgos)."""
    obs = {"id": item["id"], "entidad": item["entidad"], "nombre": item["nombre"]}
    hallazgos = []
    for clase in ("pdf", "word"):
        url = item.get("url_" + clase)
        if not url:
            continue
        h, _, err = pedir(url, "HEAD")
        if err and err.startswith("http_404"):
            hallazgos.append({"tipo": "no_encontrado", "clase": clase, "url": url,
                              "detalle": "el archivo ya no está en esa ruta"})
            obs[clase] = {"error": err}
            continue
        f = firma(h)
        antes = (previo or {}).get(clase) or {}
        obs[clase] = {"firma": f}
        cambio_cabecera = bool(f and antes.get("firma") and f != antes["firma"])
        sin_senal = f is None or err == "head_no_permitido"
        if forzar or sin_senal or cambio_cabecera:
            _, cuerpo, err2 = pedir(url, "GET")
            if err2 or cuerpo is None:
                hallazgos.append({"tipo": "inaccesible", "clase": clase,
                                  "url": url, "detalle": err2 or "sin cuerpo"})
                obs[clase]["error"] = err2
                continue
            sha = hashlib.sha256(cuerpo).hexdigest()
            obs[clase]["sha256"] = sha
            obs[clase]["bytes"] = len(cuerpo)
            declarado = item.get("sha_" + clase)
            if declarado and sha != declarado:
                hallazgos.append({
                    "tipo": "modificado", "clase": clase, "url": url,
                    "detalle": "sha publicado %s… != archivado %s…"
                               % (sha[:12], declarado[:12])})
        time.sleep(PAUSA)
    return obs, hallazgos


def revisar_catalogo(entidad, previo):
    """Detecta movimiento en la página de catálogo (posibles altas o bajas)."""
    url = CATALOGOS.get(entidad)
    if not url:
        return None, []
    _, cuerpo, err = pedir(url, "GET")
    if err or cuerpo is None:
        return ({"error": err},
                [{"tipo": "catalogo_inaccesible", "entidad": entidad,
                  "url": url, "detalle": err or "sin cuerpo"}])
    sha = hashlib.sha256(cuerpo).hexdigest()
    obs = {"sha256": sha, "bytes": len(cuerpo)}
    if previo and previo.get("sha256") and previo["sha256"] != sha:
        return obs, [{"tipo": "catalogo_movido", "entidad": entidad, "url": url,
                      "detalle": "la página de catálogo cambió: revisar altas o bajas"}]
    return obs, []


ETIQUETAS = {
    "modificado": "Archivo modificado en el sitio del Congreso",
    "no_encontrado": "El archivo ya no está en su ruta (404)",
    "inaccesible": "No se pudo leer el archivo",
    "catalogo_movido": "La página de catálogo cambió",
    "catalogo_inaccesible": "No se pudo leer la página de catálogo",
}


def escribir_reporte(hallazgos, revisados, segundos, notas):
    os.makedirs(VIG, exist_ok=True)
    ahora = datetime.now(timezone.utc)
    L = ["# Vigilancia de reformas", "",
         "Corrida: %s · %d ordenamientos revisados · %ds"
         % (ahora.strftime("%Y-%m-%d %H:%M UTC"), revisados, segundos), ""]
    if not hallazgos:
        L.append("**Sin cambios.** Ningún archivo del acervo se movió en el sitio "
                 "de los Congresos desde la última revisión.")
    else:
        por_tipo = {}
        for x in hallazgos:
            por_tipo.setdefault(x["tipo"], []).append(x)
        n = len(por_tipo.get("modificado", []))
        if n:
            L.append("**%d archivo(s) cambiaron.** Requiere conversión y "
                     "validación: pasa este reporte al pipeline de "
                     "mantenimiento." % n)
        else:
            L.append("**Atención requerida**, pero ningún cambio de contenido "
                     "confirmado.")
        L.append("")
        for tipo in ("modificado", "no_encontrado", "catalogo_movido",
                     "inaccesible", "catalogo_inaccesible"):
            if tipo not in por_tipo:
                continue
            L += ["## " + ETIQUETAS[tipo], "",
                  "| Entidad | ID | Ordenamiento | Archivo | Detalle |",
                  "|---|---:|---|---|---|"]
            for x in por_tipo[tipo]:
                L.append("| %s | %s | %s | %s | %s |" % (
                    x.get("entidad", "—"), x.get("id", "—"),
                    (x.get("nombre") or "—")[:60], x.get("clase", "—"),
                    x.get("detalle", "")))
            L.append("")
    if notas:
        L += ["## Notas de la corrida", ""] + ["- " + n for n in notas] + [""]
    L += ["---", "",
          "Esta revisión **detecta**, no convierte ni actualiza el acervo. Un "
          "cambio de archivo no siempre es una reforma: el Congreso puede "
          "regenerar un PDF sin modificar su contenido. La conversión, la "
          "validación y el commit se hacen aparte, con supervisión."]
    txt = "\n".join(L) + "\n"
    open(os.path.join(VIG, "reporte.md"), "w", encoding="utf-8").write(txt)
    return txt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entidad", help="Sinaloa o Nayarit; por omisión, ambas")
    ap.add_argument("--forzar-descarga", action="store_true",
                    help="descarga y coteja SHA-256 de todo")
    a = ap.parse_args()
    ents = [a.entidad] if a.entidad else list(ENTIDADES)

    os.makedirs(VIG, exist_ok=True)
    ruta = os.path.join(VIG, "estado.json")
    previo = {}
    if os.path.exists(ruta):
        try:
            previo = json.load(open(ruta, encoding="utf-8"))
        except Exception:
            previo = {}
    primera = not previo.get("ordenamientos")

    t0 = time.time()
    nuevo = {"actualizado": datetime.now(timezone.utc).isoformat(),
             "ordenamientos": {}, "catalogos": {}}
    hallazgos, notas, revisados = [], [], 0

    for ent in ents:
        inv = inventario(ent)
        if not inv:
            notas.append("%s: no se encontró el árbol de ordenamientos." % ent)
            continue
        obs_cat, hc = revisar_catalogo(ent, (previo.get("catalogos") or {}).get(ent))
        if obs_cat:
            nuevo["catalogos"][ent] = obs_cat
        if not primera:
            hallazgos += hc
        for item in inv:
            clave = "%s/%d" % (ent, item["id"])
            obs, hs = revisar(item, (previo.get("ordenamientos") or {}).get(clave),
                              a.forzar_descarga or primera)
            nuevo["ordenamientos"][clave] = obs
            revisados += 1
            for h in hs:
                h["entidad"] = ent
                h["id"] = item["id"]
                h["nombre"] = item["nombre"]
            if primera:
                hallazgos += [x for x in hs
                              if x["tipo"] in ("no_encontrado", "inaccesible")]
            else:
                hallazgos += hs

    if primera:
        notas.append("Primera corrida: se levantó la línea base. A partir de la "
                     "próxima se reportan los cambios.")

    json.dump(nuevo, open(ruta, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    txt = escribir_reporte(hallazgos, revisados, int(time.time() - t0), notas)
    print(txt)
    salida = os.environ.get("GITHUB_OUTPUT")
    if salida:
        with open(salida, "a") as f:
            f.write("hallazgos=%s\n" % ("si" if hallazgos else "no"))
            f.write("revisados=%d\n" % revisados)
    return 0


if __name__ == "__main__":
    sys.exit(main())
