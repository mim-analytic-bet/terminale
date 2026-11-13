#!/usr/bin/env python3
"""Champions League in MODALITA' OSSERVAZIONE: elabora partite future con il modello Elo europeo (coppe_modello.py),
tiene la memoria delle previsioni (dati/coppe/previsioni_CL.csv) e misura il track record vero (solo previsioni fatte PRIMA del calcio d'inizio).
Nessun dato inventato: squadre senza rating affidabile vengono escluse e segnalate."""
import csv, difflib, json, math, os, re, unicodedata, datetime as dt
import coppe_modello as CM

BASE = CM.BASE
D = os.path.join(BASE, "dati", "coppe")
NOMI = {"cl": "Champions", "el": "Europa League"}
def percorsi(comp):
    c = comp.upper()
    return (os.path.join(D, f"{c}_live.json"), os.path.join(D, f"previsioni_{c}.csv"), os.path.join(D, "memoria_coppe.json" if comp == "cl" else f"memoria_coppe_{c}.json"))
CAMPI = ["id", "data", "ora", "casa", "ospite", "rh", "ra", "trend_h", "trend_a", "w_dom", "p1", "pX", "p2", "lh", "la", "e1", "eX", "e2", "retro", "stato", "gc", "go"]
STAGE = {"LEAGUE_STAGE": None, "PLAYOFFS": (9, "Spareggi"), "LAST_16": (10, "Ottavi"), "QUARTER_FINALS": (11, "Quarti"), "SEMI_FINALS": (12, "Semifinali"), "FINAL": (13, "Finale")}
W_DOM0, W_DOM_MAX, CAP_AGG = 0.25, 1.0, 40.0
TOKEN = {"fc", "cf", "ac", "as", "sc", "sk", "fk", "bk", "afc", "sv", "ssc", "sl", "kv", "ks", "cd", "us", "rc", "ud", "pae", "nk", "the", "de", "da", "do", "del", "club", "sporting", "calcio", "clube", "futebol", "04", "05", "1846", "1899", "1909"}
ALIAS = {"paris saint germain": "paris sg", "internazionale milano": "inter", "club atletico madrid": "ath madrid", "atletico madrid": "ath madrid", "bayern munchen": "bayern munich",
         "borussia dortmund": "dortmund", "bayer leverkusen": "leverkusen", "manchester city": "man city", "manchester united": "man united", "tottenham hotspur": "tottenham",
         "newcastle united": "newcastle", "athletic club": "ath bilbao", "eintracht frankfurt": "ein frankfurt", "olympique marseille": "marseille", "olympique lyonnais": "lyon",
         "ac milan": "milan", "borussia monchengladbach": "m gladbach", "real sociedad": "sociedad", "rb leipzig": "rb leipzig", "ssc napoli": "napoli", "as monaco": "monaco",
         "atalanta bc": "atalanta", "ac fiorentina": "fiorentina", "aston villa": "aston villa", "nottingham forest": "nott m forest", "rayo vallecano": "vallecano", "real betis": "betis", "como 1907": "como"}


ALIAS_EU = {"lask linz": "lask", "aek": "aek athen", "olympiacos": "olympiakos piraeus", "sparta prague": "sparta praha"}
NUOVI_EU = {"celta vigo", "lillestrom"}  # club senza storico europeo recente nel dataset (confermati a mano)


def norm(x):
    x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower().replace("&", " ")
    x = re.sub(r"[^a-z0-9 ]", " ", x)
    return " ".join(w for w in x.split() if w not in TOKEN) or x.strip()


def abbina(nome, candidati, soglia=0.86, alias=None):
    """Restituisce il candidato piu' simile (o None). Esatto dopo normalizzazione, poi alias, poi similarita'."""
    n = norm(nome); n = (alias or {}).get(n, n); mappa = {}
    for c in candidati: mappa.setdefault(norm(c), c)
    if n in mappa: return mappa[n]
    for k, c in mappa.items():
        if len(n) >= 5 and (n in k or k in n) and min(len(n), len(k)) >= 5: return c
    best = max(mappa, key=lambda k: difflib.SequenceMatcher(None, n, k).ratio(), default=None)
    if best and difflib.SequenceMatcher(None, n, best).ratio() >= soglia: return mappa[best]
    return None


def risultato90(m):
    sc = m.get("score") or {}; reg = sc.get("regularTime") or {}
    if reg.get("home") is not None: return reg["home"], reg["away"]
    if sc.get("duration") == "REGULAR" and (sc.get("fullTime") or {}).get("home") is not None: return sc["fullTime"]["home"], sc["fullTime"]["away"]
    return None


def carica_log(LOG):
    try: return {r["id"]: r for r in csv.DictReader(open(LOG, encoding="utf-8"))}
    except Exception: return {}


def salva_log(log, LOG):
    os.makedirs(D, exist_ok=True)
    with open(LOG, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, CAMPI); w.writeheader()
        for k in sorted(log, key=lambda k: (log[k]["data"], k)): w.writerow({c: log[k].get(c, "") for c in CAMPI})


def carica_mem(MEM):
    try: return json.load(open(MEM, encoding="utf-8"))
    except Exception: return {"w_dom": W_DOM0, "storia_w": []}


def probs(rh, ra, neutro, P, agg_h=0.0, agg_a=0.0):
    lh, la = CM.gol_attesi(rh, ra, neutro, P, agg_h, agg_a); M = CM.matrice(lh, la, P["rho"]); return lh, la, M


def brier(p, o): return sum((p[i] - o[i]) ** 2 for i in range(3))


def esito(gc, go): return (1, 0, 0) if gc > go else (0, 1, 0) if gc == go else (0, 0, 1)


def adatta_w(log, P, mem, avvisi):
    """Ricalibra il peso della forma nazionale SOLO sulle previsioni vere (non retroattive) concluse. Serve almeno 40 partite."""
    righe = [r for r in log.values() if r.get("retro") == "0" and r.get("gc") not in ("", None)]
    if len(righe) < 40: return mem["w_dom"], len(righe)
    def costo(w):
        t = 0.0
        for r in righe:
            rh, ra = float(r["rh"]), float(r["ra"]); ag = lambda tr: max(-CAP_AGG, min(CAP_AGG, w * 100 * float(tr or 0)))
            _, _, M = probs(rh, ra, 0, P, ag(r["trend_h"]), ag(r["trend_a"])); t += brier(CM.esiti(M), esito(int(r["gc"]), int(r["go"])))
        return t / len(righe) + 0.02 * (w - W_DOM0) ** 2
    w = min([i / 10 for i in range(0, int(W_DOM_MAX * 10) + 1)], key=costo)
    if abs(w - mem["w_dom"]) > 1e-9:
        mem["storia_w"] = (mem.get("storia_w") or [])[-9:] + [{"data": dt.date.today().isoformat(), "w": w, "n": len(righe)}]
    return w, len(righe)


def elabora(oggi, forma_naz=None, avvisi=None, comp="cl"):
    """Ritorna {"turni": {...}, "track": {...}} oppure None. forma_naz(nome_api) -> {"trend":float,"summary5":str,"xgd5":float,"campionato":str,"csv":str} o None."""
    avvisi = avvisi if avvisi is not None else []; NOME = NOMI[comp]; LIVE, LOG, MEM = percorsi(comp)
    if not os.path.exists(LIVE): avvisi.append(f"{NOME}: dati live non ancora scaricati (serve la chiave API della fonte)"); return None
    live = json.load(open(LIVE, encoding="utf-8")); partite = live["matches"]
    storico = CM.leggi_storico(); note = {m["casa"] for m in storico} | {m["ospite"] for m in storico}
    mem = carica_mem(MEM); P = dict(CM.PARAMS0); log = carica_log(LOG); w_dom, n_real = adatta_w(log, P, mem, avvisi); mem["w_dom"] = w_dom
    # 1) risultati live conclusi -> aggiorno rating in ordine cronologico (memoria del modello)
    mappa_nome = {}
    nuovi = set()
    def nome_storico(n):
        if n not in mappa_nome:
            c = abbina(n, note, alias=ALIAS_EU)
            if c is None and norm(n) in NUOVI_EU: c = n; nuovi.add(n)
            if c is None:  # nessuna somiglianza con nessuno storico: club mai visto in Europa -> rating iniziale, segnalato (non inventato)
                k = norm(n)
                if max((difflib.SequenceMatcher(None, k, norm(x)).ratio() for x in note), default=0) < 0.6: c = n; nuovi.add(n)
            mappa_nome[n] = c
        return mappa_nome[n]
    fin, future, scartate = [], [], set()
    for m in partite:
        t = m.get("homeTeam", {}).get("name"), m.get("awayTeam", {}).get("name")
        if not all(t): continue
        d = dt.datetime.fromisoformat(m["utcDate"].replace("Z", "+00:00"))
        (fin if m.get("status") == "FINISHED" else future).append((d, m, t))
    st = CM.Stato(P)
    for m in storico: st.aggiorna(m)
    cutoff_storico = max(m["data"] for m in storico)
    eu = {}  # rendimento europeo della stagione: nome_storico -> [V,N,P,GF,GS]
    for d, m, t in sorted(fin, key=lambda x: x[0]):
        if d.date() <= cutoff_storico: continue  # gia' nello storico openfootball
        r90 = risultato90(m); a, b = nome_storico(t[0]), nome_storico(t[1])
        if r90 is None or not a or not b:
            if not (a and b): scartate.update(x for x, y in zip(t, (a, b)) if not y)
            continue
        mm = {"data": d.date(), "comp": comp, "casa": a, "ospite": b, "gc": r90[0], "go": r90[1], "neutro": 1 if m.get("stage") == "FINAL" else 0}
        st.inizio_stagione(mm["data"]); rh, ra = st.rating(a), st.rating(b); (p1, px, p2), (lh, la) = st.aggiorna(mm)
        k = str(m["id"]); riga = log.get(k)
        o = esito(*r90)
        if riga is None:  # mai prevista prima del calcio d'inizio: ricostruzione, non conta come previsione vera
            log[k] = {"id": k, "data": d.date().isoformat(), "ora": d.astimezone(dt.timezone(dt.timedelta(hours=1))).strftime("%H:%M"), "casa": a, "ospite": b, "rh": f"{rh:.1f}", "ra": f"{ra:.1f}",
                      "trend_h": "", "trend_a": "", "w_dom": "", "p1": f"{p1:.4f}", "pX": f"{px:.4f}", "p2": f"{p2:.4f}", "lh": f"{lh:.3f}", "la": f"{la:.3f}",
                      "e1": f"{p1:.4f}", "eX": f"{px:.4f}", "e2": f"{p2:.4f}", "retro": "1", "stato": "FINISHED", "gc": str(r90[0]), "go": str(r90[1])}
        else:
            riga["stato"] = "FINISHED"; riga["gc"], riga["go"] = str(r90[0]), str(r90[1])
        for sq, gf, gs in ((a, r90[0], r90[1]), (b, r90[1], r90[0])):
            e = eu.setdefault(sq, [0, 0, 0, 0, 0]); e[0 if gf > gs else 1 if gf == gs else 2] += 1; e[3] += gf; e[4] += gs
    # 2) partite future: previsione con stato aggiornato (+ forma nazionale)
    st.inizio_stagione(oggi)  # applica il ritorno verso la media della nuova stagione anche se non ci sono ancora partite giocate
    in_cl = {nome_storico(x) for _, mm_, tt in fin + future for x in tt} - {None}
    ranking = sorted(((st.rating(t), t) for t in in_cl), reverse=True)
    posiz = {t: i + 1 for i, (r, t) in enumerate(ranking)}
    turni = {}
    for d, m, t in sorted(future, key=lambda x: x[0]):
        if m.get("status") in ("POSTPONED", "CANCELLED", "SUSPENDED"): continue
        a, b = nome_storico(t[0]), nome_storico(t[1])
        if not (a and b): scartate.update(x for x, y in zip(t, (a, b)) if not y); continue
        dn = [forma_naz(x) if forma_naz else None for x in t]
        trh, tra = (dn[0] or {}).get("trend"), (dn[1] or {}).get("trend")
        ag = lambda tr: max(-CAP_AGG, min(CAP_AGG, w_dom * 100 * tr)) if tr is not None else 0.0
        neutro = 1 if m.get("stage") == "FINAL" else 0
        rh, ra = st.rating(a), st.rating(b)
        lh, la, M = probs(rh, ra, neutro, P, ag(trh), ag(tra)); p1, px, p2 = CM.esiti(M)
        _, _, M0 = probs(rh, ra, neutro, P); e1, ex, e2 = CM.esiti(M0)
        giorno = d.astimezone(dt.timezone(dt.timedelta(hours=1)))  # ora italiana (CET); +1h in estate gestita dal fuso sotto
        try:
            from zoneinfo import ZoneInfo; giorno = d.astimezone(ZoneInfo("Europe/Rome"))
        except Exception: pass
        ora = giorno.strftime("%H:%M") if m.get("status") == "TIMED" else None
        stg = STAGE.get(m.get("stage")); tk, lbl = (m.get("matchday") or 0, f"Giornata {m.get('matchday')}") if stg is None else stg
        if not tk: continue
        rec = {"turno": tk, "etichetta": lbl, "giorno": giorno.date().isoformat(), "ora": ora, "casa_api": t[0], "ospite_api": t[1], "casa": a, "ospite": b, "id": str(m["id"]),
               "rh": rh, "ra": ra, "agg_h": ag(trh), "agg_a": ag(tra), "neutro": neutro, "p": (p1, px, p2), "p_elo": (e1, ex, e2), "lh": lh, "la": la, "M": M,
               "pos_h": posiz.get(a), "pos_a": posiz.get(b), "eu_h": eu.get(a), "eu_a": eu.get(b), "naz_h": dn[0], "naz_a": dn[1], "w_dom": w_dom,
               "nuovi": (a in nuovi, b in nuovi), "ritorno": bool(stg and tk in (10, 11, 12)), "sn_h": m["homeTeam"].get("shortName") or t[0], "sn_a": m["awayTeam"].get("shortName") or t[1]}
        turni.setdefault(tk, {"etichetta": lbl, "partite": []})["partite"].append(rec)
        k = rec["id"]; riga = log.get(k)
        if giorno.astimezone(dt.timezone.utc) > dt.datetime.now(dt.timezone.utc) and (riga is None or riga.get("retro") == "0" or riga.get("stato") != "FINISHED"):
            log[k] = {"id": k, "data": giorno.date().isoformat(), "ora": ora or "", "casa": a, "ospite": b, "rh": f"{rh:.1f}", "ra": f"{ra:.1f}", "trend_h": "" if trh is None else f"{trh:.3f}",
                      "trend_a": "" if tra is None else f"{tra:.3f}", "w_dom": f"{w_dom:.2f}", "p1": f"{p1:.4f}", "pX": f"{px:.4f}", "p2": f"{p2:.4f}", "lh": f"{lh:.3f}", "la": f"{la:.3f}",
                      "e1": f"{e1:.4f}", "eX": f"{ex:.4f}", "e2": f"{e2:.4f}", "retro": "0", "stato": "SCHEDULED", "gc": "", "go": ""}
    if scartate: avvisi.append(NOME + ": rating non affidabile (nome squadra non riconosciuto), partite escluse per: " + ", ".join(sorted(scartate)))
    # 3) track record vero (solo previsioni fatte prima del calcio d'inizio) vs Elo puro vs frequenze di base
    bt = json.load(open(os.path.join(D, "backtest.json"), encoding="utf-8")); base = bt["frequenze_base_1X2"]
    def metr(rs, ch):
        n = len(rs); 
        if not n: return {"n": 0}
        b = sum(brier([float(r[c]) for c in ch], esito(int(r["gc"]), int(r["go"]))) for r in rs) / n
        bb = sum(brier(base, esito(int(r["gc"]), int(r["go"]))) for r in rs) / n
        hit = sum(max(range(3), key=lambda i: float(r[ch[i]])) == esito(int(r["gc"]), int(r["go"])).index(1) for r in rs) / n
        return {"n": n, "brier": round(b, 4), "brier_base": round(bb, 4), "hit": round(hit * 100)}
    chiuse = [r for r in log.values() if r.get("gc") not in ("", None)]
    reali = [r for r in chiuse if r.get("retro") == "0"]; retro = [r for r in chiuse if r.get("retro") == "1"]
    track = {"reali": metr(reali, ("p1", "pX", "p2")), "reali_elo_puro": metr(reali, ("e1", "eX", "e2")), "retro": metr(retro, ("p1", "pX", "p2")),
             "backtest": {k: bt[k] for k in ("n_test", "brier_modello", "brier_frequenze_base", "hit_1x2", "test_da")}, "w_dom": w_dom, "aperte": sum(1 for r in log.values() if r.get("gc") in ("", None)),
             "aggiornato": dt.datetime.now().strftime("%d/%m/%Y %H:%M")}
    salva_log(log, LOG); mem["aggiornato"] = track["aggiornato"]; json.dump(mem, open(MEM, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return {"turni": turni, "track": track, "ratings_n": len(ranking)}
