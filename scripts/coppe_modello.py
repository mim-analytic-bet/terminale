#!/usr/bin/env python3
"""Modello per le coppe europee: Elo europeo costruito SOLO sui risultati reali (dati/coppe/storico_europa.csv + partite live),
trasformato in gol attesi con Poisson/Dixon-Coles. Ogni partita giocata aggiorna i rating (la 'memoria' del modello).
I parametri si tarano su dati passati con test walk-forward fuori campione (nessun look-ahead)."""
import csv, json, math, os, datetime as dt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORICO = os.path.join(BASE, "dati", "coppe", "storico_europa.csv")
PARAMS0 = {"ha": 65.0, "k": 0.0042, "mu": 2.75, "K": 36.0, "Kq": 12.0, "carry": 0.95, "init": 1400.0, "rho": 0.08}  # tarati su CL 2013-2023 (walk-forward), testati su 2023-2026
MAXG = 10


def leggi_storico(path=STORICO):
    out = []
    for r in csv.DictReader(open(path, encoding="utf-8")):
        out.append({"data": dt.date.fromisoformat(r["data"]), "comp": r["comp"], "casa": r["casa"], "ospite": r["ospite"],
                    "gc": int(r["gc"]), "go": int(r["go"]), "neutro": int(r.get("neutro") or 0)})
    out.sort(key=lambda m: m["data"])
    return out


def pois(l):
    p = [math.exp(-l)]
    for i in range(1, MAXG + 1): p.append(p[-1] * l / i)
    return p


def matrice(lh, la, rho):
    ph, pa = pois(lh), pois(la)
    M = [[ph[i] * pa[j] for j in range(MAXG + 1)] for i in range(MAXG + 1)]
    M[0][0] *= max(0.0, 1 - lh * la * rho); M[0][1] *= max(0.0, 1 + lh * rho); M[1][0] *= max(0.0, 1 + la * rho); M[1][1] *= max(0.0, 1 - rho)
    t = sum(map(sum, M))
    return [[x / t for x in r] for r in M]


def esiti(M):
    p1 = sum(M[i][j] for i in range(MAXG + 1) for j in range(i)); px = sum(M[i][i] for i in range(MAXG + 1)); p2 = 1 - p1 - px
    return p1, px, p2


def gol_attesi(rh, ra, neutro, P, agg_h=0.0, agg_a=0.0):
    """rh/ra = rating Elo; agg_* = correzioni (forma) in punti Elo."""
    d = rh + agg_h - (ra + agg_a) + (0 if neutro else P["ha"])
    return P["mu"] / 2 * math.exp(P["k"] * d / 2), P["mu"] / 2 * math.exp(-P["k"] * d / 2)


def stagione(d): return d.year if d.month >= 7 else d.year - 1


class Stato:
    """Rating correnti + storia dei risultati (memoria)."""
    def __init__(self, P=None):
        self.P = dict(PARAMS0, **(P or {})); self.r = {}; self.stag = None; self.n = {}

    def rating(self, t): return self.r.get(t, self.P["init"])

    def inizio_stagione(self, d):
        s = stagione(d)
        if self.stag is not None and s != self.stag:
            m = sum(self.r.values()) / len(self.r) if self.r else 1500
            for t in self.r: self.r[t] = m + self.P["carry"] * (self.r[t] - m)
        self.stag = s

    def prevedi(self, casa, osp, neutro=0, agg_h=0.0, agg_a=0.0):
        lh, la = gol_attesi(self.rating(casa), self.rating(osp), neutro, self.P, agg_h, agg_a)
        M = matrice(lh, la, self.P["rho"]); return lh, la, M

    def aggiorna(self, m):
        self.inizio_stagione(m["data"])
        lh, la, M = self.prevedi(m["casa"], m["ospite"], m["neutro"])
        p1, px, p2 = esiti(M); gc, go = m["gc"], m["go"]
        S = 1.0 if gc > go else 0.5 if gc == go else 0.0
        E = p1 + 0.5 * px
        gd = abs(gc - go); G = 1.0 if gd <= 1 else 1.5 if gd == 2 else (11 + gd) / 8
        K = (self.P["K"] if m["comp"] in ("cl", "el", "conf") else self.P["Kq"]) * G
        self.r[m["casa"]] = self.rating(m["casa"]) + K * (S - E)
        self.r[m["ospite"]] = self.rating(m["ospite"]) - K * (S - E)
        self.n[m["casa"]] = self.n.get(m["casa"], 0) + 1; self.n[m["ospite"]] = self.n.get(m["ospite"], 0) + 1
        return (p1, px, p2), (lh, la)


def walk_forward(matches, P=None, solo=("cl",), da=None):
    """Prevede ogni partita PRIMA di vederla, poi aggiorna. Restituisce le metriche sulle partite delle competizioni 'solo' dal 'da' in poi."""
    st = Stato(P); br = ll = n = 0; hit = 0; freq = [0, 0, 0]; rows = []
    for m in matches:
        pr, (lh, la) = st.aggiorna(m)
        if m["comp"] in solo and (da is None or m["data"] >= da):
            o = (1, 0, 0) if m["gc"] > m["go"] else (0, 1, 0) if m["gc"] == m["go"] else (0, 0, 1)
            br += sum((pr[i] - o[i]) ** 2 for i in range(3)); n += 1; hit += max(range(3), key=lambda i: pr[i]) == o.index(1)
            ph, pa = pois(lh), pois(la); ll += -math.log(max(1e-9, ph[min(m["gc"], MAXG)] * pa[min(m["go"], MAXG)]))
            for i in range(3): freq[i] += o[i]
            rows.append((m, pr, o))
    return {"n": n, "brier": br / max(1, n), "ll_gol": ll / max(1, n), "hit": hit / max(1, n), "freq": [f / max(1, n) for f in freq], "rows": rows, "stato": st}


def brier_base(rows_train_freq, rows):
    f = rows_train_freq
    return sum(sum((f[i] - o[i]) ** 2 for i in range(3)) for _, _, o in rows) / max(1, len(rows))
