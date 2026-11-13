"""Estrae i 2 colori dominanti di ogni stemma (assets/loghi) e li salva in dati/colori_squadre.json.
Se Pillow non c'e' (o lo stemma non e' cambiato) usa la cache gia' salvata."""
import os, json, colorsys

def _hex(c): return "#%02x%02x%02x" % c

def dominanti(path):
    from PIL import Image
    im = Image.open(path).convert("RGBA"); im.thumbnail((96, 96))
    px = [p[:3] for p in im.getdata() if p[3] > 200]
    if not px: return None
    pal = Image.new("RGB", (len(px), 1)); pal.putdata(px)
    q = pal.quantize(colors=10, method=Image.Quantize.MEDIANCUT)
    cols = q.getpalette()[:30]; cnt = sorted(q.getcolors(), reverse=True)   # (n, indice)
    cand = []
    for n, i in cnt:
        c = tuple(cols[3*i:3*i+3]); h, s, v = colorsys.rgb_to_hsv(*(x/255 for x in c))
        cand.append((n, c, s, v))
    def tinta(c): return colorsys.rgb_to_hsv(*(x/255 for x in c))[0] * 360
    def dist_tinta(h1, h2):
        d = abs(h1 - h2) % 360; return min(d, 360 - d)
    vivi = [x for x in cand if x[2] >= 0.40 and x[3] >= 0.30]            # colori saturi e luminosi
    scelti = []
    if vivi:
        scelti.append(vivi[0][1])
        for _, c, s, v in vivi[1:]:
            if dist_tinta(tinta(c), tinta(scelti[0])) >= 40: scelti.append(c); break
    if len(scelti) < 2:                                                    # nessun secondo colore vivace: bianco (se presente) o nero
        bianchi = [x for x in cand if x[2] < 0.15 and x[3] > 0.85]
        scuri = [x for x in cand if x[3] < 0.22]
        extra = sorted(bianchi + scuri, key=lambda x: -x[0])
        if extra: scelti.append(extra[0][1])
    if not scelti:
        grigi = sorted(cand, key=lambda x: -x[0]); scelti = [grigi[0][1]] if grigi else []
    if not scelti: return None
    if len(scelti) == 1: scelti.append(tuple(min(255, int(x*0.55)) for x in scelti[0]))
    return [_hex(c) for c in scelti]

def aggiorna(loghi, base, cache_path):
    cache = json.load(open(cache_path, encoding="utf-8")) if os.path.exists(cache_path) else {}
    mancanti = []
    for nome, rel in loghi.items():
        p = os.path.join(base, rel.lstrip("./"))
        if not os.path.exists(p): mancanti.append(nome); continue
        firma = f"v2-{os.path.getsize(p)}"
        if cache.get(nome, {}).get("firma") == firma: continue
        try: c = dominanti(p)
        except Exception: c = None
        if c: cache[nome] = {"colori": c, "firma": firma}
        elif nome not in cache: mancanti.append(nome)
    json.dump(cache, open(cache_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return {k: v["colori"] for k, v in cache.items()}, mancanti
