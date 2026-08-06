# 8-4절: LLM 챗봇 — 스레드를 대화 문맥으로 쓰는 AI 처리기
# 필요 환경 변수: OPENAI_API_KEY, (선택) OPENAI_MODEL
import asyncio
import os

from openai import OpenAI

from bot_core import Bot

client = OpenAI()  # OPENAI_API_KEY 환경 변수를 자동으로 읽습니다

MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """당신은 우리 회사의 업무 도우미 봇 '업무봇'입니다.
- 한국어로, 정중하지만 간결하게 답합니다.
- 회사 업무(일정, 문서 작성, 코드, 일반 지식)를 돕습니다.
- 모르는 것은 아는 척하지 않고 모른다고 말합니다.
- 인사·급여 등 민감한 개인 정보 질문에는 담당 부서 문의를 안내합니다."""

MAX_TURNS = 20  # 문맥으로 보낼 최근 대화 수 (토큰 비용 통제)


def build_messages(bot, post):
    """스레드의 대화 기록을 LLM 메시지 형식으로 변환"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    root_id = post["root_id"] or post["id"]
    thread = bot.mm.get(f"/posts/{root_id}/thread")

    # 스레드 게시물을 시간순으로 정렬해 role을 부여
    posts = sorted(thread["posts"].values(), key=lambda p: p["create_at"])
    for p in posts[-MAX_TURNS:]:
        text = p["message"].replace(bot.mention, "").strip()
        if not text:
            continue
        role = "assistant" if p["user_id"] == bot.me["id"] else "user"
        messages.append({"role": role, "content": text})
    return messages


def llm_handler(bot, post):
    try:
        messages = build_messages(bot, post)
        res = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=1000,
        )
        return res.choices[0].message.content
    except Exception as e:
        print(f"[LLM 오류] {e}")
        return "지금은 답변을 만들 수 없습니다. 잠시 후 다시 시도해 주세요."


if __name__ == "__main__":
    asyncio.run(Bot(llm_handler).run())
