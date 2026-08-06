// 10-3절: 보안 지킴이 플러그인 — 게시 전 개입(금칙어 차단·주민번호 마스킹) + 슬래시 커맨드
package main

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/mattermost/mattermost/server/public/model"
	"github.com/mattermost/mattermost/server/public/plugin"
)

type GuardPlugin struct {
	plugin.MattermostPlugin
}

// 금칙어 목록 — 실무라면 플러그인 설정이나 KV 저장소로 관리합니다
var bannedWords = []string{"프로젝트X", "사내비밀"}

// 주민등록번호 패턴 (앞 6자리-뒤 7자리)
var rrnPattern = regexp.MustCompile(`\d{6}-\d{7}`)

// 훅 1: OnActivate — 활성화 시 슬래시 커맨드를 등록합니다.
func (p *GuardPlugin) OnActivate() error {
	return p.API.RegisterCommand(&model.Command{
		Trigger:          "보안규칙",
		AutoComplete:     true,
		AutoCompleteDesc: "적용 중인 보안 규칙을 보여줍니다",
		DisplayName:      "보안 규칙 안내",
	})
}

// 훅 2: MessageWillBePosted — 게시 직전에 호출됩니다.
// 반환값: (수정된 게시물, 거부 사유) — 사유가 있으면 게시가 차단됩니다.
func (p *GuardPlugin) MessageWillBePosted(c *plugin.Context, post *model.Post) (*model.Post, string) {
	// 기능 1: 금칙어 차단
	for _, w := range bannedWords {
		if strings.Contains(post.Message, w) {
			return nil, fmt.Sprintf("보안 정책 위반: '%s'는 채널에 게시할 수 없는 단어입니다.", w)
		}
	}

	// 기능 2: 주민등록번호 마스킹 후 게시 허용
	if rrnPattern.MatchString(post.Message) {
		post.Message = rrnPattern.ReplaceAllStringFunc(post.Message, func(s string) string {
			return s[:6] + "-*******"
		})
	}
	return post, ""
}

// 훅 3: ExecuteCommand — /보안규칙 처리. 외부 서버가 필요 없습니다.
func (p *GuardPlugin) ExecuteCommand(c *plugin.Context, args *model.CommandArgs) (*model.CommandResponse, *model.AppError) {
	text := fmt.Sprintf(
		"#### 현재 보안 규칙\n- 금칙어 차단: %s\n- 주민등록번호 자동 마스킹",
		strings.Join(bannedWords, ", "),
	)
	return &model.CommandResponse{
		ResponseType: model.CommandResponseTypeEphemeral, // 6-2절의 '나에게만 보이기'
		Text:         text,
	}, nil
}

func main() {
	plugin.ClientMain(&GuardPlugin{})
}
