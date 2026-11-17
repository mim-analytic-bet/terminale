#!/usr/bin/env python3
"""Limite di scarichi automatici per fonte, letto da config/fonti_dati.json (autorizzazione_interna.limiti). Nessuna rete.
Uso:  limite_download.py --fonte football_data_uk      -> exit 0 se lo scarico e' consentito ora, 1 altrimenti
      limite_download.py --registra football_data_uk   -> annota uno scarico riuscito
FORZA_SCARICO=1 salta il controllo (eccezione voluta dell'utente, resta scritta nel registro)."""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CONFIG = BASE / "config" / "fonti_dati.json"
STAMP = BASE / "dati" / "scarichi_fonti.json"
GIORNI = {"lun": 0, "mar": 1, "mer": 2, "gio": 3, "ven": 4, "sab": 5, "dom": 6}


def limite(documento, fonte):
    return ((documento.get("autorizzazione_interna") or {}).get("limiti") or {}).get(fonte)


def consentito(documento, fonte, adesso, storico):
    """(bool, motivo). storico: lista di timestamp ISO con fuso degli scarichi gia' fatti per la fonte."""
    lim = limite(documento, fonte)
    if not lim:
        return True, "nessun limite configurato"
    giorni = [GIORNI[g] for g in lim.get("giorni_consentiti", []) if g in GIORNI]
    if giorni and adesso.weekday() not in giorni:
        return False, "giorno non consentito"
    fatti = [dt.datetime.fromisoformat(x) for x in storico]
    if any(x.date() == adesso.date() for x in fatti):
        return False, "gia' scaricato oggi"
    settimana = adesso.isocalendar()[:2]
    if sum(1 for x in fatti if x.isocalendar()[:2] == settimana) >= int(lim.get("max_download_settimana", 2)):
        return False, "limite settimanale raggiunto"
    return True, "consentito"


def leggi(path=STAMP):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fonte"); p.add_argument("--registra")
    p.add_argument("--config", type=Path, default=CONFIG); p.add_argument("--stamp", type=Path, default=STAMP)
    a = p.parse_args()
    adesso = dt.datetime.now(dt.timezone.utc)
    storico = leggi(a.stamp)
    if a.registra:
        storico.setdefault(a.registra, []).append(adesso.isoformat(timespec="seconds"))
        storico[a.registra] = storico[a.registra][-30:]
        a.stamp.parent.mkdir(parents=True, exist_ok=True)
        a.stamp.write_text(json.dumps(storico, indent=1), encoding="utf-8")
        print(f"{a.registra}: scarico registrato")
        return 0
    if not a.fonte:
        p.error("serve --fonte o --registra")
    if os.environ.get("FORZA_SCARICO") == "1":
        print(f"{a.fonte}: controllo del limite saltato per richiesta esplicita (FORZA_SCARICO=1)")
        return 0
    documento = json.loads(a.config.read_text(encoding="utf-8"))
    ok, motivo = consentito(documento, a.fonte, adesso, storico.get(a.fonte, []))
    print(f"{a.fonte}: {motivo}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
