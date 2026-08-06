# 10-4절: 사내 포털 웹앱 플러그인

`registerProduct`로 제품 전환 메뉴에 항목을 추가하고, 메인 패널에 사내 웹 서비스를 iframe으로 표시하는 **웹앱 전용 플러그인**입니다 (Go 서버 컴포넌트 없음).

## 커스터마이징

| 바꿀 것 | 위치 |
|---|---|
| 표시할 URL | `webapp/src/components/portal_view.tsx`의 `PORTAL_URL` |
| 메뉴 이름 | `webapp/src/index.tsx`의 `'사내 포털'` |
| 라우트 | `webapp/src/index.tsx`의 `PORTAL_ROUTE` (팀 슬러그와 충돌 금지) |
| 플러그인 id | `plugin.json` + `webapp/src/manifest.ts` **동시 변경** |

## 빌드·번들

```bash
cd webapp
npm install
npm run build                      # → webapp/dist/main.js

cd ..
mkdir -p build/com.example.portal/webapp/dist
cp plugin.json build/com.example.portal/
cp webapp/dist/main.js build/com.example.portal/webapp/dist/
cd build && tar -czf com.example.portal-0.1.0.tar.gz com.example.portal
```

시스템 콘솔 → 플러그인 관리에서 업로드 후 **활성화** → 웹앱 새로고침.

## 주의

- 임베드 대상이 `X-Frame-Options`/CSP `frame-ancestors`로 iframe을 차단하면 빈 화면이 됩니다 (책 10-4절).
- `registerProduct`는 본체의 INTERNAL API입니다 — 서버 메이저 업그레이드 후 동작 확인 필요.
- 안 보일 때의 4단계 진단은 책 10-4절 표 참조 (`window.plugins` → `/api/v4/plugins/webapp` → Network).
