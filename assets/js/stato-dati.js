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
  // Freschezza: soglie indicative (scelte di progetto non statistiche). Pagina: aggiornamenti automatici ogni 6-9 ore. Risultati: giornate settimanali.
  function freschezza(isoAggiornato, risultatiDa, now) {
    const n = now || Date.now();
    const ore = isoAggiornato && !isNaN(Date.parse(isoAggiornato)) ? Math.max(0, Math.round((n - Date.parse(isoAggiornato)) / 3600000)) : null;
    const giorni = risultatiDa ? Math.max(0, Math.floor((n - Date.parse(risultatiDa + "T00:00:00Z")) / 86400000)) : null;
    const livello = (v, verde, giallo) => v === null ? "grigio" : v <= verde ? "verde" : v <= giallo ? "giallo" : "rosso";
    return {ore, giorni, livelloPagina: livello(ore, 10, 24), livelloRisultati: livello(giorni, 4, 8)};
  }
  if (typeof module === "object" && module.exports) module.exports = {riepilogo, freschezza};
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
  const fr = freschezza(meta.aggiornato, stato.risultatiDa);
  const COL = {verde: "#065f46", giallo: "#92400e", rosso: "#991b1b", grigio: "#334155"};
  function chip(testoChip, livello) {
    const el = testo("span", testoChip);
    el.style.cssText = "display:inline-block;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;color:#fff;margin:2px 6px 2px 0;background:" + COL[livello];
    return el;
  }
  const chips = document.createElement("div"); chips.className = "qualita-freschezza"; chips.style.margin = "6px 0";
  chips.append(chip(fr.ore === null ? "Aggiornamento pagina: n.d." : "Pagina aggiornata " + (fr.ore < 1 ? "meno di un'ora fa" : fr.ore + " h fa"), fr.livelloPagina));
  chips.append(chip(fr.giorni === null ? "Risultati: n.d." : "Ultimi risultati: " + fr.giorni + (fr.giorni === 1 ? " giorno" : " giorni") + " fa", fr.livelloRisultati));
  chips.append(chip(stato.conQuote + "/" + stato.partite + " incontri con quote di mercato", stato.conQuote === 0 ? "rosso" : stato.conQuote < stato.partite ? "giallo" : "verde"));
  box.append(chips);
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
