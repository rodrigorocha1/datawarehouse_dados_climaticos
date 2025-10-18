import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    URL_API = os.environ['URL_API']
    KEY_API = os.environ['KEY_API']
