#!/usr/bin/env python3
"""Scarica orari ufficiali e assenze/squalifiche da API-Football (piano gratuito, 100 richieste/giorno).
Scrive dati/assenze.json. Non fa nulla senza la chiave API_FOOTBALL_KEY e non rompe mai l'aggiornamento:
in caso di errore tiene i dati precedenti e annota il motivo nel file.
- orari: finestra di 7 giorni (1 chiamata per campionato)
- assenze: solo per le partite che iniziano entro 36 ore (1 chiamata a partita), rinfrescate al massimo ogni 8 ore
"""
import json, os, sys, time, urllib.request, urllib.parse, datetime as dt
from zoneinfo import ZoneInfo

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "dati", "assenze.json")
API = "https://v3.football.api-sports.io"
LEGHE = {"serie-a": 135, "premier": 39, "liga": 140, "bundesliga": 78, "ligue1": 61}
ROMA = ZoneInfo("Europe/Rome")
FINESTRA_ORARI_GG, FINESTRA_ASSENZE_ORE, RINFRESCA_ORE, MAX_RICHIESTE, PAUSA = 7, 36, 8, 80, 6.5
chiave = os.environ.get("API_FOOTBALL_KEY", "").strip()
adesso = dt.datetime.now(dt.timezone.utc)
stato = {"rimaste": None, "usate": 0}


class ErroreApi(Exception):
    pass


def chiama(percorso, **params):
    if stato["usate"] >= MAX_RICHIESTE:
        raise ErroreApi("limite di richieste per esecuzione raggiunto")
    if stato["rimaste"] is not None and stato["rimaste"] <= 3:
        raise ErroreApi("richieste giornaliere quasi esaurite")
    req = urllib.request.Request(f"{API}/{percorso}?{urllib.parse.urlencode(params)}", headers={"x-apisports-key": chiave})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            corpo = json.load(r)
            rim = r.headers.get("x-ratelimit-requests-remaining")
            if rim and rim.isdigit(): stato["rimaste"] = int(rim)
    except Exception as e:
        raise ErroreApi(f"{percorso}: {e}")
    stato["usate"] += 1
    time.sleep(PAUSA)  # piano gratuito: max ~10 richieste al minuto
    err = corpo.get("errors")
    if err:
        raise ErroreApi(json.dumps(err, ensure_ascii=False)[:300])
    return corpo.get("response") or []


def carica():
    try:
        return json.load(open(OUT, encoding="utf-8"))
    except Exception:
        return {"partite": []}


def salva(d):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    vecchio = carica()
    out = {"aggiornato": adesso.isoformat(timespec="minutes"), "stato": "ok", "errori": [], "partite": []}
    if not chiave:
        vecchio.update({"stato": "senza_chiave"}); salva(vecchio); print("assenze: chiave API_FOOTBALL_KEY assente, salto"); return
    stagione = adesso.year if adesso.month >= 7 else adesso.year - 1
    precedenti = {p["id"]: p for p in vecchio.get("partite", [])}
    oggi = adesso.astimezone(ROMA).date()
    fine = oggi + dt.timedelta(days=FINESTRA_ORARI_GG)
    for lega, lid in LEGHE.items():
        try:
            fx = chiama("fixtures", league=lid, season=stagione, **{"from": oggi.isoformat(), "to": fine.isoformat()})
        except ErroreApi as e:
            out["errori"].append(f"{lega}: {e}")
            out["partite"] += [p for p in vecchio.get("partite", []) if p.get("lega") == lega]  # tengo i dati precedenti
            continue
        for f in fx:
            fid = f["fixture"]["id"]; inizio = dt.datetime.fromisoformat(f["fixture"]["date"]).astimezone(ROMA)
            nsl = f["fixture"]["status"]["short"]
            p = {"id": fid, "lega": lega, "casa": f["teams"]["home"]["name"], "ospite": f["teams"]["away"]["name"],
                 "giorno": inizio.date().isoformat(), "ora": inizio.strftime("%H:%M") if nsl == "NS" else None, "stato": nsl,
                 "assenze": None, "controllato": None}
            pv = precedenti.get(fid)
            if pv: p["assenze"], p["controllato"] = pv.get("assenze"), pv.get("controllato")
            ore_al_via = (inizio - adesso).total_seconds() / 3600
            vecchio_ok = p["controllato"] and (adesso - dt.datetime.fromisoformat(p["controllato"])).total_seconds() < RINFRESCA_ORE * 3600
            if 0 <= ore_al_via <= FINESTRA_ASSENZE_ORE and nsl == "NS" and not vecchio_ok:
                try:
                    inj = chiama("injuries", fixture=fid)
                    ass = {"casa": [], "ospite": []}
                    for i in inj:
                        lato = "casa" if i["team"]["id"] == f["teams"]["home"]["id"] else "ospite"
                        ass[lato].append({"nome": i["player"].get("name"), "tipo": i["player"].get("type"), "motivo": i["player"].get("reason")})
                    p["assenze"], p["controllato"] = ass, adesso.isoformat(timespec="minutes")
                except ErroreApi as e:
                    out["errori"].append(f"{p['casa']}-{p['ospite']}: {e}")
            out["partite"].append(p)
    if out["errori"]:
        out["stato"] = "parziale" if out["partite"] else "errore"
    out["richieste_rimaste"] = stato["rimaste"]
    if not out["partite"] and vecchio.get("partite"):  # nulla di nuovo: non cancello il vecchio
        out["partite"] = vecchio["partite"]
    salva(out)
    n_ass = sum(1 for p in out["partite"] if p.get("assenze") is not None)
    print(f"assenze: {len(out['partite'])} partite, {n_ass} con assenze controllate, richieste usate {stato['usate']}, stato {out['stato']}")
    for e in out["errori"][:5]: print("AVVISO assenze:", e)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # mai bloccare l'aggiornamento
        print("AVVISO assenze: errore imprevisto", e); sys.exit(0)
