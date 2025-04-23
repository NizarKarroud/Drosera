from twisted.protocols.basic import LineReceiver

class FakeShellProtocol(LineReceiver):
    def connectionMade(self):
        self.transport.write(b"Welcome to fake shell\n$ ")

    def lineReceived(self, line):
        response = f"You typed: {line.decode()}\n$ "
        self.transport.write(response.encode())
