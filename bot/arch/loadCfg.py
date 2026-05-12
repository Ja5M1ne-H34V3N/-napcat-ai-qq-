import json

class cfg:
    def __init__(self):
        self.CONFIG_PATH = 'bot/config/config.json'
        self.COMMAND_PATH = "bot/config/commands.json"
        self.config 
        self.command 
        self.load_config(self.CONFIG_PATH)
        self.load_command(self.COMMAND_PATH)

    def load_config(self,CONFIG_PATH):
        with open(CONFIG_PATH,'r') as f:
            self.config = json.load(f)
    
    def load_command(self,COMMAND_PATH):
        with open(COMMAND_PATH,'r') as f:
            self.command = json.load(f)