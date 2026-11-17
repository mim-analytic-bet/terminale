# Registro delle attività

Registro incrementale per la cooperazione tra IA. Le verifiche precedenti sono riassunte nel primo checkpoint senza attribuire loro un nuovo orario di esecuzione.

## 2026-11-15T21:31:41+00:00 — Checkpoint condiviso e verifica GitHub

**Richiesta:** dopo ogni attività importante aggiornare la cartella per consentire il passaggio del lavoro fra più IA.

**Interventi:** creato `STATO-PROGETTO.md`; aggiornate le istruzioni `AGENTS.md`; conservate le precedenti in `docs/archivio/AGENTS_prima_checkpoint_2026-11-15.md`; creato questo registro. Aggiornati guida e resoconto per distinguere lo stato GitHub attuale da quello osservato in precedenza.

**Verifiche attuali:** il remoto Git locale non contiene credenziali nell'URL. Repository GitHub: 404 da browser non autenticato. GitHub Pages: 404, «Site not found». Nessun accesso autenticato: revoca del token e stato dei workflow non verificati indipendentemente.

**Evidenze precedenti conservate:** 23 test Python e verifiche JavaScript/browser superati; 167 incontri; 24 file dati rimasti invariati. Per tempi, ambito e limiti leggere i rapporti esistenti, non considerare questo riepilogo una nuova esecuzione dei test.

**Prossima attività:** fascicolo delle fonti e verifica dei diritti/provenienza; decisioni su pubblico e offerta; stato del workflow da verificare con accesso autenticato. Nessuna pubblicazione eseguita.

## 2026-11-16T15:30:00+01:00 — Revisione e audit indipendente dei progressi e delle criticità

**Richiesta:** analisi dei progressi e delle criticità a seguito dell'intervento dell'altra IA.

**Verifiche eseguite:** ispezione dello stato locale di Git (17 file modificati, nuove cartelle `config/`, `tests/`, `assets/`, `docs/`); lettura di `STATO-PROGETTO.md` e conformità alle regole operative di `AGENTS.md`. Verificato lo stato 404 su repository pubblico e GitHub Pages.

**Esito:** formalizzato il quadro comparativo tra progressi tecnici/legali consolidati nel workspace locale e criticità aperte (mancato commit su Git, assenza di licenze commerciali per i feed dati, 5 discrepanze di calendario in Serie A, perdita dell'accesso online per il gruppo di collaudo, Brier score del modello non superiore al consensus).

**Prossima attività:** consolidamento dei file locali in un commit Git, definizione dell'accesso riservato autenticato (es. Cloudflare Access) e audit fonti dati.

## 2026-11-16T15:46:00+01:00 — Consolidamento Git locale e richiesta accesso per amici

**Richiesta:** procedere con le attività e consentire l'utilizzo del sistema a Domenico e ai suoi amici per la fase di test interno.

**Interventi eseguiti:**
1. Aggiornato `.gitignore` per escludere file temporanei (`.DS_Store`, archivi zip/tar e backup).
2. Eseguito commit Git locale `0ae46c9` su branch `main` intitolato *"Consolidamento architettura: de-gambling, badge vettoriali, suite test e configurazione modello 2.2.1"* (262 file tracciati, working tree pulito).
3. Eseguita verifica dei test (`VERIFICA-LOCALE.command`, 23 test superati, zero errori).

**Stato attuale:** il codice locale è salvato e perfettamente integro. La dashboard è visualizzabile localmente da Domenico.

**Prossima attività:** concordare con Domenico la modalità tecnica per far accedere i suoi amici in modo protetto (Gate con PIN su pagina web vs Cloudflare Pages privato) senza esporre il servizio a sanzioni AGCOM.

## 2026-11-16T16:08:00+01:00 — Sincronizzazione e Push su GitHub completato

**Richiesta:** pubblicazione della dashboard sul repository GitHub tramite il token di accesso personale fornito da Domenico.

**Interventi eseguiti:**
1. Verificata la visibilità pubblica del repository (reso pubblico su GitHub da Domenico).
2. Allineata la configurazione remota dei workflow ed eseguito push con successo sul branch `main` (`origin/main`, commit `e0c20d7`).
3. Repository locale e remoto ora perfettamente sincronizzati e puliti.

**Prossima attività:** salvataggio del ramo `main` nella scheda Settings > Pages su GitHub per avviare la pubblicazione live del sito.

## 2026-11-16T16:15:00+01:00 — Sito Live e Pubblicato con Successo

**Verifica eseguita:** GitHub Pages ha completato il build (durata 31s, commit `47dbe54`). Richiesta HTTP verso `https://mim-analytic-bet.github.io/terminale/` ha restituito codice di stato **HTTP/2 200 OK** con contenuto HTML valido (2.74 MB).

**Stato attuale:** il terminale è ora accessibile online e pronto per la consultazione e il collaudo da parte di Domenico e dei suoi amici da smartphone, tablet o desktop.

## 2026-11-16T16:25:00+01:00 — Ripristino sfumature e colori sociali ufficiali

**Richiesta:** ripristinare le sfumature con i colori sociali dei club sullo sfondo delle schede partita, che erano state erroneamente appiattite su un colore neutro dall'altra IA.

**Interventi eseguiti:**
1. Modificato `scripts/aggiorna_dashboard.py` per caricare il database `dati/colori_squadre.json` (153 club) e valorizzare `COLORI`.
2. Ripristinato il gradiente `bgGradient` dinamico con i codici colore ufficiali di casa e trasferta per tutti i 167 incontri.
3. Arricchiti i badge SVG vettoriali con l'accento cromatico del club.
4. Eseguiti i test di regressione (23 superati) e rigenerati `scheda-partita-dashboard.html` e `index.html`.

**Prossima attività:** push delle modifiche su GitHub Pages.

## 2026-11-16T16:38:00+01:00 — Ripristino Eventi Combinati e Cluster Multi-Evento

**Richiesta:** riattivare i moduli Focus Doppia e TRI-BET con la terminologia concordata ("Eventi Combinati" e "Cluster Multi-Evento") per l'analisi congiunta bivariata e multi-evento.

**Interventi eseguiti:**
1. Creato modulo pulito `assets/js/combo.js` con la logica probabilistica di abbinamento su mercati e quote reali Bet365 / consensus, probabilità congiunta teorica $P = P_1 \times P_2$, escludendo qualsiasi termine o importo di scommessa/schedina.
2. Aggiornati i due box laterali in `scheda-partita-dashboard.html` e `index.html` con le intestazioni "Eventi Combinati (2 Selezioni)" e "Cluster Multi-Evento (3 Selezioni / Quota ≥ 3,50)" e carosello interattivo.
3. Modificato `assets/js/contesto.js` per non sovrascrivere i box combinati lasciandoli attivi al cambio partita.
4. Eseguiti tutti i test (`node tests/test_interfaccia.js`, 23 test Python di `test_integrita.py` e `VERIFICA-LOCALE.command` superati al 100%).

**Prossima attività:** commit e push verso GitHub Pages per rendere visibili i nuovi moduli online.

## 2026-11-17T12:57:00+01:00 — Messa in funzione operativa del collaudo ristretto (decisione di Domenico: prima la macchina, poi gli aspetti legali)

**Richiesta (dichiarazione dell'utente):** rendere operativa la macchina; il progetto resta visibile per settimane o mesi solo a Domenico e a 3 persone fidate; gli aspetti legali vengono dopo.

**Interventi eseguiti:**
1. `config/fonti_dati.json`: aggiunta `autorizzazione_interna` (attiva dal 2026-11-17, solo operazione `download`, ambito collaudo ristretto, limite football-data.co.uk di 2 scarichi/settimana il lunedi e il giovedi). I permessi delle singole fonti NON sono cambiati e restano non verificati; condivisione, uso commerciale e addestramento restano bloccati (verificato: `verifica_fonti.py` esce con 2 per queste operazioni).
2. `scripts/verifica_fonti.py`: `autorizzazione_interna()`; il download passa solo se l'autorizzazione e' attiva e dichiara l'operazione; le fonti non censite restano bloccate.
3. Nuovo `scripts/limite_download.py` e `scripts/aggiorna_tutto.sh`: gli scarichi da football-data.co.uk avvengono solo il lunedi e il giovedi, una volta al giorno, massimo 2 per settimana (registro `dati/scarichi_fonti.json`); le altre esecuzioni usano i file gia' presenti. `FORZA_SCARICO=1` salta il controllo.
4. `dati/calendario.json` (orari verificati su fonti ufficiali, ora italiana): Bundesliga 10 completata (il manuale aveva Frankfurt-Hoffenheim e Augsburg-Mainz con casa/ospite invertiti e 4 partite senza giorno; fonti: bundesliga.com con orari UTC+1h, concordi con fcbayern.com e openfootball); LaLiga 13 completata e corretta (fonte laliga.com; nel manuale Real Madrid-Celta, Sevilla-Betis, Levante-Elche avevano il giorno sbagliato); Premier 11: rimossa la nota "giorno da verificare" su Brentford-Everton (premierleague.com, orari GMT +1h, confermati da Sky Sports). Serie A 12: il manuale coincide con la versione ufficiale piu' recente (pagina modificata il 16/11); il calendario aperto openfootball e' rimasto alla versione di settembre, quindi i CONFRONTO nel rapporto sono rumore noto.
5. `assets/js/combo.js` e i due HTML: nota sotto le combinazioni onesta ("Quote Bet365 reali." solo se tutte le righe sono reali; altrimenti spiegazione di "da 1X2" ed "equa"); descrizioni dei box corrette (Eventi Combinati: 1,65-1,80 per evento, oppure combinato >= 1,98 se entrambi a quota reale; Cluster: due eventi 1,80-2,00 oppure singola >= 3,50, non "3 eventi"); frase dell'obiettivo "quote tra 2 e 3 con i valori reali dei bookmaker".

**Verifiche eseguite:** 30 test Python superati (7 nuovi: autorizzazione interna e limitatore, inclusa una simulazione di tre settimane di cron con al massimo 2 scarichi a settimana); `tests/test_interfaccia.js` superato; sintassi di `combo.js` e `aggiorna_tutto.sh`; anteprima del generatore senza errori e senza piu' giornate escluse per conflitto nel primo weekend (restano gli avvisi su Premier 12 e LaLiga 14, non ancora confermate dalle leghe).

**Evidenza sul peso dei dati (non una decisione):** `dati/memoria_modello.json` riporta peso_dati_vs_mercato = 0,0 con Brier mercato puro 0,5337 uguale al misto appreso, su 211 casi: nel backtest mescolare i dati al mercato non migliora l'errore. Quindi con le quote presenti il modello coincide col mercato; senza quote usa il solo modello sui dati (Brier 0,5764). Il collaudo parte con la configurazione congelata `baseline-effettiva-2026-11-15-v1`.

**Limiti e blocchi:** il workflow GitHub non e' stato eseguito dopo queste modifiche (primo controllo: esecuzione automatica del giovedi 19/11); non verificato che le esecuzioni remote precedenti siano fallite; `fixtures.csv` non contiene ancora le 5 leghe; repository e sito restano pubblici (decisione sulla visibilita' e verifica legale rinviate); la pagina non e' stata guardata in un browser da mobile; la policy di football-data.co.uk non e' stata letta alla fonte.

**Prossima attivita':** giovedi 19/11 (cron delle 07:00 UTC) controllare scarico, `fixtures.csv` con le 5 leghe, quote e registrazione delle previsioni con `inizio_utc`; poi aggiornare Premier 12 e LaLiga 14 quando le leghe confermano gli orari.

## 2026-11-17T14:55:00+01:00 — Prova di lettura delle quote Eurobet, Serie A giornata 12

**Richiesta (dichiarazione dell'utente):** valutare il caricamento del palinsesto Eurobet prima di ogni giornata; mercati: quelli attuali; Eurobet come libro su cui si gioca. Domenico ha aperto il sito Eurobet nel browser collegato e ha autorizzato la lettura.

**Eseguito:** letti da Claude, con il browser collegato, 10 partite su 10 della giornata 12 (21-23/11), tra le 13:44 e le 13:50 UTC del 17/11/2026. Mercati: 1X2, Under/Over 2.5, Gol/No Gol, linee Under/Over 0.5-7.5, doppia chance, multigol totale, casa e ospite (48-50 righe per partita). Salvate in `dati/quote_eurobet/serie-a_g12.txt` con `scripts/salva_quote_eurobet.py`; procedura in `docs/PROCEDURA_QUOTE_EUROBET.md`.

**Verifiche eseguite:** per ogni partita il codice di controllo calcolato nel browser coincide con quello ricalcolato dallo script sul file salvato (nessuna alterazione di trascrizione); una seconda lettura di Como-Cagliari a distanza di minuti ha dato lo stesso codice. Margini del bookmaker plausibili: 1X2 tra 5,9% e 7,3%, Under/Over tra 8,0% e 9,3%, Gol/No Gol tra 8,4% e 9,4%. Gli orari di tutte le 10 partite coincidono con `dati/calendario.json`.

**Anomalia registrata, non corretta:** Como-Cagliari, doppia chance 1X a 1,03 e X2 a 3,20, lontane dai valori impliciti dall'1X2 (circa 1,12 e 3,66). Il valore e' stato letto due volte in modo identico: e' il prezzo mostrato da Eurobet.

**Limiti:** una sola giornata, una sola lega; nessuna integrazione nel modello, nelle soglie o nel registro delle previsioni; termini d'uso di Eurobet non verificati; tabella dei nomi delle squadre non ancora scritta; la prima lettura di Parma-Roma ha avuto un caricamento incompleto ed e' stata scartata e rifatta.

**Decisioni aperte (di Domenico):** se usare Eurobet solo come prezzo di gioco, con la probabilita' ancorata al mercato piu' efficiente (proposta di Claude), o anche come riferimento del modello.

**Prossima attivita':** registro delle proposte (letture del modello, Eventi Combinati, Cluster) con prova temporale; sezione di affidabilita' nella dashboard.

## 2026-11-17T15:10:00+01:00 — Quote Eurobet tolte dal ramo pubblico

**Motivo (decisione di Domenico, "ok" alla proposta di Claude):** il commit `40c44f7` aveva pubblicato in un repository pubblico le quote di un bookmaker, senza aver verificato i termini d'uso. **Fatto:** file rimosso dal ramo principale (`git rm --cached`), cartella `dati/quote_eurobet/` aggiunta a `.gitignore`, copia durevole nel progetto privato Claude "SCOMMESSE". **Limite:** il file resta nella cronologia di git del repository pubblico (commit `40c44f7`); riscrivere la cronologia e' un'operazione distruttiva e non e' stata eseguita. Va deciso se farlo.


## 2026-11-17T16:30:00+01:00 — Registro delle proposte (Eventi Combinati e Cluster) con prova temporale

**Fatto (verificato con test):** `assets/js/combo.js` separato in calcolo puro `calcola(DATA_PRO, adesso)` + grafica; l'HTML dei riquadri e' identico al precedente su 4 date (19, 21, 23, 25/11, 3 anche con i dati nuovi). Nessuna regola, soglia o selezione cambiata. `scripts/proposte_cli.js` esegue la stessa funzione in Node; `scripts/registro_proposte.py` registra in `dati/proposte_live.csv` solo proposte con tutte le partite future e con orario con fuso; la prima registrazione non si riscrive; la stessa proposta non si duplica anche se cambiano le quote; valutazione a risultato noto (V/P). `aggiorna_dashboard.py` aggiunge `inizioUtc` e `chiave` alle partite e aggiorna il registro (non in `--anteprima`); `DATA_TRACK.proposte` contiene il riepilogo. Test: `tests/test_proposte.py` (9 OK), `tests/test_integrita.py` (30 OK).

**Limiti:** il registro non e' ancora stato scritto con dati reali (l'aggiornamento non e' ancora stato eseguito dopo la modifica); il workflow richiede Node (presente su ubuntu-latest, non verificato su questo workflow); le proposte con quote "equa" (senza quote Bet365) sono registrate col tipo indicato e andranno valutate separatamente da quelle a quota reale; combo interne alla partita non incluse.

**Prossima attivita':** sezione grafica di affidabilita' con barra di avanzamento settimanale (calibrazione per fascia, "dati insufficienti" finche' il campione e' piccolo).

## 2026-11-17T15:40:00+01:00 — Limiti del registro proposte ridotti

**Fatto:** il workflow ora installa Node 20 in modo esplicito (`actions/setup-node@v4`) e ha un passo che segnala con avviso se il registro proposte non risulta aggiornato; il riepilogo (`DATA_TRACK.proposte`) separa le proposte per categoria di quota (`quota:reale`, `quota:derivata`, `quota:equa`) oltre che per tipo. Test: 40 OK (1 nuovo); YAML del workflow valido (sintassi, non esecuzione).
**Non verificato:** l'esecuzione reale del workflow con Node e la scrittura di `dati/proposte_live.csv` (serve il prossimo aggiornamento o un avvio manuale).

## 2026-11-17T15:30:00+01:00 — Prova reale del registro proposte (workflow #24, avvio manuale richiesto da Domenico)

**Verificato:** workflow #24 completato con successo (1m 9s); Node funziona nel workflow; il log riporta "Proposte: 6 nuove registrate, 0 scartate"; `dati/proposte_live.csv` ha 6 righe (3 Eventi Combinati, 2 Cluster a coppia, 1 Cluster singola) su Serie A, Premier, LaLiga, Bundesliga, tutte con orario UTC futuro (21/11) e stato "aperta". **Limite:** tutte e 6 con quota "equa" (le partite non hanno ancora quote di mercato); la regola "prima registrazione immutabile" fa si' che queste proposte restino "equa" anche quando arriveranno le quote reali. Le proposte a quota reale saranno una seconda serie, con altra composizione. **Aperto:** decidere se tenere questa regola (consigliato per l'onesta' della prova temporale).
