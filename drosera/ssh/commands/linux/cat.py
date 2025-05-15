import argparse



class cat :
    def __init__(self, args , shell ):
        self.args = args
        self.shell = shell

        self.parser = argparse.ArgumentParser(
            prog='cat',
            add_help=False,  # Disable the default help
        )

        self.parser.add_argument(
    'file',
    nargs='?',  # Optional positional argument
)

        self.parser.add_argument(
            '--help', 
            action='store_true'
        )


    def help(self):
        custom_help = """
Usage: cat [OPTION]... [FILE]...
Concatenate FILE(s) to standard output.

With no FILE, or when FILE is -, read standard input.

  -A, --show-all           equivalent to -vET
  -b, --number-nonblank    number nonempty output lines, overrides -n
  -e                       equivalent to -vE
  -E, --show-ends          display $ at end of each line
  -n, --number             number all output lines
  -s, --squeeze-blank      suppress repeated empty output lines      
  -t                       equivalent to -vT
  -T, --show-tabs          display TAB characters as ^I
  -u                       (ignored)
  -v, --show-nonprinting   use ^ and M- notation, except for LFD and TAB
      --help     display this help and exit
      --version  output version information and exit

Examples:
  cat f - g  Output f's contents, then standard input, then g's contents.
  cat        Copy standard input to standard output.

GNU coreutils online help: <https://www.gnu.org/software/coreutils/>
Report any translation bugs to <https://translationproject.org/team/>
Full documentation <https://www.gnu.org/software/coreutils/cat>
or available locally via: info '(coreutils) cat invocation'
"""
        return custom_help
    

    
    def run(self):
        try:
            # Ignore if the input contains pipe or redirection
            if any(sym in self.args for sym in ['|', '>', '>>', '<']):
                return

            args, unknown = self.parser.parse_known_args(self.args)
            if unknown:
                error_msg = f"cat: unrecognized option '{unknown[0]}'\nTry 'cat --help' for more information.\n"
                self.shell.terminal.write(error_msg)
                return
            
            if args.help:
                return self.help()
            

            if args.file and  (args.file.startswith("/") or args.file.startswith("~") ):
                path = args.file
            elif args.file:
                path = f"{self.shell.current_dir}/{args.file}"
            else:
                return '\n'
                
            formated_path = self.shell.normalize_path(path) 
            listed = self.shell.verify_path(formated_path)
               
            if isinstance(listed[0] , str) :
                with open(listed[0] , "r") as f:
                    return f"{f.read()}\n"
                
            elif listed[0] == None :
                return "\n"
            
            elif not listed[0] and listed[1] == False :
                return f"cat: {args.file}: No such file or directory\n"  
            else : 
                return f"cat : {args.file}: Is a directory\n"
        except SystemExit as e:
            # Suppress argparse's default exit
            pass


