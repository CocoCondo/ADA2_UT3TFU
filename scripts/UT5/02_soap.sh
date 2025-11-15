#!/usr/bin/env bash

set -e

GATEWAY_URL="http://localhost:8080/recipes/soap"

create_recipe() {
  curl -s -X POST "$GATEWAY_URL/create" \
    -H "Content-Type: text/xml" \
    -d '<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateRecipeRequest>
      <Name>Test SOAP Recipe</Name>
      <Steps>Step A - Step B</Steps>
    </CreateRecipeRequest>
  </soap:Body>
</soap:Envelope>'
}

list_recipes() {
  curl -s -X POST "$GATEWAY_URL/list" \
    -H "Content-Type: text/xml" \
    -d '<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ListRecipesRequest/>
  </soap:Body>
</soap:Envelope>'
}

echo "== CREATE =="
create_recipe
echo ""
echo ""
echo "== LIST =="
list_recipes
echo ""
