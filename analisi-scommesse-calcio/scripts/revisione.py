#!/usr/bin/env python3
"""Revisione dello storico dei pronostici e delle giocate.

Uso: revisione.py storico.csv [--oggi AAAA-MM-GG]

Colonne (separatore ; oppure , oppure tab). Obbligatorie: data, partita,
mercato, esito, quota (o quota_presa), prob_stimata, risultato.
Facoltative: posizione (1, 2, 3, SICURA, EXTRA), livello, quota_chiusura,
tipo_quota, prob_mercato, valore, tipo_record, puntata, profitto,
campionato, giornata, risultato_finale.
risultato: V (indovinato/vinta), P (sbagliato/persa), A (annullato), vuoto = in attesa.
Una riga è una giocata reale se ha una puntata maggiore di zero.
"""
import csv
import datetime as dt
import math
import sys

FASCE_QUOTA = [("fino a 1,50", 0, 1.50), ("1,50-1,75", 1.50, 1.75), ("1,75-2,10", 1.75, 2.10),
               ("2,10-3,00", 2.10, 3.00), ("3,00 e oltre", 3.00, 1e9)]
CAMPIONE_MINIMO = 200          # giocate reali per giudicare il metodo
CAMPIONE_MINIMO_QUOTE_ALTE = 300  # se la quota media supera 2,50


def num(s):
    s = (s or "").strip().replace("%", "").replace("€", "").replace(" ", "")
    if not s:
        return None
    if "," in s and "." in s:
        s = s.replace(".", "")
    return float(s.replace(",", "."))


def data(s):
    s = s.strip()
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d.%m.%Y"):
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            pass
    raise ValueError(f"data non riconosciuta: {s!r}")


def it(x, dec=2):
    return f"{x:.{dec}f}".replace(".", ",")


def sg(x):
    return "+" if x >= 0 else ""


def pc(x, dec=1):
    return f"{sg(x)}{it(x * 100, dec)}%"


def leggi(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        testo = f.read()
    dialetto = csv.Sniffer().sniff(testo.splitlines()[0], delimiters=";,\t")
    righe = list(csv.DictReader(testo.splitlines(), dialect=dialetto))
    out = []
    for i, r in enumerate(righe, 2):
        r = {k.strip().lower(): (v or "") for k, v in r.items() if k}
        if not r.get("data", "").strip():
            continue
        quota = num(r.get("quota_presa") or r.get("quota"))
        prob = num(r.get("prob_stimata"))
        if prob is not None and prob <= 1:
            prob *= 100
        puntata = num(r.get("puntata")) or 0.0
        esito = r.get("risultato", "").strip().upper()[:1]
        profitto = num(r.get("profitto"))
        if profitto is None and esito and puntata:
            profitto = {"V": puntata * (quota - 1), "P": -puntata, "A": 0.0}.get(esito)
        out.append(dict(
            riga=i, data=data(r["data"]), partita=r.get("partita", ""), mercato=r.get("mercato", ""),
            esito_testo=r.get("esito", ""), quota=quota, chiusura=num(r.get("quota_chiusura")),
            prob=prob, puntata=puntata, esito=esito, profitto=profitto or 0.0,
            posizione=(r.get("posizione") or r.get("livello") or "").strip().upper(),
            tipo_record=r.get("tipo_record", "").strip().upper(),
        ))
    return out


def sezione(t):
    print(f"\n== {t} ==")


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    oggi = dt.date.today()
    if "--oggi" in argv:
        oggi = data(argv[argv.index("--oggi") + 1])
    tutte = leggi(argv[0])

    futuri = [x for x in tutte if x["esito"] and x["data"] > oggi]
    g = [x for x in tutte if x not in futuri]
    concluse = [x for x in g if x["esito"] in ("V", "P")]
    annullate = [x for x in g if x["esito"] == "A"]
    attesa = [x for x in g if not x["esito"]]

    # ------------------------------------------------ pronostici (tutti)
    print(f"== PRONOSTICI (data di riferimento {oggi.isoformat()}) ==")
    if futuri:
        print(f"ATTENZIONE: {len(futuri)} righe hanno un risultato su una data futura: escluse dai conti.")
    print(f"Registrati: {len(g)} · conclusi {len(concluse)} · annullati {len(annullate)} · in attesa {len(attesa)}")
    if concluse:
        v = sum(x["esito"] == "V" for x in concluse)
        print(f"Indovinati: {v} su {len(concluse)} = {it(v / len(concluse) * 100, 1)}%")
        conp = [x for x in concluse if x["prob"] is not None]
        if conp:
            attesi = sum(x["prob"] / 100 for x in conp)
            reali = sum(x["esito"] == "V" for x in conp)
            brier = sum((x["prob"] / 100 - (x["esito"] == "V")) ** 2 for x in conp) / len(conp)
            print(f"Attesi secondo le stime: {it(attesi, 1)} · reali: {reali} · scarto {sg(reali - attesi)}{it(reali - attesi, 1)}")
            print(f"Brier score: {it(brier, 3)} (più basso è meglio; 0,25 equivale a tirare a indovinare su esiti al 50%)")

    con_chiusura = [x for x in g if x["chiusura"] and x["quota"]]
    if con_chiusura:
        clv_tutti = [x["quota"] / x["chiusura"] - 1 for x in con_chiusura]
        battute = sum(c > 0 for c in clv_tutti)
        print(f"CLV di tutti i pronostici con quota di chiusura: {pc(sum(clv_tutti) / len(clv_tutti))} su {len(con_chiusura)} · chiusura battuta {battute} volte")

    per_pos = {}
    for x in concluse:
        per_pos.setdefault(x["posizione"] or "senza posizione", []).append(x)
    if len(per_pos) > 1 or "senza posizione" not in per_pos:
        sezione("PER POSIZIONE")
        ordine = ["1", "1°", "2", "2°", "3", "3°", "SICURA", "MEDIA", "HARD", "EXTRA"]
        for nome in sorted(per_pos, key=lambda n: ordine.index(n) if n in ordine else 99):
            xs = per_pos[nome]
            v = sum(x["esito"] == "V" for x in xs)
            ps = [x["prob"] for x in xs if x["prob"] is not None]
            stim = f" | stimati in media al {it(sum(ps) / len(ps), 1)}%" if ps else ""
            print(f"{nome}: indovinati {v} su {len(xs)} = {it(v / len(xs) * 100, 1)}%{stim}")

    # ------------------------------------------------ giocate reali
    reali = [x for x in concluse if x["puntata"] > 0]
    sezione("GIOCATE REALI (righe con puntata)")
    if not reali:
        print("Nessuna giocata reale registrata: i numeri sopra misurano solo la qualità dei pronostici.")
    else:
        puntato = sum(x["puntata"] for x in reali)
        profitto = sum(x["profitto"] for x in reali)
        roi = profitto / puntato
        rend = [x["profitto"] / x["puntata"] for x in reali]
        n = len(rend)
        media = sum(rend) / n
        sd = math.sqrt(sum((r - media) ** 2 for r in rend) / (n - 1)) if n > 1 else 0.0
        ic = 1.96 * sd / math.sqrt(n) if n > 1 else float("nan")
        print(f"Giocate: {n} · vinte {sum(x['esito'] == 'V' for x in reali)} · puntato {it(puntato)} € · profitto {sg(profitto)}{it(profitto)} €")
        print(f"ROI: {pc(roi)}" + (f" · intervallo di confidenza 95%: da {pc(media - ic)} a {pc(media + ic)}" if n > 1 else ""))
        if n > 1 and media - ic <= 0 <= media + ic:
            print("L'intervallo comprende lo zero: il risultato è compatibile con il puro caso.")
        atteso = sum(x["puntata"] * (x["prob"] / 100 * x["quota"] - 1) for x in reali if x["prob"] is not None and x["quota"])
        print(f"Profitto atteso secondo le stime: {sg(atteso)}{it(atteso)} € · reale {sg(profitto)}{it(profitto)} €")
        cum, picco, dd = 0.0, 0.0, 0.0
        for x in sorted(reali, key=lambda x: (x["data"], x["riga"])):
            cum += x["profitto"]
            picco = max(picco, cum)
            dd = max(dd, picco - cum)
        print(f"Massimo drawdown: {it(dd)} € ({it(dd / puntato * 100, 1)}% del puntato)")
        cl = [x for x in reali if x["chiusura"] and x["quota"]]
        if cl:
            clv = [x["quota"] / x["chiusura"] - 1 for x in cl]
            battute = sum(c > 0 for c in clv)
            print(f"CLV medio: {pc(sum(clv) / len(clv))} su {len(cl)} giocate · quota di chiusura battuta {battute} volte su {len(cl)}")
            print("Un CLV positivo e costante è il segnale più affidabile di un vantaggio reale, molto prima del ROI.")
        else:
            print("CLV: nessuna quota di chiusura registrata. Annotala (la quota Eurobet poco prima del calcio d'inizio): è il miglior indicatore precoce.")
        quota_media = sum(x["quota"] for x in reali if x["quota"]) / n
        minimo = CAMPIONE_MINIMO_QUOTE_ALTE if quota_media > 2.5 else CAMPIONE_MINIMO
        if n < minimo:
            print(f"CAMPIONE INSUFFICIENTE: {n} giocate reali su almeno {minimo} necessarie. Nessuna conclusione sul metodo e nessuna modifica ai parametri.")

    # ------------------------------------------------ fasce e calibrazione
    sezione("PER FASCIA DI QUOTA")
    for nome, lo, hi in FASCE_QUOTA:
        xs = [x for x in concluse if x["quota"] and lo <= x["quota"] < hi]
        if not xs:
            continue
        v = sum(x["esito"] == "V" for x in xs)
        pu = sum(x["puntata"] for x in xs)
        pr = sum(x["profitto"] for x in xs)
        soldi = f" | reali: puntato {it(pu)} €, profitto {sg(pr)}{it(pr)} €, ROI {pc(pr / pu)}" if pu else ""
        print(f"{nome}: {len(xs)} pronostici | indovinati {v} ({it(v / len(xs) * 100, 1)}%){soldi}")

    sezione("CALIBRAZIONE (probabilità stimata contro frequenza reale)")
    fasce = {}
    for x in concluse:
        if x["prob"] is not None:
            fasce.setdefault(min(int(x["prob"] // 10) * 10, 90), []).append(x)
    if not fasce:
        print("Nessuna probabilità stimata registrata.")
    for b in sorted(fasce):
        xs = fasce[b]
        stim = sum(x["prob"] for x in xs) / len(xs)
        reale = sum(x["esito"] == "V" for x in xs) / len(xs) * 100
        nota = "  (meno di 30: non indicativo)" if len(xs) < 30 else ""
        print(f"{b}-{b + 10}%: {len(xs):>3} | stimata {it(stim, 1)}% | reale {it(reale, 1)}% | scarto {sg(reale - stim)}{it(reale - stim, 1)} pt{nota}")

    sezione("PERIODO CORRENTE")
    lun = oggi - dt.timedelta(days=oggi.weekday())
    sett = [x for x in g if lun <= x["data"] <= lun + dt.timedelta(days=6)]
    mese = [x for x in g if (x["data"].year, x["data"].month) == (oggi.year, oggi.month)]
    for nome, xs in (("Settimana dal " + lun.isoformat(), sett), ("Mese " + oggi.strftime("%Y-%m"), mese)):
        pu = sum(x["puntata"] for x in xs)
        pr = sum(x["profitto"] for x in xs if x["esito"])
        print(f"{nome}: {len(xs)} pronostici, puntati {it(pu)} €, profitto {sg(pr)}{it(pr)} €")

    sezione("DATI DA VERIFICARE")
    dubbi = [f"riga {x['riga']}: risultato '{x['esito']}' su data futura {x['data'].isoformat()} ({x['partita']})" for x in futuri]
    visti = {}
    for x in tutte:
        k = (x["data"], x["partita"].lower(), x["mercato"].lower(), x["esito_testo"].lower())
        if k in visti:
            dubbi.append(f"righe {visti[k]} e {x['riga']}: stessa giocata registrata due volte ({x['partita']}, {x['esito_testo']})")
        visti.setdefault(k, x["riga"])
    passate = [x for x in attesa if x["data"] < oggi]
    if passate:
        dubbi.append(f"{len(passate)} pronostici con data passata ancora senza risultato: da verificare")
    print("\n".join(dubbi) if dubbi else "Nessuno.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
