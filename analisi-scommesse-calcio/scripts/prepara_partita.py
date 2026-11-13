#!/usr/bin/env python3
"""Costruisce il file di input di modello.py da un CSV di risultati nel formato
football-data.co.uk (colonne Date, HomeTeam, AwayTeam, FTHG, FTAG, HTHG, HTAG e,
se ci sono, HxG, AxG).

Uso:
  prepara_partita.py risultati.csv "Napoli" "Torino" [opzioni] > partita.json

Opzioni:
  --prima-di AAAA-MM-GG     usa solo le partite giocate prima di questa data
  --quote "1=1,60;X=3,90;2=5,50;Over 2,5=1,85;Under 2,5=1,90"
  --q "1.60 3.90 5.50 | 1.85 1.90 | 1.95 1.80"
                            formato rapido: 1 X 2 | Over Under 2,5 | Gol No Gol
                            (blocchi facoltativi da destra; virgola o punto decimale;
                            si può aggiungere un quarto blocco "| 1X 12 X2")
  --tipo-quota Eurobet      (default Eurobet; "indicativa" se non sono quote reali)
  --rif "1.62 3.80 5.40 | 1.90 1.90"
                            quote di riferimento del mercato (consenso), formato rapido
  --fonte-rif "Betfair Exchange"
  --rif-da fixtures.csv     prende il riferimento dal file delle prossime partite di
                            football-data.co.uk: Betfair Exchange se c'è, altrimenti
                            la media dei bookmaker; aggiunge anche l'arbitro se presente
  --assenze-ok              le assenze sono verificate entro 48 ore
  --correzione casa:ASSENZA_BOMBER   ripetibile; codici in modello.py
  --partita "Napoli - Torino"

I nomi delle squadre devono essere scritti come nel CSV.
"""
import csv
import datetime as dt
import json
import sys


def leggi(path):
    with open(path, encoding="utf-8-sig") as f:
        righe = list(csv.DictReader(f))
    out = []
    for r in righe:
        try:
            d = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
        except ValueError:
            d = dt.datetime.strptime(r["Date"], "%d/%m/%y").date()
        if not r.get("FTHG"):
            continue

        def f(k):
            v = r.get(k, "")
            try:
                return float(v)
            except ValueError:
                return None
        out.append({"data": d, "casa": r["HomeTeam"], "ospite": r["AwayTeam"],
                    "gc": int(r["FTHG"]), "go": int(r["FTAG"]),
                    "gc1": int(r["HTHG"]) if r.get("HTHG") else None, "go1": int(r["HTAG"]) if r.get("HTAG") else None,
                    "xgc": f("HxG"), "xgo": f("AxG"), "riga": r})
    return out


def statistiche(partite, squadra, sede, mc, mt):
    """sede: 'casa' o 'trasferta'. Restituisce i dati per sede più il blocco 'totale'."""
    sede_p = [p for p in partite if (p["casa"] if sede == "casa" else p["ospite"]) == squadra]
    tutte = [p for p in partite if squadra in (p["casa"], p["ospite"])]

    def gf(p):
        return p["gc"] if p["casa"] == squadra else p["go"]

    def ga(p):
        return p["go"] if p["casa"] == squadra else p["gc"]

    def xf(p):
        return p["xgc"] if p["casa"] == squadra else p["xgo"]

    def xa(p):
        return p["xgo"] if p["casa"] == squadra else p["xgc"]

    def somma_x(ps, fn):
        vals = [fn(p) for p in ps]
        return round(sum(vals), 2) if ps and all(v is not None for v in vals) else None

    gol_1t = sum((p["gc1"] if p["casa"] == squadra else p["go1"]) or 0 for p in tutte if p["gc1"] is not None)
    gol_tot = sum(gf(p) for p in tutte if p["gc1"] is not None)
    blocco = {
        "partite": len(sede_p),
        "gol_fatti": sum(gf(p) for p in sede_p), "gol_subiti": sum(ga(p) for p in sede_p),
        "xg": somma_x(sede_p, xf), "xga": somma_x(sede_p, xa),
        "quota_gol_1t": round(gol_1t / gol_tot, 3) if gol_tot >= 8 else None,
        "totale": {
            "partite": len(tutte),
            "gol_fatti": sum(gf(p) for p in tutte), "gol_subiti": sum(ga(p) for p in tutte),
            "xg": somma_x(tutte, xf), "xga": somma_x(tutte, xa),
            "gol_fatti_attesi": round(sum(mc if p["casa"] == squadra else mt for p in tutte), 3),
            "gol_subiti_attesi": round(sum(mt if p["casa"] == squadra else mc for p in tutte), 3),
        },
    }
    return blocco


def costruisci(partite, casa, ospite, prima_di=None):
    if prima_di:
        partite = [p for p in partite if p["data"] < prima_di]
    if not partite:
        raise SystemExit("Nessuna partita nel CSV prima della data indicata.")
    squadre = {p["casa"] for p in partite} | {p["ospite"] for p in partite}
    for s in (casa, ospite):
        if s not in squadre:
            raise SystemExit(f"Squadra '{s}' non trovata. Nomi nel CSV: {', '.join(sorted(squadre))}")
    mc = sum(p["gc"] for p in partite) / len(partite)
    mt = sum(p["go"] for p in partite) / len(partite)
    return {
        "partita": f"{casa} - {ospite}",
        "lega": {"media_gol_casa": round(mc, 3), "media_gol_trasferta": round(mt, 3), "partite_lega": len(partite)},
        "casa": statistiche(partite, casa, "casa", mc, mt),
        "trasferta": statistiche(partite, ospite, "trasferta", mc, mt),
    }


def quote_rapide(testo):
    """'1.60 3.90 5.50 | 1.85 1.90 | 1.95 1.80 | 1.15 1.25 2.35' -> dizionario quote."""
    nomi = [["1", "X", "2"], ["Over 2,5", "Under 2,5"], ["Gol", "No Gol"], ["1X", "12", "X2"]]
    out = {}
    blocchi = [b.split() for b in testo.split("|")]
    if len(blocchi) > len(nomi):
        raise SystemExit("Formato rapido: al massimo 4 blocchi (1X2 | Over/Under 2,5 | Gol/No Gol | doppia chance)")
    for i, b in enumerate(blocchi):
        if not b:
            continue
        if len(b) != len(nomi[i]):
            raise SystemExit(f"Blocco {i + 1} ('{' '.join(b)}'): servono {len(nomi[i])} quote ({', '.join(nomi[i])})")
        for n, v in zip(nomi[i], b):
            q = float(v.replace(",", "."))
            if q <= 1.0:
                raise SystemExit(f"Quota non valida per {n}: {v}")
            out[n] = q
    return out


def riferimento_da_fixtures(path, casa, ospite):
    with open(path, encoding="utf-8-sig") as f:
        righe = [r for r in csv.DictReader(f) if r.get("HomeTeam") == casa and r.get("AwayTeam") == ospite]
    if not righe:
        raise SystemExit(f"{casa} - {ospite} non trovata nel file delle prossime partite (nomi come nel CSV).")
    r = righe[-1]

    def q(k):
        try:
            v = float(r.get(k, ""))
            return v if v > 1 else None
        except ValueError:
            return None
    for pref, fonte in (("BFE", "Betfair Exchange"), ("PS", "Pinnacle"), ("Avg", "media dei bookmaker")):
        trio = [q(pref + x) for x in ("H", "D", "A")]
        if all(trio):
            out = dict(zip(("1", "X", "2"), trio))
            ou = [q(pref + ">2.5"), q(pref + "<2.5")]
            if all(ou):
                out["Over 2,5"], out["Under 2,5"] = ou
            return out, f"{fonte} (football-data.co.uk, {r.get('Date', '')})", r.get("Referee") or None
    raise SystemExit("Nessuna quota di riferimento completa per questa partita nel file.")


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    path, casa, ospite = argv[0], argv[1], argv[2]
    opz = argv[3:]

    def val(nome):
        return opz[opz.index(nome) + 1] if nome in opz else None
    prima = val("--prima-di")
    d = costruisci(leggi(path), casa, ospite, dt.date.fromisoformat(prima) if prima else None)
    if val("--partita"):
        d["partita"] = val("--partita")
    d["assenze_verificate"] = "--assenze-ok" in opz
    d["correzioni"] = []
    for i, o in enumerate(opz):
        if o == "--correzione":
            sq, cod = opz[i + 1].split(":")
            d["correzioni"].append({"squadra": sq, "codice": cod})
    d["tipo_quota"] = val("--tipo-quota") or "Eurobet"
    d["quote"] = {}
    if val("--q"):
        d["quote"].update(quote_rapide(val("--q")))
    if val("--quote"):
        for coppia in val("--quote").split(";"):
            k, v = coppia.rsplit("=", 1)
            d["quote"][k.strip()] = float(v.replace(",", "."))
    if val("--rif"):
        d["quote_riferimento"] = quote_rapide(val("--rif"))
        d["fonte_riferimento"] = val("--fonte-rif") or "riferimento"
    if val("--rif-da"):
        rif, fonte, arbitro = riferimento_da_fixtures(val("--rif-da"), casa, ospite)
        d["quote_riferimento"], d["fonte_riferimento"] = rif, fonte
        if arbitro:
            d["arbitro"] = arbitro
    print(json.dumps(d, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
