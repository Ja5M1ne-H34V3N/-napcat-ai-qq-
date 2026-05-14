from ncatbot.core import BotClient
from ncatbot.core import GroupMessage,PrivateMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ncatbot.core.event.message_segment import Text, Image, File,At,MessageArray
import loadCfg
import os

def groupMessageReact(msg,qq:int,cfg:loadCfg.cfg,user_id): 
    print("已经进入信息处理函数")
    if isinstance(msg[0],At) and str(msg[0].qq) == str(cfg.config["my_qq"]) and isinstance(msg[1],Text) and msg[1].text.strip() in cfg.command:
        a = msg[1].text.strip()
        if a == '/help':
            print("识别指令help")
            res = '\n'
            for i in cfg.command:
                res += str(i) + '\n'
            res = res[:-2]
            resMsg = (MessageArray() + At(user_id) + Text(res))
            print(f"已经生成返回信息{resMsg}")
            return resMsg

        elif a == '/server':
            print("识别指令server")
            res = '\n'
            for i in loadCfg.loadServers():
                res += "==============\n"
                for k,v in i.items():
                    res += f"{k}:{v}\n"
            res += "=============="
            resMsg = (MessageArray() + At(user_id) + Text(res))
            return resMsg
    else:
        if not isinstance(msg[0],At):
            print("没有at")
        if not str(msg[0].qq) == str(cfg.config["my_qq"]):
            print("没有at我")
        if not (isinstance(msg[1],Text) and msg[1].text.strip() in cfg.command):
            print("不是指令")
        return None
