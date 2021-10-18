import os
import re
from dotenv import load_dotenv

load_dotenv()
LOG_OUT_FILE = os.getenv('LOG_OUT_FILE')
LOG_ERR_FILE = os.getenv('LOG_ERR_FILE')


def ensure_path(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

# regex


def extract_url(url):
    # match the board and thread_id
    res = re.search(r'.org/(.*)/thread/(.*)$', url)
    if not res:
        return None
    return res.group(1), res.group(2)

# logging


def log_out(status, message):
    ensure_path(LOG_OUT_FILE)
    with open(LOG_OUT_FILE, 'a') as f:
        f.write(f'[{status}]: {message}\n')


def log_err(message):
    ensure_path(LOG_ERR_FILE)
    with open(LOG_ERR_FILE, 'a') as f:
        f.write(f'Unhandled message: {message}\n')
