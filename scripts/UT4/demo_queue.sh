#!/usr/bin/env bash
set -e

BASE="${BASE:-http://localhost:8080}"
KEY="${GOOD_KEY:-12345-ABCDE}"

echo "→ Salud:"
curl -s -H "X-API-Key: $KEY" "$BASE/health" && echo

echo "== Obtener token =="
TOKEN=$(curl -s -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"sub":"queue-demo"}' "$BASE/auth/demo-token" \
  | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')
[ -n "$TOKEN" ] || { echo "No pude obtener token"; exit 1; }
echo "TOKEN OK"

enqueue() {
  echo -e "\n== Enqueue: $1 =="
  curl -i -H "X-API-Key: $KEY" \
       -H "Authorization: Bearer $TOKEN" \
       -H "Content-Type: application/json" \
       -d "{\"name\":\"$1\",\"steps\":\"$2\"}" \
       "$BASE/recipes/enqueue"
}

stats() {
  echo -e "\n== Queue stats =="
  curl -i -H "X-API-Key: $KEY" -H "Authorization: Bearer $TOKEN" \
    "$BASE/recipes/queue/stats"
}

stats
enqueue "Pan demo" "1) Mezclar\n2) Amasar\n3) Hornear"
enqueue "Focaccia demo" "1) Mezclar\n2) Fermentar\n3) Hornear"
enqueue "Pizza demo" "1) Mezclar\n2) Estirar\n3) Hornear"
stats

echo -e "\n→ Mirá los logs del worker para ver cómo se vacía la cola:"
echo "   docker compose logs -f worker"