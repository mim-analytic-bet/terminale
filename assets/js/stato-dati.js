(function (root) {
  "use strict";
  function riepilogo(pro, meta, now) {
    let partite = 0, conQuote = 0;
    for (const lega of Object.values(pro || {})) {
      for (const turno of Object.values(lega.turni || {})) {
        for (const partita of turno.partite || []) {
          partite++;
          if (partita.quoteMercato && Object.values(partita.quoteMercato).some(q => Number(q) > 1)) conQuote++;
        }
      }
    }
    const date = Object.values(meta.dati_fino || {}).filter(d => /^\d{4}-\d{2}-\d{2}$/.test(d)).sort();
    const prima = date[0] || null;
    const giorni = prima ? Math.max(0, Math.floor(((now || Date.now()) - Date.parse(prima + "T00:00:00Z")) / 86400000)) : null;
    return {partite, conQuote, risultatiDa: prima, risultatiA: date[date.length - 1] || null, giorni};
  }
  if (typeof module === "object" && module.exports) module.exports = {riepilogo};
  if (typeof document === "undefined" || typeof DATA_META === "undefined") return;
  const meta = DATA_META, stato = riepilogo(DATA_PRO, meta);
  const header = document.querySelector("header");
  if (!header) return;
  const box = document.createElement("section");
  box.className = "qualita-dati";
  box.setAttribute("aria-label", "Disponibilità e limiti dei dati");
  function testo(tag, contenuto, classe) {
    const el = document.createElement(tag); el.textContent = contenuto;
    if (classe) el.className = classe;
    return el;
  }
  const riga = document.createElement("div"); riga.className = "qualita-riepilogo";
  riga.append(testo("strong", "Versione di verifica interna"));
  riga.append(testo("span", stato.partite + " incontri nella vista"));
  riga.append(testo("span", stato.conQuote + " incontri con quote rilevate"));
  riga.append(testo("span", stato.risultatiDa ? "Risultati campionati fino al " + stato.risultatiDa.split("-").reverse().join("/") : "Copertura dei risultati non disponibile", "copertura-risultati"));
  box.append(riga);
  box.append(testo("p", "Le probabilità sono stime del modello. In questa versione i diritti delle fonti e la corrispondenza dei calendari devono ancora essere verificati."));
  const dettagli = document.createElement("details");
  dettagli.append(testo("summary", "Mostra limiti e aggiornamento (" + (meta.avvisi || []).length + " avvisi)"));
  dettagli.append(testo("p", "Elaborazione della pagina: " + new Date(meta.aggiornato).toLocaleString("it-IT", {timeZone: "Europe/Rome"}) + " (ora italiana). La data di elaborazione non indica nuovi risultati acquisiti."));
  const lista = document.createElement("ul");
  for (const avviso of meta.avvisi || []) lista.append(testo("li", avviso));
  dettagli.append(lista); box.append(dettagli);
  header.after(box);
  const badge = document.getElementById("status-data-badge");
  if (badge) badge.textContent = "Dati e limiti visibili";
})(typeof globalThis === "undefined" ? this : globalThis);
