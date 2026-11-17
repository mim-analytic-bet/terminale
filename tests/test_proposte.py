"""Registro delle proposte: prova temporale, immutabilita', valutazione, equivalenza con la logica della pagina."""
import copy, datetime as dt, json, shutil, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts")]
import registro_proposte as RP

UTC = dt.timezone.utc


def partita(i, casa, ospite, giorno, inizio, p1=0.58, pover=0.62, pgol=0.60):
    seg = lambda p: {"p": p}
    return {"id": i, "label": f"{casa} - {ospite}", "data": "Sabato 21 Nov · 15:00", "inizioUtc": inizio,
            "chiave": {"casa": casa, "ospite": ospite, "giorno": giorno}, "quoteMercato": None,
            "fasi": {"1": {"seg1": seg(p1), "seg2": seg(0.25), "seg3": seg(1 - p1 - 0.25)},
                     "2": {"seg1": seg(pgol), "seg2": seg(1 - pgol)},
                     "3": {"seg1": seg(pover), "seg2": seg(1 - pover)}}}


def dati(inizio="2026-11-21T14:00:00+00:00"):
    ps = [partita(1, "A", "B", "2026-11-21", inizio), partita(2, "C", "D", "2026-11-21", inizio),
          partita(3, "E", "F", "2026-11-21", inizio), partita(4, "G", "H", "2026-11-21", inizio)]
    return {"serie-a": {"nome": "Serie A", "turni": {"12": {"dataFine": "2026-11-23", "partite": ps}}}}


ADESSO = dt.datetime(2026, 11, 19, 8, 0, tzinfo=UTC)


class TestProposte(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.path = str(Path(self.d) / "p.csv")
    def tearDown(self): shutil.rmtree(self.d, ignore_errors=True)

    def proposte(self, pro=None, adesso=ADESSO):
        ps, err = RP.calcola_proposte(pro or dati(), adesso); self.assertIsNone(err); return ps

    def test_calcolo_node_produce_proposte(self):
        self.assertGreater(len(self.proposte()), 0)

    def test_registra_una_volta_sola(self):
        ps = self.proposte()
        _, n1, _ = RP.aggiorna(self.path, ps, {}, "cfg", "2.2", ADESSO)
        _, n2, _ = RP.aggiorna(self.path, ps, {}, "cfg", "2.2", ADESSO)
        self.assertGreater(n1, 0); self.assertEqual(n2, 0)

    def test_prima_registrazione_immutabile(self):
        ps = self.proposte(); RP.aggiorna(self.path, ps, {}, "cfg", "2.2", ADESSO)
        prima = {r["id"]: (r["registrata"], r["molt"], r["g1_q"], r["g1_tipo"]) for r in RP.leggi(self.path)}
        ps2 = copy.deepcopy(ps)
        for p in ps2:
            for g in p["legs"]: g["q"] *= 1.1
            p["molt"] *= 1.2
        RP.aggiorna(self.path, ps2, {}, "cfg", "2.3", ADESSO + dt.timedelta(hours=3))
        dopo = {r["id"]: (r["registrata"], r["molt"], r["g1_q"], r["g1_tipo"]) for r in RP.leggi(self.path)}
        self.assertEqual(prima, dopo)

    def test_scarta_partite_gia_iniziate_o_senza_orario(self):
        ps = self.proposte()
        _, n, s = RP.aggiorna(self.path, ps, {}, "cfg", "2.2", dt.datetime(2026, 11, 21, 15, 0, tzinfo=UTC))
        self.assertEqual(n, 0); self.assertEqual(s, len(ps))
        senza = copy.deepcopy(ps)
        for p in senza:
            p["legs"][0]["inizioUtc"] = None
        _, n, s = RP.aggiorna(self.path + "2", senza, {}, "cfg", "2.2", ADESSO)
        self.assertEqual(n, 0)

    def test_orario_senza_fuso_non_registra(self):
        ps = self.proposte()
        for p in ps:
            for g in p["legs"]: g["inizioUtc"] = "2026-11-21T14:00:00"
        _, n, _ = RP.aggiorna(self.path, ps, {}, "cfg", "2.2", ADESSO)
        self.assertEqual(n, 0)

    def test_esiti_mercati(self):
        e = RP.esito_mercato
        self.assertTrue(e("1", 2, 1)); self.assertFalse(e("1", 1, 1)); self.assertTrue(e("1X", 1, 1)); self.assertTrue(e("X2", 0, 1))
        self.assertTrue(e("Over 2,5", 2, 1)); self.assertFalse(e("Over 2,5", 1, 1)); self.assertTrue(e("Under 2,5", 1, 1))
        self.assertTrue(e("Gol", 1, 1)); self.assertTrue(e("No Gol", 2, 0)); self.assertIsNone(e("Sconosciuto", 1, 1))

    def test_valutazione_a_risultato_noto(self):
        ps = self.proposte(); righe, _, _ = RP.aggiorna(self.path, ps, {}, "cfg", "2.2", ADESSO)
        r0 = righe[0]; self.assertEqual(r0["stato"], "aperta")
        arch = {"serie-a": []}
        for r in righe:
            for i in range(1, int(r["n_gambe"]) + 1):
                arch["serie-a"].append({"casa": r[f"g{i}_casa"], "ospite": r[f"g{i}_ospite"], "data": dt.date.fromisoformat(r[f"g{i}_giorno"]), "gc": 2, "go": 1})
        righe, _, _ = RP.aggiorna(self.path, ps, arch, "cfg", "2.2", ADESSO + dt.timedelta(days=3))
        for r in righe:
            self.assertEqual(r["stato"], "valutata"); self.assertIn(r["esito"], ("V", "P"))
            self.assertEqual(r["registrata"], righe[0]["registrata"])  # la prova temporale non cambia
        self.assertEqual(RP.riepilogo(righe)["valutate"], len(righe))

    def test_riepilogo_separa_quote_equa_e_reale(self):
        base = {"cod": "P1", "n_gambe": "2", "stato": "valutata", "esito": "V", "prob": "0.36", "g1_tipo": "reale", "g2_tipo": "reale"}
        righe = [dict(base), {**base, "g2_tipo": "equa", "esito": "P"}, {**base, "g2_tipo": "derivata", "stato": "aperta", "esito": ""}]
        r = RP.riepilogo(righe)["per_tipo"]
        self.assertEqual(r["quota:reale"]["valutate"], 1); self.assertEqual(r["quota:equa"]["vinte"], 0)
        self.assertEqual(r["quota:derivata"]["registrate"], 1); self.assertIsNone(r["quota:derivata"]["brier"])
        self.assertEqual(r["P1"]["registrate"], 3)

    def test_senza_risultato_resta_aperta(self):
        ps = self.proposte(); RP.aggiorna(self.path, ps, {}, "cfg", "2.2", ADESSO)
        righe, _, _ = RP.aggiorna(self.path, ps, {"serie-a": []}, "cfg", "2.2", ADESSO)
        self.assertTrue(all(r["stato"] == "aperta" for r in righe))

    def test_equivalenza_con_la_pagina(self):
        """La pagina e il registro usano la stessa funzione: l'HTML dei box deve contenere le stesse partite delle proposte registrate."""
        import subprocess
        h = ROOT / "tests" / "_harness_combo.js"
        if not shutil.which("node"): self.skipTest("node non disponibile")
        ps = self.proposte()
        prog = ("global.document={getElementById:function(i){global.__e=global.__e||{};return global.__e[i]=global.__e[i]||{style:{},querySelectorAll:function(){return []},set innerHTML(v){this._h=v},get innerHTML(){return this._h||''}}}};"
                "global.setInterval=function(){};global.setTimeout=function(f){f()};global.DATA_PRO=JSON.parse(process.argv[2]);"
                "require(process.argv[1]);console.log(JSON.stringify([__e['corpo-combo-1']?__e['corpo-combo-1'].innerHTML:'',__e['corpo-combo-2']?__e['corpo-combo-2'].innerHTML:'']))")
        # La data fissa si ottiene con TZ e un Date sostituito
        prog = "const R=Date;global.Date=class extends R{constructor(...a){a.length?super(...a):super('2026-11-19T09:00:00+01:00')}static now(){return new R('2026-11-19T09:00:00+01:00').getTime()}};" + prog
        r = subprocess.run(["node", "-e", prog, str(ROOT / "assets" / "js" / "combo.js"), json.dumps(dati())], capture_output=True, text=True, env={"TZ": "Europe/Rome", "PATH": "/usr/bin:/bin:/usr/local/bin"}, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        html = "".join(json.loads(r.stdout))
        # La pagina mostra una scheda per riquadro (carosello): deve coincidere con la prima proposta registrabile di ciascun gruppo.
        primo_p1 = next(p for p in ps if p["cod"] == "P1")
        primo_p2 = next(p for p in ps if p["cod"] in ("P2", "P2S"))
        for p in (primo_p1, primo_p2):
            for g in p["legs"]: self.assertIn(g["lbl"], html)
            self.assertIn("%.2f" % p["molt"], html)


if __name__ == "__main__":
    unittest.main()
