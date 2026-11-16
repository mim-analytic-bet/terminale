#!/usr/bin/env python3
"""Verifica offline il prodotto generato. Non certifica dati o conformità legale."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import configurazione_modello as CFG
import verifica_fonti as VF

ROOT = Path(__file__).resolve().parents[1]


def blocco(html, nome):
    match = re.search(r"const\s+" + re.escape(nome) + r"\s*=\s*", html)
    if not match: raise ValueError("Blocco assente: " + nome)
    return json.JSONDecoder().raw_decode(html, match.end())[0]


def verifica(root=ROOT):
    html = (root / "index.html").read_text()
    pro, meta, track, loghi = [blocco(html, n) for n in ("DATA_PRO", "DATA_META", "DATA_TRACK", "LOGHI_SQUADRE")]
    errori, competizioni, nomi = [], {}, set()
    if html != (root / "scheda-partita-dashboard.html").read_text(): errori.append("Le due viste HTML differiscono")
    if meta.get("config_id") != CFG.carica()["id"]: errori.append("Configurazione della vista non allineata")
    for key, lega in pro.items():
        n = con_quote = 0
        ids = set()
        for turno in lega["turni"].values():
            for p in turno["partite"]:
                n += 1
                if p["id"] in ids: errori.append("ID duplicato: " + str(p["id"]))
                ids.add(p["id"])
                nomi.update(p[k]["nome"] for k in ("casa", "ospite"))
                q = p.get("quoteMercato")
                if q: con_quote += 1
                f = p["fasi"]["1"]
                probabilita = [f[k]["p"] for k in ("seg1", "seg2", "seg3")]
                if any(not 0 <= x <= 1 for x in probabilita) or abs(sum(probabilita) - 1) > .016:
                    errori.append("Probabilità 1X2 non coerenti: " + str(p["id"]))
        competizioni[key] = {"partite": n, "con_quote": con_quote, "turni": list(lega["turni"])}
    for nome in nomi:
        rel = loghi.get(nome, "")
        if not rel.startswith("./assets/badges/qt_") or not (root / rel).is_file():
            errori.append("Identificatore originale mancante: " + nome)
    fonti = json.loads((root / "config/fonti_dati.json").read_text())
    protetti = ["dati/storico_live.csv", "dati/memoria_modello.json", "dati/coppe/previsioni_CL.csv", "dati/coppe/previsioni_EL.csv", "dati/coppe/memoria_coppe.json", "dati/coppe/memoria_coppe_EL.json", "storico-pronostici.csv"]
    return {"verificato_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "stato": "verifica_interna", "errori_tecnici": errori, "config_id": meta["config_id"],
            "versione_modello": meta["versione_modello"], "anteprima": meta["anteprima"],
            "competizioni": competizioni, "partite_totali": sum(x["partite"] for x in competizioni.values()),
            "dati_fino": meta["dati_fino"], "avvisi": meta["avvisi"], "backtest_solo_dati": track["totale"],
            "registro_live": track["live"], "impedimenti_condivisione": VF.impedimenti(fonti, "condivisione"),
            "impedimenti_commerciali": VF.impedimenti(fonti, "commerciale"),
            "sha256_registri": {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in protetti if (root / p).is_file()},
            "nota": "I controlli tecnici non provano autenticità dei risultati, calendario ufficiale, autorizzazioni o validità predittiva."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = verifica()
    testo = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(testo)
    print(json.dumps({"partite": report["partite_totali"], "errori_tecnici": report["errori_tecnici"],
                      "impedimenti_commerciali": len(report["impedimenti_commerciali"])}, ensure_ascii=False))
    raise SystemExit(1 if report["errori_tecnici"] else 0)


if __name__ == "__main__": main()
