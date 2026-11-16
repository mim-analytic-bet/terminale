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
  }
  root.QuantContesto = {contesto, render};
  if (typeof module === "object" && module.exports) module.exports = {contesto};
})(typeof globalThis === "undefined" ? this : globalThis);
