
# С покрытием кода
pytest --cov=app

# С указанием непокрытых строк
pytest --cov=app --cov-report=term-missing

# HTML отчёт
pytest --cov=app --cov-report=html
```
