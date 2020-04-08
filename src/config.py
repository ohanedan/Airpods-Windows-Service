import json
import os
import servicemanager

class Config():
    def __init__(self):
        home = os.environ['SYSTEMDRIVE'] + "/"

        self.configPath = os.path.join(home, ".airpods-config.json")
        if not os.path.exists(self.configPath):
            self.createDefault()
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, 
                                    0xF001, ("created empty config: " + self.configPath,))
        else:
            with open(self.configPath, 'r') as f:
                self.Data = json.load(f)
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, 
                                    0xF001, ("read existing config: " + self.configPath,))
    
    def createDefault(self):
        data = {}
        data["udp_port"] = 6161
        with open(self.configPath, 'w') as outfile:
            json.dump(data, outfile, indent=2)
        self.Data = data


if __name__ == '__main__':
    conf = Config().Data
    print(str(conf))