#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"

echo "→ DELETE /recipes (limpiar recetas + items)"
curl -i -X DELETE "${BASE_URL}/recipes"
