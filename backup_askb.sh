#!/usr/bin/env bash
set -euo pipefail

# assumes we are in the project root
DB=db/data/bot.db
LOCAL=$HOME/backups
REMOTE=gdrive:askb-backups

STAMP=$(date +%F_%H%M)
FILE="$LOCAL/bot-$STAMP.db"

mkdir -p "$LOCAL"
sqlite3 "$DB" ".backup '$FILE'"
gzip "$FILE"

# every backup goes in daily/
rclone copy "$FILE.gz" "$REMOTE/daily"

# on the 1st of the month, also keep a copy in monthly/
if [ "$(date +%d)" = "01" ]; then
    rclone copy "$FILE.gz" "$REMOTE/monthly"
fi

# prune: local 7 days, Drive daily 14 days, Drive monthly 6 months
find "$LOCAL" -name "bot-*.db.gz" -mtime +7 -delete
rclone delete "$REMOTE/daily" --min-age 14d
rclone delete "$REMOTE/monthly" --min-age 180d
rclone cleanup gdrive:    # empties the Drive trash so deleted files stop using space
