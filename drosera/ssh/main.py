import warnings
import os
from twisted.internet import reactor

from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore" , category=CryptographyDeprecationWarning) 

from sshfactory import SSHPOT
from logger import Logger 


SSH_PORT = int(os.getenv("SSH_PORT", "2222"))

pot= SSHPOT(Logger())

reactor.listenTCP(SSH_PORT, pot, interface="0.0.0.0")
reactor.run()
