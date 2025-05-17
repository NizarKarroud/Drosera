from zope.interface import implementer
from twisted.cred.checkers import FilePasswordDB, ICredentialsChecker
from twisted.cred.credentials import IUsernamePassword
from twisted.cred.error import UnauthorizedLogin

import json
import time
from pathlib import Path

# Ensure log directory exists
LOG_FILE = Path("/var/log/honeypot.json")
LOG_FILE.parent.mkdir(exist_ok=True)

def log_attack(ip, username, password):
    log_entry = {
        "timestamp": time.time(),
        "ip": ip,
        "event": "ssh_login_attempt",
        "username": username,
        "password": password  # Warning: Avoid logging sensitive data in production
    }
    
    # Append JSON line to file
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

@implementer(ICredentialsChecker)
class AuthChecker(FilePasswordDB):
    credentialInterfaces = (IUsernamePassword,)

    def __init__(self, filename, delim=b":", usernameField=0, passwordField=1, caseSensitive=True, hash=None, cache=False):
        super().__init__(filename, delim, usernameField, passwordField, caseSensitive, hash, cache)

    def requestAvatarId(self, credentials):
        try:
            username, expected_password = self.getUser(credentials.username)
            log_attack("192.168.100.4", username.decode(), credentials.password.decode())
            if credentials.password == expected_password:
                
                print(f"[+] LOGIN SUCCESS: {username.decode()} : {expected_password.decode()}")
                return username  
            else:
                print(f"[-] LOGIN FAILED (bad password): {credentials.username.decode()}")
                raise UnauthorizedLogin("Invalid password")
        except KeyError:
            print(f"[-] LOGIN FAILED (unknown user): {credentials.username.decode()}")
            raise UnauthorizedLogin("No such user")
