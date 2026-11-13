#!/usr/bin/env python3
"""Scarica gli stemmi UFFICIALI delle squadre di coppa che hanno un URL nei dati di football-data.org (dati/coppe/CL_live.json)
in assets/loghi/coppe_<slug>.<ext> e scrive dati/stemmi_coppe.json: {nome: {"file": "./assets/loghi/...", "colori": [..]|null}}.
Non blocca mai l'aggiornamento: dove lo scarico fallisce il generatore usa un distintivo provvisorio."""
import json, os, re, sys, unicodedata, urllib.request, collections
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGHI = os.path.join(BASE, "assets", "loghi"); OUT = os.path.join(BASE, "dati", "stemmi_coppe.json")


def slug(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", n).strip("_") or "squadra"


def colori_svg(testo):
    cnt = collections.Counter(c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", testo))
    def ok(c):
        r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5)); mx, mn = max(r, g, b), min(r, g, b)
        return mx > 70 and (mx - mn) > 40  # saturo e non troppo scuro
    vivi = [c for c, _ in cnt.most_common() if ok(c)]
    return vivi[:2] if len(vivi) >= 2 else None


def main():
    try: esistenti = json.load(open(OUT, encoding="utf-8"))
    except Exception: esistenti = {}
    squadre = {}
    d = os.path.join(BASE, "dati", "coppe", "CL_live.json")
    if os.path.exists(d):
        for m in json.load(open(d, encoding="utf-8")).get("matches", []):
            for k in ("homeTeam", "awayTeam"):
                t = m.get(k) or {}
                if t.get("crest") and t.get("name"): squadre[t["name"]] = t
    os.makedirs(LOGHI, exist_ok=True); nuovi = fall = 0
    for nome, t in squadre.items():
        chiavi = {nome, t.get("shortName") or nome}
        if all(k in esistenti and os.path.exists(os.path.join(BASE, esistenti[k]["file"].lstrip("./"))) for k in chiavi): continue
        ext = ".svg" if t["crest"].lower().split("?")[0].endswith(".svg") else ".png"
        rel = f"./assets/loghi/coppe_{slug(t.get('shortName') or nome)}{ext}"; dest = os.path.join(BASE, rel.lstrip("./"))
        try:
            req = urllib.request.Request(t["crest"], headers={"User-Agent": "Mozilla/5.0 terminale"})
            with urllib.request.urlopen(req, timeout=30) as r: dati = r.read()
            if len(dati) < 200: raise ValueError("file troppo piccolo")
            col = None
            if ext == ".png":
                try:
                    from PIL import Image; import io
                    Image.open(io.BytesIO(dati)).verify()
                except ImportError:
                    if not dati.startswith(b'\x89PNG\r\n\x1a\n'):
                        raise ValueError("dati non validi come PNG")
            else: col = colori_svg(dati.decode("utf-8", "ignore"))
            open(dest, "wb").write(dati)
            for k in chiavi: esistenti[k] = {"file": rel, "colori": col}
            nuovi += 1
        except Exception as e:
            fall += 1; print(f"AVVISO stemmi: {nome}: {e}")
    json.dump(esistenti, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"stemmi: {nuovi} scaricati, {fall} falliti, {len(esistenti)} in archivio")


try: main()
except Exception as e: print("AVVISO stemmi: errore generale:", e)
sys.exit(0)
