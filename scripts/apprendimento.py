"""Livello di apprendimento: misura quanto fidarsi del modello e si ricalibra da solo.
Impara UN parametro, w = peso dei gol attesi del modello contro la media di lega
(gol' = w*modello + (1-w)*media_lega), minimizzando il Brier walk-forward su partite reali
(backtest storico + registro live congelato). La memoria resta in dati/memoria_modello.json."""
import json, os, datetime as dt
import modello as mod

W_GRID = [round(x * 0.05, 2) for x in range(0, 33)]   # 0.00 .. 1.60
A_GRID = [round(x * 0.05, 2) for x in range(0, 21)]   # peso dei dati contro il mercato 0..1
MIN_CASI = 60

def _brier(lam, lg, gc, go, w):
    lh = w * lam[0] + (1 - w) * lg[0]; la = w * lam[1] + (1 - w) * lg[1]
    lh, la = max(lh, 0.15), max(la, 0.15)
    g = mod.griglia(lh, la)
    e = {"1": gc > go, "X": gc == go, "2": gc < go, "Over 2,5": gc + go > 2, "Gol": gc > 0 and go > 0}
    return sum((mod.prob(g, k) - e[k]) ** 2 for k in e)

def righe_live(log):
    out = []
    for r in log:
        if r.get("stato") == "valutata" and r.get("lh"):
            out.append({"lam": (float(r["lh"]), float(r["la"])), "lg": (float(r["mc"]), float(r["mt"])), "gc": int(r["gc"]), "go": int(r["go"])})
    return out

def impara(righe_bt, righe_lv, mem_path):
    mem = json.load(open(mem_path, encoding="utf-8")) if os.path.exists(mem_path) else {"w": 1.0, "storia": []}
    dati = righe_bt + righe_lv * 2          # le previsioni congelate pesano doppio
    if len(dati) < MIN_CASI:
        return mem
    def L(w): return sum(_brier(r["lam"], r["lg"], r["gc"], r["go"], w) for r in dati) / len(dati)
    punteggi = {w: L(w) for w in W_GRID}
    w = min(punteggi, key=punteggi.get)
    guadagno = (punteggi[1.0] - punteggi[w]) / punteggi[1.0]
    if guadagno < 0.005: w = 1.0   # guadagno sotto lo 0,5%: e' rumore, non si adotta
    voce = {"data": dt.date.today().isoformat(), "casi_backtest": len(righe_bt), "casi_live": len(righe_lv), "w": w,
            "perdita_senza_apprendimento": round(punteggi[1.0], 4), "perdita_con_apprendimento": round(punteggi[w], 4), "guadagno_pct": round(100 * guadagno, 2)}
    mem["w"] = w
    # peso dei dati nella stima combinata con il mercato (1X2), appreso dove le quote esistono
    con = [r for r in righe_bt if r.get("mk")]
    if len(con) >= MIN_CASI:
        def Lm(a):
            t = 0.0
            for r in con:
                for k in ("1", "X", "2"):
                    t += (a * r["p"][k] + (1 - a) * r["mk"][k] - (1 if r["e"][k] else 0)) ** 2
            return t / len(con)
        ps = {a: Lm(a) for a in A_GRID}; a = min(ps, key=ps.get)
        mem["a"] = a; voce["peso_dati_vs_mercato"] = a; voce["brier_mercato_puro"] = round(ps[0.0], 4); voce["brier_misto_appreso"] = round(ps[a], 4)
    ult = mem["storia"][-1] if mem["storia"] else None
    if not ult or (ult["casi_backtest"], ult["casi_live"]) != (voce["casi_backtest"], voce["casi_live"]):
        mem["storia"].append(voce)
    mem["storia"] = mem["storia"][-60:]
    json.dump(mem, open(mem_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return mem

def ricalibra(r, d, w):
    """Ricalcola griglia, probabilita' e mercati con i gol attesi ritarati. Non tocca partite con quote di riferimento."""
    if r.get("gol_attesi_mercato") or abs(w - 1.0) < 1e-9: return r
    mc, mt = d["lega"]["media_gol_casa"], d["lega"]["media_gol_trasferta"]
    lh = max(w * r["gol_attesi"]["casa"] + (1 - w) * mc, 0.15); la = max(w * r["gol_attesi"]["trasferta"] + (1 - w) * mt, 0.15)
    g = mod.griglia(lh, la)
    r = dict(r); r["gol_attesi"] = {"casa": lh, "trasferta": la}
    r["base"] = {k: mod.prob(g, k) for k in ("1", "X", "2", "Over 2,5", "Gol")}
    r["punteggi_top"] = sorted(((f"{i}-{j}", g[i][j]) for i in range(mod.MAX_GOL + 1) for j in range(mod.MAX_GOL + 1)), key=lambda x: -x[1])[:6]
    dq = []
    for n in mod.CATALOGO:
        p = mod.prob(g, n)
        if p < 0.05: continue
        qe = 1 / p; s = mod.soglia_valore(qe)
        dq.append({"mercato": n, "prob_modello": p, "quota_equa": qe, "quota_minima": (1 + s) / p})
    r["da_quotare"] = dq
    return r
