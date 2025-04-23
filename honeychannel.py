from twisted.conch.ssh.channel import SSHChannel
from twisted.conch.ssh import session
from twisted.internet import defer
import time
from FakeShell import FakeShellProtocol

class HoneyChannel(SSHChannel):
    def __init__(self ,session):
        super().__init__()
        self.session = session 

    def channelOpen(self, specificData):

        print("Channel opened successfully")
    

    def requestReceived(self, requestType, data):

        if requestType == b'pty-req':
            print("Received pty-req request")
            return defer.succeed(True)
        
        elif requestType == b'shell':
            print("Received shell request")  


            return defer.succeed(True)
        
        elif requestType == b'exec':
            print(f"Received exec request: {data}")
            return defer.succeed(True)
        else:
            print(f"Unknown request type: {requestType}")
            return defer.fail(Exception(f"Unknown request type: {requestType}"))
    
    def dataReceived(self, data):

        print(f"Data received: {data}")

    def eofReceived(self):
        print("EOF received")

    def closed(self):
        print(f"[-] Session closed at {time.ctime()}")
