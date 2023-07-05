from dasbus.connection import SystemMessageBus
from dasbus.identifier import DBusServiceIdentifier

MESSAGE_BUS = SystemMessageBus()
SERVICE = DBusServiceIdentifier(
        namespace = ("com", "cirrusled", "Nucleus1"),
        message_bus = MESSAGE_BUS
)

command = '''
{"data":{"playerId":"00000000-0000-0000-0000-000000000000","topic":"CONTROLLER_COMMAND","payload":{"requestId":"123456789","portId":"","command":"REPORT_STATUS"}}}
'''