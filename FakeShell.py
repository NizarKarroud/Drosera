from twisted.conch.recvline import HistoricRecvLine
from twisted.conch.insults.insults import ITerminalProtocol
from zope.interface import implementer

@implementer(ITerminalProtocol)
class FakeShellProtocol(HistoricRecvLine):

    def connectionMade(self):
        HistoricRecvLine.connectionMade(self)
        self.terminal.write("Welcome to RageBait shell\n")
        self.showPrompt()

    def showPrompt(self):
        self.terminal.write("$ ")

    def lineReceived(self, line):
        line = line.decode('utf-8').strip()
        print(line)
        if line == "exit":
            self.terminal.write("Bye!\n")
            self.terminal.loseConnection()
            return
        self.terminal.write(f"Command not found: {line}\n")
        self.showPrompt()
