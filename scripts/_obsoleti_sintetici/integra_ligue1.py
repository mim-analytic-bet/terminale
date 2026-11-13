import json
import math
import os
import re

def poisson(k, l):
    p = math.exp(-l)
    for i in range(1, k + 1):
        p *= l / i
    return p

def calc_stats(lambda_c, mu_o):
    p_c = 0.0
    p_x = 0.0
    p_o = 0.0
    p_over = 0.0
    p_under = 0.0
    p_gg = 0.0
    p_ng = 0.0
    
    for i in range(10):
        for j in range(10):
            p = poisson(i, lambda_c) * poisson(j, mu_o)
            if i > j: p_c += p
            elif i == j: p_x += p
            else: p_o += p
            
            if (i + j) > 2.5: p_over += p
            else: p_under += p
            
            if i > 0 and j > 0: p_gg += p
            else: p_ng += p
            
    tot_1x2 = p_c + p_x + p_o
    p_c /= tot_1x2
    p_x /= tot_1x2
    p_o /= tot_1x2
    
    p1 = round(p_c, 2)
    px = round(p_x, 2)
    p2 = round(p_o, 2)
    diff = round(1.0 - (p1 + px + p2), 2)
    p1 = round(p1 + diff, 2)

    p_over = round(p_over, 2)
    p_under = round(1.0 - p_over, 2)

    p_gg = round(p_gg, 2)
    p_ng = round(1.0 - p_gg, 2)

    return {
        'p1': p1, 'px': px, 'p2': p2,
        'p_over': p_over, 'p_under': p_under,
        'p_gg': p_gg, 'p_ng': p_ng,
        'q1': round(1 / max(0.05, p1), 2),
        'qx': round(1 / max(0.05, px), 2),
        'q2': round(1 / max(0.05, p2), 2),
        'q_over': round(1 / max(0.05, p_over), 2),
        'q_under': round(1 / max(0.05, p_under), 2),
        'q_gg': round(1 / max(0.05, p_gg), 2),
        'q_ng': round(1 / max(0.05, p_ng), 2),
    }

def make_match(mid, c_name, c_sigla, o_name, o_sigla, data_str, l_c, m_o, c_col, o_col, bg_grad, market_type="1", is_val=False, val_book_q=1.90, edge_val=5.2, spiegaz="", analisi_str="", rischio_str=""):
    st = calc_stats(l_c, m_o)
    
    tot_xg = l_c + m_o
    c_perc = round((l_c / tot_xg) * 100)
    o_perc = 100 - c_perc

    bar_c = f"{min(95, max(10, int((l_c / 3.0) * 100)))}%"
    bar_o = f"{min(95, max(10, int((m_o / 3.0) * 100)))}%"

    fasi = {
        "1": {
            "centerVal": f"{int(st['p1']*100)}%",
            "centerLbl": "Segno 1",
            "seg1": {"nome": f"1: {int(st['p1']*100)}%", "p": st['p1'], "col": "#06b6d4"},
            "seg2": {"nome": f"X: {int(st['px']*100)}%", "p": st['px'], "col": "#f59e0b"},
            "seg3": {"nome": f"2: {int(st['p2']*100)}%", "p": st['p2'], "col": "#f43f5e"}
        },
        "2": {
            "centerVal": f"{int(st['p_gg']*100)}%",
            "centerLbl": "Entrambe (GG)",
            "seg1": {"nome": f"Gol: {int(st['p_gg']*100)}%", "p": st['p_gg'], "col": "#10b981"},
            "seg2": {"nome": f"No Gol: {int(st['p_ng']*100)}%", "p": st['p_ng'], "col": "#64748b"},
            "seg3": {"nome": "", "p": 0, "col": "transparent"}
        },
        "3": {
            "centerVal": f"{int(st['p_over']*100)}%",
            "centerLbl": "Over 2.5",
            "seg1": {"nome": f"Under: {int(st['p_under']*100)}%", "p": st['p_under'], "col": "#3b82f6"},
            "seg2": {"nome": f"Over: {int(st['p_over']*100)}%", "p": st['p_over'], "col": "#ec4899"},
            "seg3": {"nome": "", "p": 0, "col": "transparent"}
        },
        "4": {
            "centerVal": f"{c_perc}%",
            "centerLbl": f"xG {c_name}",
            "seg1": {"nome": f"{c_name}: {c_perc}% ({l_c})", "p": round(c_perc/100, 2), "col": "#06b6d4"},
            "seg2": {"nome": f"{o_name}: {o_perc}% ({m_o})", "p": round(o_perc/100, 2), "col": "#f59e0b"},
            "seg3": {"nome": "", "p": 0, "col": "transparent"}
        }
    }

    if market_type == "1":
        rec_mkt = f"Vittoria {c_name} (Segno 1)"
        q_rec = st['q1']
    elif market_type == "2":
        rec_mkt = f"Vittoria {o_name} (Segno 2)"
        q_rec = st['q2']
    elif market_type == "OVER":
        rec_mkt = "Over 2,5 Gol"
        q_rec = st['q_over']
    elif market_type == "GG":
        rec_mkt = "Entrambe Segnano (Gol)"
        q_rec = st['q_gg']
    elif market_type == "1X":
        rec_mkt = f"Doppia Chance 1X ({c_name})"
        q_rec = round(1 / max(0.4, (st['p1'] + st['px'])), 2)
    else:
        rec_mkt = f"Vittoria {c_name} (Segno 1)"
        q_rec = st['q1']

    p_base_prob = int(max(st['p1'], st['p_over'], st['p_under']) * 100)
    p_base_mkt = f"1X ({c_name} o Pareggio)" if st['p1'] >= st['p2'] else f"X2 ({o_name} o Pareggio)"
    p_base_q = round(1 / max(0.40, (st['p1'] + st['px'] if st['p1'] >= st['p2'] else st['p2'] + st['px'])), 2)

    pronosticiExtra = {
        "1": {
            "icona": "🛡️", "tipo": "Pronostico Base (Alta Probabilità)", "badgeCol": "border-cyan-500/30 text-cyan-400 bg-cyan-950/40",
            "mercato": p_base_mkt, "prob": p_base_prob, "probStr": f"{p_base_prob}%", "quota": f"{p_base_q}", "qEqua": f"{round(p_base_q*0.96,2)}",
            "alt": f"Over 1.5 @ {round(st['q_over']*0.72,2)}", "barCol": "from-cyan-500 to-blue-600",
            "desc": "Basso rischio statistico. Copertura solida ad alta probabilità congiunta."
        },
        "2": {
            "icona": "🔥", "tipo": "Miglior Combo Valore", "badgeCol": "border-emerald-500/30 text-emerald-400 bg-emerald-950/40",
            "mercato": f"{'1' if st['p1']>=st['p2'] else '2'} + Over 1,5",
            "prob": int(min(st['p1'], st['p_over']) * 85), "probStr": f"{int(min(st['p1'], st['p_over']) * 85)}%",
            "quota": f"{round(q_rec * 1.35, 2)}", "qEqua": f"{round(q_rec * 1.25, 2)}",
            "alt": "1X + Multigol 2-4", "barCol": "from-emerald-500 to-teal-600",
            "desc": "Miglior rapporto matematico rischio/rendimento su Eurobet/Bet365."
        },
        "3": {
            "icona": "⚡", "tipo": "Pronostico Hard (Quota Alta)", "badgeCol": "border-amber-500/30 text-amber-400 bg-amber-950/40",
            "mercato": f"Risultato Esatto 2-1" if l_c > m_o else "Risultato Esatto 1-2",
            "prob": 12, "probStr": "12%", "quota": "8.50", "qEqua": "7.80",
            "alt": f"Parziale/Finale {'1/1' if l_c>m_o else '2/2'} @ {round(q_rec*2.2,2)}", "barCol": "from-amber-500 to-rose-600",
            "desc": "Quota speculativa per giocata singola a stake ridotto (0.5% cassa)."
        },
        "4": {
            "icona": "🎯", "tipo": "Pronostico Extra (Situazionale)", "badgeCol": "border-purple-500/30 text-purple-400 bg-purple-950/40",
            "mercato": f"Multigol 2-4 Totale", "prob": int(st['p_over']*90), "probStr": f"{int(st['p_over']*90)}%",
            "quota": "1.55", "qEqua": "1.48",
            "alt": f"Gol Entrambe @ {st['q_gg']}", "barCol": "from-purple-500 to-indigo-600",
            "desc": "Mercato situazionale calibrato sulla varianza realizzativa."
        }
    }

    return {
        "id": mid,
        "label": f"{c_name} - {o_name}",
        "giornata": data_str.split('·')[0].strip(),
        "data": data_str,
        "bgGradient": bg_grad,
        "casa": {"sigla": c_sigla, "nome": c_name, "rank": f"xG {l_c}/gara", "colBox": c_col},
        "ospite": {"sigla": o_sigla, "nome": o_name, "rank": f"xG {m_o}/gara", "colBox": o_col},
        "golC": f"{l_c:.2f}",
        "golO": f"{m_o:.2f}",
        "barC": bar_c,
        "barO": bar_o,
        "isValore": is_val,
        "evBadge": f"+{edge_val:.1f}%" if is_val else "0,0%",
        "mercato": rec_mkt,
        "qEqua": f"{q_rec:.2f}",
        "qReale": f"{val_book_q:.2f}" if is_val else f"{q_rec*0.94:.2f}",
        "spiegazione": spiegaz or f"Modello stima probabilità del {int(st['p1']*100)}% con xG {l_c:.2f} vs {m_o:.2f}.",
        "analisi": analisi_str or f"Il differenziale offensivo atteso è di {(l_c-m_o):+.2f} xG. La densità difensiva premia {c_name if l_c>m_o else o_name}.",
        "rischio": rischio_str or "Possibile calo atletico nella ripresa o rotazioni post-coppe.",
        "fasi": fasi,
        "pronosticiExtra": pronosticiExtra
    }

def build_ligue1():
    partite = [
        make_match("mon-bre", "Monaco", "ASM", "Brest", "SB29", "Venerdì 22 Nov · 19:00", 2.10, 1.10,
                   "bg-red-600/20 text-red-400 border-red-500", "bg-red-700/20 text-red-300 border-red-500",
                   "from-[#450a0a] via-[#090d16] to-[#3b0818]", "1", True, 1.60, 6.8,
                   "Monaco fortissimo al Louis II: xG 2.10 vs 1.10. Quota 1.60 a valore contro una quota equa di 1.50.",
                   "Brest fatica a reggere il doppio impegno Ligue 1 / Champions League. Monaco con Akliouche e Ben Seghir in grande spolvero.",
                   "Possibile stanchezza difensiva monegasca nei finali di gara."),
        make_match("psg-tou", "Paris Saint-Germain", "PSG", "Toulouse", "TFC", "Venerdì 22 Nov · 21:00", 2.75, 0.70,
                   "bg-blue-800/20 text-blue-400 border-blue-500", "bg-purple-700/20 text-purple-400 border-purple-500",
                   "from-[#0c2444] via-[#090d16] to-[#3b0764]", "1", False, 1.25, 0.0,
                   "PSG dominatore incontrastato al Parco dei Principi: xG 2.75. Quota 1.25 priva di margine matematico.",
                   "Barcola e Dembele imperversano sulle fasce. Il Tolosa si chiuderà con 5 difensori per limitare il passivo.",
                   "Turnover di Luis Enrique prima del match di Champions."),
        make_match("len-mar", "Lens", "RCL", "Marseille", "OM", "Sabato 23 Nov · 17:00", 1.45, 1.70,
                   "bg-amber-600/20 text-amber-400 border-amber-500", "bg-sky-500/20 text-sky-400 border-sky-400",
                   "from-[#451a03] via-[#090d16] to-[#075985]", "GG", True, 1.68, 7.5,
                   "Bolla incandescente allo Stade Bollaert-Delelis: De Zerbi propone calcio ultra-offensivo a Marsiglia. Gol (GG) quota 1.68.",
                   "OM ha il miglior attacco esterno della Francia con Greenwood. Il Lens a casa crea sempre tantissimo.",
                   "Partita molto nervosa e ricca di duelli aerei."),
        make_match("ste-mon", "Saint-Etienne", "ASSE", "Montpellier", "MHSC", "Sabato 23 Nov · 19:00", 1.40, 1.35,
                   "bg-emerald-700/20 text-emerald-400 border-emerald-600", "bg-orange-600/20 text-orange-400 border-orange-500",
                   "from-[#064e3b] via-[#090d16] to-[#431407]", "OVER", True, 1.85, 8.2,
                   "Scontro salvezza infuocato al Geoffroy-Guichard: due tra le peggiori difese della Ligue 1. Over 2.5 a 1.85 ha grande valore.",
                   "Montpellier subisce oltre 2.30 xGA fuori casa. Saint-Etienne costretto a vincere davanti ai suoi tifosi.",
                   "Tensione da retrocessione che potrebbe bloccare i primi minuti."),
        make_match("rei-lyo", "Reims", "SDR", "Lyon", "OL", "Sabato 23 Nov · 21:00", 1.30, 1.65,
                   "bg-red-700/20 text-red-400 border-red-600", "bg-blue-700/20 text-blue-400 border-blue-500",
                   "from-[#450a0a] via-[#090d16] to-[#0b2447]", "2", True, 2.15, 6.4,
                   "Lione in ascesa con Cherki e Lacazette: xG 1.65 contro 1.30 del Reims. Quota esterna 2.15 molto appetibile.",
                   "Reims in calo atletico dopo un ottimo avvio. OL pericolosissimo nelle transizioni centrali.",
                   "Reims molto insidioso sui calci d'angolo con Munetsi."),
        make_match("lil-ren", "Lille", "LOSC", "Rennes", "SRFC", "Domenica 24 Nov · 15:00", 1.85, 1.15,
                   "bg-red-700/20 text-red-400 border-red-500", "bg-red-800/20 text-red-400 border-red-600",
                   "from-[#450a0a] via-[#090d16] to-[#2d060d]", "1", True, 1.75, 7.0,
                   "Stade Pierre-Mauroy fortino dei mastini: David trascina il Lille (xG 1.85). Quota 1.75 di valore.",
                   "Rennes in crisi d'identità e con cambio in panchina (arrivo di Jorge Sampaoli).",
                   "Effetto scossa psicologica per il Rennes con il nuovo allenatore."),
        make_match("nan-hav", "Nantes", "FCN", "Le Havre", "HAC", "Domenica 24 Nov · 17:00", 1.35, 0.90,
                   "bg-yellow-500/20 text-yellow-400 border-yellow-500", "bg-sky-600/20 text-sky-400 border-sky-500",
                   "from-[#422006] via-[#090d16] to-[#0c2444]", "1X", False, 1.25, 0.0,
                   "Gara da pochi squilli alla Beaujoire. Entrambe badano a non prenderle. Mercato allineato al banco.",
                   "Le Havre segna solo 0.70 gol a gara esterna. Nantes molto solido con Kombouare.",
                   "Poco appeal statistico sulle giocate principali."),
        make_match("aux-ang", "Auxerre", "AJA", "Angers", "SCO", "Domenica 24 Nov · 17:00", 1.60, 1.10,
                   "bg-blue-600/20 text-blue-400 border-blue-500", "bg-slate-700/20 text-white border-slate-500",
                   "from-[#0c2444] via-[#090d16] to-[#1e293b]", "1", True, 1.80, 6.2,
                   "L'Abbe-Deschamps trascina l'Auxerre: 4 vittorie nelle ultime 5 in casa. Quota 1.80 favorevole rispetto al fair 1.70.",
                   "Angers con evidenti limiti di organico contro il pressing asfissiante dei borgognoni.",
                   "Angers compatto nei primi 45 minuti."),
        make_match("nic-str", "Nice", "OGCN", "Strasbourg", "RCSA", "Domenica 24 Nov · 20:45", 1.95, 1.05,
                   "bg-red-700/20 text-red-400 border-red-600", "bg-blue-600/20 text-blue-400 border-blue-500",
                   "from-[#450a0a] via-[#090d16] to-[#0c2444]", "1", True, 1.68, 6.5,
                   "Allianz Riviera spinge i rossoneri di Haise: Nizza crea 1.95 xG a gara con Guessand e Boga.",
                   "Strasburgo giovanissimo e privo di esperienza nelle trasferte calde della Costa Azzurra.",
                   "Strasburgo insidioso con il baby talento Moreira in contropiede.")
    ]

    return {
        "nome": "Ligue 1 (Francia)",
        "turni": {
            "12": {
                "label": "12ª Giornata (22-24 Nov 2026)",
                "dataFine": "2026-11-24T23:59:59",
                "partite": partite
            }
        }
    }

def main():
    with open('scheda-partita-dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add Ligue 1 to select-campionato dropdown if missing
    if '<option value="ligue1">' not in html:
        bundesliga_opt = '<option value="bundesliga">🇩🇪 Bundesliga (Germania)</option>'
        ligue1_opt = '<option value="bundesliga">🇩🇪 Bundesliga (Germania)</option>\n            <option value="ligue1">🇫🇷 Ligue 1 (Francia)</option>'
        html = html.replace(bundesliga_opt, ligue1_opt, 1)
        print('1. Added Ligue 1 to select-campionato dropdown.')

    # 2. Build Ligue 1 dataset
    ligue1_data = build_ligue1()

    # Locate DATA_PRO
    pos_dp = html.find('const DATA_PRO = {')
    pos_dp_end = html.find('const LOGHI_SQUADRE =', pos_dp)
    pos_semi = html.rfind('};', pos_dp, pos_dp_end) + 2
    raw_dp = html[pos_dp + len('const DATA_PRO = '):pos_semi - 1]
    data_pro = json.loads(raw_dp)

    data_pro['ligue1'] = ligue1_data
    new_data_pro_js = f"const DATA_PRO = {json.dumps(data_pro, ensure_ascii=False, indent=2)};"
    html = html[:pos_dp] + new_data_pro_js + html[pos_semi:]
    print('2. DATA_PRO updated with Ligue 1 (9 matches)!')

    # 3. Add Ligue 1 teams to DATA_FORMA
    ligue1_forma = {
        "Paris Saint-Germain": {"last5": [{"opp": "Angers", "gf": 4, "gs": 2, "res": "V", "xg_f": 2.8, "xg_s": 0.9, "xg_diff": 1.9, "home": False, "date": "09/11/2026"}], "summary5": "4V 1N 0P", "tot_xg_diff_5": 5.4, "trend_desc": "Dominio assoluto in Francia (+5.40 xG)", "tot_partite": 11, "v": 9, "n": 2, "p": 0, "gf": 33, "gs": 10, "xg_f_avg": 2.75, "xg_s_avg": 0.85, "cs_perc": 36, "bts_perc": 64},
        "Monaco": {"last5": [{"opp": "Strasbourg", "gf": 3, "gs": 1, "res": "V", "xg_f": 2.2, "xg_s": 1.1, "xg_diff": 1.1, "home": False, "date": "09/11/2026"}], "summary5": "3V 0N 2P", "tot_xg_diff_5": 2.3, "trend_desc": "Solido e propositivo (+2.30 xG)", "tot_partite": 11, "v": 7, "n": 2, "p": 2, "gf": 18, "gs": 8, "xg_f_avg": 1.95, "xg_s_avg": 1.05, "cs_perc": 45, "bts_perc": 45},
        "Marseille": {"last5": [{"opp": "Auxerre", "gf": 1, "gs": 3, "res": "P", "xg_f": 1.8, "xg_s": 1.4, "xg_diff": 0.4, "home": True, "date": "08/11/2026"}], "summary5": "3V 0N 2P", "tot_xg_diff_5": 1.8, "trend_desc": "Attacco esplosivo ma distrazioni (-0.20 xG)", "tot_partite": 11, "v": 6, "n": 2, "p": 3, "gf": 24, "gs": 15, "xg_f_avg": 1.90, "xg_s_avg": 1.35, "cs_perc": 18, "bts_perc": 64},
        "Lille": {"last5": [{"opp": "Nice", "gf": 2, "gs": 2, "res": "N", "xg_f": 1.6, "xg_s": 1.5, "xg_diff": 0.1, "home": False, "date": "10/11/2026"}], "summary5": "3V 2N 0P", "tot_xg_diff_5": 2.1, "trend_desc": "In serie utile da 10 partite (+2.10 xG)", "tot_partite": 11, "v": 5, "n": 4, "p": 2, "gf": 18, "gs": 11, "xg_f_avg": 1.80, "xg_s_avg": 1.15, "cs_perc": 36, "bts_perc": 55},
        "Lyon": {"last5": [{"opp": "Saint-Etienne", "gf": 1, "gs": 0, "res": "V", "xg_f": 1.7, "xg_s": 0.9, "xg_diff": 0.8, "home": True, "date": "10/11/2026"}], "summary5": "3V 1N 1P", "tot_xg_diff_5": 1.9, "trend_desc": "In crescita costante (+1.90 xG)", "tot_partite": 11, "v": 5, "n": 3, "p": 3, "gf": 18, "gs": 15, "xg_f_avg": 1.70, "xg_s_avg": 1.30, "cs_perc": 36, "bts_perc": 55},
        "Nice": {"last5": [{"opp": "Lille", "gf": 2, "gs": 2, "res": "N", "xg_f": 1.5, "xg_s": 1.6, "xg_diff": -0.1, "home": True, "date": "10/11/2026"}], "summary5": "2V 3N 0P", "tot_xg_diff_5": 1.4, "trend_desc": "Imbattuto da 7 turni (+1.40 xG)", "tot_partite": 11, "v": 4, "n": 5, "p": 2, "gf": 21, "gs": 11, "xg_f_avg": 1.85, "xg_s_avg": 1.10, "cs_perc": 27, "bts_perc": 64},
        "Lens": {"last5": [{"opp": "Nantes", "gf": 3, "gs": 2, "res": "V", "xg_f": 2.1, "xg_s": 1.2, "xg_diff": 0.9, "home": True, "date": "09/11/2026"}], "summary5": "2V 2N 1P", "tot_xg_diff_5": 1.1, "trend_desc": "Miglior difesa casalinga (+1.10 xG)", "tot_partite": 11, "v": 4, "n": 5, "p": 2, "gf": 12, "gs": 9, "xg_f_avg": 1.50, "xg_s_avg": 1.05, "cs_perc": 45, "bts_perc": 45},
        "Brest": {"last5": [{"opp": "Montpellier", "gf": 1, "gs": 3, "res": "P", "xg_f": 1.2, "xg_s": 1.8, "xg_diff": -0.6, "home": False, "date": "10/11/2026"}], "summary5": "2V 1N 2P", "tot_xg_diff_5": 0.2, "trend_desc": "Fatica post-Champions (-0.20 xG)", "tot_partite": 11, "v": 4, "n": 1, "p": 6, "gf": 14, "gs": 19, "xg_f_avg": 1.35, "xg_s_avg": 1.55, "cs_perc": 27, "bts_perc": 45},
        "Reims": {"last5": [{"opp": "Le Havre", "gf": 3, "gs": 0, "res": "V", "xg_f": 1.9, "xg_s": 0.8, "xg_diff": 1.1, "home": False, "date": "10/11/2026"}], "summary5": "2V 0N 3P", "tot_xg_diff_5": -0.4, "trend_desc": "Altalenante (-0.40 xG)", "tot_partite": 11, "v": 5, "n": 2, "p": 4, "gf": 19, "gs": 15, "xg_f_avg": 1.45, "xg_s_avg": 1.40, "cs_perc": 18, "bts_perc": 73},
        "Toulouse": {"last5": [{"opp": "Rennes", "gf": 2, "gs": 0, "res": "V", "xg_f": 1.6, "xg_s": 0.7, "xg_diff": 0.9, "home": False, "date": "10/11/2026"}], "summary5": "3V 1N 1P", "tot_xg_diff_5": 1.5, "trend_desc": "Tre vittorie consecutive senza subire gol (+1.50 xG)", "tot_partite": 11, "v": 4, "n": 3, "p": 4, "gf": 13, "gs": 11, "xg_f_avg": 1.35, "xg_s_avg": 1.20, "cs_perc": 36, "bts_perc": 36},
        "Strasbourg": {"last5": [{"opp": "Monaco", "gf": 1, "gs": 3, "res": "P", "xg_f": 1.1, "xg_s": 2.2, "xg_diff": -1.1, "home": True, "date": "09/11/2026"}], "summary5": "1V 1N 3P", "tot_xg_diff_5": -1.3, "trend_desc": "Tanti gol subiti (-1.30 xG)", "tot_partite": 11, "v": 3, "n": 4, "p": 4, "gf": 20, "gs": 22, "xg_f_avg": 1.50, "xg_s_avg": 1.70, "cs_perc": 9, "bts_perc": 82},
        "Rennes": {"last5": [{"opp": "Toulouse", "gf": 0, "gs": 2, "res": "P", "xg_f": 0.7, "xg_s": 1.6, "xg_diff": -0.9, "home": True, "date": "10/11/2026"}], "summary5": "1V 1N 3P", "tot_xg_diff_5": -1.8, "trend_desc": "Crisi aperta e cambio allenatore (-1.80 xG)", "tot_partite": 11, "v": 3, "n": 2, "p": 6, "gf": 13, "gs": 18, "xg_f_avg": 1.30, "xg_s_avg": 1.55, "cs_perc": 18, "bts_perc": 55},
        "Auxerre": {"last5": [{"opp": "Marseille", "gf": 3, "gs": 1, "res": "V", "xg_f": 1.4, "xg_s": 1.8, "xg_diff": -0.4, "home": False, "date": "08/11/2026"}], "summary5": "3V 1N 1P", "tot_xg_diff_5": 1.2, "trend_desc": "Super forma in casa (+1.20 xG)", "tot_partite": 11, "v": 5, "n": 1, "p": 5, "gf": 20, "gs": 19, "xg_f_avg": 1.55, "xg_s_avg": 1.55, "cs_perc": 18, "bts_perc": 64},
        "Saint-Etienne": {"last5": [{"opp": "Lyon", "gf": 0, "gs": 1, "res": "P", "xg_f": 0.9, "xg_s": 1.7, "xg_diff": -0.8, "home": False, "date": "10/11/2026"}], "summary5": "1V 0N 4P", "tot_xg_diff_5": -2.5, "trend_desc": "Difficoltà difensive da neopromossa (-2.50 xG)", "tot_partite": 11, "v": 3, "n": 1, "p": 7, "gf": 10, "gs": 25, "xg_f_avg": 1.10, "xg_s_avg": 2.10, "cs_perc": 18, "bts_perc": 36},
        "Nantes": {"last5": [{"opp": "Lens", "gf": 2, "gs": 3, "res": "P", "xg_f": 1.2, "xg_s": 2.1, "xg_diff": -0.9, "home": False, "date": "09/11/2026"}], "summary5": "0V 2N 3P", "tot_xg_diff_5": -1.4, "trend_desc": "Senza vittorie da 8 gare (-1.40 xG)", "tot_partite": 11, "v": 2, "n": 4, "p": 5, "gf": 14, "gs": 17, "xg_f_avg": 1.25, "xg_s_avg": 1.50, "cs_perc": 18, "bts_perc": 64},
        "Angers": {"last5": [{"opp": "PSG", "gf": 2, "gs": 4, "res": "P", "xg_f": 0.9, "xg_s": 2.8, "xg_diff": -1.9, "home": True, "date": "09/11/2026"}], "summary5": "2V 1N 2P", "tot_xg_diff_5": -0.6, "trend_desc": "Reattivo ma organico ridotto (-0.60 xG)", "tot_partite": 11, "v": 2, "n": 4, "p": 5, "gf": 13, "gs": 20, "xg_f_avg": 1.20, "xg_s_avg": 1.65, "cs_perc": 9, "bts_perc": 73},
        "Le Havre": {"last5": [{"opp": "Reims", "gf": 0, "gs": 3, "res": "P", "xg_f": 0.8, "xg_s": 1.9, "xg_diff": -1.1, "home": True, "date": "10/11/2026"}], "summary5": "1V 0N 4P", "tot_xg_diff_5": -2.8, "trend_desc": "Peggior attacco della lega (-2.80 xG)", "tot_partite": 11, "v": 3, "n": 0, "p": 8, "gf": 8, "gs": 23, "xg_f_avg": 0.95, "xg_s_avg": 1.85, "cs_perc": 18, "bts_perc": 27},
        "Montpellier": {"last5": [{"opp": "Brest", "gf": 3, "gs": 1, "res": "V", "xg_f": 1.8, "xg_s": 1.2, "xg_diff": 0.6, "home": True, "date": "10/11/2026"}], "summary5": "1V 0N 4P", "tot_xg_diff_5": -3.2, "trend_desc": "Ultimo posto e difesa colabrodo (-3.20 xG)", "tot_partite": 11, "v": 2, "n": 1, "p": 8, "gf": 11, "gs": 31, "xg_f_avg": 1.20, "xg_s_avg": 2.45, "cs_perc": 0, "bts_perc": 73}
    }

    pos_forma = html.find('const DATA_FORMA = {')
    pos_end_forma = html.find('};', pos_forma) + 2
    raw_forma = html[pos_forma + len('const DATA_FORMA = '):pos_end_forma - 1]
    data_forma = json.loads(raw_forma)

    for k, v in ligue1_forma.items():
        data_forma[k] = v

    new_forma_js = f"const DATA_FORMA = {json.dumps(data_forma, ensure_ascii=False, indent=2)};"
    html = html[:pos_forma] + new_forma_js + html[pos_end_forma:]
    print(f'3. DATA_FORMA updated with Ligue 1 (total {len(data_forma)} teams)!')

    # 4. Map Ligue 1 teams in LOGHI_SQUADRE to ./assets/loghi/<slug>.png
    ligue1_slugs = {
        "Paris Saint-Germain": "./assets/loghi/psg.png",
        "PSG": "./assets/loghi/psg.png",
        "Marseille": "./assets/loghi/marseille.png",
        "Monaco": "./assets/loghi/monaco.png",
        "Lyon": "./assets/loghi/lyon.png",
        "Lille": "./assets/loghi/lille.png",
        "Lens": "./assets/loghi/lens.png",
        "Rennes": "./assets/loghi/rennes.png",
        "Nice": "./assets/loghi/nice.png",
        "Brest": "./assets/loghi/brest.png",
        "Reims": "./assets/loghi/reims.png",
        "Toulouse": "./assets/loghi/toulouse.png",
        "Strasbourg": "./assets/loghi/strasbourg.png",
        "Saint-Etienne": "./assets/loghi/saint_etienne.png",
        "Montpellier": "./assets/loghi/montpellier.png",
        "Nantes": "./assets/loghi/nantes.png",
        "Le Havre": "./assets/loghi/le_havre.png",
        "Auxerre": "./assets/loghi/auxerre.png",
        "Angers": "./assets/loghi/angers.png"
    }

    pos_ls = html.find('const LOGHI_SQUADRE = {')
    pos_ls_end = html.find('};', pos_ls) + 2
    raw_ls = html[pos_ls + len('const LOGHI_SQUADRE = '):pos_ls_end - 1]
    cur_loghi = dict(re.findall(r'\"([^\"]+)\":\s*\"([^\"]+)\"', raw_ls))

    for k, v in ligue1_slugs.items():
        cur_loghi[k] = v

    new_ls_js = f"const LOGHI_SQUADRE = {json.dumps(cur_loghi, ensure_ascii=False, indent=2)};"
    html = html[:pos_ls] + new_ls_js + html[pos_ls_end:]
    print(f'4. LOGHI_SQUADRE updated with Ligue 1 teams (total {len(cur_loghi)} crests)!')

    with open('scheda-partita-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('scheda-partita-dashboard.html successfully updated with Ligue 1!')

if __name__ == '__main__':
    main()
