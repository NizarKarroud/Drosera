from twisted.protocols.basic import LineReceiver
import time

class FakeShellProtocol(LineReceiver):

    def __init__(self):
        pass