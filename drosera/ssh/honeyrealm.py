from twisted.cred.portal import IRealm
from twisted.conch.avatar import ConchUser
from twisted.conch.interfaces import ISession , IConchUser
from twisted.conch.ssh.session import SSHSession
from zope.interface import implementer

from twisted.conch.insults import insults
from twisted.internet import defer
from drosera.ssh.FakeShell import FakeShellProtocol

import time

@implementer(IRealm)
class HoneyRealm:
    def requestAvatar(self, avatarId, mind, *interfaces):
        if IConchUser not in interfaces:
            raise NotImplementedError("HoneyRealm only supports IConchUser interface.")
        
        user = ConchUser()
        user.channelLookup[b'session'] = HoneySession
        return IConchUser, user, lambda: None

class HoneySession(SSHSession):
    def __init__(self, avatar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.avatar = avatar
        self.protocol = None  

    def openShell(self, protocol):
        print("Opening fake shell...")
        self.protocol = protocol  
        self.protocol.makeConnection(self)

    def channelOpen(self, specificData):
        print("Channel opened successfully")
        
        shell_protocol = insults.ServerProtocol(FakeShellProtocol)
        self.openShell(shell_protocol)


    def request_pty_req(self, data):
        print("Received pty-req request")
        return defer.succeed(True)

    def request_shell(self, data):
        print("Received shell request")

        return defer.succeed(True)
    
    def request_exec(self, data):
        command = ''.join(chr(b) for b in data if 32 <= b <= 126)

        "i should parse the command and "
        print(f"Received exec request: {command}")
        return defer.succeed(True)
        
    def dataReceived(self, data):
        if self.protocol:
            self.protocol.dataReceived(data)
            
    def write(self, data):
        self.conn.sendData(self, data)

    def loseConnection(self):
        self.conn.sendClose(self)

    def eofReceived(self):
        print("EOF received")

    def closed(self):
        print(f"[-] Session closed at {time.ctime()}")
