# Skill "analisi-scommesse-calcio": descrizione completa

Documento per una revisione esterna: descrive cosa fa la skill, come funziona, come è stata testata e quali limiti sono noti. Il testo integrale delle istruzioni è in `analisi-scommesse-calcio/SKILL.md`.

---

## 1. Cos'è

Una **skill per Claude**: un pacchetto di istruzioni in linguaggio naturale (`SKILL.md`, circa 215 righe) più due script Python. Quando la richiesta dell'utente corrisponde alla descrizione della skill, Claude carica le istruzioni e le segue.

La skill **non contiene dati, quote né un modello statistico precalcolato**. Dice a Claude:
- quali dati cercare e dove;
- come trasformarli in percentuali;
- come scegliere i pronostici;
- come presentarli;
- come conservarli e verificarli dopo le partite.

I dati arrivano a ogni uso da strumenti esterni: connettori di statistiche calcistiche, ricerca web, quote incollate dall'utente.

**Utente tipo:** scommettitore italiano che gioca sul bookmaker, pre-partita, soprattutto sulla Serie A. Vuole analisi dettagliate e pronostici a livelli di quota fissi, senza limiti imposti su budget e puntate.

---

## 2. Quando si attiva

Il campo `description` (circa 1.000 caratteri) fa scattare la skill quando l'utente:
- nomina una o più partite, o una giornata di campionato, e chiede pronostici, un'analisi, una schedina, una multipla, una giocata "sicura" o "hard";
- incolla quote o screenshot del bookmaker;
- chiede come vede una partita;
- chiede com'è andata la giornata o di controllare i pronostici;
- incolla il proprio registro delle giocate.

**Campionati coperti:** Serie A (prioritaria), Premier League, Liga, Bundesliga, Ligue 1, Champions League.

---

## 3. Flusso di lavoro su una richiesta di pronostici

### 3.1 Verifica preliminare dello storico
Se esiste `storico-pronostici.csv` con partite già giocate ancora senza esito, la skill fa prima la verifica di quelle partite (vedi sezione 7).

### 3.2 Controllo del calendario
Verifica che ogni partita si giochi davvero nella data indicata: soste per le nazionali, partite già giocate, anticipi e posticipi.
- Se la data è diversa, lo dice subito.
- Se la partita è più avanti nel tempo, la analizza comunque e avvisa che dati e formazioni andranno ricontrollati.
- Poi offre di analizzare il prossimo turno delle stesse squadre.
- Non sostituisce di propria iniziativa le partite richieste.

### 3.3 Raccolta dati
Ogni dato usato va riportato con **fonte e data**.

| Categoria | Cosa raccoglie |
|---|---|
| Forma | ultime 5-10 partite, separate casa/trasferta |
| Gol | fatti e subiti, medie casa/trasferta, frequenza Over 2,5 e GG, xG/xGA se disponibili |
| Assenze | infortuni, squalifiche, probabili formazioni, rientri dalle nazionali |
| Contesto | impegni ravvicinati, motivazioni di classifica, cambi di allenatore, derby; scontri diretti con peso basso |
| Mercati speciali | marcatori: gol, tiri, minuti, rigorista, titolarità; cartellini: medie di squadra e dell'arbitro designato; corner solo se ci sono dati verificati |
| Per l'EXTRA | gol fatti e subiti per tempo, frequenza di GG e Over 3,5 |

Regole sui dati:
- Un dato mancante va segnato "non verificato" e alza l'incertezza, ma non blocca l'analisi.
- Se manca qualsiasi dato aggiornato su una partita, la skill lo chiede all'utente invece di inventarlo.
- Se un connettore dà errore, passa alla ricerca web e segnala all'utente che il connettore va ricollegato.
- Le proiezioni di modelli esterni sono solo un dato in ingresso: la stima finale è di Claude e deve partire dai dati, non dalla quota.

### 3.4 Metodo di stima
La skill **non impone una formula precisa**. Chiede di dichiarare il metodo in 2-3 righe in apertura e di applicarlo uguale a tutte le partite.

Nei test Claude ha sempre fatto così:
1. **Gol attesi** di ogni squadra: forza d'attacco moltiplicata per la debolezza difensiva dell'avversaria, rispetto alla media del campionato. Con poche giornate giocate, i numeri sono tirati verso la media di circa il 30%.
2. **Modello di Poisson** per passare dai gol attesi alla griglia dei punteggi fino al 4-4, e da lì a tutte le percentuali: 1X2, Over/Under, GG, combo, risultati esatti.
3. **Correzioni di giudizio dichiarate**, per esempio "−5% ai gol del Napoli per le assenze".

### 3.5 Controllo con il mercato
Dopo la stima dai dati, la skill la confronta con la probabilità implicita nella quota reale, tolto il margine del bookmaker (circa 5-7% sull'1X2).
- **Scarto fino a 5-6 punti:** è considerato normale.
- **Scarto oltre i 10 punti:** non va presentato come "valore", perché quasi sempre è il modello che non vede qualcosa (rosa, storico, assenze note). La stima viene avvicinata a metà strada tra modello e mercato, e vengono mostrati entrambi i numeri.

### 3.6 Scenario della partita
Per ogni partita la skill scrive:
- una riga di scenario, per esempio "Napoli favorito ma poco brillante, partita da pochi gol";
- le percentuali di base: 1 / X / 2, Over 2,5, GG;
- i 5-6 risultati esatti più probabili con la loro percentuale.

### 3.7 Scelta dei pronostici
Per ogni partita tre pronostici, più un quarto opzionale. Tutti devono essere **coerenti con lo stesso scenario**: l'HARD è lo sviluppo più audace della stessa lettura, non una scommessa scollegata.

| Livello | Fascia di quota | Uso | Mercati tipici |
|---|---|---|---|
| 🟢 SICURA | 1,25-1,35 | base per la multipla | doppia chance, Over 1,5, Under 3,5, multigol ampi, chance mix, combo prudenti |
| 🟡 MEDIA | 1,80-2,00 (tollerata 1,75-2,10) | singola o doppia | 1X2, GG/NG, Over/Under 2,5, multigol, combo, chance mix, gruppi di risultati |
| 🔴 HARD | 3,00 o più | colpo | sfavorita, pareggio, combo esito + gol, risultato esatto, multiesito, marcatore, marcatore + esito, cartellini, handicap |
| ⚡ EXTRA | quota alta, di solito 11-20 | solo per partite adatte | GG 1° tempo + GG 2° tempo, con le due gambe separate come appoggio |

Regole di scelta:
- Per ogni livello va confrontata almeno un'alternativa tra combo, chance mix, risultati, marcatori e cartellini. Vince quella con percentuale e valore migliori.
- Se in una fascia non c'è nulla di sensato, si sceglie l'esito più vicino e si spiega in una riga.
- **Combo sulla stessa partita:** le quote non si moltiplicano perché gli esiti sono correlati. Si usa la quota combo reale, oppure una quota indicativa da far verificare.
- **Chance mix ("A oppure B"):** probabilità = P(A) + P(B) − P(A e B), con la parte in comune calcolata dallo scenario.
- **Risultati:** la probabilità di un gruppo o di un multiesito è la somma dei punteggi che contiene, presi dalla griglia di Poisson. Un risultato esatto singolo raramente supera il 12-14%, quindi è da HARD. Se la skill non conosce la composizione dei gruppi bookmaker, propone i punteggi e chiede all'utente di verificarli.

### 3.8 Il pronostico EXTRA (GG 1T + GG 2T)
- **Definizione:** entrambe le squadre segnano nel primo tempo e di nuovo entrambe nel secondo, quindi almeno 4 gol.
- **Stima:**
  1. si dividono i gol attesi tra i due tempi, con i dati reali per tempo oppure con la ripartizione media di circa 45% / 55%;
  2. per ogni tempo, P(GG) = P(casa segna) × P(ospite segna);
  3. l'EXTRA è circa il prodotto dei due tempi, con una piccola correzione verso l'alto.
- **Soglia:** l'EXTRA si propone solo se la stima arriva almeno al 5-6%, contro un 2-3% tipico. In una giornata intera vale solo per le 2-3 partite migliori. Se nessuna partita è adatta, la skill lo dice.
- **Presentazione:** sempre anche come frequenza in parole, per esempio "circa 1 volta su 15".

### 3.9 Quote
- **Fonti, in ordine di preferenza:** quote date dall'utente, quote trovate online (bookmaker o altro bookmaker), quote **indicative** calcolate come 1 / probabilità stimata.
- **Etichetta obbligatoria** su ogni quota: bookmaker, altro bookmaker, indicativa.
- **Senza quote reali:** gli esiti vengono scelti per fascia di probabilità, così le quote indicative cadono nella fascia giusta:

  | Livello | Probabilità stimata |
  |---|---|
  | SICURA | 74-80% |
  | MEDIA | 48-57% |
  | HARD | 33% o meno |

- **Screenshot:** se una quota non è leggibile, la skill la chiede invece di indovinarla.

### 3.10 Probabilità e valore
Per ogni pronostico la skill riporta:
- probabilità stimata;
- probabilità implicita (1 / quota);
- **valore** = probabilità stimata × quota − 1.

Il valore è un'**informazione, non un filtro**: il pronostico viene dato comunque. Se il valore è chiaramente negativo, la skill lo segnala in mezza riga e, se esiste, propone un'alternativa nella stessa fascia. "SICURA" è il nome della fascia, non una garanzia: accanto c'è sempre la percentuale.

---

## 4. Formato della risposta

### Per ogni partita
1. Intestazione: partita, giornata, data e ora.
2. **Quadro:** 4-6 righe con i numeri e la fonte tra parentesi.
3. **Scenario**, percentuali di base e risultati più probabili.
4. **Tabella:** livello, pronostico, quota con etichetta, probabilità, valore.
5. **Un blocco per ogni pronostico**, con:
   - **Analisi** tracciabile: dato con fonte → cosa implica → effetto sulla stima → percentuale → frequenza in parole;
   - **Rischio:** il fattore che più potrebbe smentirla.

   Per combo e HARD il ragionamento è mostrato a passi, per esempio "Napoli vince 55%; se vince, Under 2,5 circa 55%; quindi circa 31%".

### Principi di scrittura ("analisi certificata")
- Ogni percentuale ha una catena di ragionamento visibile e contestabile.
- Niente frasi generiche ("squadra in forma"): sempre il numero che le dimostra.
- Dati verificati, dati non verificati e giudizi di Claude sono sempre distinti.
- Frasi brevi, niente formule, numeri arrotondati.

### Chiusura
- **Multipla delle sicure:** quota totale = prodotto delle quote, probabilità totale = prodotto delle probabilità. È indicata la sicura più debole da togliere per prima.
- **Singola o doppia** delle medie con il valore migliore.
- **HARD** più motivata.
- **Fonti** con data di consultazione.
- **Salvataggio** nello storico.

### Giornata intera
- **Apertura:** giornata, date, metodo e stato dei dati.
- **Tabellone:** una riga per partita con i tre livelli.
- **Schede complete** di tutte le partite, senza accorciare le minori.
- **Chiusura:**
  - classifica delle sicure dalla più solida alla più debole;
  - varianti della multipla con le migliori 3, 4 e 5, ciascuna con quota e probabilità;
  - le 2-3 medie migliori;
  - le 2 hard più motivate;
  - le partite da evitare, con il motivo;
  - l'elenco degli EXTRA.
- **Formato:** se la risposta è troppo lunga, le schede vanno in un documento a parte e in chat restano tabellone e chiusura.

---

## 5. Cosa la skill non fa (per scelta)

- **Nessun limite su budget, puntate o numero di giocate.** Una prima versione li prevedeva (puntata fissa, tetti settimanali e mensili, "NO BET" obbligatorio); l'utente ha chiesto di toglierli.
- **Nessuna scommessa piazzata**, nessun accesso al bookmaker.
- **Nessuna promessa di vincita.**
- **Nessun paternalismo.** Il tono è da analista a scommettitore esperto.

---

## 6. Gli script

### `scripts/valore.py`
- **Uso:**
  - `valore.py 1,85 58` per un singolo pronostico;
  - `valore.py --combo 1,30:80 1,28:82 1,35:77` per una multipla su partite diverse.
- **Output:** quota (o quota totale), probabilità implicita, probabilità stimata (anche "circa N volte su 10"), quota equa (1 / probabilità), valore.
- **Formato numeri:** accetta virgola o punto decimale.
- **Limite:** la multipla assume eventi indipendenti, quindi vale solo per partite diverse.

### `scripts/revisione.py`
- **Uso:** `revisione.py file.csv --oggi AAAA-MM-GG`.
- **Input:** CSV con separatore `;`, `,` o tab.
  - Colonne base: data, partita, mercato, esito, quota, prob_stimata, puntata, risultato (V / P / A), profitto.
  - Colonne facoltative: livello, campionato, giornata, tipo_quota, risultato_finale.
- **Output:**
  - **Riepilogo:** pronostici registrati, conclusi, annullati, in attesa; percentuale indovinati. Se ci sono puntate, anche puntato, profitto e ROI; se il profitto è vuoto lo calcola da quota e puntata.
  - **Indovinati per livello** (SICURA / MEDIA / HARD / EXTRA), confrontati con la probabilità media stimata.
  - **Rendimento per fascia di quota:** <1,50, 1,50-1,75, 1,75-2,10, 2,10-3,00, 3,00+.
  - **Calibrazione:** per fasce di probabilità stimata di 10 punti, stima media contro frequenza reale.
  - **Periodo corrente:** settimana e mese.
  - **Dati da verificare:** risultati registrati su date future (esclusi dai conti) e righe duplicate.
- **Avvertenza automatica:** con meno di 100 pronostici conclusi segnala che i risultati dipendono molto dal caso.

---

## 7. Storico e verifica di fine giornata

### Salvataggio
A ogni analisi tutti i pronostici (SICURA, MEDIA, HARD, EXTRA) vengono aggiunti a `storico-pronostici.csv`, una riga per pronostico:

```
data;campionato;giornata;partita;livello;mercato;esito;quota;tipo_quota;prob_stimata;risultato_finale;risultato;puntata;profitto
```

- Esito e risultato finale restano vuoti fino alla verifica.
- Puntata e profitto li compila l'utente, solo per i pronostici giocati davvero.

### Verifica
**Quando:** su richiesta ("com'è andata la giornata?"), oppure in automatico all'inizio di ogni uso, se nello storico ci sono partite già giocate senza esito.

**Come:**
1. Recupera con fonte: punteggio finale e del primo tempo, marcatori con minuto, cartellini se servono.
2. Giudica ogni pronostico con le regole del suo mercato: per l'EXTRA servono i gol per tempo; per i marcatori sono esclusi gli autogol. Se manca un dato necessario, la riga resta aperta: non si segna a intuito.
3. Aggiorna il file.

**Resoconto:**
- tabella partita per partita con ✅ / ❌;
- riepilogo per livello confrontato con la probabilità stimata, per esempio "SICURE 7/10 = 70%, stimate al 77%";
- esito della multipla consigliata;
- per ogni errore, se è sfortuna entro la probabilità dichiarata o un errore di analisi, e cosa cambiare;
- andamento cumulato con `revisione.py`.

**Limite:** la verifica non parte da sola a fine giornata. Avviene quando la skill viene usata, salvo un'attività pianificata impostata a parte.

---

## 8. Come è stata testata

**Metodo:**
- 5 giri di test, rifacendo il giro dopo ogni modifica.
- Ogni prova è stata eseguita da un agente separato, con la skill e senza (baseline).
- Le risposte sono state valutate contro criteri verificabili (asserzioni).
- Data simulata dei test: 11-12 novembre 2026, durante la sosta per le nazionali; partite della 12ª giornata.

**Risultati dell'ultima versione (giro 5):**

| Test | Con skill | Senza skill |
|---|---|---|
| Giornata intera di Serie A (10 partite) | 8/9 | 3/9 |
| Tre partite con quote del bookmaker date | 8/8 | 4/8 |
| Verifica di fine giornata su uno storico di 12 pronostici | 5/5 | 2/5 |
| **Totale** | **96%** | **41%** |

Giri precedenti, su versioni intermedie: 77% → 100% → 92% → 100% con la skill, contro un 40-66% senza.

**Avvertenze sui test, da considerare nella revisione:**
- **Valutazione non indipendente:** le asserzioni le ha scritte e valutate lo stesso Claude che ha scritto la skill. Non c'è stata una valutazione cieca né indipendente.
- **Pochi test:** 3-4 casi per giro, una sola esecuzione per caso. Nessuna misura della variabilità tra un'esecuzione e l'altra.
- **Baseline riutilizzate:** alcune risposte senza skill vengono da giri precedenti, con la stessa domanda.
- **Nessuna verifica predittiva:** nessun test misura se i pronostici sono giusti, perché le partite analizzate non erano ancora state giocate. I test misurano struttura, rigore, coerenza dei conti e rispetto delle regole, non l'accuratezza.
- **Storico di verifica di esempio:** le partite dell'11ª giornata usate nello storico di prova sono state controllate con risultati reali trovati sul web, ma i pronostici dello storico erano inventati per il test.
- **Esecuzioni interrotte:** la prova della giornata intera del giro 5 si è interrotta due volte per i limiti di utilizzo ed è stata ripresa. I tempi di quella prova non sono stati registrati.

**Costi osservati:**
- 3 partite: circa 140-160 mila token, 4-5 minuti.
- Giornata intera: circa 190 mila token, circa 10 minuti.
- La skill costa in media il 20-60% di token in più della baseline e richiede da 1,5 a 3 volte il tempo.

---

## 9. Criticità e limiti noti

### Dati
- **Connettore fuori uso:** il connettore TheStatsAPI risponde "chiave revocata". Senza, mancano xG, gol per tempo, tiri e minuti dei giocatori, statistiche precise casa/trasferta. Tutto viene dalla ricerca web, con qualità variabile delle fonti.
- **Quote di prova:** non sono mai state trovate online nei test. Senza le quote incollate dall'utente, quasi tutte le quote sono indicative e il valore non è calcolabile.
- **Tempistica:** a 7-10 giorni dalla partita mancano formazioni, squalifiche e arbitri. Marcatori e cartellini di fatto non sono utilizzabili prima di giovedì o venerdì.

### Modello
- **Poisson su poche giornate:** è un modello semplice basato su 11-15 giornate. Sottovaluta le grandi squadre in crisi e non tiene conto della rosa. Un esempio dai test: Napoli vincente stimato al 45%, contro il 69% implicito nella quota. La regola "a metà strada" del controllo con il mercato è una correzione empirica, non un metodo validato.
- **Correlazioni approssimate:** nelle combo e nell'EXTRA sono gestite a stima, per esempio la "piccola correzione verso l'alto".
- **Margine non sempre tolto:** il margine del bookmaker viene tolto sull'1X2, ma sugli altri mercati non c'è una procedura standard.
- **Metodo non fissato:** è dichiarato da Claude volta per volta. Due esecuzioni possono usare parametri diversi, per esempio quanto tirare i numeri verso la media.

### Struttura
- **Fasce di quota rigide:** possono costringere a scegliere esiti con valore negativo pur di riempire la fascia. La skill lo segnala, ma il pronostico lo dà comunque.
- **Calibrazione inutile all'inizio:** serve un centinaio di pronostici verificati perché i numeri per fascia dicano qualcosa.
- **Nessun apprendimento automatico:** l'analisi degli errori è testuale e la skill non corregge da sola i propri parametri.
- **Storico locale:** è un CSV nella cartella di lavoro. Se si cambia cartella o sessione, va riportato a mano.

### Uso
- La skill non contiene limiti di spesa né riferimenti al gioco responsabile, per scelta dell'utente.

---

## 10. Domande utili per la revisione

1. Il metodo (Poisson + regressione verso la media + correzioni dichiarate) va fissato nella skill con parametri precisi, per avere risultati riproducibili?
2. Il controllo con il mercato "a metà strada oltre i 10 punti" è sensato, oppure meglio un modello che usa le quote come punto di partenza e i dati come correzione?
3. Le fasce di quota fisse per livello sono il criterio giusto, o è meglio scegliere per valore atteso entro una fascia più ampia?
4. Come gestire meglio le correlazioni nelle combo sulla stessa partita e nell'EXTRA?
5. Quali fonti dati gratuite e affidabili per xG, gol per tempo, cartellini per arbitro e titolarità andrebbero indicate esplicitamente?
6. Come rendere la verifica di fine giornata e la calibrazione uno strumento che migliora davvero le stime nel tempo?
7. Il formato è troppo lungo per l'uso reale, specie per la giornata intera?
