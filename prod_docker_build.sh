# 本番環境用 80ポートで起動
# 必ず正しいパスで実行すること
# mediaディレクトリを作成
mkdir -p media

# コンテナを停止する
docker-compose -f prod-docker-compose.yml down

# イメージをビルド
docker-compose -f prod-docker-compose.yml build

# コンテナを起動する
docker-compose -f prod-docker-compose.yml up -d


