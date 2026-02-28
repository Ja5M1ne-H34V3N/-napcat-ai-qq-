from ncatbot.core import BotClient
from ncatbot.core import GroupMessage,PrivateMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# 启动ai
llm = ChatOpenAI(
    base_url="", #自行设置模型api，
    api_key="",
    model=""
)
prompt = ChatPromptTemplate.from_messages([
("system", "你是一个助手，说话即可"),
("user", "{input}")])
chain = prompt | llm
masterQQ = str(input("请输入主人的qq号，在未来，只有收到这个qq号发来的消息才会有回复"))
#编写ai对话模式使用的函数，初步计划输入想说的内容，返回回复


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
    msg_text = msg.raw_message
    user_id = msg.user_id
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
        if user_id == masterQQ and msg_text != '/aimode':
            #回复固定的私聊消息
            await bot.api.post_private_msg(user_id, text="#ccb")


if __name__ == '__main__':

    bot.run()
