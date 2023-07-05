import json

data=json.load(open('power.json'))

for port in data["data"]["payload"]["ports"]:
    print(port["id"]+":"+port["rmsVoltage"]+":"+port["rmsCurrent"]+":"+port["activePower"]+":"+port["powerFactor"]+":"+port["reactivePower"]+":"+port["apparentPower"]+":"+port["frequency"])

for port in data["data"]["payload"]["spis"]:
    print(port["portId"]+":"+port["id"]+":"+port["rmsVoltage"]+":"+port["rmsCurrent"]+":"+port["activePower"]+":"+port["powerFactor"]+":"+port["reactivePower"]+":"+port["apparentPower"]+":"+port["frequency"])
