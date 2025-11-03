#!/bin/bash
BASE_URL="http://localhost:8080"
KEY="12345-ABCDE"

echo "== Primer GET: debería venir de DB =="
curl -s -H "X-API-Key: $KEY" "$BASE_URL/products" | jq .

sleep 1
echo -e "\n== Segundo GET: debería venir de CACHE =="
curl -s -H "X-API-Key: $KEY" "$BASE_URL/products" | jq .

sleep 1
echo -e "\n== Crear nuevo producto (invalida cache) =="
curl -s -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
     -d '{"name":"Azúcar","unit":"g"}' "$BASE_URL/products" | jq .

sleep 1
echo -e "\n== GET luego de escribir: debería venir de DB otra vez =="
curl -s -H "X-API-Key: $KEY" "$BASE_URL/products" | jq .