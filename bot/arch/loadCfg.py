import json

class cfg:
    def __init__(self):
        self.CONFIG_PATH = 'bot/config/config.json'
        self.COMMAND_PATH = "bot/config/commands.json"
        # 先初始化属性，避免 AttributeError
        self.config = None
        self.command = None
        self.load_config(self.CONFIG_PATH)
        self.load_command(self.COMMAND_PATH)

    def load_config(self,CONFIG_PATH):
        with open(CONFIG_PATH,'r') as f:
            self.config = json.load(f)
    
    def load_command(self,COMMAND_PATH):
        with open(COMMAND_PATH,'r') as f:
            self.command = json.load(f)

def loadServers():
    path = "bot/data/serverinfo.json"
    with open(path,'r') as f:
        return json.load(f)