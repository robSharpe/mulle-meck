#!/bin/bash
# Starta Mulle Meck Bygger Bilar lokalt
# Dubbelklicka på den här filen i Finder för att spela

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GAME_DIR="$SCRIPT_DIR/mulle-meck-lokal"

# Döda eventuell gammal server på port 8000 (SIGTERM, inte -9; hoppa över om inga finns)
OLD_PIDS=$(lsof -ti tcp:8000)
if [ -n "$OLD_PIDS" ]; then
    echo "$OLD_PIDS" | xargs kill 2>/dev/null
fi

# Starta flertrådig server i bakgrunden
python3 "$SCRIPT_DIR/server.py" &
SERVER_PID=$!

# Stoppa servern automatiskt när fönstret stängs / scriptet avslutas
trap 'kill "$SERVER_PID" 2>/dev/null' EXIT

# Vänta tills servern svarar (max 5 sekunder)
SERVER_UP=0
for i in 1 2 3 4 5; do
    sleep 1
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        SERVER_UP=1
        break
    fi
done

if [ "$SERVER_UP" -ne 1 ]; then
    echo "Varning: servern svarade inte inom 5 sekunder – öppnar ändå."
fi

# Öppna webbläsaren
open "http://localhost:8000"

echo "Mulle Meck körs på http://localhost:8000"
echo "Stäng det här fönstret för att stoppa servern."

# Håll servern igång
wait $SERVER_PID
