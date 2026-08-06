# 9-1절: 서버 모니터링 알림봇 — 임계치 초과 시 웹훅 경고 (중복 억제 포함)
# 필요 환경 변수: MM_WEBHOOK_URL / 필요 패키지: psutil
# 주기 실행 예: */5 * * * * cd /opt/monitor && python3 monitor.py >> monitor.log 2>&1
import json
import os
import socket

import psutil
import requests

WEBHOOK_URL = os.environ["MM_WEBHOOK_URL"]
HOST = socket.gethostname()

# 항목별 임계치 (퍼센트)
THRESHOLDS = {"cpu": 80, "memory": 85, "disk": 90}

STATE_FILE = "/tmp/monitor_state.json"


def collect():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
    }


def judge(stats):
    """임계치를 넘은 항목 목록을 반환"""
    return [
        (name, value, THRESHOLDS[name])
        for name, value in stats.items()
        if value >= THRESHOLDS[name]
    ]


def send_alert(violations):
    fields = [
        {"title": name.upper(), "value": f"{value:.0f}% (임계 {limit}%)", "short": True}
        for name, value, limit in violations
    ]
    summary = ", ".join(f"{n} {v:.0f}%" for n, v, _ in violations)
    payload = {
        "username": "모니터링봇",
        "attachments": [{
            "fallback": f"{HOST} 자원 경고: {summary}",
            "color": "#E02020",
            "title": f"자원 사용률 경고 — {HOST}",
            "text": "임계치를 초과한 항목이 있습니다. 확인이 필요합니다.",
            "fields": fields,
            "footer": "monitor.py",
        }],
    }
    requests.post(WEBHOOK_URL, json=payload, timeout=10).raise_for_status()


def send_recovery():
    requests.post(WEBHOOK_URL, json={
        "username": "모니터링봇",
        "attachments": [{
            "fallback": f"{HOST} 자원 정상 복귀",
            "color": "#2EB67D",
            "title": f"정상 복귀 — {HOST}",
            "text": "모든 자원 사용률이 임계치 아래로 돌아왔습니다.",
        }],
    }, timeout=10).raise_for_status()


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"alerting": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def main():
    stats = collect()
    violations = judge(stats)
    now_alerting = sorted(n for n, _, _ in violations)
    print(f"{HOST}: {stats} → 위반 {len(violations)}건")

    # 상태가 바뀔 때만 알림 — 알림 피로 방지 (책 9-1절 4단계)
    state = load_state()
    if now_alerting != state["alerting"]:
        if now_alerting:
            send_alert(violations)          # 새 경고 (또는 항목 변화)
        else:
            send_recovery()                 # 모두 정상으로 복귀
        save_state({"alerting": now_alerting})


if __name__ == "__main__":
    main()
