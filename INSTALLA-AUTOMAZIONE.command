#!/bin/bash
# Doppio clic una sola volta: attiva l'aggiornamento automatico (ogni giorno alle 08:00, 14:00 e 23:30, e a ogni avvio del Mac).
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/scripts/verifica_fonti.py" --operazione download || exit 2
PL="$HOME/Library/LaunchAgents/com.domenico.scommesse.plist"
chmod +x "$DIR/scripts/aggiorna_tutto.sh"
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PL" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>com.domenico.scommesse</string>
<key>ProgramArguments</key><array>
  <string>/bin/bash</string>
  <string>$DIR/scripts/aggiorna_tutto.sh</string>
</array>
<key>WorkingDirectory</key><string>$DIR</string>
<key>RunAtLoad</key><true/>
<key>StartCalendarInterval</key><array>
<dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
<dict><key>Hour</key><integer>14</integer><key>Minute</key><integer>0</integer></dict>
<dict><key>Hour</key><integer>23</integer><key>Minute</key><integer>30</integer></dict>
</array>
<key>StandardOutPath</key><string>$DIR/dati/launchd.log</string>
<key>StandardErrorPath</key><string>$DIR/dati/launchd.err</string>
</dict></plist>
PLIST

launchctl bootout "gui/$(id -u)/com.domenico.scommesse" 2>/dev/null
launchctl bootstrap "gui/$(id -u)" "$PL"

if [ $? -eq 0 ]; then
  echo "======================================================"
  echo "✅ AUTOMAZIONE ATTIVA CON SUCCESSO!"
  echo "   Il Mac aggiornerà i dati e pubblicherà su GitHub:"
  echo "   - Ogni giorno alle 08:00, 14:00 e 23:30"
  echo "   - A ogni accensione del Mac"
  echo "======================================================"
else
  echo "⚠️ Installazione automatica non riuscita."
fi

sleep 3
tail -n 10 "$DIR/dati/aggiornamento.log" 2>/dev/null
echo
read -p "Premi Invio per chiudere"
