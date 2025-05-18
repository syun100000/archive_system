# Dockerを使用したデプロイ方法

## 前提条件
- Dockerがインストールされていること
- Docker Composeがインストールされていること
### Dockerがインストールされているか確認する方法
下記を実行して、Dockerがインストールされているか確認します。
- もしインストールされていない場合は、[Dockerのインストール](https://docs.docker.com/get-docker/)を参照してください。
 - Linuxにインストールする場合はGUIのないDockerのインストールをお勧めします。
#### Windows

以下のコマンドを `cmd` または `PowerShell` で実行して、DockerとDocker Composeがインストールされているか確認します。

```sh
docker --version
docker-compose --version
```

#### macOS

以下のコマンドをターミナルで実行して、DockerとDocker Composeがインストールされているか確認します。

```sh
docker --version
docker-compose --version
```

#### Ubuntu(Linux)

以下のコマンドをターミナルで実行して、DockerとDocker Composeがインストールされているか確認します。

```sh
docker --version
docker-compose --version
```

## 手順

1. このリポジトリをクローンします．
- すでにクローンしている場合や,[環境構築](../doc/install.md)を行った場合はこの手順は不要です．
   ```sh
   git clone https://github.com/syun100000/archive_system_django.git
    ```

1. クローンしたディレクトリに移動します．
    ```sh
    cd archive_system_django
    ```
2. shファイルを実行します．
    test_docker_build.shもしくはprod_docker_build.shを実行してください．
    - test_docker_build.shはアプリケーションを8000ポートで起動します．
    - prod_docker_build.shはアプリケーションを80ポートで起動します．

        **例: test_docker_build.shを実行する場合**
        ```sh
        sh test_docker_build.sh
        ``` 
        **例: prod_docker_build.shを実行する場合**
        ```sh
        sh prod_docker_build.sh
        ```

3. ブラウザで `http://localhost:8000` もしくは `http://localhost` にアクセスし、アプリが正しく動作していることを確認してください。
これで、Dockerを使用したデプロイ方法の手順は完了です。

## Docker Composeのコマンド
### Dockerコンテナの起動
- Dockerコンテナを起動するには以下のコマンドを使用します。
    ```sh
    docker-compose up -d
    ```

### Dockerコンテナの停止
- Dockerコンテナを停止するには以下のコマンドを使用します。
    ```sh
    docker-compose down
    ```

### Dockerコンテナの再起動
- Dockerコンテナを再起動するには以下のコマンドを使用します。
    ```sh
    docker-compose up -d
    ```

## トラブルシューティング
### ログの確認
- ログを確認するには以下のコマンドを使用します。
    ```sh
    docker-compose logs
    ```
- 特定のサービスのログを確認するには以下のコマンドを使用します。
    ```sh
    docker-compose logs [サービス名]
    ```
- ログをリアルタイムで確認するには以下のコマンドを使用します。
    ```sh
    docker-compose logs -f
    ```
- 特定のサービスのログをリアルタイムで確認するには以下のコマンドを使用します。
    ```sh
    docker-compose logs -f [サービス名]
    ```

### コマンドラインでのパスワードのリセット方法

1. まず，ドッカーなどのリセットしたいシステムのSHELLに入ります。

    ```sh
    docker-compose exec web sh
    ```
2. 仮想環境に入ります。

    ```sh
    source /opt/venv/bin/activate
    ```

3. `reset_password.py`を実行し画面の指示に従う。

    ```sh
    python reset_password.py
    ```

これで、パスワードのリセットが完了です。


## 不要なDockerリソースのクリーンアップ

 - 使用していないDockerリソースをクリーンアップするには、以下のコマンドを使用します。

    ```sh
    docker system prune -a
    ```

    このコマンドは、未使用のすべてのデータ（停止したコンテナ、未使用のネットワーク、未使用のボリューム、未使用のイメージ）を削除します。

