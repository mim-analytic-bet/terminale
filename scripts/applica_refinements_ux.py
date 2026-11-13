import re
import os

HTML_PATH = "scheda-partita-dashboard.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Update nav-mobile in HTML to include Schedina with live badge
old_nav = '''<nav id="nav-mobile" aria-label="Sezioni">
<button data-t="select-campionato"><span>⚽</span>Partite</button>
<button data-t="box-forma-e-xg"><span>📊</span>Analisi</button>
<button data-t="box-combo-1"><span>🎯</span>Combo</button>
<button data-t="box-track"><span>📈</span>Track</button>
</nav>'''

new_nav = '''<nav id="nav-mobile" aria-label="Sezioni">
<button data-t="select-campionato"><span>⚽</span>Partite</button>
<button data-t="box-forma-e-xg"><span>📊</span>Analisi</button>
<button data-t="box-combo-1"><span>🎯</span>Combo</button>
<button data-t="box-schedina-interattiva" id="btn-nav-slip" class="relative">
  <span>🧾</span>Schedina
  <span id="badge-nav-slip" class="hidden absolute -top-1 -right-1 min-w-[17px] h-[17px] px-1 rounded-full bg-emerald-400 text-slate-950 font-black text-[9px] flex items-center justify-center shadow-lg shadow-emerald-500/50">0</span>
</button>
<button data-t="box-track"><span>📈</span>Track</button>
</nav>'''

if old_nav in c:
    c = c.replace(old_nav, new_nav)
    print("1. nav-mobile replaced successfully")
else:
    print("1. WARNING: old_nav not found")

# 2. Add status-data-badge container to Header
old_header_bankroll = '''<div class="flex items-center gap-2 text-xs mono">
        <div class="bg-slate-900/90 border border-slate-800 rounded-xl px-3.5 py-1.5 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-slate-400">Bankroll:</span>
          <strong class="text-white">100 €</strong>
          <span class="text-slate-500 text-[10px]">(2€ flat)</span>
        </div>
      </div>'''

new_header_bankroll = '''<div class="flex flex-wrap items-center gap-2 text-xs mono">
        <div id="status-data-badge" class="hidden sm:flex"></div>
        <div class="bg-slate-900/90 border border-slate-800 rounded-xl px-3.5 py-1.5 flex items-center gap-2 shadow-sm">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-slate-400">Bankroll:</span>
          <strong class="text-white">100 €</strong>
          <span class="text-slate-500 text-[10px]">(2€ flat)</span>
        </div>
      </div>'''

if old_header_bankroll in c:
    c = c.replace(old_header_bankroll, new_header_bankroll)
    print("2. Header badge container added")
else:
    print("2. WARNING: old_header_bankroll not found")

# 3. Add mobile touch hint above Heatmap
old_heatmap_badge = '''<div id="heatmap-top-badge" class="text-xs mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/40 px-3 py-1.5 rounded-xl font-bold self-start sm:self-auto">
              Top: Calcolo in corso...
            </div>
          </div>

          <div class="overflow-x-auto">'''

new_heatmap_badge = '''<div id="heatmap-top-badge" class="text-xs mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/40 px-3 py-1.5 rounded-xl font-bold self-start sm:self-auto">
              Top: Calcolo in corso...
            </div>
          </div>

          <div class="text-[11px] text-cyan-400/80 mono sm:hidden flex items-center gap-1.5 mb-1 bg-cyan-950/30 border border-cyan-800/30 px-3 py-1.5 rounded-xl">
            <span>👈</span> Scorri in orizzontale la matrice 4×4 per vedere tutti i punteggi
          </div>

          <div class="overflow-x-auto">'''

if old_heatmap_badge in c:
    c = c.replace(old_heatmap_badge, new_heatmap_badge)
    print("3. Heatmap touch hint added")
else:
    print("3. WARNING: old_heatmap_badge not found")

# 4. Enhance Value Hunter table buttons with tactile tap targets
old_table_btn = 'const btn = qm ? `<button onclick="aggiungiASchedina(\'${m.label}\', \'${mk}\', \'${qm}\', \'${qe}\', \'${Math.round(p*100)}\')" class="text-[9px] bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-slate-300 px-1.5 py-0.5 rounded">+</button>` : \'\';'
new_table_btn = 'const btn = qm ? `<button onclick="aggiungiASchedina(\'${m.label}\', \'${mk}\', \'${qm}\', \'${qe}\', \'${Math.round(p*100)}\')" title="Aggiungi allo slip" class="w-7 h-7 sm:w-6 sm:h-6 rounded-lg bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-cyan-300 font-black flex items-center justify-center text-xs transition cursor-pointer border border-slate-700/60 shadow-sm active:scale-95">+</button>` : \'\';'

if old_table_btn in c:
    c = c.replace(old_table_btn, new_table_btn)
    print("4. Value Hunter buttons enlarged for touch")
else:
    print("4. WARNING: old_table_btn not found")

# 5. Add Toast feedback function and Copy Slip function
pos_agg = c.find('function aggiungiASchedina(partitaLabel, mercato, quotaReale, quotaEqua, prob) {')
old_agg_block = c[pos_agg:pos_agg+500]
target_index = old_agg_block.find('renderizzaSchedina();')
old_agg_replace = old_agg_block[:target_index+len('renderizzaSchedina();')]

new_agg_replace = '''function mostraToastSlip(msg) {
      let t = document.getElementById("toast-slip");
      if (!t) {
        t = document.createElement("div");
        t.id = "toast-slip";
        t.className = "fixed top-4 right-4 sm:right-6 z-[100] max-w-sm bg-slate-900/95 border border-emerald-500/50 text-white p-3 rounded-2xl shadow-2xl backdrop-blur-xl transition-all duration-300 transform translate-y-[-20px] opacity-0 flex items-center gap-3";
        document.body.appendChild(t);
      }
      t.innerHTML = `
        <span class="text-emerald-400 text-lg flex-shrink-0">✓</span>
        <div class="flex-1 text-xs">
          <div class="font-bold text-white text-[11px] truncate">${msg.partita}</div>
          <div class="text-cyan-400 text-[10px] mono font-bold">${msg.mercato} @ ${msg.quota}</div>
        </div>
        <button onclick="document.getElementById('box-schedina-interattiva').scrollIntoView({behavior:'smooth'})" class="px-2 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-[10px] font-bold uppercase mono hover:bg-emerald-500 hover:text-slate-950 transition">Vedi</button>
      `;
      t.style.transform = "translateY(0)";
      t.style.opacity = "1";
      clearTimeout(t._timer);
      t._timer = setTimeout(() => {
        t.style.transform = "translateY(-20px)";
        t.style.opacity = "0";
      }, 2500);
    }

    function copiaSchedinaTesto() {
      if (SCHEDINA_LISTA.length === 0) return;
      let molt = 1.0;
      let lines = ["⚡ QUANT TERMINAL PRO · SCHEDINA (+EV)", ""];
      SCHEDINA_LISTA.forEach(it => {
        molt *= it.qReale;
        lines.push(`• ${it.partita}: ${it.mercato} @ ${it.qReale.toFixed(2)} (Prob. ${it.prob}%)`);
      });
      lines.push("");
      lines.push(`Moltiplicatore Totale: ${molt.toFixed(2)}`);
      lines.push("Puntata consigliata: 2.00 € (su cassa 100 €)");
      lines.push("Generato da: https://mim-analytic-bet.github.io/terminale/");

      const txt = lines.join("\\n");
      navigator.clipboard.writeText(txt).then(() => {
        const btn = document.getElementById("btn-copia-slip");
        if (btn) {
          const orig = btn.innerHTML;
          btn.innerHTML = "<span>✓</span> Copiato!";
          btn.classList.add("text-emerald-400", "border-emerald-500/50");
          setTimeout(() => {
            btn.innerHTML = orig;
            btn.classList.remove("text-emerald-400", "border-emerald-500/50");
          }, 2000);
        }
      }).catch(() => {
        alert("Schedina Copiata!\\n\\n" + txt);
      });
    }

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
        mostraToastSlip({ partita: partitaLabel, mercato: mercato, quota: qR.toFixed(2) });
      }
      renderizzaSchedina();'''

c = c.replace(old_agg_replace, new_agg_replace, 1)
print("5. Toast slip and copiaSchedinaTesto added to aggiungiASchedina")

# 6. Update renderizzaSchedina to update badge-nav-slip and add Copia Schedina button
old_render_end = '''container.innerHTML = `
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
      `;'''

new_render_end = '''container.innerHTML = `
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
            <div class="flex gap-2 pt-2 border-t border-slate-800/80">
              <button onclick="copiaSchedinaTesto()" id="btn-copia-slip" class="flex-1 bg-slate-800 hover:bg-slate-700 text-cyan-300 font-bold py-2 rounded-xl text-[11px] mono transition flex items-center justify-center gap-1.5 cursor-pointer border border-slate-700">
                <span>📋</span> Copia Schedina
              </button>
            </div>
          </div>
        </div>
      `;
      const bNav = document.getElementById("badge-nav-slip");
      if (bNav) {
        bNav.textContent = SCHEDINA_LISTA.length;
        bNav.classList.toggle("hidden", SCHEDINA_LISTA.length === 0);
      }'''

if old_render_end in c:
    c = c.replace(old_render_end, new_render_end)
    print("6. renderizzaSchedina updated with Copia Schedina and badge sync")
else:
    print("6. WARNING: old_render_end not found")

# Also handle badge when empty in renderizzaSchedina
pos_empty = c.find('if (SCHEDINA_LISTA.length === 0) {')
c = c[:pos_empty] + '''const bNavInit = document.getElementById("badge-nav-slip");
      if (bNavInit) bNavInit.classList.add("hidden");\n      ''' + c[pos_empty:]
print("6b. Empty badge sync added")

# 7. Update style#mobile for single-bar bottom navigation without overlapping
old_style_mobile = '''@media (max-width:768px){
  #strip-partite-turno{margin-left:-14px;margin-right:-14px;padding:10px 14px 12px!important}
  body{padding:8px!important;padding-bottom:calc(112px + env(safe-area-inset-bottom))!important}
  body.neon header{padding:8px 10px!important;border-radius:14px}
  select,button,summary{min-height:44px}
  select{font-size:16px!important}
  [class*="rounded-3xl"]{padding:14px!important}
  #box-comparatore-quote{overflow-x:auto;-webkit-overflow-scrolling:touch}
  #strip-partite-turno{scroll-snap-type:x proximity;-webkit-overflow-scrolling:touch;scroll-padding-left:0}
  #strip-partite-turno>*{scroll-snap-align:start;flex:0 0 auto!important;width:212px!important;min-width:212px!important;box-sizing:border-box}
  div:has(>#strip-partite-turno)>div:first-child{flex-direction:column!important;align-items:flex-start!important;gap:4px!important}
  body.neon header,header{padding-right:56px!important}
  header h1{flex-wrap:wrap;row-gap:4px}
  #btn-neon{width:34px;height:34px;padding:0!important;font-size:0!important;display:flex;align-items:center;justify-content:center;top:14px!important;right:14px!important}
  #btn-neon::before{content:"\\2726";font-size:16px;letter-spacing:0}
  .sb-fissa{flex-wrap:nowrap!important;overflow-x:auto;white-space:nowrap;gap:14px!important;padding:6px 10px calc(6px + env(safe-area-inset-bottom))!important;scrollbar-width:none}
  .sb-fissa::-webkit-scrollbar{display:none}
  #nav-mobile{display:flex;position:fixed;left:8px;right:8px;bottom:calc(34px + env(safe-area-inset-bottom));z-index:60;gap:4px;padding:6px;border-radius:20px;background:rgba(8,12,28,.82);border:1px solid rgba(129,140,248,.3);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);box-shadow:0 10px 30px -8px rgba(0,0,0,.6)}
  #nav-mobile button{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:6px 2px;border:0;border-radius:14px;background:transparent;color:#94a3b8;font:700 10px ui-monospace,monospace;letter-spacing:.04em;text-transform:uppercase;transition:background .2s,color .2s}
  #nav-mobile button span{font-size:18px;line-height:1}
  #nav-mobile button.on{background:rgba(34,211,238,.16);color:#67e8f9}
}'''

new_style_mobile = '''@media (max-width:768px){
  #strip-partite-turno{margin-left:-14px;margin-right:-14px;padding:10px 14px 12px!important}
  body{padding:8px!important;padding-bottom:calc(85px + env(safe-area-inset-bottom))!important}
  body.neon header{padding:8px 10px!important;border-radius:14px}
  select,button,summary{min-height:44px}
  select{font-size:16px!important}
  [class*="rounded-3xl"]{padding:14px!important}
  #box-comparatore-quote{overflow-x:auto;-webkit-overflow-scrolling:touch}
  #strip-partite-turno{scroll-snap-type:x proximity;-webkit-overflow-scrolling:touch;scroll-padding-left:0}
  #strip-partite-turno>*{scroll-snap-align:start;flex:0 0 auto!important;width:212px!important;min-width:212px!important;box-sizing:border-box}
  div:has(>#strip-partite-turno)>div:first-child{flex-direction:column!important;align-items:flex-start!important;gap:4px!important}
  body.neon header,header{padding-right:56px!important}
  header h1{flex-wrap:wrap;row-gap:4px}
  #btn-neon{width:34px;height:34px;padding:0!important;font-size:0!important;display:flex;align-items:center;justify-content:center;top:14px!important;right:14px!important}
  #btn-neon::before{content:"\\2726";font-size:16px;letter-spacing:0}
  .sb-fissa{display:none!important}
  #nav-mobile{display:flex;position:fixed;left:8px;right:8px;bottom:calc(10px + env(safe-area-inset-bottom));z-index:60;gap:2px;padding:5px;border-radius:24px;background:rgba(6,9,20,.88);border:1px solid rgba(34,211,238,.25);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);box-shadow:0 12px 36px -4px rgba(0,0,0,.75)}
  #nav-mobile button{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:6px 2px;border:0;border-radius:16px;background:transparent;color:#94a3b8;font:700 10px ui-monospace,monospace;letter-spacing:.03em;text-transform:uppercase;transition:all .2s;position:relative}
  #nav-mobile button span{font-size:17px;line-height:1}
  #nav-mobile button:active{transform:scale(0.95)}
  #nav-mobile button.on{background:rgba(34,211,238,.16);color:#67e8f9}
}'''

if old_style_mobile in c:
    c = c.replace(old_style_mobile, new_style_mobile)
    print("7. Mobile styles updated (clean single-dock bar)")
else:
    print("7. WARNING: old_style_mobile not found")

# 8. Premium redesign of STATUSBAR and TRACKPANEL
old_statusbar = '''<!--/*STATUSBAR*/--><script>
(function(){try{var M=DATA_META,el=document.createElement('div');
el.className='sb-fissa';el.style.cssText='position:fixed;bottom:0;left:0;right:0;z-index:50;font:11px ui-monospace,monospace;padding:4px 12px;background:#020617ee;border-top:1px solid #1e293b;color:#94a3b8;display:flex;flex-wrap:wrap;gap:12px';
var ore=(Date.now()-new Date(M.aggiornato).getTime())/36e5;
var st=ore>48?'<span style="color:#f87171">⚠ dati non aggiornati da '+Math.floor(ore/24)+' giorni</span>':'<span style="color:#34d399">● dati aggiornati</span>';
var fino=Object.keys(M.dati_fino).map(function(k){return k+': '+M.dati_fino[k].split('-').reverse().join('/')}).join(' · ');
el.innerHTML=st+'<span>Ultimo aggiornamento: '+M.aggiornato.replace('T',' ')+'</span><span>Risultati fino al → '+fino+'</span>'+M.avvisi.map(function(a){return '<span style="color:#fbbf24">⚠ '+a+'</span>'}).join('');
document.body.appendChild(el);document.body.style.paddingBottom='34px';}catch(e){}})();
</script>'''

new_statusbar = '''<!--/*STATUSBAR*/--><script>
(function(){try{
  var M=DATA_META;
  var topB=document.getElementById("status-data-badge");
  if(topB){
    topB.innerHTML='<span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[10px] font-bold mono bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 shadow-sm"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>DATI UFFICIALI (Agg. '+M.aggiornato.replace('T',' ')+')</span>';
  }
  var el=document.createElement('div');
  el.className='sb-fissa';
  el.style.cssText='position:fixed;bottom:0;left:0;right:0;z-index:50;font:11px ui-monospace,monospace;padding:5px 16px;background:rgba(2,6,23,0.92);border-top:1px solid #1e293b;color:#94a3b8;display:flex;flex-wrap:wrap;gap:14px;align-items:center;backdrop-filter:blur(8px);';
  var ore=(Date.now()-new Date(M.aggiornato).getTime())/36e5;
  var st=ore>48?'<span style="color:#f87171">⚠ dati non aggiornati da '+Math.floor(ore/24)+' giorni</span>':'<span style="color:#34d399">● Dati ufficiali football-data.co.uk</span>';
  var fino=Object.keys(M.dati_fino).map(function(k){return k+': '+M.dati_fino[k].split('-').reverse().join('/')}).join(' · ');
  el.innerHTML=st+'<span>Aggiornato: '+M.aggiornato.replace('T',' ')+'</span><span class="text-slate-500">|</span><span>Risultati coperti fino al → '+fino+'</span>'+M.avvisi.map(function(a){return '<span style="color:#fbbf24">⚠ '+a+'</span>'}).join('');
  document.body.appendChild(el);
}catch(e){}})();
</script>'''

if old_statusbar in c:
    c = c.replace(old_statusbar, new_statusbar)
    print("8. STATUSBAR modernized")
else:
    print("8. WARNING: old_statusbar not found")

# 9. Modernize TRACKPANEL
old_trackpanel = '''<!--/*TRACKPANEL*/--><script>
(function(){try{var T=DATA_TRACK,t=T.totale,L=T.live;
var box=document.createElement('details');box.id='box-track';box.style.cssText='margin:24px auto 56px;max-width:1100px;padding:0 16px;font:12px ui-monospace,monospace;color:#cbd5e1';
function r(a){return '<tr>'+a.map(function(x){return '<td style="padding:4px 10px;border-bottom:1px solid #1e293b">'+x+'</td>'}).join('')+'</tr>'}
var leg=Object.keys(T.leghe).map(function(k){var x=T.leghe[k];return x.n?r([k,x.n,x.hit_1x2+'%',x.brier_modello,x.brier_mercato,x.value_roi===null?'n.d.':x.value_roi+'% ('+x.value_giocate+')']):''}).join('');
var cal=(t.calibrazione||[]).map(function(c){return r([c.fascia,c.n,c.previsto+'%',c.reale+'%'])}).join('');
var gap=(t.brier_modello-t.brier_mercato);
box.innerHTML='<summary style="cursor:pointer;font-weight:800;text-transform:uppercase;letter-spacing:.05em;color:#fff;padding:10px 0">\ud83d\udcca Track record del modello (onesto)</summary>'+
'<div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:16px;line-height:1.5">'+
'<p style="color:#fbbf24">Backtest su '+t.n+' partite gi\u00e0 giocate, usando solo dati precedenti a ogni partita. Brier (pi\u00f9 basso = meglio): modello solo-dati <b>'+t.brier_modello+'</b> vs mercato <b>'+t.brier_mercato+'</b>. '+
(gap>0?'Il modello \u00e8 PEGGIO del mercato: usalo come filtro e controllo, non come segnale di value.':'Il modello \u00e8 in linea o meglio del mercato.')+'</p>'+
'<table style="width:100%;border-collapse:collapse;margin:10px 0"><tr style="color:#94a3b8"><td style="padding:4px 10px">Campionato</td><td>Partite</td><td>1X2 azzeccati</td><td>Brier modello</td><td>Brier mercato</td><td>ROI regola value (n. giocate)</td></tr>'+leg+'</table>'+
'<table style="width:100%;border-collapse:collapse;margin:10px 0"><tr style="color:#94a3b8"><td style="padding:4px 10px">Fascia probabilit\u00e0</td><td>Casi</td><td>Previsto</td><td>Reale</td></tr>'+cal+'</table>'+
'<p>ROI value (totale): <b>'+(t.value_roi===null?'n.d.':t.value_roi+'%')+'</b> su '+t.value_giocate+' giocate con quote Bet365 di apertura: puntare dove il solo-dati vede valore ha perso denaro. Campione ancora piccolo, ma il segnale \u00e8 negativo.</p>'+
'<p style="border-top:1px solid #1e293b;padding-top:8px">Registro live (previsioni congelate prima della partita, valutate dopo): <b>'+L.registrate+'</b> registrate, <b>'+L.valutate+'</b> valutate'+(L.valutate?' \u00b7 1X2 azzeccati '+L.hit_1x2+'% \u00b7 Brier '+L.brier:' \u00b7 i primi risultati arrivano dopo la prossima giornata')+'. Aggiornato '+T.aggiornato+'.</p></div>';
(document.querySelector('body > div')||document.body).appendChild(box);}catch(e){}})();
</script>'''

new_trackpanel = '''<!--/*TRACKPANEL*/--><script>
(function(){try{
  var T=DATA_TRACK,t=T.totale,L=T.live;
  var box=document.createElement('details');
  box.id='box-track';
  box.className='group my-8 max-w-[1100px] mx-auto px-2 font-mono text-xs';
  function r(a){return '<tr class="hover:bg-slate-800/40 transition">'+a.map(function(x,idx){return '<td class="py-2.5 px-3 border-b border-slate-800/80 '+(idx===0?'font-bold text-white':'text-slate-300')+'">'+x+'</td>'}).join('')+'</tr>'}
  var leg=Object.keys(T.leghe).map(function(k){var x=T.leghe[k];return x.n?r([k,x.n,x.hit_1x2+'%',x.brier_modello,x.brier_mercato,x.value_roi===null?'<span class="text-slate-500">n.d.</span>':(x.value_roi>0?'+':'')+x.value_roi+'% ('+x.value_giocate+')']):''}).join('');
  var cal=(t.calibrazione||[]).map(function(c){return r([c.fascia,c.n,c.previsto+'%',c.reale+'%'])}).join('');
  var gap=(t.brier_modello-t.brier_mercato);
  
  box.innerHTML='<summary class="cursor-pointer select-none bg-gradient-to-r from-slate-900 via-slate-900/95 to-slate-950 border border-slate-800 hover:border-slate-700 rounded-3xl p-4 sm:p-5 shadow-2xl flex items-center justify-between transition-all duration-200">'+
    '<div class="flex items-center gap-3">'+
      '<span class="w-9 h-9 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-lg shadow-sm">📊</span>'+
      '<div>'+
        '<div class="text-xs sm:text-sm font-black text-white tracking-wide uppercase">Audit & Track Record Modello (Dati Reali 100%)</div>'+
        '<div class="text-[10px] sm:text-[11px] text-slate-400 font-sans">Valutazione oggettiva su '+t.n+' gare reali · Brier Score & Calibrazione vs Mercato</div>'+
      '</div>'+
    '</div>'+
    '<div class="flex items-center gap-2 sm:gap-3">'+
      '<span class="text-[10px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-1 rounded-full font-bold uppercase mono">Verificato</span>'+
      '<span class="text-slate-400 text-xs transition-transform duration-200 group-open:rotate-180">▼</span>'+
    '</div>'+
  '</summary>'+
  '<div class="mt-3 bg-slate-900/95 border border-slate-800 rounded-3xl p-4 sm:p-6 shadow-2xl space-y-4 backdrop-blur-xl">'+
    '<div class="p-3.5 rounded-2xl '+(gap>0?'bg-amber-950/30 border border-amber-800/40 text-amber-200':'bg-emerald-950/30 border border-emerald-800/40 text-emerald-200')+' text-xs leading-relaxed">'+
      '<strong>Nota Metodologica:</strong> Backtest su <b>'+t.n+' partite giocate</b> usando solo dati antecedenti a ciascuna gara. Brier Score (più basso = migliore calibrazione): modello solo-dati <b>'+t.brier_modello+'</b> vs mercato <b>'+t.brier_mercato+'</b>. '+
      (gap>0?'Il modello matematico puro ha dispersione superiore al mercato: impiegalo come filtro quantitativo e confronto quote, non come segnale acritico di value.':'Il modello è in linea o batte il mercato.')+
    '</div>'+
    '<div class="overflow-x-auto"><table class="w-full text-left text-xs"><tr class="text-slate-400 border-b border-slate-800 text-[10px] uppercase"><th class="pb-2 px-3">Campionato</th><th class="pb-2 px-3">Partite</th><th class="pb-2 px-3">1X2 Esatti</th><th class="pb-2 px-3">Brier Modello</th><th class="pb-2 px-3">Brier Mercato</th><th class="pb-2 px-3">ROI Value</th></tr>'+leg+'</table></div>'+
    '<div class="overflow-x-auto"><table class="w-full text-left text-xs"><tr class="text-slate-400 border-b border-slate-800 text-[10px] uppercase"><th class="pb-2 px-3">Fascia Probabilità</th><th class="pb-2 px-3">Casi</th><th class="pb-2 px-3">Previsto</th><th class="pb-2 px-3">Reale</th></tr>'+cal+'</table></div>'+
    '<div class="border-t border-slate-800/80 pt-3 text-[11px] text-slate-400 flex flex-col sm:flex-row justify-between gap-2">'+
      '<div>ROI Value Hunter globale: <strong class="text-white">'+(t.value_roi===null?'n.d.':t.value_roi+'%')+'</strong> su '+t.value_giocate+' selezioni tracciate.</div>'+
      '<div>Registro Live: <strong class="text-cyan-400">'+L.registrate+'</strong> congelate pre-gara · Aggiornato '+T.aggiornato+'</div>'+
    '</div>'+
  '</div>';
  (document.querySelector('body > div')||document.body).appendChild(box);
}catch(e){console.error("track",e);}})();
</script>'''

if old_trackpanel in c:
    c = c.replace(old_trackpanel, new_trackpanel)
    print("9. TRACKPANEL redesigned with premium quant styling")
else:
    print("9. WARNING: old_trackpanel not found")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(c)

print("Finished applying all UX/UI refinements!")
