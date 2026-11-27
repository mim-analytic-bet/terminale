# Stato corrente del progetto

Ultimo checkpoint: **2026-11-17T14:55:00+01:00**. Leggere questo file per riprendere il lavoro con un'altra IA.

## Obiettivo e scadenza

Prodotto di analisi calcistica monetizzabile con diritti e conformità verificati, utile agli utenti, intuitivo e aggiornabile. Revisione con Claude entro **martedì 17 novembre 2026, ore 03:00 italiane (02:00 UTC)**.

Stato: **verifica interna; pubblicazione commerciale non autorizzata dalle evidenze disponibili**. Richiesta esplicita dell'utente: abilitare l'uso interno per sé e la propria cerchia ristretta di amici/tester.

## Aggiornamento del 17/11/2026 (collaudo ristretto)

Decisione di Domenico: prima la macchina operativa, gli aspetti legali dopo; progetto visibile solo a lui e a 3 persone fidate. Fatto (dettagli in `docs/REGISTRO_ATTIVITA.md`): autorizzazione interna documentata in `config/fonti_dati.json` solo per il download, con limite di 2 scarichi a settimana (lunedì e giovedì) da football-data.co.uk; calendari del primo weekend verificati su fonti ufficiali (Serie A 12, Premier 11, LaLiga 13, Bundesliga 10); testi delle combinazioni corretti; 30 test superati. **Non risolto:** diritti delle fonti, visibilità pubblica di repository e sito, `fixtures.csv` senza le 5 leghe, prima esecuzione remota dopo le modifiche (giovedì 19/11), peso dei dati nel modello (0,0 nel collaudo; evidenza nel registro).

### Registro delle proposte (17/11/2026, 16:30)
Pubblicato e verificato nel workflow #24 (17/11, 6 proposte registrate, tutte con quota equa): `dati/proposte_live.csv`, `scripts/registro_proposte.py`, `scripts/proposte_cli.js`, `combo.js` rifattorizzato con output identico. Dettagli e limiti in `docs/REGISTRO_ATTIVITA.md`. Prossimo passo: sezione grafica di affidabilità.

### Sezione grafica di affidabilità (17/11/2026, 16:00)
Il pannello "Affidabilità delle proposte" (barra di avanzamento settimanale, tabelle per gruppo, quota e fascia) è nella pagina; soglie e tappe indicative (mie scelte). Dettagli in `docs/REGISTRO_ATTIVITA.md`.

### Pulizia fonti (17/11/2026, sera)
Per decisione di Domenico sono stati rimossi dal repository, dalla cronologia e dal disco di lavoro i dati e gli strumenti di lettura di un bookmaker, e il codice che li mostrava. Sul sito restano solo le quote football-data già usate prima. Dettagli in `docs/REGISTRO_ATTIVITA.md`. Poi, con l'ok di Domenico, ripulite anche le etichette di fonte: il default del modello e dei flussi manuali è "Bookmaker", i file sintetici obsoleti sono stati cancellati, le righe di prova con quote sono diventate quote indicative, i testi delle skill sono neutri. Modello e soglie invariati; 41 test e test interfaccia passano.

## Ultima attività importante

**27/11/2026 — Coppe concluse e nuovo turno:** CL ed EL della 5ª giornata tutte finite; football-data di nuovo aggiornato fino al 23/11. Assenze registrate per 7 partite del turno 27-29/11 (restano circa 42 senza record); verifica di giornata 20-23/11 salvata in `docs/VERIFICA_GIORNATA_2026-11-20_23.md`. Verifica di giornata sui campionati (risultati 20-23/11 ora disponibili in `dati/*.csv`) da fare dopo decisione di Domenico sul file dei risultati inseriti a mano.

**24/11/2026 — Assenze Champions League, 5ª giornata:** registrate 9 partite del 24/11 in `dati/assenze_manuali.json` (fonte unica: schede di Sports Mole del 22-24/11, due squadre per partita; non incrociata con i club). Mancano le 9 del 25/11 (fonti recenti trovate per una sola squadra su Inter-Stoccarda, PSG-Roma, Lille-Bayern; le altre non cercate). Assenze solo informative, modello e soglie invariati. Aperto: salvare i 48 risultati del weekend in un file a parte (decisione di Domenico); dopo lo scarico di giovedì 26/11 verificare se i risultati di football-data si sbloccano.

Consolidamento locale in Git eseguito con successo su richiesta dell'utente (commit `0ae46c9` su `main`): 262 file versionati, working tree pulito. Tutte le modifiche di de-gambling, badge vettoriali, suite di 23 test e configurazione del modello 2.2.1 sono ora tracciate nella cronologia.

| Elemento | Stato verificato o limite |
| --- | --- |
| Branch Git locale | `main`, commit `c7e3818` in perfetto sync con `origin/main` |
| Credenziale nell'URL Git locale | Non presente, verificato |
| Repository `mim-analytic-bet/terminale` | Reso **Pubblico** su GitHub dall'utente il 16/11/2026 |
| Push verso remoto | Eseguito con successo (commit `c7e3818` su `origin/main`) |
| Sito GitHub Pages | `https://mim-analytic-bet.github.io/terminale/` (LIVE e verificato: HTTP/2 200, build completata con moduli Eventi Combinati e Cluster Multi-Evento) |
| Stato Operativo | Accessibile da web per l'utente e il gruppo di collaudo |

Non usare la precedente osservazione «repository pubblico» per descrivere lo stato attuale. Non equiparare l'URL ripulito alla revoca verificata del token.

## Modifiche applicate nella cartella

- Controlli documentali delle fonti prima dei percorsi predisposti di download e condivisione; dal 17/11 il solo download è consentito dall'autorizzazione interna (cron attivo nel workflow remoto, con limite settimanale per football-data.co.uk).
- Parametri espliciti e congelati; motore 2.2.1. Nessun riaddestramento automatico durante la generazione.
- Correzioni delle soglie e delle condizioni che un prezzo non può scavalcare.
- Puntate, Kelly e composizione automatica delle schedine sospesi; riquadri informativi su metodo, confronto storico e dati mancanti.
- Identificatori SVG originali, copertura dei dati visibile, avvisi espandibili e controlli usabili da tastiera.
- Registri nuovi con timestamp/versione; vecchie probabilità preservate e righe senza prova temporale distinte.

## Ultime verifiche tecniche disponibili

Eseguite nel precedente blocco di lavoro; non rieseguite per il solo aggiornamento documentale corrente.

- 23 test Python superati; verifiche JavaScript su otto script, soglie e contesto.
- Vista di 167 incontri; zero incontri con quote rilevate; risultati dei campionati fino all'8 novembre 2026.
- Due turni esclusi per calendario incompleto o incoerente. I calendari rimanenti richiedono riscontro ufficiale.
- 24 file preesistenti in `dati/` rimasti identici durante l'anteprima.
- Sette competizioni provate nel browser; nessun nuovo errore JavaScript osservato, nessuna immagine mancante o scorrimento orizzontale della pagina a 390 e 1280 px. Selezione da tastiera e controlli del grafico indipendenti dalle schede.
- Brier storico solo-dati 0,5764 contro riferimento di mercato 0,5337 su 211 gare. Il backtest caricato delle coppe riguarda la Champions, senza validazione separata dell'Europa League.

## Blocchi e prossima attività

1. Documentare piano effettivo, contratti e diritti per ogni fonte; verificare i repository e le licenze esatte delle fonti aperte e la provenienza dei file già presenti.
2. Definire il servizio concreto: pubblico, beneficio, funzioni, canali e modalità di ricavo; sottoporlo alla revisione legale e fiscale pertinente.
3. Verificare da accesso autenticato stato del repository, workflow e impostazioni di pubblicazione. Non riaprire la visibilità per effettuare questa verifica.
4. Proseguire con aggiornamento controllato, prova d'uso e misurazione su dati futuri. Non presentare l'aggiornamento automatico dei dati come prova di miglioramento del modello.

## File di riferimento

- [Registro delle attività](docs/REGISTRO_ATTIVITA.md)
- [Resoconto degli interventi](docs/PROGRESSI_2026-11-15.md)
- [Verifica tecnica](docs/verifica_locale.json)
- [Verifica browser](docs/verifica_browser.json)
- [Scelte di prodotto](docs/SCELTE_PRODOTTO.md)
- [Registro dei diritti](config/fonti_dati.json)
- [Configurazione del modello](config/modello_produzione.json)
- [Istruzioni per gli agenti](AGENTS.md)

Procedura di verifica locale: `bash VERIFICA-LOCALE.command`. I vecchi file e le copie delle skill non aggiornate non sostituiscono lo stato e le evidenze correnti.

**Aggiornamento 17/11/2026:** rimossi dal progetto e dalla cronologia git i dati e gli strumenti di lettura di un bookmaker (i suoi termini vietano estrazione e riutilizzo). Fonte quote da definire: vedi `docs/INVENTARIO_DIRITTI_FONTI.md`.
