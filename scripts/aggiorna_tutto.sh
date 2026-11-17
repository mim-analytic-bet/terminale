#!/bin/bash
# Scarica i dati aggiornati e rigenera la dashboard. Pensato per girare da solo (launchd) o a mano.
cd "$(dirname "$0")/.." || exit 1
PY=$(command -v python3 || echo /usr/bin/python3)
# Nessun download finché piano e impieghi delle fonti non sono documentati.
"$PY" scripts/verifica_fonti.py --operazione download --fonte football_data_uk --fonte football_data_org --fonte api_ninjas --fonte openfootball || exit 2
LOG="dati/aggiornamento.log"; mkdir -p dati
M=$(date +%m); Y=$(date +%y); if [ "$M" -ge 7 ]; then S="${Y}$((Y+1))"; else S="$((Y-1))${Y}"; fi
echo "=== $(date '+%d/%m/%Y %H:%M') stagione $S ===" >> "$LOG"
ERR=0
scarica() { # url destinazione
  T=$(mktemp); if curl -sSfL --max-time 60 -o "$T" "$1" 2>>"$LOG" && head -c 8 "$T" | grep -q "Div" && [ "$(wc -l < "$T")" -gt 5 ]; then mv "$T" "$2"; echo "ok $2" >> "$LOG"; else rm -f "$T"; echo "FALLITO $2" >> "$LOG"; ERR=$((ERR+1)); fi; }
# football-data.co.uk: al massimo 2 scarichi a settimana (lun e gio), come da config/fonti_dati.json; altrimenti si usano i file gia' presenti
if "$PY" scripts/limite_download.py --fonte football_data_uk >> "$LOG" 2>&1; then
  ERR0=$ERR
  for L in I1 E0 SP1 D1 F1; do scarica "https://www.football-data.co.uk/mmz4281/$S/$L.csv" "dati/$L.csv"; done
  scarica "https://www.football-data.co.uk/fixtures.csv" "dati/fixtures.csv"
  [ "$ERR" -eq "$ERR0" ] && "$PY" scripts/limite_download.py --registra football_data_uk >> "$LOG" 2>&1
else
  echo "football-data.co.uk: nessuno scarico in questa esecuzione; uso i file gia' presenti" >> "$LOG"
fi
"$PY" scripts/assenze.py >> "$LOG" 2>&1 || true
"$PY" scripts/scarica_coppe.py >> "$LOG" 2>&1 || true
"$PY" scripts/calendario_aperto.py >> "$LOG" 2>&1 || true   # calendario aperto openfootball (solo abbinamenti)
# Gli identificatori grafici sono generati localmente: nessun download di stemmi.
OUT=$("$PY" scripts/aggiorna_dashboard.py 2>&1); RC=$?
echo "$OUT" >> "$LOG"
if [ $RC -ne 0 ]; then MSG="Errore nella generazione della dashboard (vedi dati/aggiornamento.log)"
elif [ $ERR -gt 0 ]; then MSG="$ERR download falliti: dashboard aggiornata con i dati precedenti"
elif echo "$OUT" | grep -q "^AVVISO"; then MSG="Dashboard aggiornata. $(echo "$OUT" | grep -c '^AVVISO') avvisi (calendario da completare)"
else MSG=""; fi
[ -n "$MSG" ] && osascript -e "display notification \"$MSG\" with title \"Terminale Quantitativo\"" 2>/dev/null
exit $RC
