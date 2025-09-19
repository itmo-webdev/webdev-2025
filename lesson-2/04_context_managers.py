# with open("example.txt", "w") as f:
#     f.write("Привет, мир!")
# # файл автоматически закроется


    class ManagedResource:
        def __enter__(self):
            print("Ресурс открыт")
            return "ресурс"
        
        def __exit__(self, exc_type, exc_value, traceback):
            print("Ресурс закрыт")

    with ManagedResource() as res:
        print(f"Используем {res}")


import time
from contextlib import contextmanager

@contextmanager
def timer(name="Блок кода"):
    start = time.time()
    yield
    end = time.time()
    print(f"{name} занял {end - start:.4f} секунд")

with timer("Обработка"):
    sum(range(10**6))


    