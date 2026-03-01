from ncatbot.core import BotClient
from ncatbot.core import GroupMessage,PrivateMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ncatbot.core.event.message_segment import Text, Image, File
import os
# 启动ai
llm = ChatOpenAI(
    base_url="https://newapi.ashesb.com/v1", #自行设置模型api
    api_key="sk-WYcyBGmplbbETXKvEtTjy3rIgrpNvpAcasoTOCLH7CktIZRq",
    model="gemini-2.5-flash"
)
prompt = ChatPromptTemplate.from_messages([
("system", "你是一个助手，说话即可"),
("user", "{input}")])
chain = prompt | llm
masterQQ = str(input("请输入主人的qq号，在未来，只有收到这个qq号发来的消息才会有回复"))

#初始化一些需要的保存文件的路径
fileadd = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'filesaved')
iamgeadd = os.path.join(fileadd,'image')
os.makedirs(iamgeadd,exist_ok=True)

#目前会有相应的指令集
commands = ['/aimode',
            '/quitaimode',
            '/help']

aiMode = False
#初始化机器人客户端
bot = BotClient()
@bot.private_event()
async def on_private_message(msg: PrivateMessage):

    global aiMode
    global commands
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
    #对指令进行特殊处理
    if user_id == masterQQ and msg_text in commands:
        if msg_text == "/help":
            res = ''
            for i in commands:
                res += i + "\n"
            await bot.api.post_private_msg(user_id, text=res[:-3])
            return

        if msg_text == '/quitaimode':
            aiMode = False
            await bot.api.post_private_msg(user_id, text="#退出ai对话模式")
            return
        
        if msg_text == '/aimode':
            aiMode = True
            await bot.api.post_private_msg(user_id, text="#进入ai对话模式，ai相应需要时间，有的时候需要耐心等待~")
            return

    #判断是否为ai对话状态
    if aiMode == True:
        #设计ai对话：
        if user_id == masterQQ and msg_text != '/quitaimode':
            
            response = await chain.ainvoke({"input":f"{msg_text}"})
            await bot.api.post_private_msg(user_id, text=f"{response.content}")

    else:    
        #判断是不是我本人的qq号,和具体发送内容是否为指令
        if user_id == masterQQ:
            if msg_text != '' and msg_text != '/aimode':
            #回复固定的私聊消息
                await bot.api.post_private_msg(user_id, text="#ccb")

            #接收我本人发来的文件，并将其保存到同目录下的filesaved
            if fileArray:
                for i in fileArray:
                    if isinstance(i,(Image)):
                        await i.download(iamgeadd)
                    else:
                        await i.download(fileadd)
                await bot.api.post_private_msg(user_id, text="文件已经收到，保存成功")


if __name__ == '__main__':
    bot.run()
