// 10-2절: Hello World 플러그인 — ServeHTTP 훅만 구현한 최소 서버 플러그인
package main

import (
	"fmt"
	"net/http"

	"github.com/mattermost/mattermost/server/public/plugin"
)

// Plugin 구조체 — plugin.MattermostPlugin을 품으면
// p.API로 서버 기능에 접근할 수 있는 플러그인이 됩니다.
type Plugin struct {
	plugin.MattermostPlugin
}

// ServeHTTP 훅 — /plugins/<플러그인id> 주소로 오는 HTTP 요청을 처리합니다.
func (p *Plugin) ServeHTTP(c *plugin.Context, w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Hello, world! 첫 플러그인이 응답했습니다.")
}

func main() {
	plugin.ClientMain(&Plugin{})
}
