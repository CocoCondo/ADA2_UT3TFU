#!/usr/bin/env bash
set -euo pipefail

# Colores ANSI
RED="\033[31m"
GREEN="\033[32m"
BLUE="\033[34m"
YELLOW="\033[33m"
BOLD="\033[1m"
NC="\033[0m"   # reset

BASE_URL="${BASE_URL:-http://localhost:8080}"
SOAP_URL="${BASE_URL}/recipes/soap"

line() {
  printf "${YELLOW}----------------------------------------------${NC}\n"
}

section() {
  printf "${BOLD}${BLUE}== %s ==${NC}\n" "$1"
}

step() {
  printf "${GREEN}→ %s${NC}\n" "$1"
}

# -----------------------------------------
# REST
# -----------------------------------------
section "RECIPES – REST"

step "GET /recipes"
curl -i "${BASE_URL}/recipes"
line

step "POST /recipes"
curl -i -X POST "${BASE_URL}/recipes" \
  -H "Content-Type: application/json" \
  -d '{"name": "Pan REST UT5", "steps": "Mezclar, amasar, hornear"}'
line

step "POST /recipes/{id}/items"
curl -i -X POST "${BASE_URL}/recipes/1/items" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "qty": 2.5}'
line


# -----------------------------------------
# SOAP
# -----------------------------------------
section "RECIPES – SOAP/XML"

step "SOAP create"
curl -i -X POST "${SOAP_URL}/create" \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateRecipeRequest>
      <Name>Pan SOAP UT5</Name>
      <Steps>Mezclar, amasar, hornear (SOAP)</Steps>
    </CreateRecipeRequest>
  </soap:Body>
</soap:Envelope>'
line

step "SOAP list"
curl -i -X POST "${SOAP_URL}/list" \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ListRecipesRequest/>
  </soap:Body>
</soap:Envelope>'
line

echo -e "${BOLD}${GREEN}✔ Tests completados.${NC}"
