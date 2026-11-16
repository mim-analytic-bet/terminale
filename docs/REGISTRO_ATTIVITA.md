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
