from dasbus.connection import SystemMessageBus
from dasbus.identifier import DBusServiceIdentifier

MESSAGE_BUS = SystemMessageBus()
SERVICE = DBusServiceIdentifier(
        namespace = ("com", "cirrusled", "Nucleus1"),
        message_bus = MESSAGE_BUS
)

