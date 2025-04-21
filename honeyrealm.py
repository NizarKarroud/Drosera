from twisted.cred.portal import IRealm
from twisted.conch.avatar import ConchUser
from twisted.conch.interfaces import ISession
from twisted.conch.ssh.session import SSHSession
from zope.interface import implementer

@implementer(IRealm)
class HoneyRealm:
    def requestAvatar(self, avatarId, mind, *interfaces):
        if ISession in interfaces:
            user = ConchUser()
            user.channelLookup.update({b'session': SSHSession})
            return ISession, user, lambda: None
        raise NotImplementedError("Only ISession interface is supported.")
