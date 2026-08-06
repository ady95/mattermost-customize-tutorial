# 10-3절: 보안 지킴이 플러그인

- 금칙어 포함 메시지 **게시 차단** (MessageWillBePosted)
- 주민등록번호 자동 마스킹
- `/보안규칙` 슬래시 커맨드 (외부 서버 불필요)

```bash
go mod tidy
GOOS=linux GOARCH=amd64 go build -o plugin.exe plugin.go
tar -czvf guard-plugin.tar.gz plugin.exe plugin.json
```

시스템 콘솔 → 플러그인 관리에서 업로드 후 활성화. 시험 방법은 책 10-3절 실습 3 참조.
