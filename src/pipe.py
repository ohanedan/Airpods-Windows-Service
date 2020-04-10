import win32pipe
import win32file

from logger import EmptyLogger

class Pipe():
    def __init__(self, service = None):
        if service != None:
            self.logger = service.logger
        else:
            self.logger = EmptyLogger()

        self.pipe = win32pipe.CreateNamedPipe(r'\\.\pipe\airpods-windows-service',
        win32pipe.PIPE_ACCESS_OUTBOUND,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE |
             win32pipe.PIPE_NOWAIT, 1, 65536, 65536, 0, None)

        self.logger.Log("pipe created")
        self.hasClient = False

    def SendData(self, data):
        try:
            if not self.hasClient:
                win32pipe.ConnectNamedPipe(self.pipe, None)
                self.hasClient = True
            else:
                win32file.WriteFile(self.pipe, data)
                win32file.FlushFileBuffers(self.pipe)
        except Exception:
            if self.hasClient:
                win32pipe.DisconnectNamedPipe(self.pipe)
                self.hasClient = False
            return