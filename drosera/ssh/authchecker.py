from zope.interface import implementer
from twisted.cred.checkers import FilePasswordDB, ICredentialsChecker
from twisted.cred.credentials import IUsernamePassword
from twisted.cred.error import UnauthorizedLogin




@implementer(ICredentialsChecker)
class AuthChecker(FilePasswordDB):
    credentialInterfaces = (IUsernamePassword,)

    def __init__(self, filename , delim=b":", usernameField=0, passwordField=1, caseSensitive=True, hash=None, cache=False):
        super().__init__(filename, delim, usernameField, passwordField, caseSensitive, hash, cache)

    def requestAvatarId(self, credentials):
        try:
            username, expected_password = self.getUser(credentials.username)
            if credentials.password == expected_password:
                return username  
            else:
                raise UnauthorizedLogin("Invalid password")
        except KeyError:
            raise UnauthorizedLogin("User not found")
