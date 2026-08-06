# 10-2절: Hello World 플러그인

빌드·번들 절차 (자세한 설명은 책 10-2절):

```bash
go mod tidy                                       # 의존성 정리 (go.sum 생성)
GOOS=linux GOARCH=amd64 go build -o plugin.exe plugin.go
tar -czvf hello-plugin.tar.gz plugin.exe plugin.json
```

- Windows PowerShell: `$env:GOOS="linux"; $env:GOARCH="amd64"; go build -o plugin.exe plugin.go`
- 시스템 콘솔 → 플러그인 관리에서 tar.gz 업로드 후 **활성화**
- 확인: `http://localhost:8065/plugins/com.example.hello-world`
- 사전 조건: config.json의 `PluginSettings.EnableUploads: true` + 서버 재시작 (10-2절 실습 1)
