#!/usr/bin/env bash
set -euo pipefail

# healthcheck alternando instancias
for i in {1..7}; do curl -s -H 'X-API-Key: 12345-ABCDE' http://localhost:8080/health; echo; done
# Debes ver {"ok":true,"instance":"api-1"} y {"instance":"api-2"} alternándose.
