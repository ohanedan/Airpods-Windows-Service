import socket

import win32serviceutil

import servicemanager
import win32event
import win32service

import time

from airpods import Airpods
from config import Config

class SMWinservice(win32serviceutil.ServiceFramework):

    _svc_name_ = 'airpods-service'
    _svc_display_name_ = 'Airpods Service'
    _svc_description_ = 'Airpods Service developed by ohanedan'

    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.stopping = True
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPING,
                              (self._svc_name_, ''))
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.stopping = False
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        self.airpods = Airpods()
        self.conf = Config().Data
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pass

    def stop(self):
        pass

    def main(self):
        while not self.stopping:
            data = str(self.airpods.GetDataJsonString())
            try:
                self.sock.sendto(data.encode(), ("127.0.0.1", self.conf["udp_port"]))
            except Exception as ex:
                servicemanager.LogMsg(servicemanager.EVENTLOG_ERROR_TYPE, 
                                    0xF001, (str(ex),))
                break

if __name__ == '__main__':
    SMWinservice.parse_command_line()