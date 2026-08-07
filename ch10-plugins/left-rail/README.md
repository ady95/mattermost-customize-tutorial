# 10-6절: Slack 스타일 좌측 메뉴(LeftRail) — 웹앱 소스 수정

이 항목은 플러그인이 아니라 **Mattermost 웹앱 소스 수정** 방식이므로, 독립 실행 코드가 아닌 변경 명세를 제공합니다. 반드시 책 10-6절과 함께 보세요.

## 변경 파일 6개

| 파일 (webapp/channels/src/ 기준) | 구분 | 역할 |
|---|---|---|
| components/left_rail/left_rail.tsx | 신규 | 레일 컨테이너 — 고정 항목 + 제품 구역 + 하단 관리자 |
| components/left_rail/left_rail_item.tsx | 신규 | 공통 항목 (라우트형 Link / 액션형 button, 활성 표시) |
| components/left_rail/left_rail_products.tsx | 신규 | `useProducts()`로 등록된 제품 렌더링 — 10-4 플러그인 자동 표시 |
| components/left_rail/left_rail.scss | 신규 | 폭 68px, 테마 변수만 사용 |
| components/root/root.tsx | 수정 | `<LeftRail/>` 렌더링 추가 |
| sass/base/_structure.scss | 수정 | 루트 그리드에 `left-rail` 열 추가 |

핵심 레이아웃 변경 한 줄:

```scss
grid-template-areas: "left-rail team-sidebar main app-sidebar";
```

## 레일 항목 구성

홈(`/`) · 스레드(`/{팀}/threads`) · 내 활동(`showMentions` RHS 토글) · 나중에(`showFlaggedPosts` RHS 토글) · ―구분선― · 제품들(useProducts) · 관리자(`/admin_console`, 권한자만)

## 적용 절차

1. 운영 서버와 **같은 버전 태그**의 mattermost 소스 checkout (버전 불일치 금지 — 책 10-5절 0단계)
2. 위 6개 파일 변경 적용 (patch로 관리 권장)
3. `cd webapp && npm install && make package` → `mattermost-webapp.tar.gz`
4. 운영 서버에서 `client/`로 해제 + `chown -R 2000:2000` + docker compose 볼륨 `./client:/mattermost/client` 추가 (`:ro` 금지)
5. 롤백: 볼륨 한 줄 제거 후 `up -d`

## 유지보수 주의

- root.tsx, _structure.scss는 업스트림 변경이 잦습니다 — 서버 업그레이드마다 `git apply --3way`로 patch 재적용
- 웹앱 디렉터리는 Apache v2.0 라이선스입니다 (책 1-2절·10-6절)
