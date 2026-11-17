"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const root = path.join(__dirname, "..");
const { quotaMinima } = require(path.join(root, "assets/js/probabilita.js"));
const { riepilogo, freschezza } = require(path.join(root, "assets/js/stato-dati.js"));
const { contesto } = require(path.join(root, "assets/js/contesto.js"));
for (const p of [.8, .5, .41, .405, .209, .205, .1]) {
  const q = quotaMinima(p), soglia = q <= 2.5 ? .03 : q <= 5 ? .05 : .08;
  assert.ok(p * q - 1 + 1e-12 >= soglia);
}
for (const p of [0, -1, 2, NaN, Infinity]) assert.equal(quotaMinima(p), null);
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
assert.equal(html, fs.readFileSync(path.join(root, "scheda-partita-dashboard.html"), "utf8"));
let scripts = 0;
for (const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) {
  new vm.Script(match[1], { filename: "script-inline-" + scripts++ });
}
assert.ok(scripts > 1);
assert.ok(!html.includes("Puntata consigliata: 2.00"));
assert.ok(!html.includes("kellyQuarter"));
assert.ok(!html.includes("Puntata (2% Flat)"));
assert.ok(!html.includes("probCongiunta *="));
assert.ok(!html.includes("function coppie("));
assert.ok(!html.includes("Confidenza Statistica:"));
assert.ok(!html.includes("avviaRotazioneAutomatica"));
assert.ok(html.includes('onclick="aggiornaPronosticiScorrevoli(${i})"'));
for (const file of ["assets/js/stato-dati.js", "assets/js/probabilita.js", "assets/js/contesto.js"]) new vm.Script(fs.readFileSync(path.join(root, file), "utf8"));
// Cambiare solo la data di elaborazione non deve ringiovanire i risultati.
const meta = {dati_fino: {locale: "2026-11-08"}, aggiornato: "2026-11-15T21:00:00Z"};
const a = riepilogo({}, meta, Date.parse("2026-11-15T21:00:00Z"));
const b = riepilogo({}, {...meta, aggiornato: "2026-11-15T22:00:00Z"}, Date.parse("2026-11-15T21:00:00Z"));
assert.equal(a.giorni, 7); assert.deepEqual(a, b);
assert.ok(html.includes('src="./assets/js/stato-dati.js"'));
assert.ok(!html.includes("media.api-sports.io/football/teams/"));
const { spawnSync } = require("node:child_process");
const estrazione = spawnSync("python3", ["-B", "-c", "import sys,json;sys.path.insert(0,'scripts');from verifica_snapshot import blocco;from pathlib import Path;s=Path('index.html').read_text();p=blocco(s,'DATA_PRO');print(json.dumps([{k:next(iter(v['turni'].values()))['partite'][0] for k,v in p.items()},blocco(s,'DATA_TRACK')]))"], {cwd:root,encoding:"utf8"});
assert.equal(estrazione.status, 0, estrazione.stderr || String(estrazione.error || ""));
const [pro,track] = JSON.parse(estrazione.stdout);
for (const [key,partita] of Object.entries(pro)) {
  const c = contesto(partita,track,key);
  assert.ok(c.partite > 0); assert.ok(Number.isFinite(c.errore));
  assert.ok(Number.isFinite(c.confronto));
}
console.log("Verificati calcoli di soglia, sintassi di " + scripts + " script e sospensione dei percorsi di puntata/composizione.");

{
  const t0 = Date.parse("2026-11-17T15:00:00Z");
  const a = freschezza("2026-11-17T13:00:00Z", "2026-11-15", t0);
  assert.equal(a.ore, 2); assert.equal(a.livelloPagina, "verde"); assert.equal(a.giorni, 2); assert.equal(a.livelloRisultati, "verde");
  const b = freschezza("2026-11-17T01:00:00Z", "2026-11-08", t0);
  assert.equal(b.livelloPagina, "giallo"); assert.equal(b.giorni, 9); assert.equal(b.livelloRisultati, "rosso");
  assert.equal(freschezza(null, null, t0).livelloPagina, "grigio");
  assert.ok(html.includes("function statoQuote(") && html.includes("Senza quote"));
}
