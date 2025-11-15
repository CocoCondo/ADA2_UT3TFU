# Recetas – Demo (FastAPI + HAProxy + Postgres + Nginx)

Mini API de **libro de recetas** con front estático, **2 instancias** de API balanceadas por **HAProxy** y **PostgreSQL** como base de datos. Pensado para demostrar **microservicios**

---

## 1. Requisitos

* Docker 24+ y Docker Compose v2

---

## 2. Estructura

```
C:.
│   .env
│   .gitignore
│   docker-compose.yaml
│   Dockerfile
│   README.md
│
├───db
│       init-products.sql
│       init-recipes.sql
│       init-shopping.sql
│
├───gateway
│       Dockerfile
│       haproxy.cfg
│
├───products-service
│   │   Dockerfile
│   │   requirements.txt
│   │
│   └───app
│       │   config.py
│       │   main.py
│       │
│       ├───api
│       │       products_router.py
│       │
│       ├───domain
│       │       models.py
│       │       services.py
│       │
│       └───infrastructure
│               db.py
│               mappers.py
│               repo.py
│
├───recipes-service
│   │   Dockerfile
│   │   requirements.txt
│   │
│   └───app
│       │   config.py
│       │   main.py
│       │
│       ├───api
│       │       recipes_router.py
│       │       recipes_soap_router.py
│       │
│       ├───domain
│       │       models.py
│       │       services.py
│       │
│       └───infrastructure
│               db.py
│               repo.py
│
├───scripts
│   │   demo_all.sh
│   │   demo_health.sh
│   │   demo_products.sh
│   │   demo_recipes.sh
│   │   demo_shopping.sh
│   │   load_sample_data.sh
│   │
│   └───UT5
│           00_seed.sh
│           01_test.sh
│           01_test_rest.sh
│           02_clear_recipes.sh
│           03_test_fault_isolation.sh
│
├───shopping-service
│   │   Dockerfile
│   │   requirements.txt
│   │
│   └───app
│       │   config.py
│       │   main.py
│       │
│       ├───api
│       │       shopping_router.py
│       │
│       ├───domain
│       │       models.py
│       │       services.py
│       │
│       └───infrastructure
│               db.py
│               repo.py
│
└───web
        index.html
```

---

## 3. Puertos

* **8090** → front web (Nginx)
* **8080** → API Gateway (HAProxy)
* **5432** → PostgreSQL
* **8404** → HAProxy Stats (usuario/clave: admin/admin)

---

## 4. Levantar el entorno

```bash
# Copiar y adaptar el archivo de variables:

cp .env.example .env

# Construir y levantar todo:

docker compose up -d --build

# Verificar que el gateway responda:

curl http://localhost:8080/recipes/health

# Abrir el front:

http://localhost:8090
```

> El frontend Nginx llama al API Gateway usando http://gateway:8080 dentro de la red de Docker y http://localhost:8080 desde el host. Los servicios FastAPI tienen CORS habilitado para permitir las llamadas desde el front (ajustar orígenes en producción).

---

## 5. Endpoints principales
### Microservicio products-service (dominio productos):

* `POST /products`
body: { "name": string, "unit": string }

* `GET /products`
lista todos los productos

### Microservicio recipes-service (dominio recetas):
#### REST:

* `GET /recipes`
lista todas las recetas

* `POST /recipes`
body: { "name": string, "steps"?: string }

* `POST /recipes/{id}/items`
body: { "product_id": int, "qty": float }

* `DELETE /recipes`
elimina todas las recetas e items (TRUNCATE + RESTART IDENTITY)

* `GET /health`
healthcheck del servicio

#### SOAP/XML (expuestos desde recipes-service, montados bajo /recipes/soap):

* `POST /recipes/soap/create`
CreateRecipeRequest → CreateRecipeResponse

* `POST /recipes/soap/list`
ListRecipesRequest → ListRecipesResponse

### Microservicio shopping-service (dominio listas de compras):

* `POST /shopping-lists`
body: { "name": string, "recipe_ids": [int, ...] }
crea una lista de compras a partir de recetas

* `GET /shopping-lists`
devuelve todas las listas de compras (id, name)

* `GET /shopping-lists/{id}`
devuelve una lista con sus recetas asociadas
respuesta: { "id": int, "name": string, "recipes": [recipe_id, ...] }
---

## 6. Arquitectura

Arquitectura (vista lógica)

Desde el punto de vista del host:
```

[ web (Nginx:8090) ] → [ API Gateway (HAProxy:8080) ]
│
┌─────────────────┼─────────────────┐
↓ ↓ ↓
[ products-service:8000 ] [ recipes-service:8000 ] [ shopping-service:8000 ]
│ │ │
└───────────────[ PostgreSQL:5432 ]───────────────┘
```
Cada microservicio es stateless: el estado vive en PostgreSQL.

Los datos están particionados por dominio (DB o esquema distinto para productos, recetas y shopping).

Es posible escalar horizontalmente cada servicio de forma independiente modificando docker-compose para añadir réplicas.
---

## 9. Variables de entorno

Archivo `.env` (basado en `.env.example`):

```
PRODUCTS_DATABASE_URL=postgresql://postgres:postgres@db:5432/products_db
RECIPES_DATABASE_URL=postgresql://postgres:postgres@db:5432/recipes_db
SHOPPING_DATABASE_URL=postgresql://postgres:postgres@db:5432/shopping_db
```