# Verifica giornata 20-23/11/2026 (campionati)

Calcolata il 27/11/2026 da Claude, solo in lettura: risultati dai CSV football-data in `dati/` (non più trascritti a mano), probabilità prima della partita da `dati/storico_live.csv` (ultima registrazione per partita). Nessun file di registro modificato; modello e soglie invariati.

## Sintesi (48 partite, 5 campionati)

| Misura | Modello | Mercato* |
|---|---|---|
| Brier a 3 esiti | 0,569 | 0,587 |
| Log-loss | 0,960 | 0,987 |
| Esito più probabile azzeccato | 29/48 (60%) | n.d. |

| Campionato | N | Brier modello | Brier mercato* | Esito azzeccato |
|---|---|---|---|---|
| Serie A | 10 | 0,486 | 0,426 | 8/10 |
| Premier | 10 | 0,619 | 0,706 | 5/10 |
| LaLiga | 10 | 0,585 | 0,564 | 5/10 |
| Bundesliga | 9 | 0,531 | 0,554 | 7/9 |
| Ligue 1 | 9 | 0,628 | 0,694 | 4/9 |

*Mercato = quote medie (o Bet365 se mancano) dei CSV, senza margine. Non è verificato se siano quote di apertura o di chiusura.

## Cosa si può e non si può dire

- Sul totale il modello è appena sotto il mercato (0,569 contro 0,587), ma con 48 partite la differenza è dentro il rumore: non dimostra un vantaggio.
- Favoriti: tra 45% e 60% di probabilità hanno vinto 62% (attesa 52%); sotto il 45% 50% (attesa 40%); sopra il 60% 70% (attesa 70%). Tutte e tre le fasce sono nei limiti di un campione piccolo, ma le prime due vanno nel senso di probabilità un po' prudenti.
- Over 2,5: media prevista 58%, frequenza reale 50%; Brier 0,248, praticamente uguale a quello di una previsione fissa al 50% (0,25). Nessuna abilità dimostrata su questo mercato.
- Proposte valutate: 7 vinte su 21 (33%), probabilità media attesa 32,6%. In linea, ma 20 su 22 hanno quota equa (1/p), non reale: il ROI non è calcolabile.
- Registrazioni: 35 partite del 13/11 (v2.2) e 13 del 17/11 (v2.2.1); versioni diverse nello stesso campione.

## Dettaglio partite

| Lega | Partita | P1 | PX | P2 | Esito | Risultato |
|---|---|---|---|---|---|---|
| serie-a | Como-Cagliari | 0.57 | 0.25 | 0.18 | 1 | 2-0 |
| serie-a | Lazio-Lecce | 0.65 | 0.21 | 0.14 | 1 | 3-0 |
| serie-a | Parma-Roma | 0.09 | 0.17 | 0.75 | 2 | 1-5 |
| serie-a | Napoli-Torino | 0.50 | 0.27 | 0.23 | 1 | 1-0 |
| serie-a | Juventus-Venezia | 0.60 | 0.25 | 0.15 | 1 | 4-0 |
| serie-a | Bologna-Udinese | 0.62 | 0.21 | 0.16 | X | 1-1 |
| serie-a | Sassuolo-Genoa | 0.33 | 0.28 | 0.39 | 2 | 0-2 |
| serie-a | Milan-Frosinone | 0.48 | 0.23 | 0.28 | 1 | 5-1 |
| serie-a | Atalanta-Inter | 0.14 | 0.18 | 0.67 | X | 4-4 |
| serie-a | Monza-Fiorentina | 0.41 | 0.24 | 0.35 | 1 | 3-0 |
| premier | Man City-Fulham | 0.59 | 0.23 | 0.18 | X | 1-1 |
| premier | Aston Villa-Sunderland | 0.46 | 0.25 | 0.29 | X | 0-0 |
| premier | Bournemouth-Nott'm Forest | 0.49 | 0.27 | 0.24 | 1 | 2-0 |
| premier | Chelsea-Leeds | 0.41 | 0.29 | 0.30 | 2 | 1-4 |
| premier | Coventry-Crystal Palace | 0.48 | 0.25 | 0.27 | 1 | 3-2 |
| premier | Tottenham-Ipswich | 0.53 | 0.25 | 0.22 | 1 | 2-0 |
| premier | Newcastle-Arsenal | 0.20 | 0.28 | 0.52 | X | 2-2 |
| premier | Hull-Brighton | 0.22 | 0.26 | 0.52 | 1 | 2-0 |
| premier | Liverpool-Man United | 0.56 | 0.23 | 0.21 | 1 | 4-0 |
| premier | Brentford-Everton | 0.46 | 0.28 | 0.26 | 1 | 4-0 |
| liga | Ath Bilbao-Espanol | 0.52 | 0.29 | 0.19 | 2 | 0-1 |
| liga | Alaves-La Coruna | 0.37 | 0.31 | 0.32 | 1 | 3-1 |
| liga | Vallecano-Valencia | 0.53 | 0.26 | 0.20 | 2 | 0-1 |
| liga | Sevilla-Betis | 0.38 | 0.27 | 0.35 | X | 1-1 |
| liga | Real Madrid-Celta | 0.68 | 0.22 | 0.10 | 1 | 2-1 |
| liga | Barcelona-Villarreal | 0.71 | 0.16 | 0.13 | 1 | 3-2 |
| liga | Santander-Sociedad | 0.34 | 0.23 | 0.43 | 1 | 3-2 |
| liga | Osasuna-Malaga | 0.53 | 0.26 | 0.21 | 1 | 1-0 |
| liga | Getafe-Ath Madrid | 0.17 | 0.29 | 0.54 | 2 | 0-3 |
| liga | Levante-Elche | 0.45 | 0.26 | 0.29 | X | 1-1 |
| bundesliga | Bayern Munich-FC Koln | 0.87 | 0.09 | 0.04 | X | 1-1 |
| bundesliga | Ein Frankfurt-Hoffenheim | 0.49 | 0.23 | 0.28 | 1 | 1-0 |
| bundesliga | Elversberg-Freiburg | 0.34 | 0.26 | 0.40 | 2 | 0-1 |
| bundesliga | Leverkusen-Paderborn | 0.66 | 0.21 | 0.14 | 1 | 4-0 |
| bundesliga | M'gladbach-Dortmund | 0.34 | 0.26 | 0.40 | 2 | 0-1 |
| bundesliga | Union Berlin-RB Leipzig | 0.19 | 0.21 | 0.60 | 2 | 1-5 |
| bundesliga | Schalke 04-Stuttgart | 0.39 | 0.27 | 0.34 | X | 0-0 |
| bundesliga | Augsburg-Mainz | 0.52 | 0.20 | 0.28 | 1 | 3-1 |
| bundesliga | Werder Bremen-Hamburg | 0.69 | 0.19 | 0.12 | 1 | 4-0 |
| ligue1 | Troyes-Le Havre | 0.44 | 0.27 | 0.29 | 1 | 3-1 |
| ligue1 | Nice-Paris SG | 0.23 | 0.23 | 0.54 | 2 | 2-3 |
| ligue1 | Lens-Toulouse | 0.41 | 0.26 | 0.34 | X | 1-1 |
| ligue1 | Lille-Lyon | 0.37 | 0.31 | 0.33 | 2 | 0-1 |
| ligue1 | Monaco-Auxerre | 0.56 | 0.24 | 0.20 | X | 1-1 |
| ligue1 | Strasbourg-Brest | 0.28 | 0.24 | 0.49 | 2 | 0-1 |
| ligue1 | Paris FC-Angers | 0.68 | 0.20 | 0.12 | 1 | 4-0 |
| ligue1 | Lorient-Rennes | 0.49 | 0.26 | 0.26 | X | 1-1 |
| ligue1 | Marseille-Le Mans | 0.58 | 0.20 | 0.21 | 2 | 2-3 |
