#!/usr/bin/env python3
"""
临时 RCON 连通性/认证测试脚本（不依赖机器人事件）

目标服务器（你给的）：
- 游戏端口：i.qicaiyun.cc:26883（仅用于玩家进服）
- RCON：port=25575, password=2421

用法：
在项目根目录执行其一：
  python bot/arch/rcon_test_tmp.py
或（如果你用 venv）：
  ./.venv/bin/python bot/arch/rcon_test_tmp.py

说明：
- 此脚本只做“连接 + login + 简单命令”验证，方便定位是密码/端口/防火墙/RCON未开启等问题。
- 默认测试命令用 "list"（不会广播消息），更安全。
"""

from __future__ import annotations

from mctools import RCONClient
from mctools.errors import RCONAuthenticationError

HOST = "i.qicaiyun.cc"
RCON_PORT = 25575
PASSWORD = "2421"

# 你可以改成别的命令；不想在服务器广播消息就别用 say。
TEST_COMMAND = "list"


def main():
    print(f"[info] target host={HOST} rcon_port={RCON_PORT}")
    rcon = RCONClient(HOST, port=RCON_PORT)

    try:
        ok = rcon.login(PASSWORD)
        print(f"[info] login() returned: {ok}")
        print(f"[info] is_authenticated(): {rcon.is_authenticated()}")

        if not ok:
            print(
                "[error] login 失败：通常是 rcon.password 不匹配，或连错 rcon.port/服务器没开 RCON/被防火墙拦截。"
            )
            return

        print(f"[info] sending command: {TEST_COMMAND!r}")
        resp = rcon.command(TEST_COMMAND)
        print("[info] command response:")
        print(resp)

    except RCONAuthenticationError as e:
        print(f"[auth_error] {e}")
        print(
            "[hint] 这类错误一般意味着：login 没成功（密码/端口/RCON未开），或服务端返回的 reqid 不匹配。"
        )
    except Exception as e:
        print(f"[exception] {type(e).__name__}: {e}")
    finally:
        try:
            rcon.stop()
        except Exception:
            pass
        print("[info] done")


if __name__ == "__main__":
    main()
