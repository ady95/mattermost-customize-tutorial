# 7-2절: REST API 클라이언트 뼈대 — 이후 장에서 계속 재사용
# 필요 환경 변수: MM_URL, MM_BOT_TOKEN
import os

import requests


class Mattermost:
    def __init__(self, base_url=None, token=None):
        self.base = (base_url or os.environ["MM_URL"]).rstrip("/")
        self.token = token or os.environ["MM_BOT_TOKEN"]
        self.s = requests.Session()
        self.s.headers["Authorization"] = f"Bearer {self.token}"

    def get(self, path, **params):
        r = self.s.get(f"{self.base}/api/v4{path}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def post(self, path, payload):
        r = self.s.post(f"{self.base}/api/v4{path}", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()


if __name__ == "__main__":
    mm = Mattermost()
    me = mm.get("/users/me")
    print(me["username"], me["id"])
