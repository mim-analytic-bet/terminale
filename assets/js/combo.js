(function (root) {
  "use strict";

  // ---------------------------------------------------------------------------
  // CALCOLO PURO (nessun DOM): usato dalla pagina e, in Node, dal registro delle proposte.
  // Le regole sono quelle gia' in uso: nessuna soglia e' stata cambiata nel passaggio a questo formato.
  // ---------------------------------------------------------------------------
  var MK = [
    ["1", "1", function (m) { return m.fasi[1].seg1.p; }],
    ["2", "2", function (m) { return m.fasi[1].seg3.p; }],
    ["1X", "1X", function (m) { return m.fasi[1].seg1.p + m.fasi[1].seg2.p; }],
    ["X2", "X2", function (m) { return m.fasi[1].seg2.p + m.fasi[1].seg3.p; }],
    ["Over 2,5", "Over 2,5", function (m) { return m.fasi[3].seg1.p; }],
    ["Under 2,5", "Under 2,5", function (m) { return m.fasi[3].seg2.p; }],
    ["Gol", "Gol", function (m) { return m.fasi[2].seg1.p; }],
    ["No Gol", "No Gol", function (m) { return m.fasi[2].seg2.p; }]
  ];

  var PESO_Q = { "reale": 0, "derivata": 1, "equa": 2 };

  function qm(m, k) {
    var q = m.quoteMercato;
    if (!q) return null;
    if (q[k]) return +q[k];
    if (k === "1X" && q["1"] && q["X"]) return 1 / (1 / q["1"] + 1 / q["X"]);
    if (k === "X2" && q["2"] && q["X"]) return 1 / (1 / q["2"] + 1 / q["X"]);
    return null;
  }

  function tipoQ(m, k) {
    var q = m.quoteMercato;
    if (q && q[k]) return "reale";
    if (q && (k === "1X" || k === "X2") && q["X"] && q[k === "1X" ? "1" : "2"]) return "derivata";
    return "equa";
  }

  function parsaDataPartita(strData, dataFineTurno, adesso) {
    var mesi = { "Gen": 0, "Feb": 1, "Mar": 2, "Apr": 3, "Mag": 4, "Giu": 5, "Lug": 6, "Ago": 7, "Set": 8, "Ott": 9, "Nov": 10, "Dic": 11 };
    var m = (strData || "").match(/(\d{1,2})\s+([A-Za-z]{3})/);
    if (!m) {
      if (dataFineTurno) return new Date(dataFineTurno);
      return new Date(2099, 0, 1);
    }
    var giorno = parseInt(m[1], 10);
    var meseNome = m[2];
    var mese = mesi[meseNome] !== undefined ? mesi[meseNome] : 10;
    var anno = adesso.getFullYear();
    if (dataFineTurno) {
      var df = new Date(dataFineTurno);
      anno = df.getFullYear();
      if (new Date(anno, mese, giorno).getTime() > df.getTime() + 86400000) anno -= 1;
    } else if (mese < adesso.getMonth() - 6) {
      anno += 1;
    }
    var mOra = (strData || "").match(/(\d{1,2}):(\d{2})/);
    var ore = mOra ? parseInt(mOra[1], 10) : 20;
    var min = mOra ? parseInt(mOra[2], 10) : 0;
    return new Date(anno, mese, giorno, ore, min);
  }

  function calcola(DATA_PRO, adesso) {
    adesso = adesso || new Date();
    var allPartite = [];
    Object.keys(DATA_PRO).forEach(function (k) {
      var comp = DATA_PRO[k];
      var T = comp.turni || {};
      Object.keys(T).forEach(function (t) {
        (T[t].partite || []).forEach(function (m) {
          var d = parsaDataPartita(m.data, T[t].dataFine, adesso);
          allPartite.push({ comp: k, compNome: comp.nome || k, turno: t, match: m, date: d });
        });
      });
    });

    var future = allPartite.filter(function (item) {
      return item.date.getTime() >= (adesso.getTime() - 2 * 3600 * 1000);
    });
    if (!future.length) future = allPartite;

    future.sort(function (a, b) { return a.date - b.date; });
    var primaData = future[0] ? future[0].date : new Date(adesso.getTime());
    var giornoSettimana = primaData.getDay();

    var windowEnd = new Date(primaData);
    var isCoppaBlock = false;
    if (giornoSettimana >= 2 && giornoSettimana <= 4) {
      isCoppaBlock = true;
      var giorniAFri = (5 - giornoSettimana + 7) % 7 || 7;
      windowEnd.setDate(windowEnd.getDate() + giorniAFri);
      windowEnd.setHours(4, 0, 0, 0);
    } else {
      var giorniATue = (2 - giornoSettimana + 7) % 7 || 7;
      windowEnd.setDate(windowEnd.getDate() + giorniATue);
      windowEnd.setHours(4, 0, 0, 0);
    }

    var bloccoPartite = future.filter(function (item) {
      return item.date.getTime() <= windowEnd.getTime();
    });
    if (!bloccoPartite.length) bloccoPartite = future.slice(0, 30);

    var etichettaFinestra = isCoppaBlock ? "Coppe Europee" : "Campionati";

    var C = [];
    bloccoPartite.forEach(function (item) {
      var m = item.match;
      if (DATA_PRO[item.comp] && DATA_PRO[item.comp].osservazione) return;
      MK.forEach(function (x) {
        var p = x[2](m);
        if (!(p > 0.05 && p < 0.97)) return;
        var r = qm(m, x[0]);
        var q = r || (1 / p);
        var tipo = tipoQ(m, x[0]);
        C.push({
          id: item.comp + item.turno + m.id,
          lbl: m.label,
          data: m.data,
          compNome: item.compNome,
          mer: x[1],
          p: p,
          q: q,
          ref: !!r,
          tipo: tipo,
          // campi per il registro (non usati dalla grafica)
          comp: item.comp,
          turno: item.turno,
          mid: m.id,
          inizioUtc: m.inizioUtc || null,
          chiave: m.chiave || null
        });
      });
    });

    function inRange(c, a, b) { return c.q >= a && c.q <= b; }

    function clusterEventi(a, b, minRealiComb) {
      var L = C.filter(function (c) {
        return inRange(c, a, b) || (minRealiComb && c.tipo === "reale");
      });
      var out = [];
      for (var i = 0; i < L.length; i++) {
        for (var j = i + 1; j < L.length; j++) {
          if (L[i].id !== L[j].id && L[i].lbl !== L[j].lbl) {
            var ok = (inRange(L[i], a, b) && inRange(L[j], a, b)) ||
              (minRealiComb && L[i].tipo === "reale" && L[j].tipo === "reale" && (L[i].q * L[j].q) >= minRealiComb);
            if (ok) out.push([L[i], L[j]]);
          }
        }
      }
      out.sort(function (x, y) {
        var wx = PESO_Q[x[0].tipo] + PESO_Q[x[1].tipo];
        var wy = PESO_Q[y[0].tipo] + PESO_Q[y[1].tipo];
        if (wx !== wy) return wx - wy;
        return (y[0].p * y[1].p) - (x[0].p * x[1].p);
      });
      var usati = {}, sel = [];
      out.forEach(function (o) {
        if (sel.length >= 3) return;
        if (usati[o[0].lbl] || usati[o[1].lbl]) return;
        usati[o[0].lbl] = usati[o[1].lbl] = 1;
        sel.push(o);
      });
      return sel;
    }

    var P1 = clusterEventi(1.65, 1.80, 1.98).map(function (o) { return { cod: "P1", etichetta: "Eventi Combinati (2 Selezioni)", legs: o }; });
    var P2 = clusterEventi(1.80, 2.00).slice(0, 2).map(function (o) { return { cod: "P2", etichetta: "Cluster Multi-Evento (Fascia 1.80–2.00)", legs: o }; });

    var sing = C.filter(function (c) { return c.q >= 3.5; }).sort(function (a, b) {
      if (PESO_Q[a.tipo] !== PESO_Q[b.tipo]) return PESO_Q[a.tipo] - PESO_Q[b.tipo];
      return b.p - a.p;
    });
    var seenL = {};
    sing = sing.filter(function (c) {
      if (seenL[c.lbl]) return false;
      seenL[c.lbl] = 1;
      return true;
    });
    if (sing[0]) P2.push({ cod: "P2S", etichetta: "Cluster Multi-Evento (Singola ≥ 3.50)", legs: [sing[0]] });
    if (sing[1] && P2.length < 3) P2.push({ cod: "P2S", etichetta: "Cluster Multi-Evento (Singola ≥ 3.50)", legs: [sing[1]] });

    return { P1: P1, P2: P2, isCoppaBlock: isCoppaBlock, etichettaFinestra: etichettaFinestra };
  }

  // Esporta il calcolo per Node (registro delle proposte e test)
  if (typeof module !== "undefined" && module.exports) module.exports = { calcola: calcola };

  // ---------------------------------------------------------------------------
  // GRAFICA (solo nel browser)
  // ---------------------------------------------------------------------------
  if (typeof document === "undefined" || typeof DATA_PRO === "undefined") return;
  try {
    var R = calcola(DATA_PRO, new Date());
    var etichettaFinestra = R.etichettaFinestra, isCoppaBlock = R.isCoppaBlock;

    function riga(c) {
      return '<div class="flex justify-between items-center gap-2 py-1.5 border-b border-slate-800/70">' +
        '<div>' +
        '<div class="font-bold text-white text-xs">' + c.lbl + '</div>' +
        '<div class="text-[10px] text-slate-400 mono">' + c.data + ' · <span class="text-cyan-400">' + c.compNome + '</span></div>' +
        '</div>' +
        '<div class="text-right">' +
        '<div class="font-black text-cyan-300">' + c.mer + '</div>' +
        '<div class="text-[10px] mono text-slate-400">@ ' + c.q.toFixed(2) + (c.tipo === "reale" ? "" : c.tipo === "derivata" ? " (da 1X2)" : " (equa)") + ' · ' + Math.round(c.p * 100) + '%</div>' +
        '</div>' +
        '</div>';
    }

    function scheda(legs, etichetta) {
      var molt = 1, prob = 1;
      legs.forEach(function (c) {
        molt = molt * c.q;
        prob = prob * c.p;
      });
      return '<div class="text-[10px] uppercase mono text-cyan-300 mb-1 flex justify-between items-center">' +
        '<span>' + etichetta + '</span>' +
        '<span class="text-[9px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded-full mono">' + etichettaFinestra + '</span>' +
        '</div>' +
        legs.map(riga).join("") +
        '<div class="flex justify-between mt-2 mono"><span class="text-slate-400">Moltiplicatore ' + (legs.length > 1 ? "combinato" : "singolo") + '</span><span class="font-black text-white">' + molt.toFixed(2) + '</span></div>' +
        '<div class="flex justify-between mono"><span class="text-slate-400">Prob. congiunta modello' + (legs.length > 1 ? " (indipendenti)" : "") + '</span><span class="font-black text-white">' + Math.round(prob * 100) + '%</span></div>' +
        '<div class="mt-2 text-[10px] text-slate-500 leading-snug">' +
        (legs.every(function (c) { return c.tipo === "reale"; }) ? "Quote Bet365 reali." : "Quote Bet365 reali, tranne dove indicato: &laquo;da 1X2&raquo; = ricavata dalle quote 1X2 Bet365; &laquo;equa&raquo; = 1/probabilità del modello, non una quota Bet365.") +
        '</div>';
    }

    function attivaCarosello(i, P) {
      var corpo = document.getElementById("corpo-combo-" + i);
      var dots = document.getElementById("dots-combo-" + i);
      if (!corpo) return;
      if (!P.length) {
        corpo.innerHTML = '<div class="text-slate-400 py-4">' +
          (isCoppaBlock ? 'Prossimo blocco: coppe europee in osservazione statistica.' : 'Nessuna combinazione nei filtri per la finestra (' + etichettaFinestra + ').') +
          '</div>';
        return;
      }
      var k = 0, tm;
      function show(n) {
        k = (n + P.length) % P.length;
        corpo.style.opacity = 0;
        setTimeout(function () {
          corpo.innerHTML = P[k];
          corpo.style.opacity = 1;
        }, 150);
        if (dots) {
          dots.innerHTML = P.map(function (_, j) {
            return '<button data-j="' + j + '" style="width:8px;height:8px;border-radius:9999px;border:0;background:' + (j === k ? '#22d3ee' : '#475569') + ';cursor:pointer;"></button>';
          }).join("");
          [].forEach.call(dots.querySelectorAll("button"), function (b) {
            b.onclick = function () {
              clearInterval(tm);
              show(+b.getAttribute("data-j"));
              tm = setInterval(function () { show(k + 1); }, 6000);
            };
          });
        }
      }
      corpo.style.transition = "opacity .3s";
      corpo.innerHTML = P[0];
      show(0);
      tm = setInterval(function () { show(k + 1); }, 6000);
    }

    attivaCarosello(1, R.P1.map(function (o) { return scheda(o.legs, o.etichetta); }));
    attivaCarosello(2, R.P2.map(function (o) { return scheda(o.legs, o.etichetta); }));
  } catch (e) {
    console.error("combo", e);
  }
})(typeof window !== "undefined" ? window : this);
