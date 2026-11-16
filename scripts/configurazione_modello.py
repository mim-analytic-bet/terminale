"""Configurazione operativa congelata: nessuna ottimizzazione implicita."""
import json
import math
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / "config" / "modello_produzione.json"


def carica(path=DEFAULT):
    configurazione = json.loads(Path(path).read_text(encoding="utf-8"))
    if configurazione.get("apprendimento_automatico") is not False:
        raise ValueError("La configurazione operativa deve avere apprendimento automatico disattivato.")
    for chiave, massimo in (("peso_dati", 1.0), ("fiducia_gol", 1.6), ("peso_forma_coppe", 1.0)):
        valore = configurazione.get(chiave)
        if isinstance(valore, bool) or not isinstance(valore, (float, int)) or not math.isfinite(valore) or not 0 <= valore <= massimo:
            raise ValueError(f"Parametro operativo non valido: {chiave}")
    if not configurazione.get("id"):
        raise ValueError("Identificatore della configurazione mancante.")
    return configurazione
