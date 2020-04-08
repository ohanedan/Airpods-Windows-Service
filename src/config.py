import json
import os

from pathlib import Path

class Config():
    def __init__(self):
        home = str(Path.home())
        self.configPath = os.path.join(home, ".airpods-config.json")
        if not os.path.exists(self.configPath):
            self.createDefault()
        else:
            with open(self.configPath, 'r') as f:
                self.Data = json.load(f)
    
    def createDefault(self):
        data = {}
        data["udp_port"] = 6161
        with open(self.configPath, 'w') as outfile:
            json.dump(data, outfile, indent=2)
        self.Data = data


if __name__ == '__main__':
    conf = Config().Data
    print(str(conf))