import json
import re

def main():
    with open('scheda-partita-dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    with open('scripts/statistiche_forma_serie_a.json', 'r', encoding='utf-8') as f:
        forma_json = f.read()

    # 1. Embed DATA_FORMA into script
    if 'const DATA_FORMA = ' not in html:
        target_script = '<script>'
        forma_injection = f"<script>\n    const DATA_FORMA = {forma_json};\n"
        html = html.replace(target_script, forma_injection, 1)
        print('1. DATA_FORMA successfully embedded.')
    else:
        print('1. DATA_FORMA already present.')

    # 2. Update Layout structure after banner-primo-ripiano
    # Currently after banner-primo-ripiano we have:
    # <!-- BOX VERDETTO & VALORE MATEMATICO CON GAUGE -->
    # We want:
    # <!-- MODULO 2: GUIDA FORMA REALE & xG PERFORMANCE -->
    # <div id="box-forma-e-xg"></div>
    #
    # <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
    #   <div class="lg:col-span-8 space-y-6">
    #     <!-- BOX VERDETTO -->
    #     <!-- PRONOSTICI SCORREVOLI -->
    #     <!-- MODULO 3: VALUE HUNTER ODDS COMPARATOR -->
    #     <div id="box-comparatore-quote"></div>
    #     <!-- MODULO 1: HEATMAP DINAMICA DIXON-COLES -->
    #     <div id="box-heatmap-dixon-coles"></div>
    #     <!-- BOX ANALISI TRACCIABILE -->
    #   </div>
    #   <div class="lg:col-span-4 space-y-6 sticky top-6">
    #     <!-- MODULO 4: SCHEDINA QUANTITATIVA INTERATTIVA -->
    #     <div id="box-schedina-interattiva"></div>
    #     <!-- BOX DISCIPLINA E REGOLE DI GESTIONE CAPITALE -->
    #     <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-5 shadow-2xl space-y-3">
    #       ...
    #     </div>
    #   </div>
    # </div>

    # Let's inspect where banner-primo-ripiano ends
    marker_banner_end = '<!-- Barra di potenziale offensivo in basso -->'
    pos_banner_end = html.find(marker_banner_end)
    # Find the closing </div> of banner-primo-ripiano
    pos_close_banner = html.find('</div>\n\n    <!-- BOX VERDETTO', pos_banner_end)
    if pos_close_banner == -1:
        # try without strict newline
        pos_close_banner = html.find('</div>', pos_banner_end + 300)
    
    # Let's locate the entire middle section between banner and footer
    marker_verdetto = '<!-- BOX VERDETTO & VALORE MATEMATICO'
    marker_footer = '<!-- FOOTER LEGALE'
    
    pos_v = html.find(marker_verdetto)
    pos_f = html.find(marker_footer)
    
    if pos_v != -1 and pos_f != -1:
        print(f'Found middle section from {pos_v} to {pos_f}')
        
        new_middle_section = '''<!-- MODULO 2: GUIDA FORMA REALE & xG PERFORMANCE (ULTIMI 5 MATCH REALI) -->
    <div id="box-forma-e-xg">
      <!-- Generato dinamicamente via JS dai 110 match reali di Serie A 2026/27 -->
    </div>

    <!-- GRIGLIA A 2 COLONNE: CORE ANALITICO (8/12) & SCHEDINA QUANTITATIVA / SLIP (4/12) -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      
      <!-- COLONNA PRINCIPALE ANALITICA (8/12) -->
      <div class="lg:col-span-8 space-y-6">
        
        <!-- BOX VERDETTO & VALORE MATEMATICO CON GAUGE -->
        <div id="box-verdetto-valore" class="bg-gradient-to-br from-slate-900 to-slate-950 border border-emerald-500/40 rounded-3xl p-6 shadow-2xl relative overflow-hidden">
          <!-- Generato via JS -->
        </div>

        <!-- PRONOSTICI SCORREVOLI SINCRONIZZATI (Alta Probabilità, Miglior Combo, Pronostico Hard, Pronostico Extra) -->
        <div id="box-pronostici-scorrevoli" class="bg-gradient-to-br from-slate-900/90 to-slate-950/90 border border-slate-800 rounded-3xl p-5 shadow-2xl relative overflow-hidden space-y-4">
          <!-- Intestazione con sincronizzazione timer -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
            <div class="flex items-center gap-2">
              <span class="bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider mono flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span> ROTAZIONE PRONOSTICI (4s)
              </span>
              <span class="text-xs text-slate-400 font-medium">Sincronizzati col modello quantitativo</span>
            </div>
            
            <div class="flex items-center gap-1.5 self-end sm:self-auto">
              <span class="text-[10px] text-slate-400 mono">Fase:</span>
              <span id="badge-fase-pronostico" class="bg-slate-800 text-cyan-300 border border-slate-700 text-[10px] font-bold px-2 py-0.5 rounded-md mono">
                Fase 1 · Base
              </span>
            </div>
          </div>

          <!-- Card Pronostico Attivo in Evidenza -->
          <div id="pronostico-attivo-dettaglio" class="bg-slate-950/90 border border-cyan-500/30 rounded-2xl p-4 shadow-xl relative overflow-hidden transition-all duration-500">
            <!-- Popolato via JS in sincronia con la fase torta -->
          </div>

          <!-- Griglia Compatta delle 4 Opzioni Selezionabili -->
          <div id="griglia-mini-pronostici" class="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1">
            <!-- 4 Card cliccabili popolate via JS -->
          </div>
        </div>

        <!-- MODULO 3: VALUE HUNTER ODDS COMPARATOR (Prezzo Equo vs Bookmakers ADM) -->
        <div id="box-comparatore-quote">
          <!-- Popolato dinamicamente da JS -->
        </div>

        <!-- MODULO 1: HEATMAP RISULTATI ESATTI DIXON-COLES 100% DINAMICA -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 shadow-2xl space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 class="text-sm font-extrabold uppercase tracking-wider text-white flex items-center gap-2">
                <span>🔥</span> Heatmap Punteggi Esatti (Dixon-Coles Live)
              </h3>
              <p class="text-xs text-slate-400">Distribuzione bivariata delle probabilità di punteggio (0-3 gol) calcolata live</p>
            </div>
            <div id="heatmap-top-badge" class="text-xs mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/40 px-3 py-1.5 rounded-xl font-bold self-start sm:self-auto">
              Top: Calcolo in corso...
            </div>
          </div>

          <div class="overflow-x-auto">
            <div class="min-w-[480px]" id="heatmap-grid-container">
              <!-- Popolato dinamicamente da JS per ogni match -->
            </div>
          </div>
        </div>

        <!-- BOX ANALISI TRACCIABILE & RISCHI -->
        <div id="box-analisi-tracciabile" class="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 shadow-2xl space-y-4">
          <!-- Generato via JS -->
        </div>

      </div>

      <!-- COLONNA LATERALE: SCHEDINA QUANTITATIVA (+EV BET SLIP) & GESTIONE BANKROLL (4/12) -->
      <div class="lg:col-span-4 space-y-6 lg:sticky lg:top-6">
        
        <!-- MODULO 4: SCHEDINA QUANTITATIVA INTERATTIVA -->
        <div id="box-schedina-interattiva">
          <!-- Generato via JS con calcolo real-time di moltiplicatore, probabilità e Kelly -->
        </div>

        <!-- BOX DISCIPLINA E REGOLE DI GESTIONE CAPITALE -->
        <div class="bg-gradient-to-br from-slate-900/90 to-slate-950/90 border border-slate-800 rounded-3xl p-5 shadow-2xl space-y-3">
          <div class="flex items-center gap-2 border-b border-slate-800 pb-2">
            <span class="text-amber-400 text-sm">🛡️</span>
            <span class="text-xs font-black uppercase mono text-white">Regole di Gestione Capitale</span>
          </div>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start gap-2">
              <span class="text-cyan-400 font-bold">1.</span>
              <span><strong>Solo scommesse a +EV:</strong> Non piazzare mai una giocata con quota bookmaker inferiore al prezzo equo.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-cyan-400 font-bold">2.</span>
              <span><strong>Frazione di Kelly prudente (1/4):</strong> Protegge la cassa dai drawdown statistici fisiologici.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-cyan-400 font-bold">3.</span>
              <span><strong>Tracciamento rigoroso:</strong> Ogni giocata viene registrata con quota di chiusura (CLV tracking).</span>
            </li>
          </ul>
        </div>

      </div>

    </div>

    '''
        html = html[:pos_v] + new_middle_section + html[pos_f:]
        print('2. Middle layout section replaced successfully.')
    else:
        print('Error: pos_v or pos_f not found.')

    with open('scheda-partita-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('HTML layout saved.')

if __name__ == '__main__':
    main()
