# 5-2절: Message Attachments — 서식 있는 알림 카드
# 필요 환경 변수: MM_WEBHOOK_URL
import os

import requests

WEBHOOK_URL = os.environ["MM_WEBHOOK_URL"]

payload = {
    "channel": "alerts",
    "username": "모니터링봇",
    "attachments": [
        {
            "fallback": "web-01 CPU 경고 92%",
            "color": "#E02020",
            "title": "CPU 사용률 경고",
            "title_link": "https://grafana.example.com/d/web-01",
            "text": "web-01 서버의 CPU 사용률이 임계치를 넘었습니다.",
            "fields": [
                {"title": "서버", "value": "web-01", "short": True},
                {"title": "사용률", "value": "92%", "short": True},
                {"title": "임계치", "value": "80%", "short": True},
                {"title": "지속 시간", "value": "5분", "short": True},
            ],
            "footer": "monitoring.example.com",
        }
    ],
}

if __name__ == "__main__":
    requests.post(WEBHOOK_URL, json=payload, timeout=10).raise_for_status()
    print("전송 완료")
