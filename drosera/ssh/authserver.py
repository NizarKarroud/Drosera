from twisted.conch.ssh.userauth import SSHUserAuthServer
from twisted.internet.defer import maybeDeferred


class CustomSSHUserAuthServer(SSHUserAuthServer):
    def __init__(self, portal, logger):
        self.portal = portal
        self.logger = logger
        super().__init__()

    def serviceStarted(self):
        self.logger.log_event("SSH Auth Service started.")
        super().serviceStarted()

    def tryAuth(self, kind, user, data):
        peer = self.transport.getPeer()
        client_ip = peer.address.host
        client_port = peer.address.port

        if kind.decode() != "none" : 
            self.logger.log_event(
                f"[AUTH] Method: {kind.decode()}, User: {user.decode()}, IP: {client_ip}, Port: {client_port}",
                type="info"
                    )

        d = maybeDeferred(super().tryAuth, kind, user, data)

        def log_result(result):
            self.logger.log_event(
                f"[AUTH SUCCESS] User: {user.decode()} , password: {data.decode()} via {kind.decode()}", type="info"
            )
            self.logger.log_connection( ip = client_ip , port = client_port , credentials  = (user.decode() , data.decode() ), status = "success" )
            return result

        def log_failure(failure):
            if kind.decode() != "none" : 
                self.logger.log_event(
                    f"[AUTH FAIL] User: {user.decode()} , password: {data.decode()} via {kind.decode()} - {failure.getErrorMessage()}",
                    type="warning"
                )
                self.logger.log_connection( ip = client_ip , port = client_port , credentials  = (user.decode() , data.decode() ), status = failure.getErrorMessage() )

            return failure

        d.addCallbacks(log_result, log_failure)
        return d