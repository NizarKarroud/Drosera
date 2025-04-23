from twisted.cred.portal import IRealm
from twisted.conch.avatar import ConchUser
from twisted.conch.interfaces import ISession , IConchUser
from twisted.conch.ssh.session import SSHSession
from zope.interface import implementer


from honeychannel import HoneyChannel
import time

@implementer(IRealm)
class HoneyRealm:
    def requestAvatar(self, avatarId, mind, *interfaces):
        if IConchUser not in interfaces:
            raise NotImplementedError("HoneyRealm only supports IConchUser interface.")
        
        user = ConchUser()
        user.channelLookup[b'session'] = HoneySession  
        return ISession, HoneySession(user), lambda: None


@implementer(ISession)
class HoneySession(SSHSession):
    def __init__(self, avatar):
        super().__init__()
        self.avatar = avatar
        self.channelLookup = {
            b'session': HoneyChannel,  
        }

    def openShell(self, proto):
        print("Opening fake shell...")


        

    def execCommand(self, proto, cmd):

        pass

    def lookupChannel(self, channelType, windowSize, maxPacket, packet):

        if channelType == b'session':
            self.channel = HoneyChannel(self)  
            return self.channel

        raise AttributeError(f"Unknown channel type: {channelType}")


    def closed(self):
        print(f"[-] Session closed at {time.ctime()}")