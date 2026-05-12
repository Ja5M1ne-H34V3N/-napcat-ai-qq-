from ncatbot.core import BotClient
from ncatbot.core import GroupMessage,PrivateMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ncatbot.core.event.message_segment import Text, Image, File,MessageArray
import groupMessageReact
import os
import loadCfg
import json


if __name__ == '__main__':
    config = loadCfg.cfg()
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

    @mybot.group_event()
    async def on_group_messange(msg:GroupMessage):
        messageArray = msg.message
        msg_text = ''
        group_id = msg.group_id
        user_id = msg.user_id
        if group_id == config.config['mcGroup_qq']:
            # 检测到是来自正确的群的消息，移交给正确的处理函数
            recv = groupMessageReact.groupMessageReact(messageArray,group_id,config,user_id)
            if recv:
                await bot.api.post_group_msg(group_id=group_id, message=msg)
    mybot.run()
