# Quant Terminal PRO – guida per un'altra IA (Gemini o simili)

Dashboard di analisi calcio con SOLI dati reali: Serie A, Premier, LaLiga, Bundesliga, Ligue 1. Utente: Domenico (italiano). Riferimento primario automatico Bet365 (confrontabile e giocabile su Eurobet o concessionari ADM), budget 100 €/mese. Rispondere sempre in italiano, senza assecondare: se un dato manca, dirlo.

Repo: https://github.com/mim-analytic-bet/terminale  ·  Sito: https://mim-analytic-bet.github.io/terminale/

## Come funziona
- `scripts/aggiorna_tutto.sh`: scarica i CSV di football-data.co.uk, esegue `scripts/assenze.py` (orari) e poi `scripts/aggiorna_dashboard.py`, che rigenera `scheda-partita-dashboard.html` (il sito online usa `index.html`, copia dello stesso file).
- GitHub Actions (`.github/workflows/aggiorna.yml`) lo esegue 3 volte al giorno e pubblica. Secret usato: `FOOTBALL_DATA_KEY` (football-data.org, gratuito). Dopo un push manuale, fare sempre `git fetch` + rebase: il bot committa su main.
- Modello Poisson/Dixon-Coles (`analisi-scommesse-calcio/scripts/modello.py`) con memoria (`dati/memoria_modello.json`) e track record (`dati/storico_live.csv`). Risultato dei test: il modello da solo NON batte il mercato, quindi la puntata consigliata è 0 € finché non emerge un edge. Non cambiare questa regola senza dati.
- `dati/calendario_openfootball.json` (scritto da `scripts/calendario_aperto.py` a ogni aggiornamento; fonte openfootball, CC0): abbinamenti di TUTTA la stagione per i 5 campionati. Il generatore li usa solo per completare le giornate future (max 2 per lega, `MAX_TURNI_APERTI`) con il solo abbinamento: giorno provvisorio, ora vuota, nota «data e orario provvisori». Non sovrascrive mai `calendario.json` né `fixtures.csv`. Le partite aggiunte SOLO da qui e senza quote NON entrano nel registro `storico_live.csv` (sarebbero previsioni senza ancora di mercato). Limiti verificati il 13/11/2026: giorno/ora di openfootball sono segnaposto per le giornate lontane e per Serie A giornata 12 divergono dal manuale su 5 partite su 10 (il generatore stampa le righe «CONFRONTO calendario»). Se i nomi squadra non si abbinano 1:1 ai CSV la lega viene saltata con un messaggio, mai abbinata a caso. Ligue 1: nomi openfootball non ancora verificati dal vivo.
- `dati/calendario.json`: giornate a mano (giorno/ora). Ogni lunedì l'utente lo aggiorna con le nuove giornate. Gli orari mancanti vengono completati da `dati/assenze.json` (scritto da `assenze.py`, solo orari confermati, status TIMED).

## Modifiche recenti
- Orari automatici da football-data.org (API-Football gratuito NON dà la stagione 2026/27, scartato).
- Assenze/squalifiche: NON esiste fonte gratuita automatica. Si inseriscono a mano in `dati/assenze_manuali.json`. Sono solo informative: non entrano nel calcolo. Se la partita non ha il record, la pagina mostra il banner rosso "Fattore di Rischio" (assenze non verificate). Se c'è, mostra il riquadro "Assenti e squalificati" per squadra.
- Box Focus Doppia (due partite quota 1,55–1,70) e TRI-BET (due partite 1,80–2,00 oppure singola ≥ 3,50); le quote sono "eque" (1/probabilità), non di Eurobet.

## Routine "giorno prima" (da fare per le partite del turno che inizia entro ~36 ore)
1. Leggere `dati/assenze.json` o `dati/calendario.json` per l'elenco delle partite e delle date.
2. Per ogni partita cercare sul web (fonti serie: siti dei club, Transfermarkt, Sofascore, Fantacalcio/Gazzetta per la Serie A, siti ufficiali delle leghe) infortunati e squalificati di entrambe le squadre. Non inventare: se una squadra non ha informazioni, lasciare la lista vuota SOLO se la fonte dice che non ci sono assenti; altrimenti NON creare il record per quella partita.
3. Aggiungere un record in `dati/assenze_manuali.json`, campo `partite`:
```json
{"casa":"Como","ospite":"Cagliari","giorno":"2026-11-21",
 "assenze":{"casa":[{"nome":"Cognome","tipo":"Missing Fixture","motivo":"Suspended"}],
            "ospite":[{"nome":"Cognome","tipo":"Questionable","motivo":"Knee Injury"}]},
 "controllato":"2026-11-20T09:00+00:00","fonte":"nome del sito"}
```
   `casa`/`ospite` come nel calendario (nomi football-data, es. "Man United"). `tipo`: "Missing Fixture" (assente/squalificato) o "Questionable" (in dubbio). Rimuovere i record di partite già giocate.
4. Verificare: `python3 scripts/aggiorna_dashboard.py` (deve finire con "Dashboard aggiornata") e controllare che nell'HTML compaia `"assenti": {`.
5. Pubblicare: `cp scheda-partita-dashboard.html index.html`, commit, `git fetch`, `git rebase`, `git push`.

## Regole
- Mai dati sintetici, mai quote inventate: se mancano, scriverlo.
- Non incollare né chiedere chiavi API in chat; stanno nei secret di GitHub.
- Il modello non va ritoccato per le assenze finché non ci sono ≥100 previsioni verificate.

## ATTENZIONE: non sovrascrivere il lavoro altrui
- Il repo viene modificato anche dal bot (3 aggiornamenti al giorno) e da altre IA. Prima di QUALSIASI modifica: `git pull --rebase`. Mai caricare copie locali vecchie di `scripts/`, `scheda-partita-dashboard.html`, `index.html`.
- Parti che non vanno rimosse: la chiamata a `scripts/assenze.py` in `scripts/aggiorna_tutto.sh`; le funzioni `assenze_per`/`testo_assenze` in `scripts/aggiorna_dashboard.py`; il riquadro "Assenti e squalificati" nell'HTML; il workflow `.github/workflows/aggiorna.yml` con il secret `FOOTBALL_DATA_KEY`.
- Dopo ogni modifica: `python3 scripts/aggiorna_dashboard.py` e controllare che finisca con "Dashboard aggiornata".

## Ruoli e cadenza (aggiornato)
- Normalmente il lavoro lo fa Claude, che ha accesso al repo e pubblica da solo. Questa guida serve se Claude non e' disponibile: in quel caso Domenico fa i passaggi su GitHub a mano.
- Se NON hai accesso al repo, non dire di aver aggiornato o pubblicato nulla. Consegna a Domenico solo il contenuto completo del file da modificare e le istruzioni per incollarlo (GitHub > file > matita > Commit changes), poi "Actions > Aggiorna dashboard > Run workflow". Non usare PUBBLICA-GITHUB.command (carica la copia locale vecchia e cancella il lavoro recente).
- Controlli assenze: giovedi' sera (partite di venerdi' e sabato) e sabato mattina (domenica e lunedi'). Il lunedi' si aggiorna `dati/calendario.json` con il nuovo turno e si tolgono le partite gia' giocate.
- In `assenze_manuali.json` restano solo partite future; il `controllato` e' la data/ora UTC reale del controllo.

## Modulo coppe europee (Champions League, modalità osservazione)
- `scripts/scarica_coppe.py` (football-data.org, stessa chiave `FOOTBALL_DATA_KEY`) scrive `dati/coppe/CL_live.json`; `scripts/coppe.py` + `coppe_modello.py` calcolano un modello **Elo europeo** (storico openfootball in `dati/coppe/storico_europa.csv`), correzione con la forma nel campionato nazionale, memoria in `dati/coppe/memoria_coppe.json`, log previsioni pre-partita in `dati/coppe/previsioni_CL.csv` e track record reale (Brier vs Elo puro vs frequenze).
- Il generatore aggiunge `DATA_PRO["champions"]` con `osservazione: true`: modello NON validato, puntata sempre 0 €, escluso da Doppia/TRI-BET/combo (lo script COMBO salta le chiavi con `osservazione`). Se mancano i dati live la voce sparisce dal menu.
- Non toccare né cancellare `memoria_coppe.json` e `previsioni_CL.csv`: sono la memoria del modello. - **Europa League** (aggiunta): stesso modello e stesse regole (osservazione, stake 0 €). Fonte: API Ninjas (`league=uel`, secret `API_NINJAS_KEY`, solo uso NON commerciale sul piano gratuito: passare al piano a pagamento prima di monetizzare). `scarica_coppe.py` converte il formato API Ninjas in quello di football-data.org e scrive `dati/coppe/EL_live.json`; `coppe.elabora(..., comp="el")` usa `previsioni_EL.csv` e `memoria_coppe_EL.json`. Formato risposta API Ninjas (campo `round`, giornata, risultato a 90') NON ancora verificato dal vivo: controllare gli avvisi del primo giro del bot. Lo storico openfootball di EL/Conference arriva solo al 2024-25.
- Conference, Mondiali, Europei, Nations League: non ancora implementati (nessuna fonte gratuita affidabile per la Conference).

## Stemmi delle coppe (regola: TUTTE le squadre devono avere uno stemma)
- Priorità: 1) PNG manuale `assets/loghi/<nome_squadra_slug>.png` (sempre vince), 2) stemma ufficiale scaricato da `scripts/scarica_stemmi.py` (URL `crest` di football-data.org per le squadre di Champions → `assets/loghi/coppe_*.png|svg`, indice in `dati/stemmi_coppe.json`), 3) distintivo PROVVISORIO con iniziali generato da `assicura_stemmi()` (`assets/loghi/prov_*.png`).
- Le voci `prov_`/`coppe_` vengono rivalutate a ogni giro: quando arriva lo stemma ufficiale sostituisce il provvisorio. L'avviso "Stemma PROVVISORIO" elenca le squadre da sistemare. Gli stemmi sono marchi dei club: uso personale OK, da verificare prima di monetizzare.

## Heatmap risultato esatto (aggiornata 13/11/2026)
- La heatmap NON ricalcola più una griglia propria (prima: 0-3 gol, rho -0.06, senza normalizzazione). Ora usa `m.heat`, generato da `heat()` in `aggiorna_dashboard.py` dalla STESSA matrice del modello (MAX_GOL=10, rho del modello, normalizzata).
- Le celle "4+" aggregano tutti i punteggi con 4 o più gol (per casa e/o ospite): la somma è sempre 100% e coerente con 1X2/Gol/Over. Il top-3 è calcolato sulla matrice completa.
- Non reintrodurre calcoli Poisson nel JS: se serve cambiare la griglia, modificare `heat()`.

## Mercati Multigol (aggiornati 13/11/2026)
- `multigol(g, d)` in `scripts/aggiorna_dashboard.py` calcola, dalla stessa matrice del modello (come la heatmap), il campo `mg` di ogni partita: Multigol Totale, Casa, Ospite, 1T, 2T e combo (1/X/2/1X/X2/12 e Gol/No Gol + Multigol totale). Riquadro "Mercati Multigol" in `renderizzaMultigol(m)` (HTML).
- 1T/2T: Poisson indipendenti per tempo, medie = gol attesi × quota di gol al 1T (storica della squadra, ridotta al 50% verso la media di lega 0.45; per le coppe solo media di lega). Approssimazione, non coerente al 100% con la matrice a tempo pieno.
- Inserimento nel catalogo decisionale con vincoli rigorosi concordati con Domenico:
  - `Multigol 1-4` e `Multigol 2-5` aggiunti a `CATALOGO` in `modello.py` insieme ai classici (1-2, 1-3, 2-3, 2-4, 3-5).
  - Funzione `seleziona_livelli(dq)` in `aggiorna_dashboard.py`: vincolo di massimo 1 solo multigol per partita tra i tre livelli (Alta Probabilità, Equilibrato, Hard), quota minima multigol >= 1.25 (probabilità <= 80%, scartando multigol iper-ampi), e gli altri due slot sempre garantiti su mercati tradizionali (1X2, U/O, Doppia Chance, Gol/NoGol).
  - Riferimento quote: Bet365 / media mercato (aggiornata via `fixtures.csv` di football-data.co.uk).
  - Precisazione (verifica di Claude, 13/11/2026 sera): il codice applica SOLO due vincoli, multigol ≤80% nel livello Alta e massimo 1 multigol per partita (se non esiste un'alternativa non multigol, il vincolo può non reggere). NON esiste una lista di multigol ammessi per livello: non scriverla nei documenti come se fosse implementata. Nei test, 94 partite su 148 hanno un multigol tra i livelli (spesso 2-5 o 1-4 in Equilibrato).
  - Quota mostrata nei livelli e nella schedina (slip), decisione di Domenico (13/11 sera): per evitare che l'utente studi una schedina con quote gonfiate o irrealistiche rispetto al banco reale, il campo `quota` mostra la QUOTA BANCO REALE (la quota reale Bet365 dal feed per i mercati presenti in fixtures.csv, oppure la quota stimata con aggio standard del 7,5% per multigol e mercati derivati, e aggio 15% sul risultato esatto). La quota equa pura (1/probabilità) resta tracciata nel campo analitico `qEqua` e nella descrizione. In questo modo la schedina calcola il moltiplicatore sul prezzo effettivo con cui l'utente scommette su Bet365 o Eurobet.
  - Riferimento quote, versione corretta il 13/11 sera: le quote usate per ANCORARE il modello (probabilità) sono, nell'ordine, Betfair Exchange, Pinnacle, media dei bookmaker, Bet365 solo se mancano le altre (margine dell'exchange ~0,8% contro ~5,5% di Bet365 nei dati di football-data). Le quote MOSTRATE come confronto sono quelle di Bet365 (`quote_bet365()` in `prepara_partita.py`), etichettate "prezzo di confronto, non Eurobet". Con `--rif-da` e senza `--q`, `d["quote"]` viene riempito con le quote Bet365 (tipo_quota "Bet365"): non sono quelle di Eurobet e vanno ricontrollate su Eurobet. Non testato su partite dei 5 campionati principali: oggi `dati/fixtures.csv` contiene solo leghe inglesi minori (sosta nazionali), l'effetto si vedrà dal prossimo turno.
  - Misura (sandbox, 13/11): con il catalogo esteso i livelli cambiano in 20 partite di campionato su 48 e 27 su 48 mostrano un multigol tra i livelli; le probabilità 1X2 dei campionati non cambiano. (Una cifra precedente di "76 probabilità cambiate" era sbagliata: veniva dalle coppe, vedi sotto.)
  - Anomalia RISOLTA (13/11 sera): le coppe davano numeri diversi a ogni esecuzione perché lo storico openfootball scrive 19 club in due modi (es. 'Juventus' e 'Juventus FC') e `abbina()` sceglieva a caso (ordine degli insiemi di stringhe). Correzioni in `scripts/coppe.py`: `unifica_storico()` (un solo rating per club) e `abbina()` deterministico (candidati ordinati). Verificato: 4 esecuzioni con semi diversi danno file identici. Le probabilità delle coppe sono cambiate (rating più completi, es. Galatasaray da 1396 a 1452); backtest 503 partite: Brier 0,5653 -> 0,5489 (parametri non ritarati). Nessuna previsione reale conclusa era stata registrata (le righe 'retro 0' sono tutte ancora da giocare e vengono riscritte fino al calcio d'inizio), quindi il track record live non è compromesso. Non ci sono confronti con le quote per le coppe.

## Stato del collaudo (aggiornato 13/11/2026 sera)
- Le modifiche ai multigol nel catalogo e al riferimento Bet365 (commit 7e8ce30, 65b1283) sono state tenute per decisione di Domenico a collaudo già iniziato. Il confronto con i pronostici precedenti non è più valido: il collaudo è ripartito da questo momento. La nuova data di fine collaudo va fissata con Domenico.
- Da ora fino a nuovo avviso: nessun'altra modifica a modello, catalogo, soglie o riferimento quote senza decisione esplicita di Domenico.
