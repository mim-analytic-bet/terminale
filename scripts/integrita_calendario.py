"""Controlli strutturali: non certificano la corrispondenza al calendario ufficiale."""
from collections import Counter
from datetime import date, datetime
from zoneinfo import ZoneInfo

FUSO = ZoneInfo("Europe/Rome")

def errori_turno(partite, squadre):
    errori, coppie, presenze = [], [], Counter()
    for partita in partite:
        casa, ospite = partita.get("casa"), partita.get("ospite")
        if not casa or not ospite or casa == ospite:
            errori.append("Abbinamento non valido")
            continue
        if casa not in squadre or ospite not in squadre:
            errori.append(f"Club non presente nei dati della competizione: {casa} / {ospite}")
        coppie.append((casa, ospite)); presenze.update((casa, ospite))
        try:
            date.fromisoformat(partita["giorno"])
            if partita.get("ora"):
                datetime.strptime(partita["ora"], "%H:%M")
        except (ValueError, KeyError, TypeError):
            errori.append(f"Data/orario non valido: {casa} / {ospite}")
    if len(coppie) != len(set(coppie)):
        errori.append("Incontro duplicato nello stesso turno")
    ripetute = sorted(nome for nome, n in presenze.items() if n > 1)
    if ripetute:
        errori.append("Club ripetuti nello stesso turno: " + ", ".join(ripetute))
    return errori


def futura(partita, adesso=None):
    """Un orario mancante non viene inventato. Data odierna non basta a provare pre-partita."""
    adesso = adesso or datetime.now(FUSO)
    giorno = date.fromisoformat(partita["giorno"])
    if not partita.get("ora"):
        return giorno > adesso.astimezone(FUSO).date()
    inizio = datetime.fromisoformat(partita["giorno"] + "T" + partita["ora"]).replace(tzinfo=FUSO)
    return inizio > adesso
