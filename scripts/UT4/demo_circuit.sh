docker compose stop api1
for i in {1..4}; do curl -s -H 'X-API-Key: 12345-ABCDE' http://localhost:8080/health; echo; sleep 1; done #Esperado: el loop sigue respondiendo (solo api-2). En Stats api1 pasa a DOWN y luego UP al volver.
docker compose start api1