# 6-1절: 사용자 정의 슬래시 커맨드 — /contacts 처리 서버
# 주의: 커맨드 트리거는 영문 소문자·숫자만 가능합니다 (한글 트리거는 등록 거부 — v11.9 실측)
# 필요 환경 변수: MM_SLASH_TOKEN (커맨드 등록 후 발급되는 토큰)
import os

from flask import Flask, jsonify, request

app = Flask(__name__)
MM_TOKEN = os.environ.get("MM_SLASH_TOKEN", "")

# 실무라면 DB나 인사 시스템 API에서 조회할 부분입니다
CONTACTS = {
    "kim":  {"이름": "김개발", "부서": "개발팀", "내선": "1001"},
    "lee":  {"이름": "이기획", "부서": "기획팀", "내선": "2002"},
    "park": {"이름": "박운영", "부서": "운영팀", "내선": "3003"},
}


@app.route("/contacts", methods=["POST"])
def contacts():
    data = request.form
    if MM_TOKEN and data.get("token") != MM_TOKEN:
        return "invalid token", 403

    keyword = data.get("text", "").strip().lower()
    if not keyword:
        return jsonify({
            "response_type": "ephemeral",
            "text": "사용법: `/contacts <검색어>` — 예: `/contacts kim`",
        })

    hits = {k: v for k, v in CONTACTS.items() if keyword in k}
    if not hits:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"`{keyword}` 검색 결과가 없습니다.",
        })

    rows = ["| 이름 | 부서 | 내선 |", "|---|---|---|"]
    for c in hits.values():
        rows.append(f"| {c['이름']} | {c['부서']} | {c['내선']} |")
    return jsonify({
        "response_type": "ephemeral",
        "text": "\n".join(rows),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
