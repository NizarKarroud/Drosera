from twisted.conch.ssh.factory import SSHFactory
from twisted.conch.ssh.keys import Key
from twisted.cred.portal import Portal
from authchecker import AuthChecker
from honeyrealm import HoneyRealm

class SSHPOT(SSHFactory):
    def __init__(self):
        self.publicKeys = {
            b'ssh-rsa': Key.fromFile('ssh_host_rsa_key.pub')
        }
        self.privateKeys = {
            b'ssh-rsa': Key.fromFile('ssh_host_rsa_key')
        }
        super().__init__()
        self.portal = Portal(HoneyRealm())
        self.portal.registerChecker(AuthChecker("passw.txt"))
