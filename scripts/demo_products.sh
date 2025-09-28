#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"

pp() {
  if command -v jq >/dev/null 2>&1; then jq .; else cat; fi
}

wait_ready() {
  echo "→ Esperando API en $BASE_URL/health ..."
  for i in {1..30}; do
    if curl -fsS "$BASE_URL/health" >/dev/null; then
      echo "✓ API lista"
      return 0
    fi
    sleep 1
  done
  echo "✗ API no responde" >&2
  exit 1
}

wait_ready

echo
echo "== Crear productos =="
curl -sS -X POST "$BASE_URL/products" -H 'content-type: application/json' \
  -d '{"name":"Harina","unit":"g"}' | pp
curl -sS -X POST "$BASE_URL/products" -H 'content-type: application/json' \
  -d '{"name":"Agua","unit":"ml"}' | pp
curl -sS -X POST "$BASE_URL/products" -H 'content-type: application/json' \
  -d '{"name":"Levadura","unit":"g"}' | pp
curl -sS -X POST "$BASE_URL/products" -H 'content-type: application/json' \
  -d '{"name":"Sal","unit":"g"}' | pp

echo
echo "== Listar productos =="
curl -sS "$BASE_URL/products" | pp
