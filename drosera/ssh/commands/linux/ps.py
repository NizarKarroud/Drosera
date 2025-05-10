
import argparse


class ps :
    def __init__(self, args , shell ):
        self.args = args
        self.shell = shell

        self.parser = argparse.ArgumentParser(
            prog='ps',
            add_help=False,  # Disable the default help
        )

        self.parser.add_argument(
            '--help', 
            action='store_true'
        )



    def help(self):
        custom_help = """
Usage:
 ps [options]

 Try 'ps --help <simple|list|output|threads|misc|all>'     
  or 'ps --help <s|l|o|t|m|a>'
 for additional help text.

For more details see ps(1).
"""
        return custom_help


    def run(self):

        try:
            # Ignore if the input contains pipe or redirection
            if any(sym in self.args for sym in ['|', '>', '>>', '<']):
                return

            args, unknown = self.parser.parse_known_args(self.args)
            if unknown:
                error_msg = f"ps: unrecognized option '{unknown[0]}'\nTry 'ps --help' for more information.\n"
                self.shell.terminal.write(error_msg)
                return
            
            if args.help:
                return self.help()
            

            else :
                ps_infos ="""
PID TTY          TIME CMD
1 ?        00:00:01 systemd
55 ?        00:00:00 sshd
105 ?        00:00:00 cron
120 ?        00:00:00 rsyslogd
130 ?        00:00:00 systemd-logind
145 ?        00:00:00 dbus-daemon
180 ?        00:00:00 nginx
200 ?        00:00:00 apache2
205 ?        00:00:00 apache2
206 ?        00:00:00 apache2
220 ?        00:00:00 mysqld
230 ?        00:00:00 python3
240 ?        00:00:00 bash
260 ?        00:00:00 top
270 ?        00:00:00 netcat
397 pts/0    00:00:00 bash
474 pts/0    00:00:00 ps
"""
                return self.shell.terminal.write(ps_infos)


        except SystemExit as e:
        # Suppress argparse's default exit
            pass
