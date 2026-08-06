# Mattermost를 활용한 업무용 메신저 만들기 — 예제 코드

위키독스 책 [「Mattermost를 활용한 업무용 메신저 만들기」](https://wikidocs.net)의 장별 예제 코드 저장소입니다.

- 기준 버전: Mattermost v11.9 / Python 3.10+ / Go 1.22+ (10장)
- 책 본문의 코드와 동일하며, 장·절 번호로 폴더가 구성되어 있습니다.

## 폴더 구성

| 폴더 | 책의 장 | 내용 |
|---|---|---|
| [ch05-webhooks/](ch05-webhooks/) | 5장 | Incoming/Outgoing Webhook, 첨부 메시지 |
| [ch06-slash-commands/](ch06-slash-commands/) | 6장 | 슬래시 커맨드 서버, 지연 응답 |
| [ch07-rest-api/](ch07-rest-api/) | 7장 | REST API 클라이언트, WebSocket 이벤트 수신 |
| [ch08-chatbot/](ch08-chatbot/) | 8장 | 챗봇 뼈대(bot_core) + 에코봇·명령형·LLM 처리기 |
| [ch09-projects/](ch09-projects/) | 9장 | 모니터링 알림봇, 일일 리포트 봇, FAQ 챗봇 |
| [ch10-plugins/](ch10-plugins/) | 10장 | Go 서버 플러그인 2종, 웹앱 플러그인, LeftRail 안내 |
| [appendix/](appendix/) | 부록B | 백업 스크립트 |

## 공통 준비

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt

cp .env.example .env            # 값을 채운 뒤 셸에 로드해서 사용
```

각 파이썬 예제는 환경 변수로 서버 주소와 토큰을 받습니다. 필요한 변수는 [.env.example](.env.example)과 각 파일 상단 주석을 참고하세요.

> 챕터 폴더는 서로 독립적으로 실행되도록 공용 모듈(`mm_client.py`, `bot_core.py`)을 폴더마다 복사해 두었습니다. 원본 정의는 각각 7-2절, 8-2절입니다.

## 안내

- 이 저장소의 토큰·URL·회사명은 모두 예시 값입니다. 실제 토큰을 코드나 커밋에 넣지 마세요 (책 7-1절의 토큰 관리 원칙 참조).
- 실습 순서와 상세 설명은 책 본문을 따라 진행하는 것을 전제로 합니다.
