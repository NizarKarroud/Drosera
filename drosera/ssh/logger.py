import logging
import colorlog
import string 
import json
from datetime import datetime, timezone
from pathlib import Path

class Logger :
    def __init__(self):

        self.log_format = '[+] %(log_color)s%(asctime)s - %(levelname)s - %(message)s'
        self.date_format = '%Y-%m-%d %H:%M:%S'

        self.logger = colorlog.getLogger()
        self.handler = logging.StreamHandler()

        self.formatter = colorlog.ColoredFormatter(
            self.log_format, datefmt=self.date_format,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )

        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)

        self.log_file = Path("/var/log/honeypot.json")
        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            if not self.log_file.exists():
                self.log_file.touch()
        except Exception as e:
            self.logger.error(f"Could not create log file: {e}")


    def log_event(self , event : str , type:str = "info"):
        log_method = getattr(self.logger, type , self.logger.info)

        if callable(log_method):
            log_method(event)



    def log_connection(self , ip , port , credentials , status ):
        with open(self.log_file, "a") as f:
            log = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ip": ip,
                "port": port,
                "event": "ssh logging attempt",
                "protocol": "ssh",
                "fields": {
                    "username": credentials[0],
                    "password": "".join(c for c in  credentials[1] if c in string.printable).strip(),
                    "status": status
                }
            }            
            f.write(json.dumps(log) + '\n')


    def log_logout(self , ip , port , username , duration):
        with open(self.log_file, "a") as f:
            log = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ip": ip,
                "port": port,
                "event": "ssh session closure",
                "protocol": "ssh",
                "fields": {
                    "username": username,
                    "duration" : duration
                }
            }            
            f.write(json.dumps(log) + '\n')
