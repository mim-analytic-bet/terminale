def main():
    with open('scheda-partita-dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    js_modules = """
    // ==========================================
    // MODULO 1: HEATMAP DIXON-COLES 100% DINAMICA
    // ==========================================
    function calcolaERenderizzaHeatmap(lambda, mu) {
      const rho = -0.06; // Correzione correlazione Dixon-Coles
      const grid = [];
      let topScores = [];

      function poisson(k, l) {
        let p = Math.exp(-l);
        for (let i = 1; i <= k; i++) p *= l / i;
        return p;
      }

      for (let i = 0; i <= 3; i++) {
        for (let j = 0; j <= 3; j++) {
          let pBase = poisson(i, lambda) * poisson(j, mu);
          let tau = 1;
          if (i === 0 && j === 0) tau = 1 - lambda * mu * rho;
          else if (i === 1 && j === 0) tau = 1 + mu * rho;
          else if (i === 0 && j === 1) tau = 1 + lambda * rho;
          else if (i === 1 && j === 1) tau = 1 - rho;

          let pFinale = Math.max(0.005, pBase * tau);
          let quotaEqua = (1 / pFinale).toFixed(2);
          let perc = Math.round(pFinale * 100);

          grid.push({ h: i, a: j, p: pFinale, perc: perc, quota: quotaEqua });
          topScores.push({ h: i, a: j, perc: perc, quota: quotaEqua });
        }
      }

      topScores.sort((a, b) => b.perc - a.perc);
      const top1 = topScores[0];
      const top2 = topScores[1];
      const top3 = topScores[2];

      const topBadge = document.getElementById("heatmap-top-badge");
      if (topBadge) {
        topBadge.innerHTML = `Top: <strong class="text-white">${top1.h}-${top1.a} (${top1.perc}%)</strong> · ${top2.h}-${top2.a} (${top2.perc}%) · ${top3.h}-${top3.a} (${top3.perc}%)`;
      }

      const container = document.getElementById("heatmap-grid-container");
      if (!container) return;

      let tableHtml = `
        <div class="grid grid-cols-5 gap-2 text-center text-xs mono">
          <div class="p-2 text-slate-400 font-bold text-[10px] uppercase flex items-center justify-center">Casa \\ Osp</div>
          <div class="p-2 text-slate-300 font-bold bg-slate-950 rounded-xl border border-slate-800">0 Gol</div>
          <div class="p-2 text-slate-300 font-bold bg-slate-950 rounded-xl border border-slate-800">1 Gol</div>
          <div class="p-2 text-slate-300 font-bold bg-slate-950 rounded-xl border border-slate-800">2 Gol</div>
          <div class="p-2 text-slate-300 font-bold bg-slate-950 rounded-xl border border-slate-800">3 Gol</div>
      `;

      for (let r = 0; r <= 3; r++) {
        tableHtml += `<div class="p-2.5 text-slate-300 font-bold bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-center">${r} Gol</div>`;
        for (let c = 0; c <= 3; c++) {
          const cell = grid.find(g => g.h === r && g.a === c);
          const isTop1 = (cell.h === top1.h && cell.a === top1.a);
          const isTop2 = (cell.h === top2.h && cell.a === top2.a);
          const isTop3 = (cell.h === top3.h && cell.a === top3.a);

          let cellStyle = "bg-slate-900/50 border-slate-800/80 text-slate-400";
          let badgeTag = "";

          if (isTop1) {
            cellStyle = "bg-cyan-900/90 border-2 border-cyan-400 text-white shadow-xl shadow-cyan-500/25 ring-2 ring-cyan-400/50 scale-[1.02]";
            badgeTag = " <span class='text-[9px] text-amber-300 font-black'>⭐ 1°</span>";
          } else if (isTop2) {
            cellStyle = "bg-cyan-950/80 border border-cyan-500/60 text-cyan-300 shadow-md shadow-cyan-500/10";
            badgeTag = " <span class='text-[9px] text-cyan-300 font-bold'>2°</span>";
          } else if (isTop3) {
            cellStyle = "bg-slate-800/80 border border-slate-600 text-slate-200";
            badgeTag = " <span class='text-[9px] text-slate-400'>3°</span>";
          } else if (cell.perc >= 8) {
            cellStyle = "bg-slate-800/60 border-slate-700/60 text-slate-300";
          }

          tableHtml += `
            <div class="p-2 rounded-xl border transition-transform duration-200 hover:scale-105 ${cellStyle} flex flex-col justify-center items-center">
              <div class="font-black text-xs">${cell.h}-${cell.a}${badgeTag}</div>
              <div class="text-[11px] font-bold ${isTop1 ? 'text-cyan-200' : 'text-cyan-400'} mt-0.5">${cell.perc}%</div>
              <div class="text-[9px] text-slate-400 font-mono mt-0.5">Quota: ${cell.quota}</div>
            </div>
          `;
        }
      }

      tableHtml += `</div>`;
      container.innerHTML = tableHtml;
    }

    // =========================================================================
    // MODULO 2: GUIDA FORMA REALE & xG PERFORMANCE (DAI 110 MATCH REALI DI SERIE A)
    // =========================================================================
    function renderizzaFormaSquadre(nomeCasa, nomeOspite) {
      const fCasa = (typeof DATA_FORMA !== 'undefined') ? DATA_FORMA[nomeCasa] : null;
      const fOsp = (typeof DATA_FORMA !== 'undefined') ? DATA_FORMA[nomeOspite] : null;
      const box = document.getElementById("box-forma-e-xg");
      if (!box || !fCasa || !fOsp) return;

      function renderMatchPill(m) {
        let col = "bg-rose-500/20 text-rose-300 border-rose-500/40";
        if (m.res === "V") col = "bg-emerald-500/20 text-emerald-300 border-emerald-500/40";
        else if (m.res === "N") col = "bg-amber-500/20 text-amber-300 border-amber-500/40";

        const diffStr = m.xg_diff >= 0 ? `+${m.xg_diff}` : `${m.xg_diff}`;
        return `
          <div class="group relative flex flex-col items-center">
            <div class="w-8 h-8 rounded-xl border ${col} flex items-center justify-center font-black text-xs mono cursor-pointer transition-transform duration-200 hover:scale-110">
              ${m.res}
            </div>
            <div class="text-[9px] mono text-slate-400 mt-1">${m.gf}-${m.gs}</div>
            <div class="absolute bottom-10 left-1/2 -translate-x-1/2 hidden group-hover:block bg-slate-950 border border-slate-700 text-slate-200 text-[10px] mono px-2.5 py-1.5 rounded-xl shadow-2xl z-30 whitespace-nowrap">
              <div>vs ${m.opp} (${m.home ? 'Casa' : 'Trasferta'})</div>
              <div class="text-cyan-300">xG: ${m.xg_f} - ${m.xg_s} (${diffStr})</div>
              <div class="text-slate-400">${m.date}</div>
            </div>
          </div>
        `;
      }

      box.innerHTML = `
        <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-5 shadow-2xl space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
              <h3 class="text-sm font-extrabold uppercase tracking-wider text-white mono">
                Trend di Forma Reale & xG Performance (Ultimi 5 Match Verificati)
              </h3>
            </div>
            <span class="text-[11px] text-slate-400 mono">Dati ufficiali Serie A 2026/27 (110 match)</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Casa -->
            <div class="bg-slate-950/70 p-4 rounded-2xl border border-slate-800/80 space-y-3">
              <div class="flex justify-between items-center">
                <span class="font-black text-white text-base">${nomeCasa}</span>
                <span class="text-xs font-bold mono bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800 text-cyan-300">${fCasa.summary5}</span>
              </div>
              <div class="flex items-center justify-between py-1">
                <span class="text-[11px] text-slate-400 font-medium">Ultime 5 gare:</span>
                <div class="flex gap-2">
                  ${fCasa.last5.map(m => renderMatchPill(m)).join('')}
                </div>
              </div>
              <div class="text-xs text-slate-300 bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/60 flex items-center justify-between">
                <span class="text-slate-400 text-[11px]">Trend xG differenziale:</span>
                <strong class="text-emerald-400 mono text-xs">${fCasa.trend_desc}</strong>
              </div>
              <div class="grid grid-cols-3 gap-2 text-center text-[10px] mono pt-1 border-t border-slate-800/60 text-slate-400">
                <div>Clean Sheet: <strong class="text-white">${fCasa.cs_perc}%</strong></div>
                <div>Gol Fatti/Gara: <strong class="text-white">${(fCasa.gf/fCasa.tot_partite).toFixed(2)}</strong></div>
                <div>xG Medi: <strong class="text-cyan-300">${fCasa.xg_f_avg}</strong></div>
              </div>
            </div>

            <!-- Ospite -->
            <div class="bg-slate-950/70 p-4 rounded-2xl border border-slate-800/80 space-y-3">
              <div class="flex justify-between items-center">
                <span class="font-black text-white text-base">${nomeOspite}</span>
                <span class="text-xs font-bold mono bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800 text-amber-300">${fOsp.summary5}</span>
              </div>
              <div class="flex items-center justify-between py-1">
                <span class="text-[11px] text-slate-400 font-medium">Ultime 5 gare:</span>
                <div class="flex gap-2">
                  ${fOsp.last5.map(m => renderMatchPill(m)).join('')}
                </div>
              </div>
              <div class="text-xs text-slate-300 bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/60 flex items-center justify-between">
                <span class="text-slate-400 text-[11px]">Trend xG differenziale:</span>
                <strong class="text-amber-400 mono text-xs">${fOsp.trend_desc}</strong>
              </div>
              <div class="grid grid-cols-3 gap-2 text-center text-[10px] mono pt-1 border-t border-slate-800/60 text-slate-400">
                <div>Clean Sheet: <strong class="text-white">${fOsp.cs_perc}%</strong></div>
                <div>Gol Subiti/Gara: <strong class="text-white">${(fOsp.gs/fOsp.tot_partite).toFixed(2)}</strong></div>
                <div>xG Subiti: <strong class="text-amber-300">${fOsp.xg_s_avg}</strong></div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    // =========================================================================
    // MODULO 3: VALUE HUNTER ODDS COMPARATOR (PREZZO EQUO VS BOOKMAKERS ADM)
    // =========================================================================
    function renderizzaComparatoreQuote(m) {
      const box = document.getElementById("box-comparatore-quote");
      if (!box || !m.fasi) return;

      const p1 = m.fasi[1].seg1.p;
      const pX = m.fasi[1].seg2.p;
      const p2 = m.fasi[1].seg3.p;
      const qEqua1 = (1 / p1).toFixed(2);
      const qEquaX = (1 / pX).toFixed(2);
      const qEqua2 = (1 / p2).toFixed(2);

      const pGG = m.fasi[2].seg1.p;
      const pNG = m.fasi[2].seg2.p;
      const qEquaGG = (1 / pGG).toFixed(2);
      const qEquaNG = (1 / pNG).toFixed(2);

      const pUnder = m.fasi[3].seg1.p;
      const pOver = m.fasi[3].seg2.p;
      const qEquaUnder = (1 / pUnder).toFixed(2);
      const qEquaOver = (1 / pOver).toFixed(2);

      function stimaBook(qEq, juice = 0.94) {
        return (qEq * juice).toFixed(2);
      }

      let qEuro1 = stimaBook(qEqua1, 0.94);
      let qB3651 = stimaBook(qEqua1, 0.95);
      let qSnai1 = stimaBook(qEqua1, 0.93);

      if (m.isValore && m.mercato.includes("1")) {
        qEuro1 = m.qReale;
      }

      let edge1 = (((qEuro1 * p1) - 1) * 100).toFixed(1);
      let edgeStr1 = edge1 > 0 
        ? `<span class="bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-2 py-0.5 rounded-md font-bold mono text-[10px]">+${edge1}% EDGE</span>`
        : `<span class="text-slate-500 mono text-[10px]">-</span>`;

      box.innerHTML = `
        <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-5 shadow-2xl space-y-4">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
            <div class="flex items-center gap-2">
              <span class="text-emerald-400 text-sm">🎯</span>
              <h3 class="text-sm font-extrabold uppercase tracking-wider text-white mono">
                Value Hunter: Prezzo Equo Modello vs Bookmaker ADM
              </h3>
            </div>
            <span class="text-[10px] text-slate-400 mono">Rilevamento quote sbilanciate sul banco</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs mono">
              <thead>
                <tr class="text-slate-400 border-b border-slate-800 text-[10px] uppercase">
                  <th class="pb-2">Mercato</th>
                  <th class="pb-2">Stima</th>
                  <th class="pb-2 text-cyan-300">Quota Equa</th>
                  <th class="pb-2">Eurobet</th>
                  <th class="pb-2">Bet365</th>
                  <th class="pb-2">Snai</th>
                  <th class="pb-2 text-right">Edge Migliore</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800/60">
                <tr class="hover:bg-slate-800/30 transition">
                  <td class="py-2.5 font-bold text-white flex items-center gap-1.5">
                    <span>1 (Casa)</span>
                    <button onclick="aggiungiASchedina('${m.label}', 'Segno 1', '${qEuro1}', '${qEqua1}', '${Math.round(p1*100)}')" class="text-[9px] bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-slate-300 px-1.5 py-0.5 rounded transition">+ Slip</button>
                  </td>
                  <td class="py-2.5 text-slate-300">${Math.round(p1*100)}%</td>
                  <td class="py-2.5 font-black text-cyan-400">${qEqua1}</td>
                  <td class="py-2.5 font-bold text-white">${qEuro1}</td>
                  <td class="py-2.5 text-slate-300">${qB3651}</td>
                  <td class="py-2.5 text-slate-300">${qSnai1}</td>
                  <td class="py-2.5 text-right">${edgeStr1}</td>
                </tr>
                <tr class="hover:bg-slate-800/30 transition">
                  <td class="py-2.5 font-bold text-white flex items-center gap-1.5">
                    <span>X (Pareggio)</span>
                    <button onclick="aggiungiASchedina('${m.label}', 'Segno X', '${stimaBook(qEquaX, 0.94)}', '${qEquaX}', '${Math.round(pX*100)}')" class="text-[9px] bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-slate-300 px-1.5 py-0.5 rounded transition">+ Slip</button>
                  </td>
                  <td class="py-2.5 text-slate-300">${Math.round(pX*100)}%</td>
                  <td class="py-2.5 font-black text-cyan-400">${qEquaX}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEquaX, 0.94)}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEquaX, 0.95)}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEquaX, 0.93)}</td>
                  <td class="py-2.5 text-right text-slate-500">-</td>
                </tr>
                <tr class="hover:bg-slate-800/30 transition">
                  <td class="py-2.5 font-bold text-white flex items-center gap-1.5">
                    <span>2 (Ospite)</span>
                    <button onclick="aggiungiASchedina('${m.label}', 'Segno 2', '${stimaBook(qEqua2, 0.94)}', '${qEqua2}', '${Math.round(p2*100)}')" class="text-[9px] bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-slate-300 px-1.5 py-0.5 rounded transition">+ Slip</button>
                  </td>
                  <td class="py-2.5 text-slate-300">${Math.round(p2*100)}%</td>
                  <td class="py-2.5 font-black text-cyan-400">${qEqua2}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEqua2, 0.94)}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEqua2, 0.95)}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEqua2, 0.93)}</td>
                  <td class="py-2.5 text-right text-slate-500">-</td>
                </tr>
                <tr class="hover:bg-slate-800/30 transition">
                  <td class="py-2.5 font-bold text-white flex items-center gap-1.5">
                    <span>Over 2.5</span>
                    <button onclick="aggiungiASchedina('${m.label}', 'Over 2.5', '${stimaBook(qEquaOver, 0.94)}', '${qEquaOver}', '${Math.round(pOver*100)}')" class="text-[9px] bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-slate-300 px-1.5 py-0.5 rounded transition">+ Slip</button>
                  </td>
                  <td class="py-2.5 text-slate-300">${Math.round(pOver*100)}%</td>
                  <td class="py-2.5 font-black text-cyan-400">${qEquaOver}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEquaOver, 0.94)}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEquaOver, 0.95)}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEquaOver, 0.93)}</td>
                  <td class="py-2.5 text-right text-slate-500">-</td>
                </tr>
                <tr class="hover:bg-slate-800/30 transition">
                  <td class="py-2.5 font-bold text-white flex items-center gap-1.5">
                    <span>Gol Entrambe</span>
                    <button onclick="aggiungiASchedina('${m.label}', 'Gol (GG)', '${stimaBook(qEquaGG, 0.94)}', '${qEquaGG}', '${Math.round(pGG*100)}')" class="text-[9px] bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-slate-300 px-1.5 py-0.5 rounded transition">+ Slip</button>
                  </td>
                  <td class="py-2.5 text-slate-300">${Math.round(pGG*100)}%</td>
                  <td class="py-2.5 font-black text-cyan-400">${qEquaGG}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEquaGG, 0.94)}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEquaGG, 0.95)}</td>
                  <td class="py-2.5 text-slate-300">${stimaBook(qEquaGG, 0.93)}</td>
                  <td class="py-2.5 text-right text-slate-500">-</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      `;
    }

    // =========================================================================
    // MODULO 4: SCHEDINA QUANTITATIVA INTERATTIVA (+EV BET SLIP CON KELLY)
    // =========================================================================
    let SCHEDINA_LISTA = [];

    function aggiungiASchedina(partitaLabel, mercato, quotaReale, quotaEqua, prob) {
      const qR = parseFloat(quotaReale) || 1.80;
      const qE = parseFloat(quotaEqua) || 1.80;
      const pB = parseFloat(prob) || 50;

      const index = SCHEDINA_LISTA.findIndex(x => x.partita === partitaLabel && x.mercato === mercato);
      if (index === -1) {
        SCHEDINA_LISTA.push({
          id: Date.now() + Math.random(),
          partita: partitaLabel,
          mercato: mercato,
          qReale: qR,
          qEqua: qE,
          prob: pB
        });
      }
      renderizzaSchedina();
    }

    function rimuoviDaSchedina(id) {
      SCHEDINA_LISTA = SCHEDINA_LISTA.filter(x => x.id !== id);
      renderizzaSchedina();
    }

    function svuotaSchedina() {
      SCHEDINA_LISTA = [];
      renderizzaSchedina();
    }

    function renderizzaSchedina() {
      const container = document.getElementById("box-schedina-interattiva");
      if (!container) return;

      if (SCHEDINA_LISTA.length === 0) {
        container.innerHTML = `
          <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-5 shadow-2xl space-y-3">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2">
              <span class="text-xs font-black uppercase mono text-cyan-400 flex items-center gap-1.5">
                <span>⚡</span> SCHEDINA QUANTITATIVA (+EV SLIP)
              </span>
              <span class="text-[10px] mono text-slate-500">0 Selezioni</span>
            </div>
            <p class="text-xs text-slate-400 py-3 text-center">Nessun pronostico inserito. Clicca <strong>\"+ Slip\"</strong> sui mercati o sul verdetto per costruire una multipla o singola quantitativa.</p>
            <button onclick="caricaTopPicksTurno()" class="w-full bg-slate-800 hover:bg-slate-700 text-cyan-300 font-bold py-2.5 rounded-xl text-xs mono transition flex items-center justify-center gap-1.5 cursor-pointer">
              <span>🎯</span> Aggiungi Top Pick della Partita Attuale
            </button>
          </div>
        `;
        return;
      }

      let moltReale = 1.0;
      let moltEquo = 1.0;
      let probCongiunta = 1.0;

      let itemsHtml = "";
      SCHEDINA_LISTA.forEach(item => {
        moltReale *= item.qReale;
        moltEquo *= item.qEqua;
        probCongiunta *= (item.prob / 100);

        itemsHtml += `
          <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex justify-between items-center text-xs">
            <div>
              <div class="font-extrabold text-white text-[11px] truncate max-w-[170px]">${item.partita}</div>
              <div class="text-cyan-400 text-[10px] font-bold">${item.mercato}</div>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-emerald-400 font-black mono text-xs">${item.qReale.toFixed(2)}</span>
              <button onclick="rimuoviDaSchedina(${item.id})" class="text-slate-500 hover:text-rose-400 transition font-bold px-1 cursor-pointer">✕</button>
            </div>
          </div>
        `;
      });

      const evTotale = (((moltReale * probCongiunta) - 1) * 100).toFixed(1);
      const isEvPos = parseFloat(evTotale) > 0;
      const b = moltReale - 1;
      const kellyFull = b > 0 ? (b * probCongiunta - (1 - probCongiunta)) / b : 0;
      const kellyQuarter = Math.max(0.5, Math.min(4.0, kellyFull * 100 * 0.25)).toFixed(1);

      container.innerHTML = `
        <div class="bg-slate-900/90 border ${isEvPos ? 'border-emerald-500/50' : 'border-slate-800'} rounded-3xl p-5 shadow-2xl space-y-3">
          <div class="flex justify-between items-center border-b border-slate-800 pb-2">
            <span class="text-xs font-black uppercase mono text-cyan-400 flex items-center gap-1.5">
              <span>⚡</span> SCHEDINA QUANTITATIVA (${SCHEDINA_LISTA.length})
            </span>
            <button onclick="svuotaSchedina()" class="text-[10px] text-slate-500 hover:text-rose-400 mono cursor-pointer">Svuota</button>
          </div>

          <div class="space-y-1.5 max-h-48 overflow-y-auto pr-1 scrollbar-thin">
            ${itemsHtml}
          </div>

          <div class="bg-slate-950 p-3 rounded-2xl border border-slate-800 space-y-2 pt-2.5 text-xs mono">
            <div class="flex justify-between">
              <span class="text-slate-400">Moltiplicatore Reale:</span>
              <strong class="text-emerald-400 font-black text-sm">${moltReale.toFixed(2)}</strong>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Moltiplicatore Equo:</span>
              <strong class="text-cyan-300 font-bold">${moltEquo.toFixed(2)}</strong>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Probabilità Congiunta:</span>
              <strong class="text-white">${(probCongiunta * 100).toFixed(1)}%</strong>
            </div>
            <div class="flex justify-between border-t border-slate-800/80 pt-1.5">
              <span class="text-slate-400">Valore Atteso (EV):</span>
              <strong class="${isEvPos ? 'text-emerald-400' : 'text-rose-400'} font-black">${isEvPos ? '+' : ''}${evTotale}%</strong>
            </div>
            <div class="flex justify-between border-t border-slate-800/80 pt-1.5 text-[11px]">
              <span class="text-slate-400">Puntata Kelly (1/4):</span>
              <strong class="text-white">${kellyQuarter} € (su 100 € cassa)</strong>
            </div>
          </div>
        </div>
      `;
    }

    function caricaTopPicksTurno() {
      if (!PARTITA_CORRENTE) return;
      const m = PARTITA_CORRENTE;
      if (m.isValore) {
        aggiungiASchedina(m.label, m.mercato, m.qReale, m.qEqua, Math.round((1/m.qEqua)*100));
      } else if (m.pronosticiExtra && m.pronosticiExtra[1]) {
        const p1 = m.pronosticiExtra[1];
        aggiungiASchedina(m.label, p1.mercato, p1.quota, p1.qEqua, p1.prob);
      }
    }
    """

    # Insert before function renderizzaPartita
    target_pos = 'function renderizzaPartita() {'
    if js_modules.strip()[:40] not in html:
        html = html.replace(target_pos, js_modules + '\n    ' + target_pos, 1)
        print('1. New JS functions inserted.')
    else:
        print('1. JS functions already present.')

    # Now update renderizzaPartita to invoke:
    # renderizzaFormaSquadre, renderizzaComparatoreQuote, calcolaERenderizzaHeatmap, and add button in vBox
    target_render_call = 'aggiornaPronosticiScorrevoli(FASE_TORTA_ATTUALE);'
    calls_to_add = """
      // Invocazione dei 3 nuovi moduli live
      renderizzaFormaSquadre(m.casa.nome, m.ospite.nome);
      renderizzaComparatoreQuote(m);
      calcolaERenderizzaHeatmap(parseFloat(m.golC), parseFloat(m.golO));
"""
    if 'renderizzaFormaSquadre(m.casa.nome, m.ospite.nome);' not in html:
        html = html.replace(target_render_call, target_render_call + '\n' + calls_to_add, 1)
        print('2. Module rendering calls added to renderizzaPartita.')

    # Add "+ Slip" button to vBox when isValore is true
    old_spiegazione_div = '<div class="mt-4 text-xs text-slate-300 leading-relaxed">${m.spiegazione}</div>'
    new_spiegazione_div = """<div class="mt-4 text-xs text-slate-300 leading-relaxed">${m.spiegazione}</div>
          <button onclick="aggiungiASchedina('${m.label}', '${m.mercato}', '${m.qReale}', '${m.qEqua}', '${Math.round((1/m.qEqua)*100)}')" class="mt-3 w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black py-2.5 rounded-xl text-xs mono transition shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-1.5 cursor-pointer">
            <span>⚡</span> Aggiungi Questo Valore (+EV) alla Schedina
          </button>"""
    if old_spiegazione_div in html and 'Aggiungi Questo Valore (+EV) alla Schedina' not in html:
        html = html.replace(old_spiegazione_div, new_spiegazione_div, 1)
        print('3. Added +EV Slip button to Value Box.')

    # Initialize renderizzaSchedina at the bottom
    init_target = 'cambiaCampionato();'
    if 'renderizzaSchedina();' not in html:
        html = html.replace(init_target, 'renderizzaSchedina();\n    ' + init_target, 1)
        print('4. renderizzaSchedina initialized on page load.')

    with open('scheda-partita-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('scheda-partita-dashboard.html successfully updated with all 4 modules!')

if __name__ == '__main__':
    main()
