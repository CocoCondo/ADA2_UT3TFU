#!/usr/bin/env bash
set -euo pipefail

# Config
BASE_URL="${BASE_URL:-http://localhost:8080}"
CLEAN="${CLEAN:-false}"   # CLEAN=true para borrar antes (requiere endpoints DELETE)

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

extract_id() {  # lee {"id":N,...} por stdin o 1er arg
  local text="${1:-}"
  [[ -z "$text" ]] && text="$(cat)"
  echo "$text" | sed -n 's/.*"id"[ ]*:[ ]*\([0-9][0-9]*\).*/\1/p' | head -n1
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


create_product() {
  curl -sS -X POST "$BASE_URL/products" -H 'content-type: application/json' \
    -d "{\"name\":\"$1\",\"unit\":\"$2\"}" >/dev/null
}

add_item() { # recipe_id, product_id, qty
  curl -sS -X POST "$BASE_URL/recipes/$1/items" -H 'content-type: application/json' \
    -d "{\"product_id\":$2,\"qty\":$3}" | pp
}

# --- RUN ---
wait_ready

if [[ "$CLEAN" == "true" ]]; then
  echo "== Limpieza previa (DELETE masivos) =="
  curl -sS -X DELETE "$BASE_URL/shopping-lists" | pp || true
  curl -sS -X DELETE "$BASE_URL/recipes"        | pp || true
  curl -sS -X DELETE "$BASE_URL/products"       | pp || true
fi

echo
echo "== Asegurar productos base =="
create_product "Harina" "g"
create_product "Agua" "ml"
create_product "Levadura" "g"
create_product "Sal" "g"
echo "Productos:"
curl -sS "$BASE_URL/products" | pp
echo

HARINA_ID="$(id_by_product_name Harina)";     [[ -z "${HARINA_ID:-}"    ]] && { echo "✗ Falta Harina";  exit 1; }
AGUA_ID="$(id_by_product_name Agua)";         [[ -z "${AGUA_ID:-}"      ]] && { echo "✗ Falta Agua";    exit 1; }
LEVADURA_ID="$(id_by_product_name Levadura)"; [[ -z "${LEVADURA_ID:-}"  ]] && { echo "✗ Falta Levadura"; exit 1; }
SAL_ID="$(id_by_product_name Sal)";           [[ -z "${SAL_ID:-}"       ]] && { echo "✗ Falta Sal";     exit 1; }

echo
echo "== Crear receta: Pan casero =="
R1=$(curl -sS -X POST "$BASE_URL/recipes" -H 'content-type: application/json' \
  -d '{"name":"Pan casero","steps":"1) Mezclar 2) Amasar 3) Hornear"}')
RID1="$(extract_id "$R1")"; echo "$R1" | pp
[[ -z "$RID1" ]] && { echo "✗ No obtuve RID1"; exit 1; }

echo
echo "== Agregar ingredientes a Pan casero ($RID1) =="
add_item "$RID1" "$HARINA_ID" 500
add_item "$RID1" "$AGUA_ID"   300
add_item "$RID1" "$LEVADURA_ID" 10
add_item "$RID1" "$SAL_ID"      8

echo
echo "== Crear 2 recetas extra: Pizza base y Focaccia =="
R2=$(curl -sS -X POST "$BASE_URL/recipes" -H 'content-type: application/json' \
  -d '{"name":"Pizza base","steps":"Mezclar, amasar, leudar, estirar"}'); echo "$R2" | pp
RID2="$(extract_id "$R2")"; [[ -z "$RID2" ]] && { echo "✗ No obtuve RID2"; exit 1; }

R3=$(curl -sS -X POST "$BASE_URL/recipes" -H 'content-type: application/json' \
  -d '{"name":"Focaccia","steps":"Amasar, leudar, hornear con aceite y sal gruesa"}'); echo "$R3" | pp
RID3="$(extract_id "$R3")"; [[ -z "$RID3" ]] && { echo "✗ No obtuve RID3"; exit 1; }

echo
echo "== Ingredientes para Pizza base ($RID2) y Focaccia ($RID3) =="
add_item "$RID2" "$HARINA_ID" 400
add_item "$RID2" "$AGUA_ID"   250
add_item "$RID2" "$SAL_ID"     7

add_item "$RID3" "$HARINA_ID" 300
add_item "$RID3" "$AGUA_ID"   200
add_item "$RID3" "$SAL_ID"     6

echo
echo "== Crear lista de compras con [$RID2,$RID3] =="
CL=$(curl -sS -X POST "$BASE_URL/shopping-lists" -H 'content-type: application/json' \
  -d "{\"name\":\"Compras panificados\",\"recipe_ids\":[$RID2,$RID3]}")
echo "$CL" | pp
LID="$(extract_id "$CL")"; [[ -z "$LID" ]] && { echo "✗ No obtuve ID de lista"; exit 1; }

echo
echo "== Ver detalle de la lista $LID =="
curl -sS "$BASE_URL/shopping-lists/$LID" | pp

echo
echo "✔ Demo completa."
