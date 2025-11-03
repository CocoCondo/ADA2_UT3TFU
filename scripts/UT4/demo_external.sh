# ver INSTANCE dentro de contenedores
docker compose exec api1 printenv | grep INSTANCE
docker compose exec api2 printenv | grep INSTANCE

# comprobar desde el LB
for i in {1..4}; do curl -s -H 'X-API-Key: 12345-ABCDE' http://localhost:8080/health; echo; done

#Qué: misma imagen, comportamiento distinto por variables externas.
#Esperado: INSTANCE=api-1 / api-2 en env; /health refleja la instancia sin cambiar código.