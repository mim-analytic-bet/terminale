#!/usr/bin/env python3
"""Converte i file openfootball (champions-league) in un CSV storico: dati/coppe/storico_europa.csv
Colonne: data,comp,fase,casa,ospite,gc,go,neutro   (gc/go = punteggio dopo 90 minuti)
Uso: python3 scripts/coppe_storico.py <cartella_clone_openfootball>
Fonte: github.com/openfootball/champions-league (dominio pubblico)."""
import csv, os, re, sys, datetime as dt

MESI = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
COMP = {"cl.txt": "cl", "clq.txt": "clq", "el.txt": "el", "elq.txt": "elq", "conf.txt": "conf", "confq.txt": "confq"}
RIGA = re.compile(r"^\s+(?:(\d\d:\d\d)\s+)?(.+?)\s+v\s+(.+?)\s{2,}(\d+)-(\d+)(.*)$")
DATA = re.compile(r"^\s{2}(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+([A-Z][a-z]{2})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$")
PAESE = re.compile(r"\s*\([A-Z]{3}\)\s*$")


def pulisci(n): return PAESE.sub("", n).strip()


def leggi_file(path, comp, stagione):
    anno0 = int(stagione[:4]); out = []; fase = ""; cur = None; ultimo_mese = None
    for riga in open(path, encoding="utf-8"):
        riga = riga.rstrip("\r\n")
        if riga.startswith("▪"): fase = riga[1:].strip(); continue
        m = DATA.match(riga)
        if m:
            mese = MESI[m.group(1)]; giorno = int(m.group(2))
            anno = int(m.group(3)) if m.group(3) else (anno0 if mese >= 7 else anno0 + 1)  # stagione: lug-dic = anno di inizio, gen-giu = anno dopo
            cur = dt.date(anno, mese, giorno); continue
        m = RIGA.match(riga)
        if not (m and cur): continue
        casa, osp, a, b, resto = pulisci(m.group(2)), pulisci(m.group(3)), int(m.group(4)), int(m.group(5)), m.group(6)
        if "a.e.t." in resto:  # dopo i supplementari: il punteggio dei 90' e' il primo nella parentesi
            p = re.search(r"\((\d+)-(\d+),", resto)
            if not p: continue
            a, b = int(p.group(1)), int(p.group(2))
        neutro = 1 if re.search(r"Final$", fase) and "Semi" not in fase else 0
        out.append((cur.isoformat(), comp, fase, casa, osp, a, b, neutro))
    return out


def main(base, dest):
    righe = []
    for s in sorted(os.listdir(base)):
        if not re.match(r"\d{4}-\d{2}$", s): continue
        for f, comp in COMP.items():
            p = os.path.join(base, s, f)
            if os.path.exists(p): righe += leggi_file(p, comp, s)
    righe.sort()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["data", "comp", "fase", "casa", "ospite", "gc", "go", "neutro"]); w.writerows(righe)
    print(f"{len(righe)} partite scritte in {dest}")


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ofb"
    main(base, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dati", "coppe", "storico_europa.csv"))
