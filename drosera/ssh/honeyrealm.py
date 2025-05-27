from twisted.cred.portal import IRealm
from twisted.conch.avatar import ConchUser
from twisted.conch.interfaces import ISession , IConchUser
from twisted.conch.ssh.session import SSHSession
from zope.interface import implementer

from twisted.conch.insults import insults
from twisted.internet import defer
from FakeShell import FakeShellProtocol

import time

@implementer(IRealm)
class HoneyRealm:
    def requestAvatar(self, avatarId, mind, *interfaces):
        if IConchUser not in interfaces:
            raise NotImplementedError("HoneyRealm only supports IConchUser interface.")
        
        user = ConchUser()
        user.username = avatarId.decode()
        user.channelLookup[b'session'] = HoneySession
        return IConchUser, user, lambda: None

class HoneySession(SSHSession):
    def __init__(self, avatar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.avatar = avatar
        self.username = avatar.username
        self.protocol = None  

    def openShell(self, protocol):
        self.protocol = protocol  
        self.protocol.makeConnection(self)



    def channelOpen(self, specificData):
        peer = self.getPeer().address  
        host = self.getHost().address  


        self.peer = (peer.host, peer.port)
        self.host = (host.host, host.port)
        
        shell_protocol = insults.ServerProtocol(FakeShellProtocol ,session=self)
        self.openShell(shell_protocol)


    def request_pty_req(self, data):
        return defer.succeed(True)

    def request_shell(self, data):
        return defer.succeed(True)
    
    def request_exec(self, data):

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
