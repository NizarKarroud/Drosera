import logging
import colorlog
import requests , os

import json
from datetime import datetime, timezone
from pathlib import Path

# Ensure log directory exists

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
        self.log_file.parent.mkdir(exist_ok=True)

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
                    "password": credentials[1],
                    "status": status
                }
            }            
            f.write(json.dumps(log) + '\n')

        self.logger.info(
            f"SSH login attempt from {ip}:{port} - Username: {credentials[0]} | Password: {credentials[1]} | Status: {status}"
        )




# ip_api=os.getenv('IPINFO_API_KEY')
# response = requests.get(f"https://ipinfo.io/8.8.8.8/json?token={ip_api}")
# data = response.json()
# print(data)





