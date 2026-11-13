import re

def main():
    with open('scheda-partita-dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update LOGHI_SQUADRE and add LOGHI_FALLBACK_CDN
    old_loghi_start = html.find('const LOGHI_SQUADRE = {')
    old_loghi_end = html.find('};', old_loghi_start) + 2

    new_loghi_def = """const LOGHI_SQUADRE = {
      // Serie A 2026/27 (File locali ad altissima risoluzione, 0 latenza e 0 blocchi)
      "Atalanta": "./assets/loghi/atalanta.png",
      "Bologna": "./assets/loghi/bologna.png",
      "Cagliari": "./assets/loghi/cagliari.png",
      "Como": "./assets/loghi/como.png",
      "Fiorentina": "./assets/loghi/fiorentina.png",
      "Frosinone": "./assets/loghi/frosinone.png",
      "Genoa": "./assets/loghi/genoa.png",
      "Inter": "./assets/loghi/inter.png",
      "Juventus": "./assets/loghi/juventus.png",
      "Lazio": "./assets/loghi/lazio.png",
      "Lecce": "./assets/loghi/lecce.png",
      "Milan": "./assets/loghi/milan.png",
      "Monza": "./assets/loghi/monza.png",
      "Napoli": "./assets/loghi/napoli.png",
      "Parma": "./assets/loghi/parma.png",
      "Roma": "./assets/loghi/roma.png",
      "Sassuolo": "./assets/loghi/sassuolo.png",
      "Torino": "./assets/loghi/torino.png",
      "Udinese": "./assets/loghi/udinese.png",
      "Venezia": "./assets/loghi/venezia.png",
      // Top Club Europei
      "Arsenal": "./assets/loghi/arsenal.png",
      "Real Madrid": "./assets/loghi/real_madrid.png",
      "Barcelona": "./assets/loghi/barcelona.png",
      "Manchester City": "./assets/loghi/manchester_city.png",
      "Liverpool": "./assets/loghi/liverpool.png",
      "Chelsea": "./assets/loghi/chelsea.png",
      "Manchester United": "./assets/loghi/manchester_united.png",
      "Tottenham": "./assets/loghi/tottenham.png",
      "Bayern": "./assets/loghi/bayern.png",
      "Bayern München": "./assets/loghi/bayern_munchen.png",
      "PSG": "./assets/loghi/psg.png",
      "Paris Saint-Germain": "./assets/loghi/paris_saint-germain.png"
    };

    // Fallback Cloud CDN se i file locali non vengono trovati
    const LOGHI_FALLBACK_CDN = {
      "Napoli": "https://media.api-sports.io/football/teams/492.png",
      "Juventus": "https://media.api-sports.io/football/teams/496.png",
      "Milan": "https://media.api-sports.io/football/teams/489.png",
      "Inter": "https://media.api-sports.io/football/teams/505.png",
      "Roma": "https://media.api-sports.io/football/teams/497.png",
      "Lazio": "https://media.api-sports.io/football/teams/487.png",
      "Atalanta": "https://media.api-sports.io/football/teams/499.png",
      "Fiorentina": "https://media.api-sports.io/football/teams/502.png",
      "Bologna": "https://media.api-sports.io/football/teams/500.png",
      "Torino": "https://media.api-sports.io/football/teams/503.png",
      "Como": "https://media.api-sports.io/football/teams/895.png",
      "Cagliari": "https://media.api-sports.io/football/teams/490.png",
      "Parma": "https://media.api-sports.io/football/teams/523.png",
      "Udinese": "https://media.api-sports.io/football/teams/494.png",
      "Genoa": "https://media.api-sports.io/football/teams/495.png",
      "Lecce": "https://media.api-sports.io/football/teams/867.png",
      "Monza": "https://media.api-sports.io/football/teams/1579.png",
      "Sassuolo": "https://media.api-sports.io/football/teams/488.png",
      "Frosinone": "https://media.api-sports.io/football/teams/512.png",
      "Venezia": "https://media.api-sports.io/football/teams/517.png",
      "Arsenal": "https://media.api-sports.io/football/teams/42.png",
      "Real Madrid": "https://media.api-sports.io/football/teams/541.png",
      "Barcelona": "https://media.api-sports.io/football/teams/529.png",
      "Manchester City": "https://media.api-sports.io/football/teams/50.png",
      "Liverpool": "https://media.api-sports.io/football/teams/40.png",
      "Chelsea": "https://media.api-sports.io/football/teams/49.png",
      "Manchester United": "https://media.api-sports.io/football/teams/33.png",
      "Tottenham": "https://media.api-sports.io/football/teams/47.png",
      "Bayern": "https://media.api-sports.io/football/teams/157.png",
      "Bayern München": "https://media.api-sports.io/football/teams/157.png",
      "PSG": "https://media.api-sports.io/football/teams/85.png",
      "Paris Saint-Germain": "https://media.api-sports.io/football/teams/85.png"
    };

    function gestisciErroreLogo(img, tipo) {
      if (!img.dataset.triedCdn && PARTITA_CORRENTE) {
        img.dataset.triedCdn = "1";
        const teamName = (tipo === 'casa') ? PARTITA_CORRENTE.casa.nome : PARTITA_CORRENTE.ospite.nome;
        if (LOGHI_FALLBACK_CDN[teamName]) {
          img.src = LOGHI_FALLBACK_CDN[teamName];
          return;
        }
      }
      img.classList.add("hidden");
      const sigla = document.getElementById(`sigla-${tipo}`);
      if (sigla) sigla.classList.remove("hidden");
    }"""

    if old_loghi_start != -1:
        html = html[:old_loghi_start] + new_loghi_def + html[old_loghi_end:]
        print('1. LOGHI_SQUADRE and LOGHI_FALLBACK_CDN updated successfully.')
    else:
        print('Error: old_loghi_start not found.')

    # 2. Update aggiornaStrisciaPartite with double fallback
    old_strip_fn_start = html.find('function aggiornaStrisciaPartite')
    old_strip_fn_end = html.find('function selezionaPartita', old_strip_fn_start)

    new_strip_fn = """function aggiornaStrisciaPartite(turno, partitaIdSelezionata) {
      const strip = document.getElementById("strip-partite-turno");
      if (!strip || !turno || !turno.partite) return;
      let html = "";
      turno.partite.forEach(p => {
        const logoC = LOGHI_SQUADRE[p.casa.nome] || "";
        const logoO = LOGHI_SQUADRE[p.ospite.nome] || "";
        const cdnC = LOGHI_FALLBACK_CDN[p.casa.nome] || "";
        const cdnO = LOGHI_FALLBACK_CDN[p.ospite.nome] || "";
        const isAttiva = (p.id === partitaIdSelezionata);
        const activeCls = isAttiva
          ? "border-cyan-400 bg-cyan-950/60 shadow-lg shadow-cyan-500/20 ring-2 ring-cyan-400/80 scale-[1.02]"
          : "border-slate-800 bg-slate-950/70 hover:border-slate-700 opacity-75 hover:opacity-100";

        const dataPart = p.data ? p.data.split('·')[0].trim() : '';
        const oraPart = p.data && p.data.split('·')[1] ? p.data.split('·')[1].trim() : '';

        html += `
          <div onclick="selezionaPartita('${p.id}')" class="min-w-[175px] cursor-pointer p-2.5 rounded-2xl border transition-all duration-200 ${activeCls} flex flex-col justify-between select-none">
            <div class="flex justify-between items-center text-[10px] text-slate-400 mono font-semibold mb-1.5">
              <span>${dataPart}</span>
              <span class="text-cyan-400 font-bold">${oraPart}</span>
            </div>
            <div class="flex items-center justify-around py-1">
              <div class="w-8 h-8 flex items-center justify-center p-0.5">
                <img src="${logoC}" alt="${p.casa.nome}" class="w-full h-full object-contain filter drop-shadow" onerror="if(!this.dataset.cdn && '${cdnC}'){ this.dataset.cdn='1'; this.src='${cdnC}'; } else { this.style.display='none'; this.nextElementSibling.style.display='block'; }" />
                <span class="hidden font-black text-xs mono text-white">${p.casa.sigla}</span>
              </div>
              <span class="text-[10px] font-black text-slate-500 mono">VS</span>
              <div class="w-8 h-8 flex items-center justify-center p-0.5">
                <img src="${logoO}" alt="${p.ospite.nome}" class="w-full h-full object-contain filter drop-shadow" onerror="if(!this.dataset.cdn && '${cdnO}'){ this.dataset.cdn='1'; this.src='${cdnO}'; } else { this.style.display='none'; this.nextElementSibling.style.display='block'; }" />
                <span class="hidden font-black text-xs mono text-white">${p.ospite.sigla}</span>
              </div>
            </div>
            <div class="mt-1 pt-1.5 border-t border-slate-800/60 flex justify-between items-center text-[11px] font-extrabold">
              <span class="text-white truncate max-w-[68px]">${p.casa.nome}</span>
              <span class="text-slate-500 text-[10px]">-</span>
              <span class="text-white truncate max-w-[68px] text-right">${p.ospite.nome}</span>
            </div>
          </div>
        `;
      });
      strip.innerHTML = html;
    }
    """

    if old_strip_fn_start != -1 and old_strip_fn_end != -1:
        html = html[:old_strip_fn_start] + new_strip_fn + html[old_strip_fn_end:]
        print('2. aggiornaStrisciaPartite updated successfully.')
    else:
        print('Error: old_strip_fn not found.')

    # 3. Update logo images in HTML banner to use gestisciErroreLogo
    html = html.replace('onerror="this.classList.add(\'hidden\'); document.getElementById(\'sigla-casa\').classList.remove(\'hidden\');"', 'onerror="gestisciErroreLogo(this, \'casa\')"')
    html = html.replace('onerror="this.classList.add(\'hidden\'); document.getElementById(\'sigla-ospite\').classList.remove(\'hidden\');"', 'onerror="gestisciErroreLogo(this, \'ospite\')"')

    # Also enhance watermark opacity for high visibility
    html = html.replace('opacity-[0.09] filter blur-[0.5px]', 'opacity-[0.14] filter blur-[0.5px]')

    with open('scheda-partita-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('scheda-partita-dashboard.html updated with bulletproof local + CDN fallback logos!')

if __name__ == '__main__':
    main()
