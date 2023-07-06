from dasbus.loop import EventLoop
from dasbus.connection import SystemMessageBus
from dasbus.identifier import DBusServiceIdentifier
import json
from os import system
from time import sleep
from threading import Thread

MESSAGE_BUS = SystemMessageBus()
SERVICE = DBusServiceIdentifier(
        namespace = ("com", "cirrusled", "Nucleus1"),
        message_bus = MESSAGE_BUS
)

command = '''
{"data":{"playerId":"00000000-0000-0000-0000-000000000000","topic":"CONTROLLER_COMMAND","payload":{"requestId":"123456789","portId":"","command":"REPORT_STATUS"}}}
'''

SPI1_Port = 'Port A'
SPI1_Index = '1'
SPI2_Port = 'Port B'
SPI2_Index = '1'

DB="/var/log/cirrus-rrd/power"

def callback(data):
    SPI1_V = SPI1_I = SPI1_PF = SPI2_V = SPI2_I = SPI2_PF = 0
    powerdata = json.loads(data)
    for port in powerdata["data"]["payload"]["ports"]:
      if (port["id"]=='Port A'):
        PortA_V = port["rmsVoltage"]
        PortA_I = port["rmsCurrent"]
        PortA_PF = port["powerFactor"]
      elif (port["id"]=='Port B'):
        PortB_V = port["rmsVoltage"]
        PortB_I = port["rmsCurrent"]
        PortB_PF = port["powerFactor"]
    #if "spis" in powerdata["data"]["payload"]:
    #  for port in powerdata["data"]["payload"]["spis"]:
    #    if (port["portId"]==SPI1_Port and port["id"]==SPI1_Index):
    #      SPI1_V = port["rmsVoltage"]
    #      SPI1_I = port["rmsCurrent"]
    #      SPI1_PF = port["powerFactor"]
    #    elif (port["portId"] == SPI2_Port and port["id"] == SPI2_Index):
    #      SPI2_V = port["rmsVoltage"]
    #      SPI2_I = port["rmsCurrent"]
    #      SPI2_PF = port["powerFactor"]

    shell = "rrdtool updatev {}.rrd N:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(
      DB,
      PortA_V, PortA_I, PortA_PF,
      PortB_V, PortB_I, PortB_PF,
      SPI1_V, SPI1_I, SPI1_PF,
      SPI2_V, SPI2_I, SPI2_PF)
    system(shell)

def trigger():
  triggerproxy = SERVICE.get_proxy()
  while True:
    triggerproxy.SendServerEvent(command)
    sleep(300)

if __name__ == "__main__":
    new_thread = Thread(target=trigger)
    new_thread.start()
    proxy = SERVICE.get_proxy()
    proxy.StatusReportOccurred.connect(callback)
    loop = EventLoop()
    loop.run()

