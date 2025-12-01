from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

app = FastAPI()

instrumentator = Instrumentator()
instrumentator.instrument(app)

RANDOM_NUMBER_TOTAL = Counter(
    "random_number", "Total number of random number"
)


@app.on_event("startup")
def _startup():
    instrumentator.expose(app)


@app.get("/")
def index():
    return {"message": "hello"}


@app.get("/compute")
def compute():

    x = sum(i * i for i in range(10000))
    RANDOM_NUMBER_TOTAL.inc()
    return {"result": x}


