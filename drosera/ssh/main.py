import warnings
import os
from twisted.internet import reactor

from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore" , category=CryptographyDeprecationWarning) 

from sshfactory import SSHPOT

SSH_PORT = int(os.getenv("SSH_PORT", "2222"))
LOG_FILE = os.getenv("LOG_FILE", "/var/log/honeypot.json") 

pot= SSHPOT()

reactor.listenTCP(SSH_PORT, pot, interface="0.0.0.0")
reactor.run()
