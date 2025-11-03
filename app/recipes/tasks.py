# app/recipes/tasks.py
import asyncio
_queue = asyncio.Queue()
_processing = False

async def worker(cb=lambda *_: None):
    global _processing
    if _processing: return
    _processing = True
    while True:
        job = await _queue.get()
        # simula trabajo pesado
        await asyncio.sleep(2)
        try:
            cb(job)  # opcional: log
        finally:
            _queue.task_done()

def enqueue(job: dict):
    loop = asyncio.get_event_loop()
    loop.create_task(_queue.put(job))
    loop.create_task(worker())