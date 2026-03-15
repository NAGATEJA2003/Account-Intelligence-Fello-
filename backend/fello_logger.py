import logging
import os
import sys

# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'logs')

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        # Ensure logs directory exists
        os.makedirs(LOGS_DIR, exist_ok=True)
        log_path = os.path.join(LOGS_DIR, "fello_operations.log")

        fh = logging.FileHandler(log_path, encoding='utf-8')
        # Use StreamHandler with UTF-8 encoding for console output
        try:
            ch = logging.StreamHandler(stream=sys.stdout)
            # Force UTF-8 encoding for Windows compatibility
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger