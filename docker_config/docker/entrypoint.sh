#!/bin/sh
# このスクリプトは、コンテナが起動するときに実行される
echo "Starting entrypoint.sh"

set -e

# データベースが起動するまで待機
echo "Waiting for MySQL..."
while ! mysqladmin ping -h "db1" --silent; do
    sleep 1
done

echo "MySQL is up - executing command"

# マイグレーションを実行
echo "Running migrations"
python manage.py migrate
echo "Migrations complete"

# 静的ファイルを収集
echo "Collecting static files"
python manage.py collectstatic --noinput
echo "Static files collected"

# メディアファイルのパーミッションを変更
chmod -R 777 /app/media
# configのパーミッションを変更
chmod -R 777 /app/archive_system/config
# Apacheをフォアグラウンドで起動
echo "Starting Apache"
apache2ctl -D FOREGROUND
echo "Apache started"
