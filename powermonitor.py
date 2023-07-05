from signal import signal, SIGINT
from sys import exit
from os.path import exists
from os import system 
from datetime import datetime
from time import sleep
import json
from dasbus.connection import SystemMessageBus
from dasbus.loop import EventLoop
import sys

DB="/var/log/cirrus-rrd/power"
capture_window=3    # seconds to capture packet
heartbeat=30        # seconds sleep between captures
capture_space=60    # seconds between recorded values


SPI1_Port = 'PortA'
SPI1_Index = 1

SPI2_Port = 'PortB'
SPI2_Index = 1

command = '''
{"data":{"playerId":"00000000-0000-0000-0000-000000000000","topic":"CONTROLLER_COMMAND","payload":{"requestId":"123456789","portId":"","command":"REPORT_STATUS"}}}
'''

powerdata = {}

def dump(loop, data):
  global powerdata
  try:
    powerdata = json.dumps(json.loads(data), indent=2)
  except:
    print('Fail to parse the data:')
    print(data)
  loop.quit()

def sigint_handler(signal, frame):
  exit(0)

if __name__ == '__main__':
  # handle the keyboard interrupt signal
  signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
  # start the d-bus test
  loop = EventLoop()
  bus = SystemMessageBus()
  proxy = bus.get_proxy(
    'com.cirrusled.Nucleus1',
    '/com/cirrusled/Nucleus1')
  while True:
    proxy.StatusReportOccurred.connect(lambda data: dump(loop, data))
    proxy.SendServerEvent(command)
    loop.run()
    for port in powerdata["data"]["payload"]["ports"]:
      if (port["id"]=='PortA'):
        PortA_V = port["rmsVoltage"]
        PortA_I = port["rmsCurrent"]
        PortA_PF = port["powerFactor"]
      elif (port["id"]=='PortB'):
        PortB_V = port["rmsVoltage"]
        PortB_I = port["rmsCurrent"]
        PortB_PF = port["powerFactor"]
    
    for port in powerdata["data"]["payload"]["spis"]:
      if (port["portId"] == SPI1_Port and port["id"] == SPI1_Index):
        SPI1_V  = port["rmsVoltage"]
        SPI1_I  = port["rmsCurrent"]
        SPI1_PF = port["powerFactor"]
      elif (port["portId"] == SPI2_Port and port["id"] == SPI2_Index):
        SPI2_V  = port["rmsVoltage"]
        SPI2_I  = port["rmsCurrent"]
        SPI2_PF = port["powerFactor"]

    shell = "rrdtool updatev {}.rrd N:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(
              DB,
              PortA_V, PortA_I, PortA_PF,
              PortB_V, PortB_I, PortB_PF,
              SPI1_V, SPI1_I, SPI1_PF,
              SPI2_V, SPI2_I, SPI2_PF
              )
    system(shell)
    sleep(heartbeat)

