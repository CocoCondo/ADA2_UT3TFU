#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"

echo "== Test REST: products =="
curl -s -o /dev/null -w "GET /products -> HTTP %{http_code}\n" \
  "${BASE_URL}/products"

echo "== Test REST: recipes =="
curl -s -o /dev/null -w "GET /recipes -> HTTP %{http_code}\n" \
  "${BASE_URL}/recipes"

echo "== Test REST: shopping-lists =="
curl -s -o /dev/null -w "GET /shopping-lists -> HTTP %{http_code}\n" \
  "${BASE_URL}/shopping-lists"

echo "== Test POST /products =="
curl -s -o /dev/null -w "POST /products -> HTTP %{http_code}\n" \
  -X POST "${BASE_URL}/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Harina", "unit": "kg"}'

echo "== Test POST /recipes =="
curl -s -o /dev/null -w "POST /recipes -> HTTP %{http_code}\n" \
  -X POST "${BASE_URL}/recipes" \
  -H "Content-Type: application/json" \
  -d '{"name": "Pan casero"}'

echo "== Test POST /shopping-lists =="
curl -s -o /dev/null -w "POST /shopping-lists -> HTTP %{http_code}\n" \
  -X POST "${BASE_URL}/shopping-lists" \
  -H "Content-Type: application/json" \
  -d '{"name": "Compra UT5"}'