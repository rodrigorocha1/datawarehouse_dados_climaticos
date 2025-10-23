import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    URL_OPEN_API = os.environ['URL_OPEN_API']
    KEY_OPEN_API = os.environ['KEY_OPEN_API']
    UNITS_OPEN_API = os.environ['UNITS_OPEN_API']
    LANG_OPEN_API = os.environ['LANG_OPEN_API']
    ID_BANCO_LOG = os.environ['ID_BANCO_LOG']
    ID_BANCO_STG = os.environ['ID_BANCO_STG']
    ID_BANCO_DW = os.environ['ID_BANCO_DW']
