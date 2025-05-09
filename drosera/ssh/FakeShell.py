from twisted.conch.recvline import HistoricRecvLine
from twisted.conch.insults.insults import ITerminalProtocol
from zope.interface import implementer
from drosera.ssh.commands.CommandParser import CommandParser
import json 

@implementer(ITerminalProtocol)
class FakeShellProtocol(HistoricRecvLine):


    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ssh_session = session
        self.username = session.username
        self.current_dir = "~"
        self.command_parser = CommandParser(self)
        self.identity = ""
        self.ssh_server = session.host
        self.client = session.peer
        with open("drosera\\ssh\\FS\\files\\directory_tree.json") as fs :
            self.fs = json.load(fs)

    def connectionMade(self):
        HistoricRecvLine.connectionMade(self)
        self.terminal.write("""
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.11.0-24-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

Expanded Security Maintenance for Applications is not enabled.

237 updates can be applied immediately.
To see these additional updates run: apt list --upgradable    

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status
                            
Last login: Tue Apr 30 20:33:57 2025 from 26.102.246.130\n""")
        
        self.showPrompt()

    def showPrompt(self):
        if self.username == "root":
            self.identity = f"root@{self.ssh_server[0]}:{self.current_dir}# "    
        else :
            self.identity = f"{self.username}@{self.ssh_server[0]}:{self.current_dir}$ "    

        self.terminal.write(self.identity)

    def lineReceived(self, line):
        line = line.decode('utf-8').strip()
        if line == "exit":
            self.terminal.write("Bye!\n")
            self.terminal.loseConnection()
            return
        elif line == "clear":
            self.terminal.write("\x1b[2J\x1b[H")
            self.showPrompt()

            return
        cmd_list = self.command_parser.parse(line)
        self.command_parser.call(cmd_list)

        self.showPrompt()

    def verify_path(self , path : list) -> bool : 
        if not path:
            return True

        current = self.fs
        for part in path:
            if part not in current:
                return False
            current = current[part]
        return True


    def normalize_path(self , path_str):
        if path_str.startswith('/'):
            # Absolute path
            path_parts = path_str.rstrip('/').split('/')
            return path_parts
        
        elif path_str.startswith('~'):
            # Home path
            sub_path = path_str[1:].strip('/')
            return ['', 'home', 'nizar'] + (sub_path.split('/') if sub_path else [])
        
        else:
            # Relative path
            if self.current_dir == "~":
                self.current_dir = "/home/nizar/"

            path_parts = self.current_dir+ path_str
            
            return path_parts.rstrip("/").split('/')