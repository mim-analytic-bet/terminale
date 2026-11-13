#!/usr/bin/env python3
"""Scarica da football-data.org (piano gratuito) le partite della Champions League della stagione corrente in dati/coppe/CL_live.json.
Richiede FOOTBALL_DATA_KEY. Se fallisce, lascia il file precedente. Non blocca mai l'aggiornamento."""
import json, os, sys, urllib.request, datetime as dt
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chiave = os.environ.get("FOOTBALL_DATA_KEY", "").strip()
oggi = dt.date.today(); stagione = oggi.year if oggi.month >= 7 else oggi.year - 1
if not chiave:
    print("coppe: chiave FOOTBALL_DATA_KEY assente, salto"); sys.exit(0)
dest = os.path.join(BASE, "dati", "coppe", "CL_live.json")
try:
    req = urllib.request.Request(f"https://api.football-data.org/v4/competitions/CL/matches?season={stagione}", headers={"X-Auth-Token": chiave})
    with urllib.request.urlopen(req, timeout=40) as r: corpo = json.load(r)
    if not corpo.get("matches"): raise ValueError("nessuna partita nella risposta")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    json.dump({"scaricato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"), "stagione": stagione, "matches": corpo["matches"]}, open(dest, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"coppe: CL {stagione}: {len(corpo['matches'])} partite scaricate")
except Exception as e:
    msg = str(e)
    if hasattr(e, "read"):
        try: msg += " " + e.read().decode()[:200]
        except Exception: pass
    print("AVVISO coppe: download Champions fallito:", msg)
sys.exit(0)
