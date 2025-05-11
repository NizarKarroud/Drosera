
import argparse


class history :
    def __init__(self, args , shell ):
        self.args = args
        self.shell = shell

        self.parser = argparse.ArgumentParser(
            prog='history',
            add_help=False,  # Disable the default help
        )

        self.parser.add_argument(
            '--help', 
            action='store_true'
        )



    def help(self):
        custom_help = """
history: history [-c] [-d offset] [n] or history -anrw [filename] or history -ps arg [arg...]
    Display or manipulate the history list.

    Display the history list with line numbers, prefixing each modified
    entry with a `*'.  An argument of N lists only the last N entries.

    Options:
      -c        clear the history list by deleting all of the entries
      -d offset delete the history entry at position OFFSET. Negative
                offsets count back from the end of the history list

      -a        append history lines from this session to the history file
      -n        read all history lines not already read from the history file
                and append them to the history list
      -r        read the history file and append the contents to the history
                list
      -w        write the current history to the history file

      -p        perform history expansion on each ARG and display the result
                without storing it in the history list
      -s        append the ARGs to the history list as a single entry

    If FILENAME is given, it is used as the history file.  Otherwise,
    if HISTFILE has a value, that is used, else ~/.bash_history.

    If the HISTTIMEFORMAT variable is set and not null, its value is used
    as a format string for strftime(3) to print the time stamp associated
    with each displayed history entry.  No time stamps are printed otherwise.

    Exit Status:
    Returns success unless an invalid option is given or an error occurs.
"""
        return custom_help


    def run(self):
        try:
            # Ignore if the input contains pipe or redirection
            if any(sym in self.args for sym in ['|', '>', '>>', '<']):
                return

            args, unknown = self.parser.parse_known_args(self.args)
            if unknown:
                error_msg = f"history: unrecognized option '{unknown[0]}'\nTry 'history --help' for more information.\n"
                self.shell.terminal.write(error_msg)
                return
            
            if args.help:
                return self.help()

            else :
                history = ""
                for index , cmd  in enumerate(self.shell.historyLines , start=1) :
                        history += f"   {index}  {cmd.decode('utf-8')}\n"
                        

                return self.shell.terminal.write(history)

        except SystemExit as e:
        # Suppress argparse's default exit
            pass
