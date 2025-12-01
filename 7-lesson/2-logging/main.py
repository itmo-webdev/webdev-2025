import logging
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/hello")
async def hello():
    logger.info("Hello endpoint called")
    return {"message": "hello"}