from twisted.conch.recvline import HistoricRecvLine
from twisted.conch.insults.insults import ITerminalProtocol
from zope.interface import implementer
from drosera.ssh.commands.CommandParser import CommandParser

@implementer(ITerminalProtocol)
class FakeShellProtocol(HistoricRecvLine):

    def connectionMade(self):
        HistoricRecvLine.connectionMade(self)
        self.command_parser = CommandParser(self)
        self.terminal.write("Welcome to RageBait shell\n")
        self.showPrompt()

    def showPrompt(self):
        self.terminal.write("$ ")

    def lineReceived(self, line):
        line = line.decode('utf-8').strip()
        if line == "exit":
            self.terminal.write("Bye!\n")
            self.terminal.loseConnection()
            return
        cmd_list = self.command_parser.parse(line)
        self.command_parser.call(cmd_list)

        self.showPrompt()
