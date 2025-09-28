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

extract_id_from_create() {  # recibe JSON como texto
  echo "$1" | sed -n 's/.*"id"[ ]*:[ ]*\([0-9][0-9]*\).*/\1/p' | head -n1
}

id_by_product_name() {
  local name="$1" json
  json="$(curl -sS "$BASE_URL/products")"

  # Preferir python3 (código vía -c, JSON por stdin)
  if command -v python3 >/dev/null 2>&1; then
    python3 -c '
import sys, json
data = json.loads(sys.stdin.read())
name = sys.argv[1]
print(next((str(x.get("id")) for x in data if x.get("name")==name), ""), end="")
' "$name" <<<"$json"
    return
  fi

  # Fallback con sed (asume campos en el orden que devuelve la API)
  echo "$json" | sed -n "s/.*{\"name\":\"$name\"[^}]*\"id\":[ ]*\\([0-9][0-9]*\\).*/\\1/p" | head -n1
}


wait_ready

echo
echo "== Asegurar productos base (Harina, Agua, Levadura, Sal) =="
curl -sS -X POST "$BASE_URL/products" -H 'content-type: application/json' -d '{"name":"Harina","unit":"g"}' >/dev/null || true
curl -sS -X POST "$BASE_URL/products" -H 'content-type: application/json' -d '{"name":"Agua","unit":"ml"}'    >/dev/null || true
curl -sS -X POST "$BASE_URL/products" -H 'content-type: application/json' -d '{"name":"Levadura","unit":"g"}' >/dev/null || true
curl -sS -X POST "$BASE_URL/products" -H 'content-type: application/json' -d '{"name":"Sal","unit":"g"}'      >/dev/null || true

echo "Productos actuales:"
curl -sS "$BASE_URL/products" | pp
echo

HARINA_ID="$(id_by_product_name Harina)";     [[ -z "${HARINA_ID:-}"    ]] && { echo "✗ No encontré ID de Harina";  exit 1; }
AGUA_ID="$(id_by_product_name Agua)";         [[ -z "${AGUA_ID:-}"      ]] && { echo "✗ No encontré ID de Agua";    exit 1; }
LEVADURA_ID="$(id_by_product_name Levadura)"; [[ -z "${LEVADURA_ID:-}"  ]] && { echo "✗ No encontré ID de Levadura"; exit 1; }
SAL_ID="$(id_by_product_name Sal)";           [[ -z "${SAL_ID:-}"       ]] && { echo "✗ No encontré ID de Sal";     exit 1; }

echo "Productos OK → Harina:$HARINA_ID Agua:$AGUA_ID Levadura:$LEVADURA_ID Sal:$SAL_ID"

echo
echo "== Crear 2 recetas nuevas =="
CREATE1=$(curl -sS -X POST "$BASE_URL/recipes" -H 'content-type: application/json' \
  -d '{"name":"Pizza base","steps":"Mezclar, amasar, leudar, estirar"}')
RID1=$(extract_id_from_create "$CREATE1"); [[ -z "$RID1" ]] && { echo "✗ No obtuve RID1"; exit 1; }
echo "RID1=$RID1 ($CREATE1)"

CREATE2=$(curl -sS -X POST "$BASE_URL/recipes" -H 'content-type: application/json' \
  -d '{"name":"Focaccia","steps":"Amasar, leudar, hornear con aceite y sal gruesa"}')
RID2=$(extract_id_from_create "$CREATE2"); [[ -z "$RID2" ]] && { echo "✗ No obtuve RID2"; exit 1; }
echo "RID2=$RID2 ($CREATE2)"

echo
echo "== Agregar ingredientes a $RID1 (Pizza base) =="
curl -sS -X POST "$BASE_URL/recipes/$RID1/items" -H 'content-type: application/json' -d "{\"product_id\":$HARINA_ID,\"qty\":400}" | pp
curl -sS -X POST "$BASE_URL/recipes/$RID1/items" -H 'content-type: application/json' -d "{\"product_id\":$AGUA_ID,\"qty\":250}"   | pp
curl -sS -X POST "$BASE_URL/recipes/$RID1/items" -H 'content-type: application/json' -d "{\"product_id\":$SAL_ID,\"qty\":7}"     | pp

echo
echo "== Agregar ingredientes a $RID2 (Focaccia) =="
curl -sS -X POST "$BASE_URL/recipes/$RID2/items" -H 'content-type: application/json' -d "{\"product_id\":$HARINA_ID,\"qty\":300}" | pp
curl -sS -X POST "$BASE_URL/recipes/$RID2/items" -H 'content-type: application/json' -d "{\"product_id\":$AGUA_ID,\"qty\":200}"   | pp
curl -sS -X POST "$BASE_URL/recipes/$RID2/items" -H 'content-type: application/json' -d "{\"product_id\":$SAL_ID,\"qty\":6}"     | pp

echo
echo "== Crear lista de compras desde [$RID1,$RID2] =="
CREATE_LIST=$(curl -sS -X POST "$BASE_URL/shopping-lists" -H 'content-type: application/json' \
  -d "{\"name\":\"Compras panificados\",\"recipe_ids\":[$RID1,$RID2]}")
echo "$CREATE_LIST" | pp
LID=$(extract_id_from_create "$CREATE_LIST"); [[ -z "$LID" ]] && { echo "✗ No obtuve ID de lista"; exit 1; }

echo
echo "== Ver detalle de la lista $LID =="
curl -sS "$BASE_URL/shopping-lists/$LID" | pp
