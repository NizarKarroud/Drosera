import argparse


class cd :
    def __init__(self, args , shell ):
        self.args = args
        self.shell = shell

        self.parser = argparse.ArgumentParser(
            prog='cd',
            add_help=False,  # Disable the default help
            description='Change the shell working directory'
        )

        self.parser.add_argument(
    'dir',
    nargs='?',  # Optional positional argument
    default=None,
    help='Target directory to change into'
)

        self.parser.add_argument(
            '--help', 
            action='store_true'
        )


    def help(self):
        custom_help = """
cd: cd [-L|[-P [-e]] [-@]] [dir]
    Change the shell working directory.

    Change the current directory to DIR.  The default DIR is the value of the 
    HOME shell variable.

    The variable CDPATH defines the search path for the directory containing  
    DIR.  Alternative directory names in CDPATH are separated by a colon (:). 
    A null directory name is the same as the current directory.  If DIR begins
    with a slash (/), then CDPATH is not used.

    If the directory is not found, and the shell option `cdable_vars' is set, 
    the word is assumed to be  a variable name.  If that variable has a value,
    its value is used for DIR.

    Options:
      -L        force symbolic links to be followed: resolve symbolic
                links in DIR after processing instances of `..'
      -P        use the physical directory structure without following        
                symbolic links: resolve symbolic links in DIR before
                processing instances of `..'
      -e        if the -P option is supplied, and the current working
                directory cannot be determined successfully, exit with
                a non-zero status
      -@        on systems that support it, present a file with extended
                attributes as a directory containing the file attributes

    The default is to follow symbolic links, as if `-L' were specified.
    `..' is processed by removing the immediately previous pathname component
    back to a slash or the beginning of DIR.

    Exit Status:
    Returns 0 if the directory is changed, and if $PWD is set successfully when
    -P is used; non-zero otherwise.
"""
        return custom_help
    

    
    def run(self):
        try:
            # Ignore if the input contains pipe or redirection
            if any(sym in self.args for sym in ['|', '>', '>>', '<']):
                return

            args, unknown = self.parser.parse_known_args(self.args)
            if unknown:
                error_msg = f"cd: unrecognized option '{unknown[0]}'\nTry 'cd --help' for more information.\n"
                self.shell.terminal.write(error_msg)
                return
            
            if args.help:
                return self.help()
            
            elif args.dir is None or  args.dir == "~" :
                self.shell.current_dir = "~"
                return

            else :
                path = self.shell.normalize_path(str(args.dir))
                if self.shell.verify_path(path) :
                    path_str = "/".join(path)
                    if path_str.startswith("/home/nizar"):
                        path_str = path_str.replace("/home/nizar", "~", 1)

                    self.shell.current_dir = path_str
                    return
                else : 
                    return f"-bash: cd: {args.dir}: No such file or directory\n"
        except SystemExit as e:
            # Suppress argparse's default exit
            pass


