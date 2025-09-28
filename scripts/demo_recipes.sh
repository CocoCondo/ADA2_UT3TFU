#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"

pp() { cat; }

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
echo "== Crear receta: Pan casero =="
CREATE_RES=$(curl -sS -X POST "$BASE_URL/recipes" \
  -H 'content-type: application/json' \
  -d '{"name":"Pan casero","steps":"1) Mezclar 2) Amasar 3) Hornear"}')

echo "$CREATE_RES" | pp

# Extraer id sin jq
RID=$(echo "$CREATE_RES" | sed -n 's/.*\"id\"[ ]*:[ ]*\([0-9][0-9]*\).*/\1/p')

if [[ -z "$RID" ]]; then
  echo "No pude extraer el ID de la receta. Revisá la respuesta."
  exit 1
fi

echo "RID=$RID"

echo
echo "== Listar recetas =="
curl -sS "$BASE_URL/recipes" | pp

echo
echo "== Agregar ingredientes a la receta $RID =="
curl -sS -X POST "$BASE_URL/recipes/$RID/items" -H 'content-type: application/json' \
  -d '{"product_id":1,"qty":500}' | pp
curl -sS -X POST "$BASE_URL/recipes/$RID/items" -H 'content-type: application/json' \
  -d '{"product_id":2,"qty":300}' | pp
curl -sS -X POST "$BASE_URL/recipes/$RID/items" -H 'content-type: application/json' \
  -d '{"product_id":3,"qty":10}' | pp
curl -sS -X POST "$BASE_URL/recipes/$RID/items" -H 'content-type: application/json' \
  -d '{"product_id":4,"qty":8}' | pp
