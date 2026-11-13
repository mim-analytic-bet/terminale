#!/usr/bin/env python3
import json, os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

with open(os.path.join(ROOT_DIR, 'scripts', 'database_serie_a_completo.json'), 'r', encoding='utf-8') as f:
    full_db = json.load(f)

# Premier League Giornata 12 reale
pl_g12_partite = [
    {
        "id": "not-che",
        "label": "Nottingham Forest - Chelsea",
        "bgGradient": "from-[#3a0a10] via-[#090d16] to-[#071d42]",
        "casa": { "sigla": "NFO", "nome": "Nottingham Forest", "rank": "5° posto · 19 pt", "colBox": "bg-red-600/20 text-red-400 border-red-500" },
        "ospite": { "sigla": "CHE", "nome": "Chelsea", "rank": "3° posto · 22 pt", "colBox": "bg-blue-600/20 text-blue-400 border-blue-400" },
        "data": "Venerdì 27 Nov · 21:00",
        "giornata": "Premier League · 12ª Giornata",
        "golC": "1.25",
        "golO": "1.85",
        "barC": "40%",
        "barO": "60%",
        "fasi": {
            1: { "label": "Fase 1: 1X2", "centerVal": "48%", "centerLbl": "Segno 2", "seg1": { "p": 0.28, "col": "#06b6d4", "nome": "1: 28%" }, "seg2": { "p": 0.24, "col": "#f59e0b", "nome": "X: 24%" }, "seg3": { "p": 0.48, "col": "#f43f5e", "nome": "2: 48%" } },
            2: { "label": "Fase 2: GG / NG", "centerVal": "62%", "centerLbl": "Gol (GG)", "seg1": { "p": 0.62, "col": "#10b981", "nome": "Gol: 62%" }, "seg2": { "p": 0.38, "col": "#64748b", "nome": "No Gol: 38%" }, "seg3": { "p": 0.0, "col": "transparent", "nome": "" } },
            3: { "label": "Fase 3: Under / Over 2.5", "centerVal": "60%", "centerLbl": "Over 2.5", "seg1": { "p": 0.60, "col": "#8b5cf6", "nome": "Over: 60%" }, "seg2": { "p": 0.40, "col": "#3b82f6", "nome": "Under: 40%" }, "seg3": { "p": 0.0, "col": "transparent", "nome": "" } },
            4: { "label": "Fase 4: xG per Squadra", "centerVal": "1.25 vs 1.85", "centerLbl": "Volume xG", "seg1": { "p": 0.40, "col": "#ef4444", "nome": "Forest: 40% (1.25)" }, "seg2": { "p": 0.60, "col": "#3b82f6", "nome": "Chelsea: 60% (1.85)" }, "seg3": { "p": 0.0, "col": "transparent", "nome": "" } }
        },
        "isValore": True,
        "evBadge": "+4,2%",
        "mercato": "Gol (Entrambe le squadre segnano)",
        "qEqua": "1.61",
        "qReale": "1.72",
        "spiegazione": "Forest micidiale in ripartenza al City Ground con Wood; Chelsea con Palmer produce oltre 1.8 xG esterni.",
        "analisi": "Il Chelsea subisce gol da 6 trasferte consecutive. Il Forest ha trovato la via della rete nell'80% delle gare interne. Edge matematico +4,2%.",
        "rischio": "Chelsea che blocca le corsie laterali limitando i rifornimenti aerei per Wood.",
        "pronosticiExtra": {
            1: { "tipo": "ALTA PROBABILITÀ (BASE)", "icona": "🛡️", "mercato": "Over 1.5 Gol", "alt": "X2 (72%)", "prob": 82, "probStr": "82%", "quota": "1.22", "badgeCol": "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", "barCol": "from-emerald-500 to-teal-400", "desc": "Anticipo del venerdì di Premier con indici offensivi elevati." },
            2: { "tipo": "MIGLIOR COMBO", "icona": "⚡", "mercato": "Gol + Over 2.5", "alt": "X2 + Gol (56%)", "prob": 58, "probStr": "58%", "quota": "1.95", "badgeCol": "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", "barCol": "from-cyan-500 to-blue-500", "desc": "Entrambe a segno in match da almeno 3 reti totali." },
            3: { "tipo": "PRONOSTICO HARD", "icona": "🎯", "mercato": "2 + Gol", "alt": "Ris. Esatto 1-2 (11%)", "prob": 32, "probStr": "32%", "quota": "3.40", "badgeCol": "text-rose-400 bg-rose-500/10 border-rose-500/30", "barCol": "from-rose-500 to-amber-500", "desc": "Successo dei Blues con gol subito dai padroni di casa." },
            4: { "tipo": "PRONOSTICO EXTRA", "icona": "🔮", "mercato": "Palmer Marcatore o Assist", "alt": "Multigol 2-4 (73%)", "prob": 62, "probStr": "62%", "quota": "1.85", "badgeCol": "text-purple-400 bg-purple-500/10 border-purple-500/30", "barCol": "from-purple-500 to-indigo-500", "desc": "Coinvolto nel 68% delle azioni offensive del Chelsea." }
        }
    },
    {
        "id": "eve-liv",
        "label": "Everton - Liverpool",
        "bgGradient": "from-[#082347] via-[#090d16] to-[#3a0a10]",
        "casa": { "sigla": "EVE", "nome": "Everton", "rank": "15° posto · 11 pt", "colBox": "bg-blue-600/20 text-blue-400 border-blue-500" },
        "ospite": { "sigla": "LIV", "nome": "Liverpool", "rank": "1° posto · 28 pt", "colBox": "bg-red-700/20 text-red-400 border-red-600" },
        "data": "Domenica 29 Nov · 15:00",
        "giornata": "Premier League · 12ª Giornata",
        "golC": "0.90",
        "golO": "2.20",
        "barC": "29%",
        "barO": "71%",
        "fasi": {
            1: { "label": "Fase 1: 1X2", "centerVal": "64%", "centerLbl": "Segno 2", "seg1": { "p": 0.15, "col": "#06b6d4", "nome": "1: 15%" }, "seg2": { "p": 0.21, "col": "#f59e0b", "nome": "X: 21%" }, "seg3": { "p": 0.64, "col": "#f43f5e", "nome": "2: 64%" } },
            2: { "label": "Fase 2: GG / NG", "centerVal": "53%", "centerLbl": "Gol (GG)", "seg1": { "p": 0.53, "col": "#10b981", "nome": "Gol: 53%" }, "seg2": { "p": 0.47, "col": "#64748b", "nome": "No Gol: 47%" }, "seg3": { "p": 0.0, "col": "transparent", "nome": "" } },
            3: { "label": "Fase 3: Under / Over 2.5", "centerVal": "62%", "centerLbl": "Over 2.5", "seg1": { "p": 0.62, "col": "#8b5cf6", "nome": "Over: 62%" }, "seg2": { "p": 0.38, "col": "#3b82f6", "nome": "Under: 38%" }, "seg3": { "p": 0.0, "col": "transparent", "nome": "" } },
            4: { "label": "Fase 4: xG per Squadra", "centerVal": "0.90 vs 2.20", "centerLbl": "Volume xG", "seg1": { "p": 0.29, "col": "#38bdf8", "nome": "Everton: 29% (0.90)" }, "seg2": { "p": 0.71, "col": "#ef4444", "nome": "Liverpool: 71% (2.20)" }, "seg3": { "p": 0.0, "col": "transparent", "nome": "" } }
        },
        "isValore": True,
        "evBadge": "+5,1%",
        "mercato": "2 + Over 1.5 Gol",
        "qEqua": "1.62",
        "qReale": "1.74",
        "spiegazione": "Derby del Merseyside a Goodison Park: i Reds di Slot guidano la Premier e creano 2.2 xG attesi.",
        "analisi": "Il Liverpool ha vinto 8 delle prime 11 partite. L'Everton fatica a reggere il ritmo sui 90 minuti. Quota 1.74 con chiaro vantaggio matematico.",
        "rischio": "Intensità fisica e agonistica tipica del derby di Liverpool che può spezzettare il gioco.",
        "pronosticiExtra": {
            1: { "tipo": "ALTA PROBABILITÀ (BASE)", "icona": "🛡️", "mercato": "Segno 2 (Liverpool)", "alt": "Over 1.5 (84%)", "prob": 64, "probStr": "64%", "quota": "1.45", "badgeCol": "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", "barCol": "from-emerald-500 to-teal-400", desc: "La capolista della Premier League nel derby cittadino." },
            2: { "tipo": "MIGLIOR COMBO", "icona": "⚡", "mercato": "2 + Over 1.5 Gol", "alt": "2 + Over 2.5 (54%)", "prob": 61, "probStr": "61%", "quota": "1.74", "badgeCol": "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", "barCol": "from-cyan-500 to-blue-500", desc: "Vittoria esterna dei Reds con almeno 2 gol totali nel match." },
            3: { "tipo": "PRONOSTICO HARD", "icona": "🎯", "mercato": "Liverpool vince a zero (2 + NoGol)", "alt": "Ris. Esatto 0-2 (12%)", "prob": 34, "probStr": "34%", "quota": "2.65", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", "barCol": "from-rose-500 to-amber-500", desc: "Miglior difesa della Premier League contro attacco toffees a basso rendimento." },
            4: { "tipo": "PRONOSTICO EXTRA", "icona": "🔮", "mercato": "Salah Marcatore", "alt": "Over 9.5 Corner", "prob": 52, "probStr": "52%", "quota": "2.10", "badgeCol": "text-purple-400 bg-purple-500/10 border-purple-500/30", "barCol": "from-purple-500 to-indigo-500", desc: "L'egiziano è storicamente letale nel derby del Merseyside." }
        }
    }
]

full_db["premier"] = {
    "nome": "Premier League (Inghilterra)",
    "turni": {
        "12": {
            "label": "12ª Giornata (27-29 Nov 2026)",
            "dataFine": "2026-11-29T23:59:59",
            "partite": pl_g12_partite
        }
    }
}

# Genera il file JS pulito
js_content = f"""
    let FASE_TORTA_ATTUALE = 1;
    let TIMER_TORTA = null;
    let PARTITA_CORRENTE = null;

    const DATA_PRO = {json.dumps(full_db, ensure_ascii=False, indent=2)};

    // LOGICA DI CONTROLLO E AUTO-ROLLOVER DEL CALENDARIO
    function cambiaCampionato() {{
      const campKey = document.getElementById("select-campionato").value;
      const camp = DATA_PRO[campKey] || DATA_PRO["serie-a"];
      
      const selectG = document.getElementById("select-giornata");
      selectG.innerHTML = "";
      
      const turniKeys = Object.keys(camp.turni).map(Number).sort((a,b) => a - b);
      const adesso = new Date();
      
      // Auto-Rollover: trova il primo turno la cui data di fine è ancora futura
      let turnoAttivo = turniKeys[0];
      let isRolloverEseguito = false;

      for (let k of turniKeys) {{
        const t = camp.turni[k];
        const fineTurno = new Date(t.dataFine);
        if (adesso <= fineTurno) {{
          turnoAttivo = k;
          break;
        }} else {{
          isRolloverEseguito = true;
        }}
      }}

      // Popola select-giornata
      turniKeys.forEach(k => {{
        const t = camp.turni[k];
        const opt = document.createElement("option");
        opt.value = k;
        const fine = new Date(t.dataFine);
        const concluso = adesso > fine;
        opt.textContent = `${{t.label}} ${{concluso ? '🏁 [Concluso]' : '🟢 [Attivo]'}}`;
        if (k === turnoAttivo) opt.selected = true;
        selectG.appendChild(opt);
      }});

      // Aggiorna indicatore badge rollover
      const badge = document.getElementById("badge-rollover");
      if (badge) {{
        if (isRolloverEseguito) {{
          badge.textContent = "🟢 AUTO-ROLLOVER ATTIVO";
          badge.className = "text-[9px] text-cyan-400 mono font-bold";
        }} else {{
          badge.textContent = "🟢 TURNO CORRENTE LIVE";
          badge.className = "text-[9px] text-emerald-400 mono font-bold";
        }}
      }}

      cambiaGiornata();
    }}

    function cambiaGiornata() {{
      const campKey = document.getElementById("select-campionato").value;
      const camp = DATA_PRO[campKey] || DATA_PRO["serie-a"];
      const gKey = document.getElementById("select-giornata").value;
      const turno = camp.turni[gKey] || camp.turni[Object.keys(camp.turni)[0]];

      const selectP = document.getElementById("select-partita");
      selectP.innerHTML = "";

      turno.partite.forEach((p, idx) => {{
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = `${{p.label}} (${{p.data.split('·')[0].trim()}})`;
        if (idx === 0) opt.selected = true;
        selectP.appendChild(opt);
      }});

      renderizzaPartita();
    }}

    function renderizzaPartita() {{
      const campKey = document.getElementById("select-campionato").value;
      const camp = DATA_PRO[campKey] || DATA_PRO["serie-a"];
      const gKey = document.getElementById("select-giornata").value;
      const turno = camp.turni[gKey] || camp.turni[Object.keys(camp.turni)[0]];
      const partitaId = document.getElementById("select-partita").value;

      PARTITA_CORRENTE = turno.partite.find(p => p.id === partitaId) || turno.partite[0];

      if (!PARTITA_CORRENTE) return;

      const m = PARTITA_CORRENTE;

      // Sfumatura autentica primo ripiano
      const banner = document.getElementById("banner-primo-ripiano");
      banner.className = `border border-slate-800 rounded-3xl p-6 shadow-2xl relative overflow-hidden transition-all duration-700 bg-gradient-to-r ${{m.bgGradient}}`;

      document.getElementById("match-giornata").textContent = m.giornata;
      document.getElementById("match-data").textContent = m.data;

      // Squadre
      document.getElementById("nome-casa").textContent = m.casa.nome;
      document.getElementById("nome-casa-short").textContent = m.casa.nome;
      document.getElementById("sigla-casa").textContent = m.casa.sigla;
      document.getElementById("rank-casa").textContent = m.casa.rank;
      document.getElementById("box-badge-casa").className = `w-16 h-16 rounded-2xl flex items-center justify-center font-black text-2xl mono shadow-xl border-2 ${{m.casa.colBox}}`;

      document.getElementById("nome-ospite").textContent = m.ospite.nome;
      document.getElementById("nome-ospite-short").textContent = m.ospite.nome;
      document.getElementById("sigla-ospite").textContent = m.ospite.sigla;
      document.getElementById("rank-ospite").textContent = m.ospite.rank;
      document.getElementById("box-badge-ospite").className = `w-16 h-16 rounded-2xl flex items-center justify-center font-black text-2xl mono shadow-xl border-2 ${{m.ospite.colBox}}`;

      document.getElementById("xg-dettaglio-casa").textContent = `Attesi: ${{m.golC}} gol`;
      document.getElementById("xg-dettaglio-ospite").textContent = `Attesi: ${{m.golO}} gol`;

      // Barre xG
      document.getElementById("bar-xg-c").style.width = m.barC;
      document.getElementById("bar-xg-o").style.width = m.barO;

      // Aggiorna Donut a Torta e Pronostici Scorrevoli alla fase corrente
      aggiornaDonut(FASE_TORTA_ATTUALE);
      aggiornaPronosticiScorrevoli(FASE_TORTA_ATTUALE);

      // Valore Box
      const vBox = document.getElementById("box-verdetto-valore");
      if (m.isValore) {{
        vBox.className = "bg-gradient-to-br from-slate-900 to-slate-950 border border-emerald-500/40 rounded-3xl p-6 shadow-2xl relative overflow-hidden";
        vBox.innerHTML = `
          <div class="flex justify-between items-start mb-4">
            <div class="flex items-center gap-2">
              <span class="bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider mono flex items-center gap-1.5">
                <span>💎</span> EDGE MATEMATICO RILEVATO
              </span>
              <span class="text-xs text-slate-400 font-medium">Eurobet vs Prezzo Equo</span>
            </div>
            <div class="text-right">
              <div class="text-[10px] uppercase text-slate-400 font-bold mono">Valore Atteso (EV)</div>
              <div class="text-2xl font-black text-emerald-400 mono">${{m.evBadge}}</div>
            </div>
          </div>
          <div class="bg-slate-950 p-4 rounded-2xl border border-slate-800/80 space-y-3">
            <div class="flex justify-between items-baseline">
              <div>
                <span class="text-[11px] text-slate-400 uppercase font-bold mono">Mercato Consigliato</span>
                <div class="text-xl md:text-2xl font-black text-white">${{m.mercato}}</div>
              </div>
              <div class="text-right">
                <span class="text-[10px] text-slate-400 uppercase font-bold mono">Puntata (2% Flat)</span>
                <div class="text-lg font-black text-white mono">2,00 €</div>
              </div>
            </div>
            <div class="space-y-1.5 pt-1">
              <div class="flex justify-between text-xs mono">
                <span class="text-slate-400">Prezzo Equo Stimato: <strong class="text-white">${{m.qEqua}}</strong></span>
                <span class="text-emerald-400 font-bold">Quota Eurobet: <strong class="text-emerald-300 text-sm">${{m.qReale}}</strong></span>
              </div>
              <div class="h-2.5 w-full bg-slate-900 rounded-full overflow-hidden flex border border-slate-800">
                <div class="bg-slate-600 h-full" style="width: 70%"></div>
                <div class="bg-emerald-500 h-full animate-pulse" style="width: 30%"></div>
              </div>
              <div class="flex justify-between text-[10px] text-slate-400 mono">
                <span>Stima Reale Modello</span>
                <span>Margine a favore sul banco</span>
                <span>Implicita Quota Eurobet</span>
              </div>
            </div>
          </div>
          <div class="mt-4 text-xs text-slate-300 leading-relaxed">${{m.spiegazione}}</div>
        `;
      }} else {{
        vBox.className = "bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-3xl p-6 shadow-2xl relative overflow-hidden";
        vBox.innerHTML = `
          <div class="flex justify-between items-start mb-4">
            <div class="flex items-center gap-2">
              <span class="bg-slate-800 text-slate-300 border border-slate-700 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider mono flex items-center gap-1.5">
                <span>🛡️</span> FILTRO CAPITALE: NESSUN EDGE
              </span>
              <span class="text-xs text-slate-400 font-medium">Prezzo Eurobet Penalizzante</span>
            </div>
            <div class="text-right">
              <div class="text-[10px] uppercase text-slate-400 font-bold mono">Puntata Consigliata</div>
              <div class="text-xl font-black text-white mono">0,00 €</div>
            </div>
          </div>
          <div class="bg-slate-950 p-4 rounded-2xl border border-slate-800 text-xs space-y-2">
            <div class="text-lg font-black text-slate-200">${{m.mercato}}</div>
            <p class="text-slate-400">${{m.spiegazione}}</p>
          </div>
        `;
      }}

      // Analisi Tracciabile
      document.getElementById("box-analisi-tracciabile").innerHTML = `
        <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
          <div class="font-bold text-white flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
            <span>Catena Logica dell'Analista (Numeri Verificati)</span>
          </div>
          <p>${{m.analisi}}</p>
          <div class="p-2.5 rounded-xl bg-rose-950/30 border border-rose-900/40 text-[11px] text-rose-300 flex items-center gap-2">
            <span>⚠️</span>
            <span><strong>Fattore di Rischio:</strong> ${{m.rischio}}</span>
          </div>
        </div>
      `;
    }}
"""

with open(os.path.join(ROOT_DIR, 'scripts', 'dataset_dashboard_snippet.js'), 'w', encoding='utf-8') as f:
    f.write(js_content.strip())

print("Snippet generato e pronto per l'iniezione!")
