import os
from pathlib import Path

from dotenv import load_dotenv

VERSION = '26.1127.1706'

BASE_DIR = Path(__file__).resolve().parent.parent

# 启动时所在目录，作为工具的默认工作目录
WORKSPACE = Path.cwd().resolve()

dotenv_path = BASE_DIR / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

BASH_PATH = os.environ.get('BASH_PATH')

LLM_MODEL = os.environ.get('MODEL', 'deepseek-flash')
LLM_URL = os.environ.get('API_BASE_URL')
LLM_KEY = os.environ.get('API_KEY')
