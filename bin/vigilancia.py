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

Cubre los tres acervos: Sinaloa, Nayarit y Federal (Cámara de Diputados).

Uso:
    python3 bin/vigilancia.py [--entidad Federal] [--forzar-descarga]
"""
import argparse, hashlib, json, os, re, sys, time
import urllib.request, urllib.error, urllib.parse
from datetime import datetime, timezone

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
VIG = os.path.join(RAIZ, "vigilancia")
ENTIDADES = ("Sinaloa", "Nayarit", "Federal")
UA = ("biblioteca-legislativa/1.0 (vigilancia de reformas; "
      "+github.com/enriquedilo/biblioteca-legislativa)")
TIMEOUT = 30
REINTENTOS = 2
PAUSA = 0.4  # cortesía con los servidores del Congreso
# Cuando el servidor no da cabeceras utiles, se pide solo el principio del
# archivo en vez de bajarlo entero: basta para notar que cambio y no descarga
# cientos de MB cada semana (la tarifa de la LIGIE sola pesa ~100 MB).
PREFIJO = 262144           # 256 KB
LIMITE_DESCARGA = 12 << 20  # 12 MB: por encima se usa el prefijo salvo --forzar

# Una entidad puede publicar su catálogo en más de una página. La Cámara
# separa leyes y reglamentos: vigilar solo la portada dejaba 131 reglamentos
# sin cobertura y hundía el porcentaje por debajo del umbral, de modo que el
# control de enlaces huérfanos se abstenía para todo el acervo federal.
CATALOGOS = {
    # La Gaceta es una aplicación de una sola página: su raíz no responde a una
    # petición simple (URLError en cada corrida). Se vigila la página del
    # Congreso que publica el listado, que sí es HTML servido.
    "Sinaloa": ("https://www.congresosinaloa.gob.mx/leyes-estatales/",),
    "Nayarit": ("https://congresonayarit.gob.mx/legislacion-estatal/",),
    "Federal": ("https://www.diputados.gob.mx/LeyesBiblio/index.htm",
                "https://www.diputados.gob.mx/LeyesBiblio/regla.htm"),
}
RE_ENLACE = re.compile(rb'href\s*=\s*["\']([^"\']+\.(?:pdf|docx?|rtf))["\']',
                       re.IGNORECASE)


def pedir(url, metodo="HEAD", prefijo=None):
    """Devuelve (cabeceras, cuerpo_o_None, error_o_None).

    Con `prefijo` pide solo los primeros N bytes (Range). Si el servidor no
    respeta Range devolvera el archivo completo: se corta al leerlo."""
    for intento in range(REINTENTOS + 1):
        try:
            cab = {"User-Agent": UA}
            if prefijo:
                cab["Range"] = "bytes=0-%d" % (prefijo - 1)
            req = urllib.request.Request(url, method=metodo, headers=cab)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                h = {k.lower(): v for k, v in r.headers.items()}
                cuerpo = None
                if metodo == "GET":
                    cuerpo = r.read(prefijo) if prefijo else r.read()
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
            "vigencia_anual": bool(d.get("vigencia_anual")),
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
        # Si la biblioteca nunca archivó ese formato, su URL es informativa:
        # el archivo no existe en el sitio y un 404 no es novedad. Vigilar solo
        # lo que efectivamente se descargó evita un aviso repetido cada semana.
        if not item.get("sha_" + clase):
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
            # Un archivo grande no se baja entero solo para saber si cambio:
            # se compara su principio contra el de la corrida anterior. Con
            # --forzar-descarga si se baja completo y se coteja el SHA-256
            # declarado en metadata.json.
            tam = (f or {}).get("content_length") or 0
            parcial = (not forzar) and (sin_senal or tam > LIMITE_DESCARGA)
            _, cuerpo, err2 = pedir(url, "GET", PREFIJO if parcial else None)
            if err2 or cuerpo is None:
                hallazgos.append({"tipo": "inaccesible", "clase": clase,
                                  "url": url, "detalle": err2 or "sin cuerpo"})
                obs[clase]["error"] = err2
                continue
            sha = hashlib.sha256(cuerpo).hexdigest()
            if parcial:
                obs[clase]["sha256_prefijo"] = sha
                obs[clase]["bytes_prefijo"] = len(cuerpo)
                ant = antes.get("sha256_prefijo")
                if ant and ant != sha:
                    hallazgos.append({
                        "tipo": "posible_modificacion", "clase": clase,
                        "url": url,
                        "detalle": "cambio el inicio del archivo (primeros "
                                   "%d KB); el servidor no da cabeceras "
                                   "utiles" % (len(cuerpo) // 1024)})
            else:
                obs[clase]["sha256"] = sha
                obs[clase]["bytes"] = len(cuerpo)
                declarado = item.get("sha_" + clase)
                if declarado and sha != declarado:
                    hallazgos.append({
                        "tipo": "modificado", "clase": clase, "url": url,
                        "detalle": "sha publicado %s… != archivado %s…"
                                   % (sha[:12], declarado[:12])})
        # Una discrepancia confirmada sigue vigente hasta que el acervo se
        # actualice. Sin esto, la alerta dura una sola corrida: a la siguiente
        # las cabeceras ya coinciden con lo observado, no se vuelve a
        # descargar y el pendiente desaparece del reporte con el texto viejo
        # todavía en la biblioteca.
        declarado = item.get("sha_" + clase)
        visto = obs[clase].get("sha256") or antes.get("sha256")
        ya = any(x.get("tipo") == "modificado" and x.get("clase") == clase
                 for x in hallazgos)
        if declarado and visto and visto != declarado and not ya:
            obs[clase].setdefault("sha256", visto)
            hallazgos.append({
                "tipo": "pendiente_de_actualizar", "clase": clase, "url": url,
                "detalle": "el archivo publicado sigue difiriendo del "
                           "archivado (%s… != %s…)" % (visto[:12],
                                                       declarado[:12])})
        time.sleep(PAUSA)
    return obs, hallazgos


def prefijos_de(inventario_ent):
    """(host, primer segmento) de las URL que el acervo ya tiene para esa
    entidad. Con eso se distingue un enlace del catálogo de uno del menú del
    sitio: en Sinaloa, el único PDF del HTML es «Estadística Parlamentaria»,
    que cambia de número cada mes y no es un ordenamiento."""
    pref = set()
    for it in inventario_ent:
        for u in (it.get("url_pdf"), it.get("url_word")):
            if not u:
                continue
            try:
                p = urllib.parse.urlparse(u)
            except ValueError:
                continue
            seg = [x for x in p.path.split("/") if x]
            if p.netloc and seg:
                pref.add((p.netloc.lower(), seg[0].lower()))
    return pref


def del_catalogo(enlaces, url_catalogo, prefijos):
    """Se queda con los enlaces que viven donde viven los ordenamientos."""
    if not prefijos:
        return enlaces
    dentro = []
    for e in enlaces:
        try:
            a = urllib.parse.urlparse(urllib.parse.urljoin(url_catalogo, e))
        except ValueError:
            continue
        seg = [x for x in a.path.split("/") if x]
        if seg and (a.netloc.lower(), seg[0].lower()) in prefijos:
            dentro.append(e)
    return dentro


def revisar_catalogo(entidad, previo, inventario_ent=()):
    """Detecta movimiento en la página de catálogo (posibles altas o bajas)."""
    urls = CATALOGOS.get(entidad)
    if not urls:
        return None, []
    if isinstance(urls, str):
        urls = (urls,)
    url = urls[0]
    prefijos = prefijos_de(inventario_ent)
    enlaces, crudos, fallos = [], 0, []
    for u in urls:
        _, cuerpo, err = pedir(u, "GET")
        if err or cuerpo is None:
            fallos.append({"tipo": "catalogo_inaccesible", "entidad": entidad,
                           "url": u, "detalle": err or "sin cuerpo"})
            continue
        # Comparar la lista de documentos enlazados, no el HTML entero: una
        # fecha o un banner en la portada no son un alta ni una baja.
        brutos = sorted(set(m.group(1).decode("utf-8", "replace")
                            for m in RE_ENLACE.finditer(cuerpo)))
        crudos += len(brutos)
        enlaces += [urllib.parse.urljoin(u, e)
                    for e in del_catalogo(brutos, u, prefijos)]
    if fallos and not enlaces:
        return {"error": fallos[0]["detalle"]}, fallos
    enlaces = sorted(set(enlaces))
    if not enlaces:
        # El catálogo de Sinaloa se arma con JavaScript desde otro host: su
        # lista nunca está en el HTML servido. Se deja constancia y no se
        # reporta nada, en vez de vigilar lo primero que se parezca a un
        # documento. Las altas de Sinaloa se detectan por otra vía.
        return ({"lista_no_observable": True, "enlaces_crudos": crudos}, fallos)
    absolutos = enlaces
    # La huella se calcula sobre la forma normalizada: que el sitio cambie una
    # ruta de mayúsculas a minúsculas no es un alta ni una baja.
    sha = hashlib.sha256("\n".join(_clave(e) for e in enlaces)
                         .encode("utf-8")).hexdigest()
    # Se guarda la lista, no solo su huella: decir «algo cambió» sin decir qué
    # dejó pasar dos meses una reforma de la Constitución de Nayarit.
    obs = {"sha256_enlaces": sha, "enlaces": len(enlaces), "lista": absolutos}
    hallazgos = list(fallos)
    antes = set((previo or {}).get("lista") or [])
    ant_sha = (previo or {}).get("sha256_enlaces")
    if antes:
        ahora_k = {_clave(e): e for e in absolutos}
        antes_k = {_clave(e): e for e in antes}
        altas = sorted(ahora_k[k] for k in set(ahora_k) - set(antes_k))
        bajas = sorted(antes_k[k] for k in set(antes_k) - set(ahora_k))
        if altas or bajas:
            hallazgos.append({
                "tipo": "catalogo_movido", "entidad": entidad, "url": url,
                "detalle": _detalle_diferencia(altas, bajas)})
    elif ant_sha and ant_sha != sha:
        # Primera corrida tras el cambio: todavía no hay lista guardada.
        hallazgos.append({"tipo": "catalogo_movido", "entidad": entidad,
                          "url": url,
                          "detalle": "la lista del catálogo cambió (%d enlaces); "
                                     "desde la próxima corrida se dirá cuáles"
                                     % len(enlaces)})
    hallazgos += _huerfanos(entidad, inventario_ent, set(absolutos), obs)
    return obs, hallazgos


RE_ANIO = re.compile(r"(?<!\d)(20\d{2})(?!\d)")


def urls_del_siguiente_ejercicio(url):
    """Candidatas para el ejercicio siguiente, sustituyendo el año en la URL.

    Las leyes de ingresos y los presupuestos no se reforman: se sustituyen
    cada año por un archivo nuevo con otro nombre. Vigilar el archivo de 2026
    no entera jamás de que se publicó el de 2027, porque el de 2026 sigue
    donde estaba y sin cambios. Por eso se prueba la misma ruta con el año
    siguiente."""
    anios = RE_ANIO.findall(url or "")
    if not anios:
        return []
    actual = max(int(a) for a in anios)
    sig = str(actual + 1)
    cands = [RE_ANIO.sub(lambda m: sig if m.group(1) == str(actual) else m.group(1), url)]
    # Algunos sitios versionan la carpeta y no el archivo, o al revés: se
    # prueba también sustituyendo solo la última aparición.
    i = url.rfind(str(actual))
    if i >= 0:
        otra = url[:i] + sig + url[i + 4:]
        if otra not in cands:
            cands.append(otra)
    return [c for c in cands if c != url]


def revisar_ejercicio_anual(item):
    """¿Ya se publicó el documento del ejercicio siguiente?"""
    if not item.get("vigencia_anual") or not item.get("url_pdf"):
        return []
    for u in urls_del_siguiente_ejercicio(item["url_pdf"]):
        cab, _, err = pedir(u, "HEAD")
        if err or not cab:
            continue
        return [{"tipo": "ejercicio_siguiente_publicado", "entidad": item["entidad"],
                 "id": item["id"], "nombre": item["nombre"], "url": u,
                 "detalle": "el sitio ya publica el documento del ejercicio "
                            "siguiente en %s; el archivado no cambia porque "
                            "se sustituye, no se reforma" % u}]
    return []


def _clave(u):
    """Forma comparable de una URL. Las rutas del Congreso de Nayarit traen
    tramos en mayúsculas -QUE_HACEMOS/LEGISLACION_ESTATAL- y los enlaces del
    HTML no siempre conservan la caja. Comparar en crudo hacía que ninguna URL
    archivada coincidiera con el catálogo: la cobertura salía 0% y el control
    de huérfanos se abstenía siempre, sin reportarlo. Nunca llegó a correr."""
    return (u or "").strip().lower()


def _nombre_archivo(u):
    return urllib.parse.unquote(urllib.parse.urlparse(u).path.rsplit("/", 1)[-1])


def _detalle_diferencia(altas, bajas, tope=12):
    partes = []
    for et, xs in (("alta", altas), ("baja", bajas)):
        if not xs:
            continue
        nombres = [_nombre_archivo(x) for x in xs[:tope]]
        extra = "" if len(xs) <= tope else " y %d más" % (len(xs) - tope)
        partes.append("%s (%d): %s%s" % (et, len(xs), ", ".join(nombres), extra))
    return "el catálogo cambió — " + "; ".join(partes)


def _huerfanos(entidad, inventario_ent, enlaces, obs):
    """Ordenamientos cuya URL archivada ya no aparece en el catálogo.

    Es el caso que pasó inadvertido dos meses: el Congreso no sobreescribió el
    archivo, subió otro con el nombre terminado en «-1» y cambió el enlace. La
    URL vieja sigue respondiendo y con el mismo contenido, así que la revisión
    por SHA no ve nada; lo que cambió fue a dónde apunta el catálogo.

    Solo se reporta si el catálogo cubre casi todo el acervo. En la Cámara, la
    portada no enlaza los reglamentos, y sin esta cautela saldrían ciento y
    pico de falsos positivos."""
    con_url = [it for it in inventario_ent if it.get("url_pdf")]
    if not con_url:
        return []
    claves = {_clave(e) for e in enlaces}
    dentro = [it for it in con_url if _clave(it["url_pdf"]) in claves]
    cobertura = len(dentro) / len(con_url)
    obs["cobertura"] = round(cobertura, 3)
    if cobertura < 0.9:
        obs["huerfanos_no_evaluables"] = True
        return []
    fuera = [it for it in con_url if _clave(it["url_pdf"]) not in claves]
    return [{"tipo": "enlace_fuera_del_catalogo", "entidad": entidad,
             "id": it["id"], "nombre": it["nombre"], "url": it["url_pdf"],
             "detalle": "el catálogo ya no enlaza este archivo: el sitio "
                        "publicó otro y la URL archivada quedó congelada"}
            for it in fuera]


ETIQUETAS = {
    "modificado": "Archivo modificado en el sitio oficial",
    "posible_modificacion": "Posible modificación (cambió el inicio del archivo)",
    "pendiente_de_actualizar": "Cambio ya detectado, acervo aún sin actualizar",
    "no_encontrado": "El archivo ya no está en su ruta (404)",
    "inaccesible": "No se pudo leer el archivo",
    "catalogo_movido": "La página de catálogo cambió",
    "ejercicio_siguiente_publicado": "Se publicó el documento del ejercicio siguiente",
    "enlace_fuera_del_catalogo": "El catálogo dejó de enlazar el archivo archivado",
    "catalogo_inaccesible": "No se pudo leer la página de catálogo",
}


def escribir_reporte(hallazgos, revisados, segundos, notas):
    os.makedirs(VIG, exist_ok=True)
    ahora = datetime.now(timezone.utc)
    L = ["# Vigilancia de reformas", "",
         "Corrida: %s · %d ordenamientos revisados · %ds"
         % (ahora.strftime("%Y-%m-%d %H:%M UTC"), revisados, segundos), ""]
    if not hallazgos:
        L.append("**Sin cambios.** Ningún archivo del acervo se movió en los "
                 "sitios de los Congresos ni de la Cámara de Diputados desde la "
                 "última revisión.")
    else:
        por_tipo = {}
        for x in hallazgos:
            por_tipo.setdefault(x["tipo"], []).append(x)
        n = len(por_tipo.get("modificado", [])) + len(
            por_tipo.get("pendiente_de_actualizar", []))
        if n:
            L.append("**%d archivo(s) cambiaron.** Requiere conversión y "
                     "validación: pasa este reporte al pipeline de "
                     "mantenimiento." % n)
        else:
            L.append("**Atención requerida**, pero ningún cambio de contenido "
                     "confirmado.")
        L.append("")
        # El orden es el de lectura; lo que no esté previsto va al final en
        # vez de desaparecer. Una categoría nueva que no se imprime equivale a
        # no detectarla: `enlace_fuera_del_catalogo` se perdió así.
        orden = ("modificado", "pendiente_de_actualizar",
                 "ejercicio_siguiente_publicado",
                 "posible_modificacion", "enlace_fuera_del_catalogo",
                 "no_encontrado", "catalogo_movido", "inaccesible",
                 "catalogo_inaccesible")
        for tipo in orden + tuple(sorted(set(por_tipo) - set(orden))):
            if tipo not in por_tipo:
                continue
            L += ["## " + ETIQUETAS.get(tipo, tipo), "",
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
    ap.add_argument("--entidad",
                    help="Sinaloa, Nayarit o Federal; por omisión, las tres")
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
        obs_cat, hc = revisar_catalogo(
            ent, (previo.get("catalogos") or {}).get(ent), inv)
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
            if not primera:
                hs += revisar_ejercicio_anual(item)
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
