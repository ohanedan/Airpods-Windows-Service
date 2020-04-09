import json
import os

class Config():
    def __init__(self, service):
        home = os.environ['SYSTEMDRIVE'] + "/"

        self.configPath = os.path.join(home, ".airpods-config.json")
        if not os.path.exists(self.configPath):
            self.createDefault()
            service.logger.Log("created empty config: " + self.configPath)
        else:
            with open(self.configPath, 'r') as f:
                self.Data = json.load(f)
            service.logger.Log("read existing config: " + self.configPath)
    
    def createDefault(self):
        data = {}
        data["udp_port"] = 6161
        with open(self.configPath, 'w') as outfile:
            json.dump(data, outfile, indent=2)
        self.Data = data
