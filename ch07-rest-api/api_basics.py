# 7-2절 실습 2~4 종합: 채널 ID 찾기, 메시지 보내기/읽기, 첨부 카드
# 필요 환경 변수: MM_URL, MM_BOT_TOKEN, MM_TEAM(팀 URL 이름), MM_CHANNEL(채널 URL 이름)
import os

from mm_client import Mattermost

TEAM = os.environ.get("MM_TEAM", "ourcompany")
CHANNEL = os.environ.get("MM_CHANNEL", "alerts")

mm = Mattermost()

# 실습 2: 채널 ID 찾기 — 이름(URL 이름)으로 팀 → 채널 순서로 조회
team = mm.get(f"/teams/name/{TEAM}")
channel = mm.get(f"/teams/{team['id']}/channels/name/{CHANNEL}")
print("채널 ID:", channel["id"])

# 실습 3: 메시지 보내기
post = mm.post("/posts", {
    "channel_id": channel["id"],
    "message": "REST API로 보낸 첫 메시지입니다.",
})
print("게시물 ID:", post["id"])

# 스레드 답글 달기 — root_id에 원본 게시물 ID를 지정
mm.post("/posts", {
    "channel_id": channel["id"],
    "message": "이 메시지는 스레드 답글입니다.",
    "root_id": post["id"],
})

# 첨부 카드 보내기 — API에서는 props 안에 attachments를 넣습니다 (웹훅과 다른 점!)
mm.post("/posts", {
    "channel_id": channel["id"],
    "message": "",
    "props": {
        "attachments": [
            {"fallback": "요약", "color": "#2EB67D",
             "title": "API 첨부 카드", "text": "5-2절의 카드를 API로 보냈습니다."}
        ]
    },
})

# 실습 4: 메시지 읽기 — posts는 {id: 게시물} 딕셔너리, order가 시간 역순 ID 목록
data = mm.get(f"/channels/{channel['id']}/posts", per_page=5)
for post_id in data["order"]:
    p = data["posts"][post_id]
    print(p["user_id"][:6], "|", p["message"][:40])
