#!/usr/bin/env python3
"""Backtest del modello sulle partite già giocate di un CSV football-data.co.uk.

Uso: backtest.py risultati.csv [--min-partite 40] [--pesi 0,0.1,0.2,0.35]

Per ogni partita usa solo i dati disponibili prima di quella data, calcola le
probabilità 1X2 del modello e le confronta con il mercato (quote medie AvgH/AvgD/AvgA
senza margine) e con il risultato. Riporta:
- Brier score di mercato, modello solo dati e modello combinato col mercato per ogni peso;
- scarto medio del modello sulla favorita del mercato (bias);
- giocate 1X2 che le regole della skill avrebbero fatto (quota Bet365 di apertura),
  con profitto, ROI e CLV contro la quota Bet365 di chiusura.
Serve a scegliere PESO_DATI in modello.py su dati reali invece che a intuito.
"""
import math
import sys

import modello as M
import prepara_partita as P


def f(r, k):
    try:
        return float(r.get(k, ""))
    except ValueError:
        return None


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    partite = sorted(P.leggi(argv[0]), key=lambda p: p["data"])
    min_lega = int(argv[argv.index("--min-partite") + 1]) if "--min-partite" in argv else 40
    pesi = [float(x) for x in argv[argv.index("--pesi") + 1].split(",")] if "--pesi" in argv else [0.0, 0.1, 0.2, 0.35]

    risultati = []
    for p in partite:
        prima = [q for q in partite if q["data"] < p["data"]]
        if len(prima) < min_lega:
            continue
        r = p["riga"]
        q_avg = {"1": f(r, "AvgH"), "X": f(r, "AvgD"), "2": f(r, "AvgA")}
        if not all(q_avg.values()):
            continue
        d = P.costruisci(prima, p["casa"], p["ospite"])
        if d["casa"]["totale"]["partite"] < 2 * M.MIN_PARTITE or d["trasferta"]["totale"]["partite"] < 2 * M.MIN_PARTITE:
            continue
        s = sum(1 / v for v in q_avg.values())
        pm = {k: (1 / v) / s for k, v in q_avg.items()}
        lh, la, _ = M.gol_attesi(d)
        lm = M.lambda_mercato({"1": (pm["1"], ""), "x": (pm["X"], ""), "2": (pm["2"], "")})
        esito = "1" if p["gc"] > p["go"] else "X" if p["gc"] == p["go"] else "2"
        voce = {"esito": esito, "mercato": pm, "dati": None, "pesi": {},
                "q": {"1": f(r, "B365H"), "X": f(r, "B365D"), "2": f(r, "B365A")},
                "qc": {"1": f(r, "B365CH"), "X": f(r, "B365CD"), "2": f(r, "B365CA")}}
        g = M.griglia(lh, la)
        voce["dati"] = {k: M.prob(g, k) for k in ("1", "X", "2")}
        for w in pesi:
            bh = math.exp(w * math.log(lh) + (1 - w) * math.log(lm[0]))
            ba = math.exp(w * math.log(la) + (1 - w) * math.log(lm[1]))
            gb = M.griglia(bh, ba)
            voce["pesi"][w] = {k: M.prob(gb, k) for k in ("1", "X", "2")}
        risultati.append(voce)

    n = len(risultati)
    print(f"Partite nel backtest: {n} (modello v{M.VERSIONE_MODELLO})")
    if not n:
        return 0

    def brier(get):
        return sum(sum((get(v)[k] - (v["esito"] == k)) ** 2 for k in ("1", "X", "2")) for v in risultati) / n

    print(f"Brier mercato: {brier(lambda v: v['mercato']):.4f}")
    print(f"Brier solo dati: {brier(lambda v: v['dati']):.4f}")
    for w in pesi:
        print(f"Brier dati {w * 100:.0f}% + mercato {(1 - w) * 100:.0f}%: {brier(lambda v, w=w: v['pesi'][w]):.4f}")
    scarti = [v["dati"][max(v["mercato"], key=v["mercato"].get)] - max(v["mercato"].values()) for v in risultati]
    print(f"Scarto medio dei soli dati sulla favorita del mercato: {sum(scarti) / n * 100:+.1f} punti")

    w = M.PESO_DATI
    if w not in pesi:
        return 0
    giocate, profitto, clv = 0, 0.0, []
    for v in risultati:
        if max(abs(v["dati"][k] - v["mercato"][k]) for k in ("1", "X", "2")) > M.SOGLIA_DISACCORDO:
            continue
        for k in ("1", "X", "2"):
            p, q = v["pesi"][w][k], v["q"][k]
            if not q:
                continue
            pmk = v["mercato"][k]
            if abs(p - pmk) > M.SOGLIA_ANOMALIA or (pmk < 0.20 and p > M.RAPPORTO_ANOMALIA * pmk):
                continue
            if p * q - 1 >= M.soglia_valore(q):
                giocate += 1
                profitto += (q - 1) if v["esito"] == k else -1
                if v["qc"][k]:
                    clv.append(q / v["qc"][k] - 1)
    print(f"\nRegole della skill con PESO_DATI = {w}: {giocate} giocate 1X2")
    if giocate:
        print(f"Profitto {profitto:+.2f} unità · ROI {profitto / giocate * 100:+.1f}%"
              + (f" · CLV medio {sum(clv) / len(clv) * 100:+.1f}% su {len(clv)}" if clv else ""))
        print("Con meno di 200 giocate questi numeri sono quasi solo rumore: conta di più il confronto dei Brier.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
