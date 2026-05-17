from ncatbot.core import BotClient
from ncatbot.core import GroupMessage,PrivateMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ncatbot.core.event.message_segment import Text, Image, File,At,MessageArray
import loadCfg
from mcstatus import JavaServer
from mctools import RCONClient
import os
import time

def groupMessageReact(msg,qq:int,cfg:loadCfg.cfg,user_id): 
    print("已经进入信息处理函数")
    if isinstance(msg[0],At) and str(msg[0].qq) == str(cfg.config["my_qq"]) and isinstance(msg[1],Text) :
        a = msg[1].text.strip()
        print(a)
        if a == '/help':
            print("识别指令help")
            res = '\n'
            for i in cfg.command:
                res += str(i) + '\n'
            res = res[:-1]
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
            
                
            try:   
                a = i['服务器链接'].split(":")
                server = JavaServer(a[0],int(a[1]))
                res += f"ping_ms:{int(server.ping())}\n"
                res += f"在线人数：{server.status().players.online}/{server.status().players.max}\n"
                
            except Exception as e:
                print(e)
                res += "未连接到服务器"
            res += "=============="
            resMsg = (MessageArray() + At(user_id) + Text(res))
            return resMsg
        
        elif a.split(' ')[0] == "/tellserver":
            mess = ""
            for i in a.split()[1:]:
                mess += i

            HOST = loadCfg.loadServers()[0]['服务器链接'].split(":")[0]
            print(HOST)
            PORT = 25575
            pwd = cfg.config["rconpwd"]
            print(pwd)
            rcon = RCONClient(HOST, port=PORT)
            print(rcon.login(pwd))
            time.sleep(5)
            rcon.command(f"say {mess}")
            rcon.stop()
            print("发送指令成功")
    else:
        if not isinstance(msg[0],At):
            print("没有at")
        if not str(msg[0].qq) == str(cfg.config["my_qq"]):
            print("没有at我")
        if not (isinstance(msg[1],Text) and msg[1].text.strip() in cfg.command):
            print("不是指令")
        return None
