#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"

SOAP_BODY='<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:rec="http://example.com/recipes">
   <soapenv:Header/>
   <soapenv:Body>
      <rec:GetRecipeByIdRequest>
         <rec:id>1</rec:id>
      </rec:GetRecipeByIdRequest>
   </soapenv:Body>
</soapenv:Envelope>'

echo "== Test SOAP /recipes/soap =="
curl -s -w "\nHTTP %{http_code}\n" \
  -X POST "${BASE_URL}/recipes/soap" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -d "${SOAP_BODY}"