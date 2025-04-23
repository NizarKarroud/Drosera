from zope.interface import implementer
from twisted.cred.checkers import FilePasswordDB, ICredentialsChecker
from twisted.cred.credentials import IUsernamePassword
from twisted.cred.error import UnauthorizedLogin

@implementer(ICredentialsChecker)
class AuthChecker(FilePasswordDB):
    credentialInterfaces = (IUsernamePassword,)

    def __init__(self, filename, delim=b":", usernameField=0, passwordField=1, caseSensitive=True, hash=None, cache=False):
        super().__init__(filename, delim, usernameField, passwordField, caseSensitive, hash, cache)

    def requestAvatarId(self, credentials):
        try:
            username, expected_password = self.getUser(credentials.username)
            if credentials.password == expected_password:
                
                print(f"[+] LOGIN SUCCESS: {username.decode()} : {expected_password.decode()}")
                return username  
            else:
                print(f"[-] LOGIN FAILED (bad password): {credentials.username.decode()}")
                raise UnauthorizedLogin("Invalid password")
        except KeyError:
            print(f"[-] LOGIN FAILED (unknown user): {credentials.username.decode()}")
            raise UnauthorizedLogin("No such user")
