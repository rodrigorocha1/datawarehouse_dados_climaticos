import logging
from abc import ABC, abstractmethod


class Ilog(ABC, logging.Handler):

    @abstractmethod
    def emit(self, record: logging.LogRecord):
        pass
