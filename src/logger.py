import servicemanager

class Logger():
    def __init__(self, service):
        self.service = service

    def Log(self, message):
        message = 'The {} service {}.'.format(self.service._svc_name_, message)
        servicemanager.LogInfoMsg(message)
        

class EmptyLogger():
    def Log(self, message):
        return