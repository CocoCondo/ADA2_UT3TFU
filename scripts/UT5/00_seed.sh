#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"

echo "== Seed: PRODUCTS =="

curl -s "${BASE_URL}/products" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"name": "Tomate", "unit": "kg"}' \
  | jq .

curl -s "${BASE_URL}/products" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"name": "Pasta seca", "unit": "pack"}' \
  | jq .

curl -s "${BASE_URL}/products" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"name": "Queso rallado", "unit": "paquete"}' \
  | jq .

curl -s "${BASE_URL}/products" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"name": "Lechuga", "unit": "unidad"}' \
  | jq .


echo
echo "== Seed: RECIPES =="

curl -s "${BASE_URL}/recipes" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
        "name": "Pasta con salsa de tomate",
        "instructions": "Hervir la pasta, preparar salsa con tomate y mezclar.",
        "ingredients": [
          {"product_name": "Pasta seca", "quantity": 1, "unit": "pack"},
          {"product_name": "Tomate", "quantity": 0.5, "unit": "kg"},
          {"product_name": "Queso rallado", "quantity": 1, "unit": "paquete"}
        ]
      }' \
  | jq .

curl -s "${BASE_URL}/recipes" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
        "name": "Ensalada mixta",
        "instructions": "Cortar vegetales, mezclar y condimentar.",
        "ingredients": [
          {"product_name": "Lechuga", "quantity": 1,