from common import SERVICE
from time import sleep
from common import command


if __name__ == "__main__":
    proxy = SERVICE.get_proxy()
    while True:
        proxy.SendServerEvent(command)
        sleep(3)


