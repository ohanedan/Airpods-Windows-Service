import servicemanager
import win32serviceutil
import win32event
import win32service
import sys

from airpods import Airpods
from logger import Logger
from pipe import Pipe

class SMWinservice(win32serviceutil.ServiceFramework):

    _svc_name_ = 'airpods-service'
    _svc_display_name_ = 'Airpods Service'
    _svc_description_ = 'Airpods Service developed by ohanedan'

    @classmethod
    def parse_command_line(cls):
        if len(sys.argv) == 1 and \
                sys.argv[0].endswith('.exe') and \
                not sys.argv[0].endswith(r'win32\PythonService.exe'):
            
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(cls)
            servicemanager.StartServiceCtrlDispatcher()
        
        else:
            if len(sys.argv) == 2 and sys.argv[1] == 'help':
                sys.argv = sys.argv[:1]
                
            win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        self.logger = Logger(self)
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.stopping = True
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.logger.Log("stopping")
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.stopping = False
        self.start()
        self.logger.Log("starting")
        self.main()

    def start(self):
        self.airpods = Airpods(self)
        self.pipe = Pipe(self)
        pass

    def stop(self):
        pass

    def main(self):
        while not self.stopping:
            try:
                data = self.airpods.GetDataJsonString()
                data = data + "\n"
                self.pipe.SendData(data.encode())
            except Exception as ex:
                self.logger.Log("error on send: " + str(ex))
                break

if __name__ == '__main__':
    SMWinservice.parse_command_line()