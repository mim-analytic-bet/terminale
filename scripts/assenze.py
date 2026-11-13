#!/usr/bin/env python3
"""Scarica gli orari ufficiali dei prossimi 10 giorni da football-data.org (piano gratuito, 10 richieste/minuto)
e scrive dati/assenze.json (usato dal generatore per compilare gli orari mancanti).
Le assenze/squalifiche NON sono nel piano gratuito: si inseriscono a mano in dati/assenze_manuali.json.
Senza la chiave FOOTBALL_DATA_KEY non fa nulla; in caso di errore tiene i dati precedenti e annota il motivo. Non blocca mai l'aggiornamento.
"""
import json, os, sys, time, urllib.request, datetime as dt
from zoneinfo import ZoneInfo

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "dati", "assenze.json")
API = "https://api.football-data.org/v4/competitions"
LEGHE = {"serie-a": "SA", "premier": "PL", "liga": "PD", "bundesliga": "BL1", "ligue1": "FL1"}
ROMA = ZoneInfo("Europe/Rome")
chiave = os.environ.get("FOOTBALL_DATA_KEY", "").strip()
adesso = dt.datetime.now(dt.timezone.utc)


def carica():
    try: return json.load(open(OUT, encoding="utf-8"))
    except Exception: return {"partite": []}


def salva(d):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    vecchio = carica()
    if not chiave:
        print("orari: chiave FOOTBALL_DATA_KEY assente, salto"); return
    out = {"aggiornato": adesso.isoformat(timespec="minutes"), "fonte": "football-data.org", "stato": "ok", "errori": [], "partite": []}
    oggi = adesso.astimezone(ROMA).date(); fine = oggi + dt.timedelta(days=10)
    for lega, cod in LEGHE.items():
        req = urllib.request.Request(f"{API}/{cod}/matches?dateFrom={oggi}&dateTo={fine}", headers={"X-Auth-Token": chiave})
        try:
            with urllib.request.urlopen(req, timeout=30) as r: corpo = json.load(r)
        except Exception as e:
            msg = str(e)
            if hasattr(e, "read"):
                try: msg += " " + e.read().decode()[:200]
                except Exception: pass
            out["errori"].append(f"{lega}: {msg}")
            out["partite"] += [p for p in vecchio.get("partite", []) if p.get("lega") == lega]
            time.sleep(7); continue
        for m in corpo.get("matches", []):
            inizio = dt.datetime.fromisoformat(m["utcDate"].replace("Z", "+00:00")).astimezone(ROMA)
            out["partite"].append({"id": m["id"], "lega": lega, "casa": m["homeTeam"].get("name") or m["homeTeam"].get("shortName"),
                                   "ospite": m["awayTeam"].get("name") or m["awayTeam"].get("shortName"), "giorno": inizio.date().isoformat(),
                                   "ora": inizio.strftime("%H:%M") if m.get("status") == "TIMED" else None, "stato": m.get("status"), "assenze": None, "controllato": None})
        time.sleep(7)  # 10 richieste/minuto nel piano gratuito
    if out["errori"]: out["stato"] = "parziale" if out["partite"] else "errore"
    salva(out)
    print(f"orari: {len(out['partite'])} partite, con orario {sum(1 for p in out['partite'] if p['ora'])}, stato {out['stato']}")
    for e in out["errori"][:5]: print("AVVISO orari:", e)


if __name__ == "__main__":
    try: main()
    except Exception as e:
        print("AVVISO orari: errore imprevisto", e); sys.exit(0)
