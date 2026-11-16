#!/bin/bash
# Doppio clic per inviare tutti gli aggiornamenti al sito GitHub Pages:
# https://mim-analytic-bet.github.io/terminale/
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR" || exit 1
if ! python3 scripts/verifica_fonti.py --operazione condivisione; then
  echo "⚠️  AVVISO FONTI: diritti commerciali non documentati."
  echo "   Procedo in modalità COLLAUDO PRIVATO E INTERNO tra amici (non commerciale)."
  echo
fi

echo "========================================================"
echo "   PUBBLICAZIONE SITO: mim-analytic-bet.github.io/terminale"
echo "========================================================"
echo

# 1. Assicura che index.html sia allineato alla dashboard
cp scheda-partita-dashboard.html index.html

# 2. Aggiunge i file web necessari per GitHub Pages
git add -- index.html scheda-partita-dashboard.html assets/js/ assets/css/ assets/badges/ || exit 1

# 3. Commit con data e orario (se ci sono modifiche)
DATA_STR=$(date '+%d/%m/%Y %H:%M')
git commit -m "Aggiornamento dati e UI terminale: $DATA_STR" 2>/dev/null || true

echo "Invio delle modifiche su GitHub in corso..."
git push -u origin main

if [ $? -eq 0 ]; then
  echo
  echo "✅ SUCCESSO! Il sito è aggiornato:"
  echo "   🌐 https://mim-analytic-bet.github.io/terminale/"
  osascript -e "display notification \"Sito aggiornato con successo!\" with title \"GitHub Pages Deploy\"" 2>/dev/null
else
  echo
  echo "⚠️ Si è verificato un errore durante il push. Verifica la connessione internet."
fi

echo
read -p "Premi Invio per chiudere"
