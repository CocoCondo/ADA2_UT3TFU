# app/workers/recipes_worker.py
import json, time, logging
import redis
from app.config import settings

logging.basicConfig(level=logging.INFO, format="worker:%(levelname)s:%(message)s")
log = logging.getLogger("worker")
r = redis.from_url(settings.REDIS_URL)
QUEUE_KEY = "recipes_queue"

def process(job: dict):
    # Simula trabajo "pesado"
    payload = job.get("payload") or {}
    name = (payload.get("name") or "sin-nombre")
    log.info(f"Procesando job {job['id']} → receta='{name}'")
    time.sleep(2)  # simular CPU/IO
    log.info(f"OK job {job['id']}")

def main():
    log.info("Esperando trabajos en Redis…")
    while True:
        item = r.brpop(QUEUE_KEY, timeout=0)  # bloquea hasta que haya
        if item:
            _, data = item
            try:
                job = json.loads(data)
                process(job)
            except Exception as e:
                log.error(f"Fallo procesando job: {e}")

if __name__ == "__main__":
    main()