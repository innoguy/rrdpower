from dasbus.loop import EventLoop
from dasbus.connection import SystemMessageBus
from dasbus.identifier import DBusServiceIdentifier
from common import MESSAGE_BUS, SERVICE
import json

SPI1_Port = 'Port A'
SPI1_Index = 1
SPI2_Port = 'Port B'
SPI2_Index = 1

DB="/var/log/cirrus-rrd/power"

def callback(data):
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
    if "spis" in powerdata["data"]["payload"]:
      for port in powerdata["data"]["payload"]["spis"]:
        if (port["portId"]==SPI1_Port and port["id"]==SPI2_Index):
          SPI1_V = port["rmsVoltage"]
          SPI1_I = port["rmsCurrent"]
          SPI1_PF = port["powerFactor"]
        elif (port["portId"] == SPI2_Port and port["id"] == SPI2_Index):
          SPI2_V = port["rmsVoltage"]
          SPI2_I = port["rmsCurrent"]
          SPI2_PF = port["powerFactor"]
    else:
      SPI1_V = 0
      SPI1_I = 0
      SPI1_PF = 0
      SPI2_V = 0
      SPI2_I = 0
      SPI2_PF = 0

    shell = "rrdtool updatev {}.rrd N:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(
              DB,
              PortA_V, PortA_I, PortA_PF,
              PortB_V, PortB_I, PortB_PF,
              SPI1_V, SPI1_I, SPI1_PF,
              SPI2_V, SPI2_I, SPI2_PF
              )
    print(shell)


if __name__ == "__main__":
    proxy = SERVICE.get_proxy()
    proxy.StatusReportOccurred.connect(callback)
    loop = EventLoop()
    loop.run()

