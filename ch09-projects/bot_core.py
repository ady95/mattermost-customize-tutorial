# 8-2절: 챗봇 공통 뼈대 — 수신(WebSocket)·판단·응답(REST)을 담당
# 처리기(handler) 함수만 갈아 끼우면 새 챗봇이 됩니다 (8장~9장 공용)
# 필요 환경 변수: MM_URL, MM_BOT_TOKEN, (선택) MM_WS_URL
import asyncio
import json
import os

import websockets

from mm_client import Mattermost

MM_WS_URL = os.environ.get("MM_WS_URL", "ws://localhost:8065/api/v4/websocket")
MM_BOT_TOKEN = os.environ["MM_BOT_TOKEN"]


class Bot:
    def __init__(self, handler):
        self.mm = Mattermost()
        self.me = self.mm.get("/users/me")          # 봇 자신의 정보
        self.mention = f"@{self.me['username']}"     # 예: @workbot
        self.handler = handler                       # 3단계: 처리 함수

    # ── 2단계: 판단 ──────────────────────────────
    def should_reply(self, post, channel_type):
        if post["user_id"] == self.me["id"]:
            return False                             # 규칙 1: 자기 메시지 무시
        if post.get("props", {}).get("from_bot") == "true":
            return False                             # 다른 봇·웹훅도 무시
        if channel_type == "D":
            return True                              # 규칙 2: DM은 항상 응답
        return self.mention in post["message"]       # 채널에서는 멘션 시만

    # ── 4단계: 응답 (스레드로) ───────────────────
    def reply(self, post, text):
        self.mm.post("/posts", {
            "channel_id": post["channel_id"],
            "message": text,
            "root_id": post["root_id"] or post["id"],  # 규칙 3: 스레드 답글
        })

    # ── 1단계: 수신 루프 ────────────────────────
    async def listen(self):
        async with websockets.connect(MM_WS_URL) as ws:
            await ws.send(json.dumps({
                "seq": 1,
                "action": "authentication_challenge",
                "data": {"token": MM_BOT_TOKEN},
            }))
            print(f"연결됨 — {self.mention} 대기 중")
            async for raw in ws:
                msg = json.loads(raw)
                if msg.get("event") != "posted":
                    continue
                post = json.loads(msg["data"]["post"])
                ctype = msg["data"].get("channel_type", "")
                if not self.should_reply(post, ctype):
                    continue
                text = self.handler(self, post)      # 3단계 호출
                if text:
                    self.reply(post, text)

    async def run(self):
        while True:                                   # 재접속 루프 (7-3절)
            try:
                await self.listen()
            except (websockets.ConnectionClosed, ConnectionError, OSError) as e:
                print(f"연결 끊김: {e} — 5초 후 재접속")
                await asyncio.sleep(5)
