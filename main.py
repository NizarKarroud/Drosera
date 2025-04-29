from twisted.internet import reactor
import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore" , category=CryptographyDeprecationWarning) 

from drosera.ssh.sshfactory import SSHPOT

pot= SSHPOT()

reactor.listenTCP(2222, pot, interface="0.0.0.0")
reactor.run()
