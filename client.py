from common import SERVICE
from time import sleep

command = '''
{"data":{"playerId":"00000000-0000-0000-0000-000000000000","topic":"CONTROLLER_COMMAND","payload":{"requestId":"123456789","portId":"","command":"REPORT_STATUS"}}}
'''

if __name__ == "__main__":
    proxy = SERVICE.get_proxy()
    while True:
        proxy.SendServerEvent(command)
        sleep(30)


