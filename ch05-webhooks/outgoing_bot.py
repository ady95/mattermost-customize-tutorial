# 5-3절: Outgoing Webhook — 트리거 단어(#점심)에 반응하는 수신 서버
# 필요 환경 변수: MM_OUTGOING_TOKEN (웹훅 등록 후 발급되는 토큰)
import os
import random

from flask import Flask, jsonify, request

app = Flask(__name__)

MM_TOKEN = os.environ.get("MM_OUTGOING_TOKEN", "")

MENUS = ["김치찌개", "제육볶음", "돈까스", "쌀국수", "샐러드"]


@app.route("/lunch", methods=["POST"])
def lunch():
    data = request.form  # 기본 content-type은 form-urlencoded

    # 토큰 검증 — Mattermost가 보낸 요청이 맞는지 확인
    if MM_TOKEN and data.get("token") != MM_TOKEN:
        return "invalid token", 403

    user = data.get("user_name", "someone")
    text = data.get("text", "")
    print(f"[수신] {user}: {text}")

    menu = random.choice(MENUS)
    return jsonify({
        "text": f"@{user} 오늘 점심은 **{menu}** 어떠세요?",
        "username": "점심봇",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
