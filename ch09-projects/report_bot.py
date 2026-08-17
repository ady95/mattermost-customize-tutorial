# 9-2절: 일일 리포트 봇 — 매일 아침 지표를 채널에 게시하고 고정(pin)
# 필요 환경 변수: MM_URL, MM_BOT_TOKEN, (선택) REPORT_REPO, GITHUB_TOKEN, MM_WEBHOOK_URL
# 주기 실행 예: 0 9 * * 1-5 cd /opt/reportbot && python3 report_bot.py >> report.log 2>&1
import os
from datetime import datetime, timedelta, timezone

import requests

from mm_client import Mattermost

REPO = os.environ.get("REPORT_REPO", "mattermost/mattermost")
GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")
TEAM = os.environ.get("MM_TEAM", "ourcompany")
CHANNEL = os.environ.get("MM_CHANNEL", "town-square")
KST = timezone(timedelta(hours=9))


def gh_paged(path, **params):
    """페이지를 끝까지 따라가며 모두 모읍니다 (GitHub는 한 페이지 최대 100건).
    대형 저장소에서는 호출량이 늘어나므로 GITHUB_TOKEN 설정을 권합니다."""
    headers = {"Authorization": f"Bearer {GH_TOKEN}"} if GH_TOKEN else {}
    items, page = [], 1
    while True:
        r = requests.get(f"https://api.github.com{path}", headers=headers,
                         params={**params, "per_page": 100, "page": page}, timeout=15)
        r.raise_for_status()
        batch = r.json()
        items.extend(batch)
        if len(batch) < 100:
            return items
        page += 1


def yesterday_range():
    """어제 00:00~오늘 00:00(한국 시간)을 GitHub API용 UTC 문자열로 변환"""
    today = datetime.now(KST).replace(hour=0, minute=0, second=0, microsecond=0)
    start = today - timedelta(days=1)

    def to_utc(d):
        return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return to_utc(start), to_utc(today)


def fetch_github_stats(repo):
    """어제 하루의 저장소 활동을 수집 — 실무에서는 사내 지표 조회로 교체"""
    since, until = yesterday_range()

    # 커밋 — since와 until을 함께 줘서 어제 하루로 정확히 한정
    commits = gh_paged(f"/repos/{repo}/commits", since=since, until=until)

    # 이슈 — Issues API는 PR도 함께 돌려주므로 pull_request 키가 있는 항목을 제외
    issues_raw = gh_paged(f"/repos/{repo}/issues", state="all", since=since)
    updated_issues = [i for i in issues_raw
                      if "pull_request" not in i and since <= i["updated_at"] < until]

    # 열린 PR — 기간 집계가 아니라 "현재 열려 있는 수"입니다
    open_prs = gh_paged(f"/repos/{repo}/pulls", state="open")

    return {
        "commits": len(commits),
        "updated_issues": len(updated_issues),
        "open_prs": len(open_prs),
    }


def build_report(stats):
    today = datetime.now().strftime("%Y-%m-%d (%a)")
    return f"""#### 일일 리포트 — {today}

| 지표 | 값 |
|:---|---:|
| 어제 커밋 | {stats['commits']}건 |
| 어제 갱신된 이슈 | {stats['updated_issues']}건 |
| 현재 열린 PR | {stats['open_prs']}건 |

대상 저장소: `{REPO}` · 자동 생성 리포트입니다.
"""


def unpin_old_reports(mm, channel_id, keep):
    pinned = mm.get(f"/channels/{channel_id}/pinned")
    for pid, p in pinned["posts"].items():
        if pid != keep and "일일 리포트" in p["message"]:
            mm.post(f"/posts/{pid}/unpin", {})


def main():
    mm = Mattermost()
    stats = fetch_github_stats(REPO)

    team = mm.get(f"/teams/name/{TEAM}")
    channel = mm.get(f"/teams/{team['id']}/channels/name/{CHANNEL}")

    post = mm.post("/posts", {
        "channel_id": channel["id"],
        "message": build_report(stats),
    })

    # 오늘 리포트를 채널에 고정 (어제 것은 내리기)
    unpin_old_reports(mm, channel["id"], keep=post["id"])
    mm.post(f"/posts/{post['id']}/pin", {})
    print(f"게시 완료: {post['id']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # 실패 알림 — 9-1절의 웹훅으로 경고 (MM_WEBHOOK_URL이 설정된 경우)
        webhook = os.environ.get("MM_WEBHOOK_URL")
        if webhook:
            requests.post(webhook, json={
                "username": "모니터링봇",
                "text": f"일일 리포트 생성 실패: `{e}`",
            }, timeout=10)
        raise
