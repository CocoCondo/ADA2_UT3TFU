#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"

echo "== Estado inicial: todos los servicios arriba =="
curl -s -o /dev/null -w "GET /products -> HTTP %{http_code}\n" \
  "${BASE_URL}/products"
curl -s -o /dev/null -w "GET /recipes -> HTTP %{http_code}\n" \
  "${BASE_URL}/recipes"
curl -s -o /dev/null -w "GET /shopping-lists -> HTTP %{http_code}\n" \
  "${BASE_URL}/shopping-lists"

echo
echo "== Simulando fallo SOLO en recipes-service =="
docker compose stop recipes-service
sleep 5

echo
echo "== Pruebas después del fallo en recipes-service =="
curl -s -o /dev/null -w "GET /products -> HTTP %{http_code}\n" \
  "${BASE_URL}/products"
curl -s -o /dev/null -w "GET /recipes -> HTTP %{http_code}\n" \
  "${BASE_URL}/recipes"
curl -s -o /dev/null -w "GET /shopping-lists -> HTTP %{http_code}\n" \
  "${BASE_URL}/shopping-lists"

echo
echo "== Restaurando recipes-service =="
docker compose start recipes-service
sleep 5

echo
echo "== Verificación final: todos arriba de nuevo =="
curl -s -o /dev/null -w "GET /recipes -> HTTP %{http_code}\n" \
  "${BASE_URL}/recipes"