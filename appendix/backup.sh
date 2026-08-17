#!/bin/bash
# 부록B: Mattermost 백업 스크립트 — DB 덤프 + 파일 데이터 아카이브
#
# 중요: 정합성 있는 백업을 위해 백업 동안 Mattermost 애플리케이션을 중지합니다
#       (공식 배포 문서 권장). postgres는 pg_dump를 위해 켜 둡니다.
#       중단 시간은 보통 1분 안팎이므로 사용량이 적은 새벽에 실행하세요.
#
# 공식 docker compose 구성(mattermost/docker) 디렉터리에서 실행하는 것을 전제로 합니다.
# cron 등록 예: 0 3 * * * cd /opt/docker && /opt/docker/backup.sh >> /var/log/mm-backup.log 2>&1
set -e

BACKUP_DIR=/backup/mattermost
STAMP=$(date +%Y%m%d_%H%M%S)
COMPOSE="docker compose -f docker-compose.yml -f docker-compose.without-nginx.yml"

mkdir -p "$BACKUP_DIR"

# 스크립트가 중간에 실패해도 서버는 반드시 다시 올린다 (핵심 안전장치)
trap '$COMPOSE start mattermost' EXIT

# 1. Mattermost 애플리케이션 중지 — DB와 파일의 시점을 일치시키기 위해
$COMPOSE stop mattermost

# 2. DB 덤프 — 사용자/DB 이름은 .env 값과 맞추세요
$COMPOSE exec -T postgres pg_dump -U mmuser mattermost \
  | gzip > "$BACKUP_DIR/db_$STAMP.sql.gz"

# 3. 파일 데이터 아카이브 (설정 + 업로드 파일 + 플러그인)
tar czf "$BACKUP_DIR/files_$STAMP.tar.gz" ./volumes/app/mattermost

# 4. 애플리케이션 재기동
$COMPOSE start mattermost
trap - EXIT

# 5. 30일 지난 백업 정리
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete

echo "백업 완료: $STAMP"

# (선택) 9-1절 웹훅으로 성공 알림 — MM_WEBHOOK_URL 환경 변수 설정 시
# curl -s -X POST -H 'Content-Type: application/json' \
#   -d "{\"username\": \"모니터링봇\", \"text\": \"백업 완료: $STAMP\"}" "$MM_WEBHOOK_URL"
