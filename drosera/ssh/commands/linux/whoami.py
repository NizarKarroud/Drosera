import argparse

class whoami :
    def __init__(self, args , shell ):
        self.args = args
        self.shell = shell

        self.parser = argparse.ArgumentParser(
            prog='whoami',
            add_help=False,  # Disable the default help
            description='Print the user name associated with the current effective user ID.'
        )


        self.parser.add_argument(
            '--help', 
            action='store_true'
        )


    def help(self):
        custom_help = """
Usage: whoami [OPTION]...
Print the user name associated with the current effective user ID.   
Same as id -un.

      --help     display this help and exit
      --version  output version information and exit

GNU coreutils online help: <https://www.gnu.org/software/coreutils/> 
Report any translation bugs to <https://translationproject.org/team/>
Full documentation <https://www.gnu.org/software/coreutils/whoami>   
or available locally via: info '(coreutils) whoami invocation'     
"""
        return custom_help
    

    
    def run(self):
        try:
            # Ignore if the input contains pipe or redirection
            if any(sym in self.args for sym in ['|', '>', '>>', '<']):
                return

            args, unknown = self.parser.parse_known_args(self.args)
            if unknown:
                error_msg = f"whoami: unrecognized option '{unknown[0]}'\nTry 'whoami --help' for more information.\n"
                self.shell.terminal.write(error_msg)
                return
            
            if args.help:
                return self.help()
            

            else :
                return f'{self.shell.username}\n'

        except SystemExit as e:
            # Suppress argparse's default exit
            pass


