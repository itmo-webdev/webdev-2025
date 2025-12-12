from fastapi import FastAPI, HTTPException

app = FastAPI()


def add(a: int, b: int) -> int:
    """Сложение двух чисел."""
    return a + b


def divide(a: int, b: int) -> float:
    """Деление двух чисел."""
    if b == 0:
        raise ValueError("Деление на ноль")
    return a / b


@app.get("/")
def root():
    return {"message": "Hello"}


@app.get("/add")
def api_add(a: int, b: int):
    return {"result": add(a, b)}


@app.get("/divide")
def api_divide(a: int, b: int):
    try:
        return {"result": divide(a, b)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
