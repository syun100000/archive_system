# ベースイメージを指定
FROM ubuntu:24.04

# 必要なライブラリをインストール
RUN apt-get update && \
    apt-get install -y apache2 python3 python3-venv pkg-config locales libmysqlclient-dev libapache2-mod-wsgi-py3 build-essential libffi-dev python3-dev mysql-client && \
    tesseract-ocr \
    tesseract-ocr-jpn \
    rm -rf /var/lib/apt/lists/*

# ロケールを設定
RUN locale-gen ja_JP.UTF-8

# Apacheの設定ファイルを有効化
RUN a2enmod wsgi

# 作業ディレクトリを設定
WORKDIR /app

# ソースコードをコピー
COPY . /app/

# 仮想環境を作成
RUN python3 -m venv /opt/venv

# 仮想環境のpipで依存関係をインストール
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# 環境変数を設定（仮想環境のパスを優先）
ENV PATH="/opt/venv/bin:$PATH"
ENV ENVIRONMENT="docker"
ENV DJANGO_SETTINGS_MODULE="archive_system.settings_docker"
# Apacheの設定ファイルをコピー
COPY ./docker_config/apache/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./docker_config/apache/apache2.conf /etc/apache2/apache2.conf
COPY ./docker_config/apache/envvars /etc/apache2/envvars
# wsgi.pyのコピー（wsgi.py.sampleから生成）
COPY archive_system/wsgi.py.sample /app/archive_system/wsgi.py

# エントリーポイントスクリプトをコピー
COPY ./docker_config/docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# メディアディレクトリを作成
RUN mkdir -p /app/media

# ポートを公開
EXPOSE 80

# サーバー起動コマンドをエントリーポイントに設定
CMD ["/app/entrypoint.sh"]