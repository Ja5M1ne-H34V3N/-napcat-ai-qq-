from ncatbot.core import BotClient
from ncatbot.core import GroupMessage,PrivateMessage
from ncatbot.types import PlainText, parse_segment
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ncatbot.core.event.message_segment import Text, Image, File,At,MessageArray
import loadCfg
import os

def groupMessageReact(msg,qq:int,cfg:loadCfg.cfg,user_id): 
    if isinstance(msg[0],At) and msg[0] == At(cfg.config["my_qq"]) and isinstance(msg[1],Text) and msg[1].text.strip() in cfg.command.values:
        a = msg.text.strip()
        if a == '/help':
            res = ''
            for i in cfg.command.values()
            res += str(i) + '\n'
        res = res[:-2]
        resMsg = (MessageArray + At(user_id) + Text(res))
        return resMsg

        elif a == '/server':
            return 0
            '待重写'
    else:
        return None

