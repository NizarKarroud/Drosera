import argparse


class curl :
    def __init__(self, args , shell ):
        self.args = args
        self.shell = shell

        self.parser = argparse.ArgumentParser(
            prog='curl',
            add_help=False,  # Disable the default help
        )
        

        self.parser.add_argument(
            '--help', 
            action='store_true'
        )

        self.parser.add_argument(
            'url',
            nargs="?"
        )



    def help(self):
        custom_help = """
Usage: curl [options...] <url>
 -d, --data <data>          HTTP POST data
 -f, --fail                 Fail silently (no output at all) on HTTP errors
 -h, --help <category>      Get help for commands
 -i, --include              Include protocol response headers in the output
 -o, --output <file>        Write to file instead of stdout
 -O, --remote-name          Write output to a file named as the remote file
 -s, --silent               Silent mode
 -T, --upload-file <file>   Transfer local FILE to destination
 -u, --user <user:password> Server user and password
 -A, --user-agent <name>    Send User-Agent <name> to server
 -v, --verbose              Make the operation more talkative
 -V, --version              Show version number and quit

This is not the full help, this menu is stripped into categories.
Use "--help category" to get an overview of all categories.
For all options use the manual or "--help all".
"""
        return custom_help

    def run(self):

        try:
            # Ignore if the input contains pipe or redirection
            if any(sym in self.args for sym in ['|', '>', '>>', '<']):
                return

            args, unknown = self.parser.parse_known_args(self.args)
            if unknown:
                error_msg = f"curl: unrecognized option '{unknown[0]}'\nTry 'curl --help' for more information.\n"
                self.shell.terminal.write(error_msg)
                return
            
            if args.help :
                return self.help()
            
        except SystemExit as e:
        # Suppress argparse's default exit
            pass
