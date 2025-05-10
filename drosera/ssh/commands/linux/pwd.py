import argparse


class pwd :
    def __init__(self, args , shell ):
        self.args = args
        self.shell = shell

        self.parser = argparse.ArgumentParser(
            prog='pwd',
            add_help=False,  # Disable the default help
            description='Print the name of the current working directory.'
        )

        self.parser.add_argument(
            '--help', 
            action='store_true'
        )




    def help(self):
        custom_help = """
pwd: pwd [-LP]
    Print the name of the current working directory.

    Options:
      -L        print the value of $PWD if it names the current working 
                directory
      -P        print the physical directory, without any symbolic links

    By default, `pwd' behaves as if `-L' were specified.

    Exit Status:
    Returns 0 unless an invalid option is given or the current directory
    cannot be read.
"""
        return custom_help

    def run(self):
        args = self.parser.parse_args(self.args)
        if args.help:
            return self.help()
        else : 
            return self.shell.terminal.write(f"{self.shell.current_dir}\n")

