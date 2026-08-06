# 9-3절: 사내 FAQ 챗봇 — 검색 + LLM 조합 (RAG 기본형)
# 필요 환경 변수: MM_URL, MM_BOT_TOKEN, OPENAI_API_KEY, (선택) OPENAI_MODEL
import asyncio
import json
import os

from openai import OpenAI

from bot_core import Bot

client = OpenAI()
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

with open("faq.json", encoding="utf-8") as f:
    FAQ = json.load(f)


def search_faq(query, top_n=3):
    """질문과 겹치는 단어 수로 FAQ 점수를 매겨 상위 n건 반환.
    규모가 커지면 이 함수만 임베딩 검색으로 교체하면 됩니다 (책 9-3절)."""
    words = set(query.split())
    scored = []
    for item in FAQ:
        haystack = item["q"] + " " + " ".join(item["tags"])
        score = sum(1 for w in words if w in haystack)
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:top_n]]


SYSTEM_PROMPT = """당신은 사내 FAQ 도우미 '규정봇'입니다. 규칙:
1. 아래 [사내 FAQ]에 있는 내용만 근거로 답합니다.
2. FAQ에 없는 내용은 "등록된 규정에서 찾지 못했습니다. 총무팀(#general-support 채널)에 문의해 주세요."라고 답합니다.
3. 추측하거나 일반 상식으로 메꾸지 않습니다.
4. 답 끝에 근거가 된 FAQ 질문을 "근거: ..." 형태로 표시합니다."""


def faq_handler(bot, post):
    query = post["message"].replace(bot.mention, "").strip()
    if not query:
        return "사내 규정에 대해 물어보세요. 예: 연차 이월 되나요?"

    hits = search_faq(query)
    if not hits:
        return "등록된 규정에서 찾지 못했습니다. 총무팀(#general-support 채널)에 문의해 주세요."

    context = "\n\n".join(f"Q: {h['q']}\nA: {h['a']}" for h in hits)
    res = client.chat.completions.create(
        model=MODEL,
        max_tokens=600,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"[사내 FAQ]\n{context}\n\n[질문]\n{query}"},
        ],
    )
    return res.choices[0].message.content


if __name__ == "__main__":
    asyncio.run(Bot(faq_handler).run())
