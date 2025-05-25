from twisted.conch.ssh.userauth import SSHUserAuthServer

class CustomSSHUserAuthServer(SSHUserAuthServer):
    def __init__(self, portal, logger):
        self.portal = portal
        self.logger = logger
        super().__init__()

    def serviceStarted(self):
        self.logger.log_event("SSH Auth Service started.")
        super().serviceStarted()

    def ssh_USERAUTH_REQUEST(self, packet):
        peer = self.transport.getPeer()
        client_ip = peer.address.host
        client_port = peer.address.port

        self.logger.log_event(f"Auth request received: {packet}")
        self.logger.log_event(f"{client_ip} , {client_port}" , type="qs")


        return super().ssh_USERAUTH_REQUEST(packet)