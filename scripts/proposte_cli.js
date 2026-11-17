#!/usr/bin/env node
// Calcola le proposte (Eventi Combinati, Cluster Multi-Evento) con la STESSA funzione che usa la pagina (assets/js/combo.js).
// Ingresso (stdin): {"data_pro": {...}, "adesso": "2026-11-19T09:00:00+01:00"}
// Uscita (stdout): lista JSON di proposte con le gambe, il moltiplicatore e la probabilita' congiunta del modello.
"use strict";
var fs = require("fs");
var path = require("path");
var core = require(path.join(__dirname, "..", "assets", "js", "combo.js"));
var input = JSON.parse(fs.readFileSync(0, "utf8"));
var R = core.calcola(input.data_pro, new Date(input.adesso));
function paccheta(lista) {
  return lista.map(function (o) {
    var molt = 1, prob = 1;
    o.legs.forEach(function (c) { molt *= c.q; prob *= c.p; });
    return { cod: o.cod, etichetta: o.etichetta, legs: o.legs, molt: molt, prob: prob };
  });
}
process.stdout.write(JSON.stringify({
  finestra: R.etichettaFinestra,
  coppe: R.isCoppaBlock,
  proposte: paccheta(R.P1).concat(paccheta(R.P2))
}));
