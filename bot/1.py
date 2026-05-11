import requests
import json

# -------------------------- 配置项 --------------------------
ST_URL = "http://127.0.0.1:2690"
BASIC_AUTH = ("bean17", "bean17")  # 你的账号密码
CHARACTER_ID = "你的角色ID"  # 从ST地址栏复制（如 char_xxxx）
# -----------------------------------------------------------

def get_csrf_token():
    """获取 CSRF 令牌（自动处理 cookie）"""
    session = requests.Session()  # 保持会话，自动管理 cookie
    # 1. 自定义请求头（模拟浏览器）
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Origin": ST_URL,
        "Referer": f"{ST_URL}/"
    }
    # 2. 获取 CSRF 令牌
    response = session.get(
        url=f"{ST_URL}/api/csrf-token",
        auth=BASIC_AUTH,
        headers=headers
    )
    if response.status_code == 200:
        csrf_token = response.json().get("token")
        return session, csrf_token  # 返回会话（含cookie）和令牌
    else:
        raise Exception(f"获取CSRF令牌失败：{response.status_code}")

def send_message_to_st(user_message: str, user_id: str = "ncatbot_user"):
    """发送消息到 ST，获取 AI 回复"""
    # 1. 获取 CSRF 令牌和会话
    session, csrf_token = get_csrf_token()
    
    # 2. 自定义完整请求头（规避所有校验）
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Origin": ST_URL,
        "Referer": f"{ST_URL}/",
        "Content-Type": "application/json",
        "X-CSRF-Token": csrf_token  # 携带 CSRF 令牌
    }
    
    # 3. 构造消息参数
    payload = {
        "character_id": CHARACTER_ID,
        "user_id": user_id,
        "message": user_message,
        "use_memory": True,
        "use_scenario": True
    }
    
    # 4. 发送请求（自动携带 cookie 和认证）
    response = session.post(
        url=f"{ST_URL}/api/chat/send",
        auth=BASIC_AUTH,
        headers=headers,
        json=payload,
        timeout=30
    )
    
    # 5. 解析回复
    if response.status_code == 200:
        result = response.json()
        return result.get("reply", "暂无回复")
    else:
        raise Exception(f"调用ST失败：{response.status_code}，内容：{response.text}")

# -------------------------- 测试调用 --------------------------
if __name__ == "__main__":
    try:
        reply = send_message_to_st("你好，能听到我说话吗？")
        print(f"ST 回复：{reply}")
    except Exception as e:
        print(f"错误：{str(e)}")