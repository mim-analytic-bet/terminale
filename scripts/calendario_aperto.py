#!/usr/bin/env python3
"""Calendario delle giornate da fonte aperta (openfootball, dominio pubblico CC0): abbinamenti casa/ospite di TUTTA la stagione.

Cosa e' affidabile e cosa no (verificato il 13/11/2026 su Serie A, Premier, LaLiga, Bundesliga):
- gli ABBINAMENTI di ogni giornata sono completi e affidabili;
- giorno e orario SONO PROVVISORI finche' la lega non li fissa: le giornate lontane hanno un solo giorno segnaposto e nessun orario.
  Anche per le giornate vicine, per Serie A giornata 12 openfootball e calendario.json divergono su 5 partite su 10 (vedi confronta()).
Per questo qui si usano SOLO gli abbinamenti: il giorno e' marcato 'provvisorio', l'ora resta vuota, e nulla di manuale viene mai sovrascritto.

Uso:  python3 scripts/calendario_aperto.py          scarica e scrive dati/calendario_openfootball.json (se fallisce lascia il file precedente)
"""
import datetime as dt, difflib, json, os, re, sys, unicodedata, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(BASE, "dati", "calendario_openfootball.json")
RAW = "https://raw.githubusercontent.com/openfootball/{repo}/master/{path}"

# lega -> (repo, percorso con {S} = stagione tipo 2026-27, file CSV football-data con i nomi squadra usati dalla dashboard)
FONTI = {
    "serie-a": ("italy", "{S}/1-seriea.txt", "I1"),
    "premier": ("england", "{S}/1-premierleague.txt", "E0"),
    "liga": ("espana", "{S}/1-liga.txt", "SP1"),
    "bundesliga": ("deutschland", "{S}/1-bundesliga.txt", "D1"),
    "ligue1": ("europe", "france/{S}_fr1.txt", "F1"),
}
FUSO_ORA = {"premier": 1}  # openfootball scrive l'ora locale: Inghilterra = Italia - 1h (usata solo se l'orario e' confermato)

MESI = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}

# Nomi openfootball (normalizzati) -> nome nei CSV football-data. Quelli non elencati si abbinano per prefissi di parola; l'abbinamento
# e' accettato solo se copre TUTTE le squadre del CSV una a una, altrimenti la lega viene saltata con un avviso (mai abbinamenti a caso).
ALIAS = {
    "fc internazionale milano": "Inter", "acf fiorentina": "Fiorentina", "ac monza": "Monza", "us sassuolo calcio": "Sassuolo",
    "manchester city fc": "Man City", "manchester united fc": "Man United", "nottingham forest fc": "Nott'm Forest",
    "brighton & hove albion fc": "Brighton", "tottenham hotspur fc": "Tottenham", "hull city afc": "Hull",
    "deportivo alaves": "Alaves", "athletic club": "Ath Bilbao", "club atletico de madrid": "Ath Madrid", "real betis balompie": "Betis",
    "rc celta de vigo": "Celta", "rcd espanyol de barcelona": "Espanol", "rc deportivo la coruna": "La Coruna", "malaga cf": "Malaga",
    "real racing club de santander": "Santander", "real sociedad de futbol": "Sociedad", "rayo vallecano de madrid": "Vallecano",
    "fc bayern munchen": "Bayern Munich", "borussia dortmund": "Dortmund", "eintracht frankfurt": "Ein Frankfurt", "1. fc koln": "FC Koln",
    "hamburger sv": "Hamburg", "borussia monchengladbach": "M'gladbach", "1. fsv mainz 05": "Mainz", "fc schalke 04": "Schalke 04",
    "1. fc union berlin": "Union Berlin", "sv werder bremen": "Werder Bremen", "tsg 1899 hoffenheim": "Hoffenheim", "bayer 04 leverkusen": "Leverkusen",
    "sc paderborn 07": "Paderborn", "sv 07 elversberg": "Elversberg", "sc freiburg": "Freiburg", "vfb stuttgart": "Stuttgart", "fc augsburg": "Augsburg",
    "real madrid cf": "Real Madrid", "fc barcelona": "Barcelona",
}
# Ligue 1: i nomi openfootball non sono stati verificati a mano; frammenti riconosciuti nell'ordine (primo che combacia)
FRAMMENTI = [("saint germain", "Paris SG"), ("saint-germain", "Paris SG"), ("paris fc", "Paris FC"), ("rennais", "Rennes"), ("lyonnais", "Lyon"),
             ("brestois", "Brest"), ("marseille", "Marseille"), ("havre", "Le Havre"), ("le mans", "Le Mans")]
STOP = {"fc", "cf", "ac", "as", "ss", "us", "afc", "sc", "sv", "ud", "rc", "rcd", "ca", "club", "calcio", "de", "la", "le", "del", "the", "1", "1909",
        "1913", "1907", "1899", "04", "05", "07", "29"}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9&.' -]", " ", s)).strip()


def _tok(s):
    return [t for t in re.split(r"[ .'\-]+", norm(s)) if t and t not in STOP]


def abbina_nomi(nomi_of, nomi_csv):
    """{nome openfootball: nome CSV}. None se l'abbinamento non e' completo, univoco e 1:1 (per non scrivere mai partite sbagliate)."""
    csv_set, out = set(nomi_csv), {}
    for n in nomi_of:
        k = norm(n); c = ALIAS.get(k)
        if c is None:
            for fr, nm in FRAMMENTI:
                if fr in k: c = nm; break
        if c is None:
            cand = [x for x in csv_set if all(any(w.startswith(t) for w in _tok(n)) for t in _tok(x))] if csv_set else []
            if len(cand) == 1: c = cand[0]
            elif not cand:
                best = difflib.get_close_matches(k, [norm(x) for x in csv_set], n=1, cutoff=0.82)
                c = next((x for x in csv_set if norm(x) == best[0]), None) if best else None
        if c is None or c not in csv_set: return None, n
        out[n] = c
    if len(set(out.values())) != len(out) or set(out.values()) != csv_set: return None, "copertura incompleta"
    return out, None


RIGA_PARTITA = re.compile(r"^\s+(?:(\d{1,2}:\d{2})\s+)?(\S.*?)\s+v\s+(\S.*?)(?:\s+(\d+-\d+)(?:\s+\([^)]*\))?)?\s*$")
RIGA_DATA = re.compile(r"^\s+(?:[A-Za-z]{3})\s+([A-Za-z]{3})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$")
RIGA_TURNO = re.compile(r"^[▪»]\s*(?:Matchday|Round|Giornata|Journee|Journée|Spieltag)\s+(\d+)", re.I)


def parsa(testo):
    """Testo openfootball -> {n_giornata: [ {casa, ospite, giorno, ora, giocata} ]}. L'ora e' quella scritta (locale), None se assente."""
    turni, n, anno, ult_mese, giorno, ora = {}, None, None, None, None, None
    for riga in testo.splitlines():
        m = RIGA_TURNO.match(riga)
        if m: n, giorno, ora = int(m.group(1)), None, None; continue
        if n is None: continue
        d = RIGA_DATA.match(riga)
        if d:
            mese = MESI.get(d.group(1).lower())
            if mese is None: continue
            if d.group(3): anno = int(d.group(3))
            elif anno is not None and ult_mese is not None and mese < ult_mese: anno += 1
            if anno is None: continue
            ult_mese = mese; giorno = dt.date(anno, mese, int(d.group(2))).isoformat(); ora = None; continue
        p = RIGA_PARTITA.match(riga)
        if p and giorno:
            if p.group(1): ora = p.group(1)
            turni.setdefault(n, []).append({"casa": p.group(2).strip(), "ospite": p.group(3).strip(), "giorno": giorno, "ora": ora, "giocata": bool(p.group(4))})
    return turni


def scarica(stagione=None):
    oggi = dt.date.today(); y = stagione or (oggi.year if oggi.month >= 7 else oggi.year - 1); S = f"{y}-{str(y + 1)[2:]}"
    out = {"scaricato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"), "stagione": S, "fonte": "openfootball (CC0)", "leghe": {}}
    for key, (repo, path, _) in FONTI.items():
        testo = None
        for ramo in ("master", "main"):
            try:
                url = RAW.format(repo=repo, path=path.format(S=S)).replace("/master/", f"/{ramo}/")
                with urllib.request.urlopen(url, timeout=40) as r: testo = r.read().decode("utf-8"); break
            except Exception as e: err = e
        if testo is None: print(f"AVVISO calendario aperto: {key} non scaricato ({err})"); continue
        t = parsa(testo)
        if len(t) < 10: print(f"AVVISO calendario aperto: {key} non interpretabile ({len(t)} giornate trovate)"); continue
        out["leghe"][key] = {"turni": {str(n): v for n, v in sorted(t.items())}}
        print(f"calendario aperto: {key} {S}: {sum(len(v) for v in t.values())} partite in {len(t)} giornate")
    if not out["leghe"]: print("calendario aperto: nessun download riuscito, tengo il file precedente"); return False
    # una lega non scaricata questa volta non cancella quella gia' salvata
    if os.path.exists(DEST):
        try:
            vecchio = json.load(open(DEST, encoding="utf-8"))
            if vecchio.get("stagione") == S:
                for k, v in vecchio.get("leghe", {}).items(): out["leghe"].setdefault(k, v)
        except Exception: pass
    json.dump(out, open(DEST, "w", encoding="utf-8"), ensure_ascii=False)
    return True


def carica(base=BASE):
    p = os.path.join(base, "dati", "calendario_openfootball.json")
    if not os.path.exists(p): return None
    try: return json.load(open(p, encoding="utf-8"))
    except Exception: return None


def turno_confermato(partite):
    """Vero se la giornata ha gia' orari veri: almeno due slot (giorno, ora) diversi. Un solo giorno segnaposto = provvisorio."""
    return len({(e["giorno"], e["ora"]) for e in partite}) >= 2 and any(e["ora"] for e in partite)


def per_lega(cal, key, nomi_csv):
    """{n_giornata: {'confermato': bool, 'partite': [ {casa, ospite, giorno, ora, giocata} ]}} coi nomi dei CSV, oppure (None, motivo)."""
    if not cal or key not in (cal.get("leghe") or {}): return None, "fonte non disponibile"
    turni = cal["leghe"][key]["turni"]
    nomi = {e[k] for v in turni.values() for e in v for k in ("casa", "ospite")}
    mappa, perche = abbina_nomi(sorted(nomi), nomi_csv)
    if mappa is None: return None, f"nomi squadra non abbinabili ({perche})"
    out = {}
    for n, v in turni.items():
        conf = turno_confermato(v)
        ore = FUSO_ORA.get(key, 0)
        lista = []
        for e in v:
            ora = e["ora"]
            if ora and ore:
                h, mi = ora.split(":"); ora = f"{(int(h) + ore) % 24:02d}:{mi}"
            lista.append({"casa": mappa[e["casa"]], "ospite": mappa[e["ospite"]], "giorno": e["giorno"], "ora": ora if conf else None, "giocata": e["giocata"]})
        out[int(n)] = {"confermato": conf, "partite": lista}
    return out, None


def confronta(manuale, of_turni):
    """Differenze tra il calendario manuale e openfootball sulle stesse partite (solo giornate con orari confermati). Lista di stringhe."""
    righe = []
    for n, t in of_turni.items():
        if not t["confermato"]: continue
        man = {(e["casa"], e["ospite"]): e for e in (manuale.get(str(n)) or {}).get("partite", [])}
        for e in t["partite"]:
            m = man.get((e["casa"], e["ospite"]))
            if m and (m.get("giorno") != e["giorno"] or (m.get("ora") and e["ora"] and m["ora"] != e["ora"])):
                righe.append(f"giornata {n} {e['casa']}-{e['ospite']}: manuale {m.get('giorno')} {m.get('ora')} | openfootball {e['giorno']} {e['ora']}")
    return righe


if __name__ == "__main__":
    sys.exit(0 if scarica() else 1)
