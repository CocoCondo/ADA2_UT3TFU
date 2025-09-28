# Recetas – Demo (FastAPI + HAProxy + Postgres + Nginx)

Mini API de **libro de recetas** con front estático, **2 instancias** de API balanceadas por **HAProxy** y **PostgreSQL** como base de datos. Pensado para demostrar **contenedores**, **escalado horizontal (stateless)**, **balanceo**, y **scripts de prueba**.

---

## 1. Requisitos

* Docker 24+ y Docker Compose v2

---

## 2. Estructura

```
recetas-app/
├─ app/                    # backend FastAPI por dominios (products/recipes/shopping)
├─ db/init.sql             # DDL inicial (Postgres)
├─ haproxy/haproxy.cfg     # frontend :80 → api1/api2 ; stats :8404
├─ web/index.html          # front estático (Nginx)
├─ scripts/*.sh            # scripts de demo (curl)
│   ├─ demo_products.sh
│   ├─ demo_recipes.sh
│   ├─ demo_shopping.sh
│   └─ demo_all.sh         # ejecuta todo el flujo (productos→recetas→listas)
├─ Dockerfile              # imagen de la API
├─ docker-compose.yaml     # db + api(1,2) + lb + web
├─ requirements.txt        # dependencias Python
└─ .env.example            # variables (DATABASE_URL, INSTANCE, ENV)
```

---

## 3. Puertos

* **8090** → Front web (Nginx)
* **8080** → API (vía HAProxy)
* **8404** → HAProxy Stats (usuario/clave: `admin`/`admin`)

---

## 4. Levantar el entorno

```bash
# 1) build + up
docker compose up -d --build

# 2) verificar servicios
curl http://localhost:8080/health
# → {"ok":true,"instance":"api-1"} o "api-2"

# 3) abrir el front
# http://localhost:8090
```

> Si el front (8090) consulta a la API (8080), FastAPI ya trae CORS habilitado en `app/main.py`. Ajustar orígenes en producción.

---

## 5. Endpoints principales

* `GET /health`
* `POST /products` `{ name, unit }`
* `GET /products`
* `POST /recipes` `{ name, steps? }`
* `GET /recipes`
* `POST /recipes/{id}/items` `{ product_id, qty }`
* `POST /shopping-lists` `{ name, recipe_ids[] }`
* `GET /shopping-lists/{id}`

---

## 6. Scripts de demo

```bash
# Alterna instancias (muestra api-1 / api-2)
bash scripts/demo_health.sh

# Crear y listar productos
bash scripts/demo_products.sh

# Crear receta y agregar ingredientes
bash scripts/demo_recipes.sh

# Crear varias recetas y una lista de compras
bash scripts/demo_shopping.sh

# Demo completa (productos → recetas → listas)
bash scripts/demo_all.sh
```

---

## 7. HAProxy Stats

* Config: `haproxy/haproxy.cfg` (sección `listen stats`)
* Acceso: [http://localhost:8404](http://localhost:8404) (usuario `admin`, pass `admin`)

---

## 8. Arquitectura

```
[ web (Nginx:8090) ]  →  [ HAProxy:8080 ]  →  [ api1:8000 ]
                                         └→ [ api2:8000 ]
                                     ↘
                                  [ Postgres:5432 ]
```

* La API es **stateless** (se puede escalar). El estado persiste en **Postgres**.

---

## 9. Variables de entorno

Archivo `.env` (basado en `.env.example`):

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/recipes
INSTANCE=api
ENV=dev
```

> `INSTANCE` se muestra en `/health` para ver el balanceo.

---

## 10. Troubleshooting

* **`COPY requirements.txt` no encontrado**: revisá que `requirements.txt` esté en el *context* del `Dockerfile` y que `.dockerignore` no lo excluya.
* **CORS**: si front y API corren en puertos distintos, configurar `CORSMiddleware` en `app/main.py`.
* **DB no lista**: Compose ya define `depends_on: service_healthy`. Esperá a que la healthcheck pase.
* **ON CONFLICT error en shopping_list_items**: asegurate de que la tabla tenga `PRIMARY KEY (list_id, product_id)`.
* **500 en `/shopping-lists/{id}`**: verificar que `qty` se devuelva casteado a `float` en `repo.get_list`.

---

## Comandos útiles

```bash
# logs
docker compose logs -f lb api1 api2 db web

# rebuild sin cache
docker compose build --no-cache

# rebuild solo un servicio
docker compose up -d --no-deps --build api1

# parar y limpiar
docker compose down -v
```