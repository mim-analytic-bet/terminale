#!/bin/bash
# Ricostruisce la vista dai soli file locali, senza download né scrittura dei registri.
cd "$(dirname "$0")" || exit 1
python3 -B -m unittest discover -s tests || exit 1
if command -v node >/dev/null; then node tests/test_interfaccia.js || exit 1; fi
python3 -B scripts/aggiorna_dashboard.py --anteprima || exit 1
python3 -B scripts/verifica_snapshot.py --output docs/verifica_locale.json
