# 50 lecturas concurrentes (solo lectura, servicio sin estado)
seq 50 | xargs -n1 -P10 -I{} curl -s http://localhost:8080/health >/dev/null
