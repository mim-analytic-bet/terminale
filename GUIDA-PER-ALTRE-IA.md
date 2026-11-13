# Quant Terminal PRO – guida per un'altra IA (Gemini o simili)

Dashboard di analisi calcio con SOLI dati reali: Serie A, Premier, LaLiga, Bundesliga, Ligue 1. Utente: Domenico (italiano). Riferimento primario automatico Bet365 (confrontabile e giocabile su Eurobet o concessionari ADM), budget 100 €/mese. Rispondere sempre in italiano, senza assecondare: se un dato manca, dirlo.

Repo: https://github.com/mim-analytic-bet/terminale  ·  Sito: https://mim-analytic-bet.github.io/terminale/

## Come funziona
- `scripts/aggiorna_tutto.sh`: scarica i CSV di football-data.co.uk, esegue `scripts/assenze.py` (orari) e poi `scripts/aggiorna_dashboard.py`, che rigenera `scheda-partita-dashboard.html` (il sito online usa `index.html`, copia dello stesso file).
- GitHub Actions (`.github/workflows/aggiorna.yml`) lo esegue 3 volte al giorno e pubblica. Secret usato: `FOOTBALL_DATA_KEY` (football-data.org, gratuito). Dopo un push manuale, fare sempre `git fetch` + rebase: il bot committa su main.
- Modello Poisson/Dixon-Coles (`analisi-scommesse-calcio/scripts/modello.py`) con memoria (`dati/memoria_modello.json`) e track record (`dati/storico_live.csv`). Risultato dei test: il modello da solo NON batte il mercato, quindi la puntata consigliata è 0 € finché non emerge un edge. Non cambiare questa regola senza dati.
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
