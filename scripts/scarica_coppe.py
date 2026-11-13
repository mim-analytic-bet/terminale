#!/usr/bin/env python3
"""Scarica (1) la Champions da football-data.org (chiave FOOTBALL_DATA_KEY) e (2) l'Europa League da API Ninjas (chiave API_NINJAS_KEY, league=uel;
piano gratuito: solo uso NON commerciale). Scrive dati/coppe/CL_live.json e EL_live.json. Se fallisce lascia i file precedenti. Non blocca mai l'aggiornamento."""
import json, os, sys, urllib.request, datetime as dt
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import time
oggi = dt.date.today(); stagione = oggi.year if oggi.month >= 7 else oggi.year - 1
DEST = os.path.join(BASE, "dati", "coppe")


def salva(nome, stagione, matches, extra=None):
    os.makedirs(DEST, exist_ok=True)
    json.dump({"scaricato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"), "stagione": stagione, "matches": matches, **(extra or {})}, open(os.path.join(DEST, nome), "w", encoding="utf-8"), ensure_ascii=False)


def http(url, header, valore):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={header: valore}), timeout=40) as r: return json.load(r)
    except Exception as e:
        msg = str(e)
        if hasattr(e, "read"):
            try: msg += " " + e.read().decode()[:200]
            except Exception: pass
        raise RuntimeError(msg)


def champions():
    chiave = os.environ.get("FOOTBALL_DATA_KEY", "").strip()
    if not chiave: print("coppe: chiave FOOTBALL_DATA_KEY assente, salto la Champions"); return
    try:
        corpo = http(f"https://api.football-data.org/v4/competitions/CL/matches?season={stagione}", "X-Auth-Token", chiave)
        if not corpo.get("matches"): raise ValueError("nessuna partita nella risposta")
        salva("CL_live.json", stagione, corpo["matches"]); print(f"coppe: CL {stagione}: {len(corpo['matches'])} partite scaricate")
    except Exception as e: print("AVVISO coppe: download Champions fallito:", e)


FASI = [("playoff", "PLAYOFFS"), ("play-off", "PLAYOFFS"), ("round of 16", "LAST_16"), ("last 16", "LAST_16"), ("quarter", "QUARTER_FINALS"), ("semi", "SEMI_FINALS"), ("final", "FINAL")]


def converti_ninjas(g):
    """Formato API Ninjas -> formato football-data.org (lo stesso che legge coppe.py). Tutto cio' che manca resta None (mai inventato)."""
    st = {"final": "FINISHED", "scheduled": "TIMED", "delayed": "TIMED", "in_progress": "IN_PLAY", "postponed": "POSTPONED", "canceled": "CANCELLED", "suspended": "SUSPENDED"}.get(g.get("status"), "SCHEDULED")
    ora = g.get("start_time") or (g["date"] + "T00:00:00Z"); sc = {"duration": "REGULAR"}
    hs, as_ = g.get("home_score"), g.get("away_score"); dec = g.get("decided_in"); ps = g.get("period_scores") or {}
    if st == "FINISHED" and hs is not None and as_ is not None:
        if dec in ("extra_time", "penalties") and len(ps.get("home") or []) >= 2 and len(ps.get("away") or []) >= 2:
            sc = {"regularTime": {"home": sum(ps["home"][:2]), "away": sum(ps["away"][:2])}}  # 90 minuti = somma dei primi due tempi
        elif dec in ("extra_time", "penalties"): st = "FINISHED_NO90"  # risultato a 90' non ricavabile: non usato
        else: sc["fullTime"] = {"home": hs, "away": as_}
    rnd = (g.get("round") or "").lower(); stage = "LEAGUE_STAGE"
    for k, v in FASI:
        if k in rnd: stage = v; break
    md = None
    if stage == "LEAGUE_STAGE":
        import re
        m = re.search(r"(\d+)", g.get("round") or ""); md = int(m.group(1)) if m else None
    return {"id": g["game_id"], "utcDate": ora, "status": st, "matchday": md, "stage": stage, "_season_type": g.get("season_type"),
            "homeTeam": {"name": g["home_team"]["name"], "shortName": g["home_team"].get("name")}, "awayTeam": {"name": g["away_team"]["name"], "shortName": g["away_team"].get("name")}, "score": sc}


def europa():
    chiave = (os.environ.get("API_NINJAS_KEY") or "").strip()
    if not chiave: print("coppe: chiave API_NINJAS_KEY assente, salto l'Europa League"); return
    # Il piano gratuito non ammette limit/offset: si interroga un giorno alla volta (mercoledi' e giovedi'), in modo incrementale.
    dest = os.path.join(DEST, "EL_live.json"); prec, fatti = {}, set()
    try:
        vecchio = json.load(open(dest, encoding="utf-8")); fatti = set(vecchio.get("giorni_ok", []))
        for m in vecchio.get("matches", []): prec[m["id"]] = m
    except Exception: pass
    try:
        g = dt.date(stagione, 9, 10); giorni = []
        while g <= oggi + dt.timedelta(days=14):
            if g.weekday() in (2, 3) and (g >= oggi - dt.timedelta(days=3) or g.isoformat() not in fatti): giorni.append(g)
            g += dt.timedelta(days=1)
        nuovi, tot_err = 0, 0
        for g in giorni:
            try:
                pag = http(f"https://api.api-ninjas.com/v1/soccermatches?league=uel&date={g.isoformat()}", "X-Api-Key", chiave)
            except RuntimeError as e:
                tot_err += 1
                if tot_err >= 3: raise
                print("AVVISO coppe: EL", g, e); continue
            time.sleep(0.4)
            if not isinstance(pag, list): continue
            if g < oggi - dt.timedelta(days=3): fatti.add(g.isoformat())
            for x in pag:
                if x.get("home_team") and x.get("away_team") and x.get("game_id") and x.get("season") in (None, stagione):
                    c = converti_ninjas(x)
                    if c["status"] != "FINISHED_NO90": prec[c["id"]] = c; nuovi += 1
        conv = list(prec.values())
        if not conv: raise ValueError("nessuna partita trovata (la fonte potrebbe non avere ancora il calendario)")
        per_sq = {}
        for m in sorted((m for m in conv if m["stage"] == "LEAGUE_STAGE" and m["matchday"] is None), key=lambda m: m["utcDate"]):
            for sq in (m["homeTeam"]["name"], m["awayTeam"]["name"]): per_sq[sq] = per_sq.get(sq, 0) + 1
            m["matchday"] = per_sq[m["homeTeam"]["name"]]
        salva("EL_live.json", stagione, conv, {"giorni_ok": sorted(fatti)}); print(f"coppe: EL {stagione}: {len(conv)} partite in archivio ({len(giorni)} giorni interrogati)")
    except Exception as e: print("AVVISO coppe: download Europa League fallito:", e)


champions(); europa()
sys.exit(0)
