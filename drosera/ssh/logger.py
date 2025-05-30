import logging
import colorlog
import string 
import json
from datetime import datetime, timezone
from pathlib import Path
import requests 


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


    def get_geo(self , ip ):
        try:
            res = requests.get(f"https://ipinfo.io/{ip}/json")
            if res.status_code == 200:
                data = res.json()
                if data.get("bogon" ,"") == True:
                    return {}
                return {
                    "city": data.get("city"),
                    "country": data.get("country"),
                    "loc": data.get("loc"), 
                    "org": data.get("org"),
                    "postal": data.get("postal"),
                    "timezone": data.get("timezone")
                }
        except Exception as e:
            self.log_event(f"GeoIP lookup failed for {ip}: {e}")
        return {}
    
    def log_event(self , event : str , type:str = "info"):
        log_method = getattr(self.logger, type , self.logger.info)

        if callable(log_method):
            log_method(event)



    def log_connection(self , ip , port , credentials , status ):
        geo = self.get_geo(ip)

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
                },
                "geo": geo  

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
                },
                "geo": {}  
    
            }            
            f.write(json.dumps(log) + '\n')

    def log_command(self , ip , port , username , command , directory  , args=""):
        with open(self.log_file, "a") as f:
            log = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ip": ip,
                "port": port,
                "event": "ssh command execution",
                "protocol": "ssh",
                "fields": {
                    "username": username,
                    "directory" : directory,
                    "command" : command,
                    "args" : args
                },
                "geo": {}  
            }            
            f.write(json.dumps(log) + '\n')
