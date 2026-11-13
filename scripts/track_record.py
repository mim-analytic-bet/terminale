"""Track record del modello: (1) backtest walk-forward sulle partite gia' giocate (solo dati precedenti),
(2) registro live: le previsioni vengono congelate PRIMA della partita e valutate quando arriva il risultato."""
import csv, math, os, datetime as dt
import prepara_partita as pp
import modello as mod

MIN_LEGA = 30   # partite minime di lega prima di prevedere
MIN_TOT = 6     # partite minime per squadra (casa+trasferta) nel backtest
SOGLIA_VALORE = 0.05
MERCATI = ("1", "X", "2", "Over 2,5", "Gol")

def _f(r, k):
    try:
        v = float(r.get(k, "")); return v if v > 1 else None
    except ValueError:
        return None

def esiti(p):
    return {"1": p["gc"] > p["go"], "X": p["gc"] == p["go"], "2": p["gc"] < p["go"],
            "Over 2,5": p["gc"] + p["go"] > 2, "Gol": p["gc"] > 0 and p["go"] > 0}

def backtest(partite):
    partite = sorted(partite, key=lambda p: p["data"])
    righe = []
    for p in partite:
        prima = [q for q in partite if q["data"] < p["data"]]
        if len(prima) < MIN_LEGA: continue
        try:
            d = pp.costruisci(prima, p["casa"], p["ospite"])
            if d["casa"]["totale"]["partite"] < MIN_TOT or d["trasferta"]["totale"]["partite"] < MIN_TOT: continue
            d["assenze_verificate"] = False
            ra = mod.analizza(d); b = ra["base_dati"]
            lam = (ra["gol_attesi_dati"]["casa"], ra["gol_attesi_dati"]["trasferta"])
            lg = (d["lega"]["media_gol_casa"], d["lega"]["media_gol_trasferta"])
        except SystemExit:
            continue
        r = p["riga"]; e = esiti(p)
        q = {"1": _f(r, "B365H"), "X": _f(r, "B365D"), "2": _f(r, "B365A"), "Over 2,5": _f(r, "B365>2.5")}
        a = [_f(r, "AvgH"), _f(r, "AvgD"), _f(r, "AvgA")]
        mk = None
        if all(a):
            s = sum(1 / x for x in a); mk = {k: (1 / x) / s for k, x in zip("1 X 2".split(), a)}
        righe.append({"p": b, "e": e, "q": q, "mk": mk, "lam": lam, "lg": lg, "gc": p["gc"], "go": p["go"]})
    return righe

def riepilogo(righe):
    n = len(righe)
    if n == 0: return {"n": 0}
    def brier(sel):
        return sum(sum((pr[k] - (1 if e[k] else 0)) ** 2 for k in "1 X 2".split()) for pr, e in sel) / len(sel)
    mod_ = [(r["p"], r["e"]) for r in righe]
    con_mk = [r for r in righe if r["mk"]]
    out = {"n": n, "brier_modello": round(brier(mod_), 4)}
    out["hit_1x2"] = round(100 * sum(max("1 X 2".split(), key=lambda k: r["p"][k]) in [k for k in "1 X 2".split() if r["e"][k]] for r in righe) / n, 1)
    if con_mk:
        out["brier_mercato"] = round(brier([(r["mk"], r["e"]) for r in con_mk]), 4)
        out["brier_modello_su_stesse"] = round(brier([(r["p"], r["e"]) for r in con_mk]), 4)
        out["n_mercato"] = len(con_mk)
    # calibrazione: fasce di probabilita' su tutti i 5 mercati
    fasce = [(0, .2), (.2, .35), (.35, .5), (.5, .65), (.65, .8), (.8, 1.01)]
    cal = []
    for lo, hi in fasce:
        v = [(r["p"][k], r["e"][k]) for r in righe for k in MERCATI if lo <= r["p"][k] < hi]
        if v: cal.append({"fascia": f"{int(lo*100)}-{min(int(hi*100),100)}%", "n": len(v), "previsto": round(100 * sum(x for x, _ in v) / len(v), 1), "reale": round(100 * sum(y for _, y in v) / len(v), 1)})
    out["calibrazione"] = cal
    # regola di valore: puntare 1u se prob*quota-1 >= soglia (quote Bet365 di apertura)
    pn, profitto = 0, 0.0
    for r in righe:
        for k, qv in r["q"].items():
            if qv and r["p"][k] * qv - 1 >= SOGLIA_VALORE:
                pn += 1; profitto += (qv - 1) if r["e"][k] else -1
    out["value_giocate"] = pn; out["value_roi"] = round(100 * profitto / pn, 1) if pn else None
    return out

# ---------- registro live ----------
CAMPI = ["lega", "casa", "ospite", "giorno", "registrata", "versione", "lh", "la", "mc", "mt", "p1", "pX", "p2", "pOver25", "pGol",
         "q1", "qX", "q2", "qOver25", "gc", "go", "stato"]

def leggi_log(path):
    if not os.path.exists(path): return []
    return list(csv.DictReader(open(path, encoding="utf-8")))

def aggiorna_live(path, previsioni, archivi):
    """previsioni: lista dict (lega, casa, ospite, giorno, p1.., q..); archivi: {lega: partite CSV}."""
    log = leggi_log(path); chiavi = {(r["lega"], r["casa"], r["ospite"]) for r in log}
    oggi = dt.date.today().isoformat()
    for p in previsioni:
        if (p["lega"], p["casa"], p["ospite"]) in chiavi: continue
        log.append({**{c: "" for c in CAMPI}, **p, "registrata": oggi, "versione": mod.VERSIONE_MODELLO, "stato": "aperta"})
    for r in log:
        if r["stato"] == "valutata": continue
        for g in archivi.get(r["lega"], []):
            if g["casa"] == r["casa"] and g["ospite"] == r["ospite"] and g["data"].isoformat() >= r["registrata"][:10]:
                r["gc"], r["go"], r["stato"] = g["gc"], g["go"], "valutata"; break
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPI); w.writeheader(); w.writerows(log)
    return log

def riepilogo_live(log):
    val = [r for r in log if r["stato"] == "valutata"]
    out = {"registrate": len(log), "valutate": len(val)}
    if val:
        def fl(x): return float(x)
        hit = 0; br = 0.0
        for r in val:
            gc, go = int(r["gc"]), int(r["go"]); e = {"1": gc > go, "X": gc == go, "2": gc < go}
            pr = {"1": fl(r["p1"]), "X": fl(r["pX"]), "2": fl(r["p2"])}
            hit += e[max(pr, key=pr.get)]; br += sum((pr[k] - e[k]) ** 2 for k in pr)
        out["hit_1x2"] = round(100 * hit / len(val), 1); out["brier"] = round(br / len(val), 4)
    return out
