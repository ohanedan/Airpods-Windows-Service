from logging import Formatter, Handler
import logging

import servicemanager

class _LogHandler(Handler):
    def emit(self, record):
        servicemanager.LogInfoMsg(record.getMessage())

class Logger():
    def __init__(self, service):
        self.service = service
        self._configure_logging()

    def Log(self, message):
        message = 'The {} service {}.'.format(self.service._svc_name_, message)
        logging.info(message)

    def _configure_logging(self):
        formatter = Formatter('%(message)s')
        
        handler = _LogHandler()
        handler.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

class EmptyLogger():
    def Log(self, message):
        return