import json
import signal
import sys
from dasbus.connection import SystemMessageBus
from dasbus.loop import EventLoop

command = '''
{"data":{"playerId":"00000000-0000-0000-0000-000000000000","topic":"CONTROLLER_COMMAND","payload":{"requestId":"123456789","portId":"","command":"REPORT_STATUS"}}}
'''

def dump(loop, data):
  try:
    print(json.dumps(json.loads(data), indent=2))
  except:
    print('Fail to parse the data:')
    print(data)
  loop.quit()

if __name__ == '__main__':
  # handle the keyboard interrupt signal
  signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
  # start the d-bus test
  loop = EventLoop()
  bus = SystemMessageBus()
  proxy = bus.get_proxy(
    'com.cirrusled.Nucleus1',
    '/com/cirrusled/Nucleus1')
  proxy.StatusReportOccurred.connect(lambda data: dump(loop, data))
  proxy.SendServerEvent(command)
  loop.run()
