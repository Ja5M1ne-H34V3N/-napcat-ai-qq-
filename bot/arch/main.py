from ncatbot.core import BotClient
from ncatbot.core import GroupMessage,PrivateMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ncatbot.core.event.message_segment import Text, Image, File
import os
import json
CONFIG_PATH = '../config/config.json'
COMMAND_PATH = "../config/command.json"
class cfg:
    def __init__(self):
        pass
if __name__ == '__main__':
    mybot = BotClient()
    @mybot.private_event()
    async def on_private_message(msg: PrivateMessage):
        fileArray = []
    messageArray = msg.message
    msg_text = ''
    user_id = msg.user_id

    #检查是否有文件
    for i in messageArray:
        print(type(i))
        if isinstance(i,(Image)):
            fileArray.append(i)
        if isinstance(i, Text):
            msg_text += i.text + " "

    print(messageArray)
    mybot.run()
