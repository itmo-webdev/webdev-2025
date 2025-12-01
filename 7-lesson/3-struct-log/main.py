import structlog
from fastapi import FastAPI, Request
import time
import logging

logging.basicConfig(
    level=logging.INFO,
)

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.EventRenamer("event"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log = structlog.get_logger()

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000

    log.info(
        "request_handled",
        path=request.url.path,
        method=request.method,
        status_code=response.status_code,
        duration_ms=round(duration, 2),
    )
    return response

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    log.info("get_user_called", user_id=user_id)
    return {"user_id": user_id}