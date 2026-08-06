# 8-3절: 명령형 챗봇 — "명령어 → 함수" 라우팅 구조
import asyncio
import random
from datetime import datetime

from bot_core import Bot

# ── 명령 함수들: (bot, post, args) → 답 문자열 ──────────


def cmd_help(bot, post, args):
    lines = ["제가 할 수 있는 일입니다.", ""]
    for name, (_, desc) in COMMANDS.items():
        lines.append(f"- `{name}` — {desc}")
    return "\n".join(lines)


def cmd_time(bot, post, args):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"현재 시각은 **{now}** 입니다."


def cmd_lunch(bot, post, args):
    menu = random.choice(["김치찌개", "제육볶음", "돈까스", "쌀국수", "샐러드"])
    return f"오늘 점심은 **{menu}** 어떠세요?"


OWNERS = {"결제": "김개발", "배포": "박운영", "디자인": "이기획"}


def cmd_owner(bot, post, args):
    if not args:
        return f"조회할 업무를 알려 주세요. 예: `담당자 배포`\n등록된 업무: {', '.join(OWNERS)}"
    key = args[0]
    if key in OWNERS:
        return f"**{key}** 담당자는 **{OWNERS[key]}** 님입니다."
    return f"`{key}` 업무를 찾지 못했습니다. 등록된 업무: {', '.join(OWNERS)}"


# ── 라우팅 테이블 ───────────────────────────────────────

COMMANDS = {
    "도움말":  (cmd_help,  "명령 목록을 보여줍니다"),
    "시간":    (cmd_time,  "현재 시각을 알려줍니다"),
    "점심":    (cmd_lunch, "점심 메뉴를 추천합니다"),
    "담당자":  (cmd_owner, "업무별 담당자를 알려줍니다 (예: 담당자 배포)"),
}


def command_handler(bot, post):
    text = post["message"].replace(bot.mention, "").strip()
    if not text:
        return cmd_help(bot, post, [])

    words = text.split()
    name, args = words[0], words[1:]

    if name in COMMANDS:
        func, _ = COMMANDS[name]
        try:
            return func(bot, post, args)
        except Exception as e:
            print(f"[오류] {name}: {e}")
            return "명령을 처리하는 중 문제가 발생했습니다. 잠시 후 다시 시도해 주세요."

    return f"`{name}` 명령을 모르겠어요. `도움말`을 입력해 보세요."


if __name__ == "__main__":
    asyncio.run(Bot(command_handler).run())
