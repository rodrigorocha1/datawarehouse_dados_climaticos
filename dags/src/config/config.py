from dotenv import load_dotenv

load_dotenv()

from airflow.models import Variable


class Config:
    URL_OPEN_API = Variable.get('URL_OPEN_API')
    KEY_OPEN_API = Variable.get('KEY_OPEN_API')
    UNITS_OPEN_API = Variable.get('UNITS_OPEN_API')
    LANG_OPEN_API = Variable.get('LANG_OPEN_API')
    ID_BANCO_LOG = Variable.get('ID_BANCO_LOG')
    ID_BANCO_STG = Variable.get('ID_BANCO_STG')
    ID_BANCO_DW = Variable.get('ID_BANCO_DW')
