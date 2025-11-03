#!/usr/bin/env bash
set -e

BASE="${BASE:-http://localhost:8080}"
KEY="${KEY:-12345-ABCDE}"

echo "→ Salud:"
curl -s -H "X-API-Key: $KEY" "$BASE/health" && echo

echo
echo "== Solicitar token en /auth/demo-token =="
RESP=$(curl -s -i -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"sub":"alumno-ucu","extra":{"role":"tester"}}' \
  "$BASE/auth/demo-token")

STATUS=$(printf "%s" "$RESP" | sed -n '1{s/.* \([0-9][0-9][0-9]\).*/\1/p}')
CT=$(printf "%s" "$RESP" | sed -n 's/^content-type: \(.*\)$/\1/ip' | tr -d '\r')

printf "HTTP %s | %s\n" "$STATUS" "$CT"
BODY=$(printf "%s" "$RESP" | sed -n '1,/^\r$/d;p')

if [ "$STATUS" != "200" ]; then
  echo "✗ Falla al obtener token. Cuerpo:"
  echo "$BODY" | head -n 50
  exit 1
fi

# Intentar extraer el token (sin jq)
TOKEN=$(printf "%s" "$BODY" | sed -n 's/.*"token"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)

if [ -z "$TOKEN" ]; then
  echo "✗ No pude extraer 'token' del JSON devuelto:"
  echo "$BODY" | head -n 30
  exit 1
fi

echo "✓ Token obtenido (40 chars): ${TOKEN:0:40}..."

echo
echo "== /recipes sin token → 401 =="
curl -si -H "X-API-Key: $KEY" "$BASE/recipes" | head -n 10

echo
echo "== /recipes con token → 200 =="
curl -si -H "X-API-Key: $KEY" -H "Authorization: Bearer $TOKEN" \
  "$BASE/recipes" | head -n 20
