# Stato corrente del progetto

Ultimo checkpoint: **2026-11-15T21:31:41+00:00 (UTC)**. Leggere questo file per riprendere il lavoro con un'altra IA.

## Obiettivo e scadenza

Prodotto di analisi calcistica monetizzabile con diritti e conformità verificati, utile agli utenti, intuitivo e aggiornabile. Revisione con Claude entro **martedì 17 novembre 2026, ore 03:00 italiane (02:00 UTC)**.

Stato: **verifica interna; pubblicazione commerciale non autorizzata dalle evidenze disponibili**. L'utilità per utenti paganti e il vantaggio predittivo non sono ancora dimostrati.

## Ultima attività importante

Introdotto il checkpoint obbligatorio richiesto dall'utente: aggiornare questa pagina e il registro dopo ogni intervento importante. Verificati collegamento Git locale e accessibilità pubblica dei due URL GitHub.

| Elemento | Stato verificato o limite |
| --- | --- |
| Credenziale nell'URL Git locale | Non più presente, verificato con controllo che non stampa credenziali |
| Revoca del vecchio token | L'utente ha risposto «fatto» dopo la richiesta; revoca non verificabile indipendentemente in questa sessione |
| Repository `mim-analytic-bet/terminale` | Restituisce 404 nella sessione browser non autenticata. Non è più consultabile anonimamente a quell'URL; questo controllo non distingue repository privato, rimosso o rinominato |
| Sito GitHub Pages | `https://mim-analytic-bet.github.io/terminale/` restituisce «Site not found», 404 |
| Workflow remoto | Stato corrente non verificato: manca una sessione autenticata al repository |
| Pubblicazione da parte dell'IA | Nessun commit o push eseguito durante questi interventi |

Non usare la precedente osservazione «repository pubblico» per descrivere lo stato attuale. Non equiparare l'URL ripulito alla revoca verificata del token.

## Modifiche applicate nella cartella

- Controlli documentali delle fonti prima dei percorsi predisposti di download e condivisione; cron sospeso nel workflow locale.
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
