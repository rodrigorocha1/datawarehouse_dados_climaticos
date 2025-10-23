import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    URL_OPEN_API = os.environ['URL_OPEN_API']
    KEY_OPEN_API = os.environ['KEY_OPEN_API']
    UNITS_OPEN_API = os.environ['UNITS_OPEN_API']
    LANG_OPEN_API = os.environ['LANG_OPEN_API']
