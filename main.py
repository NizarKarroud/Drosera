from twisted.internet import reactor
import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore" , category=CryptographyDeprecationWarning) 

from sshfactory import SSHPOT

pot= SSHPOT()

reactor.listenTCP(2222, pot, interface="127.0.0.1")
reactor.run()
