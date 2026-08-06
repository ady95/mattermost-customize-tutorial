# 8-2절: 에코봇 — 받은 말을 그대로 되돌려주는 처리기
import asyncio

from bot_core import Bot


def echo_handler(bot, post):
    # 멘션 문자열은 지우고 나머지를 그대로 반환
    text = post["message"].replace(bot.mention, "").strip()
    if not text:
        return "네, 부르셨나요?"
    return f"따라하기: {text}"


if __name__ == "__main__":
    asyncio.run(Bot(echo_handler).run())
