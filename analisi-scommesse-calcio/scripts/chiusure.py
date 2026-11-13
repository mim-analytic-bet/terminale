#!/usr/bin/env python3
"""Quote di chiusura nello storico, per misurare il CLV.

Uso:
  chiusure.py storico.csv --da-fare [--oggi AAAA-MM-GG]
      elenca le righe di oggi e domani senza quota di chiusura (controllo pre-partita)
  chiusure.py storico.csv --imposta "12=1,88; 13=3,60"
      scrive la quota di chiusura Eurobet nelle righe indicate (numero di riga del file)
  chiusure.py storico.csv --da-csv risultati.csv
      riempie le chiusure ancora vuote di 1X2 e Over/Under 2,5 con la quota media di
      chiusura del mercato presa dal CSV di football-data.co.uk (riferimento, non Eurobet)

La colonna fonte_chiusura dice da dove viene ogni quota: "Eurobet" oppure
"media mercato". Il file viene riscritto con lo stesso separatore.
"""
import csv
import datetime as dt
import sys


def num(s):
    s = (s or "").strip().replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def it(x):
    return f"{x:.2f}".replace(".", ",")


def data(s):
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return dt.datetime.strptime(s.strip(), f).date()
        except ValueError:
            pass
    return None


def carica(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        testo = f.read()
    sep = csv.Sniffer().sniff(testo.splitlines()[0], delimiters=";,\t").delimiter
    righe = list(csv.DictReader(testo.splitlines(), delimiter=sep))
    campi = list(righe[0].keys()) if righe else testo.splitlines()[0].split(sep)
    for c in ("quota_chiusura", "fonte_chiusura"):
        if c not in campi:
            campi.append(c)
    for r in righe:
        for c in ("quota_chiusura", "fonte_chiusura"):
            r.setdefault(c, "")
            r[c] = r[c] or ""
    return righe, campi, sep


def salva(path, righe, campi, sep):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campi, delimiter=sep, extrasaction="ignore")
        w.writeheader()
        w.writerows(righe)


COLONNE_CSV = {"1": "AvgCH", "x": "AvgCD", "2": "AvgCA", "over 2,5": "AvgC>2.5", "under 2,5": "AvgC<2.5"}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    path = argv[0]
    righe, campi, sep = carica(path)
    oggi = dt.date.fromisoformat(argv[argv.index("--oggi") + 1]) if "--oggi" in argv else dt.date.today()

    if "--da-fare" in argv:
        domani = oggi + dt.timedelta(days=1)
        da_fare = [(i, r) for i, r in enumerate(righe, 2)
                   if data(r.get("data", "")) in (oggi, domani) and not r["quota_chiusura"].strip()]
        if not da_fare:
            print("Nessuna quota di chiusura da annotare per oggi e domani.")
            return 0
        print("Quote di chiusura da annotare (Eurobet, 10-15 minuti prima del calcio d'inizio):")
        for i, r in da_fare:
            giocata = " · GIOCATA" if num(r.get("puntata")) else ""
            print(f"riga {i}: {r.get('data')} {r.get('partita')} · {r.get('esito')} · presa a {r.get('quota')}{giocata}")
        print('Poi: chiusure.py storico.csv --imposta "riga=quota; riga=quota"')
        return 0

    if "--imposta" in argv:
        n = 0
        for coppia in argv[argv.index("--imposta") + 1].split(";"):
            if not coppia.strip():
                continue
            riga, q = coppia.split("=")
            idx = int(riga) - 2
            if not 0 <= idx < len(righe):
                raise SystemExit(f"Riga {riga} inesistente")
            valore = num(q)
            if not valore or valore <= 1:
                raise SystemExit(f"Quota non valida: {q}")
            righe[idx]["quota_chiusura"] = it(valore)
            righe[idx]["fonte_chiusura"] = "Eurobet"
            n += 1
        salva(path, righe, campi, sep)
        print(f"Aggiornate {n} righe.")
        return 0

    if "--da-csv" in argv:
        with open(argv[argv.index("--da-csv") + 1], encoding="utf-8-sig") as f:
            partite = list(csv.DictReader(f))
        indice = {}
        for p in partite:
            d = data(p.get("Date", ""))
            indice[(p.get("HomeTeam", "").lower(), p.get("AwayTeam", "").lower())] = (d, p)
        n, saltate = 0, []
        for i, r in enumerate(righe, 2):
            if r["quota_chiusura"].strip():
                continue
            col = COLONNE_CSV.get(r.get("esito", "").strip().lower())
            if not col:
                continue
            nomi = [x.strip().lower() for x in r.get("partita", "").split(" - ")]
            trovata = indice.get(tuple(nomi)) if len(nomi) == 2 else None
            d_r = data(r.get("data", ""))
            if not trovata or (d_r and trovata[0] and abs((trovata[0] - d_r).days) > 2):
                saltate.append(f"riga {i} ({r.get('partita')})")
                continue
            q = num(trovata[1].get(col))
            if q:
                r["quota_chiusura"] = it(q)
                r["fonte_chiusura"] = "media mercato"
                n += 1
        salva(path, righe, campi, sep)
        print(f"Chiusure aggiunte dalla media di mercato: {n}.")
        if saltate:
            print("Partite non trovate nel CSV (nomi diversi o non ancora giocate): " + ", ".join(saltate))
        return 0

    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
