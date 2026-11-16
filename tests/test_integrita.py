"""Regressioni numeriche e controlli su copie dei dati locali, senza creare incontri."""
import copy
import csv
import datetime as dt
import json
import shutil
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "analisi-scommesse-calcio" / "scripts")]
import modello as M
import configurazione_modello as CFG
import integrita_calendario as IC
import verifica_fonti as VF
import track_record as TR
import coppe as CP


def caso_numerico():
    # Dati esclusivamente matematici: nessuna squadra, calendario o quota osservata.
    griglia = M.griglia(1.5, 1.5)
    quote = {k: 1 / M.prob(griglia, k) for k in ("1", "X", "2", "Gol")}
    squadra = {"partite": 5, "gol_fatti": 8, "gol_subiti": 8,
               "totale": {"partite": 10, "gol_fatti": 15, "gol_subiti": 15,
                          "gol_fatti_attesi": 15, "gol_subiti_attesi": 15}}
    return {"partita": "Caso numerico di test, senza evento sportivo",
            "lega": {"media_gol_casa": 1.5, "media_gol_trasferta": 1.5},
            "casa": copy.deepcopy(squadra), "trasferta": copy.deepcopy(squadra),
            "assenze_verificate": True, "tipo_quota": "caso numerico di test",
            "quote_riferimento": quote, "quote": {**quote, "Gol": quote["Gol"] * 1.06}}


class GateTest(unittest.TestCase):
    def analizza(self, dati):
        with patch.object(M, "lambda_mercato", return_value=(1.5, 1.5)):
            return M.analizza(dati)

    def test_controllo_positivo_numerico(self):
        r = self.analizza(caso_numerico())
        self.assertTrue(any(v["stato"].startswith("GIOCABILE") for v in r["podio"]))

    def test_prezzo_non_scavalca_assenze(self):
        d = caso_numerico(); d["assenze_verificate"] = False
        r = self.analizza(d)
        self.assertEqual(r["podio"], [])
        self.assertTrue(all(v["stato"] == "DATI INSUFFICIENTI" for v in r["valutazioni"]))

    def test_prezzo_non_scavalca_campione(self):
        d = caso_numerico(); d["casa"]["totale"]["partite"] = 9
        self.assertEqual(self.analizza(d)["podio"], [])

    def test_prezzo_non_scavalca_disaccordo(self):
        d = caso_numerico()
        d["quote_riferimento"].update({"1": 1 / .65, "X": 1 / .20, "2": 1 / .15})
        r = self.analizza(d)
        self.assertIsNotNone(r["disaccordo_1x2"])
        self.assertEqual(r["podio"], [])

    def test_prezzo_non_scavalca_anomalia_relativa(self):
        d = caso_numerico()
        d["quote_riferimento"]["Esatto 2-2"] = 25.0
        d["quote"]["Esatto 2-2"] = 28.0
        r = self.analizza(d)
        voce = next(v for v in r["valutazioni"] if v["mercato"] == "Esatto 2-2")
        self.assertEqual(voce["stato"], "ANOMALIA DI MERCATO")

    def test_senza_ancora_completa_nessuna_classificazione_giocabile(self):
        d = caso_numerico(); d["quote"] = {"Gol": d["quote"]["Gol"]}
        d["quote_riferimento"] = {"Gol": d["quote_riferimento"]["Gol"]}
        r = self.analizza(d)
        self.assertEqual(r["podio"], [])
        self.assertEqual(r["valutazioni"][0]["stato"], "SENZA RIFERIMENTO 1X2 REALE")


class ProbabilitaTest(unittest.TestCase):
    def test_soglie_coerenti_anche_ai_confini(self):
        for p in (.8, .5, .41, .405, .209, .205, .1):
            q = M.quota_minima(p)
            self.assertGreaterEqual(p * q - 1 + 1e-12, M.soglia_valore(q))

    def test_probabilita_non_valide(self):
        for p in (0, -1, 2, float("nan"), float("inf")):
            with self.assertRaises(ValueError): M.quota_minima(p)

    def test_matrice_normalizzata(self):
        g = M.griglia(1.6, 1.2)
        self.assertAlmostEqual(sum(map(sum, g)), 1, places=12)
        self.assertAlmostEqual(sum(M.prob(g, k) for k in ("1", "X", "2")), 1, places=12)
        self.assertAlmostEqual(M.prob(g, "Gol") + M.prob(g, "No Gol"), 1, places=12)


class ConfigurazioneTest(unittest.TestCase):
    def test_baseline_esplicita_congelata(self):
        c = CFG.carica()
        self.assertEqual(c["versione_engine"], M.VERSIONE_MODELLO)
        self.assertIs(c["apprendimento_automatico"], False)
        self.assertEqual(c["peso_dati"], 0.0)

    def test_parametri_non_finiti_rifiutati(self):
        c = CFG.carica(); c["peso_dati"] = float("nan")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "config.json"; p.write_text(json.dumps(c))
            with self.assertRaises(ValueError): CFG.carica(p)


class FontiTest(unittest.TestCase):
    def test_permesso_richiede_documentazione(self):
        d = {"fonti": {"x": {"piano_verificato": True, "permessi": {"download": True}, "evidenze": []}}}
        self.assertTrue(VF.impedimenti(d, "download"))

    def test_permesso_richiesto_distinto_dagli_altri(self):
        d = {"fonti": {"x": {"piano_verificato": True, "evidenze": ["Riferimento di prova"], "permessi": {"download": True}}}}
        self.assertFalse(VF.impedimenti(d, "download"))
        self.assertTrue(VF.impedimenti(d, "commerciale"))
        self.assertTrue(VF.impedimenti(d, "download", ["sconosciuta"]))

    def test_registro_corrente_blocca_impieghi_non_verificati(self):
        d = json.loads(VF.DEFAULT.read_text())
        for operazione in ("download", "condivisione", "commerciale", "addestramento"):
            self.assertTrue(VF.impedimenti(d, operazione))


class CalendarioTest(unittest.TestCase):
    def setUp(self):
        cal = json.loads((ROOT / "dati" / "calendario.json").read_text())
        self.partite = cal["serie-a"]["turni"]["12"]["partite"]
        self.squadre = {p[k] for p in self.partite for k in ("casa", "ospite")}

    def test_duplicazione_record_esistente_rifiutata(self):
        self.assertTrue(IC.errori_turno(self.partite + self.partite[:1], self.squadre))

    def test_solo_struttura_non_certifica_fonte(self):
        self.assertEqual(IC.errori_turno(self.partite, self.squadre), [])

    def test_partita_iniziata_esclusa(self):
        p = self.partite[0]
        inizio = dt.datetime.fromisoformat(p["giorno"] + "T" + p["ora"]).replace(tzinfo=ZoneInfo("Europe/Rome"))
        self.assertTrue(IC.futura(p, inizio - dt.timedelta(seconds=1)))
        self.assertFalse(IC.futura(p, inizio))

    def test_ora_mancante_non_inventata(self):
        p = dict(self.partite[0], ora=None)
        inizio = dt.datetime.fromisoformat(p["giorno"] + "T00:00").replace(tzinfo=ZoneInfo("Europe/Rome"))
        self.assertFalse(IC.futura(p, inizio))


class RegistroTest(unittest.TestCase):
    def setUp(self):
        cal = json.loads((ROOT / "dati/calendario.json").read_text())
        p = cal["serie-a"]["turni"]["12"]["partite"][0]
        self.inizio = dt.datetime.fromisoformat(p["giorno"] + "T" + p["ora"]).replace(tzinfo=IC.FUSO)
        self.previsione = {"lega": "serie-a", "casa": p["casa"], "ospite": p["ospite"], "giorno": p["giorno"],
                           "inizio_utc": self.inizio.astimezone(dt.timezone.utc).isoformat(), "p1": .4, "pX": .3, "p2": .3}

    def test_previsione_congelata_con_ora_e_versione(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "log.csv"
            prima = TR.aggiorna_live(path, [self.previsione], {}, adesso=self.inizio-dt.timedelta(hours=2))
            modifica = dict(self.previsione, p1=.5, pX=.2)
            dopo = TR.aggiorna_live(path, [modifica], {}, adesso=self.inizio-dt.timedelta(hours=1))
            self.assertEqual(len(dopo), 1)
            self.assertEqual(float(dopo[0]["p1"]), prima[0]["p1"])
            self.assertEqual(dopo[0]["registrata"], prima[0]["registrata"])
            self.assertTrue(TR.prova_temporale(dopo[0]))

    def test_non_registra_dopo_inizio_o_senza_ora(self):
        with tempfile.TemporaryDirectory() as d:
            for p, now in [(self.previsione, self.inizio), (dict(self.previsione, inizio_utc=""), self.inizio-dt.timedelta(hours=2))]:
                self.assertEqual(TR.aggiorna_live(Path(d)/"log.csv", [p], {}, adesso=now), [])

    def test_vecchie_righe_non_acquisiscono_prove_inventate(self):
        vecchie = [r for r in TR.leggi_log(ROOT / "dati/storico_live.csv") if not r.get("inizio_utc")]
        self.assertGreater(len(vecchie), 0)
        self.assertTrue(all(not TR.prova_temporale(r) for r in vecchie))
        self.assertEqual(TR.riepilogo_live(vecchie)["senza_prova_temporale"], len(vecchie))

    def test_registro_coppe_duplicato_non_viene_azzerato(self):
        r = next(iter(CP.carica_log(ROOT / "dati/coppe/previsioni_CL.csv").values()))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "duplicato.csv"
            with path.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(r)); writer.writeheader(); writer.writerows([r, r])
            with self.assertRaises(ValueError): CP.carica_log(path)

    def test_coppe_non_riscrive_previsioni_esistenti(self):
        # Elabora solo copie dei dati già presenti; nessun download o incontro inventato.
        with tempfile.TemporaryDirectory() as d:
            copia = Path(d) / "coppe"
            shutil.copytree(ROOT / "dati/coppe", copia)
            log = copia / "previsioni_CL.csv"
            prima = CP.carica_log(log)
            with patch.object(CP, "D", str(copia)):
                CP.elabora(dt.date(2026, 11, 15), scrivi=True)
            dopo = CP.carica_log(log)
            self.assertGreater(len(prima), 0)
            for k, r in prima.items():
                for campo in ("p1", "pX", "p2", "rh", "ra", "lh", "la", "w_dom"):
                    self.assertEqual(r[campo], dopo[k][campo])


if __name__ == "__main__":
    unittest.main()
