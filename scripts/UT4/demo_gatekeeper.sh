#!/usr/bin/env bash
set -e

BASE="${BASE:-http://localhost:8080}"
GOOD_KEY="${GOOD_KEY:-12345-ABCDE}"      # debe coincidir con haproxy.cfg
BAD_KEY="${BAD_KEY:-malclave}"

divider() { echo -e "\n--------------------------------------------------------\n"; }

echo "🔐 DEMO: Gatekeeper (HAProxy bloquea por API-Key)"
echo "Base URL: $BASE"
divider

# 1️⃣ SIN API KEY → 403
echo "== 1) Request sin X-API-Key (debería dar 403) =="
curl -i "$BASE/products"
divider

# 2️⃣ CON API KEY CORRECTA → 200 OK
echo "== 2) Request con X-API-Key correcta (debería dar 200) =="
curl -i -H "X-API-Key: $GOOD_KEY" "$BASE/products"
divider

# 3️⃣ CON API KEY INCORRECTA → 403
echo "== 3) Request con X-API-Key incorrecta (debería dar 403) =="
curl -i -H "X-API-Key: $BAD_KEY" "$BASE/products"
divider

