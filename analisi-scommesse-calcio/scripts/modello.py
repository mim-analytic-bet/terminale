#!/usr/bin/env python3
"""Modello fisso di una partita: gol attesi, griglia dei punteggi, probabilità di
tutti i mercati, confronto con le quote, podio delle giocate.

Uso:
  modello.py partita.json            output leggibile
  modello.py partita.json --json     output JSON (per salvare o confrontare)
  modello.py --esempio               stampa un file di input di esempio

Tutti i parametri sono fissi (vedi PARAMETRI): stessi dati in ingresso danno
sempre gli stessi numeri, in qualsiasi sessione.
"""
import json
import math
import re
import sys

# ---------------------------------------------------------------- PARAMETRI
VERSIONE_MODELLO = "2.2"
K_SHRINK = 3            # peso, in partite, della media di campionato
K_SHRINK_SEDE = 6       # come sopra, solo se mancano i dati totali e si usano quelli per sede
PESO_XG = 0.6           # se ci sono xG: 60% xG + 40% gol reali
K_CAMPO = None          # fattore campo per squadra: peso, in partite, del fattore medio di lega (None = spento)
RHO_DC = -0.10          # correzione Dixon-Coles sui punteggi bassi
MAX_GOL = 10            # griglia 0..10 per squadra
QUOTA_1T_LEGA = 0.45    # quota media dei gol segnati nel primo tempo
MIN_PARTITE = 5         # dati minimi per sede (casa / trasferta)
PESO_DATI = 0.20        # peso dei dati nella stima finale (il resto è il mercato); da backtest, vedi SKILL.md
SOGLIA_DISACCORDO = 0.15  # se i soli dati distano più di 15 punti dal mercato sull'1X2: NO BET sulla partita
SOGLIA_ANOMALIA = 0.08  # scarto stima-mercato oltre il quale un singolo mercato non si gioca
RAPPORTO_ANOMALIA = 1.5 # per esiti sotto il 20%: modello > 1,5 volte il mercato
FASCIA_SICURA = (1.25, 1.35)

# Correzioni ammesse: codice -> (su cosa agisce, moltiplicatore)
CORREZIONI = {
    "ASSENZA_BOMBER":       ("attacco", 0.92),  # capocannoniere o rigorista fuori
    "ASSENZE_ATTACCO_2":    ("attacco", 0.88),  # due titolari offensivi fuori
    "ASSENZA_PORTIERE":     ("difesa", 1.06),   # portiere titolare fuori
    "ASSENZE_DIFESA_2":     ("difesa", 1.08),   # due difensori titolari fuori
    "TURNOVER":             ("attacco", 0.95),  # turnover dichiarato per coppe
    "NULLA_DA_CHIEDERE":    ("attacco", 0.95),  # nessun obiettivo di classifica
}


def soglia_valore(q):
    if q <= 2.50:
        return 0.03
    if q <= 5.0:
        return 0.05
    return 0.08


# ---------------------------------------------------------------- MODELLO
def tasso(sq, chiave_gol, chiave_xg, media_lega):
    n = sq["partite"]
    oss = sq[chiave_gol] / n if n else media_lega
    if sq.get(chiave_xg) is not None and n:
        oss = PESO_XG * sq[chiave_xg] / n + (1 - PESO_XG) * oss
    return (n * oss + K_SHRINK * media_lega) / (n + K_SHRINK)


def forza(tot, chiave, chiave_xg, chiave_attesi):
    """Rapporto tra gol (o mix xG/gol) e gol attesi per una squadra media con lo
    stesso calendario casa/trasferta, tirato verso 1 con peso K_SHRINK partite."""
    n = tot["partite"]
    oss = tot[chiave]
    if tot.get(chiave_xg) is not None:
        oss = PESO_XG * tot[chiave_xg] + (1 - PESO_XG) * oss
    att = tot[chiave_attesi]
    media = att / n
    return (oss + K_SHRINK * media) / (att + K_SHRINK * media)


def fattore_sede(sede, tot, chiave, chiave_xg, chiave_attesi, media_sede):
    n = sede["partite"]
    if not n:
        return 1.0

    def mix(b, att):
        o = b[chiave]
        if b.get(chiave_xg) is not None:
            o = PESO_XG * b[chiave_xg] + (1 - PESO_XG) * o
        return o / att
    r_sede = mix(sede, n * media_sede)
    r_tot = mix(tot, tot[chiave_attesi])
    if r_tot <= 0:
        return 1.0
    r = r_sede / r_tot
    return (n * r + K_CAMPO) / (n + K_CAMPO)


def gol_attesi(d):
    lega, casa, osp = d["lega"], d["casa"], d["trasferta"]
    mc, mt = lega["media_gol_casa"], lega["media_gol_trasferta"]
    if casa.get("totale") and osp.get("totale"):
        # Metodo principale: tutte le partite della stagione, normalizzate per sede
        tc, to = casa["totale"], osp["totale"]
        att_c = forza(tc, "gol_fatti", "xg", "gol_fatti_attesi")
        dif_c = forza(tc, "gol_subiti", "xga", "gol_subiti_attesi")
        att_o = forza(to, "gol_fatti", "xg", "gol_fatti_attesi")
        dif_o = forza(to, "gol_subiti", "xga", "gol_subiti_attesi")
        if K_CAMPO is not None:
            # Fattore campo della singola squadra: quanto rende nella sede di questa
            # partita rispetto alla sua media stagionale, tirato verso 1 (= fattore di lega)
            att_c *= fattore_sede(casa, tc, "gol_fatti", "xg", "gol_fatti_attesi", mc)
            dif_c *= fattore_sede(casa, tc, "gol_subiti", "xga", "gol_subiti_attesi", mt)
            att_o *= fattore_sede(osp, to, "gol_fatti", "xg", "gol_fatti_attesi", mt)
            dif_o *= fattore_sede(osp, to, "gol_subiti", "xga", "gol_subiti_attesi", mc)
    else:
        # Ripiego: solo partite in casa per la squadra di casa, in trasferta per l'ospite
        global K_SHRINK
        k0, K_SHRINK = K_SHRINK, K_SHRINK_SEDE
        att_c = tasso(casa, "gol_fatti", "xg", mc) / mc
        dif_c = tasso(casa, "gol_subiti", "xga", mt) / mt
        att_o = tasso(osp, "gol_fatti", "xg", mt) / mt
        dif_o = tasso(osp, "gol_subiti", "xga", mc) / mc
        K_SHRINK = k0
    mult = {"casa": {"attacco": 1.0, "difesa": 1.0}, "trasferta": {"attacco": 1.0, "difesa": 1.0}}
    applicate = []
    for c in d.get("correzioni", []):
        if c["codice"] not in CORREZIONI:
            raise SystemExit(f"Correzione non ammessa: {c['codice']}. Ammesse: {', '.join(CORREZIONI)}")
        cosa, m = CORREZIONI[c["codice"]]
        mult[c["squadra"]][cosa] *= m
        applicate.append(f"{c['squadra']}: {c['codice']} ({cosa} x{m})")
    lh = mc * att_c * dif_o * mult["casa"]["attacco"] * mult["trasferta"]["difesa"]
    la = mt * att_o * dif_c * mult["trasferta"]["attacco"] * mult["casa"]["difesa"]
    return lh, la, applicate


def pois(k, lam):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def griglia(lh, la, rho=RHO_DC):
    g = [[pois(i, lh) * pois(j, la) for j in range(MAX_GOL + 1)] for i in range(MAX_GOL + 1)]
    if rho:
        g[0][0] *= 1 - lh * la * rho
        g[0][1] *= 1 + lh * rho
        g[1][0] *= 1 + la * rho
        g[1][1] *= 1 - rho
    tot = sum(map(sum, g))
    return [[x / tot for x in r] for r in g]


# ---------------------------------------------------------------- MERCATI
def num(s):
    return float(s.replace(",", "."))


def predicato(nome):
    """Restituisce una funzione (h, a) -> bool per un mercato a tempo pieno."""
    n = nome.strip()
    low = n.lower()
    if " oppure " in low:
        parti = [predicato(p) for p in re.split(r"\s+oppure\s+", n, flags=re.I)]
        return lambda h, a: any(p(h, a) for p in parti)
    if " + " in n:
        parti = [predicato(p) for p in n.split(" + ")]
        return lambda h, a: all(p(h, a) for p in parti)
    fissi = {
        "1": lambda h, a: h > a, "x": lambda h, a: h == a, "2": lambda h, a: h < a,
        "1x": lambda h, a: h >= a, "x2": lambda h, a: h <= a, "12": lambda h, a: h != a,
        "gol": lambda h, a: h > 0 and a > 0, "gg": lambda h, a: h > 0 and a > 0,
        "no gol": lambda h, a: h == 0 or a == 0, "ng": lambda h, a: h == 0 or a == 0,
    }
    if low in fissi:
        return fissi[low]
    m = re.fullmatch(r"(casa|ospite)?\s*(over|under)\s*([\d,\.]+)", low)
    if m:
        chi, tipo, s = m.group(1), m.group(2), num(m.group(3))
        val = (lambda h, a: h) if chi == "casa" else (lambda h, a: a) if chi == "ospite" else (lambda h, a: h + a)
        return (lambda h, a: val(h, a) > s) if tipo == "over" else (lambda h, a: val(h, a) < s)
    m = re.fullmatch(r"(casa|ospite)?\s*multigol\s*(\d+)\s*-\s*(\d+)", low)
    if m:
        chi, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
        val = (lambda h, a: h) if chi == "casa" else (lambda h, a: a) if chi == "ospite" else (lambda h, a: h + a)
        return lambda h, a: lo <= val(h, a) <= hi
    m = re.fullmatch(r"(?:esatto\s*)?(\d+)\s*-\s*(\d+)", low)
    if m:
        x, y = int(m.group(1)), int(m.group(2))
        return lambda h, a: h == x and a == y
    m = re.fullmatch(r"(?:esatti|multiesito|gruppo)\s*(.+)", low)
    if m:
        punteggi = [tuple(map(int, p.split("-"))) for p in re.split(r"\s*[/,]\s*", m.group(1))]
        return lambda h, a: (h, a) in punteggi
    raise SystemExit(f"Mercato non riconosciuto: '{nome}'")


def prob(g, nome):
    p = predicato(nome)
    return sum(g[i][j] for i in range(MAX_GOL + 1) for j in range(MAX_GOL + 1) if p(i, j))


def p_segna(lam):
    return 1 - math.exp(-lam)


def tempi(d, lh, la):
    q1c = d["casa"].get("quota_gol_1t")
    q1o = d["trasferta"].get("quota_gol_1t")
    reali = q1c is not None and q1o is not None
    q1c = QUOTA_1T_LEGA if q1c is None else q1c
    q1o = QUOTA_1T_LEGA if q1o is None else q1o
    gg1 = p_segna(lh * q1c) * p_segna(la * q1o)
    gg2 = p_segna(lh * (1 - q1c)) * p_segna(la * (1 - q1o))
    return {"GG 1T": gg1, "GG 2T": gg2, "GG 1T + GG 2T": gg1 * gg2, "dati_per_tempo_reali": reali}


CATALOGO = (
    ["1", "X", "2", "1X", "X2", "12", "Gol", "No Gol"]
    + [f"{t} {s}" for s in ("0,5", "1,5", "2,5", "3,5", "4,5") for t in ("Over", "Under")]
    + ["Multigol 1-2", "Multigol 1-3", "Multigol 2-3", "Multigol 2-4", "Multigol 3-5"]
    + ["Casa Over 0,5", "Casa Over 1,5", "Ospite Over 0,5", "Ospite Over 1,5"]
    + [f"{e} + {u}" for e in ("1", "X", "2", "1X", "X2") for u in ("Over 1,5", "Over 2,5", "Under 2,5", "Under 3,5", "Gol", "No Gol")]
    + ["Gol + Over 2,5", "No Gol + Under 2,5"]
    + [f"{a} oppure {b}" for a, b in (("1", "Over 2,5"), ("2", "Over 2,5"), ("1", "Gol"), ("2", "Gol"),
                                        ("X", "Gol"), ("X", "Under 2,5"), ("1", "Under 2,5"), ("2", "Under 2,5"))]
)

# Gruppi di esiti che si escludono e coprono tutto: servono per togliere il margine
GRUPPI_DEVIG = [["1", "X", "2"], ["Gol", "No Gol"]] + [[f"Over {s}", f"Under {s}"] for s in ("0,5", "1,5", "2,5", "3,5", "4,5")] \
    + [[f"Casa Over {s}", f"Casa Under {s}"] for s in ("0,5", "1,5", "2,5")] \
    + [[f"Ospite Over {s}", f"Ospite Under {s}"] for s in ("0,5", "1,5", "2,5")]


def norm(k):
    return re.sub(r"\s+", " ", k.strip()).lower()


def prob_mercato(quote):
    """Probabilità senza margine, per ogni quota. Restituisce {nome: (p, metodo)}."""
    q = {norm(k): v for k, v in quote.items()}
    out = {}
    margine_1x2 = None
    for gr in GRUPPI_DEVIG:
        nomi = [norm(x) for x in gr]
        if all(n in q for n in nomi):
            inv = [1 / q[n] for n in nomi]
            s = sum(inv)
            if nomi[0] == "1":
                margine_1x2 = s
            for n, i in zip(nomi, inv):
                out[n] = (i / s, "margine tolto sul mercato completo")
    if all(n in out for n in ("1", "x", "2")):
        p1, px, p2 = out["1"][0], out["x"][0], out["2"][0]
        for n, v in (("1x", p1 + px), ("x2", px + p2), ("12", p1 + p2)):
            if n in q:
                out[n] = (v, "dal 1X2 senza margine")
    for n, v in q.items():
        if n not in out:
            if margine_1x2:
                out[n] = ((1 / v) / margine_1x2, "margine stimato dal 1X2")
            else:
                out[n] = (1 / v, "margine non tolto (nessun mercato completo)")
    return out


# ---------------------------------------------------------------- ANALISI
def lambda_mercato(pm):
    """Gol attesi impliciti nelle quote: i due valori che riproducono meglio
    1X2 (e Over 2,5 se c'è) senza margine. Ricerca a griglia, prima larga poi fine."""
    obiettivo = [("1", pm["1"][0]), ("X", pm["x"][0]), ("2", pm["2"][0])]
    if "over 2,5" in pm:
        obiettivo.append(("Over 2,5", pm["over 2,5"][0]))

    def errore(lh, la):
        g = griglia(lh, la)
        return sum((prob(g, n) - p) ** 2 for n, p in obiettivo)

    best = None
    for passo, centro, raggio in ((0.10, None, None), (0.02, None, 0.12), (0.005, None, 0.03)):
        if best is None:
            xs = [0.2 + passo * i for i in range(int((3.8 - 0.2) / passo) + 1)]
            ys = xs
        else:
            xs = [best[1] - raggio + passo * i for i in range(int(2 * raggio / passo) + 1)]
            ys = [best[2] - raggio + passo * i for i in range(int(2 * raggio / passo) + 1)]
        for x in xs:
            for y in ys:
                if x <= 0 or y <= 0:
                    continue
                e = errore(x, y)
                if best is None or e < best[0]:
                    best = (e, x, y)
    return best[1], best[2]


def analizza(d):
    lh_d, la_d, applicate = gol_attesi(d)
    g_dati = griglia(lh_d, la_d)
    base_dati = {n: prob(g_dati, n) for n in ["1", "X", "2", "Over 2,5", "Gol"]}
    if d["casa"].get("totale") and d["trasferta"].get("totale"):
        pc, po = d["casa"]["totale"]["partite"], d["trasferta"]["totale"]["partite"]
        minimo, cosa = 2 * MIN_PARTITE, "partite giocate"
    else:
        pc, po = d["casa"]["partite"], d["trasferta"]["partite"]
        minimo, cosa = MIN_PARTITE, "partite per sede"
    dati_ok = pc >= minimo and po >= minimo and d.get("assenze_verificate", False)
    motivi_gate = []
    if pc < minimo or po < minimo:
        motivi_gate.append(f"meno di {minimo} {cosa} (casa {pc}, trasferta {po})")
    if not d.get("assenze_verificate", False):
        motivi_gate.append("assenze non verificate entro 48 ore dalla partita")

    quote = d.get("quote", {})
    tipo_quota = d.get("tipo_quota", "Eurobet")
    quota_reale = tipo_quota.lower() not in ("indicativa", "")
    pm = prob_mercato(quote) if quote else {}
    # Quote di riferimento: il consenso del mercato (exchange o media di molti
    # bookmaker), più efficiente delle quote di un singolo bookmaker. Se ci sono,
    # sono loro l'ancora del modello e il metro per giudicare il prezzo Eurobet.
    rif = d.get("quote_riferimento") or {}
    fonte_rif = d.get("fonte_riferimento", "riferimento")
    pm_rif = prob_mercato(rif) if rif else {}
    pm_ancora = pm_rif if all(k in pm_rif for k in ("1", "x", "2")) else pm
    ancora_ok = (pm_ancora is pm_rif and pm_rif) or quota_reale

    # Stima finale: se ci sono le quote 1X2 reali, i gol attesi sono una media fissa
    # (in scala logaritmica) tra quelli dei dati (peso PESO_DATI) e quelli impliciti
    # nel mercato. Il mercato contiene informazioni che i dati della stagione non hanno
    # (rosa, storico, assenze note); i dati servono a trovare dove il mercato sbaglia.
    disaccordo_1x2 = None
    lambda_mkt = None
    if ancora_ok and all(k in pm_ancora for k in ("1", "x", "2")):
        pm_a = pm_ancora
        lambda_mkt = lambda_mercato(pm_a)
        dev = {k: base_dati[k.upper()] - pm_a[k][0] for k in ("1", "x", "2")}
        peggiore = max(dev, key=lambda k: abs(dev[k]))
        if abs(dev[peggiore]) > SOGLIA_DISACCORDO:
            disaccordo_1x2 = (f"esito {peggiore.upper()}: dati {base_dati[peggiore.upper()] * 100:.0f}% "
                              f"contro mercato {pm_a[peggiore][0] * 100:.0f}%")
        lh = math.exp(PESO_DATI * math.log(lh_d) + (1 - PESO_DATI) * math.log(lambda_mkt[0]))
        la = math.exp(PESO_DATI * math.log(la_d) + (1 - PESO_DATI) * math.log(lambda_mkt[1]))
        ancora = fonte_rif if pm_a is pm_rif else tipo_quota
        metodo_stima = f"dati {PESO_DATI * 100:.0f}% + mercato {(1 - PESO_DATI) * 100:.0f}% ({ancora})"
    else:
        lh, la = lh_d, la_d
        metodo_stima = "solo dati (nessuna quota 1X2 reale)"

    g = griglia(lh, la)
    t = tempi(d, lh, la)
    base = {n: prob(g, n) for n in ["1", "X", "2", "Over 2,5", "Gol"]}
    punteggi = sorted(((g[i][j], f"{i}-{j}") for i in range(MAX_GOL + 1) for j in range(MAX_GOL + 1)), reverse=True)[:6]

    valutazioni = []
    for nome, q in quote.items():
        if nome.strip().upper().startswith("GG 1T") or nome.strip().upper() == "GG 2T":
            p = t[nome.strip()] if nome.strip() in t else None
            if p is None:
                continue
            speciale = "GG tempi"
        else:
            p = prob(g, nome)
            speciale = None
        p_m, metodo = pm[norm(nome)]
        valore = p * q - 1
        soglia = soglia_valore(q)
        # l'anomalia si misura contro il riferimento, se c'è (più affidabile di Eurobet)
        p_cfr = pm_rif.get(norm(nome), (p_m, None))[0]
        scarto = p - p_cfr
        anomalia = abs(scarto) > SOGLIA_ANOMALIA or (p_cfr < 0.20 and p > RAPPORTO_ANOMALIA * p_cfr)
        if not quota_reale:
            stato = "SENZA QUOTA REALE"
        elif not dati_ok:
            stato = "DATI INSUFFICIENTI"
        elif speciale and not t["dati_per_tempo_reali"]:
            stato = "DATI PER TEMPO MANCANTI"
        elif disaccordo_1x2:
            stato = "PARTITA IN DISACCORDO COL MERCATO"
        elif anomalia:
            stato = "ANOMALIA DI MERCATO"
        elif valore >= soglia:
            stato = "GIOCABILE"
        else:
            stato = "VALORE INSUFFICIENTE"
        # Valore di prezzo: la quota Eurobet contro la probabilità del consenso
        p_r = pm_rif.get(norm(nome), (None, None))[0]
        valore_prezzo = p_r * q - 1 if p_r else None
        if quota_reale and p_r and valore_prezzo >= soglia and abs(p - p_r) <= SOGLIA_ANOMALIA \
                and not (speciale and not t["dati_per_tempo_reali"]) and (disaccordo_1x2 or valore >= 0):
            stato = "GIOCABILE (modello e prezzo)" if stato == "GIOCABILE" else "GIOCABILE (prezzo)"
        elif stato == "GIOCABILE":
            stato = "GIOCABILE (modello)"
        valutazioni.append({
            "mercato": nome, "quota": q, "prob_modello": p, "prob_mercato": p_m, "metodo_margine": metodo,
            "valore": valore, "soglia": soglia, "quota_minima": (1 + soglia) / p if p > 0 else None,
            "scarto": scarto, "stato": stato, "prob_riferimento": p_r, "valore_prezzo": valore_prezzo,
            "quota_equa_riferimento": 1 / p_r if p_r else None,
        })

    giocabili = sorted([v for v in valutazioni if v["stato"].startswith("GIOCABILE")],
                       key=lambda v: max(v["valore"], v["valore_prezzo"] if v["valore_prezzo"] is not None else -1), reverse=True)
    podio = giocabili[:3]

    # SICURA per la multipla: tra le quote reali in fascia, quella col valore migliore
    in_fascia = [v for v in valutazioni if FASCIA_SICURA[0] <= v["quota"] <= FASCIA_SICURA[1]]
    sicura = max(in_fascia, key=lambda v: v["valore"]) if in_fascia else None
    if sicura is None:
        cand = [(prob(g, n), n) for n in CATALOGO]
        cand = [(p, n) for p, n in cand if 1 / FASCIA_SICURA[1] <= p <= 1 / FASCIA_SICURA[0]]
        if cand:
            p, n = max(cand)
            sicura = {"mercato": n, "quota": None, "prob_modello": p, "quota_equa": 1 / p, "stato": "DA QUOTARE"}

    # Mercati del catalogo non quotati: quota minima per giocarli
    quotati = {norm(k) for k in quote}
    da_quotare = []
    for n in CATALOGO:
        if norm(n) in quotati:
            continue
        p = prob(g, n)
        if p < 0.05:
            continue
        q_eq = 1 / p
        s = soglia_valore(q_eq)
        da_quotare.append({"mercato": n, "prob_modello": p, "quota_equa": q_eq, "quota_minima": (1 + s) / p})

    return {
        "versione_modello": VERSIONE_MODELLO, "partita": d.get("partita", ""),
        "gol_attesi": {"casa": lh, "trasferta": la}, "gol_attesi_dati": {"casa": lh_d, "trasferta": la_d},
        "gol_attesi_mercato": ({"casa": lambda_mkt[0], "trasferta": lambda_mkt[1]} if lambda_mkt else None),
        "metodo_stima": metodo_stima, "base_dati": base_dati, "correzioni": applicate,
        "gate_dati": {"ok": dati_ok, "motivi": motivi_gate}, "disaccordo_1x2": disaccordo_1x2,
        "base": base, "punteggi_top": [(s, p) for p, s in punteggi],
        "tempi": t, "valutazioni": valutazioni, "podio": podio, "sicura_multipla": sicura,
        "da_quotare": da_quotare, "tipo_quota": tipo_quota, "fonte_riferimento": fonte_rif if rif else None,
    }


# ---------------------------------------------------------------- OUTPUT
def pc(x, d=1):
    return f"{x * 100:.{d}f}%".replace(".", ",")


def it(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def sg(x):
    return "+" if x >= 0 else ""


def stampa(r):
    print(f"== {r['partita']} · modello v{r['versione_modello']} ==")
    gd_, gm_ = r["gol_attesi_dati"], r["gol_attesi_mercato"]
    print(f"Gol attesi dai dati: casa {it(gd_['casa'])} · trasferta {it(gd_['trasferta'])}")
    if gm_:
        print(f"Gol attesi impliciti nelle quote: casa {it(gm_['casa'])} · trasferta {it(gm_['trasferta'])}")
    print(f"Gol attesi finali ({r['metodo_stima']}): casa {it(r['gol_attesi']['casa'])} · trasferta {it(r['gol_attesi']['trasferta'])}")
    if r["correzioni"]:
        print("Correzioni applicate: " + "; ".join(r["correzioni"]))
    gd = r["gate_dati"]
    print("Dati minimi: " + ("OK" if gd["ok"] else "NON SUFFICIENTI -> " + "; ".join(gd["motivi"])))
    bd = r["base_dati"]
    print(f"Solo dati: 1 {pc(bd['1'])} · X {pc(bd['X'])} · 2 {pc(bd['2'])} · Over 2,5 {pc(bd['Over 2,5'])} · Gol {pc(bd['Gol'])}")
    b = r["base"]
    print(f"Stima finale: 1 {pc(b['1'])} · X {pc(b['X'])} · 2 {pc(b['2'])} · Over 2,5 {pc(b['Over 2,5'])} · Gol {pc(b['Gol'])}")
    print("Risultati più probabili: " + " · ".join(f"{s} {pc(p)}" for s, p in r["punteggi_top"]))
    t = r["tempi"]
    nota = "dati per tempo reali" if t["dati_per_tempo_reali"] else "ripartizione media di lega, solo indicativo"
    print(f"GG 1T {pc(t['GG 1T'])} · GG 2T {pc(t['GG 2T'])} · GG 1T + GG 2T {pc(t['GG 1T + GG 2T'])} ({nota})")

    if r["valutazioni"]:
        print(f"\n-- Quote ({r['tipo_quota']}) --")
        con_rif = any(v["prob_riferimento"] for v in r["valutazioni"])
        extra = f"{'p rif.':>9}{'v.prezzo':>10}" if con_rif else ""
        print(f"{'mercato':<28}{'quota':>7}{'p stima':>11}{'p mercato':>11}{'valore':>9}{'q.min':>7}{extra}  stato")
        for v in sorted(r["valutazioni"], key=lambda v: v["valore"], reverse=True):
            ex = ""
            if con_rif:
                ex = (f"{pc(v['prob_riferimento']):>9}{sg(v['valore_prezzo'])}{pc(v['valore_prezzo']):>9}"
                      if v["prob_riferimento"] else f"{'-':>9}{'-':>10}")
            print(f"{v['mercato']:<28}{it(v['quota']):>7}{pc(v['prob_modello']):>11}{pc(v['prob_mercato']):>11}"
                  f"{sg(v['valore'])}{pc(v['valore']):>8}{it(v['quota_minima']):>7}{ex}  {v['stato']}")
        if r["fonte_riferimento"]:
            print(f"Riferimento: {r['fonte_riferimento']} (senza margine). v.prezzo = quota Eurobet contro la probabilità del riferimento.")
        metodi = sorted({v["metodo_margine"] for v in r["valutazioni"]})
        print("Margine: " + "; ".join(metodi))

    if r["disaccordo_1x2"]:
        print(f"\nATTENZIONE: i dati della stagione e il mercato sono in forte disaccordo sull'1X2 ({r['disaccordo_1x2']}). Probabile informazione che i dati non contengono: nessuna giocata su questa partita.")

    print("\n-- Podio --")
    if r["podio"]:
        for i, v in enumerate(r["podio"], 1):
            vp = f" · valore di prezzo {sg(v['valore_prezzo'])}{pc(v['valore_prezzo'])}" if v["valore_prezzo"] is not None else ""
            print(f"{i}° {v['mercato']} @ {it(v['quota'])} · {pc(v['prob_modello'])} · valore {sg(v['valore'])}{pc(v['valore'])}{vp} · {v['stato'].split('(')[1].rstrip(')')}")
    else:
        if r["tipo_quota"].lower() == "indicativa" or not r["valutazioni"]:
            motivo = "nessuna quota reale"
        elif not r["gate_dati"]["ok"]:
            motivo = "dati insufficienti"
        elif r["disaccordo_1x2"]:
            motivo = "dati in forte disaccordo col mercato"
        else:
            motivo = "nessun mercato supera la soglia di valore senza anomalie"
        print(f"NO BET ({motivo})")

    s = r["sicura_multipla"]
    if s:
        if s.get("quota"):
            print(f"\nSICURA per la multipla: {s['mercato']} @ {it(s['quota'])} · {pc(s['prob_modello'])} · valore {sg(s['valore'])}{pc(s['valore'])}")
        else:
            print(f"\nSICURA per la multipla (da quotare): {s['mercato']} · {pc(s['prob_modello'])} · quota equa {it(s['quota_equa'])}")

    top = sorted(r["da_quotare"], key=lambda v: v["prob_modello"], reverse=True)
    if top:
        print("\n-- Mercati non quotati: giocabili solo se la quota è almeno la quota minima --")
        for v in top[:15]:
            print(f"{v['mercato']:<28}{pc(v['prob_modello']):>8}  quota equa {it(v['quota_equa']):>6}  quota minima {it(v['quota_minima']):>6}")


ESEMPIO = {
    "partita": "Napoli - Torino",
    "lega": {"media_gol_casa": 1.60, "media_gol_trasferta": 1.51},
    "casa": {"partite": 6, "gol_fatti": 10, "gol_subiti": 6, "xg": None, "xga": None, "quota_gol_1t": None},
    "trasferta": {"partite": 5, "gol_fatti": 7, "gol_subiti": 6, "xg": None, "xga": None, "quota_gol_1t": None},
    "assenze_verificate": True,
    "correzioni": [{"squadra": "casa", "codice": "ASSENZA_BOMBER"}],
    "tipo_quota": "Eurobet",
    "quote": {"1": 1.60, "X": 3.90, "2": 5.50, "1X": 1.15, "X2": 2.35, "Over 1,5": 1.28, "Under 1,5": 3.50,
              "Over 2,5": 1.85, "Under 2,5": 1.90, "Gol": 1.95, "No Gol": 1.80},
}


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    if argv[0] == "--esempio":
        print(json.dumps(ESEMPIO, indent=2, ensure_ascii=False))
        return 0
    with open(argv[0], encoding="utf-8") as f:
        d = json.load(f)
    r = analizza(d)
    if "--json" in argv:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        stampa(r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
