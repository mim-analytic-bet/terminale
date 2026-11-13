#!/usr/bin/env python3
"""Ricostruisce i 4 campionati esteri della dashboard SOLO da dati reali.
Fonti: dati/E0|SP1|D1|F1.csv (risultati+xG), dati/fixtures.csv (quote, se la partita c'e'),
dati/calendario.json (abbinamenti ufficiali). Nessun testo scritto a mano, nessuna quota inventata.
Uso:  python3 scripts/aggiorna_dashboard.py            (dalla cartella scommesse)
"""
import csv, json, os, sys, shutil, re, datetime as dt, hashlib
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "analisi-scommesse-calcio", "scripts"))
sys.path.insert(0, os.path.join(BASE, "scripts"))
import prepara_partita as pp
import modello as mod
import track_record as TR
import apprendimento as AP
import colori_squadre as CS
W_APP = 1.0
RAW = {}
COLORI = {}
NEUTRO = ["#1e3a5f", "#334155"]
NUOVI_LOGHI = {"Leeds": "leeds", "Sunderland": "sunderland", "Hull": "hull_city", "Coventry": "coventry_city", "Elche": "elche", "Levante": "levante",
    "Deportivo": "deportivo", "Racing Santander": "racing_santander", "Málaga": "malaga", "Elversberg": "elversberg", "Paderborn": "paderborn",
    "Amburgo": "hamburger_sv", "Colonia": "koln", "Schalke 04": "schalke_04", "Troyes": "troyes", "Paris FC": "paris_fc", "Le Mans": "le_mans", "Lorient": "lorient",
    "Atlético Madrid": "atletico_madrid", "Athletic Club": "athletic_bilbao", "Betis": "real_betis", "Celta": "celta_vigo", "Alavés": "alaves",
    "Bayern Monaco": "bayern_munchen", "Eintracht Francoforte": "eintracht_frankfurt", "Mönchengladbach": "borussia_monchengladbach",
    "Werder Brema": "werder_bremen", "Stoccarda": "stuttgart", "Magonza": "mainz", "Lione": "lyon", "Marsiglia": "marseille"}

HTML = os.path.join(BASE, "scheda-partita-dashboard.html")
LEGHE = {"serie-a": "I1", "premier": "E0", "liga": "SP1", "bundesliga": "D1", "ligue1": "F1"}
NOMI = {  # nome CSV -> nome mostrato
 "Man City": "Manchester City", "Man United": "Manchester United", "Nott'm Forest": "Nottingham Forest",
 "Ath Madrid": "Atlético Madrid", "Ath Bilbao": "Athletic Club", "Sociedad": "Real Sociedad", "Espanol": "Espanyol",
 "Vallecano": "Rayo Vallecano", "La Coruna": "Deportivo", "Santander": "Racing Santander", "Alaves": "Alavés", "Malaga": "Málaga",
 "Bayern Munich": "Bayern Monaco", "FC Koln": "Colonia", "Ein Frankfurt": "Eintracht Francoforte", "M'gladbach": "Mönchengladbach",
 "Werder Bremen": "Werder Brema", "Dortmund": "Borussia Dortmund", "Leverkusen": "Bayer Leverkusen", "Stuttgart": "Stoccarda",
 "Paris SG": "Paris Saint-Germain", "Marseille": "Marsiglia", "Lyon": "Lione", "Hamburg": "Amburgo", "Mainz": "Magonza",
}
GIORNI = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
MESI = ["", "Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
PAL = ["sky", "rose", "amber", "emerald", "violet", "cyan", "orange", "indigo", "teal", "fuchsia"]

def nome(x): return NOMI.get(x, x)

def coppia(cols):
    """Due colori per lo sfondo: se il secondo e' bianco/grigio/nero lo sostituisce con una tinta chiara del primo (niente riflessi grigi)."""
    import colorsys
    c1 = cols[0]; c2 = cols[1] if len(cols) > 1 else cols[0]
    def hsv(h): return colorsys.rgb_to_hsv(*(int(h[i:i+2], 16) / 255 for i in (1, 3, 5)))
    def hx(r, g_, b): return "#%02x%02x%02x" % (round(r*255), round(g_*255), round(b*255))
    h1, s1, v1 = hsv(c1); h2, s2, v2 = hsv(c2)
    if s1 < 0.2:                                   # primo colore grigio/bianco (es. Juventus): usa un azzurro freddo neutro
        c1 = "#5b6b8c"; h1, s1, v1 = hsv(c1)
    if s2 < 0.2 or v2 < 0.22:
        c2 = hx(*colorsys.hsv_to_rgb(h1, max(0.35, s1 * 0.55), min(1.0, v1 + 0.28)))
    return [c1, c2]
def sigla(x): return "".join(c for c in nome(x) if c.isalpha()).upper()[:3]
def colore(x):
    c = PAL[int(hashlib.md5(x.encode()).hexdigest(), 16) % len(PAL)]
    return f"bg-{c}-500/20 text-{c}-400 border-{c}-400"

def classifica(partite):
    t = {}
    for p in partite:
        for sq, gf, gs in ((p["casa"], p["gc"], p["go"]), (p["ospite"], p["go"], p["gc"])):
            r = t.setdefault(sq, [0, 0, 0, 0])
            r[0] += 3 if gf > gs else 1 if gf == gs else 0; r[1] += gf - gs; r[2] += gf; r[3] += gs
    ordine = sorted(t, key=lambda s: (-t[s][0], -t[s][1], -t[s][2]))
    return {s: (i + 1, t[s]) for i, s in enumerate(ordine)}

def forma(partite, sq):
    mie = sorted([p for p in partite if sq in (p["casa"], p["ospite"])], key=lambda p: p["data"])
    def riga(p):
        c = p["casa"] == sq
        gf, gs = (p["gc"], p["go"]) if c else (p["go"], p["gc"])
        xf, xs = (p["xgc"], p["xgo"]) if c else (p["xgo"], p["xgc"])
        xf = xf if xf is not None else 0.0; xs = xs if xs is not None else 0.0
        return {"opp": nome(p["ospite"] if c else p["casa"]), "gf": gf, "gs": gs,
                "res": "V" if gf > gs else "N" if gf == gs else "P", "xg_f": round(xf, 2), "xg_s": round(xs, 2),
                "xg_diff": round(xf - xs, 2), "home": c, "date": p["data"].strftime("%d/%m/%Y")}
    tutte = [riga(p) for p in mie]; l5 = tutte[-5:]
    v = sum(r["res"] == "V" for r in tutte); n = sum(r["res"] == "N" for r in tutte); pr = sum(r["res"] == "P" for r in tutte)
    d5 = round(sum(r["xg_diff"] for r in l5), 2); N = len(tutte)
    tr = (f"Creazione offensiva dominante ({d5:+.2f} xG diff)" if d5 > 1 else
          f"Squadra in difficoltà sotto porta/difesa ({d5:+.2f} xG diff)" if d5 < -1 else f"Equilibrio xG ({d5:+.2f} xG diff)")
    return {"last5": l5, "summary5": f"{sum(r['res']=='V' for r in l5)}V {sum(r['res']=='N' for r in l5)}N {sum(r['res']=='P' for r in l5)}P",
            "tot_xg_diff_5": d5, "trend_desc": tr, "tot_partite": N, "v": v, "n": n, "p": pr,
            "gf": sum(r["gf"] for r in tutte), "gs": sum(r["gs"] for r in tutte),
            "xg_f_avg": round(sum(r["xg_f"] for r in tutte) / N, 2), "xg_s_avg": round(sum(r["xg_s"] for r in tutte) / N, 2),
            "cs_perc": round(100 * sum(r["gs"] == 0 for r in tutte) / N), "bts_perc": round(100 * sum(r["gf"] > 0 and r["gs"] > 0 for r in tutte) / N)}

def scegli(mercati, lo, hi, escludi=()):
    c = [m for m in mercati if lo <= m["prob_modello"] <= hi and "Over 0,5" not in m["mercato"]]
    return sorted(c, key=lambda m: -m["prob_modello"])

def heat(g, k=4):
    """Griglia per la heatmap, presa dalla STESSA matrice del modello (0..10 gol, normalizzata): celle 0..k esatte e colonna/riga 'k+' che somma la coda,
    cosi' le probabilita' sommano al 100% e coincidono con 1X2/Over/Gol mostrati. 'top' = i 3 punteggi piu' probabili sull'intera matrice."""
    n = len(g); tot = sum(map(sum, g))
    def b(i): return min(i, k)
    c = [[0.0] * (k + 1) for _ in range(k + 1)]
    for i in range(n):
        for j in range(n): c[b(i)][b(j)] += g[i][j] / tot
    top = sorted(((g[i][j] / tot, i, j) for i in range(n) for j in range(n)), reverse=True)[:3]
    return {"k": k, "c": [[round(x, 5) for x in r] for r in c], "top": [[i, j, round(p, 5)] for p, i, j in top]}


def pron(m, tipo, icona, bc, br, desc, alt=None):
    p = round(m["prob_modello"] * 100)
    return {"tipo": tipo, "icona": icona, "mercato": m["mercato"], "alt": alt or "-", "prob": p, "probStr": f"{p}%",
            "quota": f"{m['quota_equa']:.2f}", "qEqua": f"{m['quota_equa']:.2f}", "badgeCol": bc, "barCol": br,
            "desc": f"{desc} Quota equa {m['quota_equa']:.2f}: gioca solo se il bookmaker paga almeno {m['quota_minima']:.2f}."}

# ---- assenze/orari da API-Football (dati/assenze.json, scritto da scripts/assenze.py) ----
import difflib, unicodedata
def _norm(x):
    x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower()
    x = re.sub(r"[^a-z0-9 ]", " ", x)
    return " ".join(w for w in x.split() if w not in ("fc", "afc", "cf", "ac", "as", "ssc", "sc", "us", "calcio", "club", "de", "1", "04", "05", "fsv", "sv", "rc", "ud", "cd", "rcd", "ca"))
_ALIAS = {"man utd": "manchester united", "man united": "manchester united", "man city": "manchester city", "nott m forest": "nottingham forest", "ath madrid": "atletico madrid",
          "ath bilbao": "athletic club", "sociedad": "real sociedad", "espanol": "espanyol", "milan": "ac milan", "inter": "inter", "paris sg": "paris saint germain",
          "m gladbach": "borussia monchengladbach", "dortmund": "borussia dortmund", "leverkusen": "bayer leverkusen", "ein frankfurt": "eintracht frankfurt", "st pauli": "st pauli",
          "betis": "real betis", "celta": "celta vigo", "vallecano": "rayo vallecano", "wolves": "wolverhampton wanderers", "spurs": "tottenham", "newcastle": "newcastle united",
          "west ham": "west ham united", "leeds": "leeds united", "brighton": "brighton hove albion", "stuttgart": "vfb stuttgart", "mainz": "mainz 05", "hoffenheim": "tsg hoffenheim",
          "lyon": "olympique lyonnais", "marseille": "olympique marseille", "monaco": "as monaco", "lille": "lille osc"}
def _sim(a, b):
    a, b = _norm(a), _norm(b); a = _ALIAS.get(a, a)
    if not a or not b: return 0.0
    if a == b or a in b or b in a: return 1.0
    return difflib.SequenceMatcher(None, a, b).ratio()
_ASS = None
def assenze_per(casa, osp, giorno):
    """Restituisce il record API-Football della partita (o None). Abbina i nomi di entrambe le squadre."""
    global _ASS
    if _ASS is None:
        try: _ASS = json.load(open(os.path.join(BASE, "dati", "assenze.json"), encoding="utf-8"))
        except Exception: _ASS = {"partite": []}
        try:  # assenze inserite a mano (ricerca web il giorno prima): hanno la precedenza
            man = json.load(open(os.path.join(BASE, "dati", "assenze_manuali.json"), encoding="utf-8")).get("partite", [])
            _ASS["partite"] = [x for x in _ASS.get("partite", []) if not any(_sim(x["casa"], m["casa"]) >= .8 and _sim(x["ospite"], m["ospite"]) >= .8 and x["giorno"] == m["giorno"] for m in man)] + man
        except Exception: pass
    best, bs = None, 0
    for p in _ASS.get("partite", []):
        if giorno and p.get("giorno") and abs((dt.date.fromisoformat(p["giorno"]) - dt.date.fromisoformat(giorno)).days) > 1: continue
        a, b = _sim(casa, p["casa"]), _sim(osp, p["ospite"])
        if min(a, b) >= 0.6 and a + b > bs: best, bs = p, a + b
    return best
def testo_assenze(rec, casa, osp):
    """Elenco leggibile delle assenze; None se la fonte non ha controllato questa partita."""
    if not rec or rec.get("assenze") is None: return None
    def lato(lista, squadra):
        if not lista: return f"{squadra}: nessuna assenza segnalata"
        voci = []
        for x in lista:
            m = (x.get("motivo") or "").strip(); t = x.get("tipo") or ""
            voci.append(f"{x.get('nome','?')} ({m or 'n.d.'}{', in dubbio' if t == 'Questionable' else ''})")
        return f"{squadra}: " + ", ".join(voci)
    return lato(rec["assenze"]["casa"], nome(casa)) + " | " + lato(rec["assenze"]["ospite"], nome(osp))

def costruisci_partita(lega, cod, partite, cl, e, turno_lbl, fixtures):
    casa, osp = e["casa"], e["ospite"]
    rec_api = assenze_per(casa, osp, e.get("giorno"))
    if rec_api and rec_api.get("ora") and not e.get("ora") and (not e.get("giorno") or e["giorno"] == rec_api["giorno"]):
        e = dict(e, giorno=rec_api["giorno"], ora=rec_api["ora"], nota=None)  # orario ufficiale da API-Football
    d = pp.costruisci(partite, casa, osp)
    d["assenze_verificate"] = False
    rif = None
    try:
        q, fonte, arb = pp.riferimento_da_fixtures(fixtures, casa, osp)
        d["quote_riferimento"] = q; d["fonte_riferimento"] = fonte; rif = (q, fonte)
    except SystemExit:
        pass
    r = mod.analizza(d)
    RAW[(casa, osp)] = (r["gol_attesi"]["casa"], r["gol_attesi"]["trasferta"], d["lega"]["media_gol_casa"], d["lega"]["media_gol_trasferta"])
    r = AP.ricalibra(r, d, W_APP)
    b = r["base"]; p1, px, p2 = b["1"], b["X"], b["2"]; pg = b["Gol"]; po = b["Over 2,5"]
    gc, go = r["gol_attesi"]["casa"], r["gol_attesi"]["trasferta"]
    dq = r["da_quotare"]
    bc = {1: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", 2: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30",
          3: "text-rose-400 bg-rose-500/10 border-rose-500/30", 4: "text-purple-400 bg-purple-500/10 border-purple-500/30"}
    br = {1: "from-emerald-500 to-teal-400", 2: "from-cyan-500 to-blue-500", 3: "from-rose-500 to-amber-500", 4: "from-purple-500 to-indigo-500"}
    triv = ("Over 0,5",)
    a = scegli(dq, 0.74, 0.90, triv); bb = scegli(dq, 0.55, 0.73, triv); c = scegli(dq, 0.30, 0.50, triv)
    pe = {}
    if a: pe["1"] = pron(a[0], "ALTA PROBABILITÀ (BASE)", "🛡️", bc[1], br[1], "Mercato a probabilità più alta secondo il modello.", f"{a[1]['mercato']} ({round(a[1]['prob_modello']*100)}%)" if len(a) > 1 else None)
    if bb: pe["2"] = pron(bb[0], "EQUILIBRATO", "⚡", bc[2], br[2], "Miglior rapporto probabilità/quota del fascio medio.", f"{bb[1]['mercato']} ({round(bb[1]['prob_modello']*100)}%)" if len(bb) > 1 else None)
    if c: pe["3"] = pron(c[0], "PRONOSTICO HARD", "🎯", bc[3], br[3], "Più rischioso, probabilità più bassa.", f"{c[1]['mercato']} ({round(c[1]['prob_modello']*100)}%)" if len(c) > 1 else None)
    s, ps = r["punteggi_top"][0]
    pe["4"] = {"tipo": "PRONOSTICO EXTRA", "icona": "🔮", "mercato": f"Risultato esatto {s}", "alt": f"{r['punteggi_top'][1][0]} ({round(r['punteggi_top'][1][1]*100)}%)",
               "prob": round(ps * 100), "probStr": f"{round(ps*100)}%", "quota": f"{1/ps:.2f}", "qEqua": f"{1/ps:.2f}", "badgeCol": bc[4], "barCol": br[4],
               "desc": "Punteggio più probabile per il modello Dixon-Coles."}
    cc, oc = cl[casa], cl[osp]
    fcs, fos = forma(partite, casa), forma(partite, osp)
    # data
    if e.get("giorno"):
        g = dt.date.fromisoformat(e["giorno"]); data = f"{GIORNI[g.weekday()]} {g.day} {MESI[g.month]}" + (f" · {e['ora']}" if e.get("ora") else " · orario da confermare")
    else:
        data = f"{turno_lbl.get('finestra','')} · giorno e orario da confermare"
    if e.get("nota"): data += " (verificare)"
    mq = None
    if rif:
        q, fonte = rif; mq = dict(q); mq["fonte"] = fonte
    _t1 = pe.get("1") or pe.get("2") or pe.get("3") or pe.get("4") or {}
    _merc = f"Miglior stima del modello: {_t1.get('mercato','n.d.')} ({_t1.get('probStr','n.d.')})"
    _qe = _t1.get("qEqua", "")
    _spieg = (f"Stime del modello — 1: {round(p1*100)}% · X: {round(px*100)}% · 2: {round(p2*100)}% · Gol: {round(pg*100)}% · Over 2.5: {round(po*100)}%. "
              f"Attesa gol (xG modello): {nome(casa)} {gc:.2f} – {nome(osp)} {go:.2f}. "
              + (f"Quota equa {_qe}: giocala solo se il bookmaker paga almeno quel prezzo con margine. " if _qe else "")
              + ((f"Quote di riferimento ({mq['fonte']}): " + " · ".join(f"{k} {mq[k]}" for k in ('1','X','2') if k in mq) + ". ") if mq else "Quote di mercato non disponibili per questa partita. ")
              + "Puntata consigliata 0 € finché non emerge un edge verificato: nei test il modello da solo non batte il mercato, quindi nessuna giocata è forzata.")
    _ta = testo_assenze(rec_api, casa, osp)
    _assenti = None
    if _ta:
        _assenti = {"casa": rec_api["assenze"]["casa"], "ospite": rec_api["assenze"]["ospite"], "controllato": (rec_api.get("controllato") or "")[:16].replace("T", " "),
                    "fonte": rec_api.get("fonte") or "ricerca web"}
        _rischio = "Assenze e squalificati verificati (vedi riquadro). Le formazioni probabili non sono incluse e le assenze NON entrano nel calcolo del modello: controlla le ufficiali prima di giocare."
    else:
        _rischio = "Assenze, squalifiche e formazioni NON verificate: il modello usa solo risultati e xG. Controlla le ufficiali prima di giocare."
    _rischio += "" if mq else " Nessuna quota di mercato disponibile per questa partita nei dati."
    return {
        "id": (sigla(casa) + "-" + sigla(osp)).lower(), "label": f"{nome(casa)} - {nome(osp)}",
        "bgGradient": f"from-[{coppia(COLORI.get(nome(casa), NEUTRO))[0]}] via-[#090d16] to-[{coppia(COLORI.get(nome(osp), NEUTRO))[0]}]",
        "colori": {"casa": coppia(COLORI.get(nome(casa), NEUTRO)), "ospite": coppia(COLORI.get(nome(osp), NEUTRO))},
        "casa": {"sigla": sigla(casa), "nome": nome(casa), "rank": f"{cc[0]}° · {cc[1][0]} pt", "colBox": colore(casa)},
        "ospite": {"sigla": sigla(osp), "nome": nome(osp), "rank": f"{oc[0]}° · {oc[1][0]} pt", "colBox": colore(osp)},
        "data": data, "giornata": f"{lega} · {turno_lbl['giornata']}",
        "golC": f"{gc:.2f}", "golO": f"{go:.2f}", "barC": f"{round(100*gc/(gc+go))}%", "barO": f"{100-round(100*gc/(gc+go))}%",
        "fasi": {
            "1": {"label": "Fase 1: 1X2", "centerVal": f"{round(max(p1,px,p2)*100)}%", "centerLbl": "Segno " + ("1" if p1 >= max(px, p2) else "X" if px >= p2 else "2"),
                  "seg1": {"p": round(p1, 3), "col": "#06b6d4", "nome": f"1: {round(p1*100)}%"}, "seg2": {"p": round(px, 3), "col": "#f59e0b", "nome": f"X: {round(px*100)}%"},
                  "seg3": {"p": round(p2, 3), "col": "#f43f5e", "nome": f"2: {round(p2*100)}%"}},
            "2": {"label": "Fase 2: GG / NG", "centerVal": f"{round(max(pg,1-pg)*100)}%", "centerLbl": "Gol (GG)" if pg >= .5 else "No Gol",
                  "seg1": {"p": round(pg, 3), "col": "#10b981", "nome": f"Gol: {round(pg*100)}%"}, "seg2": {"p": round(1-pg, 3), "col": "#64748b", "nome": f"No Gol: {round((1-pg)*100)}%"},
                  "seg3": {"p": 0.0, "col": "transparent", "nome": ""}},
            "3": {"label": "Fase 3: Under / Over 2.5", "centerVal": f"{round(max(po,1-po)*100)}%", "centerLbl": "Over 2.5" if po >= .5 else "Under 2.5",
                  "seg1": {"p": round(po, 3), "col": "#8b5cf6", "nome": f"Over: {round(po*100)}%"}, "seg2": {"p": round(1-po, 3), "col": "#3b82f6", "nome": f"Under: {round((1-po)*100)}%"},
                  "seg3": {"p": 0.0, "col": "transparent", "nome": ""}},
            "4": {"label": "Fase 4: xG per Squadra", "centerVal": f"{gc:.2f} vs {go:.2f}", "centerLbl": "Volume xG",
                  "seg1": {"p": round(gc/(gc+go), 2), "col": "#0ea5e9", "nome": f"{nome(casa)}: {round(100*gc/(gc+go))}% ({gc:.2f})"},
                  "seg2": {"p": round(go/(gc+go), 2), "col": "#d97706", "nome": f"{nome(osp)}: {round(100*go/(gc+go))}% ({go:.2f})"},
                  "seg3": {"p": 0.0, "col": "transparent", "nome": ""}}},
        "isValore": False, "evBadge": "", "mercato": _merc, "qEqua": _qe, "qReale": "",
        "spiegazione": _spieg, "quoteMercato": mq,
        "analisi": (f"{nome(casa)}: {fcs['summary5']} nelle ultime 5, xG diff {fcs['tot_xg_diff_5']:+.2f}, {fcs['gf']} gol fatti e {fcs['gs']} subiti in {fcs['tot_partite']} gare. "
                    f"{nome(osp)}: {fos['summary5']} nelle ultime 5, xG diff {fos['tot_xg_diff_5']:+.2f}, {fos['gf']} fatti e {fos['gs']} subiti in {fos['tot_partite']}. (Dati football-data.co.uk)"),
        "rischio": _rischio, "assenti": _assenti,
        "heat": heat(mod.griglia(gc, go)), "pronosticiExtra": pe}, fcs, fos

# ---- Champions League in modalita' osservazione (scripts/coppe.py) ----
def _csv_squadre(archivi):
    return {t: (k, pt) for k, pt in archivi.items() for t in {p["casa"] for p in pt} | {p["ospite"] for p in pt}}

def _forma_naz_factory(archivi):
    import coppe as CP
    squadre = _csv_squadre(archivi); nomi_leghe = {"serie-a": "Serie A", "premier": "Premier League", "liga": "LaLiga", "bundesliga": "Bundesliga", "ligue1": "Ligue 1"}
    def f(api_name):
        c = CP.abbina(api_name, list(squadre), soglia=0.88, alias=CP.ALIAS)
        if not c: return None
        k, pt = squadre[c]; fc = forma(pt, c)
        if fc["tot_partite"] < 6: return None
        return {"trend": fc["tot_xg_diff_5"] / 5 - (fc["xg_f_avg"] - fc["xg_s_avg"]), "summary5": fc["summary5"], "xgd5": fc["tot_xg_diff_5"], "campionato": nomi_leghe.get(k, k), "csv": c, "n": fc["tot_partite"]}
    return f, squadre

def _nome_vis(api_name, sn, squadre):
    import coppe as CP
    c = CP.abbina(api_name, list(squadre), soglia=0.88, alias=CP.ALIAS)
    if c: return nome(c)
    return re.sub(r"\s+(FC|CF|SK|FK|AFC)$", "", re.sub(r"^(FC|AFC|SK|FK)\s+", "", sn or api_name)).strip()

def costruisci_partita_coppa(rec, squadre, track, NC="Champions", NL="Champions League"):
    M = rec["M"]; n = len(M); p1, px, p2 = rec["p"]; gc, go = rec["lh"], rec["la"]
    pg = 1 - sum(M[0][j] for j in range(n)) - sum(M[i][0] for i in range(n)) + M[0][0]
    def over(x): return 1 - sum(M[i][j] for i in range(n) for j in range(n) if i + j <= x)
    po = over(2); casa, osp = _nome_vis(rec["casa_api"], rec["sn_h"], squadre), _nome_vis(rec["ospite_api"], rec["sn_a"], squadre)
    cands = [("1", p1), ("X", px), ("2", p2), ("1X", p1 + px), ("X2", px + p2), ("12", p1 + p2), ("Gol", pg), ("No Gol", 1 - pg), ("Over 1,5", over(1)), ("Over 2,5", po),
             ("Over 3,5", over(3)), ("Under 2,5", 1 - po), ("Under 3,5", 1 - over(3))]
    dq = [{"mercato": m_, "prob_modello": p_, "quota_equa": 1 / p_, "quota_minima": 1.03 / p_} for m_, p_ in cands if 0.05 < p_ < 0.97]
    bc = {1: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", 2: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", 3: "text-rose-400 bg-rose-500/10 border-rose-500/30", 4: "text-purple-400 bg-purple-500/10 border-purple-500/30"}
    br = {1: "from-emerald-500 to-teal-400", 2: "from-cyan-500 to-blue-500", 3: "from-rose-500 to-amber-500", 4: "from-purple-500 to-indigo-500"}
    a = scegli(dq, 0.74, 0.90); bb = scegli(dq, 0.55, 0.73); c = scegli(dq, 0.30, 0.50); pe = {}
    alt = lambda l: f"{l[1]['mercato']} ({round(l[1]['prob_modello']*100)}%)" if len(l) > 1 else None
    if a: pe["1"] = pron(a[0], "ALTA PROBABILITÀ (BASE)", "🛡️", bc[1], br[1], "Mercato a probabilità più alta secondo il modello (non validato).", alt(a))
    if bb: pe["2"] = pron(bb[0], "EQUILIBRATO", "⚡", bc[2], br[2], "Fascia media del modello Elo europeo (non validato).", alt(bb))
    if c: pe["3"] = pron(c[0], "PRONOSTICO HARD", "🎯", bc[3], br[3], "Più rischioso, probabilità più bassa.", alt(c))
    flat = sorted(((M[i][j], i, j) for i in range(n) for j in range(n)), reverse=True)[:2]
    pe["4"] = {"tipo": "PRONOSTICO EXTRA", "icona": "🔮", "mercato": f"Risultato esatto {flat[0][1]}-{flat[0][2]}", "alt": f"{flat[1][1]}-{flat[1][2]} ({round(flat[1][0]*100)}%)", "prob": round(flat[0][0] * 100),
               "probStr": f"{round(flat[0][0]*100)}%", "quota": f"{1/flat[0][0]:.2f}", "qEqua": f"{1/flat[0][0]:.2f}", "badgeCol": bc[4], "barCol": br[4], "desc": "Punteggio più probabile (90 minuti)."}
    g = dt.date.fromisoformat(rec["giorno"]); data = f"{GIORNI[g.weekday()]} {g.day} {MESI[g.month]}" + (f" · {rec['ora']}" if rec.get("ora") else " · orario da confermare")
    def riga_eu(e): return f"in {NC} quest'anno {e[0]}V {e[1]}N {e[2]}P, gol {e[3]}-{e[4]}" if e else f"in {NC} quest'anno: nessuna partita giocata"
    def riga_naz(dn): return (f"in {dn['campionato']} {dn['summary5']} nelle ultime 5 (xG diff {dn['xgd5']:+.2f})" if dn else "forma nazionale non disponibile (campionato fuori dai 5 seguiti)")
    analisi = (f"{casa}: Elo europeo {rec['rh']:.0f}" + (f" ({rec['pos_h']}ª tra le squadre in {NC})" if rec.get("pos_h") else "") + f"; {riga_eu(rec['eu_h'])}; {riga_naz(rec['naz_h'])}. "
               f"{osp}: Elo europeo {rec['ra']:.0f}" + (f" ({rec['pos_a']}ª)" if rec.get("pos_a") else "") + f"; {riga_eu(rec['eu_a'])}; {riga_naz(rec['naz_a'])}. "
               + (f"ATTENZIONE: {' e '.join(n for n, f in zip((casa, osp), rec.get('nuovi', (False, False))) if f)} senza storico europeo: rating di partenza standard, affidabilità bassa. " if any(rec.get("nuovi", ())) else "") +
               f"Correzione forma nazionale applicata: {rec['agg_h']:+.0f} / {rec['agg_a']:+.0f} punti Elo (peso {rec['w_dom']:.2f}, ricalibrato sui risultati). (Dati: openfootball, " + ("football-data.org" if NC == "Champions" else "API Ninjas") + ")")
    qe = (pe.get("1") or pe.get("2") or pe.get("3") or pe["4"]); 
    spieg = (f"Stime del modello (90 minuti) — 1: {round(p1*100)}% · X: {round(px*100)}% · 2: {round(p2*100)}% · Gol: {round(pg*100)}% · Over 2.5: {round(po*100)}%. Attesa gol: {casa} {gc:.2f} – {osp} {go:.2f}. "
             f"Quote di mercato non disponibili per le coppe. Puntata consigliata 0 € finché il modello non è validato sulle previsioni reali.")
    ass = assenze_per(rec["casa_api"], rec["ospite_api"], rec["giorno"]); ta = testo_assenze(ass, casa, osp); assenti = None
    rischio = "MODALITÀ OSSERVAZIONE: modello Elo europeo non ancora validato sulle previsioni reali. Assenze, squalifiche e formazioni NON verificate."
    if ta:
        assenti = {"casa": ass["assenze"]["casa"], "ospite": ass["assenze"]["ospite"], "controllato": (ass.get("controllato") or "")[:16].replace("T", " "), "fonte": ass.get("fonte") or "ricerca web"}
        rischio = "MODALITÀ OSSERVAZIONE: modello non validato. Assenze verificate (vedi riquadro); non entrano nel calcolo e le formazioni probabili non sono incluse."
    return {
        "id": (sigla(casa) + "-" + sigla(osp)).lower() + ("-" + rec["id"][-3:]), "label": f"{casa} - {osp}",
        "bgGradient": f"from-[{coppia(COLORI.get(casa, NEUTRO))[0]}] via-[#090d16] to-[{coppia(COLORI.get(osp, NEUTRO))[0]}]",
        "colori": {"casa": coppia(COLORI.get(casa, NEUTRO)), "ospite": coppia(COLORI.get(osp, NEUTRO))},
        "casa": {"sigla": sigla(casa), "nome": casa, "rank": f"Elo {rec['rh']:.0f}" + (f" · {rec['pos_h']}°" if rec.get("pos_h") else ""), "colBox": colore(casa)},
        "ospite": {"sigla": sigla(osp), "nome": osp, "rank": f"Elo {rec['ra']:.0f}" + (f" · {rec['pos_a']}°" if rec.get("pos_a") else ""), "colBox": colore(osp)},
        "data": data, "giornata": f"{NL} · {rec['etichetta']}",
        "golC": f"{gc:.2f}", "golO": f"{go:.2f}", "barC": f"{round(100*gc/(gc+go))}%", "barO": f"{100-round(100*gc/(gc+go))}%",
        "fasi": {
            "1": {"label": "Fase 1: 1X2", "centerVal": f"{round(max(p1,px,p2)*100)}%", "centerLbl": "Segno " + ("1" if p1 >= max(px, p2) else "X" if px >= p2 else "2"),
                  "seg1": {"p": round(p1, 3), "col": "#06b6d4", "nome": f"1: {round(p1*100)}%"}, "seg2": {"p": round(px, 3), "col": "#f59e0b", "nome": f"X: {round(px*100)}%"}, "seg3": {"p": round(p2, 3), "col": "#f43f5e", "nome": f"2: {round(p2*100)}%"}},
            "2": {"label": "Fase 2: GG / NG", "centerVal": f"{round(max(pg,1-pg)*100)}%", "centerLbl": "Gol (GG)" if pg >= .5 else "No Gol",
                  "seg1": {"p": round(pg, 3), "col": "#10b981", "nome": f"Gol: {round(pg*100)}%"}, "seg2": {"p": round(1-pg, 3), "col": "#64748b", "nome": f"No Gol: {round((1-pg)*100)}%"}, "seg3": {"p": 0.0, "col": "transparent", "nome": ""}},
            "3": {"label": "Fase 3: Under / Over 2.5", "centerVal": f"{round(max(po,1-po)*100)}%", "centerLbl": "Over 2.5" if po >= .5 else "Under 2.5",
                  "seg1": {"p": round(po, 3), "col": "#8b5cf6", "nome": f"Over: {round(po*100)}%"}, "seg2": {"p": round(1-po, 3), "col": "#3b82f6", "nome": f"Under: {round((1-po)*100)}%"}, "seg3": {"p": 0.0, "col": "transparent", "nome": ""}},
            "4": {"label": "Fase 4: xG per Squadra", "centerVal": f"{gc:.2f} vs {go:.2f}", "centerLbl": "Gol attesi",
                  "seg1": {"p": round(gc/(gc+go), 2), "col": "#0ea5e9", "nome": f"{casa}: {round(100*gc/(gc+go))}% ({gc:.2f})"}, "seg2": {"p": round(go/(gc+go), 2), "col": "#d97706", "nome": f"{osp}: {round(100*go/(gc+go))}% ({go:.2f})"}, "seg3": {"p": 0.0, "col": "transparent", "nome": ""}}},
        "isValore": False, "evBadge": "", "mercato": f"Miglior stima del modello: {qe['mercato']} ({qe['probStr']})", "qEqua": qe.get("qEqua", ""), "qReale": "", "spiegazione": spieg, "quoteMercato": None,
        "analisi": analisi, "rischio": rischio, "assenti": assenti, "osservazione": track, "heat": heat(M), "pronosticiExtra": pe}

def _slug(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", n).strip("_") or "squadra"


def _distintivo(nome):
    """Distintivo PROVVISORIO (scudo con iniziali) per le squadre senza stemma ufficiale. Ritorna (percorso relativo, [col1, col2])."""
    import colorsys
    h = int(hashlib.md5(nome.encode()).hexdigest()[:6], 16)
    c1 = tuple(int(255 * x) for x in colorsys.hsv_to_rgb((h % 360) / 360, 0.62, 0.62)); c2 = tuple(int(255 * x) for x in colorsys.hsv_to_rgb(((h % 360) + 35) / 360, 0.55, 0.88))
    rel = f"./assets/loghi/prov_{_slug(nome)}.png"; dest = os.path.join(BASE, rel.lstrip("./"))
    if not os.path.exists(dest):
        try:
            from PIL import Image, ImageDraw, ImageFont
            S = 256; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            scudo = [(28, 20), (228, 20), (228, 130), (128, 238), (28, 130)]
            d.polygon(scudo, fill=c1 + (255,)); d.polygon([(46, 38), (210, 38), (210, 124), (128, 214), (46, 124)], fill=c2 + (255,))
            parole = [w for w in re.split(r"[\s\-/]+", nome) if w and not w.isdigit() and w.lower() not in ("fc", "sc", "ac", "as", "sk", "fk", "de", "da", "del", "club", "pae", "nk", "rc")]
            ini = ("".join(w[0] for w in parole[:3]) if len(parole) > 1 else (parole[0][:3] if parole else nome[:3])).upper()
            font = None
            for fp in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"):
                try: font = ImageFont.truetype(fp, 84 if len(ini) < 3 else 68); break
                except Exception: pass
            if font is None:
                try: font = ImageFont.load_default(size=72)
                except Exception: font = ImageFont.load_default()
            d.text((128, 100), ini, fill=(15, 23, 42, 255), font=font, anchor="mm")
            im.save(dest)
        except Exception:
            pass
    return rel, ["#%02x%02x%02x" % c1, "#%02x%02x%02x" % c2]


def assicura_stemmi(pro, loghi, avvisi):
    """Ogni squadra delle coppe DEVE avere uno stemma: 1) PNG manuale assets/loghi/<slug>.png, 2) stemma ufficiale scaricato (dati/stemmi_coppe.json),
    3) distintivo provvisorio generato. Aggiorna loghi e COLORI. Ritorna True se ha aggiunto qualcosa."""
    try: uff = json.load(open(os.path.join(BASE, "dati", "stemmi_coppe.json"), encoding="utf-8"))
    except Exception: uff = {}
    import coppe as CP
    uff_n = {CP.norm(k): v for k, v in uff.items()}
    nomi = sorted({m[k]["nome"] for c in pro.values() for t in c["turni"].values() for m in t["partite"] for k in ("casa", "ospite")} - set(loghi))
    prov = []; agg = False
    for n in nomi:
        man = f"./assets/loghi/{_slug(n)}.png"; u = uff.get(n) or uff_n.get(CP.norm(n))
        if os.path.exists(os.path.join(BASE, man.lstrip("./"))):
            loghi[n] = man
            if n not in COLORI:
                try:
                    c = CS.dominanti(os.path.join(BASE, man.lstrip("./")))
                    if c: COLORI[n] = c
                except Exception: pass
        elif u and os.path.exists(os.path.join(BASE, u["file"].lstrip("./"))):
            loghi[n] = u["file"]
            if u.get("colori"): COLORI[n] = u["colori"]
            elif u["file"].endswith(".png"):
                try: c = CS.dominanti(os.path.join(BASE, u["file"].lstrip("./"))); COLORI[n] = c or COLORI.get(n, NEUTRO)
                except Exception: pass
        else:
            rel, col = _distintivo(n); loghi[n] = rel; COLORI[n] = col; prov.append(n)
        agg = True
    if prov: avvisi.append("Stemma PROVVISORIO (distintivo con iniziali, manca lo stemma ufficiale): " + ", ".join(prov) + " - metti il PNG in assets/loghi/<nome_squadra>.png per sostituirlo")
    return agg


def blocco_coppe(archivi, oggi, avvisi, comp="cl", cache=None):
    """Ritorna il blocco DATA_PRO['champions'] oppure None."""
    import coppe as CP
    f, squadre = _forma_naz_factory(archivi)
    NC = CP.NOMI[comp]; NL = "Champions League" if comp == "cl" else "Europa League"
    if cache is not None and comp in cache: r = cache[comp]
    else:
        r = CP.elabora(oggi, f, avvisi, comp)
        if cache is not None: cache[comp] = r
    if not r or not r["turni"]: return None
    turni = {}
    for tk, t in sorted(r["turni"].items()):
        giorni = sorted(x["giorno"] for x in t["partite"]); d1, d2 = dt.date.fromisoformat(giorni[0]), dt.date.fromisoformat(giorni[-1])
        fin = f"{d1.day}-{d2.day} {MESI[d2.month]}" if d1.month == d2.month else f"{d1.day} {MESI[d1.month]}-{d2.day} {MESI[d2.month]}"
        turni[str(tk)] = {"label": f"{t['etichetta']} ({fin} {d2.year})", "dataFine": giorni[-1] + "T23:59:59", "partite": [costruisci_partita_coppa(x, squadre, r["track"], NC, NL) for x in t["partite"]]}
        if any(not x.get("ora") for x in t["partite"]): avvisi.append(f"{NC}: {t['etichetta']} ha partite con orario da confermare")
    return {"nome": NL, "osservazione": True, "turni": turni, "track": r["track"]}

PANNELLO = r'''<!--/*TRACKPANEL*/--><script>
(function(){try{var T=DATA_TRACK,t=T.totale,L=T.live;
var box=document.createElement('details');box.style.cssText='margin:24px auto 56px;max-width:1100px;padding:0 16px;font:12px ui-monospace,monospace;color:#cbd5e1';
function r(a){return '<tr>'+a.map(function(x){return '<td style="padding:4px 10px;border-bottom:1px solid #1e293b">'+x+'</td>'}).join('')+'</tr>'}
var leg=Object.keys(T.leghe).map(function(k){var x=T.leghe[k];return x.n?r([k,x.n,x.hit_1x2+'%',x.brier_modello,x.brier_mercato,x.value_roi===null?'n.d.':x.value_roi+'% ('+x.value_giocate+')']):''}).join('');
var cal=(t.calibrazione||[]).map(function(c){return r([c.fascia,c.n,c.previsto+'%',c.reale+'%'])}).join('');
var gap=(t.brier_modello-t.brier_mercato);
box.innerHTML='<summary style="cursor:pointer;font-weight:800;text-transform:uppercase;letter-spacing:.05em;color:#fff;padding:10px 0">\ud83d\udcca Track record del modello (onesto)</summary>'+
'<div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:16px;line-height:1.5">'+
'<p style="color:#fbbf24">Backtest su '+t.n+' partite gi\u00e0 giocate, usando solo dati precedenti a ogni partita. Brier (pi\u00f9 basso = meglio): modello solo-dati <b>'+t.brier_modello+'</b> vs mercato <b>'+t.brier_mercato+'</b>. '+
(gap>0?'Il modello \u00e8 PEGGIO del mercato: usalo come filtro e controllo, non come segnale di value.':'Il modello \u00e8 in linea o meglio del mercato.')+'</p>'+
'<table style="width:100%;border-collapse:collapse;margin:10px 0"><tr style="color:#94a3b8"><td style="padding:4px 10px">Campionato</td><td>Partite</td><td>1X2 azzeccati</td><td>Brier modello</td><td>Brier mercato</td><td>ROI regola value (n. giocate)</td></tr>'+leg+'</table>'+
'<table style="width:100%;border-collapse:collapse;margin:10px 0"><tr style="color:#94a3b8"><td style="padding:4px 10px">Fascia probabilit\u00e0</td><td>Casi</td><td>Previsto</td><td>Reale</td></tr>'+cal+'</table>'+
'<p>ROI value (totale): <b>'+(t.value_roi===null?'n.d.':t.value_roi+'%')+'</b> su '+t.value_giocate+' giocate con quote Bet365 di apertura: puntare dove il solo-dati vede valore ha perso denaro. Campione ancora piccolo, ma il segnale \u00e8 negativo.</p>'+
(T.apprendimento&&T.apprendimento.storia.length?'<p style="border-top:1px solid #1e293b;padding-top:8px">Memoria del modello: fiducia nei gol attesi w = <b>'+T.apprendimento.w+'</b> (1 = piena)'+(T.apprendimento.a!==null&&T.apprendimento.a!==undefined?' \u00b7 peso dei dati contro il mercato = <b>'+T.apprendimento.a+'</b> (0 = solo mercato)':'')+'. Si riaddestra ad ogni aggiornamento su backtest + registro live ('+T.apprendimento.storia.length+' ricalibrazioni salvate in dati/memoria_modello.json).</p>':'')+
'<p style="border-top:1px solid #1e293b;padding-top:8px">Registro live (previsioni congelate prima della partita, valutate dopo): <b>'+L.registrate+'</b> registrate, <b>'+L.valutate+'</b> valutate'+(L.valutate?' \u00b7 1X2 azzeccati '+L.hit_1x2+'% \u00b7 Brier '+L.brier:' \u00b7 i primi risultati arrivano dopo la prossima giornata')+'. Aggiornato '+T.aggiornato+'.</p></div>';
(document.querySelector('body > div')||document.body).appendChild(box);}catch(e){}})();
</script>'''

def parsa_blocco(s, nome_const):
    i = s.index(f"const {nome_const} = ") + len(f"const {nome_const} = ")
    j, depth, ins, esc = i, 0, False, False
    while True:
        ch = s[j]
        if ins:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': ins = False
        elif ch == '"': ins = True
        elif ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0: break
        j += 1
    return i, j + 1, json.loads(s[i:j + 1])

def file_dati(cod):
    p = os.path.join(BASE, "dati", cod + ".csv")
    if not os.path.exists(p) and cod == "I1":
        p = os.path.join(BASE, "risultati.csv")
    return p

def turni_automatici(partite, fixtures, oggi):
    """Partite future lette da fixtures.csv (football-data): abbinamenti, data, ora (UK+1h) e quote reali."""
    if not os.path.exists(fixtures): return {}
    giocate = {(p["data"], p["casa"], p["ospite"]) for p in partite}
    squadre = {p["casa"] for p in partite} | {p["ospite"] for p in partite}
    gg = {}
    for p in partite:
        for sq in (p["casa"], p["ospite"]): gg[sq] = gg.get(sq, 0) + 1
    out = {}
    cod = partite[0]["riga"]["Div"]
    for r in csv.DictReader(open(fixtures, encoding="utf-8-sig")):
        if r.get("Div") != cod: continue
        try: d = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
        except ValueError: continue
        if d < oggi or (d, r["HomeTeam"], r["AwayTeam"]) in giocate: continue
        if r["HomeTeam"] not in squadre or r["AwayTeam"] not in squadre: continue
        ora = None
        if r.get("Time"):
            h, m = r["Time"].split(":"); ora = f"{(int(h)+1)%24:02d}:{m}"
            if int(h)+1 >= 24: d = d + dt.timedelta(days=1)
        n = max(gg[r["HomeTeam"]], gg[r["AwayTeam"]]) + 1
        out.setdefault(str(n), []).append({"casa": r["HomeTeam"], "ospite": r["AwayTeam"], "giorno": d.isoformat(), "ora": ora})
    return out

def main():
    oggi = dt.datetime.now().date()
    cal = json.load(open(os.path.join(BASE, "dati", "calendario.json"), encoding="utf-8"))
    fix = os.path.join(BASE, "dati", "fixtures.csv")
    s = open(HTML, encoding="utf-8").read()
    bk = HTML.replace(".html", ".BACKUP-prima-aggiornamento.html")
    if not os.path.exists(bk): shutil.copy(HTML, bk)
    global COLORI
    la, lb, loghi = parsa_blocco(s, "LOGHI_SQUADRE")
    for _k in [k for k, v in loghi.items() if "/prov_" in v or "/coppe_" in v]: del loghi[_k]  # stemmi di coppa: rivalutati a ogni giro (provvisorio -> ufficiale appena disponibile)
    for nm_, f_ in NUOVI_LOGHI.items():
        if os.path.exists(os.path.join(BASE, "assets", "loghi", f_ + ".png")): loghi[nm_] = f"./assets/loghi/{f_}.png"
    s = s[:la] + json.dumps(loghi, ensure_ascii=False, indent=2) + s[lb:]
    try:
        COLORI, _man = CS.aggiorna(loghi, BASE, os.path.join(BASE, "dati", "colori_squadre.json"))
    except Exception as ex_:
        cp = os.path.join(BASE, "dati", "colori_squadre.json")
        COLORI = {k: v["colori"] for k, v in json.load(open(cp)).items()} if os.path.exists(cp) else {}
    a, b, pro = parsa_blocco(s, "DATA_PRO")
    nuove_forme, rapporto, avvisi, dati_fino = {}, [], [], {}
    previsioni, archivi, track = [], {}, {"leghe": {}}
    tutte_righe = []
    global W_APP
    live_path = os.path.join(BASE, "dati", "storico_live.csv"); mem_path = os.path.join(BASE, "dati", "memoria_modello.json")
    bt = {k: TR.backtest(pp.leggi(file_dati(c))) for k, c in LEGHE.items() if os.path.exists(file_dati(c))}
    mem = AP.impara([r for v in bt.values() for r in v], AP.righe_live(TR.leggi_log(live_path)), mem_path)
    W_APP = mem.get("w", 1.0)
    if "a" in mem: mod.PESO_DATI = mem["a"]
    for key, cod in LEGHE.items():
        nm = (cal.get(key) or {}).get("nome") or {"serie-a": "Serie A (Italia)"}.get(key, key)
        if not os.path.exists(file_dati(cod)):
            avvisi.append(f"{nm}: file dati mancante ({cod}.csv), campionato non aggiornato"); continue
        partite = pp.leggi(file_dati(cod)); cl = classifica(partite)
        ultima = max(p["data"] for p in partite); dati_fino[key] = ultima.isoformat()
        archivi[key] = partite
        rr = bt[key]; tutte_righe += rr; track["leghe"][nm.split(" (")[0]] = TR.riepilogo(rr)
        manuali = ((cal.get(key) or {}).get("turni")) or {}
        turni_src = {k: {"giornata": t["giornata"], "finestra": t.get("finestra"), "dataFine": t.get("dataFine"), "partite": list(t["partite"])} for k, t in manuali.items()}
        viste = {(e["casa"], e["ospite"]) for t in turni_src.values() for e in t["partite"]}
        for n, lista in turni_automatici(partite, fix, oggi).items():
            nuovi = [e for e in lista if (e["casa"], e["ospite"]) not in viste]
            if not nuovi: continue
            t = turni_src.setdefault(n, {"giornata": f"{n}ª Giornata", "finestra": None, "dataFine": None, "partite": []})
            t["partite"] += nuovi
        turni = {}
        for tk, t in sorted(turni_src.items(), key=lambda kv: int(kv[0])):
            giorni = [e["giorno"] for e in t["partite"] if e.get("giorno")]
            fine = t.get("dataFine") or (max(giorni) if giorni else None)
            if not fine or dt.date.fromisoformat(fine[:10]) < oggi: continue
            lista = []
            for e in t["partite"]:
                m, f1, f2 = costruisci_partita(nm.split(" (")[0], cod, partite, cl, e, t, fix)
                lista.append(m); nuove_forme[nome(e["casa"])] = f1; nuove_forme[nome(e["ospite"])] = f2
                fs = m["fasi"]; q = m.get("quoteMercato") or {}
                previsioni.append({"lega": key, "casa": e["casa"], "ospite": e["ospite"], "giorno": e.get("giorno") or "", "p1": fs["1"]["seg1"]["p"], "pX": fs["1"]["seg2"]["p"], "p2": fs["1"]["seg3"]["p"],
                                   "pOver25": fs["3"]["seg1"]["p"], "pGol": fs["2"]["seg1"]["p"], "lh": RAW[(e["casa"], e["ospite"])][0], "la": RAW[(e["casa"], e["ospite"])][1], "mc": RAW[(e["casa"], e["ospite"])][2], "mt": RAW[(e["casa"], e["ospite"])][3], "q1": q.get("1", ""), "qX": q.get("X", ""), "q2": q.get("2", ""), "qOver25": q.get("Over 2,5", "")})
            if giorni:
                d1, d2 = dt.date.fromisoformat(min(giorni)), dt.date.fromisoformat(max(giorni))
                fin = f"{d1.day}-{d2.day} {MESI[d2.month]}" if d1.month == d2.month else f"{d1.day} {MESI[d1.month]}-{d2.day} {MESI[d2.month]}"
            else: fin = t.get("finestra") or ""
            turni[tk] = {"label": f"{t['giornata']} ({fin} {d2.year if giorni else ''})".replace(" )", ")"), "dataFine": fine[:10] + "T23:59:59", "partite": lista}
            if any(not e.get("giorno") or not e.get("ora") for e in t["partite"]):
                avvisi.append(f"{nm}: {t['giornata']} ha partite con giorno/orario da confermare")
            if any(e.get("nota") for e in t["partite"]):
                avvisi.append(f"{nm}: {t['giornata']} ha date da verificare")
        if not turni:
            avvisi.append(f"{nm}: nessuna giornata futura (aggiungi il turno in dati/calendario.json o scarica fixtures.csv aggiornato)")
            if key in pro: pass
        else:
            pro[key] = {"nome": nm, "turni": turni}
        rapporto.append(f"{nm}: {sum(len(t['partite']) for t in turni.values())} partite in {len(turni)} giornate, dati fino al {ultima:%d/%m/%Y} ({len(partite)} gare)")
    log = TR.aggiorna_live(live_path, previsioni, archivi)
    track["totale"] = TR.riepilogo(tutte_righe); track["live"] = TR.riepilogo_live(log)
    track["apprendimento"] = {"w": mem.get("w"), "a": mem.get("a"), "storia": mem.get("storia", [])[-5:]}
    track["aggiornato"] = dt.datetime.now().strftime("%d/%m/%Y %H:%M")
    def _coppe(cache):
        for _comp, _chiave, _nome in (("cl", "champions", "Champions League"), ("el", "europa", "Europa League")):
            try:
                _ch = blocco_coppe(archivi, oggi, avvisi if cache is not None and not cache.get("_2") else [], _comp, cache)
                if _ch: pro[_chiave] = _ch
                else: pro.pop(_chiave, None)
            except Exception as _e:
                pro.pop(_chiave, None); avvisi.append(f"{_nome}: errore nell'elaborazione ({_e})")
    _cache = {}; _coppe(_cache)
    try:
        if assicura_stemmi(pro, loghi, avvisi): _cache["_2"] = True; _coppe(_cache)  # secondo passaggio: i colori dei nuovi stemmi entrano nelle schede
    except Exception as _e:
        avvisi.append(f"Stemmi coppe: errore ({_e})")
    for _chiave, _nome in (("champions", "Champions League"), ("europa", "Europa League")):
        if _chiave in pro: rapporto.append(f"{_nome} (osservazione): {sum(len(t['partite']) for t in pro[_chiave]['turni'].values())} partite in {len(pro[_chiave]['turni'])} turni")
    s = s[:a] + json.dumps(pro, ensure_ascii=False, indent=2) + s[b:]
    la, lb, _vecchi = parsa_blocco(s, "LOGHI_SQUADRE"); s = s[:la] + json.dumps(loghi, ensure_ascii=False, indent=2) + s[lb:]
    a, b, forma_d = parsa_blocco(s, "DATA_FORMA"); forma_d.update(nuove_forme)
    s = s[:a] + json.dumps(forma_d, ensure_ascii=False, indent=2) + s[b:]
    senza = sorted({m[k]["nome"] for c in pro.values() for t in c["turni"].values() for m in t["partite"] for k in ("casa", "ospite")} - set(loghi))
    if senza: avvisi.append("Stemma mancante (colori neutri): " + ", ".join(senza) + " - aggiungi il PNG in assets/loghi")
    meta = {"aggiornato": dt.datetime.now().isoformat(timespec="minutes"), "dati_fino": dati_fino, "avvisi": avvisi}
    blocco = "/*META*/const DATA_META = " + json.dumps(meta, ensure_ascii=False) + ";/*ENDMETA*/\n    "
    if "/*META*/" in s:
        s = re.sub(r"/\*META\*/.*?/\*ENDMETA\*/\n    ", lambda m: blocco, s, count=1, flags=re.S)
    else:
        s = s.replace("const DATA_PRO = ", blocco + "const DATA_PRO = ", 1)
    blk = "/*TRACK*/const DATA_TRACK = " + json.dumps(track, ensure_ascii=False) + ";/*ENDTRACK*/\n    "
    if "/*TRACK*/" in s: s = re.sub(r"/\*TRACK\*/.*?/\*ENDTRACK\*/\n    ", lambda m: blk, s, count=1, flags=re.S)
    else: s = s.replace("const DATA_PRO = ", blk + "const DATA_PRO = ", 1)
    if "/*TRACKPANEL*/" not in s:
        s = s.replace("</body>", PANNELLO + "\n</body>", 1)
    if "/*STATUSBAR*/" not in s:
        barra = """<!--/*STATUSBAR*/--><script>
(function(){try{var M=DATA_META,el=document.createElement('div');
el.style.cssText='position:fixed;bottom:0;left:0;right:0;z-index:50;font:11px ui-monospace,monospace;padding:4px 12px;background:#020617ee;border-top:1px solid #1e293b;color:#94a3b8;display:flex;flex-wrap:wrap;gap:12px';
var ore=(Date.now()-new Date(M.aggiornato).getTime())/36e5;
var st=ore>48?'<span style="color:#f87171">\u26a0 dati non aggiornati da '+Math.floor(ore/24)+' giorni</span>':'<span style="color:#34d399">\u25cf dati aggiornati</span>';
var fino=Object.keys(M.dati_fino).map(function(k){return k+': '+M.dati_fino[k].split('-').reverse().join('/')}).join(' \u00b7 ');
el.innerHTML=st+'<span>Ultimo aggiornamento: '+M.aggiornato.replace('T',' ')+'</span><span>Risultati fino al \u2192 '+fino+'</span>'+M.avvisi.map(function(a){return '<span style="color:#fbbf24">\u26a0 '+a+'</span>'}).join('');
document.body.appendChild(el);document.body.style.paddingBottom='34px';}catch(e){}})();
</script>"""
        s = s.replace("</body>", barra + "\n</body>", 1)
    open(HTML, "w", encoding="utf-8").write(s)
    open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(s)
    print("\n".join(rapporto)); print("\n".join("AVVISO: " + x for x in avvisi)); print("Dashboard aggiornata:", HTML)

if __name__ == "__main__":
    main()
