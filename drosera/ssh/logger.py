import logging
import colorlog

LOG_FORMAT = '[+] %(log_color)s%(asctime)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logger = colorlog.getLogger()
handler = logging.StreamHandler()

formatter = colorlog.ColoredFormatter(
    LOG_FORMAT, datefmt=DATE_FORMAT,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)



