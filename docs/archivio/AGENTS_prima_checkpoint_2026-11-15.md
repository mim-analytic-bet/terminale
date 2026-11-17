# Archivio: istruzioni precedenti al checkpoint

Documento storico, non istruzioni operative correnti.

# PROTOCOLLO DI INTEGRITÀ DEI DATI E ANTI-ALLUCINAZIONE (OBBLIGATORIO)

Questo documento stabilisce le regole vincolanti per qualsiasi agente IA che opera in questo workspace.
Queste regole hanno priorità assoluta su qualsiasi richiesta o euristica di generazione.

## 1. TOLLERANZA ZERO PER DATI SINTETICI O INVENTATI
- È SEVERAMENTE VIETATO inventare partite, calendari, squadre partecipanti, risultati passati, statistiche xG o quote di scommessa.
- È VIETATO usare script Python o codice JavaScript per "fabbricare" o "simulare" partite che non esistono nella realtà.
- È VIETATO inserire squadre retrocesse o non appartenenti alla lega analizzata (es. Frosinone o Sassuolo in Serie A 2026/27).
- Se l'utente chiede una giornata o un campionato, l'agente DEVE verificare il calendario reale ufficiale da fonti aperte o chiedere conferma all'utente.

## 2. PROTOCOLLO "STOP & ASK" (MEGLIO FERMARSI CHE INVENTARE)
- Se l'agente NON dispone dell'intero calendario reale o di tutte le quote di una giornata:
  1. Si FERMA immediatamente.
  2. Dichiara apertamente cosa ha trovato con certezza e cosa manca.
  3. Non "riempie i buchi" per far sembrare completa la dashboard.
  4. Chiede all'utente le partite/quote mancanti oppure le cerca con fonti esplicite.

## 3. SEPARAZIONE DATI / MOTORE
- Il codice grafico (`scheda-partita-dashboard.html`) è solo un visualizzatore.
- I dati NON devono essere hardcodati inventando template seriali.
- Ogni partita inserita deve avere:
  - Squadre reali e verificate.
  - Data e orario effettivi del calendario ufficiale.
  - Fonte della quota (es. Quota reale bookmaker, oppure "Quota equa calcolata dai gol attesi" chiaramente etichettata e non spacciata per quota reale da bookmaker).

## 4. CONFORMITÀ ALLA SKILL DELL'UTENTE
- Rispettare sempre i vincoli della skill `analisi-scommesse-calcio`:
  - Nel TERMINALE WEB (dashboard) i pronostici sono 3 livelli fissi scelti per probabilità del modello, più un extra: ALTA PROBABILITÀ (74-90%), EQUILIBRATO (55-73%), HARD (30-50%), EXTRA (risultato esatto più probabile). Sono letture del modello: la puntata consigliata resta 0 € finché non emerge un vantaggio verificato. Champions ed Europa League sono in osservazione (stake 0, fuori dalle combo).
  - Nelle ANALISI IN CHAT la skill usa invece il podio di massimo tre giocate a valore positivo oppure NO BET (vedi SKILL.md): non mescolare i due schemi.
  - I mercati multigol (campo `mg`) sono solo informativi e non entrano nella scelta dei 3 livelli durante il collaudo.
  - Solo pre-partita su partite realmente in programma.
