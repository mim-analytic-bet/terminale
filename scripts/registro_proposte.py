"""Registro delle proposte (Eventi Combinati, Cluster Multi-Evento) con prova temporale.

Principi (stessi del registro delle partite, scripts/track_record.py):
- una proposta entra nel registro solo se TUTTE le sue partite hanno un orario di inizio con fuso e iniziano dopo il momento della registrazione;
- una proposta registrata non si riscrive: dopo la registrazione cambiano solo i campi di valutazione (esito delle gambe, stato, esito);
- la stessa proposta (stesso tipo, stesse partite, stessi mercati) non si registra due volte, anche se in un'esecuzione successiva le quote sono cambiate:
  vale la prima registrazione, con la quota e il tipo di quota (reale, derivata, equa) di quel momento;
- non si inventano risultati: una gamba si valuta solo se esiste la partita giocata con lo stesso giorno e gli stessi nomi.
Le proposte NON implicano puntate o consigli di gioco: sono eventi che il modello segnala e di cui si misura l'affidabilita'.
"""
import csv, datetime as dt, hashlib, json, os, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(BASE, "scripts", "proposte_cli.js")
SCHEMA = "1"
MAX_GAMBE = 2


def _campi():
    c = ["id", "registrata", "cod", "etichetta", "n_gambe"]
    for i in range(1, MAX_GAMBE + 1):
        c += [f"g{i}_lega", f"g{i}_casa", f"g{i}_ospite", f"g{i}_giorno", f"g{i}_mercato", f"g{i}_q", f"g{i}_tipo", f"g{i}_p", f"g{i}_inizio_utc", f"g{i}_esito"]
    return c + ["molt", "prob", "inizio_utc", "config_id", "versione", "schema", "stato", "esito"]


CAMPI = _campi()


def esito_mercato(mercato, gc, go):
    """True/False se il mercato si e' verificato con il risultato finale gc-go; None se il mercato non e' noto."""
    r = {"1": lambda: gc > go, "2": lambda: go > gc, "1X": lambda: gc >= go, "X2": lambda: go >= gc,
         "Over 2,5": lambda: gc + go >= 3, "Under 2,5": lambda: gc + go <= 2,
         "Gol": lambda: gc > 0 and go > 0, "No Gol": lambda: not (gc > 0 and go > 0)}.get(mercato)
    return None if r is None else bool(r())


def calcola_proposte(pro, adesso, node="node"):
    """Esegue la stessa funzione della pagina (assets/js/combo.js) in Node. Ritorna (proposte, errore|None)."""
    if adesso.tzinfo is None: raise ValueError("L'orario deve avere un fuso")
    env = {**os.environ, "TZ": "Europe/Rome"}  # la finestra settimanale della pagina usa il fuso locale degli utenti italiani
    try:
        r = subprocess.run([node, CLI], input=json.dumps({"data_pro": pro, "adesso": adesso.isoformat()}), capture_output=True, text=True, timeout=60, env=env)
    except (OSError, subprocess.SubprocessError) as e:
        return [], f"Node non disponibile o in errore: {e}"
    if r.returncode != 0:
        return [], "Calcolo delle proposte fallito: " + (r.stderr.strip().splitlines() or ["errore sconosciuto"])[-1]
    try:
        return json.loads(r.stdout)["proposte"], None
    except (ValueError, KeyError) as e:
        return [], f"Risposta del calcolo non valida: {e}"


def _chiave(p):
    return p["cod"] + "|" + "|".join(sorted(f"{g['comp']}:{(g.get('chiave') or {}).get('casa')}-{(g.get('chiave') or {}).get('ospite')}:{(g.get('chiave') or {}).get('giorno')}:{g['mer']}" for g in p["legs"]))


def _id(chiave):
    return hashlib.sha1(chiave.encode("utf-8")).hexdigest()[:10]


def leggi(path):
    if not os.path.exists(path): return []
    with open(path, newline="", encoding="utf-8") as f: return list(csv.DictReader(f))


def _scrivi(path, righe):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPI); w.writeheader(); w.writerows(righe)


def _inizio(g):
    try:
        d = dt.datetime.fromisoformat(g["inizioUtc"])
    except (KeyError, TypeError, ValueError):
        return None
    return d if d.tzinfo is not None else None


def valuta(righe, archivi):
    """Valuta le gambe con risultato noto. Cambia solo i campi di valutazione."""
    for r in righe:
        if r["stato"] == "valutata": continue
        esiti = []
        for i in range(1, int(r["n_gambe"]) + 1):
            e = r[f"g{i}_esito"]
            if not e:
                for g in archivi.get(r[f"g{i}_lega"], []):
                    if g["casa"] == r[f"g{i}_casa"] and g["ospite"] == r[f"g{i}_ospite"] and g["data"].isoformat() == r[f"g{i}_giorno"]:
                        v = esito_mercato(r[f"g{i}_mercato"], g["gc"], g["go"])
                        if v is not None: e = "V" if v else "P"
                        break
                r[f"g{i}_esito"] = e
            esiti.append(e)
        if "P" in esiti: r["stato"], r["esito"] = "valutata", "P"          # una gamba persa decide la combinazione
        elif esiti and all(e == "V" for e in esiti): r["stato"], r["esito"] = "valutata", "V"
    return righe


def aggiorna(path, proposte, archivi, config_id, versione, adesso=None):
    """Registra le proposte nuove (con prova temporale) e valuta quelle con risultati. Ritorna (righe, nuove, scartate)."""
    adesso = adesso or dt.datetime.now(dt.timezone.utc)
    if adesso.tzinfo is None: raise ValueError("L'orario del registro deve avere un fuso")
    righe = leggi(path); presenti = {r["id"] for r in righe}; nuove = scartate = 0
    for p in proposte:
        if not 1 <= len(p["legs"]) <= MAX_GAMBE: scartate += 1; continue
        ini = [_inizio(g) for g in p["legs"]]
        if any(x is None or x <= adesso for x in ini) or any(not g.get("chiave") for g in p["legs"]): scartate += 1; continue
        pid = _id(_chiave(p))
        if pid in presenti: continue
        riga = {c: "" for c in CAMPI}
        riga.update({"id": pid, "registrata": adesso.isoformat(timespec="seconds"), "cod": p["cod"], "etichetta": p["etichetta"], "n_gambe": len(p["legs"]),
                     "molt": round(p["molt"], 4), "prob": round(p["prob"], 4), "inizio_utc": min(ini).isoformat(), "config_id": config_id,
                     "versione": versione, "schema": SCHEMA, "stato": "aperta"})
        for i, (g, x) in enumerate(zip(p["legs"], ini), 1):
            k = g["chiave"]
            riga.update({f"g{i}_lega": g["comp"], f"g{i}_casa": k["casa"], f"g{i}_ospite": k["ospite"], f"g{i}_giorno": k["giorno"], f"g{i}_mercato": g["mer"],
                         f"g{i}_q": round(g["q"], 4), f"g{i}_tipo": g["tipo"], f"g{i}_p": round(g["p"], 4), f"g{i}_inizio_utc": x.isoformat()})
        righe.append(riga); presenti.add(pid); nuove += 1
    valuta(righe, archivi)
    _scrivi(path, righe)
    return righe, nuove, scartate


def categoria_quota(r):
    """'reale' = tutte le gambe con quota Bet365; 'derivata' = nessuna equa ma almeno una ricavata dall'1X2; 'equa' = almeno una gamba senza quota di mercato.
    Le categorie si valutano separatamente: una quota equa e' 1/p del modello e non misura il confronto con il mercato."""
    tipi = [r[f"g{i}_tipo"] for i in range(1, int(r["n_gambe"]) + 1)]
    return "equa" if "equa" in tipi else ("derivata" if "derivata" in tipi else "reale")


def riepilogo(righe):
    """Conteggi per la dashboard, per tipo di proposta e per categoria di quota (reale / derivata / equa), separati.
    Nessuna percentuale di successo qui: la soglia di campione minimo e' decisa da chi mostra i dati ('dati insufficienti')."""
    out = {"registrate": len(righe), "valutate": 0, "per_tipo": {}}
    for r in righe:
        valutata = r["stato"] == "valutata"
        if valutata: out["valutate"] += 1
        for chiave in (r["cod"], "quota:" + categoria_quota(r)):
            t = out["per_tipo"].setdefault(chiave, {"registrate": 0, "valutate": 0, "vinte": 0, "prob_media": 0.0, "somma_brier": 0.0})
            t["registrate"] += 1
            if valutata:
                y = 1 if r["esito"] == "V" else 0
                t["valutate"] += 1; t["vinte"] += y
                t["prob_media"] += float(r["prob"]); t["somma_brier"] += (float(r["prob"]) - y) ** 2
    for t in out["per_tipo"].values():
        n = t["valutate"]
        t["prob_media"] = round(t["prob_media"] / n, 4) if n else None
        t["brier"] = round(t["somma_brier"] / n, 4) if n else None
        del t["somma_brier"]
    return out
