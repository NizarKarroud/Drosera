import argparse
import ipaddress
import random
from twisted.internet import reactor

class ping : 
    def __init__(self, args , shell ):
        self.args = args
        self.shell = shell
        self.ip = None
        self.icmp_seq = 1
        self.total_time = 0

        self.parser = argparse.ArgumentParser(
            prog='ping',
            add_help=False,  # Disable the default help
        )

        self.parser.add_argument(
            '-help', 
            action='store_true'
        )

        self.parser.add_argument(
           'ip' ,
            nargs="?"
        )
    
    def help(self):
        custom_help = """
Usage
  ping [options] <destination>

Options:
  <destination>      dns name or ip address
  -a                 use audible ping
  -A                 use adaptive ping
  -B                 sticky source address
  -c <count>         stop after <count> replies
  -D                 print timestamps
  -d                 use SO_DEBUG socket option
  -f                 flood ping
  -h                 print help and exit
  -I <interface>     either interface name or address
  -i <interval>      seconds between sending each packet
  -L                 suppress loopback of multicast packets
  -l <preload>       send <preload> number of packages while waiting replies
  -m <mark>          tag the packets going out
  -M <pmtud opt>     define mtu discovery, can be one of <do|dont|want>     
  -n                 no dns name resolution
  -O                 report outstanding replies
  -p <pattern>       contents of padding byte
  -q                 quiet output
  -Q <tclass>        use quality of service <tclass> bits
  -s <size>          use <size> as number of data bytes to be sent
  -S <size>          use <size> as SO_SNDBUF socket option value
  -t <ttl>           define time to live
  -U                 print user-to-user latency
  -v                 verbose output
  -V                 print version and exit
  -w <deadline>      reply wait <deadline> in seconds
  -W <timeout>       time to wait for response

IPv4 options:
  -4                 use IPv4
  -b                 allow pinging broadcast
  -R                 record route
  -T <timestamp>     define timestamp, can be one of <tsonly|tsandaddr|tsprespec>

IPv6 options:
  -6                 use IPv6
  -F <flowlabel>     define flow label, default is random
  -N <nodeinfo opt>  use icmp6 node info query, try <help> as argument

For more details see ping(8).
"""
        return custom_help

    def simulate_ping_loop(self, ip, latency_range):
        if not getattr(self.shell, 'ping_active', True):  # Exit if ping was canceled
            return

        latency = random.uniform(*latency_range)
        self.shell.terminal.write(
            f"64 bytes from {ip}: icmp_seq={self.icmp_seq} ttl=64 time={latency:.1f} ms\n"
        )
        self.icmp_seq += 1
        self.total_time += latency
        
        self.shell.active_task = reactor.callLater(1, self.simulate_ping_loop, ip, latency_range)        

    def print_stats(self):
        stats = (
            f"\n--- {self.ip} ping statistics ---\n"
            f"{self.icmp_seq-1} packets transmitted, {self.icmp_seq -1} received, 0% packet loss, time {self.total_time}ms\n"
        )
        self.shell.terminal.write(stats)

    def run(self):

        try:
            # Ignore if the input contains pipe or redirection
            if any(sym in self.args for sym in ['|', '>', '>>', '<']):
                return

            args, unknown = self.parser.parse_known_args(self.args)
            if unknown:
                error_msg = f"ping: unrecognized option '{unknown[0]}'\nTry 'ping -help' for more information.\n"
                return error_msg
            
            if args.help:
                return self.help()
            
            if not args.ip:
                return "ping: usage error: Destination address required\n"

            try:
                ip = ipaddress.ip_address(args.ip)
                self.ip = ip
                self.shell.terminal.write(f"PING {ip} ({ip}) 56(84) bytes of data.\n")
                
                self.shell.ping_active = True
                self.shell.current_ping_instance = self

                self.simulate_ping_loop(ip, latency_range=(0.3, 1.2) if ip.is_private else (20.0, 80.0))
                
            except ValueError:
                return f"ping: {args.ip}: Name or service not known\n"

        except SystemExit as e:
        # Suppress argparse's default exit
            pass