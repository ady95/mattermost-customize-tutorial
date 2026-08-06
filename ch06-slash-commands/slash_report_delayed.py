# 6-2절: 3초 제한을 넘는 작업의 지연 응답 — response_url 활용
import threading
import time

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


def heavy_work(response_url, keyword):
    time.sleep(10)  # 오래 걸리는 작업이라고 가정
    requests.post(response_url, json={
        "response_type": "ephemeral",
        "text": f"`{keyword}` 리포트가 준비되었습니다: https://report.example.com/123",
    }, timeout=10)


@app.route("/report", methods=["POST"])
def report():
    data = request.form
    keyword = data.get("text", "")
    response_url = data.get("response_url")

    # 백그라운드로 작업을 넘기고
    threading.Thread(target=heavy_work, args=(response_url, keyword)).start()

    # 3초 안에 접수 응답부터 돌려줍니다
    return jsonify({
        "response_type": "ephemeral",
        "text": "리포트를 생성 중입니다. 잠시 후 결과를 보내 드릴게요.",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
