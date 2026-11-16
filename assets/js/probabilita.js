/* Calcoli di presentazione: stessa soglia a fasce di modello.py. */
(function (root) {
  "use strict";
  function quotaMinima(probabilita) {
    if (!Number.isFinite(probabilita) || probabilita <= 0 || probabilita > 1) return null;
    var fasce = [[2.50, 0.03], [5.0, 0.05], [Infinity, 0.08]];
    for (var i = 0; i < fasce.length; i++) {
      var prezzo = (1 + fasce[i][1]) / probabilita;
      if (prezzo <= fasce[i][0]) return Math.ceil(prezzo * 100 - 1e-9) / 100;
    }
  }
  var api = Object.freeze({ quotaMinima: quotaMinima });
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.QuantMath = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
