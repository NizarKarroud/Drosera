import shlex
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
            args = " ".join(cmd[1:])
            self.fake_shell.logger.log_command( self.fake_shell.client[0] ,  self.fake_shell.client[1] , self.fake_shell.username , prog , self.current_dir , args)

            module = importlib.import_module(f"commands.linux.{prog}")
            prog_func = getattr(module , prog , None )
            instance = prog_func(cmd[1:] , self.fake_shell)
            output = instance.run()
            if output :
                self.fake_shell.terminal.write(output)
                

        except (ModuleNotFoundError, AttributeError) as e:
            self.fake_shell.terminal.write(f"Command '{prog}' not found\n")
            self.fake_shell.showPrompt()


    