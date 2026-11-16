(function (root) {
  "use strict";
  const leghe = {"serie-a":"Serie A", premier:"Premier League", liga:"LaLiga", bundesliga:"Bundesliga", ligue1:"Ligue 1"};
  function contesto(m, track, key) {
    const coppa = Boolean(m.osservazione), storico = coppa ? (m.osservazione.backtest || {}) : ((track.leghe || {})[leghe[key]] || {});
    return {
      coppa,
      metodo: coppa ? "Elo europeo con forma nazionale" : "Poisson con correzione Dixon-Coles",
      partite: coppa ? storico.n_test : storico.n,
      errore: storico.brier_modello,
      confronto: coppa ? storico.brier_frequenze_base : storico.brier_mercato,
      riferimento: coppa ? "frequenze storiche degli esiti" : "probabilità ricavate dalle quote storiche",
      quote: Boolean(m.quoteMercato && Object.keys(m.quoteMercato).length),
      assenze: Boolean(m.assenti && m.assenti.controllato)
    };
  }
  function render(m, track, key) {
    const c = contesto(m, track, key);
    function riempi(id, titolo, righe) {
      const el = document.getElementById(id); if (!el) return;
      el.replaceChildren();
      const h = document.createElement("h3"); h.textContent = titolo; h.className = "contesto-titolo"; el.append(h);
      for (const riga of righe) { const p = document.createElement("p"); p.textContent = riga; p.className = "contesto-testo"; el.append(p); }
    }
    riempi("box-schedina-interattiva", "Metodo della scheda", [c.metodo,
      "I gol attesi sono stime matematiche. Le percentuali descrivono il modello e non misurano la certezza del risultato."]);
    riempi("corpo-combo-1", "Confronto storico", [
      c.partite ? (c.coppa ? "Backtest caricato su Champions League: " : "Campione di valutazione: ") + c.partite + " incontri." : "Campione di valutazione non disponibile.",
      ...(key === "europa" ? ["Non è disponibile un backtest separato dell’Europa League: questo campione non dimostra l’accuratezza su questa competizione."] : []),
      Number.isFinite(c.errore) && Number.isFinite(c.confronto) ? "Errore Brier del modello: " + c.errore + "; riferimento: " + c.confronto + " (" + c.riferimento + "). Un valore più basso indica minore errore." : "Confronto dell’errore non disponibile.",
      "La verifica storica riguarda il campione indicato. Le prestazioni future richiedono previsioni registrate prima degli eventi."
    ]);
    riempi("corpo-combo-2", "Disponibilità della scheda", [
      c.quote ? "Quote presenti nel file di origine: verificare operatore e data di rilevazione." : "Quote rilevate non disponibili: il confronto con prezzi attuali è assente.",
      c.assenze ? "Assenze segnalate dalla fonte, escluse dal calcolo delle probabilità." : "Assenze e formazioni non verificate, escluse dal calcolo delle probabilità.",
      "Il calendario caricato richiede riscontro con la fonte ufficiale. Le date provvisorie sono indicate nella scheda."
    ]);
  }
  root.QuantContesto = {contesto, render};
  if (typeof module === "object" && module.exports) module.exports = {contesto};
})(typeof globalThis === "undefined" ? this : globalThis);
