#!/usr/bin/env python3
"""Controllo documentale locale prima di download o pubblicazione. Nessuna rete."""
import argparse
import json
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / "config" / "fonti_dati.json"


def impedimenti(documento, operazione, fonti=None):
    if not isinstance(documento, dict) or not isinstance(documento.get("fonti"), dict):
        return ["Registro delle fonti mancante o non valido"]
    registro = documento["fonti"]
    nomi = list(registro) if fonti is None else list(fonti)
    if not nomi:
        return ["Nessuna fonte indicata nel registro"]
    errori = []
    for nome in nomi:
        fonte = registro.get(nome)
        if not isinstance(fonte, dict):
            errori.append(f"{nome}: fonte non censita")
            continue
        if fonte.get("piano_verificato") is not True or not fonte.get("evidenze"):
            errori.append(f"{nome}: piano e autorizzazione non documentati")
        elif fonte.get("permessi", {}).get(operazione) is not True:
            errori.append(f"{nome}: operazione {operazione} non autorizzata nel registro")
    return errori


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT)
    parser.add_argument("--operazione", choices=("download", "condivisione", "commerciale", "addestramento"))
    parser.add_argument("--fonte", action="append")
    args = parser.parse_args()
    try:
        documento = json.loads(args.config.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("BLOCCO FONTI: registro non disponibile:", exc)
        return 2
    if args.operazione is None:
        for nome, fonte in documento.get("fonti", {}).items():
            print(f"{nome}: " + ("documentata" if fonte.get("piano_verificato") and fonte.get("evidenze") else "da verificare"))
        return 0
    errori = impedimenti(documento, args.operazione, args.fonte)
    for errore in errori:
        print("BLOCCO FONTI:", errore)
    if not errori:
        print("Registro documentale compatibile con l'operazione; non sostituisce una verifica legale.")
    return 2 if errori else 0


if __name__ == "__main__":
    raise SystemExit(main())
