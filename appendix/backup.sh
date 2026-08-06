#!/bin/bash
# 부록B: Mattermost 백업 스크립트 — DB 덤프 + 파일 데이터 아카이브
# 공식 docker compose 구성(mattermost/docker) 디렉터리에서 실행하는 것을 전제로 합니다.
# cron 등록 예: 0 3 * * * cd /opt/docker && /opt/docker/backup.sh >> /var/log/mm-backup.log 2>&1
set -e

BACKUP_DIR=/backup/mattermost
STAMP=$(date +%Y%m%d_%H%M%S)
COMPOSE="docker compose -f docker-compose.yml -f docker-compose.without-nginx.yml"

mkdir -p "$BACKUP_DIR"

# 1. DB 덤프 (서비스 중단 없이 가능) — 사용자/DB 이름은 .env 값과 맞추세요
$COMPOSE exec -T postgres pg_dump -U mmuser mattermost \
  | gzip > "$BACKUP_DIR/db_$STAMP.sql.gz"

# 2. 파일 데이터 아카이브 (설정 + 업로드 파일 + 플러그인)
tar czf "$BACKUP_DIR/files_$STAMP.tar.gz" ./volumes/app/mattermost

# 3. 30일 지난 백업 정리
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete

echo "백업 완료: $STAMP"

# (선택) 9-1절 웹훅으로 성공 알림 — MM_WEBHOOK_URL 환경 변수 설정 시
# curl -s -X POST -H 'Content-Type: application/json' \
#   -d "{\"username\": \"모니터링봇\", \"text\": \"백업 완료: $STAMP\"}" "$MM_WEBHOOK_URL"
