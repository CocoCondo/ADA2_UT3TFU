# Recetas – Demo (FastAPI + HAProxy + Postgres + Redis + Nginx)

### Mini API de libro de recetas con front estático, 2 instancias de API balanceadas por HAProxy, PostgreSQL como base de datos, Redis para caché y cola de trabajos, y un worker separado para procesar las tareas en segundo plano.
Pensado para demostrar contenedores, escalado horizontal (stateless), balanceo, patrones de disponibilidad y seguridad, y scripts de prueba automáticos.

## Requisitos

#### Docker 24+ y Docker Compose v2

#### (Opcional) jq para formatear JSON en los scripts

## Estructura del proyecto
```
recetas-app/
├─ app/
│ ├─ products/ (módulo de productos)
│ ├─ recipes/ (módulo de recetas y cola)
│ ├─ shopping/ (módulo de listas de compras)
│ ├─ auth/ (emisión y validación de tokens JWT)
│ ├─ security.py (Gatekeeper + RequireJWT)
│ ├─ config.py (configuración centralizada)
│ └─ workers/recipes_worker.py (worker que procesa jobs de Redis)
│
├─ db/init.sql (esquema inicial de Postgres)
├─ haproxy/haproxy.cfg (proxy inverso y Gatekeeper)
├─ web/index.html (front estático con Nginx)
│
├─ scripts/ (scripts de prueba con curl)
│ ├─ demo_health.sh
│ ├─ demo_products.sh
│ ├─ demo_recipes.sh
│ ├─ demo_shopping.sh
│ ├─ demo_cache.sh
│ ├─ demo_queue.sh
│ ├─ demo_federated.sh
│ └─ demo_gatekeeper.sh
│
├─ Dockerfile
├─ docker-compose.yaml
├─ requirements.txt
└─ .env.example
```
## Puertos
```
Nginx: 8090 (Front web estático)

HAProxy: 8080 (Proxy hacia API)

HAProxy Stats: 8404 (Panel admin/admin)

Postgres: 5432 (Base de datos)

Redis: 6379 (Cache y cola de jobs)
```

## Levantar el entorno
```
docker compose up -d --build

curl -H "X-API-Key: supersecreto" http://localhost:8080/health
```
