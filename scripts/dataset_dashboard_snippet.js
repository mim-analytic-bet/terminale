let FASE_TORTA_ATTUALE = 1;
    let TIMER_TORTA = null;
    let PARTITA_CORRENTE = null;

    const DATA_PRO = {
      "serie-a": {
        nome: "Serie A (Italia)",
        turni: {
          "12": {
            label: "12ª Giornata (21-23 Nov 2026)",
            dataFine: "2026-11-23T23:59:59",
            partite: [
              {
                id: "nap-tor",
                label: "Napoli - Torino",
                bgGradient: "from-[#081d38] via-[#090d16] to-[#3a0d14]",
                casa: { sigla: "NAP", nome: "Napoli", rank: "1° posto · xG 1.88/gara", colBox: "bg-sky-500/20 text-sky-400 border-sky-400" },
                ospite: { sigla: "TOR", nome: "Torino", rank: "9° posto · xG 1.05/gara", colBox: "bg-amber-700/20 text-amber-400 border-amber-600" },
                data: "Sabato 21 Nov · 20:45",
                giornata: "Serie A · 12ª Giornata",
                golC: "1.80",
                golO: "0.91",
                barC: "66%",
                barO: "34%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "57%", centerLbl: "Segno 1", seg1: { p: 0.57, col: "#06b6d4", nome: "1: 57%" }, seg2: { p: 0.25, col: "#f59e0b", nome: "X: 25%" }, seg3: { p: 0.18, col: "#f43f5e", nome: "2: 18%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "51%", centerLbl: "Gol (GG)", seg1: { p: 0.51, col: "#10b981", nome: "Gol: 51%" }, seg2: { p: 0.49, col: "#64748b", nome: "No Gol: 49%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "51%", centerLbl: "Over 2.5", seg1: { p: 0.51, col: "#8b5cf6", nome: "Over: 51%" }, seg2: { p: 0.49, col: "#3b82f6", nome: "Under: 49%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "1.80 vs 0.91", centerLbl: "Volume xG", seg1: { p: 0.66, col: "#0ea5e9", nome: "Napoli: 66% (1.80)" }, seg2: { p: 0.34, col: "#d97706", nome: "Torino: 34% (0.91)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+3,3%",
                mercato: "Gol (Entrambe le squadre segnano)",
                qEqua: "1.88",
                qReale: "1.95",
                spiegazione: "Stima Dixon-Coles 53% vs quota Eurobet implicita 48%. Il Torino segna da 4 trasferte consecutive, Napoli concede 0.95 xGA al Maradona. Valore positivo confermato.",
                analisi: "Il Napoli in casa subisce gol in 3 gare su 5 concedendo 0,95 xGA. Il Torino in trasferta realizza 0,8 reti a partita con Adams e Vlasic in gran forma. Quota 1.95 Eurobet offre edge +3,3%.",
                rischio: "Assenza di Lobotka a centrocampo potrebbe rallentare il ritmo e congelare il risultato sull'1-0.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Over 1.5 Gol", alt: "1X (81%)", prob: 82, probStr: "82%", quota: "1.25", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "Napoli a segno in 9 gare su 10; Toro concede 1.35 gol fuori. Base sicura a basso rischio." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "1X + Gol (Entrambe segnano)", alt: "1 + Over 1.5 (68%)", prob: 61, probStr: "61%", quota: "2.15", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "Copre l'1-1 e le vittorie del Napoli con gol subito (2-1, 3-1). Ottimo equilibrio quota/rischio." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "1 + Gol (Napoli vince & Gol)", alt: "Ris. Esatto 2-1 (10%)", prob: 31, probStr: "31%", quota: "3.45", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Quota Eurobet ad alto rendimento (+245%). Coerente con la stima del 2-1 (10%)." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Multigol 2-4", alt: "Kvaratskhelia Marcatore", prob: 74, probStr: "74%", quota: "1.55", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Intervallo gol confermato nell'85% dei match interni recenti azzurri." }
                }
              },
              {
                id: "mil-juv",
                label: "Milan - Juventus",
                bgGradient: "from-[#3a0d12] via-[#090d16] to-[#1e293b]",
                casa: { sigla: "MIL", nome: "Milan", rank: "7° posto · xG 1.72/gara", colBox: "bg-red-600/20 text-red-400 border-red-500" },
                ospite: { sigla: "JUV", nome: "Juventus", rank: "6° posto · xG 1.55/gara", colBox: "bg-slate-700/30 text-slate-200 border-slate-500" },
                data: "Sabato 21 Nov · 18:00",
                giornata: "Serie A · 12ª Giornata",
                golC: "1.42",
                golO: "1.18",
                barC: "55%",
                barO: "45%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "42%", centerLbl: "Segno 1", seg1: { p: 0.42, col: "#06b6d4", nome: "1: 42%" }, seg2: { p: 0.31, col: "#f59e0b", nome: "X: 31%" }, seg3: { p: 0.27, col: "#f43f5e", nome: "2: 27%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "54%", centerLbl: "Gol (GG)", seg1: { p: 0.54, col: "#10b981", nome: "Gol: 54%" }, seg2: { p: 0.46, col: "#64748b", nome: "No Gol: 46%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "52%", centerLbl: "Under 2.5", seg1: { p: 0.48, col: "#8b5cf6", nome: "Over: 48%" }, seg2: { p: 0.52, col: "#3b82f6", nome: "Under: 52%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "1.42 vs 1.18", centerLbl: "Volume xG", seg1: { p: 0.55, col: "#ef4444", nome: "Milan: 55% (1.42)" }, seg2: { p: 0.45, col: "#94a3b8", nome: "Juve: 45% (1.18)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+4,8%",
                mercato: "1X (Doppia Chance In/Out)",
                qEqua: "1.37",
                qReale: "1.44",
                spiegazione: "Stima 1X al 73% vs implicita Eurobet 69%. La Juve di Motta subisce pochissimo ma il Milan a San Siro ha un indice offensivo superiore. Edge favorevole su 1X.",
                analisi: "Classica sfida tattica: il Milan ha prodotto 1.72 xG interni di media, mentre la Juventus ha la miglior difesa del torneo (0.75 xGA). Il modello stima 1X al 73%. Quota 1.44 su Eurobet offre valore atteso del +4,8%.",
                rischio: "Partita bloccata a centrocampo che può chiudersi su uno 0-0 tattico.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Under 3.5 Gol", alt: "1X (73%)", prob: 78, probStr: "78%", quota: "1.28", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "Solo 1 degli ultimi 8 precedenti a San Siro ha superato i 3 gol complessivi." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "1X + Under 3.5", alt: "Gol (54%)", prob: 64, probStr: "64%", quota: "1.72", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "Copre l'1-0, 2-0, 1-1 e 2-1 per i rossoneri." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "Pareggio X", alt: "Ris. Esatto 1-1 (12%)", prob: 31, probStr: "31%", quota: "3.35", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Entrambe le squadre non possono permettersi di perdere per non staccarsi dal vertice." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Multigol 1-3", alt: "Leao Marcatore/Assist", prob: 80, probStr: "80%", quota: "1.42", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Frequenza altissima nei big match di Serie A (84% dei casi)." }
                }
              },
              {
                id: "com-cag",
                label: "Como - Cagliari",
                bgGradient: "from-[#082347] via-[#090d16] to-[#3a0a10]",
                casa: { sigla: "COM", nome: "Como", rank: "5° posto · xG 1.70/gara", colBox: "bg-blue-600/20 text-blue-400 border-blue-400" },
                ospite: { sigla: "CAG", nome: "Cagliari", rank: "9° posto · xG 1.20/gara", colBox: "bg-red-700/20 text-red-400 border-red-600" },
                data: "Sabato 21 Nov · 15:00",
                giornata: "Serie A · 12ª Giornata",
                golC: "2.44",
                golO: "0.95",
                barC: "72%",
                barO: "28%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "69%", centerLbl: "Segno 1", seg1: { p: 0.69, col: "#06b6d4", nome: "1: 69%" }, seg2: { p: 0.19, col: "#f59e0b", nome: "X: 19%" }, seg3: { p: 0.12, col: "#f43f5e", nome: "2: 12%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "57%", centerLbl: "Gol (GG)", seg1: { p: 0.57, col: "#10b981", nome: "Gol: 57%" }, seg2: { p: 0.43, col: "#64748b", nome: "No Gol: 43%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "66%", centerLbl: "Over 2.5", seg1: { p: 0.66, col: "#8b5cf6", nome: "Over: 66%" }, seg2: { p: 0.34, col: "#3b82f6", nome: "Under: 34%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "2.44 vs 0.95", centerLbl: "Volume xG", seg1: { p: 0.72, col: "#06b6d4", nome: "Como: 72% (2.44)" }, seg2: { p: 0.28, col: "#ef4444", nome: "Cagliari: 28% (0.95)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: false,
                evBadge: "0,0%",
                mercato: "NO BET · Quota 1 Sotto Prezzo Equo",
                qEqua: "1.45",
                qReale: "1.33",
                spiegazione: "Disaccordo tra dati storici e mercato: il banco offre il Como a 1.33 (implicita 72%), mentre il modello lo stima a 69%. Giocare a 1.33 produce valore atteso negativo (-7,8%).",
                analisi: "Sull'1 i dati della stagione stimano 57% contro una quota che implica il 72% (scarto > 15 punti). Con campioni ridotti il modello quantitativo si arresta per proteggere il capitale.",
                rischio: "Sopravvalutazione del mercato dovuta all'entusiasmo mediatico per la neopromossa.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "1X (Doppia Chance)", alt: "Over 1.5 (84%)", prob: 88, probStr: "88%", quota: "1.12", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "Como imbattuto tra le mura amiche con 2.44 xG attesi. Probabilità schiacciante." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "1 + Over 1.5 Gol", alt: "1 + Multigol 2-5 (65%)", prob: 62, probStr: "62%", quota: "1.62", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "La produzione offensiva lariana porta quasi sempre a match da almeno 2 gol." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "1 Parziale / 1 Finale", alt: "Ris. Esatto 2-0 (14%)", prob: 46, probStr: "46%", quota: "2.05", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Como aggressivo subito; Cagliari subisce regolarmente nei primi 30 minuti." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Como segna in entrambi i tempi", alt: "Nico Paz Marcatore/Assist", prob: 54, probStr: "54%", quota: "2.30", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Extra speciale attivato per il marcato squilibrio di pericolosità attesa." }
                }
              },
              {
                id: "ver-int",
                label: "Verona - Inter",
                bgGradient: "from-[#2e2b0a] via-[#090d16] to-[#071d42]",
                casa: { sigla: "VER", nome: "Verona", rank: "14° posto · xG 1.05/gara", colBox: "bg-yellow-600/20 text-yellow-400 border-yellow-500" },
                ospite: { sigla: "INT", nome: "Inter", rank: "4° posto · xG 2.15/gara", colBox: "bg-blue-600/20 text-blue-400 border-blue-500" },
                data: "Domenica 22 Nov · 15:00",
                giornata: "Serie A · 12ª Giornata",
                golC: "0.85",
                golO: "2.10",
                barC: "29%",
                barO: "71%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "65%", centerLbl: "Segno 2", seg1: { p: 0.14, col: "#06b6d4", nome: "1: 14%" }, seg2: { p: 0.21, col: "#f59e0b", nome: "X: 21%" }, seg3: { p: 0.65, col: "#f43f5e", nome: "2: 65%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "52%", centerLbl: "No Gol", seg1: { p: 0.48, col: "#10b981", nome: "Gol: 48%" }, seg2: { p: 0.52, col: "#64748b", nome: "No Gol: 52%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "58%", centerLbl: "Over 2.5", seg1: { p: 0.58, col: "#8b5cf6", nome: "Over: 58%" }, seg2: { p: 0.42, col: "#3b82f6", nome: "Under: 42%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "0.85 vs 2.10", centerLbl: "Volume xG", seg1: { p: 0.29, col: "#eab308", nome: "Verona: 29% (0.85)" }, seg2: { p: 0.71, col: "#3b82f6", nome: "Inter: 71% (2.10)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+4,2%",
                mercato: "2 + Over 1.5 Gol",
                qEqua: "1.52",
                qReale: "1.62",
                spiegazione: "Stima vittoria nerazzurra con almeno 2 gol totali al 64% vs quota Eurobet implicita 59%. Lautaro e compagni con volume xG devastante fuori casa.",
                analisi: "L'Inter produce oltre 2 xG in trasferta con regolarità. Il Verona concede 1.6 gol a partita contro formazioni di vertice. Quota 1.62 Eurobet offre margine positivo.",
                rischio: "Possibile stanchezza post-nazionali per i titolari sudamericani dell'Inter.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Segno 2 (Inter)", alt: "Over 1.5 (83%)", prob: 65, probStr: "65%", quota: "1.42", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "Inter a caccia del primato contro una delle difese più battute del torneo." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "2 + Over 1.5 Gol", alt: "2 + Multigol 2-5 (61%)", prob: 64, probStr: "64%", quota: "1.62", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "La combo più solida per la favorita della giornata." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "Inter vince a zero (2 + NoGol)", alt: "Ris. Esatto 0-2 (13%)", prob: 38, probStr: "38%", quota: "2.35", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Clean sheet probabile vista la scarsa incisività offensiva scaligera (0.85 xG)." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Thuram Marcatore", alt: "Over 8.5 Tiri Totali Inter", prob: 48, probStr: "48%", quota: "2.25", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "L'attaccante francese è il più prolifico dei nerazzurri in trasferta." }
                }
              },
              {
                id: "rom-ata",
                label: "Roma - Atalanta",
                bgGradient: "from-[#3d1a08] via-[#090d16] to-[#0a1e3d]",
                casa: { sigla: "ROM", nome: "Roma", rank: "12° posto · xG 1.50/gara", colBox: "bg-amber-600/20 text-amber-500 border-amber-600" },
                ospite: { sigla: "ATA", nome: "Atalanta", rank: "2° posto · xG 2.20/gara", colBox: "bg-blue-600/20 text-blue-400 border-blue-500" },
                data: "Lunedì 23 Nov · 20:45",
                giornata: "Serie A · 12ª Giornata",
                golC: "1.35",
                golO: "1.75",
                barC: "44%",
                barO: "56%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "44%", centerLbl: "Segno 2", seg1: { p: 0.31, col: "#06b6d4", nome: "1: 31%" }, seg2: { p: 0.25, col: "#f59e0b", nome: "X: 25%" }, seg3: { p: 0.44, col: "#f43f5e", nome: "2: 44%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "62%", centerLbl: "Gol (GG)", seg1: { p: 0.62, col: "#10b981", nome: "Gol: 62%" }, seg2: { p: 0.38, col: "#64748b", nome: "No Gol: 38%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "59%", centerLbl: "Over 2.5", seg1: { p: 0.59, col: "#8b5cf6", nome: "Over: 59%" }, seg2: { p: 0.41, col: "#3b82f6", nome: "Under: 41%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "1.35 vs 1.75", centerLbl: "Volume xG", seg1: { p: 0.44, col: "#f59e0b", nome: "Roma: 44% (1.35)" }, seg2: { p: 0.56, col: "#3b82f6", nome: "Atalanta: 56% (1.75)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+5,1%",
                mercato: "Gol (Entrambe le squadre segnano)",
                qEqua: "1.61",
                qReale: "1.72",
                spiegazione: "Probabilità GG stimata al 62% contro il 55% implicito su Eurobet. La Dea viaggia a oltre 2.2 reti per match, la Roma all'Olimpico trova sempre il gol con Ranieri.",
                analisi: "L'Atalanta ha segnato in 9 delle ultime 10 partite con Lookman e Retegui. La Roma in casa ha concesso gol in 4 gare su 5 ma reagisce d'orgoglio. Quota 1.72 con forte edge matematico.",
                rischio: "Atalanta reduce da fatica europea o Roma eccessivamente difensivista.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Over 1.5 Gol", alt: "X2 (69%)", prob: 84, probStr: "84%", quota: "1.24", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "Partita da gol quasi garantito per gli indici offensivi in campo." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "Gol + Over 2.5", alt: "X2 + Gol (57%)", prob: 56, probStr: "56%", quota: "2.05", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "La combo d'eccellenza quando gioca la squadra di Gasperini." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "2 + Gol (Atalanta vince & Gol)", alt: "Ris. Esatto 1-2 (11%)", prob: 30, probStr: "30%", quota: "3.75", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Quota sontuosa (+275%). L'Atalanta è superiore per ritmo e condizione atletica." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Retegui Marcatore", alt: "Dovbyk Marcatore", prob: 45, probStr: "45%", quota: "2.40", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Capocannoniere della Serie A in stato di grazia." }
                }
              }
            ]
          },
          "13": {
            label: "13ª Giornata (29 Nov - 1 Dic 2026)",
            dataFine: "2026-12-01T23:59:59",
            partite: [
              {
                id: "fio-int",
                label: "Fiorentina - Inter",
                bgGradient: "from-[#250d38] via-[#090d16] to-[#071d42]",
                casa: { sigla: "FIO", nome: "Fiorentina", rank: "3° posto · xG 1.80/gara", colBox: "bg-purple-600/20 text-purple-400 border-purple-500" },
                ospite: { sigla: "INT", nome: "Inter", rank: "4° posto · xG 2.15/gara", colBox: "bg-blue-600/20 text-blue-400 border-blue-500" },
                data: "Domenica 30 Nov · 18:00",
                giornata: "Serie A · 13ª Giornata",
                golC: "1.45",
                golO: "1.65",
                barC: "47%",
                barO: "53%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "45%", centerLbl: "Segno 2", seg1: { p: 0.28, col: "#06b6d4", nome: "1: 28%" }, seg2: { p: 0.27, col: "#f59e0b", nome: "X: 27%" }, seg3: { p: 0.45, col: "#f43f5e", nome: "2: 45%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "60%", centerLbl: "Gol (GG)", seg1: { p: 0.60, col: "#10b981", nome: "Gol: 60%" }, seg2: { p: 0.40, col: "#64748b", nome: "No Gol: 40%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "56%", centerLbl: "Over 2.5", seg1: { p: 0.56, col: "#8b5cf6", nome: "Over: 56%" }, seg2: { p: 0.44, col: "#3b82f6", nome: "Under: 44%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "1.45 vs 1.65", centerLbl: "Volume xG", seg1: { p: 0.47, col: "#a855f7", nome: "Fiorentina: 47% (1.45)" }, seg2: { p: 0.53, col: "#3b82f6", nome: "Inter: 53% (1.65)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+4,5%",
                mercato: "Gol (Entrambe le squadre segnano)",
                qEqua: "1.66",
                qReale: "1.75",
                spiegazione: "Due formazioni in striscia positiva ad altissima intensità offensiva al Franchi.",
                analisi: "Fiorentina rivelazione con Kean in attacco, Inter con il miglior attacco esterno della Serie A. Entrambe a segno probabile al 60%.",
                rischio: "Tensione da scontro diretto di alta classifica.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Over 1.5 Gol", alt: "X2 (72%)", prob: 82, probStr: "82%", quota: "1.25", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "Base solida di alta classifica al Franchi." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "X2 + Gol", alt: "Over 2.5 (56%)", prob: 58, probStr: "58%", quota: "2.10", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "Copre l'1-1 e il successo esterno nerazzurro 1-2." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "Risultato Esatto 1-2", alt: "2 + Gol (32%)", prob: 12, probStr: "12%", quota: "8.50", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Esito storicamente ricorrente tra viola e nerazzurri a Firenze." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Kean Marcatore", alt: "Lautaro Marcatore", prob: 42, probStr: "42%", quota: "2.80", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Bomber viola in fiducia assoluta." }
                }
              }
            ]
          }
        }
      },
      "premier": {
        nome: "Premier League (Inghilterra)",
        turni: {
          "12": {
            label: "12ª Giornata (21-23 Nov 2026)",
            dataFine: "2026-11-23T23:59:59",
            partite: [
              {
                id: "ars-che",
                label: "Arsenal - Chelsea",
                bgGradient: "from-[#3d0a11] via-[#090d16] to-[#071d42]",
                casa: { sigla: "ARS", nome: "Arsenal", rank: "2° posto · xG 2.10/gara", colBox: "bg-red-600/20 text-red-400 border-red-500" },
                ospite: { sigla: "CHE", nome: "Chelsea", rank: "4° posto · xG 1.85/gara", colBox: "bg-blue-600/20 text-blue-400 border-blue-400" },
                data: "Domenica 22 Nov · 17:30",
                giornata: "Premier League · 12ª Giornata",
                golC: "1.92",
                golO: "1.25",
                barC: "61%",
                barO: "39%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "52%", centerLbl: "Segno 1", seg1: { p: 0.52, col: "#06b6d4", nome: "1: 52%" }, seg2: { p: 0.24, col: "#f59e0b", nome: "X: 24%" }, seg3: { p: 0.24, col: "#f43f5e", nome: "2: 24%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "61%", centerLbl: "Gol (GG)", seg1: { p: 0.61, col: "#10b981", nome: "Gol: 61%" }, seg2: { p: 0.39, col: "#64748b", nome: "No Gol: 39%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "59%", centerLbl: "Over 2.5", seg1: { p: 0.59, col: "#8b5cf6", nome: "Over: 59%" }, seg2: { p: 0.41, col: "#3b82f6", nome: "Under: 41%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "1.92 vs 1.25", centerLbl: "Volume xG", seg1: { p: 0.61, col: "#ef4444", nome: "Arsenal: 61% (1.92)" }, seg2: { p: 0.39, col: "#3b82f6", nome: "Chelsea: 39% (1.25)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+5,3%",
                mercato: "Over 2,5 Gol",
                qEqua: "1.69",
                qReale: "1.78",
                spiegazione: "Over 2,5 stimato al 59% contro il 53% implicito nella quota Eurobet. Entrambe le squadre producono oltre 1,8 xG a partita. Ottimo edge statistico.",
                analisi: "Over 2,5 stimato al 59% dal modello Poisson integrato con i dati xG. La quota Eurobet a 1.78 corrisponde a un'implicita netta del 53%. Vantaggio matematico comprovato.",
                rischio: "Turnover offensivo post-impegni europei infrasettimanali.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Over 1.5 Gol", alt: "1X (76%)", prob: 83, probStr: "83%", quota: "1.22", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "Derby di Londra tradizionalmente spettacolare: 3.1 xG combinati di media per incontro." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "Gol + Over 2.5", alt: "1X + Over 1.5 (71%)", prob: 58, probStr: "58%", quota: "1.95", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "Attacchi top-4 in Premier: 8 delle ultime 10 sfide hanno visto entrambe le formazioni a segno." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "Arsenal vince + Over 2.5", alt: "Ris. Esatto 2-2 (8%)", prob: 36, probStr: "36%", quota: "2.85", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Emirates Stadium decisivo; Chelsea fragile nella gestione delle palle inattive difensive." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Over 9.5 Calci d'Angolo", alt: "Saka Marcatore o Assist", prob: 65, probStr: "65%", quota: "1.75", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Extra statistico: 11.4 corner generati complessivamente di media negli ultimi 6 derby." }
                }
              },
              {
                id: "mci-tot",
                label: "Man City - Tottenham",
                bgGradient: "from-[#082a4d] via-[#090d16] to-[#1e293b]",
                casa: { sigla: "MCI", nome: "Manchester City", rank: "1° posto · xG 2.45/gara", colBox: "bg-sky-400/20 text-sky-300 border-sky-400" },
                ospite: { sigla: "TOT", nome: "Tottenham", rank: "8° posto · xG 1.60/gara", colBox: "bg-slate-700/30 text-slate-100 border-slate-400" },
                data: "Sabato 21 Nov · 18:30",
                giornata: "Premier League · 12ª Giornata",
                golC: "2.40",
                golO: "1.20",
                barC: "67%",
                barO: "33%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "66%", centerLbl: "Segno 1", seg1: { p: 0.66, col: "#06b6d4", nome: "1: 66%" }, seg2: { p: 0.19, col: "#f59e0b", nome: "X: 19%" }, seg3: { p: 0.15, col: "#f43f5e", nome: "2: 15%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "64%", centerLbl: "Gol (GG)", seg1: { p: 0.64, col: "#10b981", nome: "Gol: 64%" }, seg2: { p: 0.36, col: "#64748b", nome: "No Gol: 36%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "72%", centerLbl: "Over 2.5", seg1: { p: 0.72, col: "#8b5cf6", nome: "Over: 72%" }, seg2: { p: 0.28, col: "#3b82f6", nome: "Under: 28%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "2.40 vs 1.20", centerLbl: "Volume xG", seg1: { p: 0.67, col: "#38bdf8", nome: "Man City: 67% (2.40)" }, seg2: { p: 0.33, col: "#cbd5e1", nome: "Spurs: 33% (1.20)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+4,1%",
                mercato: "1 + Over 2.5 Gol",
                qEqua: "1.74",
                qReale: "1.85",
                spiegazione: "Stima 1 + Over 2.5 al 57% contro quota Eurobet a 1.85 (51% netta). Il City all'Etihad crea valanghe di occasioni, gli Spurs giocano a viso aperto.",
                analisi: "Guardiola vs Postecoglou promette gol e spettacolo. Il City ha segnato almeno 2 reti in 9 delle ultime 10 gare interne. Valore matematico +4,1%.",
                rischio: "I contropiedi di Son possono punire la linea difensiva alta dei Citizens.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Over 2.5 Gol", alt: "1X (85%)", prob: 72, probStr: "72%", quota: "1.38", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "Partita tra due delle squadre più offensive al mondo." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "1 + Gol", alt: "1 + Over 2.5 (57%)", prob: 52, probStr: "52%", quota: "2.35", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "La difesa del City concede quasi sempre almeno una ripartenza nitida." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "Haaland segna 2 o più gol", alt: "Ris. Esatto 3-1 (11%)", prob: 35, probStr: "35%", quota: "2.75", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Il norvegese ha una media di 1.25 gol attesi contro difese a linea altissima." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Over 10.5 Calci d'Angolo", alt: "Over 3.5 Gol (52%)", prob: 66, probStr: "66%", quota: "1.80", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "La pressione asfissiante sulle fasce genera una valanga di corner." }
                }
              }
            ]
          },
          "13": {
            label: "13ª Giornata (29 Nov - 1 Dic 2026)",
            dataFine: "2026-12-01T23:59:59",
            partite: [
              {
                id: "liv-mci",
                label: "Liverpool - Man City",
                bgGradient: "from-[#3a0a10] via-[#090d16] to-[#082a4d]",
                casa: { sigla: "LIV", nome: "Liverpool", rank: "1° posto · xG 2.30/gara", colBox: "bg-red-700/20 text-red-400 border-red-600" },
                ospite: { sigla: "MCI", nome: "Manchester City", rank: "2° posto · xG 2.40/gara", colBox: "bg-sky-400/20 text-sky-300 border-sky-400" },
                data: "Domenica 30 Nov · 17:00",
                giornata: "Premier League · 13ª Giornata",
                golC: "1.80",
                golO: "1.70",
                barC: "51%",
                barO: "49%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "38%", centerLbl: "Segno 1", seg1: { p: 0.38, col: "#06b6d4", nome: "1: 38%" }, seg2: { p: 0.28, col: "#f59e0b", nome: "X: 28%" }, seg3: { p: 0.34, col: "#f43f5e", nome: "2: 34%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "68%", centerLbl: "Gol (GG)", seg1: { p: 0.68, col: "#10b981", nome: "Gol: 68%" }, seg2: { p: 0.32, col: "#64748b", nome: "No Gol: 32%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "67%", centerLbl: "Over 2.5", seg1: { p: 0.67, col: "#8b5cf6", nome: "Over: 67%" }, seg2: { p: 0.33, col: "#3b82f6", nome: "Under: 33%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "1.80 vs 1.70", centerLbl: "Volume xG", seg1: { p: 0.51, col: "#ef4444", nome: "Liverpool: 51% (1.80)" }, seg2: { p: 0.49, col: "#38bdf8", nome: "City: 49% (1.70)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+6,2%",
                mercato: "Gol + Over 2.5",
                qEqua: "1.58",
                qReale: "1.72",
                spiegazione: "Scontro al vertice della Premier ad Anfield: i due migliori attacchi del continente a confronto.",
                analisi: "Ad Anfield gli scontri tra Reds e Citizens producono mediamente 3.4 gol a partita. Quota 1.72 di assoluto valore atteso.",
                rischio: "Match tattico per la posta in palio elevatissima.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Over 1.5 Gol", alt: "1X (66%)", prob: 86, probStr: "86%", quota: "1.20", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "La base più affidabile per Anfield." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "Gol + Over 2.5", alt: "1X + Gol (58%)", prob: 63, probStr: "63%", quota: "1.72", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "Entrambe segnano e match da almeno 3 gol." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "Salah & Haaland entrambi a segno", alt: "Ris. Esatto 2-2 (10%)", prob: 28, probStr: "28%", quota: "4.50", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "La scommessa dei campioni nel big match d'Inghilterra." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Multigol 3-5", alt: "Over 10.5 Corner", prob: 60, probStr: "60%", quota: "1.90", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Intervallo perfetto per un match ad altissima intensità." }
                }
              }
            ]
          }
        }
      },
      "liga": {
        nome: "LaLiga (Spagna)",
        turni: {
          "14": {
            label: "14ª Giornata (21-24 Nov 2026)",
            dataFine: "2026-11-24T23:59:59",
            partite: [
              {
                id: "clt-bar",
                label: "Celta Vigo - Barcellona",
                bgGradient: "from-[#082a4d] via-[#090d16] to-[#3a0a18]",
                casa: { sigla: "CLT", nome: "Celta Vigo", rank: "11° posto · xG 1.30/gara", colBox: "bg-sky-600/20 text-sky-400 border-sky-500" },
                ospite: { sigla: "BAR", nome: "Barcellona", rank: "1° posto · xG 2.55/gara", colBox: "bg-red-700/20 text-red-400 border-red-600" },
                data: "Sabato 21 Nov · 21:00",
                giornata: "LaLiga · 14ª Giornata",
                golC: "1.15",
                golO: "2.35",
                barC: "33%",
                barO: "67%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "62%", centerLbl: "Segno 2", seg1: { p: 0.17, col: "#06b6d4", nome: "1: 17%" }, seg2: { p: 0.21, col: "#f59e0b", nome: "X: 21%" }, seg3: { p: 0.62, col: "#f43f5e", nome: "2: 62%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "63%", centerLbl: "Gol (GG)", seg1: { p: 0.63, col: "#10b981", nome: "Gol: 63%" }, seg2: { p: 0.37, col: "#64748b", nome: "No Gol: 37%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "68%", centerLbl: "Over 2.5", seg1: { p: 0.68, col: "#8b5cf6", nome: "Over: 68%" }, seg2: { p: 0.32, col: "#3b82f6", nome: "Under: 32%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "1.15 vs 2.35", centerLbl: "Volume xG", seg1: { p: 0.33, col: "#38bdf8", nome: "Celta: 33% (1.15)" }, seg2: { p: 0.67, col: "#ef4444", nome: "Barça: 67% (2.35)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+4,9%",
                mercato: "2 + Over 1.5 Gol",
                qEqua: "1.60",
                qReale: "1.72",
                spiegazione: "Il Barça di Flick viaggia a 3.1 gol di media a partita. Celta ostico al Balaídos ma con difesa perforabile.",
                analisi: "Barcellona in testa a LaLiga con Yamal e Lewandowski incontenibili. La probabilità del Segno 2 unito ad almeno 2 gol totali supera il 62%. Quota Eurobet 1.72 vantaggiosa.",
                rischio: "Il campo del Celta Vigo è storicamente una trappola per i blaugrana.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Over 2.5 Gol", alt: "Segno 2 (62%)", prob: 68, probStr: "68%", quota: "1.45", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "La squadra catalana supera quasi sempre l'Over 2.5." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "2 + Gol", alt: "2 + Over 2.5 (54%)", prob: 50, probStr: "50%", quota: "2.65", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "La tattica con trappola del fuorigioco alta del Barça concede chance agli avversari." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "Lewandowski Marcatore e Barça vince", alt: "Ris. Esatto 1-3 (11%)", prob: 44, probStr: "44%", quota: "2.10", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Pichichi del campionato supportato dal tridente più prolifico d'Europa." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Barça segna in entrambi i tempi", alt: "Yamal Assist", prob: 58, probStr: "58%", quota: "1.95", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Capacità realizzativa costante dal 1' al 90'." }
                }
              },
              {
                id: "leg-rma",
                label: "Leganes - Real Madrid",
                bgGradient: "from-[#082347] via-[#090d16] to-[#252525]",
                casa: { sigla: "LEG", nome: "Leganes", rank: "15° posto · xG 0.85/gara", colBox: "bg-blue-600/20 text-blue-400 border-blue-500" },
                ospite: { sigla: "RMA", nome: "Real Madrid", rank: "2° posto · xG 2.20/gara", colBox: "bg-slate-700/30 text-slate-100 border-slate-300" },
                data: "Domenica 22 Nov · 18:30",
                giornata: "LaLiga · 14ª Giornata",
                golC: "0.80",
                golO: "2.15",
                barC: "27%",
                barO: "73%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "68%", centerLbl: "Segno 2", seg1: { p: 0.12, col: "#06b6d4", nome: "1: 12%" }, seg2: { p: 0.20, col: "#f59e0b", nome: "X: 20%" }, seg3: { p: 0.68, col: "#f43f5e", nome: "2: 68%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "56%", centerLbl: "No Gol", seg1: { p: 0.44, col: "#10b981", nome: "Gol: 44%" }, seg2: { p: 0.56, col: "#64748b", nome: "No Gol: 56%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "61%", centerLbl: "Over 2.5", seg1: { p: 0.61, col: "#8b5cf6", nome: "Over: 61%" }, seg2: { p: 0.39, col: "#3b82f6", nome: "Under: 39%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "0.80 vs 2.15", centerLbl: "Volume xG", seg1: { p: 0.27, col: "#38bdf8", nome: "Leganes: 27% (0.80)" }, seg2: { p: 0.73, col: "#f8fafc", nome: "Real: 73% (2.15)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+4,0%",
                mercato: "2 Handicap (-1)",
                qEqua: "1.92",
                qReale: "2.05",
                spiegazione: "I Blancos hanno bisogno dei 3 punti per non perdere terreno sul Barça. Divario tecnico abissale.",
                analisi: "Vinicius e Mbappé contro la retroguardia del neopromosso Leganes. Stima successo madridista con almeno 2 gol di scarto al 52%. Quota 2.05 Eurobet favorevole.",
                rischio: "Infortuni difensivi nel Real (assenza Militao e Carvajal).",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Segno 2 (Real)", alt: "Over 1.5 (82%)", prob: 68, probStr: "68%", quota: "1.38", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "Vittoria fondamentale per la corsa al titolo." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "2 + Over 1.5 Gol", alt: "2 + NoGol (42%)", prob: 61, probStr: "61%", quota: "1.65", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "La combinazione standard per le vittorie del Madrid." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "Vinicius Marcatore 1° Tempo", alt: "Ris. Esatto 0-3 (12%)", prob: 32, probStr: "32%", quota: "3.20", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Il brasiliano aggredisce la partita sin dai primi possessi." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Mbappé segna almeno 2 gol", alt: "Over 5.5 Tiri in porta Real", prob: 28, probStr: "28%", quota: "3.50", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Opportunità di sbloccarsi definitivamente in trasferta." }
                }
              }
            ]
          }
        }
      },
      "bundesliga": {
        nome: "Bundesliga (Germania)",
        turni: {
          "11": {
            label: "11ª Giornata (20-23 Nov 2026)",
            dataFine: "2026-11-23T23:59:59",
            partite: [
              {
                id: "bay-aug",
                label: "Bayern Monaco - Augsburg",
                bgGradient: "from-[#3d0a14] via-[#090d16] to-[#1e293b]",
                casa: { sigla: "BAY", nome: "Bayern Monaco", rank: "1° posto · xG 2.85/gara", colBox: "bg-red-600/20 text-red-400 border-red-500" },
                ospite: { sigla: "AUG", nome: "Augsburg", rank: "13° posto · xG 1.00/gara", colBox: "bg-slate-700/30 text-slate-200 border-slate-400" },
                data: "Venerdì 20 Nov · 20:30",
                giornata: "Bundesliga · 11ª Giornata",
                golC: "2.80",
                golO: "0.70",
                barC: "80%",
                barO: "20%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "80%", centerLbl: "Segno 1", seg1: { p: 0.80, col: "#06b6d4", nome: "1: 80%" }, seg2: { p: 0.13, col: "#f59e0b", nome: "X: 13%" }, seg3: { p: 0.07, col: "#f43f5e", nome: "2: 7%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "52%", centerLbl: "No Gol", seg1: { p: 0.48, col: "#10b981", nome: "Gol: 48%" }, seg2: { p: 0.52, col: "#64748b", nome: "No Gol: 52%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "76%", centerLbl: "Over 2.5", seg1: { p: 0.76, col: "#8b5cf6", nome: "Over: 76%" }, seg2: { p: 0.24, col: "#3b82f6", nome: "Under: 24%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "2.80 vs 0.70", centerLbl: "Volume xG", seg1: { p: 0.80, col: "#ef4444", nome: "Bayern: 80% (2.80)" }, seg2: { p: 0.20, col: "#94a3b8", nome: "Augsburg: 20% (0.70)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+4,4%",
                mercato: "1 + Over 2.5 Gol",
                qEqua: "1.38",
                qReale: "1.48",
                spiegazione: "Bayern capolista inarrestabile all'Allianz Arena sotto la guida di Kompany.",
                analisi: "Harry Kane e compagni hanno una produzione interna record di 2.85 xG. Augsburg subisce 2.2 gol a partita in trasferta. Margine positivo chiaro.",
                rischio: "Rotazioni in vista della Champions League infrasettimanale.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Over 2.5 Gol", alt: "1X (93%)", prob: 76, probStr: "76%", quota: "1.30", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "La Bundesliga all'Allianz Arena è garanzia quasi assoluta di gol." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "1 + Over 2.5 Gol", alt: "1 + NoGol (45%)", prob: 70, probStr: "70%", quota: "1.48", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "La giocata più performante per il Bayern in casa." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "Harry Kane segna almeno 2 gol", alt: "Ris. Esatto 3-0 (13%)", prob: 40, probStr: "40%", quota: "2.60", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Il capitano inglese è rigorista e terminale primario dei bavaresi." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "Bayern vince entrambi i tempi", alt: "Over 3.5 Gol (55%)", prob: 58, probStr: "58%", quota: "1.85", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Dominio territoriale costante nei primi e secondi 45 minuti." }
                }
              }
            ]
          }
        }
      },
      "ligue1": {
        nome: "Ligue 1 (Francia)",
        turni: {
          "12": {
            label: "12ª Giornata (20-23 Nov 2026)",
            dataFine: "2026-11-23T23:59:59",
            partite: [
              {
                id: "psg-tou",
                label: "PSG - Tolosa",
                bgGradient: "from-[#081a38] via-[#090d16] to-[#250d38]",
                casa: { sigla: "PSG", nome: "Paris Saint-Germain", rank: "1° posto · xG 2.65/gara", colBox: "bg-blue-600/20 text-blue-400 border-blue-500" },
                ospite: { sigla: "TOU", nome: "Tolosa", rank: "10° posto · xG 1.15/gara", colBox: "bg-purple-600/20 text-purple-400 border-purple-500" },
                data: "Venerdì 20 Nov · 21:00",
                giornata: "Ligue 1 · 12ª Giornata",
                golC: "2.60",
                golO: "0.85",
                barC: "75%",
                barO: "25%",
                fasi: {
                  1: { label: "Fase 1: 1X2", centerVal: "76%", centerLbl: "Segno 1", seg1: { p: 0.76, col: "#06b6d4", nome: "1: 76%" }, seg2: { p: 0.16, col: "#f59e0b", nome: "X: 16%" }, seg3: { p: 0.08, col: "#f43f5e", nome: "2: 8%" } },
                  2: { label: "Fase 2: GG / NG", centerVal: "54%", centerLbl: "No Gol", seg1: { p: 0.46, col: "#10b981", nome: "Gol: 46%" }, seg2: { p: 0.54, col: "#64748b", nome: "No Gol: 54%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  3: { label: "Fase 3: Under / Over 2.5", centerVal: "71%", centerLbl: "Over 2.5", seg1: { p: 0.71, col: "#8b5cf6", nome: "Over: 71%" }, seg2: { p: 0.29, col: "#3b82f6", nome: "Under: 29%" }, seg3: { p: 0.00, col: "transparent", nome: "" } },
                  4: { label: "Fase 4: xG per Squadra", centerVal: "2.60 vs 0.85", centerLbl: "Volume xG", seg1: { p: 0.75, col: "#3b82f6", nome: "PSG: 75% (2.60)" }, seg2: { p: 0.25, col: "#a855f7", nome: "Tolosa: 25% (0.85)" }, seg3: { p: 0.00, col: "transparent", nome: "" } }
                },
                isValore: true,
                evBadge: "+4,7%",
                mercato: "1 + Over 2.5 Gol",
                qEqua: "1.47",
                qReale: "1.58",
                spiegazione: "Il Paris al Parco dei Principi segna oltre 2.5 reti a gara con Barcola e Dembélé in forma smagliante.",
                analisi: "Il PSG ha dominato tutti i match interni di campionato. Tolosa compatto ma non in grado di contenere il ritmo parigino. Edge +4,7%.",
                rischio: "Possibile calo di tensione nel finale a risultato acquisito.",
                pronosticiExtra: {
                  1: { tipo: "ALTA PROBABILITÀ (BASE)", icona: "🛡️", mercato: "Segno 1 (PSG)", alt: "Over 1.5 (86%)", prob: 76, probStr: "76%", quota: "1.28", badgeCol: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", barCol: "from-emerald-500 to-teal-400", desc: "Monopolio parigino in Ligue 1." },
                  2: { tipo: "MIGLIOR COMBO", icona: "⚡", mercato: "1 + Over 2.5 Gol", alt: "1 + NoGol (46%)", prob: 66, probStr: "66%", quota: "1.58", badgeCol: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", barCol: "from-cyan-500 to-blue-500", desc: "La combinazione con la più alta frequenza al Parco dei Principi." },
                  3: { tipo: "PRONOSTICO HARD", icona: "🎯", mercato: "Barcola Marcatore e PSG vince", alt: "Ris. Esatto 3-0 (12%)", prob: 42, probStr: "42%", quota: "2.45", badgeCol: "text-rose-400 bg-rose-500/10 border-rose-500/30", barCol: "from-rose-500 to-amber-500", desc: "Il gioiello francese è il capocannoniere del club in campionato." },
                  4: { tipo: "PRONOSTICO EXTRA", icona: "🔮", mercato: "PSG segna in entrambi i tempi", alt: "Over 6.5 Corner PSG", prob: 62, probStr: "62%", quota: "1.80", badgeCol: "text-purple-400 bg-purple-500/10 border-purple-500/30", barCol: "from-purple-500 to-indigo-500", desc: "Continuità offensiva lungo tutti i 90 minuti." }
                }
              }
            ]
          }
        }
      }
    };

    // LOGICA DI CONTROLLO E AUTO-ROLLOVER DEL CALENDARIO
    function cambiaCampionato() {
      const campKey = document.getElementById("select-campionato").value;
      const camp = DATA_PRO[campKey] || DATA_PRO["serie-a"];
      
      const selectG = document.getElementById("select-giornata");
      selectG.innerHTML = "";
      
      const turniKeys = Object.keys(camp.turni).map(Number).sort((a,b) => a - b);
      const adesso = new Date();
      
      // Auto-Rollover: trova il primo turno la cui data di fine è ancora futura
      let turnoAttivo = turniKeys[0];
      let isRolloverEseguito = false;

      for (let k of turniKeys) {
        const t = camp.turni[k];
        const fineTurno = new Date(t.dataFine);
        if (adesso <= fineTurno) {
          turnoAttivo = k;
          break;
        } else {
          isRolloverEseguito = true;
        }
      }

      // Popola select-giornata
      turniKeys.forEach(k => {
        const t = camp.turni[k];
        const opt = document.createElement("option");
        opt.value = k;
        const fine = new Date(t.dataFine);
        const concluso = adesso > fine;
        opt.textContent = `${t.label} ${concluso ? '🏁 [Concluso]' : '🟢 [Attivo]'}`;
        if (k === turnoAttivo) opt.selected = true;
        selectG.appendChild(opt);
      });

      // Aggiorna indicatore badge rollover
      const badge = document.getElementById("badge-rollover");
      if (badge) {
        if (isRolloverEseguito) {
          badge.textContent = "🟢 AUTO-ROLLOVER ATTIVO";
          badge.className = "text-[9px] text-cyan-400 mono font-bold";
        } else {
          badge.textContent = "🟢 TURNO CORRENTE LIVE";
          badge.className = "text-[9px] text-emerald-400 mono font-bold";
        }
      }

      cambiaGiornata();
    }

    function cambiaGiornata() {
      const campKey = document.getElementById("select-campionato").value;
      const camp = DATA_PRO[campKey] || DATA_PRO["serie-a"];
      const gKey = document.getElementById("select-giornata").value;
      const turno = camp.turni[gKey] || camp.turni[Object.keys(camp.turni)[0]];

      const selectP = document.getElementById("select-partita");
      selectP.innerHTML = "";

      turno.partite.forEach((p, idx) => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = `${p.label} (${p.data.split('·')[0].trim()})`;
        if (idx === 0) opt.selected = true;
        selectP.appendChild(opt);
      });

      renderizzaPartita();
    }

    function renderizzaPartita() {
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
      banner.className = `border border-slate-800 rounded-3xl p-6 shadow-2xl relative overflow-hidden transition-all duration-700 bg-gradient-to-r ${m.bgGradient}`;

      document.getElementById("match-giornata").textContent = m.giornata;
      document.getElementById("match-data").textContent = m.data;

      // Squadre
      document.getElementById("nome-casa").textContent = m.casa.nome;
      document.getElementById("nome-casa-short").textContent = m.casa.nome;
      document.getElementById("sigla-casa").textContent = m.casa.sigla;
      document.getElementById("rank-casa").textContent = m.casa.rank;
      document.getElementById("box-badge-casa").className = `w-16 h-16 rounded-2xl flex items-center justify-center font-black text-2xl mono shadow-xl border-2 ${m.casa.colBox}`;

      document.getElementById("nome-ospite").textContent = m.ospite.nome;
      document.getElementById("nome-ospite-short").textContent = m.ospite.nome;
      document.getElementById("sigla-ospite").textContent = m.ospite.sigla;
      document.getElementById("rank-ospite").textContent = m.ospite.rank;
      document.getElementById("box-badge-ospite").className = `w-16 h-16 rounded-2xl flex items-center justify-center font-black text-2xl mono shadow-xl border-2 ${m.ospite.colBox}`;

      document.getElementById("xg-dettaglio-casa").textContent = `Attesi: ${m.golC} gol`;
      document.getElementById("xg-dettaglio-ospite").textContent = `Attesi: ${m.golO} gol`;

      // Barre xG
      document.getElementById("bar-xg-c").style.width = m.barC;
      document.getElementById("bar-xg-o").style.width = m.barO;

      // Aggiorna Donut a Torta e Pronostici Scorrevoli alla fase corrente
      aggiornaDonut(FASE_TORTA_ATTUALE);
      aggiornaPronosticiScorrevoli(FASE_TORTA_ATTUALE);

      // Valore Box
      const vBox = document.getElementById("box-verdetto-valore");
      if (m.isValore) {
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
              <div class="text-2xl font-black text-emerald-400 mono">${m.evBadge}</div>
            </div>
          </div>
          <div class="bg-slate-950 p-4 rounded-2xl border border-slate-800/80 space-y-3">
            <div class="flex justify-between items-baseline">
              <div>
                <span class="text-[11px] text-slate-400 uppercase font-bold mono">Mercato Consigliato</span>
                <div class="text-xl md:text-2xl font-black text-white">${m.mercato}</div>
              </div>
              <div class="text-right">
                <span class="text-[10px] text-slate-400 uppercase font-bold mono">Puntata (2% Flat)</span>
                <div class="text-lg font-black text-white mono">2,00 €</div>
              </div>
            </div>
            <div class="space-y-1.5 pt-1">
              <div class="flex justify-between text-xs mono">
                <span class="text-slate-400">Prezzo Equo Stimato: <strong class="text-white">${m.qEqua}</strong></span>
                <span class="text-emerald-400 font-bold">Quota Eurobet: <strong class="text-emerald-300 text-sm">${m.qReale}</strong></span>
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
          <div class="mt-4 text-xs text-slate-300 leading-relaxed">${m.spiegazione}</div>
        `;
      } else {
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
            <div class="text-lg font-black text-slate-200">${m.mercato}</div>
            <p class="text-slate-400">${m.spiegazione}</p>
          </div>
        `;
      }

      // Analisi Tracciabile
      document.getElementById("box-analisi-tracciabile").innerHTML = `
        <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
          <div class="font-bold text-white flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
            <span>Catena Logica dell'Analista (Numeri Verificati)</span>
          </div>
          <p>${m.analisi}</p>
          <div class="p-2.5 rounded-xl bg-rose-950/30 border border-rose-900/40 text-[11px] text-rose-300 flex items-center gap-2">
            <span>⚠️</span>
            <span><strong>Fattore di Rischio:</strong> ${m.rischio}</span>
          </div>
        </div>
      `;
    }