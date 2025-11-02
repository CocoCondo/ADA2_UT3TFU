from fastapi import HTTPException
from .schemas import RecipeIn, RecipeOut, RecipeItemIn
from . import repo
import redis
from app.config import settings
import json, uuid, time

r = redis.from_url(settings.REDIS_URL)

QUEUE_KEY = "recipes_queue"

def enqueue_recipe(data: dict) -> dict:
    job = {
        "id": str(uuid.uuid4()),
        "ts": int(time.time()),
        "type": "recipe.create",
        "payload": data,
    }
    r.lpush(QUEUE_KEY, json.dumps(job))
    size = r.llen(QUEUE_KEY)
    return {"status": "queued", "job_id": job["id"], "queue_size": size}

def queue_stats() -> dict:
    size = r.llen(QUEUE_KEY)
    # peek no destructivo (LRANGE 0..2)
    sample = [json.loads(x) for x in r.lrange(QUEUE_KEY, 0, 2)]
    return {"size": size, "head": sample}

def create_recipe(data: RecipeIn) -> dict:
    rid = repo.insert_recipe(data.model_dump())
    return {"id": rid, "status": "created"}

def get_all_recipes() -> list[RecipeOut]:
    return [RecipeOut(**r) for r in repo.list_recipes()]

def add_recipe_item(recipe_id: int, item: RecipeItemIn):
    try:
        repo.add_item(recipe_id, item.product_id, item.qty)
    except Exception as e:
        raise HTTPException(400, f"No se pudo agregar ingrediente: {e}")
    return {"status": "ok"}
