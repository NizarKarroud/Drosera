from twisted.cred.portal import IRealm
from twisted.conch.avatar import ConchUser
from twisted.conch.interfaces import ISession , IConchUser
from twisted.conch.ssh.session import SSHSession
from zope.interface import implementer
from datetime import datetime, timezone

from twisted.conch.insults import insults
from twisted.internet import defer
from FakeShell import FakeShellProtocol

import time

@implementer(IRealm)
class HoneyRealm:
    def __init__(self, logger):
        self.logger = logger

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IConchUser not in interfaces:
            raise NotImplementedError("HoneyRealm only supports IConchUser interface.")
        
        user = ConchUser()
        user.username = avatarId.decode()
                
        def session_factory(*args, **kwargs):
            return HoneySession(*args, logger=self.logger, **kwargs)

        user.channelLookup[b'session'] = session_factory
        return IConchUser, user, lambda: None

class HoneySession(SSHSession):
    def __init__(self, avatar, *args, logger=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.avatar = avatar
        self.username = avatar.username
        self.protocol = None  
        self.logger = logger
        
    def openShell(self, protocol):
        self.protocol = protocol  
        self.protocol.makeConnection(self)



    def channelOpen(self, specificData):
        peer = self.getPeer().address  
        host = self.getHost().address  


        self.peer = (peer.host, peer.port)
        self.host = (host.host, host.port)

        self.start_time = datetime.now(timezone.utc)

        shell_protocol = insults.ServerProtocol(FakeShellProtocol ,session=self , logger =self.logger)
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
        pass

    def closed(self):
        ip , port = self.peer
        duration = (datetime.now(timezone.utc) - self.start_time).total_seconds()

        self.logger.log_event(f"Session closed at {time.ctime()} {self.username}")

        self.logger.log_logout(ip , port , self.username , duration)
