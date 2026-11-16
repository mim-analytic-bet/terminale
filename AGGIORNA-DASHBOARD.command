#!/bin/bash
cd "$(dirname "$0")"
./scripts/aggiorna_tutto.sh
ESITO=$?
if [ "$ESITO" -eq 0 ]; then tail -15 dati/aggiornamento.log; fi
if [ "$ESITO" -ne 0 ]; then exit "$ESITO"; fi
read -p "Premi invio per chiudere"
