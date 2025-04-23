from twisted.protocols.basic import LineReceiver

class FakeExecProtocol(LineReceiver):
    def __init__(self):
        pass