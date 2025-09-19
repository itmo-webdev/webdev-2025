import subprocess

def ping(host):
    subprocess.call(["ping", "-c", "1", host])

# def ping(host):
#     # ⚠️ Уязвимость: небезопасно формировать команду через shell=True
#     command = f"ping -c 1 {host}"
#     subprocess.call(command, shell=True)

if __name__ == "__main__":
    user_input = input("Введите адрес: ")
    ping(user_input)