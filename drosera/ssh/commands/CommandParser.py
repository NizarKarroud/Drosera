import shlex
import argparse
import importlib

class CommandParser:
    def __init__(self , fake_shell):
        self.fake_shell = fake_shell
    
    def parse(self,command : str) -> list :
        try : 
            args = shlex.split(command)
            return args
        except Exception as e :
            return ''
        
    def call(self , cmd : list ):
        try : 
            prog = cmd[0]

            
            module = importlib.import_module(f"drosera.ssh.commands.linux.{prog}")
            prog_func = getattr(module , prog , None )
            instance = prog_func(cmd[1:])
            output = instance.run()
            self.fake_shell.terminal.write(output)

        except (ModuleNotFoundError, AttributeError) as e:
            self.fake_shell.terminal.write(f"Command '{prog}' not found\n")



    