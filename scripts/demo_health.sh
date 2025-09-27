# healthcheck alternando instancias
for i in {1..7}; do curl -s http://localhost:8080/health; echo; done
# Debes ver {"ok":true,"instance":"api-1"} y {"instance":"api-2"} alternándose.
