# Quant Terminal: stato del lavoro al 15 novembre 2026

Scadenza di revisione: martedì 17 novembre 2026, ore 03:00 italiane (02:00 UTC). Questo documento descrive modifiche locali verificabili. Non attesta la conformità legale, l'avvenuta pubblicazione o un'attività autonoma in background.

## Risultato di questa fase

Il progetto dispone ora di una versione interna più trasparente, con controlli sulle fonti, parametri espliciti e verifiche ripetibili. **Non è ancora pronto per essere venduto o condiviso come prodotto autorizzato.**

| Obiettivo | Cosa è stato realizzato | Cosa manca |
| --- | --- | --- |
| Monetizzazione lecita | Registro dei diritti; blocchi nei comandi di download, pubblicazione e installazione del timer; sospensione locale del cron GitHub | Contratti delle fonti, forma concreta del servizio, verifica normativa professionale, assetto fiscale e contrattuale, protezione dell'accesso |
| Utilità | Metodo, dati mancanti e confronto storico consultabili per la partita scelta; quote teoriche distinte da prezzi rilevati | Pubblico prioritario e problema verificato con utenti; disponibilità di dati autorizzati e aggiornati; prova di disponibilità a pagare |
| Interfaccia | Stato dei dati leggibile, avvisi espandibili, identificatori SVG originali, controlli accessibili da tastiera, navigazione mobile coerente | Revisione completa della densità, accessibilità, dipendenze esterne e prestazioni; prova con utenti |
| Aggiornamento e miglioramento | Configurazione congelata; nuovi registri con timestamp/versione; vecchie previsioni preservate; verifiche automatiche locali | Acquisizione da fonti autorizzate, osservazione su eventi futuri, valutazione separata dei nuovi modelli e rilascio con possibilità di ripristino |

## Evidenze disponibili

- Vista rigenerata dai file locali: **167 incontri**, dei quali 77 nei campionati nazionali e 90 nelle coppe. Nessuna quota rilevata disponibile nel campione corrente.
- I risultati dei cinque campionati arrivano all'**8 novembre 2026**. La data di generazione della pagina non prova un nuovo download.
- LaLiga, turno 13: escluso per date mancanti. Bundesliga, turno 10: escluso per date mancanti e club ripetuti dopo la fusione dei calendari. Non sono stati inventati nuovi abbinamenti o orari per riempire i vuoti.
- Restano divergenze tra calendari caricati; il controllo strutturale non certifica il calendario ufficiale. L'avviso è visibile nella pagina.
- Backtest riprodotto sui file locali: 211 gare, Brier del modello solo-dati **0,5764**, riferimento di mercato **0,5337**; un valore più basso indica minore errore probabilistico. La simulazione storica di 258 selezioni produce **−26,3%**. Non è un rendimento reale né una validazione dell'attuale configurazione completa.
- Registro nazionale precedente: 58 righe, nessuna valutata; le 58 righe non hanno la nuova prova temporale. Non sono stati inventati timestamp per sanarle.
- Coppe: il backtest caricato riguarda 503 incontri di Champions League. L'Europa League usava lo stesso riferimento: la vista ora segnala che manca una validazione specifica per l'Europa League.
- Tutti i **24 file già presenti in `dati/`** sono rimasti identici byte per byte durante la rigenerazione in anteprima. Impronte dei registri principali in `verifica_locale.json`.

L'autenticità e la provenienza di ogni singolo risultato, calendario e osservazione non sono state certificate. I numeri sopra descrivono il contenuto dei file disponibili e l'esecuzione del codice su quei file.

## Modifiche tecniche

1. `config/fonti_dati.json` documenta cinque gruppi di fonti. Tutti i permessi restano non verificati finché non vengono raccolte evidenze del piano e degli usi autorizzati. `scripts/verifica_fonti.py` blocca i percorsi predisposti; non sostituisce la verifica dei contratti.
2. Rimosso il cron dal workflow locale di aggiornamento. I downloader hanno controlli iniziali. Il download automatico degli stemmi è stato tolto dal flusso principale. Il timer già eventualmente installato sul Mac incontra il nuovo blocco locale; non è stato disinstallato.
3. Configurazione `baseline-effettiva-2026-11-15-v1`: motore 2.2.1, peso dati 0, fiducia gol 1, peso forma coppe 0,25. Riproduce i parametri effettivi precedenti, che differivano dalla descrizione 20/80; non rappresenta un miglioramento dimostrato. Senza un riferimento quote il modello usa il percorso disponibile sui dati storici. L'ottimizzazione automatica durante la generazione è sospesa.
4. Corretto il percorso in cui un prezzo alto poteva scavalcare dati insufficienti, assenza di riferimento completo, disaccordo o anomalia. Allineato il calcolo delle soglie tra motore e interfaccia, inclusi i passaggi di fascia e l'arrotondamento per eccesso.
5. Sospesi importi, Kelly, composizione e selezione automatica di schedine multi-evento. I riquadri mostrano ora metodo, qualità dei dati e confronto storico. Rinominare un modulo o inserire un disclaimer, da solo, non risolve la qualificazione giuridica del servizio.
6. La vista usa identificatori testuali originali in `assets/badges/`; non richiama più il CDN degli stemmi. I vecchi file grafici non sono stati cancellati dalla cartella, dalla cronologia o dalle copie remote. Il riutilizzo dei nomi dei club e gli altri asset richiedono comunque verifica contestuale.
7. Nuove righe del registro nazionale: timestamp con fuso, orario di inizio, versione e configurazione; nessuna nuova registrazione dopo l'inizio o senza orario. Le previsioni esistenti non vengono sovrascritte. Le vecchie righe restano distinte nella valutazione.
8. Coppe: nuove previsioni con timestamp e versione, preservazione delle probabilità già registrate, rifiuto di registri con ID duplicati. La prova dell'ordine temporale non prova l'autenticità della fonte.
9. Pagina con copertura dei risultati e avvisi espandibili; rimossa la barra fissa che occupava molto spazio. Corretto l'errore di caricamento dei loghi e il formato percentuale del backtest delle coppe. I gol attesi sono presentati come stime, senza attribuirli a un feed xG osservato. Il diagramma degli esiti e le schede a diverse probabilità hanno ora selezioni indipendenti; nessuna rotazione automatica.
10. `GUIDA-PER-ALTRE-IA.md` distingue lo stato attuale dalle indicazioni storiche superate. Le copie delle skill e gli archivi precedenti richiedono ancora un riallineamento: non vanno usati per ripristinare automaticamente moduli o affermazioni obsolete.

## Verifiche e riproduzione

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/aggiorna_dashboard.py --anteprima
node tests/test_interfaccia.js
python3 -B scripts/verifica_snapshot.py --output docs/verifica_locale.json
```

Oppure: `bash VERIFICA-LOCALE.command`. Non scarica dati e non scrive nei registri delle previsioni; ricostruisce gli HTML, gli identificatori originali e il rapporto di verifica.

- 23 test Python superati: condizioni del motore, soglie, normalizzazione, configurazione, autorizzazioni documentali, calendario e conservazione dei registri.
- Verifiche JavaScript: soglie, sintassi degli script, identità dei due HTML, indisponibilità dei percorsi di puntata, copertura dei risultati indipendente dalla rigenerazione, contesto delle competizioni.
- I comandi di download, pubblicazione e installazione dell'automazione terminano con codice 2 prima delle rispettive operazioni, dato lo stato corrente dei diritti.
- `verifica_snapshot.py`: nessun errore tecnico nei controlli implementati; impedimenti alla condivisione e all'uso commerciale presenti. L'assenza di errori tecnici non certifica il prodotto.
- Verifica browser locale su desktop e telefono: selettori delle sette competizioni, immagini e navigazione da tastiera; nessun nuovo errore JavaScript osservato e nessuno scorrimento orizzontale della pagina a 390 e 1280 px. Grafico e schede sono indipendenti. Gli elementi a scorrimento, come la lista incontri e le tabelle, mantengono lo scorrimento interno. Evidenze circoscritte in `verifica_browser.json`.

Il workflow `Verifica locale senza rete dati` è stato preparato per un'esecuzione manuale su GitHub. Non è stato caricato né eseguito sul remoto.

## Aggiornamento GitHub successivo all'intervento dell'utente

Checkpoint: 2026-11-15T21:31:41+00:00. L'utente ha risposto «fatto» dopo la richiesta di intervento su GitHub.

- Verificato: il collegamento Git locale non contiene più credenziali nell'URL.
- Verificato: il repository `mim-analytic-bet/terminale` restituisce 404 da browser non autenticato; non è consultabile anonimamente a quell'URL. Non si può distinguere con questo solo controllo tra repository privato, rimosso o rinominato.
- Verificato: `https://mim-analytic-bet.github.io/terminale/` restituisce 404, «Site not found».
- Non verificato indipendentemente: revoca del vecchio token e stato del workflow remoto. La sessione browser non è autenticata.
- Nessun commit o push eseguito dall'IA. La precedente osservazione di repository pubblico descriveva lo stato prima dell'intervento dell'utente.

La cartella dispone ora di `STATO-PROGETTO.md` e `docs/REGISTRO_ATTIVITA.md`. Per esplicita richiesta dell'utente, ogni intervento importante deve essere seguito dal loro aggiornamento.

## Ordine delle prossime attività fino alla revisione

| Priorità | Consegna concreta | Criterio di completamento |
| --- | --- | --- |
| P0 | Revoca credenziale, controllo accessi e arresto del vecchio aggiornamento remoto | Evidenza delle impostazioni effettive; vecchio URL e pubblicazioni verificati |
| P0 | Fascicolo delle fonti e provenienza dei dati | Piano/contratto, licenza, attribuzione, limiti di riuso, pubblicazione, vendita e addestramento documentati per ogni fonte |
| P0 | Definizione del servizio da sottoporre al professionista | Pubblico, funzioni, messaggi, canali, prezzi, mercati geografici e percorso di acquisto concreti; valutazione legale riferita a quel servizio |
| P1 | Flusso di analisi più breve | Un utente individua partita, probabilità, origine e limiti senza spiegazione esterna; prova osservata con almeno tre persone, senza inventare riscontri |
| P1 | Prototipo dell'offerta | Problema e benefici verificabili; almeno un test esplicito di disponibilità a pagare; niente promesse di vincita o di accuratezza non dimostrata |
| P1 | Aggiornamento controllato | Fonte autorizzata, data di acquisizione registrata, errori visibili, salvataggio atomico e ripristino della versione valida precedente |
| P2 | Valutazione dei modelli candidati | Campione futuro separato, confronto con baseline, calibrazione e incertezza; nessuna promozione automatica del modello ritarato sullo stesso campione |
| Finale | Pacchetto di revisione per Claude | Questo documento, rapporto JSON, codice locale, risultati delle verifiche, decisioni aperte e distinzione tra modifiche locali e remote |

Non è possibile fissare responsabilmente alla scadenza una certificazione di liceità o una prestazione predittiva futura: dipendono da documenti, decisioni e osservazioni che il codice non può produrre da solo.

## Riferimenti da conservare nel fascicolo

- Football-data.co.uk: https://football-data.co.uk/contact.php
- Football-data.org: https://www.football-data.org/about
- API Ninjas: https://api-ninjas.com/tos
- Openfootball: documentare i repository e le licenze esatte, non solo il profilo https://github.com/openfootball
- AGCOM: verificare il servizio concreto e la comunicazione rispetto alla disciplina sulla pubblicità del gioco; la qualificazione non dipende solo dai nomi dei moduli o dal disclaimer.
