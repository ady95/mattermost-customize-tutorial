# 5-1절: Incoming Webhook으로 메시지 보내기
# 필요 환경 변수: MM_WEBHOOK_URL
import os

import requests

WEBHOOK_URL = os.environ["MM_WEBHOOK_URL"]  # URL은 환경 변수로 관리


def send(text, channel=None, username=None):
    payload = {"text": text}
    if channel:
        payload["channel"] = channel
    if username:
        payload["username"] = username
    r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    r.raise_for_status()


if __name__ == "__main__":
    send("Python에서 보낸 메시지입니다.")

    # 5-1절 실습 4: 채널·발신자 바꾸기 (필요 시 주석 해제)
    # send("공지 채널로 보냅니다", channel="town-square")
    # send("개인 알림입니다", channel="@alice")
    # send("배포가 완료되었습니다", username="배포봇")
