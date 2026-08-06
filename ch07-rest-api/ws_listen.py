# 7-3절: WebSocket으로 실시간 이벤트 받기 (재접속 루프 포함)
# 필요 환경 변수: MM_BOT_TOKEN, (선택) MM_WS_URL
import asyncio
import json
import os

import websockets

MM_WS_URL = os.environ.get("MM_WS_URL", "ws://localhost:8065/api/v4/websocket")
MM_BOT_TOKEN = os.environ["MM_BOT_TOKEN"]


async def listen():
    async with websockets.connect(MM_WS_URL) as ws:
        # 연결 직후 토큰으로 인증
        await ws.send(json.dumps({
            "seq": 1,
            "action": "authentication_challenge",
            "data": {"token": MM_BOT_TOKEN},
        }))

        async for raw in ws:
            msg = json.loads(raw)              # 1차 파싱: 이벤트 봉투
            event = msg.get("event")
            if not event:
                continue
            print(f"[이벤트] {event}")

            if event == "posted":
                # data.post는 JSON "문자열" — 두 번 파싱해야 합니다 (책의 함정 포인트)
                post = json.loads(msg["data"]["post"])
                print("  채널:", post["channel_id"])
                print("  작성자:", post["user_id"])
                print("  내용:", post["message"])
                print("  스레드:", post["root_id"] or "(새 스레드)")


async def run_forever():
    while True:
        try:
            await listen()
        except (websockets.ConnectionClosed, ConnectionError, OSError) as e:
            print(f"연결 끊김: {e} — 5초 후 재접속")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(run_forever())
