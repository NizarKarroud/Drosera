from twisted.conch.ssh.factory import SSHFactory
from twisted.conch.ssh.keys import Key
from twisted.cred.portal import Portal
from authchecker import AuthChecker
from honeyrealm import HoneyRealm
from twisted.conch.ssh import connection


from authserver import CustomSSHUserAuthServer

class SSHPOT(SSHFactory):
    def __init__(self, logger):
        self.publicKeys = {
            b'ssh-rsa': Key.fromFile('ssh_host_rsa_key.pub')
        }
        self.privateKeys = {
            b'ssh-rsa': Key.fromFile('ssh_host_rsa_key')
        }

        self.portal = Portal(HoneyRealm(logger))
        self.portal.registerChecker(AuthChecker("passw.txt"))

        self.services = {
            b'ssh-userauth': lambda: CustomSSHUserAuthServer(self.portal, logger),
            b'ssh-connection': connection.SSHConnection
        }
        
        super().__init__()
